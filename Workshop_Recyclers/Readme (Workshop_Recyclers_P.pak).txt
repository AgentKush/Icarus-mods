Workshop_Recyclers_P.pak
----------------------------------------------------------------------
Mod Version: 5.8

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
Two recycling machines (Biofuel T3 + Organic T4) plus an Incinerator for instant item destruction. 3,051 incinerate recipes + 2,258 recycle/deconstruct recipes. 100% material returns on recycling.


Ver 5.8
Updated for the November 2026 game update. Removed 41 recipes for items the game no
longer has (the update deleted the Electric Motor, Cobalt Ore, Cobalt Ingot and the
explosive sniper rounds; the rest were unreleased workshop items or items with no item
data), so the machines no longer list recipes that can never run. Fixed 25 recipes that
gave nothing: 17 Platinum Sheath and 4 saddle outputs used the wrong item name, and 4
deconstruct recipes tried to output animal carcasses, which cannot be made (they now
give Wool or a Ram, Sheep or Pig head, matching the vanilla recipes). Removed
Deconstruct Raw Meat (no single vanilla source to return), 3 duplicate recipes that
overwrote each other, and an unused timing field from every incinerate recipe. Added
incinerate recipes for the 17 new items. 5,312 recipes: 1,943 deconstruct, 315 recycle,
3,051 incinerate and 3 crafting.

Ver 5.7
Fixed Incinerator and Biofuel Recycler meshes for the June 2026 update - they now use the real electric-furnace and cleaning-device models (the old meshes were removed by the update).

Ver 5.5
Added 886 missing incinerate recipes (frozen wood, frozen ore, raw ores, food, building pieces, seeds, etc). 3,054 total incinerate recipes now cover every item in the game. Fixed icon (was using non-existent asset), fixed mesh (Mesh_Electric_Furnace doesn't exist), repositioned tech tree to avoid vanilla overlap.

Ver 5.3
New machine: Incinerator. Electric-powered processor that instantly destroys any item with no output. 2,168 incinerate recipes covering every recyclable/deconstructable item. Crafted at Fabricator/..

Ver 5.2
Crash fix: Fixed EXCEPTION_ACCESS_VIOLATION crash caused by incorrect DataTableName references in v5.1 recipes. All recipe outputs now correctly use D_ItemTemplate, all inputs use D_ItemsStatic. Fi..

Ver 5.1
Added 158 new recipes: 6 mission items (Gyro, Navigation, Thruster, Enzyme Storage, High-Tech Assembled, Recombined Tech), 10 DLC items (Lava Hunter trophies, Homestead decor), 29 national flags, 1..

Ver 5.0
Complete rebuild: Fixed root cause of all currency outputs failing - processor recipes cannot output D_MetaCurrency, so all 317 workshop recycle recipes now output physical items (Ren, Meta_Resourc..

Ver 4.7
Fixed MetaResource currency outputs, added 285 new Recycle_ recipes.

Ver 4.6
Fixed 47 recipes to return correct exotic items.

Ver 4.5
Added 60 new recycle recipes for DLC workshop items.

Ver 4.4
Fixed 135 recipe output references.

Ver 4.3
Game update compatibility fix - fixed 57 broken input refs, 12 broken output refs, removed 62 deleted items, added 12 new recipes.

Ver 4.2
Repair fix - both recyclers now hammer repairable with custom D_Durable entry.

Ver 4.1
Week 213+ compatibility update.

Ver 4.0
Major update - 100% workshop cost returns, fixed 74 currency refs, 28 name typos.

Ver 3.0
Major cleanup - fixed 63 broken item references, removed 136 invalid recipes.

## Files Modified:
  Crafting-D_RecipeSets       (3 entries)
  Traits-D_Processing         (3 entries)
  Traits-D_Itemable           (3 entries)
  Items-D_ItemsStatic         (3 entries)
  Items-D_ItemTemplate        (3 entries)
  Talents-D_Talents           (3 entries)
  Traits-D_Durable            (1 entries)
  Crafting-D_ProcessorRecipes (5312 entries)
  Inventory-D_InventoryInfo   (1 entries)
  Traits-D_Inventory          (1 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Workshop_Recyclers.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods