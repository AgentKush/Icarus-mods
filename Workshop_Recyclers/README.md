<div align="center">

# Workshop Recyclers

[![Version](https://img.shields.io/badge/v5.8.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Two recycling machines (Biofuel T3 + Organic T4) plus an Incinerator for instant item destruction. 5,312 recipes: 1,943 deconstruct + 315 recycle + 3,051 incinerate + 3 crafting

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Overview

Introduces two dedicated recycling machines that enable full material recovery from both Workshop purchases and crafted items, plus an **Incinerator** for instant item destruction. Returns **100% of original Workshop costs** — including Ren, Exotics (purple), Red Exotics, Biomass, and Uranium. Deconstruction stops at processed materials (ingots, refined goods) — no raw ores or pyritic crusts.

## Features

### Biofuel Recycler

| Specification | Value |
|---------------|-------|
| Base Machine | Biofuel Bio-Cleaner (T3) |
| Crafted At | Machining Bench / Fabricator |
| Function | Recycles workshop items into currencies AND crafted items into materials |
| Repair Materials | Electronics (hammer repairable) |

### Organic Residue Recycler

| Specification | Value |
|---------------|-------|
| Base Machine | Organic Residue Cleanser (T4) |
| Crafted At | Fabricator |
| Function | Recycles workshop items into currencies AND crafted items into materials |
| Repair Materials | Electronics (hammer repairable) |

### Incinerator

| Specification | Value |
|---------------|-------|
| Base Machine | Electric Furnace visual |
| Crafted At | Fabricator / Manufacturer |
| Function | Instantly destroys any item — no output |
| Power | Electric (2,500 mW) |
| Unlock | Requires Organic Recycler talent |
| Recipes | 3,051 items (every item in the game) |

### Combined Statistics

| Metric | Value |
|--------|-------|
| Total Recipes | 5,312 |
| Workshop Items Recyclable | 315 |
| Crafted Items Deconstructable | 1,943 |
| Incineratable Items | 3,051 |

## Currency Returns

Workshop items return **100% of their original replication cost** as physical items:

| Workshop Currency | Returns As | Count |
|-------------------|------------|-------|
| Credits only | Ren | 195 |
| Exotics (purple) only | Meta_Resource | 12 |
| Credits + Exotics | Ren + Meta_Resource | 74 |
| Red Exotics only | Exotic_Red | 15 |
| Credits + Red Exotics | Ren + Exotic_Red | 21 |
| Biomass + Credits | Biomass + Ren | 8 |
| Uranium + Credits | Uranium_Rod + Ren | 8 |
| Uranium only | Uranium_Rod | 2 |

### How It Works

Workshop currencies cannot be directly output by processor recipes (the game engine silently drops `D_MetaCurrency` outputs). This mod maps each currency to its physical item equivalent:

| Currency | Physical Item | Data Table |
|----------|---------------|------------|
| Credits | Ren | D_ItemTemplate |
| Exotic1 (purple) | Meta_Resource | D_ItemTemplate |
| Exotic_Red | Exotic_Red | D_ItemTemplate |
| Biomass | Biomass | D_ItemTemplate |
| Exotic_Uranium | Uranium_Rod | D_ItemTemplate |

### Example Returns

| Item | Original Cost | Returns |
|------|---------------|---------|
| Basic Envirosuit | 25 Credits | 25 Ren |
| Module Tracker | 50 Credits + 10 Exotics | 50 Ren + 10 Meta_Resource |
| Inaris Alpha Axe | 400 Exotics | 400 Meta_Resource |
| Shengong Echo Axe | 150 Red Exotics | 150 Exotic_Red |
| Shengong Delta Bow | 250 Credits + 50 Red Exotics | 250 Ren + 50 Exotic_Red |
| Sandworm Inhaler | 100 Credits + 10 Biomass | 100 Ren + 10 Biomass |
| Bulky Armor Head | 100 Credits + 75 Uranium | 100 Ren + 75 Uranium_Rod |

## Technical Specifications

| Metric | Value |
|--------|-------|
| Total Modifications | 5,350 |
| New Machines | 3 |
| Recipe Entries | 5,312 |

### Files Modified
- `Crafting-D_RecipeSets.json` (3 entries)
- `Traits-D_Processing.json` (3 entries)
- `Traits-D_Itemable.json` (3 entries)
- `Items-D_ItemsStatic.json` (3 entries)
- `Items-D_ItemTemplate.json` (3 entries)
- `Talents-D_Talents.json` (3 entries)
- `Crafting-D_ProcessorRecipes.json` (5,312 entries)
- `Traits-D_Durable.json` (1 entry)


## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus
5. Craft recyclers at the appropriate workstation

## Gameplay Notes

- Returns **100% of original replication costs** as physical items
- Items costing multiple currencies (e.g. Credits + Exotics) return both as physical items
- Deconstruction returns processed materials — **no raw ores or pyritic crusts**
- A Steel Pickaxe returns Steel Ingots, not Metal Ore
- Enables inventory cleanup with zero loss
- Strategic for managing Workshop credit and exotic economy
- Useful for recovering materials from outdated gear
- **Incinerator** instantly destroys any item — covers every item in the game (3,051 recipes)
- Incinerator crafted at Fabricator (20 Steel Ingot, 10 Electronics, 40 Concrete Mix, 4 Glass)
- Note: FPS may dip while the Incinerator UI is open due to recipe count — returns to normal when closed
- All three machines repairable with Electronics + any hammer

## Compatibility

| Mod | Status |
|-----|--------|
| FastProcessing (v4.5+) | Compatible |
| Agent's BioLab | Compatible |
| Hidden Building Pieces | Compatible |
| All AgentKush mods | Compatible |

## Version History

| Version | Changes |
|---------|---------|
| 5.8.1 | New icon and banner, drawn from the mod's live data. No gameplay change. |
| 5.8 | Updated for the November 2026 game update. Removed 41 recipes for items the game no longer has (the update deleted the Electric Motor, Cobalt Ore, Cobalt Ingot and the explosive sniper rounds; the rest were unreleased workshop items or items with no item data), so the machines no longer list recipes that can never run. Fixed 25 recipes that gave nothing: 17 Platinum Sheath and 4 saddle outputs used the wrong item name, and 4 deconstruct recipes tried to output animal carcasses, which cannot be made (they now give Wool or a Ram, Sheep or Pig head, matching the vanilla recipes). Removed Deconstruct Raw Meat (no single vanilla source to return), 3 duplicate recipes that overwrote each other, and an unused timing field from every incinerate recipe. Added incinerate recipes for the 17 new items. 5,312 recipes: 1,943 deconstruct, 315 recycle, 3,051 incinerate and 3 crafting. |
| 5.7 | **June 2026 update fix.** The Incinerator and Biofuel Recycler stopped placing after the update renamed the meshes they used. Both now point at their correct machine models (Incinerator → electric furnace, Biofuel Recycler → cleaning device). |
| 5.5 | **Full incinerate coverage.** Added 886 missing recipes (frozen wood, frozen ore, raw ores, food, building pieces, seeds). 3,054 total incinerate recipes — every item in the game. Fixed icon (invalid asset path), mesh (non-existent reference), and tech tree overlap. |
| 5.4 | **Incinerator fixes:** Fixed missing tech tree icon (invalid asset path), fixed placement issue (non-existent mesh reference), repositioned tech tree nodes to avoid overlap with vanilla T4 Fabricator items. |
| 5.3 | **New machine: Incinerator.** Electric-powered processor that instantly destroys any item with no output. 2,168 incinerate recipes covering every recyclable/deconstructable item. Crafted at Fabricator/Manufacturer. Unlocked after Organic Recycler. |
| 5.2 | **Crash fix:** Fixed EXCEPTION_ACCESS_VIOLATION crash caused by incorrect DataTableName references in v5.1 recipes. All recipe outputs now correctly use D_ItemTemplate, all inputs use D_ItemsStatic. Fixed 130 input RowName mismatches from new recipes using D_ItemTemplate names instead of D_ItemsStatic names. |
| 5.1 | Added 158 new recipes: 6 mission items (Gyro, Navigation, Thruster, Enzyme Storage, High-Tech Assembled, Recombined Tech), 10 DLC items (Lava Hunter trophies, Homestead decor), 29 national flags, 18 missing workshop items (Carbon Armor Alpha/Beta, Larkwell White armor, Shengong hammers/sickles, Biolab inhalers, Inaris items, 9Diamonds Shield), 30 food recipes, 16 furniture/decor, 13 armor/equipment, 10 stations/deployables, 26 misc (fertility serums, saddles, platinum tools, building pieces). All Deconstruct recipes return 100% crafting materials. All 333 workshop items now covered. |
| 5.0 | **Complete rebuild:** Fixed root cause of all currency outputs failing — processor recipes cannot output D_MetaCurrency, so all 317 workshop recycle recipes now output physical items (Ren, Meta_Resource, Exotic_Red, Biomass, Uranium_Rod) via D_ItemTemplate. Regenerated all 1,808 deconstruct recipes from current game data using ItemStaticData lookup. Removed 30 raw ore and pyritic crust deconstruct recipes, stripped ore/crust outputs from 33 more — deconstruction now stops at ingots and refined materials. All crafting times matched to base game. Zero broken references. |
| 4.7 | Fixed MetaResource currency outputs, added 285 new Recycle_ recipes. |
| 4.6 | Fixed 47 recipes to return correct exotic items. |
| 4.5 | Added 60 new recycle recipes for DLC workshop items. |
| 4.4 | Fixed 135 recipe output references. |
| 4.3 | Game update compatibility fix — fixed 57 broken input refs, 12 broken output refs, removed 62 deleted items, added 12 new recipes. |
| 4.2 | Repair fix — both recyclers now hammer repairable with custom D_Durable entry. |
| 4.1 | Week 213+ compatibility update. |
| 4.0 | Major update — 100% workshop cost returns, fixed 74 currency refs, 28 name typos. |
| 3.0 | Major cleanup — fixed 63 broken item references, removed 136 invalid recipes. |
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
