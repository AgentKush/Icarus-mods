#!/usr/bin/env python3
"""
Apply the verified structural fixes to the mod EXMODs.

Every fix here was checked against the current (Sept-2026) extracted game data before
being written down, and the reasoning is in the comment above each one. Run with
--check first to see what would change.

    python .github/scripts/apply_fixes.py --check
    python .github/scripts/apply_fixes.py --write
    python .github/scripts/apply_fixes.py --write No_Food_Spoilage

Afterwards, repack the bundles so the shipped .EXMODZ matches:

    python .github/scripts/repack_exmodz.py --write

NOTE ON ROW NAMES: Unreal resolves DataTable row handles through FName, which is
case-insensitive. Vanilla itself ships 80 references that differ from their target row
only by case (AntiPoison_Tonic -> Antipoison_Tonic, WaterBomb -> Waterbomb, ...), and
those items work in game. So a case-only mismatch is NOT a defect and is never "fixed"
here.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# The five multiplier speed mods and their target factor. FastProcessing_Instant is
# handled separately because "instant" is not a division.
SPEED_MODS = {
    "FastProcessing_All_5x": 5,
    "FastProcessing_All_10x": 10,
    "FastProcessing_All_15x": 15,
    "FastProcessing_All_25x": 25,
    "Faster_Crafting": 2,
}


# ── helpers ───────────────────────────────────────────────────────────────────

def load(mod: str) -> tuple[Path, dict]:
    p = REPO / mod / f"{mod}.EXMOD"
    return p, json.loads(p.read_text(encoding="utf-8-sig"))


def block(exmod: dict, table: str) -> list | None:
    """Return the File_Items list for the block whose CurrentFile names `table`."""
    for b in exmod.get("Rows") or []:
        if b.get("CurrentFile", "").replace(".json", "").split("-")[-1] == table:
            return b.setdefault("File_Items", [])
    return None


def drop_rows(items: list, names: set[str], log: list, why: str) -> None:
    keep = [r for r in items if r.get("Name") not in names]
    removed = sorted({r.get("Name") for r in items} & names)
    if removed:
        log.append(f"    removed {len(removed)} rows ({why}): {', '.join(removed)}")
    items[:] = keep


def drop_prop(items: list, prop: str, log: list, where: str) -> None:
    n = 0
    for r in items:
        if prop in r:
            del r[prop]
            n += 1
    if n:
        log.append(f"    deleted property '{prop}' from {n} {where} rows")


def drop_nested_prop(items: list, listkey: str, prop: str, log: list) -> None:
    n = 0
    for r in items:
        for e in r.get(listkey) or []:
            if isinstance(e, dict) and prop in e:
                del e[prop]
                n += 1
    if n:
        log.append(f"    deleted '{listkey}[].{prop}' ({n} occurrences)")


def repoint(items: list, rowname: str, path: str, old: str, new: str, log: list) -> None:
    """path is 'Inputs[0].Element' style, limited to what we need here."""
    for r in items:
        if r.get("Name") != rowname:
            continue
        listkey, _, field = path.partition("[0].")
        for e in r.get(listkey) or []:
            tgt = e.get(field) or {}
            if tgt.get("RowName") == old:
                tgt["RowName"] = new
                log.append(f"    {rowname}: {listkey}[].{field} {old} -> {new}")
                return
    log.append(f"    !! {rowname}: expected {old} at {path}, not found")


# ── the fixes ─────────────────────────────────────────────────────────────────

def fix_no_food_spoilage(x: dict, log: list) -> None:
    recipes = block(x, "D_ProcessorRecipes")
    decay = block(x, "D_Decayable")

    # Five Spoil_Raw_Meat_* rows point at item names that exist in no build. The mod
    # ALREADY ships correct recipes for the same five items (Spoil_Raw_Bacon,
    # Spoil_Soft_Meat, Spoil_White_Meat, Spoil_Stringy_Meat, Spoil_Gamey_Meat), so
    # repointing would give two composter recipes per item. Delete the broken twins.
    drop_rows(recipes, {
        "Spoil_Raw_Meat_Bacon", "Spoil_Raw_Meat_Soft", "Spoil_Raw_Meat_White",
        "Spoil_Raw_Meat_Stringy", "Spoil_Raw_Meat_Gamey",
    }, log, "duplicate of an already-correct recipe")

    # No item named Yam exists anywhere in either build; the comparable root crop
    # (Kumara) already has its own Spoil_Kumara row.
    drop_rows(recipes, {"Spoil_Yam"}, log, "no such item in any build")

    # Fish_15/16_Var3+Var4 never existed; Fish_17_Var3/Var4 were removed by the Sept
    # build. Fish_18/Fish_19 still have Var3/Var4, so those rows stay.
    drop_rows(recipes, {
        "Spoil_Fish_15_Var3", "Spoil_Fish_15_Var4",
        "Spoil_Fish_16_Var3", "Spoil_Fish_16_Var4",
        "Spoil_Fish_17_Var3", "Spoil_Fish_17_Var4",
    }, log, "fish variant does not exist in the current build")

    # These two have a real counterpart and no existing correct row, so repoint.
    repoint(recipes, "Spoil_Raw_Meat_Tbone", "Inputs[0].Element", "Raw_Meat_Tbone", "Fatty_Tbone", log)
    repoint(recipes, "Spoil_Raw_Meat_Steak", "Inputs[0].Element", "Raw_Meat_Steak", "Giant_Steak", log)
    repoint(recipes, "Spoil_Berries", "Inputs[0].Element", "Berries", "Berry", log)
    repoint(recipes, "Spoil_Soybean", "Inputs[0].Element", "Soybean", "Bean", log)
    repoint(recipes, "Spoil_Prickly_Pear", "Inputs[0].Element", "Prickly_Pear", "PricklyPear", log)
    # Coconut_Mature / _Mid / _Young are left alone on purpose - case-only mismatch.

    # SAFETY FIX. Vanilla Decay_NoDecay is {"Name":"Decay_NoDecay"} with every field at
    # its default, i.e. DecayTime 0 = never decays. The mod set DecayTime 300, which put
    # a decay timer on the 19 permanent objects that use it: all four Saddle Carts, the
    # Speeder Bike saddle, both Landing Pads, the Advanced Exotic Delivery Interface,
    # Animal Silage and ten mission Stasis Bags.
    for r in decay:
        if r.get("Name") == "Decay_NoDecay" and r.get("DecayTime") != 0:
            log.append(f"    Decay_NoDecay: DecayTime {r.get('DecayTime')} -> 0 (never decays, as vanilla)")
            r["DecayTime"] = 0

    # Decay_Advanced_Leather is a production chain, not spoilage: vanilla SpoilTime 60
    # turns "Curing Leather" into Advanced_Leather. The mod's blanket SpoilTime=0 sweep
    # killed it. Restore vanilla - same class of bug the author already fixed for the
    # coconut ripening chain in v2.2.
    for r in decay:
        if r.get("Name") == "Decay_Advanced_Leather":
            r["SpoilTime"] = 60
            r["SpoiledItem"] = {"RowName": "Advanced_Leather", "DataTableName": "D_ItemTemplate"}
            log.append("    Decay_Advanced_Leather: restored SpoilTime 60 -> Advanced_Leather "
                       "(curing chain, not spoilage)")

    x["version"] = "2.3"


def fix_passive_ore(x: dict, log: list) -> None:
    # DisplayName/Description are not properties of D_ItemTemplate (its struct is
    # ItemStaticData / ItemDynamicData / ItemCustomStats / CustomProperties /
    # DatabaseGUID / ItemOwnerLookupId / RuntimeTags). The mod already sets the same
    # text correctly in D_Itemable, so deleting these loses nothing.
    tmpl = block(x, "D_ItemTemplate")
    drop_prop(tmpl, "DisplayName", log, "D_ItemTemplate")
    drop_prop(tmpl, "Description", log, "D_ItemTemplate")

    # Inputs[] elements only have Element and Count. DynamicProperties and Alterations
    # exist on Outputs[] only - 0 of 5939 vanilla input entries carry them.
    recipes = block(x, "D_ProcessorRecipes")
    drop_nested_prop(recipes, "Inputs", "DynamicProperties", log)
    drop_nested_prop(recipes, "Inputs", "Alterations", log)

    x["version"] = "7.8"


def fix_item_kits(x: dict, log: list) -> None:
    """Agents Individual Item Kits.

    Four defects plus the 23 items the Sept-2026 build added.
    """
    stat = block(x, "D_ItemsStatic")
    itemb = block(x, "D_Itemable")
    tmpl = block(x, "D_ItemTemplate")
    cons = block(x, "D_Consumable")
    tal = block(x, "D_Talents")
    ws = block(x, "D_WorkshopItems")

    # (1) Icon and Category are not properties of D_WorkshopItems (the struct is exactly
    # Item / ResearchCost / ReplicationCost / RequiredMission) so the game discards them.
    # They are also redundant: the icon a player sees comes from D_Itemable.Icon, which
    # this mod sets on all 2,683 Itemable rows with the identical path, and the category
    # comes from D_Talents.TalentTree -> D_TalentTrees.Archetype, which is wired
    # correctly. Removing them cannot change anything a player sees, and it removes the
    # only thing in this mod that the game's row parser could object to.
    drop_prop(ws, "Icon", log, "D_WorkshopItems")
    drop_prop(ws, "Category", log, "D_WorkshopItems")

    # (2) Four kits granted nothing: they used ConsumeType + Recipes, neither of which is
    # a property of D_Consumable, instead of Byproducts. All four payload items exist.
    grants = {
        "Agent_Single_Submachine_Gun_Sandwyrm": "Submachine_Gun_Sandwyrm",
        "Agent_Single_Submachine_Gun_Scout": "Submachine_Gun_Scout",
        "Agent_Single_Checkered_Flag": "Checkered_Flag",
        "Agent_Single_Speeder_Kit": "Speeder_Kit",
    }
    for r in cons:
        tgt = grants.get(r.get("Name"))
        if not tgt:
            continue
        r.pop("ConsumeType", None)
        r.pop("Recipes", None)
        r["Modifier"] = {"ModifierLifetime": 0}
        r["Byproducts"] = [{"RowName": tgt, "DataTableName": "D_ItemTemplate"}]
        log.append(f"    {r['Name']}: now grants {tgt} (was ConsumeType/Recipes, which the game ignores)")

    # (3) Fish_17_Var3 / Fish_17_Var4 were removed from the game by the Sept build. The
    # mod already has working kits for the two survivors (Fish_17, Fish_17_Var2), so
    # there is no non-duplicate re-target. Remove both kits completely - all six rows
    # each - so no half-kit is left pointing at a deleted row.
    for base in ("Agent_Single_Fish_17_Var3", "Agent_Single_Fish_17_Var4"):
        drop_rows(stat, {base}, log, "item removed from the game in Sept 2026")
        drop_rows(tmpl, {base}, log, "companion of a removed kit")
        drop_rows(cons, {base}, log, "companion of a removed kit")
        drop_rows(itemb, {"Item_" + base}, log, "companion of a removed kit")
        drop_rows(tal, {"Talent_" + base}, log, "companion of a removed kit")
        drop_rows(ws, {"Meta_" + base}, log, "companion of a removed kit")

    # (4) FName is case-insensitive, so these pairs were the same key and the second row
    # silently overwrote the first - two kits' worth of rows doing nothing. Both members
    # of each pair grant the identical item, so drop the spelling that does not match the
    # D_ItemTemplate row name.
    for dup in ("Agent_Single_Fatty_Tbone", "Agent_Single_WaterBomb"):
        drop_rows(stat, {dup}, log, "case-duplicate of an identical kit (FName collision)")
        drop_rows(tmpl, {dup}, log, "case-duplicate")
        drop_rows(cons, {dup}, log, "case-duplicate")
        drop_rows(itemb, {"Item_" + dup}, log, "case-duplicate")
        drop_rows(tal, {"Talent_" + dup}, log, "case-duplicate")
        drop_rows(ws, {"Meta_" + dup}, log, "case-duplicate")

    # (5) The Sept-2026 build added 32 items. 23 of them are player-obtainable content
    # with no kit. (The 9 skipped are quest/dev junk or workshop container rows whose
    # payload is kitted instead: the 4 Eden audio logs, Fertility_Serum_Orka and
    # _Storca - both broken vanilla stubs with no ItemsStatic row - Mission_Bull,
    # Meta_Resource_Pack_Salt and Workshop_Sawblade_Bundle.)
    added = add_new_kits(x, log)
    if added:
        relayout_grid(x, log)

    x["version"] = "5.3"


# item -> (category index 1-20, research cost, replication cost)
# Category order matches the mod's own left-to-right grid and the README table.
NEW_KITS = {
    "Salt_Stack_500":                    (1,  20, 10),   # Raw Resources
    "Sandwyrm_Wing":                     (1,  50, 25),
    "Fish_15_Var2":                      (4,  10,  5),   # Food
    "Fish_16_Var2":                      (4,  10,  5),
    "Fish_20":                           (4,  10,  5),
    "Fertility_Serum_Boar":              (5,  40, 20),   # Drinks & Medicine
    "Fertility_Serum_SwampBird":         (5,  40, 20),
    "Fertility_Serum_Tundra_Monkey":     (5,  40, 20),
    "Fertility_Serum_Tusker":            (5,  40, 20),
    "Butcher_Knife":                     (6,  50, 25),   # Melee Weapons
    "T2_Launcher":                       (8, 200,100),   # Firearms
    "Sawblade":                          (9,  20, 10),   # Ammunition
    "Sawblade_x20":                      (9,  50, 25),
    "Launcher_Ammo_Rudimentary_Grenade": (10, 75, 40),   # Explosives
    "Launcher_Ammo_Rudimentary_Smoke":   (10, 75, 40),
    "T3_Backpack":                       (12, 50, 25),   # Armor
    "Carbon_Fishing_Rod":                (14, 50, 25),   # Tools
    "Meta_Flashlight":                   (14, 50, 25),
    "Wood_Floor_Refined_Curved":         (16, 15,  8),   # Building Pieces
    "Anvil_Bench_T4_v2":                 (17,100, 50),   # Crafting Stations
    "Meta_Oxite_Dissolver_Printed":      (17,100, 50),
    "Thumper_Deep":                      (18,150, 75),   # Deployables
    "Weapon_Rack_T3":                    (18, 25, 12),
}

GAME_DATA = Path(r"C:\Users\finla\Desktop\data")


def _vanilla(rel: str) -> dict:
    return {r["Name"]: r for r in json.loads((GAME_DATA / rel).read_text(encoding="utf-8-sig"))["Rows"]}


def add_new_kits(x: dict, log: list) -> int:
    """Build the six rows each new kit needs, copying display name and icon from the
    game's own D_Itemable row so the kit looks exactly like the item it contains."""
    if not GAME_DATA.exists():
        log.append(f"    !! game data not found at {GAME_DATA} - skipping the 23 new kits")
        return 0
    v_tmpl = _vanilla("Items/D_ItemTemplate.json")
    v_stat = _vanilla("Items/D_ItemsStatic.json")
    v_item = _vanilla("Traits/D_Itemable.json")

    stat, itemb, tmpl = block(x, "D_ItemsStatic"), block(x, "D_Itemable"), block(x, "D_ItemTemplate")
    cons, tal, ws = block(x, "D_Consumable"), block(x, "D_Talents"), block(x, "D_WorkshopItems")
    have = {r["Name"] for r in tmpl}

    n = 0
    for item, (cat, research, replication) in NEW_KITS.items():
        kit = f"Agent_Single_{item}"
        if kit in have:
            continue
        if item not in v_tmpl:
            log.append(f"    !! {item} is not in the current D_ItemTemplate - skipped")
            continue
        # display data: follow ItemTemplate -> ItemsStatic -> Itemable
        sid = (v_tmpl[item].get("ItemStaticData") or {}).get("RowName")
        srow = v_stat.get(sid) or {}
        irow = v_item.get((srow.get("Itemable") or {}).get("RowName")) or {}
        disp = re.search(r'"([^"]*)"\s*\)\s*$', irow.get("DisplayName") or "")
        label = disp.group(1) if disp else item.replace("_", " ")
        icon = irow.get("Icon")
        if not icon:
            log.append(f"    !! {item} has no icon in D_Itemable - skipped")
            continue

        stat.append({
            "Name": kit,
            "Meshable": {"RowName": "Mesh_Meta_Item_Repair"},
            "Itemable": {"RowName": f"Item_{kit}"},
            "Interactable": {"RowName": "Item"},
            "Highlightable": {"RowName": "Generic"},
            "Consumable": {"RowName": kit},
            "Usable": {"RowName": "Consume"},
            "Decayable": {"RowName": "Decay_General"},
            "Audio": {"RowName": "Default"},
            "Manual_Tags": {"GameplayTags": [{"TagName": "Item.Meta.Consumable"}]},
        })
        itemb.append({
            "Name": f"Item_{kit}",
            "DisplayName": f'NSLOCTEXT("D_Itemable", "Item_{kit}-DisplayName", "{label} Kit")',
            "Icon": icon,
            "Description": f'NSLOCTEXT("D_Itemable", "Item_{kit}-Description", "Kit item contains 1x {label}")',
            "FlavorText": f'NSLOCTEXT("D_Itemable", "Item_{kit}-FlavorText", "Individual item kit")',
            "Weight": 500,
        })
        tmpl.append({"Name": kit, "ItemStaticData": {"RowName": kit}})
        cons.append({
            "Name": kit,
            "Modifier": {"ModifierLifetime": 0},
            "Byproducts": [{"RowName": item, "DataTableName": "D_ItemTemplate"}],
        })
        ws.append({
            "Name": f"Meta_{kit}",
            "Item": {"RowName": kit},
            "ResearchCost": [{"Meta": {"RowName": "Credits", "DataTableName": "D_MetaCurrency"},
                              "Amount": research}],
            "ReplicationCost": [{"Meta": {"RowName": "Credits", "DataTableName": "D_MetaCurrency"},
                                 "Amount": replication}],
        })
        tal.append({
            "Name": f"Talent_{kit}",
            "ExtraData": {"RowName": f"Meta_{kit}", "DataTableName": "D_WorkshopItems"},
            "TalentTree": {"RowName": "Workshop_AgentKits"},
            "Position": {"X": 0, "Y": 0},          # set by relayout_grid
            "Size": {"X": 250, "Y": 250},
            "_cat": cat,                            # temporary, stripped in relayout
        })
        n += 1
    if n:
        log.append(f"    added {n} new kits for items the Sept-2026 build introduced")
    return n


ROWS, COL_STEP, GROUP_GAP, Y0, Y_STEP = 5, 300, 600, 250, 300


def relayout_grid(x: dict, log: list) -> None:
    """Re-flow the whole workshop grid: 5 rows per column, 20 category blocks left to
    right with a one-column gap between blocks. Existing kits keep their category and
    their order within it; new kits are appended to the end of their category."""
    tal = block(x, "D_Talents")
    # Recover each existing kit's category from its current X, using the same block
    # boundaries the mod already had (a jump larger than one column starts a new block).
    old = [r for r in tal if "_cat" not in r]
    xs = sorted({r["Position"]["X"] for r in old})
    bounds, cur = [], [xs[0]]
    for a, b in zip(xs, xs[1:]):
        if b - a > COL_STEP:
            bounds.append((cur[0], cur[-1])); cur = [b]
        else:
            cur.append(b)
    bounds.append((cur[0], cur[-1]))
    if len(bounds) != 20:
        log.append(f"    !! expected 20 category blocks, found {len(bounds)} - grid NOT re-laid out")
        for r in tal: r.pop("_cat", None)
        return

    def cat_of(r):
        if "_cat" in r:
            return r["_cat"]
        px = r["Position"]["X"]
        for i, (lo, hi) in enumerate(bounds, start=1):
            if lo <= px <= hi:
                return i
        return 20

    # stable: existing kits in their current reading order, new kits last
    order = sorted(range(len(tal)), key=lambda i: (
        cat_of(tal[i]),
        1 if "_cat" in tal[i] else 0,
        tal[i]["Position"]["X"] if "_cat" not in tal[i] else 0,
        tal[i]["Position"]["Y"] if "_cat" not in tal[i] else 0,
    ))

    col = 0
    prev_cat = None
    placed = 0
    for idx in order:
        r = tal[idx]
        c = cat_of(r)
        if prev_cat is None:
            col = 0
        elif c != prev_cat:
            col += 1 + (GROUP_GAP - COL_STEP) // COL_STEP   # blank column between blocks
            placed = 0
        if placed and placed % ROWS == 0:
            col += 1
        r["Position"] = {"X": 100 + col * COL_STEP, "Y": Y0 + (placed % ROWS) * Y_STEP}
        r.pop("_cat", None)
        placed += 1
        prev_cat = c
    maxx = max(r["Position"]["X"] for r in tal)
    log.append(f"    re-laid out the workshop grid: {len(tal)} tiles, 20 blocks, X 100..{maxx}")


# ── EXMOD descriptions ────────────────────────────────────────────────────────
# The Mod Manager's downloader expects ONE version + description in this field. A
# chained "v1.4: ... | v1.3: ... | v1.2: ..." history breaks it. The full history
# belongs in README.md and the .txt readme, not here.

DESCRIPTIONS = {
 "Turret_Variants":
   "v3.7: Tuned arc-projectile turret balance (contributed by asconley, PR #16) - trimmed "
   "Crossbow (55->50m), Bow (60->55m), Javelin (70->65m) and Rapid Crossbow (45->40m) ranges so "
   "the gravity-affected shot drops onto the target instead of overshooting, and raised Javelin "
   "launch force (2200->12000) so spears actually reach that range. Adds 15 automated turret "
   "variants with unique characteristics, proper ammo matching and a line-of-sight fix.",

 "Hidden_Building_Pieces":
   "v4.5: Fixed the frame pieces, which had never worked properly. Ten had a Stability row that "
   "does not exist (Limestone_General, Scoria_General, Sandworm_General, Stone_Brick_General, "
   "Glass_General_Tempered), seven had a build Type that does not exist (Frame_FullFrame, "
   "Frame_HalfFrame - the real names are Frame and Frame_Angle), and five recipes asked for "
   "ingredients with no such item (Iron_Ingot, Sandite - now Aluminium and Sandworm_Scale). Also "
   "moved the piece tags out of an invalid property into Manual_Tags so they actually apply. "
   "Unlocks 34 hidden building pieces - frames plus diagonal sets across 11+ materials.",

 "Resource_Repacker":
   "v1.5: Gated the five DLC recipes that had no feature gate (Limestone and Lithium behind "
   "Dangerous Horizons, Clay, Scoria and Obsidian behind New Frontiers) - without it they "
   "registered on base-game installs and pointed at stripped items. Dropped the Ren and Uranium "
   "Rod kits, whose item data the Sept update removed. Added the missing Salt Kit. Fixed the "
   "crafting sound on every recipe: Audio pointed at a D_CraftingAudioData row named "
   "\"Fabricator\", which has never existed in that table, so repacking finished in silence; it "
   "is now \"Default\". 20 recipes that repack raw resources back into UDA kits at neutral ratios.",

 "Exotic_Economy_Overhaul":
   "v2.2: Fixed missing recipe icons by setting ItemIconOverride on every recipe to its output "
   "item, so recipes show the output's icon instead of 'ICON MISSING'. Full currency exchange "
   "system - buy and sell materials with Ren, convert between exotics and currencies, "
   "cross-convert ingots, and bulk smelt ores at the correct furnaces and benches. 66 recipes.",

 "NightVisionGoggles":
   "v2.2: Fixed the crafting sound. The recipe pointed Audio at a D_CraftingAudioData row named "
   "\"Fabricator\", which has never existed in that table - \"Fabricator\" is a D_RecipeSets name. "
   "The goggles crafted in silence while every other recipe on the same bench played its sound. "
   "Now set to \"MachiningBench\", matching the vanilla Binoculars recipe. Adds craftable Night "
   "Vision Goggles with improved durability, no decay and lighter weight.",

 "Solar_Panel_Expansion":
   "v1.2: Major fix - all 4 kits granted nothing when used. They described their payload with "
   "\"ConsumeType\" and \"Recipes\", which are not properties of D_Consumable, so the game "
   "discarded them: the kit was consumed and no panel came out, with the Ren and Uranium already "
   "spent. Rewritten to the vanilla Byproducts form, so each kit now yields its real item. Also "
   "fixed the Bunker Solar Panel Kit showing the plain Solar Panel icon. Adds all solar panels "
   "and the solar backpack to a dedicated Workshop tab with fair pricing.",

 "Trap_Defense_Expansion":
   "v1.3: Fixed the crafting sound on the 12 Fabricator-tier recipes (all 4 elemental landmines, "
   "their 4 direct crafts, Batch Landmines, Landmine Field Kit, Mammoth Trap and Lava Mine). They "
   "pointed Audio at a D_CraftingAudioData row named \"Fabricator\", which has never existed in "
   "that table - \"Fabricator\" is a D_RecipeSets name. All 12 now use \"MachiningBench\", "
   "matching vanilla. Defense expansion with 23 recipes, unlocking the 4 elemental landmines.",

 "UDA_Terminal_Laptop":
   "v2.2: The recipe was never actually free - EXMOD rows merge field by field, so omitting "
   "Requirement left the vanilla Tier-2 tech gate in place. It is now explicitly None. Also "
   "fixed the crafting sound. The recipe override pointed Audio at a D_CraftingAudioData "
   "row named \"Fabricator\", which has never existed in that table - \"Fabricator\" is a "
   "D_RecipeSets name. Because this row overrides the vanilla Orbital Exchange Interface recipe, "
   "it silenced that craft for everyone with the mod installed. Restored to the vanilla value "
   "\"CraftingBench\". Reskins the Orbital Exchange Interface into a laptop, makes it craftable "
   "for free, and lets you place it indoors and on benches, tables and shelves.",

 "Workshop_Recyclers":
   "v5.8: Removed \"ProcessingTime\" from all 3,054 incinerate recipes - it is not a property of "
   "the recipe struct, so the game was discarding it. Fixed 21 recipes that produced an item "
   "under the wrong table's spelling (Platinum_Shealth, Saddle_Standard) and 4 that tried to "
   "output an animal carcass, which the game can never grant. Removed 35 recipes for items that "
   "cannot be held, were deleted by the Sept update, or were never implemented, plus 3 duplicate "
   "rows that silently overwrote each other. Two recycling machines plus an Incinerator, covering "
   "every item in the game.",

 "Dev_Tools_Kit":
   "v1.1.5: Unlocks 10 hidden developer tools in the Workshop - Thor's Hammer (fly mode), "
   "Fireball, Inspection Tool, Transform Tool, Destroy Tool and more, all free. Visible meshes "
   "for every tool and a 4-row workshop grid that fits the vertical bounds.",

 "Waste_Not":
   "v2.3: Fixed Dense Stone. It was setting the deposit's PRIMARY yield to Silica instead of its "
   "secondary, so dense stone stopped giving stone at all while still giving stone as the "
   "secondary - the inverse of what the mod is for. It now matches every other deposit. Also "
   "removed an undocumented change that gave the random-resource voxel a Stone yield vanilla "
   "does not give it. Mining yields useful secondary resources instead of Stone across 26 of the "
   "33 deposit types.",

 "AbsoluteChaos_Core":
   "v0.2.2: Zeroed the four workshop items later game updates added, which the mod had missed "
   "and which still charged credits (Flashlight, Sawblades, MXC Oxite Dissolver, Salt resource "
   "pack) - all 339 are now free. Base layer of the Absolute Chaos modpack: a 76-key player stat "
   "block and free workshop research and replication.",

 "Agents_Individual_Item_Kits":
   "v5.3: Get back kits you already researched - an older update renamed every kit's research "
   "ID, so kits researched before it showed as locked and asked for Ren again. Close Icarus and run "
   "Restore_Kit_Research.bat (in the Restore_Kit_Research folder) to restore them for free; it "
   "backs up your profile first. Added 23 kits for items from the Sept 2026 update. Fixed 4 kits "
   "that gave nothing when used (Sandwyrm SMG, Scout SMG, Checkered Flag, Speeder Kit). Removed 2 "
   "kits for fish the game deleted and 2 duplicate kits that overwrote each other. Removed two "
   "properties (Icon, Category) from every workshop entry that the game does not read. 2,702 "
   "individual item kits across 20 workshop categories.",

 **{m: (
   f"v{'1.7' if f == 2 else '5.2'}: Fixed the speed maths. Around 900 recipes were set to 0 MJ - "
   f"instant - instead of {f}x, because the generator treated a recipe's absent "
   f"RequiredMillijoules as 0 rather than the game's default of 2500. Basic crafts like the Stone "
   f"Pickaxe, Stone Axe and Wood Bow were instant. All recipes are now recomputed from the real "
   f"vanilla cost, no recipe is ever made slower than vanilla, and the list is rebuilt against the "
   f"current game data - 2,211 recipes, up from 2,175, with the removed Flaregun entry dropped. "
   f"Everything processes and crafts {f}x faster."
 ) for m, f in SPEED_MODS.items()},

 "FastProcessing_Instant":
   "v5.2: Rebuilt against the current game data - 2,211 recipes, up from 2,175, with the removed "
   "Flaregun entry dropped. Every recipe is now 1 MJ except water-consuming ones, which keep a "
   "500 MJ floor, and no recipe is ever made slower than vanilla (two fishing recipes had been "
   "made 500x slower by the floor). Processing and crafting are effectively instant.",

 "Hardcore_Rebalance_Pack":
   "v2.2: The alpha hunters now actually appear. Their 37 definitions were always correct, but "
   "the 25 rows meant to spawn them used properties D_AISpawnZones does not have, and the 25 loot "
   "tables used a 'Drops' property D_ItemRewards does not have - so the hunters were defined, "
   "never spawned, and would have dropped nothing. Both are rebuilt the way the base game does "
   "it: hunters are added to real spawn zones as rare entries in the biome's hardest tiers, and "
   "their loot uses the real Rewards format. 4-tier creature scaling, rebalanced horde waves, "
   "deadly weather and harsher survival.",

 "Creature_Difficulty_Scaling":
   "v2.4: Fixed the health-regeneration buff, which had never worked. 158 of the 180 creature "
   "growth rows targeted a stat named BaseHealthRegenPerMinute_+%, which does not exist - it is "
   "two real stat names run together - so the game ignored it and every creature kept vanilla "
   "regen. Now BaseHealthRegen_+%, with the same values. Also fixed four Styx biomes "
   "(Enclosed Wood, Ring Lake, Oasis, Dusty Barrens) that had lost their ambient sound because "
   "their Audio pointed at an atmosphere name instead of a biome-audio name. Full creature "
   "overhaul for the level 500 cap, 161 spawn zones rescaled, 136 creatures buffed by tier.",

 "No_Food_Spoilage":
   "v2.3: Fixed 12 composter recipes that pointed at items which do not exist in the game, and "
   "repointed 5 more to their real item names. Restored Decay_NoDecay to never-decay - it had "
   "been given a decay timer, which put one on saddle carts, landing pads and mission stasis "
   "bags. Restored the Advanced Leather curing chain, which the no-spoil sweep had disabled. "
   "All food and volatiles never spoil, with 122 composter recipes for raw produce.",

 "Passive_Ore_Extractor_Drills":
   "v7.8: Fixed the mining sound - all 23 miners pointed Audio at a D_CraftingAudioData row "
   "named \"Furnace\", which has never existed in that table, so they ran in silence. Now "
   "\"Default\", matching vanilla's own passive extractor recipe. 23 passive ore extractors, "
   "one per ore type, purchasable in the Workshop or craftable at the Fabricator.",
}


