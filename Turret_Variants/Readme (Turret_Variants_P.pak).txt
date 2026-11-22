Turret_Variants_P.pak
----------------------------------------------------------------------
Mod Version: 3.7.4

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
Adds 15 new automated turret variants with unique characteristics. v3.0: LOS fix PAK + proper ammo type matching (arrows, bolts, javelins, stones, biofuel) + tighter targeting.



Ver 3.7.4
The Flamethrower turret works. It was built on the game's own flamethrower turret item (the
Dangerous Horizons one) but turned it into a shotgun turret with no fuel, so it never fired
(since Ver 3.0), and with this mod installed the game's own flamethrower turret was broken too.
Turret Variants now has its own flamethrower, built on the game's working one: the real
flamethrower model and flame, filled with biofuel from a jerrycan (hold it and use the turret)
or through a biofuel pipe, and it needs power. It keeps this mod's stats (40-shot stream, 15m
range) and its T4 Fabricator blueprint, and research you already did is kept. The game's own
flamethrower turret is no longer touched. A Turret Variants flamethrower already placed or
carried becomes the game's flamethrower on the next load, with the game's stats; craft a new
one for this mod's.

Ver 3.7.3
The Sniper and Heavy Sniper turrets now load 12.7mm rounds, and the Assault Rifle and Storm
turrets load 5.56mm rounds. All four used the game's rifle turret ammo slot, which only takes
7.62mm rounds and the universal EDS round, so the two snipers couldn't be loaded at all and the two
AR turrets took only EDS. Each pair now has its own slot: the snipers take every 12.7mm round,
including the explosive one that Agent's Hidden Things or Ammo Crafting Overhaul adds (the Ver
3.7.2 note said it already loaded; it didn't), and the AR turrets take every 5.56mm round plus EDS.
A turret holds one ammo type at a time, so take any EDS out of an Assault Rifle or Storm turret
before loading 5.56mm. Turrets already placed pick up the new slots when the save loads, and
nothing in them is lost.
Known issue: the Flamethrower turret can't fire (it hasn't since Ver 3.0, when its ammo became
Biofuel with no way to fill it). Ver 3.7.4 fixes it.

Ver 3.7.2
The 15 turret blueprints no longer overlap other blueprints in the T4 Fabricator tech tree. A game
update added the T4 Carpentry Bench and the Metal Grate Floor and Stair where 7 of them sat, so
they now sit together past the end of the game's own nodes, in the same two rows. Their unlocks
and requirements are unchanged.
Ammo lists checked against the game: every turret's list is an exact copy of the game's current
list for its weapon type. Ver 3.6 called the Scyther (Marrowraith) javelin a DLC spear; it is an
item the game never released. That javelin, the Marrowraith arrow and bolt and the explosive
12.7mm round load into these turrets once Agent's Hidden Things (or, for the round, Ammo Crafting
Overhaul 1.2.2) adds them. The game's lists also name 6 other unreleased arrows and bolts; they
stay listed, as in the game, and do nothing until an item exists.

Ver 3.7.1
New icon and banner, drawn from the mod's live data. No gameplay change.

Ver 3.7
Arc-projectile turret balance pass (contributed by asconley): trimmed Crossbow (55->50m), Bow (60->55m), Javelin (70->65m) and Rapid Crossbow (45->40m) ranges so the gravity-affected shots land on target, and raised the Javelin launch force so spears reach range.

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
  Deployables-D_DeployableSetup (14 entries)
  Traits-D_Deployable           (14 entries)
  Items-D_ItemsStatic           (15 entries)
  Traits-D_Itemable             (15 entries)
  Items-D_ItemTemplate          (15 entries)
  Talents-D_Talents             (15 entries)
  Crafting-D_ProcessorRecipes   (15 entries)
  Traits-D_Durable              (1 entries)
  Tools-D_ValidAmmoTypes        (9 entries)
  Tags-D_TagQueries             (3 entries)
  Traits-D_Inventory            (5 entries)
  Inventory-D_InventoryInfo     (5 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Turret_Variants.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods