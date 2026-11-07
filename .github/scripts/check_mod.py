#!/usr/bin/env python3
"""
Check mods against a fresh game data export. Read-only.

    python .github/scripts/check_mod.py Agents_Individual_Item_Kits
    python .github/scripts/check_mod.py --all --summary
    python .github/scripts/check_mod.py Waste_Not --baseline C:/Users/finla/Desktop/data

Per mod it checks:
  refs     every {"RowName": ...} points at a row that exists in the game or in the mod
  props    every property the mod sets exists on that table's row struct
  assets   every /Game/... path exists in the export (or ships inside the mod)
  removed  rows the mod edits that the game has since deleted - the edit now creates a
           broken half-row (needs --baseline: an older export to compare against)
  dupes    two rows in one table whose names differ only by case (FName collision: one
           silently overwrites the other)
  release  EXMOD, modinfo.json and the shipped .EXMODZ agree on the version, the bundle
           matches the files on disk, and the description is a single version

The export is a folder of <Category>/D_<Table>.json data tables plus
Icarus/Content/... asset JSONs, as written by FModel.

Exit code: 0 = clean, 1 = problems found, 2 = usage error.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_GAME = Path(r"D:\Fmod Exports for Icarus\Exports")
SKIP_DIRS = {"docs", "icons", "tools", "skills", "Guide's", "issue-attachments"}
# Metadata is on every row struct but never listed in Defaults
EXTRA_DEFAULTS = {"Metadata": {"RequiredFeatureLevel": {"RowName": "None", "DataTableName": "D_FeatureLevels"}}}
ASSET_RE = re.compile(r"/Game/[A-Za-z0-9_\-/ ]+")
STAT_KEY_RE = re.compile(r'^\(Value="([^"]+)"\)$')     # stat maps key their entries this way
STAT_NAME_RE = re.compile(r"_[-+]?%?$|_\+%$")           # ...and stat names end in _+, _%, _+% (other maps reuse the key form)

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass


def load_json(p: Path):
    return json.loads(Path(p).read_bytes().decode("utf-8-sig"))


def table_of(current_file: str) -> str:
    """'Items-D_ItemsStatic.json' -> 'D_ItemsStatic'"""
    return current_file.replace(".json", "").split("-")[-1]


class Game:
    def __init__(self, root: Path, with_assets: bool = True):
        self.root = Path(root)
        self.tables: dict[str, dict] = {}
        # data tables sit one or more folders deep (Items/Types/D_BuildingTypes.json);
        # the Icarus/ tree is the asset export, not data tables
        for cat in sorted(p for p in self.root.iterdir() if p.is_dir() and p.name != "Icarus"):
            for f in sorted(cat.rglob("D_*.json")):
                try:
                    d = load_json(f)
                except Exception:
                    continue
                if not isinstance(d, dict) or not isinstance(d.get("Rows"), list):
                    continue
                t = self.tables.setdefault(f.stem, {"defaults": {}, "rows": {}})
                if not t["defaults"] and isinstance(d.get("Defaults"), dict):
                    t["defaults"] = d["Defaults"]
                for r in d["Rows"]:
                    if isinstance(r, dict) and "Name" in r:
                        t["rows"][str(r["Name"]).lower()] = r
        self.assets: set[str] = set()
        if with_assets:
            content = self.root / "Icarus" / "Content"
            for dp, _dn, fn in os.walk(content):
                rel = os.path.relpath(dp, content).replace("\\", "/")
                pre = "/game/" if rel == "." else f"/game/{rel.lower()}/"
                for f in fn:
                    if f.endswith(".json"):
                        self.assets.add(pre + f[:-5].lower())
            # Fall back to the repo's older asset list only when the export has no assets.
            # Never mix them: the list still names assets later game updates deleted, so a
            # mix lets a dead icon path pass.
            ref = REPO / ".github" / "scripts" / "game_assets.json.gz"
            if not self.assets and ref.exists():
                for lst in json.load(gzip.open(ref)).get("assets", {}).values():
                    for a in lst:
                        self.assets.add("/game/" + a.lower())

    def has_row(self, table: str, name: str) -> bool:
        t = self.tables.get(table)
        return bool(t) and name.lower() in t["rows"]

    def vanilla_refs(self, table: str, dflt: dict) -> set[tuple[str, str]]:
        """(field, RowName) for every reference the game's own rows of this table make -
        including ones that dangle in vanilla (unreleased ammo in AllArrows, for example).
        Field-specific: the same name in a different field is a different reference."""
        t = self.tables[table]
        if "vanilla_refs" not in t:
            out: set[tuple[str, str]] = set()
            for r in t["rows"].values():
                refs: list = []
                walk_refs(r, dflt, "", refs)
                for path, rn, _rt in refs:
                    if rn:
                        out.add((norm_path(path), str(rn).lower()))
            t["vanilla_refs"] = out
        return t["vanilla_refs"]

    def vanilla_props(self, table: str, dflt: dict) -> set[str]:
        """Nested keys the game's own rows use but Defaults leaves out (for example
        Generated_Tags.ParentTags) - those are real properties, not mistakes."""
        t = self.tables[table]
        if "vanilla_props" not in t:
            seen: list[str] = []
            for r in t["rows"].values():
                walk_props(r, dflt, "", seen, True)
            t["vanilla_props"] = set(seen)
        return t["vanilla_props"]


def norm_path(path: str) -> str:
    """'TV_Bolts.AmmoTypes[7]' -> 'AmmoTypes[]' (row name and list indices dropped)"""
    p = re.sub(r"\[\d+\]", "[]", path)
    return p.split(".", 1)[1] if "." in p else p


def walk_refs(val, dflt, path, out):
    if isinstance(val, dict):
        if "RowName" in val:
            tbl = val.get("DataTableName")
            if not tbl and isinstance(dflt, dict):
                tbl = dflt.get("DataTableName")
            out.append((path, val.get("RowName"), tbl))
        for k, v in val.items():
            if k in ("RowName", "DataTableName"):
                continue
            walk_refs(v, dflt.get(k) if isinstance(dflt, dict) else None, f"{path}.{k}", out)
    elif isinstance(val, list):
        tmpl = dflt[0] if isinstance(dflt, list) and dflt else None
        for i, v in enumerate(val):
            walk_refs(v, tmpl, f"{path}[{i}]", out)


def walk_props(val: dict, dflt: dict, path: str, out: list, top: bool):
    for k, v in val.items():
        if top and k == "Name":
            continue
        if k not in dflt:
            out.append(path + k)
            continue
        d = dflt[k]
        # a non-empty dict default is a struct; an empty one is a map (keys are data)
        if isinstance(v, dict) and isinstance(d, dict) and d and "RowName" not in d:
            walk_props(v, d, f"{path}{k}.", out, False)
        elif isinstance(v, list) and isinstance(d, list) and d and isinstance(d[0], dict) and "RowName" not in d[0]:
            for e in v:
                if isinstance(e, dict):
                    walk_props(e, d[0], f"{path}{k}[].", out, False)


def walk_stat_keys(val, path, out):
    """Every stat-map key ((Value="Stat")) anywhere in a row, with where it sits."""
    if isinstance(val, dict):
        for k, v in val.items():
            m = STAT_KEY_RE.match(k)
            if m:
                out.append((f"{path}.{k}", m.group(1)))
            walk_stat_keys(v, f"{path}.{k}" if not m else path, out)
    elif isinstance(val, list):
        for i, v in enumerate(val):
            walk_stat_keys(v, f"{path}[{i}]", out)


def mod_folders(names: list[str]) -> list[Path]:
    out = []
    for d in sorted(REPO.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in SKIP_DIRS:
            continue
        if (d / f"{d.name}.EXMOD").exists() and (not names or d.name in names):
            out.append(d)
    return out


def own_asset_names(mod_dir: Path) -> set[str]:
    names = set()
    for p in mod_dir.rglob("*"):
        if p.suffix.lower() in (".uasset", ".umap"):
            names.add(p.stem.lower())
    for z in mod_dir.glob("*.EXMODZ"):
        try:
            for n in zipfile.ZipFile(z).namelist():
                if n.lower().endswith((".uasset", ".umap")):
                    names.add(Path(n).stem.lower())
        except Exception:
            pass
    return names


def check_release(mod_dir: Path, exmod: dict, catalog: dict) -> list[str]:
    issues = []
    ver = exmod.get("version")
    name = mod_dir.name
    entry = None
    for e in catalog.get("mods", []):
        url = (e.get("files") or {}).get("exmodz", "")
        if f"/main/{name}/" in url:
            entry = e
            break
    if entry is None:
        issues.append("not listed in modinfo.json")
    elif entry.get("version") != ver:
        issues.append(f"modinfo.json says {entry.get('version')}, EXMOD says {ver}")
    zips = sorted(mod_dir.glob("*.EXMODZ"))
    if not zips:
        issues.append("no .EXMODZ bundle")
    else:
        z = zipfile.ZipFile(zips[0])
        stale = []
        for info in z.infolist():
            if info.is_dir():
                continue
            head, _, rest = info.filename.partition("/")
            src = mod_dir / rest if head in ("Extracted Mods", name) and rest else mod_dir / info.filename
            if src.exists() and src.read_bytes() != z.read(info.filename):
                stale.append(info.filename)
            if info.filename.upper().endswith(".EXMOD"):
                try:
                    zv = json.loads(z.read(info.filename).decode("utf-8-sig")).get("version")
                    if zv != ver:
                        issues.append(f"shipped .EXMODZ contains version {zv}, EXMOD says {ver}")
                except Exception as e:
                    issues.append(f"EXMOD inside the bundle does not parse: {e}")
        if stale:
            issues.append("bundle is stale (re-run repack_exmodz.py): " + ", ".join(stale))
    desc = exmod.get("description") or ""
    if "\n" in desc:
        issues.append("EXMOD description has line breaks (keep it to one version, one line)")
    vers = set(VERSION_RE.findall(desc))
    if len(vers) > 1:
        issues.append(f"EXMOD description mentions several versions {sorted(vers)} - the Mod Manager downloader wants one")
    if entry is not None:
        stale = sorted(set(VERSION_RE.findall(entry.get("description") or "")) - {ver})
        if stale:
            issues.append(f"modinfo.json description still mentions older version(s) {stale}")
    issues += check_docs(mod_dir, ver)
    return issues


VERSION_RE = re.compile(r"(?:^|\s|\()[vV](?:er\.?\s*)?(\d+(?:\.\d+)+)")


def check_docs(mod_dir: Path, ver: str) -> list[str]:
    """README.md, the .txt readme and the root README all say the current version."""
    issues = []
    v = re.escape(str(ver))
    md = mod_dir / "README.md"
    if not md.exists():
        issues.append("no README.md")
    else:
        t = md.read_text(encoding="utf-8", errors="replace")
        if not re.search(rf"badge/v{v}-Version", t):
            issues.append(f"README.md version badge is not v{ver}")
        # accepted entry styles: "### v1.2", "## What's New in v1.2", "| 1.2 |", "- **v1.2** - ..."
        entry_re = (rf"(^#{{2,4}}[^\n]*\bv?{v}\b)|(^\|\s*v?{v}\s*\|)|(^\s*[-*]\s*\*\*v?{v}\*\*)"
                    rf"|(\*\*v{v}\b)")
        if not re.search(entry_re, t, re.M):
            issues.append(f"README.md has no changelog entry for {ver}")
    txts = sorted(mod_dir.glob("Readme (*.txt"))
    if not txts:
        issues.append("no Readme (*_P.pak).txt")
    for txt in txts:
        t = txt.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^Mod Version:\s*(\S+)", t, re.M)
        if not m or m.group(1) != str(ver):
            issues.append(f"{txt.name} says Mod Version {m.group(1) if m else '(none)'}, EXMOD says {ver}")
        # "Ver 2.3" headings, or the indented "  v2.1 - ..." list some mods use
        if not re.search(rf"^Ver\s+{v}\b|^\s*v{v}\s*[-:]", t, re.M):
            issues.append(f"{txt.name} has no 'Ver {ver}' changelog entry")
    root = (REPO / "README.md").read_text(encoding="utf-8", errors="replace")
    m = re.search(rf"\]\({re.escape(mod_dir.name)}\)\s*\|\s*`([^`]*)`", root)
    if not m:
        issues.append("no row in the root README.md")
    elif m.group(1) != str(ver):
        issues.append(f"root README.md row says {m.group(1)}, EXMOD says {ver}")
    return issues


def check_mod(mod_dir: Path, game: Game, base: Game | None, catalog: dict) -> dict:
    exmod = load_json(mod_dir / f"{mod_dir.name}.EXMOD")
    blocks = []
    for b in exmod.get("Rows") or []:
        cf = b.get("CurrentFile", "")
        if cf:
            blocks.append((cf, table_of(cf), b.get("File_Items") or []))
    mod_rows = defaultdict(set)
    for _cf, tbl, items in blocks:
        for r in items:
            if isinstance(r, dict) and "Name" in r:
                mod_rows[tbl].add(str(r["Name"]).lower())
    own_assets = own_asset_names(mod_dir)

    stats = set(game.tables.get("D_Stats", {}).get("rows", {}))
    res = {"mod": mod_dir.name, "version": exmod.get("version"), "rows": 0, "edited": 0, "added": 0,
           "refs": [], "refs_inherited": 0, "props": [], "assets": [], "removed": [], "dupes": [], "stats": [],
           "tables_missing": [], "release": check_release(mod_dir, exmod, catalog)}
    for cf, tbl, items in blocks:
        gt = game.tables.get(tbl)
        if gt is None:
            res["tables_missing"].append(cf)
            continue
        dflt = dict(gt["defaults"])
        for k, v in EXTRA_DEFAULTS.items():
            dflt.setdefault(k, v)
        seen = {}
        for r in items:
            if not isinstance(r, dict) or "Name" not in r:
                continue
            res["rows"] += 1
            nm = str(r["Name"])
            low = nm.lower()
            if low in seen and seen[low] != nm:
                res["dupes"].append(f"{cf}: {seen[low]} / {nm}")
            seen.setdefault(low, nm)
            vrow = gt["rows"].get(low)
            if vrow is not None:
                res["edited"] += 1
            else:
                res["added"] += 1
                if base is not None and base.has_row(tbl, nm):
                    res["removed"].append(f"{cf}: {nm}")
            # properties
            bad = []
            walk_props(r, dflt, "", bad, True)
            if bad:
                ok = game.vanilla_props(tbl, dflt)
                for b in bad:
                    if b not in ok:
                        res["props"].append(f"{cf}: {nm}.{b}")
            # references
            refs = []
            walk_refs(r, dflt, nm, refs)
            vtext = json.dumps(vrow).lower() if vrow is not None else ""
            for path, rn, rt in refs:
                if not rn or rn == "None" or not rt or rt == "None":
                    continue
                if game.has_row(rt, rn) or str(rn).lower() in mod_rows.get(rt, set()):
                    continue
                if rt not in game.tables:
                    res["refs"].append(f"{cf}: {path} -> {rt}.{rn} (table {rt} not in the game)")
                    continue
                if (vtext and f'"{str(rn).lower()}"' in vtext) or \
                        (norm_path(path), str(rn).lower()) in game.vanilla_refs(tbl, dflt):
                    res["refs_inherited"] += 1          # the game's own rows carry the same dangling ref
                    continue
                note = ""
                if base is not None and base.has_row(rt, rn):
                    note = "  [removed by a game update]"
                res["refs"].append(f"{cf}: {path} -> {rt}.{rn}{note}")
            # stat names used as stat-map keys
            if stats:
                sk = []
                walk_stat_keys(r, nm, sk)
                for where, stat in sk:
                    if STAT_NAME_RE.search(stat) and stat.lower() not in stats:
                        res["stats"].append(f"{cf}: {where} -> stat '{stat}' is not in D_Stats (the game ignores it)")
            # asset paths
            if game.assets:
                for m in ASSET_RE.findall(json.dumps(r)):
                    p = m.rstrip("/ ").lower()
                    if p.endswith("_c") and p[:-2] in game.assets:
                        continue
                    if p in game.assets or p.rsplit("/", 1)[-1] in own_assets:
                        continue
                    if p.endswith("_c") and p[:-2].rsplit("/", 1)[-1] in own_assets:
                        continue
                    res["assets"].append(f"{cf}: {nm} -> {m}")
    res["problems"] = (len(res["refs"]) + len(res["props"]) + len(res["assets"]) + len(res["removed"])
                       + len(res["dupes"]) + len(res["tables_missing"]) + len(res["release"]) + len(res["stats"]))
    return res


def report(res: dict, full: bool) -> None:
    lim = None if full else 12
    print(f"\n=== {res['mod']}  v{res['version']}  ({res['rows']} rows: {res['edited']} edited, {res['added']} added)")
    for key, label in (("release", "release"), ("tables_missing", "table not in game"), ("refs", "broken ref"),
                       ("props", "unknown property"), ("stats", "unknown stat"), ("assets", "missing asset"),
                       ("removed", "row deleted from the game"), ("dupes", "case-duplicate rows")):
        items = res[key]
        if not items:
            continue
        print(f"  {label}: {len(items)}")
        for it in items[:lim]:
            print(f"     - {it}")
        if lim and len(items) > lim:
            print(f"     ... {len(items) - lim} more")
    if res["refs_inherited"]:
        print(f"  (ignored {res['refs_inherited']} dangling refs copied from the game's own rows)")
    if not res["problems"]:
        print("  OK")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mods", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--game", default=str(DEFAULT_GAME))
    ap.add_argument("--baseline", default=None, help="an older export, to spot rows the game deleted")
    ap.add_argument("--summary", action="store_true", help="one line per mod")
    ap.add_argument("--full", action="store_true", help="list every problem, not the first 12")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    if not a.mods and not a.all:
        ap.error("name one or more mod folders, or pass --all")
    dirs = mod_folders([] if a.all else a.mods)
    missing = set(a.mods) - {d.name for d in dirs}
    if missing:
        print(f"no such mod folder: {', '.join(sorted(missing))}", file=sys.stderr)
        return 2
    game = Game(Path(a.game))
    base = Game(Path(a.baseline), with_assets=False) if a.baseline else None
    catalog = load_json(REPO / "modinfo.json")
    results = [check_mod(d, game, base, catalog) for d in dirs]
    if a.summary:
        print(f"{'MOD':40} {'VER':8} {'REFS':>5} {'PROPS':>6} {'STATS':>6} {'ASSETS':>7} {'GONE':>5} {'DUPES':>6} RELEASE")
        for r in sorted(results, key=lambda r: -r["problems"]):
            rel = "; ".join(r["release"])[:90] or "ok"
            print(f"{r['mod']:40} {str(r['version']):8} {len(r['refs']):5} {len(r['props']):6} {len(r['stats']):6} "
                  f"{len(r['assets']):7} {len(r['removed']):5} {len(r['dupes']):6} {rel}")
    else:
        for r in results:
            report(r, a.full)
    if a.json:
        Path(a.json).write_text(json.dumps(results, indent=1), encoding="utf-8")
    return 1 if any(r["problems"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
