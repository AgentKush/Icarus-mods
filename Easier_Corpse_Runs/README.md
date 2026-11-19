<div align="center">

# Easier Corpse Runs

[![Version](https://img.shields.io/badge/v1.0-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

A much stronger **Death Run** boost after you respawn, so the run back to your body is **quicker and safer**.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Changes

When you respawn while you're the only player in the game, the game gives you a short "Death Run" buff. This mod makes it stronger:

| Death Run effect | Vanilla | Modded |
|---|---|---|
| Movement speed | +10% | **+30%** |
| Stamina used by sprinting | -20% | **-50%** |
| Stamina used by other actions | -20% | -20% (unchanged) |
| Perceived threat while sneaking | -15% | **-50%** |

The buff's tooltip lists the stamina part as two lines: "-20% Stamina Consumed by Actions" and "-30% Stamina Consumed by Sprinting". The game adds the two together for sprinting.

## Good to Know

- **Only while you're the only player.** The game gives the Death Run buff only while you are the only player in the game: a solo game, or alone on a hosted or dedicated server. If another player joins, the game takes the buff away, so the mod does nothing while you play with others. That is the game's own rule, and a data mod can't change it.
- **Same length as vanilla.** Up to 5 minutes, and the game ends it early when you open the bag your items were left in. This mod changes neither.
- **Sneak to use the threat cut.** The lower threat only works while you're sneaking.
- **Why only sprinting costs less.** The game has no lower limit on stamina costs. If the cut applied to every action, a few stamina foods on top would push jumps and tool swings below zero, and they would give stamina back. Sprinting can't do that, so the extra cut is on sprinting alone.
- **Stacks** with food and other buffs you have after respawning. Dying clears your food buffs, so only food you eat after you respawn stacks with it.
- **Compatible** with every other mod in the collection. No other mod edits the Death Run buff.

## Dedicated Servers

On a dedicated server it is the server, not your PC, that adds the buff and works out its effects. If only your PC has this mod, you get the vanilla boost.

1. Build your mod list in JimK72's Mod Manager as usual.
2. Copy `IMM_Merged_Mod_P.pak` and `IMM_Merged_Mod.txt` from your game's `Icarus\Content\Paks\mods` folder into the same folder on the server.
3. Restart the server. Keep the same mods and versions on the server and on every player's PC.

## How It Works

Data mod that edits the `GrantedStats` of the `DeathRun` row in `Modifiers-D_ModifierStates.json`: `BaseMovementSpeed_+%` goes from 10 to 30 and `BaseStealthThreatModifier_+%` from -15 to -50, `BaseStaminaActionCost_+%` stays at -20, and `BaseSprintingStaminaActionCost_+%` -30 is added.

The game's player controller (`BP_IcarusPlayerControllerSurvival`) adds `DeathRun` when you respawn, if the game's `Session_SoloPlay` flag is set. The game's code sets that flag while exactly one player is connected. The buff's maximum length (`SoloRespawnBuffLength`, 300 seconds) is set in the controller too, not in a data table. The game removes the buff when you open the bag your items were moved into at respawn (`BP_Overflow_Bag_Gravestone`), or when that flag turns off.

## Installation

Install via JimK72's Icarus Mod Manager. Playing on a dedicated server? Install the mod on the server too (see Dedicated Servers above).

## Changelog

### v1.0 (2026-11-19)
- Initial release
- Stronger Death Run respawn buff: +30% movement speed, sprinting costs 50% less stamina, -50% perceived threat while sneaking
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
