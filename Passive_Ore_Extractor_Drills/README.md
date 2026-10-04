<div align="center">

# Passive Ore Extractor Drills

[![Version](https://img.shields.io/badge/v7.7-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

23 passive ore extractors with drill visuals. Place anywhere, connect power, load Stone.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Description

23 passive ore extractors - one per ore type. Place anywhere, connect power, load Stone. Uses drill-visual processor for passive mining.

## How It Works

Each machine is dedicated to one ore type. Place it anywhere, connect electricity, load Stone, and it continuously produces ore. 1 Stone per cycle = generous ore output. Load 100 stone and walk away!

## Machines

| Passive Miner | Ore Output | Per Cycle | Energy Cost | Research | Replicate |
|--------------|-----------|-----------|-------------|----------|-----------|
| Passive Iron Miner | Iron | 25x | 2000 MJ | 50 | 25 |
| Passive Copper Miner | Copper | 25x | 2000 MJ | 50 | 25 |
| Passive Coal Miner | Coal | 25x | 2000 MJ | 50 | 25 |
| Passive Stone Miner | Stone | 25x | 2000 MJ | 50 | 25 |
| Passive Oxite Miner | Oxite | 15x | 3000 MJ | 75 | 35 |
| Passive Salt Miner | Salt | 15x | 3000 MJ | 75 | 35 |
| Passive Sulfur Miner | Sulfur | 15x | 3000 MJ | 75 | 35 |
| Passive Gold Miner | Gold | 15x | 3000 MJ | 75 | 35 |
| Passive Silicon Miner | Silicon | 15x | 3000 MJ | 75 | 35 |
| Passive Clay Miner | Clay | 15x | 3000 MJ | 75 | 35 |
| Passive Bauxite Miner | Bauxite | 10x | 5000 MJ | 100 | 50 |
| Passive Titanium Miner | Titanium | 10x | 5000 MJ | 100 | 50 |
| Passive Platinum Miner | Platinum | 10x | 5000 MJ | 100 | 50 |
| Passive Scoria Miner | Scoria | 10x | 5000 MJ | 100 | 50 |
| Passive Obsidian Miner | Obsidian | 10x | 5000 MJ | 100 | 50 |
| Passive Limestone Miner | Limestone | 10x | 5000 MJ | 100 | 50 |
| Passive Lithium Miner | Lithium | 10x | 5000 MJ | 100 | 50 |
| Passive Ruby Miner | Ruby | 5x | 8000 MJ | 150 | 75 |
| Passive Cobalt Miner | Cobalt | 5x | 8000 MJ | 150 | 75 |
| Passive Super Cooled Ice Miner | Super Cooled Ice | 5x | 8000 MJ | 150 | 75 |
| Passive Frozen Wood Miner | Frozen Wood | 5x | 8000 MJ | 150 | 75 |
| Passive Exotic Red Miner | Exotic Red | 5x | 8000 MJ | 150 | 75 |
| Passive Uranium Miner | Uranium | 5x | 8000 MJ | 150 | 75 |

## Fabricator Crafting Costs

All miners are craftable at the **Fabricator** with tiered material costs:

| Tier | Materials | Energy |
|------|-----------|--------|
| Common | 10 Steel Ingot, 5 Electronics, 5 Refined Metal, 4 Steel Screw | 8,000 MJ |
| Uncommon | 15 Steel Ingot, 10 Electronics, 8 Refined Copper, 6 Steel Screw, 2 Glass | 10,000 MJ |
| Rare | 5 Titanium Ingot, 20 Electronics, 10 Aluminium, 8 Steel Screw, 4 Carbon Fiber | 15,000 MJ |
| Exotic | 10 Titanium Ingot, 30 Electronics, 8 Carbon Fiber, 5 Composite Paste, 15 Aluminium | 20,000 MJ |

## Installation

1. Install JimK72's Mod Manager
2. Place the `.EXMODZ` file in your Mod Manager mods folder
3. Enable the mod and launch Icarus

## Notes

- All machines are electric-powered (connect to power grid)
- Input: 1 Stone per cycle (cheapest resource, load once and forget)
- AutoSelectRecipe is enabled — auto-picks recipe when Stone is loaded
- ManualActivation — turn on once, runs continuously
- Also craftable at the Fabricator (tiered material costs)
- Workshop tab: 'Passive Miners'
- Uses the mod's own `BP_PassiveMiner` blueprint (place-anywhere processor with the drill mesh), shipped as a cooked asset inside the EXMODZ — the Mod Manager packs it on **merge**
- Does NOT override any vanilla blueprints — fully compatible with other mods

> **Known issue:** a placed miner is duplicated each time the save is reloaded. This is in the
> `BP_PassiveMiner` blueprint itself, not the mod's data — the item definition is a clean clone of
> the vanilla Electric Furnace and nothing in the data re-creates the machine. Being investigated.

## Changelog

### v7.8
- **Fix**: all 23 miners ran silently. Their mining recipes set `Audio` to a `D_CraftingAudioData` row called `Furnace`, which has never existed in that table. Now `Default`, matching vanilla's own passive extractor recipe (`Ore_Meta`). The kit-crafting recipes were already correct and are unchanged.
- **Docs**: corrected the v7.7 entry below. It claimed the deployables had been switched to the vanilla drill blueprint; they were not, and all 23 still use `BP_PassiveMiner` — which is the right choice, because the vanilla drill blueprint only snaps to deep-ore deposits and would break "place anywhere".
- **Docs**: documented the known save-reload duplication issue.

### v7.7
- Placement fixed. *(Corrected in v7.8: this entry previously claimed the 23 `D_DeployableSetup` entries had been switched to vanilla `BP_Deep_Mining_Drill_Electric`. That edit was never made — they use the mod's own `BP_PassiveMiner`, which is shipped in the EXMODZ and packed on merge.)*

### v7.6
- Attempted to fix placement by bundling BP_PassiveMiner PAK — PAK still missing from EXMODZ, placement still broken

### v7.5
- Fixed broken Fabricator recipes — Iron_Ingot/Copper_Ingot replaced with correct Refined_Metal/Refined_Copper
- Fixed Aluminium miner — was outputting ingots (Aluminium), now correctly outputs Bauxite ore with proper icon
- Added Manufacturer bench as crafting station for all miner kits

### v7.4
- Added Fabricator crafting recipes — all 23 miners craftable in-game without Workshop
- Tiered material costs: common (Steel+Electronics), uncommon (+Glass), rare (+Titanium+Carbon Fiber), exotic (+Composite Paste)

### v7.3
- Fixed collision/interaction — machines are now solid and interactable again
- DeployableSM set to bVisible=false (invisible) but keeps StaticMesh for collision hitbox
- DeployableSK renders the animated drill visual — no double mesh, working physics

### v7.2
- Fixed double mesh rendering — removed static mesh from DeployableSM so only the animated skeletal mesh renders
- BROKEN: Removing StaticMesh also removed collision — machines became ghost objects

### v7.1
- Fixed broken drill textures — swapped furnace materials to drill materials (M_DEP_DeepMiningDrill_Electric Off/On)
- Fixed sounds — swapped furnace FMOD audio to drill sounds (SFX_DEP_ELECTRIC_DRILL_ACTIVE/STOP)
- Added drill animation — skeletal mesh with Anim_DEP_DeepMiningDrill_Electric_Active
- Fixed power config — MaxMilliwattage set to 2500 (was 125, now matches vanilla Electric Furnace)

### v7.0
- Complete rewrite using BP_PassiveMiner (renamed Electric Furnace with drill mesh swap)
- No longer overrides any vanilla blueprints — unique BP at /Game/BP/.../PassiveMiners/BP_PassiveMiner
- Processor functionality via BP_ResourceNetworkProcessor inheritance (place anywhere, no ore deposit needed)
- 13 name table swaps: mesh, materials, sounds, class name, package path

### v6.0-drill
- Attempted re-parenting drill BP from BP_Drill_Base to BP_ProcessorBase
- Crashed with 'Could not find SuperStruct ActiveStateUpdated' — BP_Drill_Base functions not in BP_ProcessorBase

### v1.0–5.0
- Initial development — experimented with Electric Furnace approach, ore node spawners, and data-only configs
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
