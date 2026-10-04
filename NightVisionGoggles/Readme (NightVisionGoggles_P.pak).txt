NightVisionGoggles_P.pak
----------------------------------------------------------------------
Mod Version: 2.2

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
Adds craftable Night Vision Goggles with improved durability, no decay, lighter weight. Craft at Fabricator, Manufacturer, or Machining Bench.



Ver 2.2
Fixed the crafting sound. The recipe pointed Audio at a D_CraftingAudioData row named
"Fabricator", which has never existed in that table - "Fabricator" is a D_RecipeSets
name, and the two tables use different keys. The goggles crafted in silence while every
other recipe on the same bench played its sound. Now set to "MachiningBench", matching
the vanilla Binoculars recipe.

Ver 2.1
Crash fix: Fixed 1 recipe output from D_ItemsStatic to D_ItemTemplate. Prevents EXCEPTION_ACCESS_VIOLATION when opening crafting stations.
Ver 2.0
Added no-decay (Decay_NoDecay) so goggles persist indefinitely. Added durability (Destroyed_Tool, 10,000 HP). Reduced weight from 5.0 to 1.0. Added Machining Bench as crafting station. Updated description.

Ver 1.1
Fixed mod format: converted from legacy structure to current name/author/Rows format.

Ver 1.0
Initial release. Unlocked hidden Night Vision item from game files. Added crafting recipe at Fabricator/Manufacturer.

## Files Modified:
  Items-D_ItemsStatic         (1 entries)
  Items-D_ItemTemplate        (1 entries)
  Traits-D_Itemable           (1 entries)
  Crafting-D_ProcessorRecipes (1 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download NightVisionGoggles.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods