<div align="center">

# Extended Wire and Pipe Tool

[![Version](https://img.shields.io/badge/v1.1.2-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/PAK%20%2B%20EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

10x range extension for all power cables and pipes. Power cables 60m, water pipes 60m, biofuel pipes 60m, crude oil pipes 100m. Also makes the game's unfinished Road Kit craftable.

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
| Roads (Road Kit, below) | 40m | **8m per piece** (short on purpose, see below) |
| Tool Trace Distance | 30m | **300m** |
| Inspector Range | 200m | **2000m** |

## Road Kit

The game ships a Road Kit that lays asphalt roads with a yellow centre line, using the same placement tool as cables and pipes. It was never finished: it has no recipe, an invisible model, a placeholder icon and no quickbar slot. This mod finishes it.

| | |
|---|---|
| Unlock | Learning the **Water Pipe Tool** blueprint (Tier 3 Machine tree) unlocks the Road Kit too |
| Crafted at | Machining Bench, Fabricator or Manufacturer |
| Cost | 50 Copper Wire, 50 Gold Wire, 4 Platinum Sheath (the Water Pipe Tool's cost) |
| Icon | A new asphalt-road icon drawn from the game's own road texture |
| In hand | The game's Tier 3 kit model, the one the Machining Bench kit uses |
| Road | The game's asphalt road (yellow centre line), 9.6m wide, surface at ground level, solid to walk on |
| Piece length | Up to 8m between points (game 40m). Each piece stretches one 3m copy of the asphalt texture, so short pieces keep it sharp |

Roads are not a released feature of the game, so try them on a new prospect first. Hold **R** to switch between curved and straight placement. Use straight when you join an existing road at an angle: a curved join can fold a 9.6m-wide road over itself.

## How It Works

PAK + EXMOD mod. The PAK side patches `BP_ActionableBehaviour_CurvedSplinePlace`: every `SplineTypeMaxDistance` entry x10 except roads, which are capped at 8m, plus the tool trace and inspector range. The EXMOD adds the Road Kit's recipe and fixes its item rows, and the bundle carries its icon texture (`ITEM_Kit_Road_0`).

Two more files are used only by roads:
- `SM_SplineRoad_Small_R` is the narrow cobblestone path the game currently draws roads with. The mod replaces it with the game's own `SM_SplineRoad` (the 9.6m asphalt road), lowered 65cm so its surface sits at ground level.
- `BP_IcarusSplineMesh_NavModifier` is the road piece component. The mod gives it the game's BlockAll collision; it inherited the cables' "ignore players" collision before.

## Installation

Install via JimK72's Icarus Mod Manager.

## Multiplayer

All players AND the server must have this mod installed.

## Changelog

### v1.1.2 (2026-11-21)
- **Road pieces capped at 8m** (was 400m; the game's value is 40m). Each piece between two points is one copy of the road mesh, which carries 3m of asphalt texture, so long pieces stretched it. At 8m it is stretched at most 2.7x. Shorter pieces also keep curved joins from swinging wide and twisting.
- Documented the Road Kit's curved/straight switch (hold R). Use straight to join an existing road at an angle.

### v1.1.1 (2026-11-21)
- **Roads fixed.** The game draws roads with an unfinished 1.9m cobblestone path mesh that players fall through. Roads now use the game's own asphalt road mesh (`SM_SplineRoad`, 9.6m wide) in its place, lowered 65cm so the surface sits at ground level instead of 75cm up.
- Road pieces now block players, using the game's BlockAll collision; before, they inherited the cables' "ignore players" collision. Cables and pipes are unchanged: they use a different component.

### v1.1 (2026-11-21)
- **Craftable Road Kit.** The game's unfinished `Kit_Road` gets a recipe at the Machining Bench, Fabricator and Manufacturer (50 Copper Wire, 50 Gold Wire, 4 Platinum Sheath, the Water Pipe Tool's cost). The recipe unlocks with the Water Pipe Tool blueprint.
- It replaces the blank blueprint placeholder with a new asphalt-road icon drawn from the game's road texture (`ITEM_Kit_Road_0`), and the invisible placeholder model with the game's Tier 3 kit model. It now has the quickbar tag, so it can be equipped, and the wire-tool tag, so the HUD shows curved or straight mode. The "To do." flavour text is removed.
- Placed roads use the game's own road mesh and material, with this mod's 400m range (game 40m).

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
