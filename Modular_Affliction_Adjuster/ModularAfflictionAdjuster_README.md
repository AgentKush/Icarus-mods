# Modular Affliction Adjuster

**Author:** AgentKush  
**Version:** 2.0  
**Compatible with:** Icarus (JimK72's Mod Manager)

## Overview

Comprehensive affliction adjustment mod covering **110 afflictions** across all biomes and hazard types. Reduces stat penalties by ~50%, extends escalation times by ~50%, and reduces damage-over-time by ~50%. Survival remains challenging but significantly more forgiving.

## Summary by Category

| Category | Count | Key Changes |
|----------|-------|-------------|
| 🤒 Diseases | 4 | 50% reduced penalties |
| 🩹 Wounds | 6 | Escalation 2min → 5min |
| 🦴 Physical Injuries | 7 | 50% reduced penalties |
| 🕳️ Cave/Underground | 1 | Escalation 2min → 5min |
| 🌡️ Temperature | 10 | Escalation 10min → 15min |
| 🍖 Survival | 7 | 50% reduced damage |
| ☠️ Poison/DOT | 20 | 50% reduced damage |
| 🐍 Creature Attacks | 11 | 50% reduced damage |
| ☢️ Radiation | 2 | 50% reduced damage |
| 🌿 Environmental | 11 | 50% reduced damage/penalties |
| ⛈️ Storms | 15 | 50% reduced penalties |
| 🏔️ Biome Weather | 23 | 50% reduced damage |
| 💎 Exotic Debuffs | 15 | 50% extended escalation |
| 💧 Dirty Water | 2 | 50% reduced penalties |

## Detailed Changes

### 🤒 Disease Afflictions

| Affliction | Original | Modified |
|------------|----------|----------|
| **Pneumonia** | -50% health regen, -50% stamina, -10% XP | -25%, -25%, -5% |
| **Food Poisoning** | -50% health, -50% stamina, -25% speed | -25%, -25%, -12% |
| **Dysentery** | -50% food recovery | -25% food recovery |
| **Dysentery (Lava)** | 8 dmg/tick | 4 dmg/tick |

### 🩹 Wound Chain

| Affliction | Escalation | Health Regen |
|------------|------------|--------------|
| **Wound** | 2min → **5min** | -80% → **-50%** |
| **Deep Wound** | 2min → **5min** | -95% → **-70%** |
| **Infected Wound** | - | -80% → **-50%** |
| **Festering Wound** | - | -95% → **-70%** |

### 🦴 Physical Injuries

| Affliction | Original | Modified |
|------------|----------|----------|
| **Concussion** | -25% craft speed, -20% move | -12%, -10% |
| **Contusion** | -25% XP, -20% move | -12%, -10% |
| **Enfeebled** | -25% melee, -20% carry | -12%, -10% |
| **Blunt Trauma** | -25% melee | -12% melee |
| **Sprained Ankle** | -25% move, -20% carry | -12%, -10% |
| **Broken Leg** | -50% move | -25% move |
| **Broken Leg (Minor)** | -10% move | -5% move |

### 🕳️ Cave Sickness (Underground)

| Setting | Original | Modified |
|---------|----------|----------|
| Escalation Time | 2min | **5min** |
| Health Regen | -50% | **-25%** |
| Max Stamina | -33% | **-16%** |

### 🌡️ Temperature Afflictions

| Affliction | Escalation | Key Changes |
|------------|------------|-------------|
| **Frostnip** | 5min → **7.5min** | -15% → **-8%** move |
| **Frostbite** | - | -25% → **-12%** move |
| **Cold** | 10min → **15min** | -25% → **-12%** stamina |
| **Hypothermia** | - | 1 → **0.5** dmg/tick |
| **Heatstroke** | 5min → **7.5min** | -15% → **-8%** carry |
| **Heat Exhaustion** | - | -30% → **-15%** health regen |
| **Overheating** | 10min → **15min** | +50% → **+25%** water |
| **Hyperthermia** | - | 1 → **0.5** dmg/tick |

### 🍖 Survival Afflictions

| Affliction | Original | Modified |
|------------|----------|----------|
| **Thirsty** | -25% stamina regen | -12% |
| **Dehydrated** | 2 dmg/tick, -50% stamina | 1 dmg, -25% |
| **Hungry** | 5min escalation | **10min** |
| **Famished** | 2 dmg/tick | 1 dmg/tick |
| **Disoriented** | -10% XP | -5% XP |
| **Suffocation** | 2% health/tick | 1%/tick |
| **Drowning** | 15 dmg/tick | 8 dmg/tick |

### ☠️ Poison & DOT Effects

| Effect | Original | Modified |
|--------|----------|----------|
| **Physical DOT** | 2 dmg | 1 dmg |
| **Burning** | 10 dmg | 5 dmg |
| **Bleeding** | 5 dmg | 2.5 dmg |
| **Radiation DOT** | 8 dmg | 4 dmg |
| **Burn** | 40 dmg | 20 dmg |
| **Poison** | 1 dmg | 0.5 dmg |
| **Poison DOT** | 5 dmg | 2.5 dmg |
| **Spore Poison** | 2 dmg | 1 dmg |

### 🐍 Creature Poisons

| Creature | Original Damage | Modified |
|----------|-----------------|----------|
| **Cave Worm** | 4 dmg | 2 dmg |
| **Sandworm** | 5 dmg | 2.5 dmg |
| **Forest Worm** | 5 dmg | 2.5 dmg |
| **Desert Worm** | 3 dmg | 1.5 dmg |
| **Arctic Worm** | 8 dmg | 4 dmg |
| **Scorpion Sting** | 10 dmg | 5 dmg |
| **Bee Swarm** | 2 dmg | 1 dmg |
| **Gas Flyer** | -60% move, -95% stamina | -30%, -50% |
| **Komodo Bite** | +100% poison duration | +50% |

### ☢️ Radiation

| Effect | Original | Modified |
|--------|----------|----------|
| **Radiation Sickness** | 50 dmg, -20% health/stamina | 25 dmg, -10% |
| **Radiation DOT** | 8 dmg | 4 dmg |

### 🌿 Environmental Hazards

| Hazard | Original | Modified |
|--------|----------|----------|
| **Miasma** | 40 dmg | 20 dmg |
| **Sulfur Pool** | 5 dmg | 2.5 dmg |
| **Spiked Brambles** | 4 dmg, -50% move | 2 dmg, -25% |
| **Swamp Water** | -20% move | -10% move |

### ⛈️ Storm Exposure

All storm intensities (Light/Medium/Heavy) reduced by ~50%:
- Movement penalties: halved
- XP penalties: halved  
- Damage (heavy storms): halved

### 🏔️ Biome Weather (23 types)

All biome weather effects reduced by ~50%:
- **Arctic**: Hail, Wind, Snow, WhiteOut
- **Conifer**: Hail, Wind, Rain, Fog
- **Desert**: Sand, Wind, Heatwave
- **Swamp**: AcidRain, AcidFog, Rain, Wind, ToxicGas
- **Volcanic**: Ash, AcidRain, SulfurReaction, Embers, Heatwave, VolcWinter, ColdFront

### 💎 Exotic Debuffs

| Tier | Escalation | Key Changes |
|------|------------|-------------|
| **Base** | 5min → **7.5min** | Consumption +20% → +10% |
| **T1** (Food/Water/Oxygen) | 3min → **4.5min** | +50% → +25% |
| **T2** (Poison/Wound/etc) | 1min → **1.5min** | 50% reduced penalties |
| **T3** (DeepWound/Temp) | - | 50% reduced penalties |
| **T4** (Rapid DOTs) | - | 35 → 17.5 dmg/tick |

## Installation

1. Copy `ModularAfflictionAdjuster.EXMODZ` to your Mod Manager folder
2. Enable via JimK72's Icarus Mod Manager
3. Launch game

## Customization

The mod is organized into 15 clearly labeled sections. To customize:

1. Extract the EXMODZ (it's a ZIP file)
2. Edit `ModularAfflictionAdjuster.EXMOD` in any text editor
3. Delete entire entries to restore vanilla behavior for specific afflictions
4. Adjust values as desired
5. Repackage as EXMODZ (ZIP and rename)

## Compatibility

- ✅ Works with most other mods
- ✅ Safe to add/remove mid-game
- ✅ All afflictions still function, just less punishing
- ⚠️ May conflict with other affliction-modifying mods

## Changelog

### v2.0
- **Major expansion**: 21 → 110 afflictions
- Added Cave Sickness (Underground)
- Added all physical injuries (Concussion, Contusion, Broken Leg, etc.)
- Added all creature poisons (Worms, Scorpions, Komodo, etc.)
- Added all storm exposure types
- Added all biome weather effects (Arctic, Desert, Swamp, Volcanic, Conifer)
- Added all exotic debuffs (T1-T4)
- Added radiation effects
- Added environmental hazards (Miasma, Sulfur, Brambles)
- Added temperature pre-stages (Frostnip, Heatstroke)

### v1.0
- Initial release with 21 core afflictions
