<div align="center">

# Mining Laser Overclock

[![Version](https://img.shields.io/badge/v1.0.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMODZ%20(PAK)-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

The **first-ever mining-laser blueprint mod**. No more stopping to let the laser cool — overclock it for sustained, uninterrupted deep mining.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Changes

| Value | Vanilla | Overclocked |
|---|---|---|
| Seconds of use before overheat | 5s | **300s** |
| Cooldown time | 5s | **1s** |

In practice the laser will never overheat during normal mining, and if you somehow push it that far it recovers almost instantly.

## How It Works

A blueprint (PAK) mod that byte-patches the `SecondsToReachMaxHeat` and `SecondsToCooldown` FloatProperties in `BP_Actionable_MiningLaser`. Bundled as cooked `.uasset`/`.uexp` files that the Mod Manager merges into the game pak. Nobody has modded an individual tool blueprint like this before.

## Installation

1. Install JimK72's Icarus Mod Manager
2. Import `Mining_Laser_Overclock.EXMODZ`
3. Rebuild the merged mod and restart Icarus

## Changelog

### v1.0.1 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v1.0
- Initial release
- Overheat threshold 5s → 300s, cooldown 5s → 1s
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
