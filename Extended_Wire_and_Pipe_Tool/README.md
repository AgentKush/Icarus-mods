<div align="center">

# Extended Wire and Pipe Tool

[![Version](https://img.shields.io/badge/v1.0.2-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

10x range extension for all power cables and pipes. Power cables 60m, water pipes 60m, biofuel pipes 60m, crude oil pipes 100m.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Changes

| Connection Type | Vanilla Range | Modded Range |
|---|---|---|
| Power Cables | 6m | **60m** |
| Water Pipes | 6m | **60m** |
| Biofuel Pipes | 6m | **60m** |
| Crude Oil Pipes | 10m | **100m** |
| Tool Trace Distance | 30m | **300m** |
| Inspector Range | 200m | **2000m** |

## How It Works

PAK mod that patches BP_ActionableBehaviour_CurvedSplinePlace to extend the SplineTypeMaxDistance values for all cable and pipe types.

## Installation

Install via JimK72's Icarus Mod Manager.

## Multiplayer

All players AND the server must have this mod installed.

## Changelog

### v1.0.2 (2026-11-21)
- `BP_ActionableBehaviour_CurvedSplinePlace` rebuilt from the 19 November 2026 game files (build 26636089) with the same changes: all 8 `SplineTypeMaxDistance` entries x10, `TraceDistance` 3000 -> 30000 and `InspectorTraceRange` 20000 -> 200000. Those 10 values are the only difference from the game's own copy.
- The old copy dated from February 2026. Its logic still matched the game, but it lacked one dependency the game has added since (`BP_IcarusSplineActor`'s nav modifier component).

### v1.0.1 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v1.0
- Initial release
- 10x range extension for all cable and pipe types
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
