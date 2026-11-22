<div align="center">

# Workshop Recyclers

[![Version](https://img.shields.io/badge/v5.9.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Two recycling machines (Biofuel T3 + Organic T4) plus an Incinerator for instant item destruction. 5,312 recipes: 1,943 deconstruct + 314 recycle + 3,052 incinerate + 3 crafting

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Overview

Introduces two dedicated recycling machines that enable full material recovery from both Workshop purchases and crafted items, plus an **Incinerator** for instant item destruction. Returns **100% of original Workshop costs** — including Ren, Exotics (purple), Red Exotics, Biomass, and Uranium. Deconstructing a crafted item returns its base crafting cost, which is mostly processed materials (ingots, refined goods); items made straight from ore, such as Flint and Black Wolf arrows, return that ore.

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
| Recipes | 3,052 items (every item in the game) |

### Combined Statistics

| Metric | Value |
|--------|-------|
| Total Recipes | 5,312 |
| Workshop Items Recyclable | 314 |
| Crafted Items Deconstructable | 1,943 |
| Incineratable Items | 3,052 |

## Currency Returns

Workshop items return **100% of their original replication cost** as physical items:

| Workshop Currency | Returns As | Count |
|-------------------|------------|-------|
| Credits only | Ren | 187 |
| Exotics (purple) only | Meta_Resource | 12 |
| Credits + Exotics | Ren + Meta_Resource | 62 |
| Red Exotics only | Exotic_Red | 15 |
| Credits + Red Exotics | Ren + Exotic_Red | 21 |
| Biomass + Credits | Biomass + Ren | 8 |
| Uranium + Credits | Uranium_Rod + Ren | 8 |
| Uranium only | Uranium_Rod | 1 |

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
| Total Modifications | 5,335 |
| New Machines | 3 |
| Recipe Entries | 5,312 |

### Files Modified
- `Traits-D_Meshable.json` (2 entries)
- `Crafting-D_RecipeSets.json` (3 entries)
- `Traits-D_Processing.json` (3 entries)
- `Traits-D_Itemable.json` (3 entries)
- `Items-D_ItemsStatic.json` (3 entries)
- `Items-D_ItemTemplate.json` (3 entries)
- `Talents-D_Talents.json` (3 entries)
- `Traits-D_Durable.json` (1 entry)
- `Crafting-D_ProcessorRecipes.json` (5,312 entries)
- `Inventory-D_InventoryInfo.json` (1 entry)
- `Traits-D_Inventory.json` (1 entry)


## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus
5. Craft recyclers at the appropriate workstation

## Gameplay Notes

- Returns **100% of original replication costs** as physical items
- Items the game crafts several at a time return the materials for the smallest batch that comes out whole: 100 Steel Screws return 1 Steel Ingot, 5 Copper Bolts return 1 Wood + 1 Copper Ingot. A smaller stack waits in the machine until there are enough
- Items costing multiple currencies (e.g. Credits + Exotics) return both as physical items
- Deconstruction returns the item's base crafting cost, mostly processed materials; items made straight from ore (such as Flint and Black Wolf arrows) return that ore
- A Steel Pickaxe returns Steel Ingots, not Metal Ore
- Enables inventory cleanup with zero loss
- Returns are the base crafting cost. Crafting-cost talents (for example Discount Wood) let you craft some items for less, so recycling those gives back a little more than you paid
- Strategic for managing Workshop credit and exotic economy
- Useful for recovering materials from outdated gear
- **Incinerator** instantly destroys any item — covers every item in the game (3,052 recipes)
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
| 5.9.1 | **Duplication fix.** 141 deconstruct recipes gave back more than the item cost, or the wrong materials. Items the game crafts several at a time returned the whole craft's materials for each single item: 1 Steel Screw returned a Steel Ingot (the game makes 100 screws from one), and 1 arrow, bolt, nail or throwing weapon returned what 3 to 10 of them cost. These 127 recipes now return exactly what the items cost: where one item's share comes out whole it still takes one item (1 Water Bomb returns 1 Leather and 3 Fiber), otherwise it takes the smallest batch that does (100 Steel Screws return 1 Steel Ingot, 5 Copper Bolts return 1 Wood and 1 Copper Ingot). A smaller stack waits in the machine until there are enough. 4 Raw Chicken also need 10 Raw Stringy Meat to make a Rooster Vestige, since butchering a vestige gives both. The Cold Steel Ingot and the Distilled Miasmic Coating return their plain recipe (1 Steel Ingot + 1 Super Cooled Ice, and 1 Crystallised Miasma), so recycling them no longer makes Shaped Ruby or Active Lithium. The Wood Floor, Wood Wall, Wood Wall Angled and Wood Roof/Ramp return the Carpentry Bench cost, which is lower than the hand-craft cost, and the Splint returns its rope recipe's cost (6 Rope instead of 100 Fiber). Ren returns 10 Tainted Plant DNA (the game's rate) instead of 100, the Homestead Fireplace Cap no longer adds 10 Iron Ingots, and the Clay, Scoria and Obsidian sledgehammer attachments and the Sandwyrm Queen Backpack and Bow return the materials they are made from. Also removed a recycle recipe that turned the First Cohort Envirosuit, which costs nothing in the Workshop, into 25 Ren, and a duplicate Bacon Butty recipe that turned stacks under 3 into Organic Resin. 5,312 recipes: 1,943 deconstruct, 314 recycle, 3,052 incinerate and 3 crafting. |
| 5.9 | Updated for the 19 November 2026 game update. Added deconstruct and incinerate recipes for the new Advanced Armor Stand. Deconstructing it returns what it costs to build: 120 Aluminium, 4 Electronics, 60 Steel Screws and 8 Composites. 5,314 recipes: 1,944 deconstruct, 315 recycle, 3,052 incinerate and 3 crafting. |
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
