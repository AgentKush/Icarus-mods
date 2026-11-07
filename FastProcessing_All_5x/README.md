<div align="center">

# Fast Processing (5x)

[![Version](https://img.shields.io/badge/v5.2-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

All crafting and processing 5x faster. 2,235 recipes rebuilt from the November 2026 game data. Water recipes have 500 MJ floor to prevent fluid bugs

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## What's Included

Covers all base game recipes plus compatibility with:
- Workshop Recyclers
- Hidden Building Pieces
- No Food Spoilage
- Turret Variants
- Culinex Food Boost Fix

## Important Notes

- **Use only ONE FastProcessing variant at a time** (5x, 10x, 15x, 25x, or Instant)
- Compatible with other EXMODZ mods
- Multiplayer compatible — all players need the same mod installed

## Technical Details

- Modifies `RequiredMillijoules` in `D_ProcessorRecipes` for each recipe
- Water-consuming recipes have a minimum floor of 500 MJ to prevent the water system from going negative
- Recipes without water/fluid requirements use standard speed calculations

## Installation

1. Download the `.EXMODZ` file
2. Place in your Mod Manager's mod folder
3. Enable in JimK72's Mod Manager
4. Launch Icarus

## Changelog


### v5.2
- Fixed the speed maths - 896 recipes were set to instant instead of 5x faster, because recipes with no listed energy cost were read as 0 instead of the game's default 2,500. Every recipe is now recomputed from the November 2026 game values: exactly 5x faster than vanilla, never slower, and water recipes keep the 500 MJ minimum. Also corrects 70 recipes whose cost had drifted from the current vanilla value, removes the 2 recipes the game deleted and adds the 62 it has gained. 2,235 recipes.

### v5.1 (2026-06-27)
- Reverted the v4.9 over-correction of the Scoria roof corner recipe — the game's recipe name really is the misspelled "Scoria_Bick_Roof_Corner", so the mod now matches it and that recipe gets the speed boost again.
### v5.0
- **Fixed:** Water dropping to negative (millions) on dedicated servers when crafting water-consuming recipes (soups, dough, pickled items, geode lamps, tempered glass, etc.). The 500 MJ water floor was lost when the recipe list was rebuilt for the DangerousHorizons update; it is now restored and applied to all 67 water-consuming recipes (those with a `ResourceInputs: Water` requirement).

### v4.9
- Fixed typo: `Clay_Bick_Roof_Corner` → `Clay_Brick_Roof_Corner`
- Fixed typo: `Scoria_Bick_Roof_Corner` → `Scoria_Brick_Roof_Corner`

### v4.7
- Added 4 new wolf recipes (Carcass_Juvenile_Snow_Wolf, Carcass_Juvenile_Wolf, Fertility_Serum_Wolf, Fertility_Serum_Wolf_Exotic)
- Total recipes: 2,175

### v4.4
- **Fixed:** Water going into negatives when crafting recipes that consume water (soups, dough, pickled items, geode lamps, etc.)
- Applied 500 MJ minimum floor to all 68 water-consuming recipes
- Non-water recipes unchanged

### v4.3
- Updated for latest game patch
- Added new recipes from recent updates
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
