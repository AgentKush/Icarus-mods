<div align="center">

# UDA Terminal Laptop

[![Version](https://img.shields.io/badge/v2.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD%20%2B%20PAK-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Reskins the **Orbital Exchange Interface** into a **laptop**, and lets you place it **indoors and on benches, tables, and shelves**. Same exchange — new look, anywhere you want it.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## What it does

Icarus's **Orbital Exchange Interface** (the deployable that opens the orbital exchange) ships as a bulky wooden radio that only stands on the ground. This mod:

- **Reskins it to the ICA hab laptop** (`SM_ORB_PRP_Laptop_01`) — a sleek terminal instead of the wooden board.
- **Lets you place it indoors and on benches, tables, and shelves** — surface snapping with free rotation.
- **Leaves the exchange function 100% vanilla** — it's the game's own interface, just wearing a laptop.

No deer trophy, no new item. It's crafted as **UDA Terminal Laptop** from a **free recipe** (no tech unlock) using the same resources as the original build.

## How it works

Two parts, both shipped together in the EXMODZ:

1. **The patched Blueprint** (`BP_Exotic_Delivery_Interface`) — shipped as a loose cooked asset (`.uasset`/`.uexp`) under `UDA_Terminal_Laptop/BP/Objects/.../`, the same way the Mod Manager packs every mesh mod. It repoints the deployable's static mesh from the wooden radio (`SM_DEP_ExoticDeliveryRadio_T2`) to the laptop (`SM_ORB_PRP_Laptop_01`); edited with UAssetAPI, only that one mesh import changes. The Mod Manager packs it into the merged pak on merge.
2. **The EXMOD** — overrides the `Exotic_Delivery_Interface` DeployableSetup (laptop placement ghost + surface-friendly placement: `MaxSurfaceSnapAngle: 180`, `SupportsCustomRotation`, restacking), gives it a **free recipe** (no tech `Requirement`), and renames it to **UDA Terminal Laptop** with a laptop icon.

## Crafting

Crafted **for free** (no tech unlock) at the **Crafting Bench, Machining Bench, Fabricator, or Manufacturer**:

| Material | Qty |
|----------|-----|
| Steel Ingot | 5 |
| Electronics | 5 |
| Glass | 3 |
| Epoxy | 2 |

Look for **UDA Terminal Laptop** in the bench's deployables list.

## Installation

1. Download `UDA_Terminal_Laptop.EXMODZ`
2. Import into **Icarus Mod Manager** (JimK72's IMM).
3. Enable, **merge**, and launch.

> The laptop mesh ships as a loose cooked asset inside the EXMODZ (under `UDA_Terminal_Laptop/BP/...`). The Mod Manager packs it into the merged pak when you **merge** — so a merge is required after import, not just enabling.

## Tips

- Place it on a desk, bench, or shelf for a proper indoor command-centre look.
- It's still the Orbital Exchange under the hood — it opens the same exchange interface, just in laptop form.
- **Requesting a drop pod needs open sky above it** (the pod descends from orbit — same as the vanilla exchange). The laptop places and opens anywhere, but to actually *Request* goods, give it clearance overhead: outside, on a balcony, or under an open roof section.

## Changelog

### v2.1
- **Now craftable for free** — recipe with no tech `Requirement` at the Crafting Bench / Machining Bench / Fabricator / Manufacturer, using Steel Ingot 5, Electronics 5, Glass 3, Epoxy 2 (the original build's resources).
- **Renamed in-game to "UDA Terminal Laptop"** with a laptop inventory icon, so it's easy to find at the bench.

### v2.0
- **Complete rebuild.** Reskins the vanilla **Orbital Exchange Interface** (`Exotic_Delivery_Interface`) into a laptop, instead of building a from-scratch deployable.
- **PAK now bundled in the EXMODZ.** The v1.x packages never included a pak, so importing them only installed data and never changed the model.
- Added indoor / bench / table placement (snap angle 180, custom rotation, restacking) and a laptop placement ghost.
- Removed all `BP_Deer_Trophy` references and the old custom item + recipe.

### v1.x (deprecated)
- Earlier attempts built a new craftable laptop from scratch using a generic deployable blueprint placed in the wrong setup slot, so it never deployed (no ghost, no placement, no interaction), and no pak was shipped. Superseded by v2.0.

---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
