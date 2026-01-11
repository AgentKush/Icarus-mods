# Workshop Recyclers

![Version](https://img.shields.io/badge/version-3.5-blue)
![Author](https://img.shields.io/badge/author-AgentKush-green)
![Compatibility](https://img.shields.io/badge/compatibility-All%20DLCs-brightgreen)

## Overview

Introduces two dedicated recycling machines that enable material recovery from both Workshop purchases and crafted items. Returns the correct currencies based on original Workshop costs - including Ren, Exotic1 (purple), and Exotic_Red.

## Features

### Biofuel Recycler

| Specification | Value |
|---------------|-------|
| Function | Converts Workshop items to currencies |
| Recipes | 280 |
| Returns | Ren, Exotic1, or Exotic_Red based on original cost |

### Organic Residue Recycler

| Specification | Value |
|---------------|-------|
| Function | Breaks down crafted items into base materials |
| Recipes | 1,343 |
| Use Case | Recover materials from obsolete equipment |

### Combined Statistics

| Metric | Value |
|--------|-------|
| Total Recipes | 1,623 |
| Workshop Items Recyclable | 280 |
| Crafted Items Recyclable | 1,343 |

## Currency Returns

Workshop items return currencies based on their original purchase cost:

| Cost Type | Returns | Count |
|-----------|---------|-------|
| Credits only | Ren | 165 |
| Exotic1 only | Exotic1 (purple) | 12 |
| Exotic_Red only | Exotic_Red | 23 |
| Credits + Exotic1 | Ren + Exotic1 | 62 |
| Credits + Exotic_Red | Ren + Exotic_Red | 18 |

### Example Returns

| Item | Original Cost | Returns |
|------|---------------|---------|
| CHAC Pistol | 500 Credits + 250 Exotic1 | 250 Ren + 125 Exotic1 |
| Carbon Armor Alpha | 50 Credits + 50 Exotic1 | 25 Ren + 25 Exotic1 |
| Inaris Bravo Tools | 200 Credits + 200 Exotic_Red | 100 Ren + 100 Exotic_Red |
| Shengong Echo Tools | 150 Exotic_Red | 75 Exotic_Red |
| Larkwell Tools | 400 Exotic1 | 200 Exotic1 |
| Agents Legendary Weapons | Special | 125 Exotic_Red each |

### Agents Legendary Weapons

All 8 Agents of Icarus DLC legendary weapons are recyclable:

- Black Wolf Revolver → 125 Exotic_Red
- Scorpion Rifle → 125 Exotic_Red
- Sandworm Crossbow → 125 Exotic_Red
- Golem Gauntlet → 125 Exotic_Red
- Legendary Bow → 125 Exotic_Red
- Legendary Sniper → 125 Exotic_Red
- Slug Launcher → 125 Exotic_Red
- Ice Mammoth Sledgehammer → 125 Exotic_Red

## Technical Specifications

| Metric | Value |
|--------|-------|
| Total Modifications | 1,635 |
| New Machines | 2 |
| Recipe Entries | 1,623 |

### Files Modified
- `Crafting-D_RecipeSets.json` (2 entries)
- `Traits-D_Processing.json` (2 entries)
- `Traits-D_Itemable.json` (2 entries)
- `Items-D_ItemsStatic.json` (2 entries)
- `Items-D_ItemTemplate.json` (2 entries)
- `Talents-D_Talents.json` (2 entries)
- `Crafting-D_ProcessorRecipes.json` (1,623 entries)

## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus
5. Craft recyclers at the appropriate workstation

## Gameplay Notes

- Returns ~50% of original currency costs
- Items costing both Credits and Exotics return both currencies
- Enables inventory cleanup without total loss
- Strategic for managing Workshop credit and exotic economy
- Useful for recovering materials from outdated gear

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
| 3.5 | Fixed Agents legendary weapons to return 125 Exotic_Red each |
| 3.4 | Fixed dual currency returns - items costing Credits + Exotics now return both |
| 3.3 | Fixed exotic returns - items costing Exotic1 or Exotic_Red now return correct currency |
| 3.2 | Added cloth armor, brutalist furniture, beacons, lab equipment recipes |
| 3.1 | Added missing workshop items (envirosuits, carbon armor, backpacks, modules) |
| 3.0 | Major cleanup - fixed 63 broken item references, removed 136 invalid recipes |
| 2.9 | Added lightning rod deconstruction recipes |
| 2.8 | Fixed tech tree positioning, added paint deconstruction recipes |
| 2.7 | Previous stable release |

---

*Part of the [AgentKush Icarus Mods](https://github.com/AgentKush/Icarus-mods) collection*
