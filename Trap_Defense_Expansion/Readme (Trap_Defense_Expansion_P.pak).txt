Trap_Defense_Expansion_P.pak
----------------------------------------------------------------------
Mod Version: 1.3

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
Defense expansion with 23 recipes using real game items. Unlocks 4 elemental landmines (Poison/Burn/Shock/Freeze) that were previously enemy-only. Adds cheaper fortifications, early-game traps, hedgehog defenses without rare drops, and batch crafting packs.



Ver 1.3
Fixed the crafting sound on the 12 Fabricator-tier recipes (all 4 elemental landmines,
their 4 direct crafts, Batch Landmines, Landmine Field Kit, Mammoth Trap, Lava Mine).
They pointed Audio at a D_CraftingAudioData row named "Fabricator", which has never
existed in that table - "Fabricator" is a D_RecipeSets name. Those crafts were silent
while Field Landmine and Wolf Trap on the same bench were not. All 12 now use
"MachiningBench", matching vanilla Landmine / IceMammoth_Trap / Lava_Hunter_Mine.

Ver 1.2
Crash fix: Fixed 23 recipe outputs from D_ItemsStatic to D_ItemTemplate. Prevents EXCEPTION_ACCESS_VIOLATION when opening crafting stations.
Ver 1.1
Complete rebuild using real game items. 23 recipes including 4 previously uncraftable elemental landmines.

Ver 1.0
Initial release (placeholder items, replaced in v1.1).

## Files Modified:
  Crafting-D_ProcessorRecipes (23 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Trap_Defense_Expansion.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods