# No Food Spoilage

**Version:** 1.0  
**Author:** AgentKush  
**Compatible with:** JimK72's Icarus Mod Manager (EXMODZ format)

## Description

Prevents all food items from spoiling in your inventory! No more worrying about meat going bad or vegetables rotting. Your food will last forever.

## What This Mod Does

- Sets `SpoilTime` to 0 for all food decay types
- Food items will **not** turn into spoiled versions
- Items still decay/disappear when dropped in the world (DecayTime unchanged)
- Only affects inventory spoilage, not world decay

## Foods Affected

| Food Type | Status |
|-----------|--------|
| Raw Meat & Chicken | ✅ No Spoil |
| Cooked Meat | ✅ No Spoil |
| Dried & Smoked Meat | ✅ No Spoil |
| Dried Fish | ✅ No Spoil |
| Fruits & Vegetables | ✅ No Spoil |
| Dried Vegetables | ✅ No Spoil |
| Coconuts (Young, Mid, Mature) | ✅ No Spoil |
| Ice | ✅ No Spoil |
| Milk & Cream | ✅ No Spoil |
| Bait | ✅ No Spoil |
| Frozen Food | ✅ No Spoil |
| Generic Food Items | ✅ No Spoil |

## Installation

1. Download `No_Food_Spoilage.EXMOD` (or `.EXMODZ` if zipped)
2. Place in your Mod Manager's `Extracted_Mods` folder
3. Use JimK72's Mod Manager to merge and install
4. Launch Icarus - food no longer spoils!

## Technical Details

This mod modifies `D_Decayable` traits. Setting `SpoilTime: 0` prevents the spoilage timer from ever completing, while preserving `DecayTime` so items still despawn naturally when dropped in the world.

## Changelog

- **v1.0** - Initial release

## License

Free to use and modify. Credit appreciated!
