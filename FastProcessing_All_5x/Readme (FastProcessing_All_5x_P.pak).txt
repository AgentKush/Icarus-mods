FastProcessing_All_5x_P.pak
----------------------------------------------------------------------
Mod Version: 5.2

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
All crafting and processing 5x faster. 2235 recipes rebuilt from the November 2026 game data. Water recipes have 500 MJ floor to prevent fluid bugs.


Ver 5.2
Fixed the speed maths - 896 recipes were set to instant instead of 5x faster, because
recipes with no listed energy cost were read as 0 instead of the game's default 2,500.
Every recipe is now recomputed from the November 2026 game values: exactly 5x faster
than vanilla, never slower, and water recipes keep the 500 MJ minimum. Also corrects 70
recipes whose cost had drifted from the current vanilla value, removes the 2 recipes the
game deleted and adds the 62 it has gained. 2,235 recipes.

Ver 5.1
Reverted the v4.9 over-correction of the Scoria roof corner recipe — the game's recipe name really is the misspelled "Scoria_Bick_Roof_Corner", so the mod now matches it and that recipe gets the speed boost again.

Ver 5.0
Fixed: Water dropping to negative on dedicated servers when crafting water-consuming recipes (soups, dough, pickled items, geode lamps, tempered glass, etc.). The 500 MJ water floor was lost in the DangerousHorizons recipe rebuild; it is now restored and applied to all 67 water-consuming recipes.

Ver 4.7
Added 4 new wolf recipes (Carcass_Juvenile_Snow_Wolf, Carcass_Juvenile_Wolf, Fertility_Serum_Wolf, Fertility_Serum_Wolf_Exotic). Total recipes: 2,175.

Ver 4.4
Fixed: Water going into negatives when crafting recipes that consume water (soups, dough, pickled items, geode lamps, etc.). Applied 500 MJ minimum floor to all 68 water-consuming recipes. Non-water recipes unchanged.

Ver 4.3
Updated for latest game patch. Added new recipes from recent updates.

## Files Modified:
  Crafting-D_ProcessorRecipes (2235 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download FastProcessing_All_5x.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods