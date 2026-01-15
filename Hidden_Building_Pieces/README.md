# Hidden Building Pieces

![Version](https://img.shields.io/badge/version-2.2.0-blue)
![Author](https://img.shields.io/badge/author-AgentKush-green)
![Compatibility](https://img.shields.io/badge/compatibility-All%20DLCs-brightgreen)

## Overview

Unlocks 54 hidden diagonal and curved building pieces for 9 different materials. These architectural elements exist within the game files but remain inaccessible in vanilla gameplay. All pieces can be repaired and crafted at appropriate workstations.

**v2.2.0 now fixes greyed-out textures** for Stone Brick and Scoria Brick diagonal/curved pieces by applying proper Scoria stone materials.

## Features

### Materials Supported

| Material | Building Types | Texture Status |
|----------|----------------|----------------|
| Concrete | Diagonal and curved elements | ✅ Native |
| Glass | Diagonal and curved elements | ✅ Native |
| Clay Brick | Diagonal and curved elements | ✅ Native |
| Stone | Diagonal and curved elements | ✅ Native |
| Scoria | Diagonal and curved elements | ✅ Native |
| Tempered Glass | Diagonal and curved elements | ✅ Native |
| Scoria Brick | Diagonal and curved elements | ✅ Fixed (uses Scoria textures) |
| Stone Brick | Diagonal and curved elements | ✅ Fixed (uses Scoria textures) |
| Ice | Diagonal and curved elements (hand-craftable) | ✅ Native |

### Building Piece Types

Each material includes diagonal floor/wall pieces, curved wall sections, corner transitions, and curved roofing elements designed to complement existing building sets.

## Crafting Stations

| Station | Materials Craftable |
|---------|---------------------|
| Masonry Bench | Clay Brick, Stone, Stone Brick sets |
| Cement Mixer | Concrete sets |
| Electric Masonry Bench | Advanced stone and brick sets |
| Glassworking Bench | Glass, Tempered Glass sets |
| Scoria Forge | Scoria, Scoria Brick sets |
| Hand Crafting | Ice sets |

## Technical Specifications

| Metric | Value |
|--------|-------|
| Total Modifications | 288 |
| Building Pieces | 54 |
| Materials | 9 |
| Texture Fixes | 72 |

### Files Modified
- `Traits-D_Itemable.json` (54 entries)
- `Items-D_ItemsStatic.json` (54 entries)
- `Items-D_ItemTemplate.json` (54 entries)
- `Crafting-D_ProcessorRecipes.json` (54 entries)
- `Building-D_BuildingSkins.json` (72 entries) - NEW in v2.2.0

## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus
5. Craft new pieces at the appropriate workstation

## Compatibility

| Mod | Status |
|-----|--------|
| FastProcessing (v4.0+) | ✅ All 54 recipes included |
| Workshop Recyclers | ✅ Compatible |
| All AgentKush mods | ✅ Compatible |

## Version History

| Version | Changes |
|---------|---------|
| 2.2.0 | **Major texture fix**: Fixed greyed-out textures for Stone Brick (36 pieces) and Scoria Brick (36 pieces) diagonal/curved building pieces by overriding D_BuildingSkins with proper Scoria stone materials |
| 2.1.2 | Fixed missing icons for Stone Brick (6 pieces), Scoria Brick (6 pieces), Scoria (4 pieces), and Ice (4 pieces) |
| 2.1.1 | Fixed missing icons for Stone building pieces |
| 2.1.0 | Expanded to 54 pieces across 9 materials |
| 1.0.7 | 18 pieces for Concrete, Glass, and Clay Brick |

## Technical Notes

The game's original data had Stone Brick and Scoria Brick diagonal/curved pieces referencing Tempered Glass materials (developer placeholder). This mod corrects them to use Scoria stone materials, which provides a much better visual match for brick building pieces.

---

*Last Updated: January 15, 2026*

*Part of the [AgentKush Icarus Mods](https://github.com/AgentKush/Icarus-mods) collection*
