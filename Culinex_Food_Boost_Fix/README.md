<div align="center">

# Culinex Food Boost Fix

[![Version](https://img.shields.io/badge/v2.9.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Fixes Chef's Backpack 25% food effectiveness boost for all 206 foods/drinks/tonics. Adds Raw Meat to Chicken butchery recipe

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

Fixes the Culinex (Chef's Backpack) 25% food effectiveness boost so it actually works when cooking food while wearing the backpack.

The vanilla game gives the Chef's Backpack a 25% cooked food effectiveness bonus, but the devs forgot to hook it up to most food items. This means wearing the backpack while cooking has zero effect on the food's buff strength for nearly every recipe in the game.

This mod fixes **206 food items** so the 25% effectiveness boost from the Chef's Backpack properly applies when you cook while wearing it.

### How It Works
- Equip the Culinex (Chef's) Backpack
- Cook any food while wearing it
- The resulting food will have 25% stronger buff stats
- Also works with Larkwell White Armor set bonus (+20%) — they stack to +45%

### Bonus Feature
- Adds Raw Chicken recipe to the Butchery Bench and Advanced Butchery Bench

## Tooltips

All 206 food items display their Chef's Backpack boosted stats and a Food Rating (S/A/B/C/D) based on efficiency per stomach slot.

## Compatibility

- ✅ Compatible with all AgentKush mods
- ⚠️ May conflict with other mods modifying `Traits-D_Itemable.json`

## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus

## Changelog

### v2.9.1 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v2.9
- **Crash fix:** Fixed remaining `D_ItemsStatic` reference in `Raw_Chicken_Butchery` recipe input. The input for `Raw_Meat` was still pointing to `D_ItemsStatic`, which caused an `EXCEPTION_ACCESS_VIOLATION` when opening the Butcher Bench. Changed to `D_ItemTemplate` (Raw_Meat exists in both tables). All recipe references now use `D_ItemTemplate` exclusively.

### v2.8
- Crash fix: Fixed 1 recipe output from D_ItemsStatic to D_ItemTemplate (prevented crash when opening crafting stations).

### v2.6
- Added 15 new DLC food/drink/tonic modifier states with Chef's Backpack bonus descriptions
- Added: AntiRadiation_Tonic, Antibiotic_Tonic, Antiparasitic_Tonic, Antipoison_Tonic, Ape_Tonic, Blood_Thinning_Tonic, Cooked_Banana, Drink_Cooling, Drink_Energised, Drink_Heated, Drink_Water, Health_Enhancement_Tonic, Stamina_Enhancement_Tonic, Strength_Enhancement_Tonic, Sustenence_Enhancement_Tonic

### v2.5
- Added Animal Gruel Rotten and Animal Silage entries
- Mod now covers 191 entries total

### v2.4
- Added Food Rating system (S/A/B/C/D) based on stats-per-stomach-slot efficiency

### v2.3
- Simplified tooltips: show only boosted values
- Added missing Thermos Coffee With Cream
- Added Raw Food, Spoiled Meat, Seed entries
- Added 15 Animal Feeds, 5 Animal Gruels, Animal Silage, and Filtered Trough Water

### v2.2
- Cleaned up tooltip formatting

### v2.1
- Added Chef's Backpack boosted stats to all food tooltips

### v2.0
- Major fix: switched from Level2 (field merge) to Level1 (full row replacement)
- Removed 6 banana foods that no longer exist in the game
- Updated all 169 food entries to match current game data

### v1.2
- Added 12 new food items (175 total)
- Fixed 91 items losing vanilla talent bonuses

### v1.1
- Rebuilt from current game data (163 foods)
- Fixed fish food items to preserve Fish Food talent

### v1.0
- Initial release with 158 food items
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
