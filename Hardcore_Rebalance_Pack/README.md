<div align="center">

# Hardcore Rebalance Pack

[![Version](https://img.shields.io/badge/v2.2.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/PAK%20%2B%20EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=unrealengine&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

For survivors who think Icarus is too easy

**1364 changes across 17 data tables + 2 blueprint overrides**

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## What This Mod Does

Transforms Icarus into a brutal survival experience. Every difficulty tier is rebalanced to push players harder with tougher creatures, deadlier weather, harsher status effects, reduced resources, and equipment that wears out faster.

**v2.0** introduces a 4-tier creature scaling system that replaces the old flat buffs, so early-game creatures don't feel as tanky as late-game bosses:

| Tier | Creatures | HP Boost | Melee Boost | Examples |
|------|-----------|----------|-------------|----------|
| 1 - Forest/Easy | 23 | +75% | +40% | Wolf, Hyena, Spider, Boar |
| 2 - Mid-Tier | 37 | +125% | +60% | Bear, Lion, Raptor, Scorpion |
| 3 - Hard Biome | 42 | +200% | +90% | Mammoth, Lava creatures, Yeti, RockGolem |
| 4 - Boss/Alpha | 12 | +300% | +120% | Mammoth_Boss, Scorpion_Boss, Sandwyrm_Queen |

## Changes by Category

### Creature AI & Spawns
| Table | Entries | Description |
|-------|---------|-------------|
| D_AIGrowth | 114 | 4-tier creature scaling: +75-300% HP and +40-120% melee across Forest/Mid/Hard/Boss tiers |
| D_AISpawnZones | 161 | Spawn zone configurations across all biomes, including the alpha hunters' spawns |
| D_AutonomousSpawns | 26 | Independent creature spawn rules |
| D_HordeWave | 21 | Horde event wave compositions |
| D_EpicCreatures | 21 | Custom alpha hunters - boss-tier roaming predators that drop exotics |
| D_ItemRewards | 8 | Bigger boss loot (Alpha Wolf, Scorpion, Hammerhead Slug, Ice Mammoth, Rock Golem, Great Ape, Sandworm) and a richer exotic-creature drop |

### 21 Alpha Hunters

Boss-tier versions of ordinary creatures that roam the world. Each one spawns as a rare variant of a normal creature of its species, with its own names, boosted HP and combat stats, and drops exotics when killed - the same system the game uses for its Exotic-Infused creatures.

| Hunter | In-game names | Spawns as | HP | Zones |
|--------|---------------|-----------|----|-------|
| Hunter_Wolf_Forest | Feral Packmaster, Bloodfang Alpha, Shadow Stalker | Wolf | +250% | 15 |
| Hunter_Bear_Forest | Ironhide Mauler, Grizzled Titan, Forest Warden | Bear | +350% | 15 |
| Hunter_Lion_Forest | Apex Prowler, Silent Killer | Jaguar / Cougar | +350% | 29 |
| Hunter_PolarBear_Arctic | Frostbitten Juggernaut, Glacial Devastator, Winterborn Titan | Polar Bear | +500% | 14 |
| Hunter_Wolf_Arctic | Blizzard Fang, Icevein Predator, Howling Wraith | Snow Leopard / Snow Wolf | +250% | 32 |
| Hunter_Mammoth_Arctic | Tundra Colossus, Permafrost Behemoth | Woolly Mammoth | +500% | 7 |
| Hunter_Scorpion_Desert | Venomspine Patriarch, Deathsting Overlord | Scorpion | +350% | 15 |
| Hunter_Hyena_Desert | Sandstorm Ravager, Dune Shredder | Hyena | +250% | 14 |
| Hunter_Rockdog_Volcanic | Magma Hound, Obsidian Ravager | Stonejaw | +250% | 29 |
| Hunter_BatDog_Volcanic | Ashen Terror, Sulfur Fiend | Drac | +250% | 51 |
| Hunter_Crocodile_Swamp | Bog Horror, Deathmaw Lurker | Crocodile | +250% | 11 |
| Hunter_Needler_Swamp | Thornspine Matriarch, Quillbeast Prime | Needler | +250% | 23 |
| Hunter_Mammoth_Boss | Tuskbreaker, Thunderhoof, Bonecrush | Woolly Mammoth | +500% | 3 |
| Hunter_Moa_Arctic | Frost Matriarch, Blizzard Runner, Tundra Stalker | Arctic Moa | +250% | 3 |
| Hunter_DesertWolf_Desert | Dune Howler, Sand Phantom, Mirage Hunter | Hyena | +250% | 3 |
| Hunter_EnragedLion_Forest | Rage Fang, Blood Stalker, Fury | Cougar | +350% | 3 |
| Hunter_Scorpion_Enraged | Venomspine, Death Sting, Barb Lord | Scorpion | +350% | 3 |
| Hunter_SnowStriker_Arctic | Blizzard Claw, Ice Reaper, Frozen Fury | Snow Stalker | +250% | 3 |
| Hunter_Yeti_Arctic | Mountain Terror, Abominable, Peak Predator | Frostfoot | +500% | 3 |
| Hunter_Jaguar_Forest | Night Prowler, Jungle Phantom, Silent Killer | Jaguar | +250% | 3 |
| Hunter_PolarBear_Roaming | Frost Maul, Tundra Fury, Iceclaw | Polar Bear | +500% | 3 |

### Weather System (NEW in v1.16, tuned in v2.0)
| Table | Entries | Description |
|-------|---------|-------------|
| D_WeatherEvents | 110 | Extended storm durations across all biomes |
| D_WeatherActions | 203 | **Storms now damage players** - enabled player damage on all Body/Chaos storm phases, boosted deployable damage +50%, doubled lightning frequency, faster wind damage ticks. v2.0: damage intensity reduced 20% for better balance |

### Status Effects & Afflictions (NEW in v1.16)
| Table | Entries | Description |
|-------|---------|-------------|
| D_AfflictionChance | 22 | Increased affliction chances (dysentery, food poisoning, pneumonia, frostbite, wounds) and longer durations |

### Resource & Equipment Nerfs (NEW in v1.16)
| Table | Entries | Description |
|-------|---------|-------------|
| D_OreDeposit | 21 | Mining takes 25-50% longer depending on ore tier |
| D_Durable | 22 | High-tier equipment durability nerfed: Steel -25%, Titanium -30%, Lithium -35%, Meta -40% |
| D_Consumable | 212 | Food healing reduced -35%, buff durations extended +25% in v2.0 (was -30%) to compensate for tougher survival |

### Survival & Environment
| Table | Entries | Description |
|-------|---------|-------------|
| D_Decayable | 33 | Accelerated food spoilage |
| D_Combustible | 4 | Modified fire behavior |
| D_ExperienceEvents | 162 | XP rebalance across activities |

### Difficulty Tiers
| Table | Entries | Description |
|-------|---------|-------------|
| D_ProspectStats | 27 | Custom stat modifiers per difficulty (NPC HP/damage/speed, storms, durability, survival, respawn, XP) |
| D_ProspectList | 197 | All maps have 4 difficulty tiers (Easy/Normal/Hard/Extreme) |

### Difficulty Scaling (Extreme Tier)
- **Creatures:** +200% HP, +100% melee damage, +45% speed, +120% perception
- **Spawns:** +120% spawn rate, +150% spawn count
- **Storms:** +350% lightning frequency, +400% player hit chance, +200% building hit, +250% tree hit
- **Durability:** +100% durability loss rate
- **Survival:** -40% player HP, -65% crafting speed
- **Respawn:** +60s delay, +400m distance
- **XP:** +50% experience gain

### Blueprint Overrides
- `BP_IcarusNPCGOAPController` - Modified creature AI behavior
- `BP_IcarusGOAPMotivation_Enraged` - Enraged state AI changes

## Installation

1. Install [JimK72's Icarus Mod Manager](https://github.com/jimk72/IcarusModManager)
2. Download `Hardcore_Rebalance_Pack.EXMODZ`
3. Import via Mod Manager

## Recommended Companion Mod

For the full hardcore experience and the hardest gameplay possible, install **Creature_Difficulty_Scaling (CDS) v2.2+** alongside this mod. CDS adds level-500 spawn zone scaling, per-player-level stat scaling rules, and tame/mount survival buffs so your pets can actually hold up against HRP's tougher creatures. Running HRP + CDS together delivers the most punishing Icarus experience possible — see the v1.18 changelog for overlap details.

## Changelog

### v2.2.1 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v2.2 (2026-11-07)
**Alpha hunters rebuilt for the November 2026 game data.**
- **9 more hunters now spawn:** Moa, Hyena, Cougar, Scorpion, Snow Stalker, Frostfoot, Jaguar and Polar Bear hunters, plus the Mammoth Boss hunter. v1.14 gave them spawn rows built from fields `D_AISpawnZones` does not have (`EpicCreature`, `SpawnBiome`, `MaxSpawnCount`, `RespawnTime`, `SpawnChance`), so they never appeared. They now spawn the way the original 12 hunters and the game's own epic creatures do: as a rare (weight 1) variant of a normal creature of their species, in up to 3 zones each, Hard tiers first.
- **Every hunter now drops exotics on kill,** using the same two stats as the game's Exotic-Infused creatures (`ExoticRewardType_Enum` 1, `BasePurpleExoticRewardChance_%` 100).
- **Removed 16 hunters** whose creature the game only spawns in missions, caves or boss fights, never in the wild: Sandworm, Alpha Wolf Boss, Landshark, Landshark Norex, Rock Golem, Juvenile Rock Golem, Great Ape, Ice Mammoth, IceBreaker, Hammerhead Slug, Mange Wolf, Poison Bear, Snow Slug, Sandwyrm Queen and Irradiated Abomination - plus the Radiation Boss, whose creature no longer exists in the game.
- **Removed 29 hunter loot tables nothing could reach.** The game picks a creature's loot from its creature type, never from the hunter, so these never dropped. The 25 added in v1.14 also used an invalid `Drops` field and a non-existent `Exotic_Ore` item.
- **Boss loot:** the Scorpion Boss loot now includes the Chitin the November update added to it (the mod was removing it); the Hammerhead Slug boss no longer lists a canteen that does not exist (`Meta_Canteen_Inaris`); the Rock Golem's shotgun shells use the current item name (`Ammo_Shell_Buckshot`).

### v2.1 (2026-06-27)
- Removed 4 stale XP-event references (KillAI / KillSmallAnimal / KillMediumAnimal / Kill_RadiationBoss) that the game replaced with per-creature events.
### v2.0 (Tiered Creature Rework)

**Major rework replacing flat creature buffs with a 4-tier scaling system.**

The old +150% HP / +75% melee was applied identically to every creature — a Wolf got the same buff as a Mammoth Boss. This made early-game disproportionately hard while late-game didn't feel as impactful. v2.0 introduces tiered scaling that matches gear progression:

- **Tier 1 - Forest/Easy** (23 creatures): +75% HP / +40% Melee — Wolves, Hyenas, Spiders, Boars, Slinkers
- **Tier 2 - Mid-Tier** (37 creatures): +125% HP / +60% Melee — Bears, Lions, Raptors, Scorpions, Crocodiles, Apes
- **Tier 3 - Hard Biome/Elite** (42 creatures): +200% HP / +90% Melee — Mammoths, Lava creatures, Yeti, RockGolems, Sandworms, Arctic/Desert fauna
- **Tier 4 - Boss/Alpha** (12 creatures): +300% HP / +120% Melee — Alpha Wolves, Mammoth Boss, Scorpion Boss, Sandwyrm Queen, Stomper Matriarch

**Epic creatures also tiered:** Forest epics 250% HP / 40% melee, mid epics 350% / 55%, apex epics 500% / 80%.

**Horde waves rebalanced:** Proper difficulty ramp from Level 30 with moderate spawns (3-6) in early waves, scaling to Level 75 with 8-15 spawning at a time in late waves.

**Weather tuning:** Storm damage intensity reduced 20% — still punishing but less frustrating chip damage.

**Consumable tuning:** Food buff durations extended 25% to compensate for the tougher survival environment.

Total changes: 1438 across 17 data tables + 2 blueprint overrides.

### v1.18 (Creature HP/Melee Rework)

**The big fix: NPC HP boosts actually work now.**

In v1.17 the `WorldNPCMaximumHealth_+%` world stat was being silently ignored for the vast majority of creatures because Icarus uses per-creature `CurveFloat` assets (e.g. `C_BearHealth`) for HP instead of a flat stat. Multiplying a world stat that the curve never reads does nothing — a vanilla Bear has ~750-3000 HP from its curve regardless of what the world stat says.

**What this version does instead:** it adds a brand new `D_AIGrowth` section with 114 hostile creature overrides. Each row adds two per-creature additive stats directly to the creature's `Base` block, which Icarus actually respects:

- `BaseMaximumHealth_+%: 150` (+150% HP baseline)
- `BaseMeleeDamage_+%: 75` (+75% melee damage baseline)

Scope: every hostile creature the mod could identify — bears, wolves, big cats, reptiles, scorpions, mammoths/tuskers, birds, bugs, bats, worms, slugs, apes, drones, irradiated, lava creatures, strikers/tanks, golems, and all hunter/boss variants. Prey animals (deer, rabbit, sheep, etc.), mounts, tamed creatures, and fish are untouched.

**Cleanup:**
- Removed the now-dead `WorldNPCMaximumHealth_+%` and `WorldNPCMeleeAttack_+%` entries from `NPC_Increase_Easy/Medium/Hard/Extreme` in `D_ProspectStats`. They were cosmetic — they showed up in the difficulty preview tooltip but did nothing. The UI will no longer claim a boost it can't deliver.

**Recommended companion mod — `Creature_Difficulty_Scaling` (CDS):**
For the full hardcore experience and the hardest gameplay, run HRP **alongside** CDS v2.2 or later. HRP owns the baseline creature HP/melee push via `D_AIGrowth`; CDS layers on top with level-500 spawn zone scaling, per-player-level scaling rules, tame/mount survival buffs, and its own tiered creature stat boosts. Together they produce the most punishing, highest-level Icarus experience the mod manager can deliver.

Heads-up on the overlap: both mods modify `BaseMaximumHealth_+%` and `BaseMeleeDamage_+%` on hostile creatures in `D_AIGrowth`. When loaded together, whichever mod loads last wins for those specific fields (per-row, not per-stat). Everything else — HRP's weather, afflictions, durability, ore, consumables, spawn rates, difficulty tiers, alpha hunters, AND CDS's spawn zone levels, scaling rules, tame buffs — stacks cleanly with no conflict. The end result is still meaningfully harder than either mod alone.

**Note on difficulty tiering:** I investigated making the HP boost scale with difficulty (Easy < Normal < Hard < Extreme) via `D_ScalingRules`. It turns out scaling rules are wired up in Blueprint code at runtime, not through data tables, so you can't attach a new rule to `BaseMaximumHealth_+%` from an EXMOD. The +150% / +75% values are flat across all difficulties. If this ends up feeling too punishing on Easy/Medium, open `Hardcore_Rebalance_Pack.EXMOD`, find the `AI-D_AIGrowth.json` block, and tune the two numbers — the existing `tools/patch_bp_floats.py` pattern shows how to iterate locally.

### v1.17 (Bug Fix Release)

**Critical fixes:**
- **Fixed NPC stat boosts not applying on Extreme difficulty.** `NPC_Increase_Extreme`, `NPC_Increase_Extreme_SpawnRates`, and `Hardcore_XP_Extreme` were silently failing to load because they referenced 6 invalid stat names that don't exist in the game's `D_Stats.json`. Removed: `WorldNPCMeleeDamage_+%`, `WorldAIPerceptionSightRadius_+%`, `WorldAIPerceptionHearingRange_+%`, `WorldNPCSpawnModifier_+%`, `WorldNPCSpawnCountModifier_+%`, `WorldPlayerXPMultiplier_+%`. The remaining valid stats now apply correctly.
- **Inverted `Hardcore_Durability_*` values.** The mod was setting `WorldItemDurability_+%` to positive values (+20/+35/+50/+100), which BUFFED tool/building HP instead of nerfing it. Tools became so tough that demolishing them required hammers and excessive time. Now correctly nerfs durability: -20/-35/-50/-90% across difficulty tiers (Extreme capped at -90 to leave 10% durability instead of zeroing out tools).

**Compensating buffs (replacing the removed invalid stats with valid equivalents):**
- **Expanded `NPC_Increase_Hard_SpawnRates` and `NPC_Increase_Extreme_SpawnRates` from 5 to 20 creatures.** Added per-creature spawn rate boosts for Boar, Buffalo, Chamois, Crocodile, Deer, Elephant, Goat, Komodo, Mammoth, Rabbit, Raccoon, Roat, Tusker, Wulv, and Zebra (Hard +50% each, Extreme +70% each). This recovers most of the intent of the removed `WorldNPCSpawnModifier_+%` and `WorldNPCSpawnCountModifier_+%` since vanilla has no global spawn modifier.
- **Bumped `Hardcore_XP_Extreme.WorldPlayerExperience_+%` from 35 to 75** to compensate for the removed `WorldPlayerXPMultiplier_+%`.
- **Note on the other 3 removed stats:** `WorldNPCMeleeDamage_+%` is already covered by `WorldNPCMeleeAttack_+%` (same underlying value in Unreal). `WorldAIPerceptionSightRadius_+%` and `WorldAIPerceptionHearingRange_+%` are now **recovered via BP override** — `BP_IcarusNPCGOAPController` (which this mod already ships) has been edited directly so all NPCs use the boosted values:
  - `SightRadius`: 10000 → **17000** (+70%)
  - `LoseSightRadius`: 135000 → **180000** (+33%, keeps aggression durations sane)
  - `HearingRange`: 15000 → **25500** (+70%)

  These values affect every NPC controller in the game (it's the parent class). If you want to tune them yourself you have two options:
  - **Quick:** edit `tools/patch_bp_floats.py` (change the `NEW_VALUES` in the `PATCHES` list), then run `python tools/patch_bp_floats.py`. This byte-patches the `.uexp` in-place. The vanilla `.uexp` is preserved as `BP/AI/GOAP/BP_IcarusNPCGOAPController.uexp.vanilla.bak` so you can always revert.
  - **Full editor:** open `BP/AI/GOAP/BP_IcarusNPCGOAPController.uasset` in [UAssetGUI](https://github.com/atenfyr/UAssetGUI) and edit the `Vision Config` and `Sound Config` exports directly. See `BP_EDIT_GUIDE.md` for the full walkthrough.

  After tuning, re-pack the EXMODZ if you want to redistribute. Note: BP class default values do **not** hot-reload on existing prospects — start a new prospect to verify changes.

## v1.16 - Hardcore Survival Update
- **FIXED:** Lightning tree hit chance stat typo (was silently ignored)
- **NEW:** D_WeatherActions - 203 storm modifications, storms now damage players directly
- **NEW:** D_AfflictionChance - 22 affliction boosts (higher chances, longer durations)
- **NEW:** D_OreDeposit - 21 ore mining time increases (25-50% longer)
- **NEW:** D_Durable - 22 durability nerfs on Steel/Titanium/Lithium/Meta gear
- **NEW:** D_Consumable - 212 food/healing nerfs (-35% healing, -30% buff duration)
- Total changes: 844 -> 1324 across 11 -> 16 data tables

### v1.15 - Extreme Cleanup
- Removed Hell difficulty tier (game engine only supports 4 tiers)
- Beefed up Extreme difficulty across all stat categories
- All 194 maps properly configured with Easy/Normal/Hard/Extreme

### v1.14 - Alpha Hunter Expansion
- Added 25 new alpha hunters (37 total) covering all vanilla boss types
- Added matching reward entries and spawn zone configurations

### v1.13 - Original Release
- 12 alpha hunters, full difficulty system, weather mods, spawn overrides
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
