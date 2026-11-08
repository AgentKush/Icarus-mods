#!/usr/bin/env python3
"""
Draw each mod's two Mod Manager images from the mod's live data.

    icons/<Folder>.png    256x256  the Mod Manager's downloader icon (modinfo.json imageURL)
    <Folder>/Banner.png   768x256  the banner packed into the mod's .EXMODZ

Live data: name and author from modinfo.json; version and entry/table counts from the EXMOD;
category from docs/categories.json; tagline from icons/taglines.json. Each PNG stores the data
it was drawn from in a tEXt chunk named "icarus-mod-image", so `--check` (and check_mod.py)
can tell when an image no longer matches its mod - no Pillow or fonts needed for that.

Usage:
    python .github/scripts/mod_images.py Waste_Not            # redraw one mod's icon and banner
    python .github/scripts/mod_images.py --all                # redraw every mod
    python .github/scripts/mod_images.py --check [Mods...]    # list out-of-date images, exit 1 if any

Drawing needs Pillow + numpy and the Windows fonts the renderer uses (Bahnschrift).
After redrawing a banner, repack the mod so the .EXMODZ carries it:
    python .github/scripts/repack_exmodz.py <Folder> --write
"""
from __future__ import annotations

import json
import struct
import sys
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CHUNK = "icarus-mod-image"
RENDERER = "blueprint-1"          # bump when the renderer's look changes, so every image redraws
ICON_FIELDS = ("renderer", "folder", "name", "version", "category")   # what the icon shows (REV x.y)
BANNER_FIELDS = ("renderer", "folder", "name", "version", "entries", "tables", "category", "tagline", "author")


def _catalog() -> dict:
    out = {}
    for e in json.loads((REPO / "modinfo.json").read_text(encoding="utf-8"))["mods"]:
        folder = e["readmeURL"].split("/main/", 1)[1].split("/", 1)[0]
        out[folder] = e
    return out


def live_data(folder: str, catalog: dict | None = None) -> dict:
    """Everything the two images show, read from the mod's own files."""
    catalog = catalog or _catalog()
    e = catalog[folder]
    exmod = next((REPO / folder).glob("*.EXMOD"))
    x = json.loads(exmod.read_text(encoding="utf-8-sig"))
    cats = json.loads((REPO / "docs" / "categories.json").read_text(encoding="utf-8"))
    tags = json.loads((REPO / "icons" / "taglines.json").read_text(encoding="utf-8"))
    if folder not in tags:
        raise KeyError(f"{folder} has no tagline in icons/taglines.json")
    rows = x.get("Rows") or []
    return {"renderer": RENDERER, "folder": folder, "name": e["name"], "version": x["version"],
            "entries": sum(len(b.get("File_Items") or []) for b in rows), "tables": len(rows),
            "category": cats.get(folder, "Uncategorized"), "tagline": tags[folder], "author": e["author"]}


def icon_path(folder: str, catalog: dict | None = None) -> Path:
    e = (catalog or _catalog())[folder]
    return REPO / e["imageURL"].split("/main/", 1)[1]


def banner_path(folder: str) -> Path:
    return REPO / folder / "Banner.png"


def read_meta(png: Path) -> dict | None:
    """The tEXt chunk this script wrote, without needing Pillow."""
    try:
        b = png.read_bytes()
    except OSError:
        return None
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    i = 8
    while i + 8 <= len(b):
        n, kind = struct.unpack(">I4s", b[i:i + 8])
        data = b[i + 8:i + 8 + n]
        if kind == b"tEXt":
            key, _, val = data.partition(b"\0")
            if key.decode("latin-1") == CHUNK:
                try:
                    return json.loads(val.decode("latin-1"))
                except ValueError:
                    return None
        elif kind == b"iTXt":
            key, _, rest = data.partition(b"\0")
            if key.decode("latin-1") == CHUNK and len(rest) >= 2:
                comp, _method = rest[0], rest[1]
                rest = rest[2:].split(b"\0", 2)[-1]
                try:
                    return json.loads((zlib.decompress(rest) if comp else rest).decode("utf-8"))
                except (ValueError, zlib.error):
                    return None
        if kind == b"IEND":
            break
        i += 12 + n
    return None


def stale(folder: str, catalog: dict | None = None) -> list[str]:
    """Problems with a mod's images, as check_mod release issues ([] when both are current)."""
    catalog = catalog or _catalog()
    try:
        want = live_data(folder, catalog)
    except (KeyError, StopIteration, OSError, ValueError) as err:
        return [f"images: cannot read live data ({err})"]
    issues = []
    for label, path, fields in (("icon", icon_path(folder, catalog), ICON_FIELDS),
                                ("banner", banner_path(folder), BANNER_FIELDS)):
        have = read_meta(path)
        if have is None:
            issues.append(f"{label} was not drawn by mod_images.py (run: python .github/scripts/mod_images.py {folder})")
            continue
        diff = [f for f in fields if have.get(f) != want[f]]
        if diff:
            issues.append(f"{label} is out of date ({', '.join(diff)}) - run: python .github/scripts/mod_images.py {folder}")
    return issues


def draw(folders: list[str]) -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import mod_image_render as renderer              # Pillow + numpy + Windows fonts

    catalog = _catalog()
    for folder in folders:
        data = live_data(folder, catalog)
        mod = {k: data[k] for k in ("folder", "name", "version", "entries", "tables", "category", "tagline", "author")}
        ip, bp = icon_path(folder, catalog), banner_path(folder)
        # one render call writes both files; each is then stamped with the data it shows
        renderer.render(mod, str(ip), str(bp))
        _restamp(ip, {k: data[k] for k in ICON_FIELDS})
        _restamp(bp, {k: data[k] for k in BANNER_FIELDS})
        print(f"drew {folder}: {ip.relative_to(REPO)}, {bp.relative_to(REPO)}")


def _restamp(png: Path, meta: dict) -> None:
    """Rewrite the image's tEXt chunk with exactly `meta` (keys sorted, so bytes are stable)."""
    from PIL import Image, PngImagePlugin

    with Image.open(png) as im:
        im.load()
        info = PngImagePlugin.PngInfo()
        info.add_text(CHUNK, json.dumps(meta, sort_keys=True, ensure_ascii=True))
        im.save(png, pnginfo=info, optimize=True)


def main(argv: list[str]) -> int:
    catalog = _catalog()
    names = [a for a in argv if not a.startswith("--")]
    folders = sorted(catalog) if ("--all" in argv or not names) else names
    unknown = [f for f in folders if f not in catalog]
    if unknown:
        print("not in modinfo.json:", ", ".join(unknown))
        return 2
    if "--check" in argv:
        bad = 0
        for f in folders:
            for issue in stale(f, catalog):
                print(f"{f}: {issue}")
                bad += 1
        print(f"{len(folders)} mods checked, {bad} image problem(s)")
        return 1 if bad else 0
    if not names and "--all" not in argv:
        print(__doc__)
        return 2
    draw(folders)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
