<div align="center">

# Night Vision Goggles

[![Version](https://img.shields.io/badge/v2.2-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Unlocks the hidden Night Vision system built into Icarus. Craft Night Vision Goggles at Fabricator, Manufacturer, or Machining Bench. Toggle with secondary action

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Features

- **Night Vision Goggles** - craftable item that toggles a post-process night vision effect
- Uses the game's built-in night vision system (PostProcess component with green tint, brightness amplification, and film grain)
- Toggled on/off with secondary action while equipped
- **No decay** - goggles won't disappear over time
- **Durable** - 10,000 durability, won't break easily
- **Lightweight** - reduced weight from 5.0 to 1.0
- Craftable at **Fabricator**, **Manufacturer**, or **Machining Bench**

## Crafting Recipe

| Material | Quantity |
|----------|----------|
| Electronics | 4 |
| Glass | 2 |
| Epoxy | 2 |

No blueprint unlock required - available immediately at the Fabricator.

## Installation

1. Download `NightVisionGoggles.EXMODZ`
2. Import into **Icarus Mod Manager** (JimK72's IMM)
3. Enable and merge mods as usual

## Changelog

### v2.2
- **Fix**: the goggles crafted in silence. The recipe set `Audio` to a `D_CraftingAudioData` row named `Fabricator`, but that table has no such row — `Fabricator` is a **`D_RecipeSets`** name, and the two tables use different keys. Now set to `MachiningBench`, which is what the vanilla **Binoculars** recipe uses (same three benches, same Glass + Epoxy inputs).

### v2.1
- Crash fix: moved 1 recipe output from D_ItemsStatic to D_ItemTemplate (prevents crash when opening crafting stations).

### v2.0
- Added no-decay (Decay_NoDecay) so goggles persist indefinitely
- Added durability (Destroyed_Tool, 10,000 HP)
- Reduced weight from 5.0 to 1.0
- Added Machining Bench as crafting station
- Updated description

### v1.1
- Fixed mod format: converted from legacy structure to current name/author/Rows format

### v1.0
- Initial release
- Unlocked hidden Night Vision item from game files
- Added crafting recipe at Fabricator/Manufacturer
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