def fix_creature_scaling(x: dict, log: list) -> None:
    """Creature Difficulty Scaling."""
    # (1) On every Styx biome it re-themes, the mod copied the AtmosphereType string into
    # Audio. D_Atmospheres really does have Swamp / Volcanic / Arena_Golem, but
    # D_BiomeAudioData names its rows differently, so four biomes ended up silent.
    # Use whatever audio vanilla pairs with the atmosphere the mod chose, so the
    # re-theme is preserved rather than reverted:
    #   Swamp       -> Wetlands      (5 vanilla biomes; ElySwamp is Elysium-only)
    #   Volcanic    -> Lava          (13 of 13 vanilla biomes)
    #   Arena_Golem -> BossGolemCave (the golem arena; DHLab is the DH lab)
    audio = {
        "Styx_EnclosedWood": "Wetlands",
        "Styx_RingLake": "Wetlands",
        "Styx_Oasis": "Lava",
        "Styx_DustyBarrens": "BossGolemCave",
    }
    for r in block(x, "D_Biomes") or []:
        want = audio.get(r.get("Name"))
        if want and (r.get("Audio") or {}).get("RowName") != want:
            old = (r.get("Audio") or {}).get("RowName")
            r["Audio"] = {"RowName": want}
            log.append(f"    {r['Name']}: Audio {old} -> {want}")

    # (2) 158 of the 180 D_AIGrowth rows buff a stat called
    # 'BaseHealthRegenPerMinute_+%', which is not in D_Stats and never has been - it is
    # the two real stats concatenated ('BaseHealthRegenPerMinute_+' flat and
    # 'BaseHealthRegen_+%' percent). The mod's values are percentages and it already
    # carries the flat stat separately, so the intended one is BaseHealthRegen_+%.
    # Until this is fixed the entire advertised regen buff does nothing.
    BAD = '(Value="BaseHealthRegenPerMinute_+%")'
    GOOD = '(Value="BaseHealthRegen_+%")'
    n = 0
    for r in block(x, "D_AIGrowth") or []:
        base = r.get("Base")
        if isinstance(base, dict) and BAD in base:
            base[GOOD] = base.pop(BAD)
            n += 1
    if n:
        log.append(f"    renamed the health-regen stat key on {n} D_AIGrowth rows "
                   f"(BaseHealthRegenPerMinute_+% is not a stat; BaseHealthRegen_+% is)")

    x["version"] = "2.4"


# ── the speed mods ────────────────────────────────────────────────────────────
# D_ProcessorRecipes.Defaults.RequiredMillijoules is 2500, and 869 vanilla rows OMIT the
# field - so their real cost is 2500, not 0. The generator that built these mods read the
# absent field as 0 and divided it, emitting 0 = INSTANT on ~900 recipes instead of the
# advertised multiplier. That is why "5x" made Stone Pickaxe, Stone Axe and Wood Bow
# instant. The same slip hit all six speed mods.
#
# Two more bugs shared by all six: Fisher_Saltwater_Fish and Fisher_Freshwater_Fish cost
# 1 MJ in vanilla but got the 500 MJ water floor applied, making them 500x SLOWER; and
# Flaregun was removed from the game, so that row dangles.

WATER_FLOOR = 500


def _water_recipes() -> set:
    pr = json.loads((GAME_DATA / "Crafting/D_ProcessorRecipes.json").read_text(encoding="utf-8-sig"))
    out = set()
    for r in pr["Rows"]:
        for ri in r.get("ResourceInputs") or []:
            if ((ri.get("Type") or {}).get("Value")) == "Water":
                out.add(r["Name"])
    return out


def _vanilla_costs():
    pr = json.loads((GAME_DATA / "Crafting/D_ProcessorRecipes.json").read_text(encoding="utf-8-sig"))
    dflt = pr["Defaults"]["RequiredMillijoules"]
    return {r["Name"]: r.get("RequiredMillijoules", dflt) for r in pr["Rows"]}, dflt


def make_speed_fix(factor: int):
    def fix(x: dict, log: list) -> None:
        if not GAME_DATA.exists():
            log.append(f"    !! game data not found at {GAME_DATA} - skipped")
            return
        van, dflt = _vanilla_costs()
        water = _water_recipes()
        rows = block(x, "D_ProcessorRecipes")

        gone = [r["Name"] for r in rows if r["Name"] not in van]
        if gone:
            drop_rows(rows, set(gone), log, "recipe no longer exists in the game")

        fixed_zero = fixed_slow = 0
        for r in rows:
            v = van.get(r["Name"])
            if v is None:
                continue
            got = r.get("RequiredMillijoules")
            target = max(1, round(v / factor))
            if r["Name"] in water:
                target = max(target, WATER_FLOOR)
            # never make a recipe slower than vanilla
            target = min(target, v)
            if got == 0:
                r["RequiredMillijoules"] = target
                fixed_zero += 1
            elif got is not None and got > v:
                r["RequiredMillijoules"] = target
                fixed_slow += 1
        if fixed_zero:
            log.append(f"    {fixed_zero} recipes were set to 0 MJ (instant) instead of {factor}x "
                       f"- recomputed from the real vanilla cost")
        if fixed_slow:
            log.append(f"    {fixed_slow} recipes were SLOWER than vanilla (the water floor applied "
                       f"to 1 MJ recipes) - capped at the vanilla cost")

        have = {r["Name"] for r in rows}
        added = 0
        for n, v in van.items():
            if n in have:
                continue
            t = max(1, round(v / factor))
            if n in water:
                t = max(t, WATER_FLOOR)
            rows.append({"Name": n, "RequiredMillijoules": min(t, v)})
            added += 1
        if added:
            log.append(f"    added {added} recipes the game has gained since the mod was last built")
        x["version"] = "1.7" if factor == 2 else "5.2"
    return fix


def fix_instant(x: dict, log: list) -> None:
    """FastProcessing Instant: 1 MJ everywhere, except keep the 500 MJ water floor and
    never go slower than vanilla."""
    if not GAME_DATA.exists():
        log.append(f"    !! game data not found at {GAME_DATA} - skipped")
        return
    van, _ = _vanilla_costs()
    water = _water_recipes()
    rows = block(x, "D_ProcessorRecipes")
    gone = [r["Name"] for r in rows if r["Name"] not in van]
    if gone:
        drop_rows(rows, set(gone), log, "recipe no longer exists in the game")
    changed = 0
    for r in rows:
        v = van.get(r["Name"])
        if v is None:
            continue
        target = min(WATER_FLOOR if r["Name"] in water else 1, v)
        if r.get("RequiredMillijoules") != target:
            r["RequiredMillijoules"] = target
            changed += 1
    have = {r["Name"] for r in rows}
    added = 0
    for n, v in van.items():
        if n in have:
            continue
        rows.append({"Name": n, "RequiredMillijoules": min(WATER_FLOOR if n in water else 1, v)})
        added += 1
    if changed:
        log.append(f"    normalised {changed} recipes (1 MJ, water floor {WATER_FLOOR}, never slower than vanilla)")
    if added:
        log.append(f"    added {added} recipes the game has gained since the mod was last built")
    x["version"] = "5.2"


def fix_workshop_recyclers(x: dict, log: list) -> None:
    """Workshop Recyclers."""
    rows = block(x, "D_ProcessorRecipes")

    # (1) "ProcessingTime" is not a property of ProcessorRecipe - the struct's timing
    # field is RequiredMillijoules. All 3,054 Incinerate_* rows carry it (always 1.0) and
    # the game discards every one. They already set RequiredMillijoules 100 as well, so
    # deleting the dead key changes nothing about how they behave.
    drop_prop(rows, "ProcessingTime", log, "D_ProcessorRecipes")

    # (2) Two output names are D_ItemsStatic row names used in a D_ItemTemplate slot.
    # The game spells the same thing differently in the two tables.
    for old, new, n in (("Platinum_Shealth", "Platinum_Sheath", 17),
                        ("Saddle_Standard", "Saddle_Mount", 4)):
        c = 0
        for r in rows:
            for o in r.get("Outputs") or []:
                el = o.get("Element") or {}
                if el.get("RowName") == old:
                    el["RowName"] = new
                    c += 1
        if c:
            log.append(f"    Outputs {old} -> {new} on {c} rows "
                       f"({old} is the D_ItemsStatic name; {new} is its D_ItemTemplate wrapper)")

    # (3) Four Deconstruct_* rows tried to output an AnimalCarcass_*, but carcasses exist
    # only in D_ItemsStatic - they are world-spawned and have no D_ItemTemplate row, so
    # they can never be produced. The mod's own rule is "outputs = the inputs of the
    # vanilla recipe that makes this item", and each row's RequiredMillijoules identifies
    # that recipe unambiguously.
    carcass = {
        "Deconstruct_Fur":        ("Wool", 2),       # Fur_From_Wool, 10000 mJ
        "Deconstruct_Gamey_Meat": ("Ram_Head", 1),   # Butcher_Meat_Ram, 7500 mJ
        "Deconstruct_Soft_Meat":  ("Sheep_Head", 1), # Butcher_Meat_Sheep, 7500 mJ
        "Deconstruct_Raw_Bacon":  ("Pig_Head", 1),   # Butcher_Meat_Pig, 7500 mJ
    }
    for r in rows:
        got = carcass.get(r.get("Name"))
        if not got:
            continue
        name, count = got
        for o in r.get("Outputs") or []:
            el = o.get("Element") or {}
            if str(el.get("RowName", "")).startswith("AnimalCarcass"):
                old = el["RowName"]
                el["RowName"] = name
                o["Count"] = count
                log.append(f"    {r['Name']}: output {old} -> {name} x{count}")

    # Deconstruct_Raw_Meat is deliberately NOT repointed. Seven vanilla recipes produce
    # Raw_Meat from a non-carcass input, all at the same cost, so the rule does not pick
    # one; and its own RequiredMillijoules is 0, which matches none of them. Rather than
    # invent an output, drop it.
    drop_rows(rows, {"Deconstruct_Raw_Meat"}, log,
              "output cannot be determined - 7 equally valid vanilla sources, no cost match")

    # (4) Inputs that no player can ever hold. Ghost items with a D_ItemTemplate row but
    # no D_ItemsStatic row, plus items the Sept build removed, plus 17 workshop entries
    # the game itself has never implemented (their vanilla D_WorkshopItems rows dangle).
    drop_rows(rows, {
        "Incinerate_Building_UpgradeTool", "Incinerate_Concrete_Sign_Small",
        "Incinerate_ScoriaBrick_Sign_Small", "Incinerate_StoneBrick_Sign_Small",
        "Incinerate_DEV_Destroy_Tool", "Incinerate_Tame_Capture_Grenade",
        "Incinerate_Saddle_Mammoth_Heavy",
    }, log, "item has no D_ItemsStatic row, so it can never be held")
    drop_rows(rows, {
        "Incinerate_LegendaryWeapon_SlugLauncher",
        "Incinerate_Meta_Resource_Pack_Ren", "Recycle_Meta_Resource_Pack_Ren",
        "Incinerate_Meta_Resource_Pack_Uranium_Rod", "Recycle_Meta_Resource_Pack_Uranium_Rod",
        "Incinerate_Fish_17_Var3", "Incinerate_Fish_17_Var4", "Incinerate_FlagPole",
    }, log, "item removed from the game by the Sept-2026 build")
    drop_rows(rows, {
        "Incinerate_Collision_Projectile", "Deconstruct_Advanced_Butchery_Bench",
    }, log, "item has never existed in any build")
    drop_rows(rows, {
        "Recycle_Meta_Larkwell_Armor_White_Arms", "Recycle_Meta_Larkwell_Armor_White_Chest",
        "Recycle_Meta_Larkwell_Armor_White_Feet", "Recycle_Meta_Larkwell_Armor_White_Head",
        "Recycle_Meta_Larkwell_Armor_White_Legs", "Recycle_Meta_Axe_Shengong_Delta",
        "Recycle_Meta_Biolab_Inhaler_GiantCat", "Recycle_Meta_Biolab_Inhaler_PlantBoss",
        "Recycle_Meta_Biolab_Inhaler_Scyther", "Recycle_Meta_Biolab_Inhaler_Thornet",
        "Recycle_Meta_Heated_Canteen_Inaris", "Recycle_Meta_Hammer_Shengong_Charlie",
        "Recycle_Meta_Hammer_Shengong_Delta", "Recycle_Meta_Hammer_Shengong_Echo",
        "Recycle_Meta_Shield_9Diamonds", "Recycle_Meta_Sickle_Shengong_01",
        "Recycle_Meta_Sickle_Shengong_02",
    }, log, "unreleased workshop item - the vanilla D_WorkshopItems row dangles too")

    # (5) FName is case-insensitive, so these three pairs were the same key and one of
    # each silently overwrote the other. Keep the spelling that matches the game's own
    # D_ItemsStatic row.
    drop_rows(rows, {
        "Deconstruct_Saddle_Bearhide",            # keeps Deconstruct_Saddle_BearHide
        "Deconstruct_Homestead_Birdbath_Iron",    # keeps ..._BirdBath_Iron
        "Deconstruct_Homestead_Birdbath_Gold",    # keeps ..._BirdBath_Gold
    }, log, "case-duplicate row name (FName collision) - the pair silently overwrote each other")

    x["version"] = "5.8"


def fix_hidden_building(x: dict, log: list) -> None:
    """Hidden Building Pieces."""
    # (1) Stability rows that do not exist. Each material routes to an existing family in
    # vanilla, proved by the equivalent vanilla buildable:
    #   Limestone -> Concrete_*   (vanilla Limestone_Frame uses Concrete_Frame)
    #   Scoria    -> Stone_*      (vanilla Scoria_Frame uses Stone_Frame)
    #   Sandworm  -> Wood_*_Reinforced
    #   StoneBrick-> Clay_Brick_* (every vanilla Stone_Brick_* piece uses it)
    #   TemperedGlass -> Glass_Tempered  (the row is not called Glass_General_Tempered)
    stability = {
        "Limestone_General": "Concrete_Frame",
        "Scoria_General": "Stone_Frame",
        "Sandworm_General": "Wood_Beam_Reinforced",
        "Stone_Brick_General": "Clay_Brick_General",
        "Scoria_Brick_General": "Clay_Brick_General",
        "ReinforcedWood_General": "Wood_General_Reinforced",
        "Glass_General_Tempered": "Glass_Tempered",
    }
    c = 0
    for r in block(x, "D_Buildable") or []:
        st = r.get("Stability") or {}
        new = stability.get(st.get("RowName"))
        if new:
            log.append(f"    {r['Name']}: Stability {st['RowName']} -> {new}")
            st["RowName"] = new
            c += 1

    # (2) D_BuildingLookup has Frame / Frame_Angle / Frame_Pillar - no FullFrame/HalfFrame.
    lookup = {"Frame_FullFrame": "Frame", "Frame_HalfFrame": "Frame_Angle"}
    for r in block(x, "D_BuildingPieces") or []:
        t = r.get("Type") or {}
        new = lookup.get(t.get("RowName"))
        if new:
            log.append(f"    {r['Name']}: Type {t['RowName']} -> {new}")
            t["RowName"] = new

    # (3) Two recipe ingredients that exist under different names. The mod builds every
    # other set from its refined material (Clay_Brick, Glass, Steel_Ingot, Wood_Refined),
    # and vanilla's own Iron_*_Ingot recipes take Aluminium, so Iron_Ingot means Aluminium.
    # Every vanilla Sandworm building recipe takes Sandworm_Scale.
    ingredient = {"Iron_Ingot": "Aluminium", "Sandite": "Sandworm_Scale"}
    for r in block(x, "D_ProcessorRecipes") or []:
        for i in r.get("Inputs") or []:
            el = i.get("Element") or {}
            new = ingredient.get(el.get("RowName"))
            if new:
                log.append(f"    {r['Name']}: input {el['RowName']} -> {new}")
                el["RowName"] = new

    # (4) Display data on D_ItemTemplate is not on that struct and is discarded; the same
    # text and icon already live on the matching D_Itemable rows.
    tmpl = block(x, "D_ItemTemplate")
    for p in ("Icon", "DisplayName", "Description"):
        drop_prop(tmpl, p, log, "D_ItemTemplate")

    # (5) "Traits" is not a property of D_ItemsStatic - the real container is Manual_Tags.
    # The tag strings are right, so move them rather than throw them away.
    moved = 0
    for r in block(x, "D_ItemsStatic") or []:
        tr = r.pop("Traits", None)
        if not tr:
            continue
        tags = [{"TagName": t} for t in tr if isinstance(t, str)]
        existing = ((r.get("Manual_Tags") or {}).get("GameplayTags")) or []
        have = {t.get("TagName") for t in existing}
        r["Manual_Tags"] = {"GameplayTags": existing + [t for t in tags if t["TagName"] not in have]}
        moved += 1
    if moved:
        log.append(f"    moved the tag list from the invalid 'Traits' property into Manual_Tags "
                   f"on {moved} D_ItemsStatic rows")

    # (6) D_BuildingSkins has only BaseMeshMaterialSlotOverrides and
    # FrameMaterialSlotOverrides; MaterialSet is discarded. The mod already sets the real
    # override maps, so the dead key can go.
    drop_prop(block(x, "D_BuildingSkins"), "MaterialSet", log, "D_BuildingSkins")

    x["version"] = "4.5"


MAX_ZONES_PER_HUNTER = 3


def _biome_of(zone: str) -> str:
    import re as _re
    if _re.search(r"Arctic|Tundra|Icesheet|Snow", zone): return "Arctic"
    if _re.search(r"Desert|Dune|Barrens|Oasis|Sand", zone): return "Desert"
    if _re.search(r"Conifer|Forest|Wood|Grass", zone): return "Forest"
    if _re.search(r"Swamp|Wetland|Marsh|Mire", zone): return "Swamp"
    if _re.search(r"Lava|Volcanic|Ash", zone): return "Volcanic"
    return "Other"


def fix_hardcore(x: dict, log: list) -> None:
    """Hardcore Rebalance Pack - make the alpha hunters and their loot actually work.

    The 37 D_EpicCreatures definitions were always fine. What never worked was the
    plumbing around them:
      * 25 "spawn zone" rows invented EpicCreature / SpawnBiome / MaxSpawnCount /
        RespawnTime / SpawnChance, none of which are D_AISpawnZones properties, so the
        hunters were defined and never spawned.
      * 25 D_ItemRewards rows put their loot under "Drops", which is not a property of
        D_ItemRewards either, so the hunters dropped nothing.
    """
    zones = block(x, "D_AISpawnZones")
    rewards = block(x, "D_ItemRewards")
    epics = {r["Name"] for r in (block(x, "D_EpicCreatures") or [])}
    epic_ai = {r["Name"]: (r.get("AISetup") or {}).get("RowName")
               for r in (block(x, "D_EpicCreatures") or [])}

    # --- 1. read the intent off the invented rows, then delete them ---
    intent = []
    for r in list(zones):
        if "EpicCreature" not in r:
            continue
        intent.append((r["EpicCreature"]["RowName"], r.get("SpawnBiome", "Other")))
    zones[:] = [r for r in zones if "EpicCreature" not in r]
    if intent:
        log.append(f"    removed {len(intent)} spawn rows built from properties D_AISpawnZones "
                   f"does not have (EpicCreature/SpawnBiome/MaxSpawnCount/RespawnTime/SpawnChance)")

    # --- 2. wire each hunter into the real zones, the way vanilla does it ---
    # Vanilla spawns an epic by adding an AISpawnList entry whose EpicCreature.Value names
    # a D_EpicCreatures row (19 such entries ship in the base game, e.g. PRO_Icesheet_Top
    # -> Snow_Wolf / RedExotic_Infused). Prefer the biome's Hard tiers so hunters stay
    # rare; fall back to every zone of that biome where no Hard tier exists.
    real = [r for r in zones if "Creatures" in r]
    by_biome: dict = {}
    for r in real:
        by_biome.setdefault(_biome_of(r["Name"]), []).append(r)
    placed = 0
    for hunter, biome in intent:
        if hunter not in epics:
            log.append(f"    !! {hunter} has no D_EpicCreatures row - not spawned")
            continue
        pool = by_biome.get(biome) or []
        hard = [r for r in pool if "Hard" in r["Name"] or "Super" in r["Name"]]
        # Keep hunters rare. Vanilla ships only 19 epic entries in total, so cap each
        # hunter at a few zones rather than seeding every zone in the biome (Swamp and
        # Volcanic have no Hard tier to narrow to).
        targets = (hard or pool)[:MAX_ZONES_PER_HUNTER]
        if not targets:
            log.append(f"    !! no {biome} zone available for {hunter} - not spawned")
            continue
        ai = epic_ai.get(hunter)
        for z in targets:
            lst = z.setdefault("Creatures", {}).setdefault("AISpawnList", [])
            if any((e.get("EpicCreature") or {}).get("Value") == hunter for e in lst):
                continue
            lst.append({
                "AISetup": {"Value": ai},
                "SpawnWeight": 1,          # rare next to the usual 4-10
                "EpicCreature": {"Value": hunter},
            })
            placed += 1
    if placed:
        log.append(f"    wired {len(intent)} alpha hunters into real spawn zones as "
                   f"{placed} AISpawnList entries (SpawnWeight 1, Hard tiers where they exist)")

    # --- 3. loot: "Drops" -> the real "Rewards" shape ---
    ITEM_FIX = {"Exotic_Ore": "Meta_Resource",          # the mod's own working rows use this
                "Ammo_Shotgun_Shell": "Ammo_Shell_Buckshot"}
    # rows that already used the real property still name two items that do not exist
    renamed = 0
    for r in rewards:
        for e in r.get("Rewards") or []:
            it = e.get("Item") or {}
            new = ITEM_FIX.get(it.get("RowName"))
            if new:
                it["RowName"] = new
                renamed += 1
    if renamed:
        log.append(f"    renamed {renamed} reward items that do not exist in the game")

    conv = 0
    for r in rewards:
        drops = r.pop("Drops", None)
        if not drops:
            continue
        out = []
        for d in drops:
            name = ITEM_FIX.get(d.get("RowName"), d.get("RowName"))
            chance = d.get("DropChance", 1.0)
            out.append({
                "Item": {"RowName": name, "DataTableName": "D_ItemTemplate"},
                # the mod wrote 0-1 fractions; D_ItemRewards uses 0-100
                "DropChance": int(round(chance * 100)) if chance <= 1 else int(chance),
                "MinRandomStackCount": d.get("MinCount", 1),
                "MaxRandomStackCount": d.get("MaxCount", 1),
                "bRewardsScale": False,
            })
        r.setdefault("Rewards", []).extend(out)
        conv += 1
    if conv:
        log.append(f"    converted {conv} loot tables from the invalid 'Drops' property to "
                   f"'Rewards' (and Exotic_Ore -> Meta_Resource, Ammo_Shotgun_Shell -> Ammo_Shell_Buckshot)")

    # --- 4. the radiation boss AISetup no longer exists ---
    for r in block(x, "D_EpicCreatures") or []:
        if (r.get("AISetup") or {}).get("RowName") == "Radiation_Boss":
            log.append("    !! Hunter_RadiationBoss references AISetup 'Radiation_Boss', which is not "
                       "in D_AISetup in either build - row removed")
    before = len(block(x, "D_EpicCreatures") or [])
    drop_rows(block(x, "D_EpicCreatures"), {"Hunter_RadiationBoss"}, log,
              "its AISetup 'Radiation_Boss' does not exist in the game")
    if len(block(x, "D_EpicCreatures")) != before:
        # and anything that referenced it
        zones_removed = 0
        for z in zones:
            lst = (z.get("Creatures") or {}).get("AISpawnList") or []
            n0 = len(lst)
            lst[:] = [e for e in lst if (e.get("EpicCreature") or {}).get("Value") != "Hunter_RadiationBoss"]
            zones_removed += n0 - len(lst)
        if zones_removed:
            log.append(f"    also removed {zones_removed} spawn entries for it")

    x["version"] = "2.2"


def fix_absolute_chaos(x: dict, log: list) -> None:
    """Absolute Chaos - Core zeroes the cost of every workshop item, but the list was
    enumerated against an older build. The Sept-2026 game has 339 workshop rows and the
    mod covers 335, so four still charge credits."""
    if not GAME_DATA.exists():
        log.append(f"    !! game data not found at {GAME_DATA} - skipped")
        return
    van = [r["Name"] for r in json.loads(
        (GAME_DATA / "MetaWorkshop/D_WorkshopItems.json").read_text(encoding="utf-8-sig"))["Rows"]]
    ws = block(x, "D_WorkshopItems")
    have = {r["Name"] for r in ws}
    free = lambda: [{"Meta": {"RowName": "Credits", "DataTableName": "D_MetaCurrency"}, "Amount": 0}]
    added = []
    for n in van:
        if n not in have:
            ws.append({"Name": n, "ResearchCost": free(), "ReplicationCost": free()})
            added.append(n)
    if added:
        log.append(f"    zeroed {len(added)} workshop items added by later game updates: "
                   f"{', '.join(added)}")
        x["version"] = "0.2.2"


def fix_waste_not(x: dict, log: list) -> None:
    """Waste Not.

    One row writes the wrong field. Stone_Dense sets ResourceType (the PRIMARY yield)
    to Silica, where every other deposit in the mod sets SecondaryResourceType. Since
    EXMOD rows merge per-property, vanilla's SecondaryResourceType (Stone) survives - so
    Dense Stone ends up giving Silica as its primary and STILL Stone as its secondary,
    the exact inverse of the mod's purpose, and the game's main stone deposit stops
    yielding stone. Stone_Normal in the same file does it correctly.
    """
    rows = block(x, "D_VoxelSetupData")
    for r in rows:
        if r.get("Name") == "Stone_Dense" and "ResourceType" in r:
            r.pop("ResourceType")
            r["SecondaryResourceType"] = {"RowName": "Silica"}
            log.append("    Stone_Dense: was setting the PRIMARY yield to Silica (leaving the "
                       "secondary as Stone) - now sets the secondary, matching Stone_Normal")

    # Random_Normal gives the random-resource voxel a Stone primary that vanilla leaves
    # unset. It is undocumented and points the opposite way to the mod's stated purpose,
    # so drop the row and let the vanilla value stand.
    drop_rows(rows, {"Random_Normal"}, log,
              "undocumented change that ADDED Stone as a primary yield; vanilla leaves it unset")

    x["version"] = "2.3"


def fix_resource_repacker(x: dict, log: list) -> None:
    """Resource Repacker."""
    rows = block(x, "D_ProcessorRecipes")

    # (1) Five recipes repack DLC-only resources but carry no feature gate, so on a
    # base-game install they register and point at items the build has stripped - exactly
    # the broken-recipe case the README says cannot happen. Gate them the way the mod
    # already gates Ruby / Uranium Rod / Ren, and the way all 931 vanilla rows do it.
    gates = {
        "Meta_Resource_Pack_Limestone": "DangerousHorizons",
        "Meta_Resource_Pack_Lithium": "DangerousHorizons",
        "Meta_Resource_Pack_Clay": "NewFrontiers",
        "Meta_Resource_Pack_Scoria": "NewFrontiers",
        "Meta_Resource_Pack_Obsidian": "NewFrontiers",
    }
    for r in rows:
        g = gates.get(r.get("Name"))
        if g and "Metadata" not in r:
            r["Metadata"] = {"RequiredFeatureLevel": {"RowName": g}}
            log.append(f"    {r['Name']}: gated behind {g} (its resource is DLC-only)")

    # (2) The Ren and Uranium Rod kits lost their D_ItemsStatic rows in the Sept build -
    # the D_ItemTemplate shell survives but has no static data, so the kit these recipes
    # hand back has no mesh, icon or use. Vanilla's own workshop entries for them are
    # equally broken; nothing here can repair that, so stop producing them.
    drop_rows(rows, {"Meta_Resource_Pack_Ren", "Meta_Resource_Pack_Uranium_Rod"}, log,
              "the kit lost its D_ItemsStatic row in the Sept-2026 build, so it has no item data")

    # (3) The game has 22 resource kits; the mod repacked 21. Salt was added after the
    # mod was last built and is base-game (no feature gate). Neutral ratio: the kit's
    # Byproducts give Salt_Stack_500, i.e. 500 Salt.
    if not any(r.get("Name") == "Meta_Resource_Pack_Salt" for r in rows):
        template = next((r for r in rows if r.get("Name") == "Meta_Resource_Pack_Silica"), None)
        if template:
            rows.append({
                "Name": "Meta_Resource_Pack_Salt",
                "RequiredMillijoules": template.get("RequiredMillijoules", 2000),
                "RecipeSets": json.loads(json.dumps(template["RecipeSets"])),
                "Inputs": [{"Element": {"RowName": "Salt", "DataTableName": "D_ItemsStatic"},
                            "Count": 500}],
                "Outputs": [{"Element": {"RowName": "Meta_Resource_Pack_Salt",
                                         "DataTableName": "D_ItemTemplate"},
                             "Count": 1, "DynamicProperties": [], "Alterations": []}],
                "Audio": {"RowName": "Default"},
            })
            log.append("    added the missing Salt Kit recipe (500 Salt -> 1 kit, neutral)")

    x["version"] = "1.5"


FIXES = OrderedDict([
    ("AbsoluteChaos_Core", fix_absolute_chaos),
    ("Waste_Not", fix_waste_not),
    ("Resource_Repacker", fix_resource_repacker),
    ("Agents_Individual_Item_Kits", fix_item_kits),
    ("Creature_Difficulty_Scaling", fix_creature_scaling),
    ("Workshop_Recyclers", fix_workshop_recyclers),
    ("Hidden_Building_Pieces", fix_hidden_building),
    ("Hardcore_Rebalance_Pack", fix_hardcore),
    ("No_Food_Spoilage", fix_no_food_spoilage),
    ("Passive_Ore_Extractor_Drills", fix_passive_ore),
    ("FastProcessing_Instant", fix_instant),
])
for _m, _f in SPEED_MODS.items():
    FIXES[_m] = make_speed_fix(_f)


def update_changelogs(mod: str, version: str, write: bool, log: list) -> None:
    """The .txt readme carries the FULL version history and is what the Mod Manager
    shows, so every release needs an entry there. README.md gets the same entry under
    its Changelog heading. Both take this release's text from the EXMOD description,
    with the leading "vX.Y: " stripped.
    """
    desc = DESCRIPTIONS.get(mod)
    if not desc or not version:
        return
    body = re.sub(r"^v[\d.]+:\s*", "", desc).strip()

    # wrap to a readable width for the plain-text readme
    words, line, lines = body.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > 88:
            lines.append(line); line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        lines.append(line)
    wrapped = "\n".join(lines)

    d = REPO / mod
    for txt in d.glob("Readme (*.txt"):
        t = txt.read_text(encoding="utf-8", errors="replace")
        if re.search(rf"^Ver {re.escape(version)}\b", t, re.M):
            continue
        t2 = re.sub(r"^Mod Version:.*$", f"Mod Version: {version}", t, count=1, flags=re.M)
        m = re.search(r"^Ver [\d.]+", t2, re.M)
        entry = f"Ver {version}\n{wrapped}\n\n"
        if m:
            t2 = t2[:m.start()] + entry + t2[m.start():]
        else:  # no history yet - start one after the description block
            m2 = re.search(r"^## Description:.*?\n\n", t2, re.S | re.M)
            at = m2.end() if m2 else len(t2)
            t2 = t2[:at] + entry + t2[at:]
        log.append(f"    changelog -> {txt.name}")
        if write:
            txt.write_text(t2, encoding="utf-8")

    md = d / "README.md"
    if md.exists():
        t = md.read_text(encoding="utf-8")
        # the badge is rewritten whether or not a changelog entry is needed - the entry
        # may already have been written by hand
        t2 = re.sub(r"(https://img\.shields\.io/badge/)v[\d.]+(-Version)",
                    rf"\g<1>v{version}\g<2>", t, count=1)
        already = (re.search(rf"^#{{2,4}}\s*v{re.escape(version)}\b", t2, re.M)         # heading style
                   or re.search(rf"^\|\s*v?{re.escape(version)}\s*\|", t2, re.M))       # table style
        wrote = False
        if not already:
            m = re.search(r"^(#{2,3}\s*(?:Changelog|Version History)\s*)$", t2, re.M)
            if m:
                rest = t2[m.end():]
                # some of these sections are a markdown table, not headings - match the
                # style already in use so the page stays consistent
                tbl = re.search(r"\A\s*\n\|[^\n]*\|\s*\n\|[-: |]+\|\s*\n", rest)
                if tbl:
                    row = f"| {version} | {body} |\n"
                    t2 = t2[:m.end()] + rest[:tbl.end()] + row + rest[tbl.end():]
                else:
                    t2 = t2[:m.end()] + f"\n\n### v{version}\n- {body}\n" + rest
                log.append("    changelog -> README.md")
                wrote = True
        # write even when there was no changelog section to add to - the version badge
        # still needs to move
        if t2 != t:
            if not wrote:
                log.append("    version badge -> README.md")
            if write:
                md.write_text(t2, encoding="utf-8")


SKIP_DIRS = {"docs", "icons", "tools", "skills", "Guide's"}


def sync_root_readme(write: bool, pending: dict | None = None) -> None:
    """Keep the repo README's headline badges and per-mod version cells honest.

    The badges count real rows in the EXMODs rather than restating a number someone
    typed once, so they cannot drift again.
    """
    p = REPO / "README.md"
    t = p.read_text(encoding="utf-8")
    orig = t

    mods = rows = recipes = 0
    for d in sorted(REPO.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in SKIP_DIRS:
            continue
        ex = sorted(d.glob("*.EXMOD"))
        if not ex:
            continue
        mods += 1
        x = json.loads(ex[0].read_text(encoding="utf-8-sig"))
        for b in x.get("Rows") or []:
            tbl = b.get("CurrentFile", "").replace(".json", "").split("-")[-1]
            n = len(b.get("File_Items") or [])
            rows += n
            if tbl == "D_ProcessorRecipes":
                recipes += n
        # version cell, e.g. "| [x](Folder) | `5.2` |"
        ver = (pending or {}).get(d.name) or x.get("version")
        if ver:
            t = re.sub(rf"(\]\({re.escape(d.name)}\)\s*\|\s*)`[^`]*`", rf"\g<1>`{ver}`", t)

    def esc(n: int) -> str:                      # shields.io wants %2C for a comma
        return f"{n:,}".replace(",", "%2C")

    t = re.sub(r"(badge/)\d+(_Mods)", rf"\g<1>{mods}\g<2>", t)
    t = re.sub(r"(badge/)[\d%A-C,]+(-Data_Entries)", rf"\g<1>{esc(rows)}\g<2>", t)
    t = re.sub(r"(badge/)[\d%A-C,]+(-Recipes)", rf"\g<1>{esc(recipes)}\g<2>", t)

    if t == orig:
        print("README.md: already in sync")
        return
    print(f"README.md: {mods} mods, {rows:,} data rows, {recipes:,} recipes")
    if write:
        p.write_text(t, encoding="utf-8")
        print("    written -> README.md")
    else:
        print("    (check only)")


def sync_modinfo(write: bool, pending: dict | None = None) -> None:
    """modinfo.json is what the Mod Manager reads to offer an update, so its `version`
    must match the EXMOD exactly.

    Only the version is synced. The two `description` fields are deliberately different:
    modinfo carries the catalogue blurb (what the mod does, shown in the downloader),
    while the EXMOD carries this release's changes. Do not copy one onto the other.
    """
    p = REPO / "modinfo.json"
    cat = json.loads(p.read_text(encoding="utf-8-sig"))
    changed = []
    for entry in cat.get("mods", []):
        url = (entry.get("files") or {}).get("exmodz", "")
        folder = url.split("/main/")[-1].split("/")[0] if "/main/" in url else None
        if not folder:
            continue
        ex = REPO / folder / f"{folder}.EXMOD"
        if not ex.exists():
            continue
        # in --check mode the EXMOD on disk is not yet updated, so prefer the version
        # this run computed
        ver = (pending or {}).get(folder)
        if ver is None:
            ver = json.loads(ex.read_text(encoding="utf-8-sig")).get("version")
        if entry.get("version") != ver:
            changed.append(f"    {folder}: version {entry.get('version')} -> {ver}")
            entry["version"] = ver
    if not changed:
        print("modinfo.json: already in sync with the EXMODs")
        return
    print("modinfo.json:")
    for c in changed:
        print(c)
    if write:
        p.write_text(json.dumps(cat, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"    written -> modinfo.json  ({len(changed)} fields)")
    else:
        print("    (check only)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mods", nargs="*", help="mod folders to fix (default: all)")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-modinfo", action="store_true",
                    help="skip syncing modinfo.json (that file is what publishes an update)")
    a = ap.parse_args()
    if not a.write:
        a.check = True

    all_mods = list(dict.fromkeys(list(FIXES) + list(DESCRIPTIONS)))
    targets = [m for m in all_mods if not a.mods or m in a.mods]
    unknown = set(a.mods) - set(all_mods)
    if unknown:
        print(f"error: no fixes defined for: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2

    pending: dict[str, str] = {}
    for mod in targets:
        p, x = load(mod)
        before = json.dumps(x, indent=2)
        log: list[str] = []
        if mod in FIXES:
            FIXES[mod](x, log)
        # single-version description (a chained history breaks the Mod Manager downloader)
        if mod in DESCRIPTIONS and x.get("description") != DESCRIPTIONS[mod]:
            x["description"] = DESCRIPTIONS[mod]
            log.append("    description -> single-version form")
        after = json.dumps(x, indent=2)
        pending[mod] = x.get("version")
        update_changelogs(mod, x.get("version"), a.write, log)
        if before == after and not log:
            print(f"{mod}: already up to date")
            continue
        print(f"{mod}:")
        for l in log:
            print(l)
        if before == after:
            continue
        if a.write:
            p.write_text(after + "\n", encoding="utf-8")
            print(f"    written -> {p.relative_to(REPO)}")
        else:
            print("    (check only - re-run with --write to apply)")

    if not a.mods:
        print()
        sync_root_readme(a.write, pending)
        if not a.no_modinfo:
            print()
            sync_modinfo(a.write, pending)
    return 0


if __name__ == "__main__":
    sys.exit(main())
