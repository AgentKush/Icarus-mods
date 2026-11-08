<div align="center">

# Dev Tools Kit

[![Version](https://img.shields.io/badge/v1.1.6-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Unlocks 11 hidden developer tools including Thor's Hammer (fly mode), Transform Tool, Destroy Tool, Inspection Tool, Fireball, Pyromancy Flame, Debug Target, and more

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Overview

Dev Tools Kit unlocks 11 hidden developer tools from the game files, making them available in the Workshop for free. These are actual tools used by RocketWerkz developers during game development - now accessible to players!

## Features

### Tools Available

| Tool | Description | Use Case |
|------|-------------|----------|
| **Thor's Hammer** | "Fly like a God, smell like a Dev" | Flight mode - hold to fly around the map |
| **Fireball** | Throwable fire projectile | Combat / fun |
| **Pyromancy Flame** | Dark Souls-inspired fire spell medium | Combat / fun |
| **Inspection Tool** | Get object info on left click, persist on right click | Debugging / building |
| **Transform Tool** | Select actors and adjust location/rotation/scale | Advanced building |
| **Destroy Tool** | Left click to destroy any actor | Building removal |
| **Unobtainable Tool** | Prevent deployables from being picked up | Base security |
| **Bug Tool** | Creates Jira bug reports (dev internal) | Curiosity item |
| **Test Seed** | Mysterious developer test seed | Unknown |
| **Deployable Dropship** | Place your own dropship anywhere | Base decoration |
| **Debug Target** | Deployable dummy target for weapon / damage testing | Testing weapons & effects |

### Workshop Access

All items appear in a new **"Developer Tools"** category in the Workshop.

| Feature | Value |
|---------|-------|
| Research Cost | **FREE** (0 credits) |
| Craft Cost | **FREE** (0 credits) |
| Pre-Unlocked | Yes |

## Technical Specifications

| Metric | Value |
|--------|-------|
| Total Modifications | 47 |
| Workshop Items Added | 11 |
| Talent Entries | 11 |
| Talent Trees | 1 |
| D_Itemable Entries | 6 |
| D_ItemsStatic Entries | 11 |
| D_ItemTemplate Entries | 6 |

### Files Modified
- `Talents-D_TalentArchetypes.json`
- `Talents-D_TalentTrees.json`
- `Talents-D_Talents.json`
- `MetaWorkshop-D_WorkshopItems.json`
- `Traits-D_Itemable.json`
- `Items-D_ItemsStatic.json`
- `Items-D_ItemTemplate.json`

## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus
5. Access tools via Workshop → Developer Tools category

## Important Notes

- These are **internal developer tools** - some may have limited or unexpected functionality
- **Thor's Hammer** and **Transform Tool** are the most useful for players
- **Bug Tool** connects to RocketWerkz's internal Jira - won't work for players
- **Deployable Dropship** may have placement restrictions
- Some tools' in-hand meshes have been substituted with visible placeholders so you can see the tool in your hand (Inspection Tool uses the Deep Ore Scanner mesh, Bug Tool uses the Beacon Tool mesh, Transform Tool uses the Building Hammer mesh)
- **Debug Target** is a deployable dummy used by the devs to test weapon damage and effects

## Compatibility

| Mod | Status |
|-----|--------|
| FastProcessing (all variants) | Compatible |
| Workshop Recyclers | Compatible |
| Hidden Building Pieces | Compatible |
| Individual Item Kits | Compatible |
| Other D_WorkshopItems mods | May conflict |

## Version History

| Version | Changes |
|---------|---------|
| 1.1.6 | New icon and banner, drawn from the mod's live data. No gameplay change. |
| 1.1.5 | **June 2026 update fix.** The update’s mesh consolidation broke Debug Target and Test Seed. Repointed Debug Target to the pivot-cube mesh and Test Seed to the seed mesh. |
| 1.1.3 | Audited against live game data. Substituted visible meshes for 3 tools that previously used the invisible placeholder mesh (Inspection Tool → Scanner DeepOre, Bug Tool → Beacon Tool, Transform Tool → Building Hammer). Added Debug Target as the 11th dev tool (dummy target for weapon testing, uses its own visible mesh). Fixed Thor's Hammer Focusable reference (Focusable_2H no longer exists in game data → now uses Focusable_Sledge). Rearranged the Developer Tools workshop tree to a 4-row × 3-column grid so it fits within the Workshop's vertical bounds (scrolls horizontally only). |
| 1.1.2 | Updated 3 item icons to match current game data: Unobtainable Tool (→ CrateEquipment icon), Test Seed (→ Red Exotic Seed icon), Deployable Dropship (→ Icarus logo icon). |
| 1.1.1 | Updated 3 item icons to match current game data: Unobtainable Tool (→ CrateEquipment icon), Test Seed (→ Red Exotic Seed icon), Deployable Dropship (→ Icarus logo icon). |
| 1.1.0 | Fixed: Added Item.Meta tags to existing game dev items (Fireball, Inspection Tool, Bug Tool, Pyromancy Flame, Transform Tool) - now all 10 items appear in Workshop |
| 1.0.0 | Initial release - 10 dev tools unlocked |
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
