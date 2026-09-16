Agents_Individual_Item_Kits_P.pak
----------------------------------------------------------------------
Mod Version: 5.3

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
2702 individual item kits with real game icons across 20 categorized workshop groups. Every player-usable game item available as a kit - fairly priced by complexity and rarity. Armor sorted by slot (head -> chest -> arms -> legs -> feet), 5-row grid layout, verified icons.

Ver 5.3
Get back kits you already researched - v4.0 renamed every kit's research ID, so kits
researched on v1.0 to v3.1 showed as locked and asked for Ren again. Close Icarus and
run Restore_Kit_Research.bat (in the Restore_Kit_Research folder) to restore them for
free; it backs up your profile first. Added 23 kits for items from the Sept 2026 update.
Fixed 4 kits that gave nothing when used (Sandwyrm SMG, Scout SMG, Checkered Flag,
Speeder Kit). Removed 2 kits for fish the game deleted and 2 duplicate kits that
overwrote each other. Removed two properties (Icon, Category) from every workshop entry
that the game does not read. 2,702 individual item kits across 20 workshop categories.

Ver 5.2
Fixed workshop grid clipping into top sell bar (Y offset shifted from 100 to 250). Re-sorted all 2,683 kits into 20 category groups with box-width spacing between each group for clear visual separation. Categories scroll left to right: Raw Resources, Refined Materials, Seeds, Food, Drinks & Medicine, Melee Weapons, Bows & Crossbows, Firearms, Ammunition, Explosives, Shields, Armor, Attachments, Tools, Gear, Building Pieces, Crafting Stations, Deployables, Lighting, Trophies & Decor.

Ver 5.1
Major cleanup and organization pass. Removed 23 dev/cosmetic kits (ExoticsReward, Spacesuit variants, Skin_Head variants) that couldn't spawn correctly. Removed the empty "Agents Individual Items" workshop tab. Re-sorted all 2683 kits into 20 logical categories. Armor now sorted by slot per set (head -> chest -> arms -> legs -> feet). Seeds grouped together (previously scattered). Grid changed from 4 rows to 5 rows per category. Fixed 13 broken or mismatched icon paths (Polarbear Arm/Leg Armor, Reed/Sugar Cane seed packs, 5 seed variants, Rifle_Assault, Pig_Trophy, Charcoal_From_Wood, Dropship flare).

Ver 5.0
Added 650 new individual item kits, bringing total to 2706. New content: full Alloy Armor set, ammo variants (Lithium, Uranium), arrow variants, 41 armor pieces, 45 attachments, 34 medicine & husbandry serums, 29 weapons (bows, spears), 70 tools & scanners, 49 food items, 58 refined resources, 150 decorations & vestiges, 69 Limestone building pieces, 18 workstations. Merged into existing 21 categories with matching pricing tiers. Removed 2 orphaned kits (FlagPole, Wood_Build_HalfNormal) that no longer exist in the game. Layout still 4 rows per category so new items fit within borderless 1080p bounds.

Ver 4.1
Rearranged workshop layout to 4 rows by unlimited columns per category so kits no longer go off the bottom of the screen in borderless 1080p (Workshop only scrolls horizontally). Fixed 2055 Item Kit icons that were previously showing the generic gray crate icon in D_Itemable - each kit now displays the actual in-game item icon in the Workshop grid and in inventory. Category spacing preserved (21 groups, 900-unit gap between each).

Ver 4.0
Added real item icons to all kits (2056/2056 matched). Single workshop tab with 21 spaced category groups. Rebuilt talent grid layout.

Ver 3.1
Description update.

Ver 3.0
Added 657 new kits.

## Get Back Kits You Already Researched:
  Version 4.0 renamed every kit's research ID. If you researched kits on
  v1.0 to v3.1, the game still has that research saved under the old IDs,
  so those kits show as locked and ask for Ren again. The Restore_Kit_Research
  tool renames the old IDs in your Icarus profile to the current ones, so
  those kits are researched again at no cost. It only changes kit research.

  1. Close Icarus completely.
  2. Open the Restore_Kit_Research folder that comes with this mod, or get
     both files from:
     https://github.com/AgentKush/Icarus-mods/tree/main/Agents_Individual_Item_Kits/Restore_Kit_Research
  3. Double-click Restore_Kit_Research.bat
  4. Start Icarus. The restored kits show as researched again.

  - It backs up your profile first (Profile.json.kitrestore_<date>.bak).
  - Running it again is safe. If there is nothing to restore, it changes nothing.
  - Preview without changing anything: Restore_Kit_Research.bat -DryRun
  - Dedicated server / custom save location:
    Restore_Kit_Research.bat -PlayerDataPath "<PlayerData folder>"
  - Kits retired in earlier versions (item left the game or dev-only kit)
    cannot come back. The tool lists any it finds in your profile.

## Files Modified:
  Items-D_ItemsStatic          (2702 entries)
  Traits-D_Itemable            (2702 entries)
  Items-D_ItemTemplate         (2702 entries)
  Traits-D_Consumable          (2702 entries)
  Talents-D_TalentArchetypes   (1 entry)
  Talents-D_TalentTrees        (1 entry)
  Talents-D_Talents            (2702 entries)
  MetaWorkshop-D_WorkshopItems (2702 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Agents_Individual_Item_Kits.EXMODZ
  3. Import via Mod Manager
  4. Updating from v3.1 or older? Run Restore_Kit_Research.bat (see above)

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods
