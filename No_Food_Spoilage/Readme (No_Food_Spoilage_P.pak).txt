No_Food_Spoilage_P.pak
----------------------------------------------------------------------
Mod Version: 2.3.1

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
Prevents all food spoilage. Items decay/despawn but never convert to spoiled versions. Covers all 33 decayable entries. Includes composter recipes so raw meats, fish, dairy, vegetables, and fruits can still be manually composted.



Ver 2.3.1
New icon and banner, drawn from the mod's live data. No gameplay change.

Ver 2.3
SAFETY FIX - the mod gave the game's never-decay profile a decay timer, so the 19 things
that are meant to last forever (all four saddle carts, the speeder saddle, the landing
pads, the advanced exotic delivery interface, animal silage and ten mission stasis bags)
could decay. They never decay again. Restored leather curing (Curing Leather turns into
Advanced Leather again - that is crafting, not spoilage). Removed 12 composter recipes
for items that do not exist and fixed 5 that pointed at renamed foods (Fatty T-Bone,
Giant Steak, Berry, Bean, Prickly Pear). Food never spoils; the composter can still turn
food into spoiled food for fertilizer.

Ver 2.2
Restored coconut ripening (young -> mid -> mature) that the no-spoil change had broken; mature coconuts no longer rot. Fixes #10.

Ver 2.1
Crash fix: Fixed 134 recipe outputs from D_ItemsStatic to D_ItemTemplate. Prevents EXCEPTION_ACCESS_VIOLATION when opening crafting stations.
Ver 2.0
Fixed composter bug - Composter recipes were missing from the EXMOD, causing items to sit in the composter without processing ([#2](https://github.com/AgentKush/Icarus-mods/issues/2)). Added 134 composter recipes to D_ProcessorRecipes for manual composting.

Ver 1.9
Added 11 new decay entries from Dangerous Horizons update.

Ver 1.8
Corrected Spoil_ composter recipes: now only covers raw meat and raw fish items. Removed incorrect composter entries for tonics, bandages, cooked foods, etc.

Ver 1.7
Added 238 missing Spoil_ composter recipes for DLC foods/tonics/consumables.

Ver 1.6
Added Decay_General and Decay_MetaItem for full coverage.

Ver 1.5
Verified all 20 decay types are current with latest game data.

Ver 1.4
Previous release with 85 composter recipes.

Ver 1.3
Added composter recipes for fish variants.

Ver 1.0
Initial release.

## Files Modified:
  Traits-D_Decayable          (33 entries)
  Crafting-D_ProcessorRecipes (122 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download No_Food_Spoilage.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods