<div align="center">

# Solar Panel Expansion

[![Version](https://img.shields.io/badge/v1.2-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Adds all solar panels and Solar Backpack to a dedicated Solar Energy Workshop tab. Includes Solar Panel Kit, Flat Solar Panel Kit, and Solar Backpack Kit with fair pricing.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Features

- **Dedicated "Solar Energy" Workshop Tab** with custom solar panel icon
- **3 Workshop Items:**
  - Solar Panel Kit (150 Credits) - Unpacks to a Solar Panel
  - Flat Solar Panel Kit (150 Credits) - Unpacks to a Flat Solar Panel
  - Solar Backpack Kit (250 Credits + 200 Exotic Uranium) - Unpacks to a Solar Backpack

## Pricing

| Item | Research Cost | Craft Cost |
|------|--------------|------------|
| Solar Panel Kit | 150 Credits | 75 Credits |
| Flat Solar Panel Kit | 150 Credits | 75 Credits |
| Solar Backpack Kit | 250 Credits + 200 Uranium | 100 Credits + 150 Uranium |

## Compatibility

- Works alongside all other mods
- Does not modify existing game recipes or items
- Adds new Workshop tab and kit items only

## Installation

Import `Solar_Panel_Expansion.EXMODZ` via Icarus Mod Manager.

## Changelog

### v1.2
- **Major fix — the kits gave you nothing.** All four kits described their contents with `ConsumeType` and `Recipes`, but neither is a property of `D_Consumable` (the struct is only `Stats`, `Modifier`, `DescriptionText`, `Byproducts`). The game discarded both at load, so using a kit played the consume animation, destroyed the kit, and handed back no panel — with the Ren, and on the backpack the Exotic Uranium, already spent and unrefundable. All four rewritten to the vanilla `Byproducts` form, matching `Workshop_Beehive_Starter_Kit`. Each kit now yields its real item: Solar Panel, Flat Solar Panel, Solar Backpack, Bunker Solar Panel.
- **Fix**: the Bunker Solar Panel Kit used the plain Solar Panel icon, making the two indistinguishable in the shop and inventory. Now uses the Bunker panel's own icon.

### v1.1 (2026-06-27)
- Added the Bunker Solar Panel as a 4th workshop kit (the game variant the mod was missing).
### v1.0 (2026-03-28)
- Initial release
- Added Solar Energy workshop tab
- Added 3 solar item kits with fair pricing
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
