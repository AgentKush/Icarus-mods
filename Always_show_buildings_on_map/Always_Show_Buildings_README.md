# Always Show Buildings On Map

![Version](https://img.shields.io/badge/version-1.0-blue)
![Icarus](https://img.shields.io/badge/game-Icarus-green)
![Author](https://img.shields.io/badge/author-AgentKush-orange)

## Description

Always shows player-built structures on the map and minimap without requiring any special stats or radar. Buildings will always display the home icon on both the world map and compass.

## What It Does

By default, Icarus requires the `MapCanSeeBuildings` player stat (typically from a radar or talent) to see your buildings on the map. This mod removes that requirement, so your bases and structures are always visible.

## Installation

1. Download `Always_Show_Buildings_On_Map.EXMODZ`
2. Place in your Icarus Mod Manager mods folder
3. Enable the mod in JimK72's Mod Manager
4. Launch the game

## Compatibility

- **Game Version**: Compatible with current Icarus weekly builds
- **Mod Conflicts**: May conflict with other mods that modify `UI-D_MapIcons.json`

## Technical Details

**Modified Data Table**: `UI-D_MapIcons.json`

**Changes Made**:
| Field | Original Value | New Value |
|-------|----------------|-----------|
| RequiredPlayerStatToShow | `MapCanSeeBuildings_?` | `None` |
| bDisplayOnCompass | `true` | `true` |

## Changelog

### v1.0
- Initial release
- Buildings always visible on map and compass

## Author

Created by **AgentKush**

## License

Free to use and modify.
