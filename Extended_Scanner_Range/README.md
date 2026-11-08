<div align="center">

# Extended Scanner Range

[![Version](https://img.shields.io/badge/v1.0.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

**10× detection range** for the Cave Scanner and Fish Finder — locate caves and fishing spots from far further out. Companion to Extended Deep Ore Scanner Range.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Changes

| Scanner | Vanilla Range | Modded Range |
|---|---|---|
| Cave Scanner | 300m | **3000m (3km)** |
| Fish Finder / base scanner | 150m | **1500m** |

The Fish Finder inherits the base scanner range, so patching the base extends it (and any other scanner without its own range override).

## How It Works

PAK mod patching `MaxScanningRange` in `BP_ActionableBehaviour_Scanner_Cave` (30000 → 300000 cm) and `BP_ActionableBehaviour_Scanner` (15000 → 150000 cm). Same-size in-place blueprint byte-patches.

## Installation

Install via JimK72's Icarus Mod Manager.

## Multiplayer

All players AND the server must have this mod installed.

## Changelog

### v1.0.1 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v1.0
- Initial release
- 10× Cave Scanner range (300m → 3000m) and 10× base/Fish Finder range (150m → 1500m)
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
