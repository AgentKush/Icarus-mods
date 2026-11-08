<div align="center">

# Faster Crafting

[![Version](https://img.shields.io/badge/v1.7.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Halves crafting time on all 2,235 recipes across every workbench. Minimum 500 MJ for water recipes

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Changes

Every recipe that has a crafting energy cost (RequiredMillijoules) is reduced by 50%. This affects all stations — Character crafting, Anvil Bench, Machining Bench, Fabricator, Kitchen, Chemistry Bench, and everything else.

This is different from the FastProcessing mods which speed up passive processor machines (furnaces, mortar, etc.). This mod speeds up active crafting where you click the craft button.

## Compatibility

- ✅ Compatible with all FastProcessing mods (they modify D_Processing, this modifies D_ProcessorRecipes)
- ✅ Compatible with Tier Upgrade Forge, Exotic Economy, Trap Defense (additive recipes)

## Installation

Import `Faster_Crafting.EXMODZ` via Icarus Mod Manager.

## Changelog


### v1.7.1 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v1.7
- Fixed the speed maths - 927 recipes were set to instant instead of 2x faster, because recipes with no listed energy cost were read as 0 instead of the game's default 2,500. Every recipe is now recomputed from the November 2026 game values: exactly 2x faster than vanilla, never slower, and water recipes keep the 500 MJ minimum. Also corrects 69 recipes whose vanilla cost the game has changed, removes the 2 recipes the game deleted and adds the 62 it has gained. 2,235 recipes.

### v1.6 (2026-06-27)
- Reverted the v4.9 over-correction of the Scoria roof corner recipe — the game's recipe name really is the misspelled "Scoria_Bick_Roof_Corner", so the mod now matches it and that recipe gets the speed boost again.
### v1.5
- Fixed typo: `Clay_Bick_Roof_Corner` → `Clay_Brick_Roof_Corner`
- Fixed typo: `Scoria_Bick_Roof_Corner` → `Scoria_Brick_Roof_Corner`

### v1.3
- Added 4 new wolf recipes (Carcass_Juvenile_Snow_Wolf, Carcass_Juvenile_Wolf, Fertility_Serum_Wolf, Fertility_Serum_Wolf_Exotic)
- Total recipes: 2,175

### v1.1
- Added 1,211 missing recipes from latest update/DLC (total: 2,163)

### v1.0
- Initial release, 952 recipes halved
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
