<div align="center">

# Creature Difficulty Scaling

[![Version](https://img.shields.io/badge/v2.4.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Dynamic creature level scaling for level 500 cap. Scales all spawn zones up to level 500, buffs creature stats by tier, adds player-level-based scaling rules, and a full affliction system with poison, concussion, epic creatures, and biome temperature modifiers

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Description

Massively overhauls creature difficulty to scale with high-level play. This mod transforms all 161 spawn zones across every biome to support creature levels up to 500, applies tiered stat buffs to 136 creatures, adds player-level-based scaling rules for dynamic difficulty, and now includes a full affliction system, epic creatures, exotic loot, and biome temperature modifiers.

Designed as the combat companion to level cap mods — without this, creatures cap at level 120 even when players can reach 500.

## What This Mod Does

### 1. Spawn Zone Level Scaling (161 zones)
All spawn zones across Olympus, Styx, Prometheus, and Elysium have been rescaled:

| Zone Difficulty | Vanilla Range | Modded Range |
|----------------|--------------|--------------|
| Starter/Outpost | 1-30 | 2-100 |
| Easy | 10-50 | 27-200 |
| Medium | 30-60 | 100-250 |
| Hard | 50-80 | 200-350 |
| Very Hard | 70-100 | 300-437 |
| Super Hard | 80-120 | 350-500 |
| Endgame (Icesheet/Ashlands) | 100-120 | 437-500 |

### 2. Creature Stat Buffs (136 creatures)
Percentage-based buffs applied by creature threat tier:

| Tier | HP | Damage | Resistance | Regen | Speed |
|------|-----|--------|------------|-------|-------|
| Passive (Deer, Rabbits, etc.) | +25% | — | — | +15% | — |
| Small Predator (Wolves, Spiders) | +50% | +30% | — | +25% | +5% |
| Medium Predator (Bears, Jaguars) | +100% | +50% | +15% | +50% | +8% |
| Boss (Mammoths, Sandworms) | +75% | +40% | +20% | +30% | — |

### 3. Player-Level Scaling Rules
Dynamic scaling rules that scale creature stats based on nearby player level:

| Scaling Rule | Effect |
|-------------|--------|
| Health | +5% per player level (up to +2500% at level 500) |
| Damage | +3% per player level (up to +1500% at level 500) |
| Resistance | +2% per player level (capped at +50%) |
| Speed | +1% per player level (capped at +25%) |
| Per-Player (multiplayer) | +75% per additional nearby player |

**Note:** The player-level scaling rules use the game's built-in `bScaleByAverageNearbyPlayerLevel` system. These rules are defined in D_ScalingRules and are available for any game system that references them. The primary scaling comes from the massively expanded spawn zone levels, which feed into the game's existing creature growth curves.

## Creature Count by Tier

| Tier | Count | Examples |
|------|-------|---------|
| Passive | 38 | Deer, Rabbits, Kea, Sheep, Chamois |
| Small Predator | 25 | Wolves, Spiders, Slugs, Hyenas |
| Medium Predator | 47 | Bears, Jaguars, Scorpions, Landsharks, Crocodiles |
| Boss | 28 | Mammoths, Polar Bear Boss, Sandworms, Rock Golem |

### 4. Affliction System (22 chances + 8 afflictions + 6 modifiers)
Creatures now inflict meaningful status effects during combat:

| Affliction | Chance | Duration | Effect |
|-----------|--------|----------|--------|
| Caveworm Poison | 100% | 40s | Poison damage over time |
| Concussion (Contusion) | 35% | 2400s | From heavy hits (buffalo, etc.) |
| Food Poisoning | 50% | 900s | From contaminated sources |
| Dysentery | 25% | 900s | From dirty water |
| Swamp Parasites | 25% | 600s | Swamp biome hazard |
| Frostnip Escalation | 50% | — | Cold exposure chains |
| Heatstroke Escalation | 50% | — | Heat exposure chains |
| Deep Wound Escalation | 15% | 2400s | Severe bleed progression |

**Stat Afflictions:**

| Affliction | Duration | Notes |
|-----------|----------|-------|
| Poison | 65s | General creature poison |
| Poison Sting | 35s | Insect/scorpion stings |
| Poison Sting (Stackable) | 20s | Stacks from swarm attacks |
| Komodo Bite | 2000s | Long-lasting infection |
| Bee Swarm | 20s | Bee hive defense |
| Sprain | 15s | Fall/impact injury |
| Exotic Debuff | 2500s | Exotic creature encounter |
| Red Exotic Debuff | 2800s | Red exotic creature encounter |

**Modifier States:**

| Modifier | Effect |
|---------|--------|
| Broken Leg | -50% movement speed, -20% stamina regen |
| Spore Poison | -20% movement speed |
| Sandworm Poison | -35% movement speed |
| Enraged (NPC) | +75 HP, +15% move speed (creature buff) |
| Splint / Workshop Splint | +10% / +20% fall damage resistance |

### 5. Epic Creatures & Exotic Loot
4 new epic creature types with custom loot tables:

| Type | Description |
|------|------------|
| Exotic Infused | Exotic-enhanced creatures |
| Red Exotic Infused | Rare red exotic variant |
| Larger Creature | Oversized creature spawns |
| Hunting Slugs | Aggressive slug encounters |

**Exotic Creature Loot Drops:**
- Leather (5-30), Fur (5-20), Bone (4-16), Meta Resource (6-30)
- 1% chance for Pyritic Crust (Purple Exotic) — rare drop

### 6. Biome Temperature Modifiers (19 biomes)
Custom temperature curves per time of day across all biomes: Conifer, Arctic, Desert, RiverLands, Desert Canyons, Southern Glacier, and all Styx/Prometheus/Elysium zones.

### 7. Prospect Difficulty Stats (6 entries)
Dynamic creature difficulty and NPC spawn rate scaling per prospect difficulty level:

| Setting | Effect |
|---------|--------|
| Easy Creatures | Reduced creature stats |
| NPC Increase Easy/Medium/Hard | Scaled NPC spawn rates |
| Hard + Spawn Rates | Maximum NPC density |
| Recon Creatures | Scouting encounter tuning |

### 8. Autonomous Spawns (6 zones)
New autonomous spawn sources: Caveworm Spawners, Swamp Gas Flyers, Lava Flyers, Spiders, Wild Beehive Trees, NPC Outposts.

## Technical Details

- Modifies **161 spawn zones** in D_AISpawnZones (all biomes, all maps)
- Modifies **180 creature entries** in D_AIGrowth (full vanilla + DLC coverage — New Frontiers, Styx, Dread)
- Adds **5 scaling rules** to D_ScalingRules
- **v2.2:** Explicitly buffs 6 tames and 16 mounts so pets can survive high-level hostile creatures
- **v2.3:** Adds **22 affliction chances**, **8 stat afflictions**, **6 modifier states**, **4 epic creatures**, **2 exotic loot tables**, **19 biome temp modifiers**, **6 prospect stats**, **6 autonomous spawns**
- 11 data tables modified across 419 total entries
- All stat buffs are percentage-based, stacking with existing creature stats
- Spawn zone scaling preserves relative difficulty progression between zones
- Compatible with any level cap mod (optimized for 500 cap)

## Biome Coverage

| Map | Zones Modified |
|-----|---------------|
| Olympus (OLY) | Conifer Easy/Medium/Hard/Super Hard, Desert Easy/Medium/Hard/Super Hard |
| Styx (STYX) | Conifer, Arctic, Desert (all tiers + Croc variants) |
| Prometheus (PRO) | Grasslands, Arctic, Tundra, Swamp, Lava, Icesheet, Ashlands, Volcanic |
| Elysium (ELY) | Arctic, Tundra, Volcanic, Geothermal, Desert, Swamp |
| Outposts | Forest, Arctic, Desert, Tundra, Volcano, Beach |

## Installation

1. Place the `.EXMODZ` file in your Icarus Mod Manager mods folder
2. Enable the mod in the Mod Manager
3. Launch the game
4. **Recommended:** Also install JimK72's Level Cap 500 mod for full experience

## Changelog


### v2.4.1 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v2.4
- Fixed the creature health-regen scaling, which never worked - 158 creature rows buffed a stat that does not exist (BaseHealthRegenPerMinute_+%), so the game ignored it; they now use the real BaseHealthRegen_+% with the same values. Fixed 4 re-themed Styx biomes having no ambient sound - they named sound sets that do not exist; they now use the ones vanilla pairs with the same atmosphere (Wetlands, Lava, BossGolemCave). Scales creature difficulty across biomes and threat levels.

### v2.3 — Affliction System & Epic Creatures (DarkAngel Collab)

Adds a full affliction/status effect system to creature combat, plus epic creatures, exotic loot, biome temperatures, and autonomous spawns. Credit to DarkAngel for contributing the affliction system, biome temps, and epic creature additions.

**New tables added:**
- **Affliction Chances (22):** Poison, concussion, frostbite, heatstroke, dysentery, wound escalation, swamp parasites, caveworm poison, and more — creatures now inflict meaningful status effects
- **Stat Afflictions (8):** Poison (65s), Poison Sting (35s), Komodo Bite (2000s), Bee Swarm (20s), Sprain (15s), Exotic Debuffs
- **Modifier States (6):** Broken Leg (-50% speed), Spore/Sandworm Poison (movement debuffs), Enraged NPC buff (+75 HP, +15% speed), Splints
- **Epic Creatures (4):** Exotic Infused, Red Exotic Infused, Larger Creature, Hunting Slugs
- **Exotic Loot (2):** Leather, Fur, Bone, Meta Resource drops + 1% Pyritic Crust (Purple Exotic) rare drop
- **Biome Temperatures (19):** Custom day/night temperature curves for all biomes
- **Prospect Stats (6):** Per-difficulty creature scaling and NPC spawn rate modifiers
- **Autonomous Spawns (6):** Caveworm Spawners, Swamp Gas Flyers, Lava Flyers, Spiders, Wild Beehives, NPC Outposts

### v2.2 — Tame & Mount Survival Pass

**Fixes the "my wolf dies in 3 seconds" problem.**

Prior versions left the Tame_* and Mount_* entries almost untouched — they had a flat 40% damage resistance but zero HP boost and zero melee damage boost. As players progressed into higher-level zones and tougher biomes, tames and mounts couldn't keep up with the scaled-up hostile creatures the mod was already buffing, and were getting shredded.

**What changed:**

| Creature class | HP | Melee | Phys Resist | Other Resists | Regen |
|---|---|---|---|---|---|
| **Tames** (6) — Wolf, Cat, Wildboar, Tundra Monkey, Orka, Storca | **+200%** | **+120%** | 40% → **60%** | 40% → **55%** (fire/frost/explosive/poison) | +100% |
| **Mounts** (16) — Horse, Buffalo, Chew, Moa, Raptor, Slinker, Snow Striker, Swamp Bird/Quad, Tusker, Woolly Mammoth, Wooly Zebra, Zebra, BlueBack, Bull | **+150%** | unchanged (mounts don't fight) | 40% → **55%** | 40% → **50%** | +75% |

Tames can now hold their own against scaled-up hostile creatures in open combat. Mounts are much harder to kill out from under you when riding through a pack.

**Not touched:** Mount_SpeederBike (it's a mechanical vehicle, not a creature), NPC companions, livestock (Pig, Sheep, Cow, Chicken, Lamb, Piglet, Rooster) — those stay vanilla since they're farm animals, not combat pets.

**DLC coverage confirmed:** CDS currently covers 100% of creatures in New Frontiers (Prometheus lava creatures), Styx (Geothermal biome, drones, Reavers), Dread (Irradiated mutations), and all juvenile/boss variants. No DLC creatures are missing.

### v2.1
- Added 44 new creature growth entries for taming/mount content (dogs, horses, mounts, juveniles, tamed pets, speeder bike)
- Total creature entries: 180 (up from 136)

### v2.1
- **Major overhaul** — expanded from creature-only buffs to full zone scaling
- Added 161 spawn zone level modifications (all maps/biomes)
- Scaled zone levels from vanilla max 120 to support level 500 cap
- Added speed scaling rule (+1% per player level, capped 25%)
- Enhanced multiplayer scaling (50% → 75% per additional player)
- Updated scaling rules InMaxValue from 100 to 500
- Updated scaling rule output ranges for 500 cap

### v1.0
- Initial release
- 136 creature modifications across 4 difficulty tiers
- 3 player-level scaling rule additions
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
