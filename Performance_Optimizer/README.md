<div align="center">

# Agents Optimization Mod

[![Version](https://img.shields.io/badge/v2.2-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/PAK%20%2B%20EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=unrealengine&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Comprehensive FPS optimization - PAK config overrides (foliage/shadow/fog/LOD reduction) plus data table changes (reduced spawns, slower hordes, extended decay, boosted fuel, weather tuning). It retunes 109 existing weather events and 5 weather pools — it does not add new ones. PAK + EXMODZ required.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Description

Comprehensive performance optimization mod combining engine-level config overrides (PAK) with data table adjustments (EXMOD) for maximum FPS improvement. The PAK component overrides foliage density, shadow quality, volumetric fog, texture streaming, and renderer settings at the engine level — changes impossible through EXMOD alone. The EXMOD component reduces creature loads, slows horde intensity, extends decay timers, boosts fuel efficiency, and biases weather toward lighter effects.

## What's New in v2.2 — PAK Engine Overrides

### Foliage & Grass (Biggest FPS Impact)
- Foliage density reduced 30-43% across all quality presets
- Grass density reduced 35-50% across all quality presets
- Foliage LOD distance scales tightened 30-40%
- MinimumScreenSize increased to cull small foliage earlier
- Ultra preset now has explicit density caps (was unlimited)

### Shadows & Lighting
- Shadow cascade count reduced (4→3 on Ultra, 3→2 on High)
- Shadow resolution capped at 2048 on High/Ultra (was 4096)
- Contact shadows disabled on Low/Medium
- Light draw distance reduced 10-22%
- Distance field shadow quality lowered

### Volumetric Fog
- Fog completely disabled on Low quality
- GridPixelSize increased 50-200% (fewer fog calculations per frame)
- GridSizeZ reduced 25-62% (less vertical fog resolution)
- History supersample count halved on Medium

### Renderer Pipeline
- Ray tracing fully disabled (RTXGI, RT shadows, reflections, AO, translucency)
- Mesh distance field generation disabled
- Reflection capture resolution halved (512→256)
- Virtual texture upload rate halved (4→2 per frame)
- Virtual texture feedback factor reduced
- Texture streaming pool sizes reduced 20-25%

### Post Processing
- Bloom quality reduced one tier across all presets
- AO radius and quality scaled down on Medium/High

## EXMOD Changes (300 Items across 7 Tables)

### AI - Creature Spawns (D_AISpawnZones) - 160 entries
- SpawnWeight reduced ~40% across all biome zones

### AI - Autonomous Spawns (D_AutonomousSpawns) - 22 entries
- MaxSpawnCount reduced 40%, MaxDistanceToPlayers reduced 25%

### Horde Waves (D_HordeWave) - 21 entries
- TotalToSpawn -40%, TimeBetweenSpawns +50%, NumberToSpawnAtATime -30%

### Weather Events (D_WeatherEvents) - 109 entries
- Tier 0-2: Duration +30% | Tier 5-6: Duration -50%

### Decay Timers (D_Decayable) - 32 entries
- All decay timers doubled

### Fuel Efficiency (D_Combustible) - 4 entries
- All fuel doubled

### Weather Pool Biasing (D_WeatherPools) - 2 entries
- T0-T2 weather boosted, T4-T6 reduced 50-85%, particle-heavy types -30%

## Installation

**Both files are required for the full optimization:**

1. Copy `Performance_Optimizer_P.pak` to your game's `Icarus\Content\Paks\mods\` folder
2. Import `Agents_Optimization_Mod.EXMODZ` using JimK72's Icarus Mod Manager
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
