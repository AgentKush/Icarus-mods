<div align="center">

# Agents Individual Item Kits

[![Version](https://img.shields.io/badge/v5.3-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

2,702 individual item kits with real game icons across 20 categorized workshop tabs. Fair pricing based on complexity (5-300 credits).

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Overview

A comprehensive Workshop expansion featuring 2,702 individual item kits, each with its real in-game icon and organized into 20 dedicated workshop tabs. Every kit contains a single item, enabling precise inventory management and eliminating the need to craft items from scratch.

## Features

- **2,702 Individual Items** - Every craftable item and raw material available separately
- **Real Game Icons** - Each kit displays its actual in-game item icon for easy identification
- **20 Workshop Tabs** - Items sorted into logical categories (Armor, Weapons, Building, Food, etc.)
- **Armor Sorted by Slot** - Head → Chest → Arms → Legs → Feet per set for clean mix-and-match
- **5-Row Grid** - Tighter layout that fits more items on-screen at 1080p
- **Dynamic Pricing** - Fair costs based on item complexity and rarity (5-300 credits)

## Get Back Kits You Already Researched

Version 4.0 renamed every kit's research ID. If you researched kits on v1.0 to v3.1, the game still has that research saved under the old IDs, so those kits show as locked and ask for Ren again.

The **Restore_Kit_Research** tool renames the old IDs in your Icarus profile to the current ones, so those kits are researched again at no cost. It only changes kit research entries.

1. Close Icarus completely.
2. Open the `Restore_Kit_Research` folder that comes with this mod, or [download it here](https://github.com/AgentKush/Icarus-mods/tree/main/Agents_Individual_Item_Kits/Restore_Kit_Research) (get both files).
3. Double-click `Restore_Kit_Research.bat`.
4. Start Icarus. The restored kits show as researched again.

- It backs up your profile first (`Profile.json.kitrestore_<date>.bak`, next to the original).
- Running it again is safe. If there is nothing to restore, it changes nothing.
- To see what it would change without changing anything, run `Restore_Kit_Research.bat -DryRun`.
- Dedicated server or a custom save location: `Restore_Kit_Research.bat -PlayerDataPath "<PlayerData folder>"`.
- Kits that were retired in earlier versions (because the item left the game or the kit was dev-only) cannot come back. The tool lists any it finds in your profile.

## Workshop Categories

| Category | Items | Category | Items |
|----------|-------|----------|-------|
| Raw Resources | 123 | Shields | 10 |
| Refined Materials | 70 | Armor | 201 |
| Seeds | 51 | Attachments | 193 |
| Food | 318 | Tools | 106 |
| Drinks & Medicine | 116 | Gear | 28 |
| Melee Weapons | 100 | Building Pieces | 279 |
| Bows & Crossbows | 25 | Crafting Stations | 133 |
| Firearms | 27 | Deployables | 317 |
| Ammunition | 111 | Lighting | 53 |
| Explosives | 25 | Trophies & Decor | 416 |

## Pricing Structure

| Tier | Credit Range | Item Examples |
|------|--------------|---------------|
| Basic | 5-10 | Seeds, raw materials, basic ores |
| Standard | 20-35 | Food, building pieces, ammo, equipment |
| Advanced | 50-75 | Backpacks, legendary weapons, workshop animals, envirosuits |
| Premium | 100-300 | Rare materials, high-tier gear, specialized items |

## Technical Specifications

| Metric | Value |
|--------|-------|
| Individual Items | 2,702 |
| Workshop Category Groups | 20 |
| Icon Coverage | 100% (all icons verified against game data) |
| Price Range | 5-300 credits |
| Grid Layout | 5 rows × unlimited columns per category |

### Files Modified
- `Items-D_ItemsStatic.json` (2,702 entries)
- `Traits-D_Itemable.json` (2,702 entries)
- `Items-D_ItemTemplate.json` (2,702 entries)
- `Traits-D_Consumable.json` (2,702 entries)
- `Talents-D_TalentArchetypes.json` (1 entry)
- `Talents-D_TalentTrees.json` (1 entry)
- `Talents-D_Talents.json` (2,702 entries)
- `MetaWorkshop-D_WorkshopItems.json` (2,702 entries)

## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus
5. Browse the 20 Workshop tabs to find individual items
6. Updating from v3.1 or older? Run the restore tool above to get your researched kits back

## Compatibility

| Mod | Status |
|-----|--------|
| All AgentKush mods | Compatible |
| Other Workshop mods | Test for conflicts |

## Version History

| Version | Changes |
|---------|---------|
| 5.3 | Get back kits you already researched - v4.0 renamed every kit's research ID, so kits researched on v1.0 to v3.1 showed as locked and asked for Ren again. Close Icarus and run Restore_Kit_Research.bat (in the Restore_Kit_Research folder) to restore them for free; it backs up your profile first. Added 23 kits for items from the Sept 2026 update. Fixed 4 kits that gave nothing when used (Sandwyrm SMG, Scout SMG, Checkered Flag, Speeder Kit). Removed 2 kits for fish the game deleted and 2 duplicate kits that overwrote each other. Removed two properties (Icon, Category) from every workshop entry that the game does not read. 2,702 individual item kits across 20 workshop categories. |
| 5.2 | Fixed workshop grid clipping — items no longer overlap the top sell bar (Y offset shifted from 100 to 250). Re-sorted all 2,683 kits into 20 category groups with box-width spacing between each group for clear visual separation. Categories scroll left to right: Raw Resources → Refined Materials → Seeds → Food → Drinks & Medicine → Melee Weapons → Bows & Crossbows → Firearms → Ammunition → Explosives → Shields → Armor → Attachments → Tools → Gear → Building Pieces → Crafting Stations → Deployables → Lighting → Trophies & Decor. |
| 5.1 | Major cleanup and organization pass. Removed 23 dev/cosmetic kits (ExoticsReward, Spacesuit variants, Skin_Head variants) that couldn't spawn correctly. Removed the empty "Agents Individual Items" workshop tab. Re-sorted all 2,683 kits into 20 logical categories. Armor now sorted by slot per set (head → chest → arms → legs → feet) for clean mix-and-match. Seeds grouped together (previously scattered). Grid changed from 4 rows to 5 rows per category. Fixed 13 broken or mismatched icon paths (Polarbear Arm/Leg Armor, Reed/Sugar Cane seed packs, 5 seed variants, Rifle_Assault, Pig_Trophy, Charcoal_From_Wood, Dropship flare). |
| 5.0 | Added 650 new individual item kits, bringing total to 2,706. New content: full Alloy Armor set, ammo variants (Lithium, Uranium), arrow variants, 41 armor pieces, 45 attachments, 34 medicine & husbandry serums, 29 weapons (bows, spears), 70 tools & scanners, 49 food items, 58 refined resources, 150 decorations & vestiges, 69 Limestone building pieces, 18 workstations. Merged into existing 21 categories with matching pricing tiers. Removed 2 orphaned kits (FlagPole, Wood_Build_HalfNormal) that no longer exist in the game. Layout remains 4 rows per category so all new items fit within borderless 1080p bounds. |
| 4.1 | Rearranged the workshop grid to 4 rows × unlimited columns per category so kits no longer go off the bottom of the screen in borderless 1080p (the Workshop only scrolls horizontally). Fixed 2055 Item Kit icons that were showing the generic gray crate in inventory - each kit now uses its actual in-game item icon in D_Itemable so the Workshop grid and inventory both show the real icons. Category spacing preserved (21 groups, 900-unit gap between each). |
| 4.0 | Added real game icons to all 2,056 kits. Organized into 21 categorized workshop tabs (Armor, Weapons, Building, Food, Tools, etc.). Rebuilt talent grid layouts. Zero uncategorized items. |
| 3.1 | Description update |
| 3.0 | Added 657 new kits (fish, flags, props, seeds, food, animals, building pieces, envirosuits, legendary weapons, ammo, backpacks, and more). Fixed 4 broken item references. Total: 2,056 kits. |
| 2.1 | Week 213+ compatibility update |
| 2.0 | Complete reorganization into 73 categories, revised pricing system |
| 1.0 | Initial release |

---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
