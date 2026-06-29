Turret_Variants_P.pak
----------------------------------------------------------------------
Mod Version: 3.6

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
Adds 15 new automated turret variants with unique characteristics. v3.0: LOS fix PAK + proper ammo type matching (arrows, bolts, javelins, stones, biofuel) + tighter targeting.



Ver 3.6
Expanded every turret's ammo list to the full current game sets - all standard, DLC and workshop ammo variants now load (added the universal Ammo_EDS round + DLC Scyther spear).

Ver 3.5
Ammo loading fix (contributed by asconley): turrets stopped accepting ammo after the w237/238 update. Added self-contained TV_ ammo categories, slot tag-queries, and custom turret inventories so spears and stone load again.

Ver 3.4
Restored all 15 turret display meshes after a bad merge swapped them for a generic fabricator box.

Ver 3.3
Fixed all 15 turret meshes for the June 2026 update - each turret now uses its real pistol/rifle/shotgun/flamethrower turret model.

Ver 3.1
Crash fix: Fixed 15 recipe outputs from D_ItemsStatic to D_ItemTemplate. Prevents EXCEPTION_ACCESS_VIOLATION when opening crafting stations.
Ver 3.0
LOS fix PAK (turrets stop shooting through walls) + proper ammo type matching (arrows, bolts, javelins, stones, biofuel) + updated descriptions.

Ver 2.5
Hammer repairable turrets (custom Turret_Repairable D_Durable entry).

Ver 2.4
Fixed backwards shooting (_C class suffix fix) + reduced yaw/pitch extents.

Ver 2.3
Fixed broken crafting recipes.

Ver 2.2
Tightened targeting parameters.

Ver 2.1
Initial 15-variant release.

## Files Modified:
  Deployables-D_Turret          (15 entries)
  Deployables-D_DeployableSetup (15 entries)
  Traits-D_Deployable           (15 entries)
  Items-D_ItemsStatic           (15 entries)
  Traits-D_Itemable             (15 entries)
  Items-D_ItemTemplate          (15 entries)
  Talents-D_Talents             (15 entries)
  Crafting-D_ProcessorRecipes   (15 entries)
  Traits-D_Durable              (1 entries)
  Tools-D_ValidAmmoTypes        (9 entries)
  Tags-D_TagQueries             (2 entries)
  Traits-D_Inventory            (3 entries)
  Inventory-D_InventoryInfo     (3 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Turret_Variants.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods