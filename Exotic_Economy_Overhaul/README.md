<div align="center">

# Exotic Economy Overhaul

[![Version](https://img.shields.io/badge/v2.2-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Full currency exchange system with 66 recipes. Buy and sell materials with Ren, convert between exotics and currencies, cross-convert ingots, and bulk smelt ores at the correct furnaces/benches. Covers all Dangerous Horizons materials

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Overview

66 currency exchange and bulk processing recipes. Convert between Ren, Exotics, Biomass, Uranium and all ingots. Every material you can buy can also be sold back. Bulk smelt ores at the correct furnaces, Chemistry Bench, and Glassworking Bench — recipes auto-appear alongside the base game smelting recipes.

## Features

### Buy Materials with Ren — 21 recipes (Machining Bench + Fabricator)

Spend workshop currency on crafting materials:

- Refined Metal, Refined Copper, Steel Ingot, Titanium Ingot, Platinum Ingot, Refined Gold
- Electronics, Carbon Fiber, Composites, Epoxy
- Gunpowder, Volatile Substance, Cold Steel Ingot
- Cobalt Ingot, Lithium Refined, Ruby Shaped, Shaped Obsidian
- Aluminium, Copper Wire, Glass, Concrete Mix

### Sell Materials for Ren — 21 recipes (Machining Bench + Fabricator)

Convert surplus materials back to workshop currency — every buyable material can be sold back:

- Refined Metal, Refined Copper, Steel, Titanium, Platinum, Gold → Ren
- Cobalt, Lithium, Ruby, Obsidian, Aluminium → Ren
- Carbon Fiber, Composites, Electronics, Cold Steel → Ren
- Copper Wire, Glass, Concrete Mix, Epoxy, Gunpowder, Volatile → Ren

### Exotic Processing — 3 recipes (Fabricator)

- Bulk raw exotic → refined exotic (20 raw → 10 refined)
- Condense exotics (10 → 5 condensed)
- Expand condensed back to regular (1 → 2)

### Exotic/Currency to Ren — 4 recipes (Fabricator)

- Exotic Red → Ren (5 exotic = 200 Ren)
- Condensed Exotics → Ren (1 = 100 Ren)
- Uranium Rod → Ren (5 = 150 Ren)
- Biomass → Ren (10 = 100 Ren)

### Ingot Cross-Conversion — 8 recipes (Machining Bench + Fabricator)

Trade between metal types at diminishing returns:

- Copper → Steel → Titanium → Platinum
- Gold ↔ Platinum
- Platinum → Cobalt → Lithium → Cold Steel

### Bulk Ore Smelting — 9 recipes (at correct game stations)

Smelt 20 ore into 10 refined in one batch. Recipes auto-appear at the same stations the base game uses for that ore type:

| Recipe | Input | Output | Station(s) |
|--------|-------|--------|------------|
| Bulk Metal Smelt | 20 Metal Ore | 10 Refined Metal | Stone/Concrete/Electric Furnace |
| Bulk Copper Smelt | 20 Copper Ore | 10 Refined Copper | Stone/Concrete/Electric Furnace |
| Bulk Gold Smelt | 20 Gold Ore | 10 Refined Gold | Concrete/Electric Furnace |
| Bulk Titanium Smelt | 20 Titanium Ore | 10 Titanium Ingot | Concrete/Electric Furnace |
| Bulk Platinum Smelt | 20 Platinum Ore | 10 Platinum Ingot | Concrete/Electric Furnace |
| Bulk Bauxite Refine | 30 Bauxite | 15 Aluminium | Concrete/Electric Furnace |
| Bulk Cobalt Smelt | 20 Cobalt Ore | 10 Cobalt Ingot | Concrete/Electric Furnace |
| Bulk Lithium Refine | 20 Lithium Ore | 10 Lithium Refined | Chemistry Bench |
| Bulk Ruby Cut | 20 Ruby Ore | 10 Ruby Shaped | Glassworking Bench |

## Icons

Every recipe sets `ItemIconOverride` to its output item, so the crafting list shows the made item's icon. Earlier versions left this to auto-resolve, which made the added conversion recipes show **ICON MISSING** in-game — v2.2 sets the icon explicitly on all 66 recipes.

## Compatibility

- ✅ Compatible with all other mods
- ✅ Compatible with FastProcessing mods

## Installation

Import `Exotic_Economy_Overhaul.EXMODZ` via Icarus Mod Manager.

## Version History

- **v2.2** - Fixed **ICON MISSING** on every recipe by setting `ItemIconOverride` to each recipe's output item. All 66 recipes now display the correct icon in the crafting list. (Recipes function identically to v2.1; this is a display fix.)
- **v2.1** - Crash fix: All recipe outputs corrected from D_ItemsStatic to D_ItemTemplate (caused EXCEPTION_ACCESS_VIOLATION). Added 14 missing recipes: Refined Copper and Refined Metal buy recipes, plus sell-back recipes for all 12 materials that could previously only be bought. Every material now has both buy and sell. 66 total recipes.
- **v2.0** - Complete rebuild. Fixed missing RequiredMillijoules on all recipes (root cause of mod being broken). Added 25 new recipes: 9 bulk ore smelting at correct furnaces/benches, Cobalt/Lithium/Ruby/Obsidian/Aluminium buy/sell, Uranium/Biomass to Ren, 3 new cross-conversions, Copper Wire/Glass/Concrete Mix purchases. 52 total recipes.
- **v1.1** - Rebuilt with correct game item names. 27 recipes.
- **v1.0** - Initial release (had invalid item references)
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
