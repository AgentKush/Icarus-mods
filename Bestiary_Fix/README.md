<div align="center">

# Bestiary Fix

[![Version](https://img.shields.io/badge/v1.1.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Fixes missing experience events that prevent Bestiary point tracking for several creatures.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## The Problem

Several creatures are missing experience events in the game data, which prevents the Bestiary from tracking kills and other actions. Additionally, the Sulfuric Spider's SkinningXPEvent incorrectly references a Kill event instead of a Skin event.

**Important caveat:** Sulfur Worm, Sulfur Vesper, Cave Worm, and Vesper all explode on death and leave no corpse. This means skinning-related Bestiary actions (Skin, SkinWithTrophyKnife, SkinOnBench) are impossible by design. The Bestiary point tracking for these creatures may also be partially broken at the engine level (C++ blueprint code) which data table mods cannot fix. This mod addresses the data table issues only.

## What This Mod Fixes

### Data Table Fixes

| Table | Entry | Fix |
|-------|-------|-----|
| D_ExperienceEvents | Kill_SulfurWorm | **Added** - was completely missing, preventing any kill tracking |
| D_AICreatureType | GeothermalSpider | **Fixed** SkinningXPEvent from Kill_Geothermal_Spider to Skin_Geothermal_Spider |

### Known Limitations

These issues exist at the engine/blueprint level and cannot be fixed with data table mods:

| Issue | Reason |
|-------|--------|
| Exploding creatures can't be skinned | Death blueprint destroys corpse - no skinning possible |
| Bestiary may not register kills for some DH creatures | Engine-level creature-to-bestiary mapping may be broken |
| Trophy crafting may not award Bestiary points | CraftTrophy tracking is hardcoded in C++ |

### How Bestiary Points Work

| Action | Points | Available for exploding creatures? |
|--------|--------|------------------------------------|
| Kill | 3 | Requires Kill event to exist (this mod adds Kill_SulfurWorm) |
| Skin | 2 | No - corpse destroyed |
| Skin with Trophy Knife | 4 | No - corpse destroyed |
| Skin on Bench | 4 | No - corpse destroyed |
| Craft Trophy | 4 | Maybe - depends on engine tracking |
| Scanned | 6 | Yes |
| KilledBy | 4 | Yes |

## Installation

1. Install [JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)
2. Download `Bestiary_Fix.EXMODZ`
3. Import via Mod Manager
4. Restart the game

## Changelog

### v1.1.1 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v1.1
- Removed skinning events for exploding creatures (worms/bats can't be skinned)
- Fixed GeothermalSpider SkinningXPEvent pointing to Kill event instead of Skin event
- Stripped down to only verifiable data table fixes

### v1.0
- Initial release
- Added Kill_SulfurWorm experience event
- Added skinning events (removed in v1.1 - creatures explode on death)

---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
