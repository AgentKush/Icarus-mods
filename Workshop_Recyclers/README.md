# Workshop Recyclers

![Version](https://img.shields.io/badge/version-4.0-blue)
![Author](https://img.shields.io/badge/author-AgentKush-green)
![Compatibility](https://img.shields.io/badge/compatibility-All%20DLCs-brightgreen)

## Overview

Introduces two dedicated recycling machines that enable full material recovery from both Workshop purchases and crafted items. Returns **100% of original Workshop costs** - including Ren, Exotics (purple), and Red Exotics.

## Features

### Biofuel Recycler

| Specification | Value |
|---------------|-------|
| Base Machine | Biofuel Bio-Cleaner (T3) |
| Function | Converts Workshop items to currencies |
| Recipes | 282 |
| Returns | 100% of Ren, Exotics, or Red Exotics |
| Repair Materials | Hammer (same as base machine) |

### Organic Residue Recycler

| Specification | Value |
|---------------|-------|
| Base Machine | Organic Residue Cleanser (T4) |
| Function | Breaks down crafted items into base materials |
| Recipes | 1,343 |
| Use Case | Recover materials from obsolete equipment |
| Repair Materials | Hammer (same as base machine) |

### Combined Statistics

| Metric | Value |
|--------|-------|
| Total Recipes | 1,625 |
| Workshop Items Recyclable | 282 |
| Crafted Items Recyclable | 1,343 |

## Currency Returns

Workshop items return **100% of their original purchase cost**:

| Cost Type | Returns | Count |
|-----------|---------|-------|
| Credits only | 100% Ren | 165 |
| Exotics only | 100% Exotics (purple) | 12 |
| Red Exotics only | 100% Red Exotics | 23 |
| Credits + Exotics | 100% Ren + 100% Exotics | 64 |
| Credits + Red Exotics | 100% Ren + 100% Red Exotics | 18 |

### Example Returns

| Item | Original Cost | Returns (100%) |
|------|---------------|----------------|
| CHAC Pistol | 500 Ren + 250 Exotics | 500 Ren + 250 Exotics |
| Carbon Armor Alpha | 50 Ren + 50 Exotics | 50 Ren + 50 Exotics |
| Inaris Bravo Tools | 200 Ren + 200 Red Exotics | 200 Ren + 200 Red Exotics |
| Larkwell Tools | 400 Exotics | 400 Exotics |
| Explorer's Backpack | 100 Ren + 250 Exotics | 100 Ren + 250 Exotics |
| IC-001 Extractor | 500 Exotics | 500 Exotics |
| IC-001 Radar | 400 Exotics | 400 Exotics |
| Agents Legendary Weapons | Special | 125 Red Exotics each |

### Agents Legendary Weapons

All 8 Agents of Icarus DLC legendary weapons are recyclable:

- Black Wolf Revolver → 125 Red Exotics
- Scorpion Rifle → 125 Red Exotics
- Sandworm Crossbow → 125 Red Exotics
- Golem Gauntlet → 125 Red Exotics
- Legendary Bow → 125 Red Exotics
- Legendary Sniper → 125 Red Exotics
- Slug Launcher → 125 Red Exotics
- Ice Mammoth Sledgehammer → 125 Red Exotics

## Technical Specifications

| Metric | Value |
|--------|-------|
| Total Modifications | 1,637 |
| New Machines | 2 |
| Recipe Entries | 1,625 |

### Files Modified
- `Crafting-D_RecipeSets.json` (2 entries)
- `Traits-D_Processing.json` (2 entries)
- `Traits-D_Itemable.json` (2 entries)
- `Items-D_ItemsStatic.json` (2 entries)
- `Items-D_ItemTemplate.json` (2 entries)
- `Talents-D_Talents.json` (2 entries)
- `Crafting-D_ProcessorRecipes.json` (1,625 entries)

## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus
5. Craft recyclers at the appropriate workstation

## Gameplay Notes

- Returns **100% of original currency costs** (full refund)
- Items costing both Ren and Exotics return both currencies
- Enables inventory cleanup with zero loss
- Strategic for managing Workshop credit and exotic economy
- Useful for recovering materials from outdated gear
- Both machines repairable with any hammer (same as base machines)

## Compatibility

| Mod | Status |
|-----|--------|
| FastProcessing (v4.0+) | ✅ Full recipe support |
| Agent's BioLab | ✅ Compatible |
| Hidden Building Pieces | ✅ Compatible |
| All AgentKush mods | ✅ Compatible |

## Version History

| Version | Changes |
|---------|---------|
| 4.0 | **Major update:** All workshop items now return 100% of original costs. Added 2 missing recipes (Shengong Delta Axe, PlantBoss Inhaler). Fixed 74 currency references (Exotic1 → Meta_Resource). Fixed 28 item name typos. Fixed hammer repair by using base game Deployable_2000 durability. |
| 3.9 | Added missing Shengong Delta Axe recipe, fixed currency return amounts |
| 3.8 | Fixed repair functionality - uses same materials as base machines |
| 3.5 | Fixed Agents legendary weapons to return 125 Red Exotics each |
| 3.4 | Fixed dual currency returns - items costing Credits + Exotics now return both |
| 3.3 | Fixed exotic returns - items costing Exotics or Red Exotics now return correct currency |
| 3.2 | Added cloth armor, brutalist furniture, beacons, lab equipment recipes |
| 3.1 | Added missing workshop items (envirosuits, carbon armor, backpacks, modules) |
| 3.0 | Major cleanup - fixed 63 broken item references, removed 136 invalid recipes |
| 2.9 | Added lightning rod deconstruction recipes |
| 2.8 | Fixed tech tree positioning, added paint deconstruction recipes |

---

*Part of the [AgentKush Icarus Mods](https://github.com/AgentKush/Icarus-mods) collection*
