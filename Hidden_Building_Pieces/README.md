<div align="center">

# Hidden Building Pieces

[![Version](https://img.shields.io/badge/v4.5-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Unlocks 34 building pieces + 1 forgotten recipe as individual craftable items

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

Unlocks **34 building pieces** that exist in the game files but aren't available to players, plus 1 forgotten recipe added to higher-tier stations. Every item is an individual craftable piece at the appropriate workbench. All pieces are **storm immune** and **hammer repairable**. Storm immunity is set per building material, so every building made of those 15 materials - the game's own pieces included - takes no wind damage.

> **v4.5:** Rebuilt for the November 2026 frame rework — every piece checked against the current game data. The Iron, Sandworm and Metal Grate pieces can now be crafted, and the frames that used deleted blueprints can be placed again.

---

## Features

### Wood Diagonal Pieces (7 items)

Non-curved diagonal Wood pieces that vanilla still doesn't include:

- Diagonal Floor, Diagonal Ramp Roof
- Diagonal Wall Solid, Diagonal Wall Angles
- Diagonal Beam Diagonal, Diagonal Beam Horizontal
- Brick Beam DiagonalBeam

**Crafted at:** Carpentry Bench

### Frames (26 items)

Frame pieces for 11 materials. Each material has the frame variants that vanilla is missing:

| Material | FullFrame | HalfFrame | Pillar | Bench |
|----------|:---------:|:---------:|:------:|-------|
| ClayBrick | x | x | x | Masonry Bench |
| Glass | x | x | x | Glassworking Bench |
| Ice | x | x | | Hand Crafting |
| Iron | x | x | x | Anvil Bench |
| Limestone | | x | | Masonry Bench |
| ReinforcedWood | x | x | | Carpentry Bench |
| Sandworm | x | x | | Masonry Bench |
| Scoria | | x | | Masonry Bench |
| ScoriaBrick | x | x | x | Masonry Bench |
| StoneBrick | x | x | x | Masonry Bench |
| TemperedGlass | x | x | x | Glassworking Bench |

### Metal Grate Quarter Floor (1 item)

- Metal Grate HalfNormal QuarterFloor

### Interior Wood Floor — The Forgotten Floor (1 recipe)

- Interior Wood Floor (`Wood_Floor_Refined`) — exists in vanilla at the Carpentry Bench only, with mismatched names across data tables making it nearly impossible to find. Now also craftable at Fabricator and Manufacturer.

**Crafted at:** Fabricator / Manufacturer (same inputs: 20 Refined Wood + 4 Copper Nails)

---

## Stats

| Category | Count |
|----------|-------|
| Craftable Items | 34 |
| Building Pieces | 36 |
| Building Skins | 34 |
| Crafting Recipes | 35 |
| Durable Entries | 16 |
| Building Types | 21 |
| **Total Data Entries** | **278** |

## Crafting Locations

| Material | Crafting Station |
|----------|-----------------|
| Wood / ReinforcedWood | Carpentry Bench |
| ClayBrick / ScoriaBrick / StoneBrick / Limestone / Sandworm / Scoria | Masonry Bench |
| Glass / TemperedGlass | Glassworking Bench |
| Iron / MetalGrate | Anvil Bench |
| Interior Wood (Forgotten Floor) | Fabricator / Manufacturer |
| Ice | Hand Crafting |

## Installation

### Via Mod Manager (Recommended)
1. Add this repository URL to the Mod Manager's modinfo sources
2. Find "Hidden Building Pieces" and install
3. Click Merge to apply

### Manual Installation
1. Download `Hidden_Building_Pieces.EXMODZ`
2. Place in: `Icarus_Mod_Manager_2_x_x/Extracted_Mods/`
3. Use the Mod Manager to merge and install

## Compatibility

- Works with all other mods
- Multiplayer compatible (all players need the mod)
- Compatible with all DLCs
- Compatible with Kepler update / Dangerous Horizons

---

## Changelog

### v4.5 (2026-11-07)
**Rebuilt for the November 2026 frame rework** - every piece checked against the current game data.
- **5 frames used blueprints the update deleted** and could not be placed: the Iron full and half frames now use the Stone frame and angled-frame blueprints (like this mod's other full and half frames), the Limestone half frame the Concrete angled frame, and the Reinforced Wood and Sandworm half frames the Wood angled frame - the same blueprints the game's own half frames use.
- **6 pieces can now be crafted.** The Iron frames, Sandworm frames and Metal Grate quarter floor asked for `Iron_Ingot` and `Sandite`, which the game does not have. They now cost what the game charges for its own pieces: Iron frames as an Iron beam set (Bauxite, Wood, Steel Screws), Sandworm frames as a Sandworm beam set (Fiber, Wood, Sandworm Scale), the Metal Grate quarter floor as a metal grate floor (Aluminium, Steel Rebar, Steel Screws).
- **Stability:** 15 pieces pointed at stability rows that do not exist; they now use the rows the game uses for those materials (Limestone -> Concrete frame, Scoria -> Stone frame, Sandworm and Reinforced Wood -> reinforced beam, Stone Brick and Scoria Brick -> clay brick, Tempered Glass -> tempered glass).
- **Piece types:** `Frame_FullFrame` / `Frame_HalfFrame` are not building types the game knows; the frames now use `Frame` / `Frame_Angle`, as the game's own full and half frames do.
- **Materials:** the clay brick and iron frame materials were renamed and the metal grate floor material moved; Stone Brick frames drop a second material the game deleted (matching the game's Stone Brick pillar); Reinforced Wood and Sandworm frames use the game's own reinforced-wood and sandworm pillar materials; the Limestone half frame uses the game's limestone frame materials.
- **Icons:** the game deleted the frame and wood diagonal icons this mod used. Frame items now show the game's pillar icon for their material; the wood diagonal, wood beam and ice frame pieces show the icon of the game piece with the same shape (the game has no wood diagonal icons).
- **Cleanup:** removed 32 building pieces and 34 skins left over from the stairs removed in v4.4, plus fields the game ignores (`Traits`, `MaterialSet`, and the icon/name/description copies on `D_ItemTemplate` - the real ones are on `D_Itemable`).

### v4.4 (2026-06-27)
- Removed 28 pieces now official in vanilla — all Corner Stairs (14), Glass/TemperedGlass Stairs (4), and curved Wood pieces (10) — added by the Week 142 (Corner & Half Stairs) and Week 234 (Curved Building) updates
- Updated all mesh references for the June 2026 game update (consolidated generic material meshes)
- Removed a stray Mesh_Generic_Ice override that conflicted with the base game's ice mesh

### v4.1 (2026-04-16)
- Added Interior Wood Floor recipe at Fabricator/Manufacturer — the "forgotten floor" that only existed at Carpentry Bench with mismatched data table names

### v4.0 (2026-04-14)
- MAJOR OVERHAUL: Rebuilt from scratch as individual items (no more sets)
- Removed all items now live in vanilla (Kepler update)
- Removed all 15 RoofPeak items (now in base game)
- Split remaining items from sets into individual craftable pieces

### v3.0.0 (2026-03-10)
- Removed 44 items now included in the base game (Kepler/Week 222 update)

### Earlier
- v2.13.x: skin/recipe/buildable reference fixes across DLC updates
