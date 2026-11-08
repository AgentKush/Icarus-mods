<div align="center">

# No Food Spoilage

[![Version](https://img.shields.io/badge/v2.3.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Prevents all food spoilage. 33 decayable entries + 122 composter recipes. Items decay/despawn normally but never convert to spoiled versions

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Features

- **33 decay types modified** — All decay types have SpoilTime set to 0 and SpoiledItem set to None
- **122 composter recipes** — Manually compost raw foods via the Composter station
  - 15 raw meats (Raw_Meat, Raw_Chicken, Raw_Fish, Raw_Bacon, all meat variants)
  - 76 whole fish (Fish_01–Fish_19 with Var2/Var3/Var4 variants)
  - 3 fish products (Fish_Chunks, Freshwater/Saltwater Fish Fillet)
  - 7 dairy/animal products (Cream, Egg, Milk, Butter, Cheese, Honey, Honeycomb)
  - 32 vegetables/fruits (Squash, Corn, Pumpkin, Carrot, Potato, Berries, Banana, Avocado, Tomato, Strawberry, and more)
  - 1 other (Bait)
- Volatile Substance decay also disabled

## Changelog

### v2.3.1 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v2.3
- SAFETY FIX - the mod gave the game's never-decay profile a decay timer, so the 19 things that are meant to last forever (all four saddle carts, the speeder saddle, the landing pads, the advanced exotic delivery interface, animal silage and ten mission stasis bags) could decay. They never decay again. Restored leather curing (Curing Leather turns into Advanced Leather again - that is crafting, not spoilage). Removed 12 composter recipes for items that do not exist and fixed 5 that pointed at renamed foods (Fatty T-Bone, Giant Steak, Berry, Bean, Prickly Pear). Food never spoils; the composter can still turn food into spoiled food for fertilizer.

### v2.2 (2026-06-27)
- Restored coconut ripening (young -> mid -> mature) that the no-spoil change had broken; mature coconuts no longer rot. Fixes #10.
- **v2.1** - Crash fix: Fixed 134 recipe outputs from D_ItemsStatic to D_ItemTemplate (prevents crash when opening crafting stations).
### v2.0 (2026-03-26)
- **Fixed composter bug** — Composter recipes were missing from the EXMOD, causing items to sit in the composter without processing ([#2](https://github.com/AgentKush/Icarus-mods/issues/2))
- Added 134 composter recipes to D_ProcessorRecipes for manual composting
- Raw meats and fish → Spoiled_Meat, vegetables/fruits → Spoiled_Plants
- Added dairy/animal products (Cream, Egg, Milk, Butter, Cheese, Honey, Honeycomb)
- Added missing fruits/vegetables (Avocado, Bramble, Kiwi_Fruit, Rhubarb, Strawberry, Sugar_Cane, Tomato, Truffle, Yeast)

### v1.9
- Added 11 new decay entries from Dangerous Horizons update

### v1.8 (2026-03-08)
- Corrected Spoil_ composter recipes: now only covers raw meat and raw fish items
- Removed incorrect composter entries for tonics, bandages, cooked foods, etc.

### v1.7 (2026-03-08)
- Added 238 missing Spoil_ composter recipes for DLC foods/tonics/consumables

### v1.6 (2026-03-08)
- Added Decay_General and Decay_MetaItem for full coverage

### v1.5
- Verified all 20 decay types are current with latest game data

### v1.4
- Previous release with 85 composter recipes

### v1.3
- Added composter recipes for fish variants

### v1.0
- Initial release
---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
