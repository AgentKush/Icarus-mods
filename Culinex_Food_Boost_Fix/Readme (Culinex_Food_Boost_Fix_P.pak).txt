Culinex_Food_Boost_Fix_P.pak
----------------------------------------------------------------------
Mod Version: 2.9

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
Fixes Culinex (Chef's Backpack) 25% food effectiveness boost to apply to all cooked foods. Also adds raw chicken to the butchery bench.



Ver 2.9
Crash fix: the Raw_Chicken_Butchery recipe still pointed its Raw_Meat input at
D_ItemsStatic, which caused an EXCEPTION_ACCESS_VIOLATION when opening the Butcher
Bench. Changed to D_ItemTemplate. Every recipe reference now uses D_ItemTemplate.

Ver 2.8
Crash fix: Fixed 1 recipe output from D_ItemsStatic to D_ItemTemplate. Prevents EXCEPTION_ACCESS_VIOLATION when opening crafting stations.

Ver 2.7
Coverage pass against the current game data.

Ver 2.6
Added 15 new DLC food/drink/tonic modifier states with Chef's Backpack bonus descriptions. Added: AntiRadiation_Tonic, Antibiotic_Tonic, Antiparasitic_Tonic, Antipoison_Tonic, Ape_Tonic, Blood_Thinning_Tonic, Cooked_Banana, Drink_Cooling, Drink_Energised, Drink_Heated, Drink_Water, Healt..

Ver 2.5
Added Animal Gruel Rotten and Animal Silage entries. Mod now covers 191 entries total.

Ver 2.4
Added Food Rating system (S/A/B/C/D) based on stats-per-stomach-slot efficiency.

Ver 2.3
Simplified tooltips: show only boosted values. Added missing Thermos Coffee With Cream. Added Raw Food, Spoiled Meat, Seed entries. Added 15 Animal Feeds, 5 Animal Gruels, Animal Silage, and Filtered Trough Water.

Ver 2.2
Cleaned up tooltip formatting.

Ver 2.1
Added Chef's Backpack boosted stats to all food tooltips.

Ver 2.0
Major fix: switched from Level2 (field merge) to Level1 (full row replacement). Removed 6 banana foods that no longer exist in the game. Updated all 169 food entries to match current game data.

Ver 1.2
Added 12 new food items (175 total). Fixed 91 items losing vanilla talent bonuses.

Ver 1.1
Rebuilt from current game data (163 foods). Fixed fish food items to preserve Fish Food talent.

Ver 1.0
Initial release with 158 food items.

## Files Modified:
  Modifiers-D_ModifierStates  (206 entries)
  Crafting-D_ProcessorRecipes (1 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Culinex_Food_Boost_Fix.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods