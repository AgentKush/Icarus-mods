<div align="center">

# Absolute Chaos - Core

[![Version](https://img.shields.io/badge/v0.2.3-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Base layer of the Absolute Chaos modpack. Overrides player Base_Stats with 76 chaos buffs (5000kg carry, 600 move speed, fall-damage immunity, zero survival drain, +900% XP and crafting) and zeros research/replication cost on all 335 workshop items. v0.2.1 drops the empty workshop tab and ships a banner.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## What this mod does

Every value below was verified against the live ProjectDaedalus export from the current game build.

**Player chaos buffs** — single-row override of `D_CharacterStartingStats.Base_Stats` with 76 stat keys:

- **Carry weight** 5000 (base was 100) + 500% multiplier
- **Movement speed** 600 (base was 355), sprint 300%, crouch 150%, swim 150%, climb 200%
- **Health** 2000 max, +500/min regen
- **Stamina** 2000 max, 10000/min regen, zero delay, -90% consumption
- **Food / water / oxygen** 3000 max each, **zero consumption per hour**
- **Fall damage** disabled entirely (min% + max% + `HasFallDamageImmunity_?`)
- **Temperature** 100% cold, heat, delta, and max-delta resistance
- **Combat** +1000% crit, +1000% stealth damage, 100% collision/tree/hardened-point resistance
- **Crafting speed** +900% (10×)
- **XP gain** +900% (10×)
- **Sprain resistance** 100%
- **Respawn delay** 1 second
- **Map visibility** buildings, health, statuses, SOS all visible

**Workshop items free** — every one of the 343 vanilla workshop items has `ResearchCost` and `ReplicationCost` set to 0 credits. Verified enumeration, not a wildcard.

**Known limitation** — because the 343 workshop rows are enumerated by name, any item added in a future Icarus weekly update will still cost credits until Core is rebuilt against the new data export. This is tracked in the v0.3 roadmap.

**v0.2.1 note** — the previously-scaffolded empty "Absolute Chaos" workshop tab has been removed. It will return in v0.3 once Chaos Kits are populated.

## Companion mods — install alongside Core for the full experience

Core is deliberately narrow so it stacks with other chaos mods instead of duplicating their rows. The complete Absolute Chaos experience is Core + the companions below. The `AbsoluteChaos_Pack` install guide documents exact versions and load order.

### From this repo (AgentKush)

| Chaos lever | Mod |
|---|---|
| Instant crafting / processing | `FastProcessing_Instant` |
| 5–10× stack sizes | `Stack_Size_Overhaul` |
| Indestructible tools & weapons | `Indestructible_Tools_Weapons` |
| No food spoilage | `No_Food_Spoilage` |
| 2× butchery / skinning drops | `Creature_Drop_Enhancer` |
| ~50% weakened afflictions | `Modular_Affliction_Adjuster` |
| ~50% boosted buffs | `Modular_Buff_Enhancer` |
| 2056 individual item kits in workshop | `Agents_Individual_Item_Kits` |
| Unlocked hidden building pieces | `Hidden_Building_Pieces` |
| Hidden dev tools unlocked | `Dev_Tools_Kit` |
| Crop growth + harvest boost | `Fish_Farming_Boost` |

### From Nexus Mods and community repos (other authors — bundled in AbsoluteChaos_Pack)

All mods below are publicly released and are bundled into the `AbsoluteChaos_Pack` meta-bundle. Credit to the original authors.

| Chaos lever | Mod | Source |
|---|---|---|
| Free + instant + no talent gates | **Ultimate Crafting Freedom** | [Nexus #143](https://www.nexusmods.com/icarus/mods/143) |
| Free-building anywhere | **FreeBuild** | [Nexus #7](https://www.nexusmods.com/icarus/mods/7) |
| 5000 kg carry, 10M durability, teleporter, no-fall, photo lens, options menu | **laanp Combined QOL** | [github.com/laanp/Icarus_Mods](https://github.com/laanp/Icarus_Mods) |
| 2-way teleporter pads + remote | **JimK72 Teleporter** | [github.com/Jimk72/Icarus_Mods](https://github.com/Jimk72/Icarus_Mods) |
| In-game chaos toggle menu | **JimK72 Custom Options** | [github.com/Jimk72/Icarus_Mods](https://github.com/Jimk72/Icarus_Mods) |
| Better mission rewards | **Better Mission Rewards** | Nexus (search by name) |
| Better dropship supplies | **Better Supplies** | Nexus (search by name) |
| Early talent access | **Zen Progression** | Nexus (search by name) |

**Conflict note:** Ultimate Crafting Freedom and FreeBuild both edit crafting recipes and will fight each other. Pick **one** — Ultimate Crafting Freedom is the recommendation because it also zeros craft time. laanp Combined QOL overlaps slightly with Core's player stats; load Core last so its numbers win.

## Tier variants

Core is the always-on layer. Install **one** of these alongside it to set the intensity:

| Tier | Carry | Speed | XP | Afflictions | Fall dmg |
|---|---|---|---|---|---|
| **Mild** | 1000 kg | 1.25× | 2× | 50 % | On |
| **Chaos** (this file's defaults) | 5000 kg | 1.5× | 10× | ~0 | Off |
| **Absolute** | 99999 kg | 2× | 25× | 0 | Off |

The tier mods ship as `AbsoluteChaos_Mild.EXMOD`, `AbsoluteChaos_Chaos.EXMOD`, `AbsoluteChaos_Absolute.EXMOD`. They override the same Core rows with escalated numbers — only install one at a time.

## Status — v0.2 (data-verified)

All row names and field keys were verified against the live `Exports/` export of the current Icarus build. The v0.1 scaffold guessed at row names in `D_ExperienceEvents`, `D_Buildable`, `D_ModifierStates`, and `D_ProspectStats` — all four tables were the wrong home for the features I wanted, and have been dropped. Everything now flows through the single `D_CharacterStartingStats.Base_Stats` row plus the bulk workshop-cost zeroing.

Known gaps deferred to v0.3:

- `Workshop_AbsoluteChaos` tab exists but no Chaos Kits have been placed in it yet.
- Building decay is not currently modified (it isn't in `D_Buildable` — needs a separate investigation to find the right table).
- XP multiplier relies on the `BaseExperience_+%` stat key. Will confirm in-game that it applies to all XP sources; if not, add an affliction that broadcasts the multiplier.

## Compatibility

- Designed to stack with the listed AgentKush mods above.
- **Conflicts with** any other mod that edits `D_ExperienceEvents`, `D_ProspectStats`, building decay, or affliction modifiers. Load Core last.
- When used with Ultimate Crafting Freedom (Nexus #143), Core's upcoming zero-workshop-cost row will be redundant but harmless.

## Installation

Import `AbsoluteChaos_Core.EXMODZ` via JimK72's Icarus Mod Manager, enable it, and also enable exactly one of the tier mods.

## Changelog


### v0.2.3 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v0.2.2
- Every workshop item is free again - the list was made against an older game, so the workshop items later updates added still charged credits; they are now zeroed too (all 343). Base layer of the Absolute Chaos modpack: a 76-key player stat block and free workshop research and replication.

### v0.2 (2026-04-08)

- Complete rewrite against verified game data.
- Dropped guessed rows for D_ExperienceEvents, D_Buildable, D_ModifierStates, D_ProspectStats — all were wrong-table targets.
- Added full `D_CharacterStartingStats.Base_Stats` override with 76 stat keys (carry, speed, health, stamina, consumption, fall damage, temperature, combat, crafting speed, XP).
- Zeroed `ResearchCost` and `ReplicationCost` on all 335 vanilla workshop items.
- Kept Absolute Chaos workshop tab scaffold.

### v0.1 (2026-04-08)

- Initial scaffold with guessed row names (flagged as TODO for verification).
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
