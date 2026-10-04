#!/usr/bin/env python3
"""
Repack a mod's .EXMODZ from the files in its folder.

An .EXMODZ is just a zip laid out as:

    Extracted Mods/<Name>.EXMOD      <- the data-table patch the Mod Manager reads
    <Name>/Banner.png
    <Name>/README.md
    <Name>/Readme (<Name>_P.pak).txt
    <Name>/...                       <- BP assets, .pak, extra docs

Editing a mod's .EXMOD or README in the repo does NOT change the .EXMODZ, and the
.EXMODZ is what users download and what the release workflow uploads. Run this after
editing a mod so the bundle matches its sources.

It works SURGICALLY: it opens the existing .EXMODZ and rewrites only those entries
whose file on disk differs, preserving every other entry byte-for-byte and keeping the
original entry order. That matters because a few bundles legitimately contain build
staging files (pak_build/, PAK_Build/) that are gitignored and so absent from the
working tree - regenerating from scratch would silently drop them.

Usage:
    python .github/scripts/repack_exmodz.py                 # check every mod, report drift
    python .github/scripts/repack_exmodz.py --write         # apply to every mod
    python .github/scripts/repack_exmodz.py Turret_Variants --write
    python .github/scripts/repack_exmodz.py --write --add-missing

Exit codes: 0 = nothing to do (or written), 1 = drift found in check mode, 2 = error.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKIP_DIRS = {"docs", "icons", "tools", "skills", "Guide's", ".github", ".git", ".vscode", ".claude"}

# Never pull these into a bundle that does not already contain them - they are
# authoring tools and build staging, not something a player needs.
NEVER_ADD_SUFFIXES = {".py", ".ps1", ".bat", ".sh"}
NEVER_ADD_DIRS = {"pak_build", "PAK_Build", "__pycache__"}

# Player-facing tools that DO ship in the bundle despite their suffix.
PLAYER_TOOL_DIRS = {"Restore_Kit_Research"}


def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def disk_path_for(entry: str, mod_dir: Path) -> Path | None:
    """Map a zip entry name back to the file it comes from in the mod folder."""
    if entry.endswith("/"):
        return None
    head, _, rest = entry.partition("/")
    if not rest:
        return mod_dir / entry
    # "Extracted Mods/X.EXMOD" and "<ModName>/..." both flatten into the mod folder
    if head in ("Extracted Mods", mod_dir.name):
        return mod_dir / rest
    return mod_dir / entry


def should_offer(rel: Path) -> bool:
    if rel.parts and rel.parts[0] in PLAYER_TOOL_DIRS:
        return True
    if rel.suffix.lower() in NEVER_ADD_SUFFIXES:
        return False
    return not any(part in NEVER_ADD_DIRS for part in rel.parts)


def process(mod_dir: Path, write: bool, add_missing: bool) -> tuple[int, list[str]]:
    zips = sorted(mod_dir.glob("*.EXMODZ"))
    if not zips:
        return 0, []
    ez = zips[0]

    with zipfile.ZipFile(ez) as z:
        infos = z.infolist()
        payload = {i.filename: z.read(i.filename) for i in infos if not i.is_dir()}

    changed: list[str] = []
    updated: dict[str, bytes] = {}
    for name, data in payload.items():
        src = disk_path_for(name, mod_dir)
        if src is None or not src.exists():
            continue  # keep bundle-only files (build staging) untouched
        fresh = src.read_bytes()
        if digest(fresh) != digest(data):
            updated[name] = fresh
            changed.append(name)

    # optionally pick up brand-new files (e.g. a newly added README)
    added: list[str] = []
    if add_missing:
        in_zip = set()
        for n in payload:
            p = disk_path_for(n, mod_dir)
            if p:
                in_zip.add(p.resolve())
        for p in sorted(mod_dir.rglob("*")):
            if not p.is_file() or p.suffix.upper() == ".EXMODZ":
                continue
            if p.resolve() in in_zip:
                continue
            rel = p.relative_to(mod_dir)
            if not should_offer(rel):
                continue
            entry = (f"Extracted Mods/{rel.as_posix()}" if p.suffix.upper() == ".EXMOD"
                     else f"{mod_dir.name}/{rel.as_posix()}")
            updated[entry] = p.read_bytes()
            added.append(entry)

    if not changed and not added:
        return 0, []

    if write:
        tmp = ez.with_suffix(".EXMODZ.tmp")
        with zipfile.ZipFile(ez) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                if info.is_dir():
                    continue
                data = updated.pop(info.filename, None)
                if data is None:
                    data = zin.read(info.filename)
                zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = info.external_attr
                zout.writestr(zi, data)
            for name, data in updated.items():  # anything newly added
                zout.writestr(name, data)
        shutil.move(str(tmp), str(ez))

    return len(changed) + len(added), changed + [f"(new) {a}" for a in added]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mods", nargs="*", help="mod folder names (default: all)")
    ap.add_argument("--write", action="store_true", help="apply changes (default: check only)")
    ap.add_argument("--add-missing", action="store_true",
                    help="also add files present in the folder but absent from the bundle")
    a = ap.parse_args()

    targets = []
    for d in sorted(REPO.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in SKIP_DIRS:
            continue
        if a.mods and d.name not in a.mods:
            continue
        targets.append(d)

    if a.mods:
        unknown = set(a.mods) - {d.name for d in targets}
        if unknown:
            print(f"error: no such mod folder: {', '.join(sorted(unknown))}", file=sys.stderr)
            return 2

    total = 0
    for d in targets:
        try:
            n, names = process(d, a.write, a.add_missing)
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR {d.name}: {type(e).__name__}: {e}", file=sys.stderr)
            return 2
        if n:
            total += n
            verb = "repacked" if a.write else "STALE"
            print(f"{verb:9} {d.name}  ({n} entr{'y' if n == 1 else 'ies'})")
            for x in names:
                print(f"            - {x}")

    if not total:
        print("All .EXMODZ bundles match their source files.")
        return 0
    if a.write:
        print(f"\nRepacked {total} entries. Commit the updated .EXMODZ files.")
        return 0
    print(f"\n{total} entries are stale. Re-run with --write to repack.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
