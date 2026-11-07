#!/usr/bin/env python3
"""Rebuild docs/index.html from EXMOD files and categories.json."""

import json
import os
import re
import glob

REPO = "AgentKush/Icarus-mods"
BASE = f"https://github.com/{REPO}"
RAW = f"{BASE}/raw/main"


def main():
    # Load category mapping
    with open("docs/categories.json") as f:
        categories = json.load(f)

    # Card text: the catalog blurb from modinfo.json says what a mod does. The EXMOD
    # description is the latest version note, so it is only the fallback.
    blurbs = {}
    with open("modinfo.json", encoding="utf-8") as f:
        for entry in json.load(f).get("mods", []):
            m = re.search(r"/main/([^/]+)/", entry.get("readmeURL", ""))
            if m and entry.get("description"):
                blurbs[m.group(1)] = entry["description"]

    # Scan all mod folders for EXMOD files
    mods = []
    new_categories = False
    for folder in sorted(os.listdir(".")):
        if not os.path.isdir(folder) or folder.startswith("."):
            continue

        # Find any .EXMOD file in the folder (handles case mismatches)
        exmod_files = glob.glob(os.path.join(folder, "*.EXMOD"))
        if not exmod_files:
            continue
        exmod = exmod_files[0]

        try:
            with open(exmod) as f:
                data = json.load(f, strict=False)
        except json.JSONDecodeError:
            print(f"  SKIP (broken JSON): {exmod}")
            continue

        name = data.get("name", folder)
        version = data.get("version", "1.0")
        file_name = data.get("fileName", folder)

        # Get description - first paragraph only, clean for display
        desc = blurbs.get(folder) or data.get("description", "")
        desc = desc.split("\r\n\r\n\r\n")[0]
        desc = desc.replace("\r\n", " ").strip()
        if len(desc) > 200:
            desc = desc[:197] + "..."

        category = categories.get(folder, "Uncategorized")
        if folder not in categories:
            categories[folder] = "Uncategorized"
            new_categories = True
            print(f"  NEW MOD: {folder} (set to Uncategorized)")

        mods.append({
            "name": name,
            "folder": folder,
            "version": version,
            "description": desc,
            "category": category,
            "readme": f"{BASE}/tree/main/{folder}",
            "download": f"{RAW}/{folder}/{file_name}.EXMODZ",
            "release": f"{BASE}/releases/tag/{folder}-v{version}",
            "banner": f"{RAW}/{folder}/Banner.png" if os.path.exists(os.path.join(folder, "Banner.png")) else ""
        })

    # Update categories.json if new mods were found
    if new_categories:
        with open("docs/categories.json", "w") as f:
            json.dump(categories, f, indent=4, ensure_ascii=True)
            f.write("\n")

    # Calculate stats
    total_mods = len(mods)
    total_entries = 0
    total_recipes = 0
    for folder_name in os.listdir("."):
        if not os.path.isdir(folder_name) or folder_name.startswith("."):
            continue
        exmod_files = glob.glob(os.path.join(folder_name, "*.EXMOD"))
        if not exmod_files:
            continue
        try:
            with open(exmod_files[0]) as f:
                data = json.load(f, strict=False)
        except json.JSONDecodeError:
            continue
        for row in data.get("Rows", []):
            items = row.get("File_Items", [])
            total_entries += len(items)
            if "D_ProcessorRecipes" in row.get("CurrentFile", ""):
                total_recipes += len(items)

    # Read current index.html
    with open("docs/index.html") as f:
        html = f.read()

    # Replace MODS array in script.js (where the data actually lives)
    mods_json = json.dumps(mods, ensure_ascii=True, separators=(",", ": "))
    with open("docs/script.js") as f:
        js = f.read()
    js = re.sub(
        r"const MODS\s*=\s*\[.*?\];",
        lambda m: f"const MODS={mods_json};",
        js,
        flags=re.DOTALL
    )
    with open("docs/script.js", "w") as f:
        f.write(js)

    # Update hero animated stat counters (data-count drives the count-up)
    html = re.sub(r'(data-count=")\d+(">0</span><span class="label">Mods)', rf'\g<1>{total_mods}\g<2>', html)
    html = re.sub(r'(data-count=")\d+(">0</span><span class="label">Data Entries)', rf'\g<1>{total_entries}\g<2>', html)
    html = re.sub(r'(data-count=")\d+(">0</span><span class="label">Recipes)', rf'\g<1>{total_recipes}\g<2>', html)

    # Update mod-count references in meta / OG / Twitter / JSON-LD
    html = re.sub(r'\d+\+ Icarus survival game mods', f'{total_mods}+ Icarus survival game mods', html)
    html = re.sub(r'\d+\+ free mods', f'{total_mods}+ free mods', html)

    with open("docs/index.html", "w") as f:
        f.write(html)

    print(f"Site updated: {total_mods} mods, {total_entries:,} entries, {total_recipes:,} recipes")

    # Safety check: scan all site files for null bytes
    corrupted = []
    for pattern in ["docs/*.js", "docs/*.css", "docs/*.html"]:
        for path in glob.glob(pattern):
            with open(path, "rb") as f:
                if b"\x00" in f.read():
                    corrupted.append(path)
    if corrupted:
        print(f"\nERROR: Null bytes detected in: {', '.join(corrupted)}")
        print("This will break the site. Strip null bytes before deploying.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
