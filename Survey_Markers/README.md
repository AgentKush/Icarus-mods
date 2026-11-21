<div align="center">

# Survey Markers

[![Version](https://img.shields.io/badge/v1.0-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

A **cheap, light Portable Beacon** you can make by hand from the start, to **mark ore, camps and cave entrances** on your map and compass.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Changes

Adds one item, the **Survey Marker**. To the game it is a Portable Beacon: you place it, interact with it and set it up in the same PORTABLE BEACON SETUP window. What changes is the cost, the weight, the stack size, the load on the floor below and the outside warning:

| | Portable Beacon (vanilla) | Survey Marker |
|---|---|---|
| Unlock | Tier 3 blueprint (level 20, after the Machining Bench and Cement Mixer) | **None** |
| Crafted | Machining Bench, Fabricator or Manufacturer | **By hand or at the Crafting Bench** |
| Recipe | 30 Gold Wire, 25 Copper Wire, 10 Steel Ingot, 20 Platinum Sheath, 10 Glass | **6 Stick, 10 Fiber, 4 Stone** |
| Made per craft | 1 | **2** |
| Weight | 10 kg | **0.5 kg** |
| Stack | 1 | **20** |
| Load on a floor it stands on | 2 | **0.25** |
| Outside warning | Shows "Must Be Placed Outside" under cover (it can still be placed there) | **None** |

Interact with a placed marker to set:

- **Name**: up to 30 characters.
- **Icon**: one of 39 pictures (camp, cave, danger, food, mine, ore, water and more).
- **Colour**: one of 10.
- **Compass view distance**: 0m, 50m, 150m, 500m (the default), 1,000m or NO LIMIT.
- **Visible to Owner Only**: hides the marker from other players' map and compass.

## Good to Know

- **It is a Portable Beacon to the game.** Same model in the world and the same picture in your inventory; only the name, description, weight and stack size tell them apart. Everything a marker shows or does, a vanilla Portable Beacon does too.
- **Placing it.** It needs a fairly level surface (up to 22.5 degrees), as the Portable Beacon does. Both can stand under a roof or in the open. Under cover the Portable Beacon shows a "Must Be Placed Outside" warning and an outside icon on its tooltip; the marker shows neither. It has not been tried in a cave yet.
- **On the map.** Every marker shows on the map at any distance, unless another player has set it to Visible to Owner Only. Hover its icon to see the name, the owner and how far away it is. Apart from the marker's own window, that is the only place the name shows.
- **On the compass.** The compass shows the marker's icon and colour, but no name or distance, and only while you are within its compass view distance. The compass measures flat distance and ignores height, so a marker far below or above you counts as close.
- **Heading to a marker.** Double-click the map next to it to drop your personal waypoint there. You get one waypoint, it is not saved, and double-clicking near it again removes it.
- **One range for everyone.** A marker has one compass view distance for all players, and it can only be changed at the marker. New markers start at 500m, so they show on the compass of everyone within 500 m. Set 0m on markers you don't need there; at 0m a marker shows on the compass only when you stand next to it.
- **NO LIMIT and your team.** When you switch a marker to NO LIMIT, it shows at once on your compass and on the compass of players who were inside its old range. Players further away keep seeing nothing until they rejoin, because the game stops updating the compass fade once a marker is on NO LIMIT. Switch to NO LIMIT while your team is near, or ask them to rejoin.
- **Owner means last editor.** A new marker has no owner. The owner is whoever last pressed OK after changing something in its window. Anyone can open any marker, change it (and so become its owner) or pick it up.
- **Visible to Owner Only is a display filter.** It hides the marker from other players' map and compass. They can still see it in the world, open it and pick it up. If someone else changes a private marker, they become the owner and you lose sight of it.
- **Picking up resets it.** Pick a marker up as you would any deployable. None of its settings are kept: placed again, it starts with the default icon, white, 500m, no name and no owner, as a Portable Beacon does.
- **No decay.** A placed or carried marker never decays. One dropped loose on the ground disappears after 10 minutes, as a dropped Portable Beacon does.
- **Removing the mod removes every Survey Marker.** Placed markers stop appearing. Markers in inventories, backpacks and storage are deleted the next time the save loads, and they do not come back. Placed markers may come back if you reinstall the mod, but this is not tested. Vanilla Portable Beacons are not affected.
- **No limit on numbers.** Every marker is sent to every player wherever they are, as Portable Beacons are. Hundreds of markers on one server have not been tested.
- **Compatible** with every other mod in the collection. Indestructible Tools & Weapons makes markers near-indestructible too, because they share the Portable Beacon's durability row. Extended Spoil Timers, Hardcore Rebalance Pack and Performance Optimizer change how long a dropped marker lasts, as they do for a dropped Portable Beacon. The Fast Processing and Faster Crafting mods don't change the marker recipe, which takes about a second.

## Missions

Some mission steps ask you to deploy a beacon near the objective. The game checks for any Portable Beacon there, so a Survey Marker counts. That applies to 24 steps in 11 missions:

| Mission | Steps | Notes |
|---|---|---|
| Conduct A Longterm Survey (three Uniao faction missions: Riverlands, Arctic and Canyons) | Deploy sheltered device near Alpha, Beta, Gamma and Delta (4 per region, 12 in all) | The marker must be under shelter. The mission gives you 4 beacons, and each site counts once, so markers don't make the scan faster. |
| OMPHALOS (EXPEDITION: STYX) | Deploy the Beacon | Within 25 m. The mission gives you beacons. |
| ZEPHYR (EXPEDITION: Ring Lake) | Deploy the Beacon | The mission gives you a beacon. |
| CRESCENDO (SURVEY: Shifting Sands) | Deploy Beacon at Location 1, 2 and 3 | The mission gives you beacons. |
| MIGRATING SANDS (SURVEY: Desert Anomaly) | Deploy Beacon at Location 1, 2 and 3 | The mission gives you beacons. |
| SHADOWED (SURVEY: Follow the Trail) | Place the Beacon within the Base | The mission gives you a beacon. |
| SMPL3: Lost (UDA faction mission) | Place a Beacon and mark the base location UDA Inspection | The mission gives you a beacon. |
| DISPATCH (DEMOLITION: Outpost) | Place Down a Beacon within the Outpost | **Easier with this mod.** The mission tells you to craft a Portable Beacon, but placing a marker finishes the step without one. The 30-second base destruction countdown starts as soon as it does. |
| DESTRUCTION (Rimetusk Campaign) | Place the Beacon Near the RIMETUSK Experiment | You still need a real Portable Beacon for the earlier step "Unlock, Craft and Pick up a Portable Beacon". You can then place a marker and keep the beacon. The 30-second explosion countdown starts as soon as the step is done. |

Where the mission gives you beacons, a marker only saves you carrying them (10 kg each) or replaces one you lost. The Longterm Survey and SMPL3: Lost have no resupply, so if you lose a beacon there, a marker spares you crafting a Tier 3 one.

- **Don't leave markers at mission sites.** The game counts any beacon near the objective, even one placed before the step started. A marker left there finishes the step about 2 seconds after it starts. In DISPATCH and DESTRUCTION that starts the 30-second countdown at once.
- **Two missions want the real item.** EXPEDITION: Riverlands (WATERFALL, "Deploy beacon in the transmission zone") and GEO-SURVEY: Canyons ("Deploy Survey Beacon at correct altitude") check for the Portable Beacon item itself, so a Survey Marker does not count there. Use the beacons those missions give you.

## Dedicated Servers

On a dedicated server it is the server, not your PC, that crafts, places and saves the markers. If only your PC has this mod, the server does not know the Survey Marker, so you can't craft or place one.

1. Build your mod list in JimK72's Mod Manager as usual.
2. Copy `IMM_Merged_Mod_P.pak` and `IMM_Merged_Mod.txt` from your game's `Icarus\Content\Paks\mods` folder into the same folder on the server.
3. Restart the server. Keep the same mods and versions on the server and on every player's PC.

Removing the mod from the server removes every Survey Marker on it, for every player (see Good to Know).

## How It Works

Data mod that adds five rows and changes no vanilla row: `Survey_Marker` in `Items-D_ItemsStatic.json`, `Items-D_ItemTemplate.json` and `Traits-D_Deployable.json`, `Item_Survey_Marker` in `Traits-D_Itemable.json` (Weight 500, MaxStack 20) and the recipe `Survey_Marker` in `Crafting-D_ProcessorRecipes.json` (recipe sets `Character` and `Crafting_Bench`, no talent, 2 per craft).

The item row is a copy of the vanilla `Portable_Beacon` row with its own Itemable and Deployable rows. Its building load is the `D_Weight` row `LightDeployable` (0.25) instead of the beacon's `MediumDeployable` (2), so markers standing on a floor weigh on it less. Its D_Deployable row sets `bMustBeOutside` to false and points at the vanilla `D_DeployableSetup` row `Portable_Beacon`, so placing a marker spawns the game's own `BP_Portable_Beacon` actor. The name, icon, colour, compass range, owner and owner-only switch are saved variables of that actor, and its map icon comes from the `D_MapIcons` row `Portable_Beacon`. These are the Portable Beacon's own features: icons and colours since Week 82, names, the map tooltip and the compass range since Week 141, and Visible to Owner Only since Week 218.

The mission steps listed above count actors of the class `BP_Portable_Beacon_C` near the objective (`BPQ_Deploy_Count` and `BPQ_Deploy_Undoable`), which is why a marker counts there. No data row can change that.

## Installation

Install via JimK72's Icarus Mod Manager. Playing on a dedicated server? Install the mod on the server too (see Dedicated Servers above).

## Changelog

### v1.0 (2026-11-20)
- Initial release
- Survey Marker: a Portable Beacon you craft by hand or at the Crafting Bench from 6 Stick, 10 Fiber and 4 Stone (2 per craft), 0.5 kg, stacks to 20, no outside warning
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
