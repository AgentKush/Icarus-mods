<div align="center">

# Always Show Buildings On Map

[![Version](https://img.shields.io/badge/v1.0.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Always shows player-built structures on the map and minimap without requiring radar or special stats.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Overview

Always shows player-built structures on the map and minimap without requiring any special stats or radar. Buildings will always display the home icon on both the world map and compass.

## Features

### Map Visibility

| Feature | Status |
|---------|--------|
| World Map Icon | ✅ Always visible |
| Minimap Icon | ✅ Always visible |
| Compass Display | ✅ Always visible |
| Radar Required | ❌ Not needed |

## How It Works

By default, Icarus requires the `MapCanSeeBuildings` player stat (typically from a radar or talent) to see your buildings on the map. This mod removes that requirement, so your bases and structures are always visible.

## Technical Specifications

| Metric | Value |
|--------|-------|
| Total Modifications | 1 |
| Map Icons Changed | 1 |

### Files Modified
- `UI-D_MapIcons.json` (1 entry)

### Changes Made

| Field | Original Value | New Value |
|-------|----------------|-----------|
| RequiredPlayerStatToShow | `MapCanSeeBuildings_?` | `None` |

## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus
5. Buildings now always appear on map and compass

## Gameplay Notes

- Ideal for Open World mode where finding your base is essential
- Eliminates need to craft radar just for building visibility
- Works with all building types and materials

## Compatibility

| Mod | Status |
|-----|--------|
| All AgentKush mods | ✅ Compatible |
| Other UI-D_MapIcons mods | ⚠️ May conflict |

## Version History

| Version | Changes |
|---------|---------|
| 1.0.1 | New icon and banner, drawn from the mod's live data. No gameplay change. |
| 1.0 | Initial release |
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
