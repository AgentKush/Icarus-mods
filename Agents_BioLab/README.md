<div align="center">

# Agent's BioLab

[![Version](https://img.shields.io/badge/v2.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

All 11 legendary weapons in the Workshop - the 9 the Bio Lab sells, plus Frostbreaker and the unreleased Slugger

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Overview

Agent's BioLab brings 11 legendary weapons to the Workshop, making these powerful end-game items accessible without relying on rare mission drops. Nine are the weapons the game's Bio Lab sells. Frostbreaker and the Slugger are legendaries the game defines but never hands out.

## Features

### Weapons Available

Names are the game's own.

| Weapon | Creature | Category | Workshop Price |
|--------|----------|----------|----------------|
| Frontier Revolver | Black Wolf | Pistol | 1,000 Exotics |
| Kinetic Rifle | Scorpion | Rifle | 1,000 Exotics |
| Tactical Bow | - | Bow | 1,000 Exotics |
| Mining Armature | Rock Golem | Gauntlet and pickaxe | 1,000 Exotics |
| Biotech Maul | Ape | Sledgehammer | 1,000 Exotics |
| Heavy Flamethrower | Lava Hunter | Flamethrower | 1,000 Exotics |
| Anti-materiel Rifle | - | Sniper rifle | 1,000 Exotics |
| Javelin Launcher | Sandworm | Crossbow | 1,000 Exotics |
| Slugger | Hammerhead Slug | Launcher | 1,000 Exotics |
| Frostbreaker | Ice Mammoth | Sledgehammer and pickaxe | 1,000 Exotics |
| Timber Extraction Unit | Sandwyrm | Chainsaw | 1,000 Exotics |

### The Slugger

The game has the Slugger's icon, gun, back tank, firing logic and slime projectile, but it never added the item row that ties them together. Without that row the Workshop showed "ICON MISSING" and the weapon did nothing. This mod adds the row using only the game's own Slugger parts:
- It fires slime globs (250 damage) and runs on water from its 30 L tank, which takes water the way the game's Fire Extinguisher does. You can't drink from it.
- Each shot uses 1 L of water, so a full tank is 30 shots. The game never set this cost; 1 L is this mod's choice.
- It can't be upgraded at the Bio Lab. The game has the Slugger's upgrades but no upgrade page for it.

## Technical Specifications

| Metric | Value |
|--------|-------|
| Total Modifications | 25 |
| Item Rows Added | 1 (Slugger) |
| Workshop Items Added | 11 |
| Talent Entries | 11 |
| Talent Trees | 1 |

### Files Modified
- `Items-D_ItemsStatic.json`
- `MetaWorkshop-D_WorkshopItems.json`
- `Talents-D_TalentArchetypes.json`
- `Talents-D_Talents.json`
- `Talents-D_TalentTrees.json`

## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus
5. Access weapons via Workshop → BioLab category

## Compatibility

| Mod | Status |
|-----|--------|
| FastProcessing (all variants) | ✅ Compatible |
| Workshop Recyclers | ✅ Compatible |
| Hidden Building Pieces | ✅ Compatible |
| Other D_WorkshopItems mods | ⚠️ May conflict |

## Version History

| Version | Changes |
|---------|---------|
| 2.1 | The Slugger works: adds the item row the game left out, so it has its icon and fires slime from a 30 L water tank (1 L a shot). Weapon names updated to the game's current ones (Biotech Maul, Frostbreaker, Timber Extraction Unit, Slugger). |
| 2.0.1 | New icon and banner, drawn from the mod's live data. No gameplay change. |
| 2.0 | Fixed Flamethrower case mismatch (`FlameThrower` → `Flamethrower`), added Sandwyrm Chainsaw |
| 1.9 | Fixed Ape Club item reference (`LegendaryWeapon_ApeClub`) - icon and workshop craft now working |
| 1.8 | Fixed item references for Ape Club and Heavy Flamethrower (Week 214 compatibility) |
| 1.7 | Previous stable release |
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
