Hardcore_Rebalance_Pack_P.pak
----------------------------------------------------------------------
Mod Version: 2.2

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD + Blueprint Overrides

## Description:
For survivors who think Icarus is too easy. v2.0 introduces a 4-tier creature scaling system
replacing the old flat buffs, so early-game creatures don't feel as tanky as late-game bosses.
Includes rebalanced horde waves, deadlier weather, harsher afflictions, reduced resources,
and equipment that wears out faster. 1364 changes across 17 data tables + 2 blueprint overrides.

For the full hardcore experience, pair with Creature_Difficulty_Scaling (CDS) v2.2+ which adds
level-500 zone scaling, per-player scaling rules, and tame/mount survival buffs.

Requires JimK72's Icarus Mod Manager: https://github.com/Jimk72/Icarus_Software

## Creature Tier System (v2.0):
  Tier 1 - Forest/Easy    (23 creatures):  +75% HP  / +40% Melee
  Tier 2 - Mid-Tier       (37 creatures):  +125% HP / +60% Melee
  Tier 3 - Hard Biome     (42 creatures):  +200% HP / +90% Melee
  Tier 4 - Boss/Alpha     (12 creatures):  +300% HP / +120% Melee

  Epic Creatures:
  - Forest Epics:   250% HP / 40% Melee
  - Mid Epics:      350% HP / 55% Melee
  - Apex Epics:     500% HP / 80% Melee

## Files Modified:
  AI-D_AIGrowth           (114 entries) - 4-tier creature HP/melee scaling
  AI-D_AISpawnZones       (161 entries) - Spawn zone configurations
  AI-D_AutonomousSpawns    (26 entries) - Independent creature spawns
  AI-D_EpicCreatures       (21 entries) - Custom alpha hunters
  Experience-D_ExperienceEvents (162 entries) - XP rewards
  Horde-D_HordeWave        (21 entries) - Horde wave compositions
  Items-D_ItemRewards        (8 entries) - Bigger boss loot
  Modifiers-D_AfflictionChance (22 entries) - Affliction chances/durations
  Prospects-D_ProspectList (197 entries) - Difficulty tiers per map
  Stats-D_ProspectStats     (27 entries) - Difficulty stat modifiers
  Traits-D_Combustible       (4 entries) - Fire behavior
  Traits-D_Consumable      (212 entries) - Food healing/buff durations
  Traits-D_Decayable        (33 entries) - Food spoilage rates
  Traits-D_Durable           (22 entries) - Equipment durability
  Weather-D_WeatherActions  (203 entries) - Storm damage/lightning
  Weather-D_WeatherEvents   (110 entries) - Storm durations
  World-D_OreDeposit         (21 entries) - Mining times

  Blueprint Overrides:
  - BP_IcarusNPCGOAPController      - Modified creature AI behavior
  - BP_IcarusGOAPMotivation_Enraged - Enraged state AI changes

## 21 Alpha Hunters:
  Boss-tier versions of ordinary creatures. Each spawns as a rare variant of a
  normal creature of its species, with its own names, boosted HP and combat
  stats, and drops exotics when killed.

  Hunter_Wolf_Forest           spawns as Wolf                 +250% HP, 15 zones
  Hunter_Bear_Forest           spawns as Bear                 +350% HP, 15 zones
  Hunter_Lion_Forest           spawns as Jaguar / Cougar      +350% HP, 29 zones
  Hunter_PolarBear_Arctic      spawns as Polar Bear           +500% HP, 14 zones
  Hunter_Wolf_Arctic           spawns as Snow Leopard / Snow Wolf +250% HP, 32 zones
  Hunter_Mammoth_Arctic        spawns as Woolly Mammoth       +500% HP, 7 zones
  Hunter_Scorpion_Desert       spawns as Scorpion             +350% HP, 15 zones
  Hunter_Hyena_Desert          spawns as Hyena                +250% HP, 14 zones
  Hunter_Rockdog_Volcanic      spawns as Stonejaw             +250% HP, 29 zones
  Hunter_BatDog_Volcanic       spawns as Drac                 +250% HP, 51 zones
  Hunter_Crocodile_Swamp       spawns as Crocodile            +250% HP, 11 zones
  Hunter_Needler_Swamp         spawns as Needler              +250% HP, 23 zones
  Hunter_Mammoth_Boss          spawns as Woolly Mammoth       +500% HP, 3 zones
  Hunter_Moa_Arctic            spawns as Arctic Moa           +250% HP, 3 zones
  Hunter_DesertWolf_Desert     spawns as Hyena                +250% HP, 3 zones
  Hunter_EnragedLion_Forest    spawns as Cougar               +350% HP, 3 zones
  Hunter_Scorpion_Enraged      spawns as Scorpion             +350% HP, 3 zones
  Hunter_SnowStriker_Arctic    spawns as Snow Stalker         +250% HP, 3 zones
  Hunter_Yeti_Arctic           spawns as Frostfoot            +500% HP, 3 zones
  Hunter_Jaguar_Forest         spawns as Jaguar               +250% HP, 3 zones
  Hunter_PolarBear_Roaming     spawns as Polar Bear           +500% HP, 3 zones

## Difficulty Scaling (Extreme Tier):
  Creatures:  +200% HP, +100% melee damage, +45% speed, +120% perception
  Spawns:     +120% spawn rate, +150% spawn count
  Storms:     +350% lightning frequency, +400% player hit chance
  Durability: +100% durability loss rate
  Survival:   -40% player HP, -65% crafting speed
  Respawn:    +60s delay, +400m distance
  XP:         +50% experience gain

## Horde Waves (v2.0):
  Early Waves  (1-2): Level 30, 3-6 spawns at a time, moderate total
  Mid Waves    (3-4): Level 45, 5-10 spawns at a time, increased total
  Late Waves   (5-7): Level 60, 6-12 spawns at a time, heavy total
  Boss Waves   (8+):  Level 75, 8-15 spawns at a time, brutal total

## Weather (v2.0 tuned):
  Storms damage players directly on all Body/Chaos phases.
  Deployable damage boosted +50%, doubled lightning frequency.
  v2.0: Damage intensity reduced 20% for better balance.

## Consumables (v2.0 tuned):
  Food healing reduced -35%.
  Buff durations extended +25% (was -30%) to compensate for tougher survival.

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Hardcore_Rebalance_Pack.EXMODZ
  3. Import via Mod Manager

## Changelog:
  v2.2 - Alpha hunters rebuilt for the Nov 2026 game: 9 v1.14 hunters now spawn (their spawn
         rows used fields the game does not have), every hunter drops exotics on kill, 16
         hunters the game cannot spawn in the wild removed, 29 unreachable loot tables removed,
         Scorpion Boss keeps the game's new Chitin, broken canteen and shotgun shell entries fixed
  v2.1 - Removed 4 stale XP-event references (KillAI/KillSmallAnimal/KillMediumAnimal/Kill_RadiationBoss) that the game replaced with per-creature events.
  v2.0 - Tiered creature scaling (4 tiers), rebalanced horde waves,
         epic creatures tiered, weather -20%, food buffs +25%
  v1.18 - NPC HP via D_AIGrowth per-creature, 114 hostile creatures
  v1.17 - Fixed Extreme difficulty stat loading, BP perception overrides
  v1.16 - Weather damage, afflictions, ore mining, durability nerfs
  v1.15 - Removed Hell tier, beefed up Extreme, 194 maps configured
  v1.14 - 25 new alpha hunters (37 total), reward entries
  v1.13 - Original release: 12 alpha hunters, difficulty system

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods
