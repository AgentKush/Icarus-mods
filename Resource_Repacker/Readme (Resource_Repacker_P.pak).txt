Resource_Repacker_P.pak
----------------------------------------------------------------------
Mod Version: 1.4

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
Adds 21 crafting recipes that repack raw resources back into UDA resource kits. Available at every player crafting bench plus handcrafting (player inventory). Recipes mirror the kit's vanilla byproduct (e.g. 100 Titanium_Ore -> 1 Titanium kit), so the mod is neutral - purely logistics, not duplication.

Ver 1.4
Fixed the crafting sound on all 21 recipes. They pointed Audio at a D_CraftingAudioData
row named "Fabricator", which has never existed in that table - "Fabricator" is a
D_RecipeSets name, and the two tables use different keys. With the reference dangling
the game played no craft-completed sound, which reads like a failed craft even though
the kit was produced. Now set to "Default", so each bench plays its own crafting sound.

KNOWN LIMITATION (v1.0 - v1.4): the game's orbital sender rejects crafted kits and routes them to a surplus overflow bag. Workshop-purchased kits work; crafted ones may not, due to a game-side check on item origin we can't override from data tables. Treat this mod as INVENTORY CONSOLIDATION + TEAMMATE SHARING for now. A Blueprint-side workaround is being investigated.

BASIC RESOURCES
  - Wood Kit       250 Wood
  - Stone Kit      250 Stone
  - Dirt Kit       50 Dirt
  - Limestone Kit  100 Limestone
  - Sulfur Kit     100 Sulfur
  - Oxite Kit      100 Oxite
  - Silica Kit     100 Silica
  - Clay Kit       100 Clay

METAL ORES
  - Iron Kit       100 Iron Ore (Metal_Ore)
  - Copper Kit     100 Copper Ore
  - Aluminium Kit  100 Bauxite
  - Gold Kit       100 Gold Ore
  - Platinum Kit   100 Platinum Ore
  - Titanium Kit   100 Titanium Ore
  - Lithium Kit    100 Lithium Ore

ADVANCED / EXOTIC
  - Scoria Kit             100 Scoria
  - Obsidian Kit           100 Obsidian
  - Synthetic Enzymes Kit  100 Synthetic Enzymes

DLC (Dangerous Horizons)
  - Ruby Kit         50 Ruby Ore
  - Uranium Rod Kit  10 Uranium Rod
  - Ren Kit          100 Ren

DLC kits are feature-gated to Dangerous Horizons - on non-DLC installs the recipes do not register at all, so there are no broken-icon recipes. The other 18 work for all players. (v1.3 removed the v1.2 tooltip override that was breaking the DLC kit display.)

## Available At
Every crafting bench AND handcrafting (player inventory):
  Character (handcrafting), Crafting_Bench, Anvil_Bench (T1/T3/T4), Armor_Bench (T1/Advanced/Electric), Carpentry_Bench (T1/T4), Masonry_Bench (T1/T3/T4), Machining_Bench, Fabricator, Manufacturer, Alteration_Bench (T1/Advanced), Chemistry_Bench, Glassworking_Bench, Herbalism_Bench, Medicine_Bench, Animal_Bench, Butchery_Bench (T1/Advanced), Kitchen_Bench (T1/Advanced), Trophy_Bench, Rustic_Decorations_Bench, Fishing_Bench_Recipes.

Ver 1.3
Fix: removed the D_Itemable tooltip override that was breaking the DLC kit icons and display names ("Recipe Name" with ICON MISSING). EXMOD merge replaces full rows rather than patching fields, so partial overrides wipe vanilla data. DLC requirement is now in this readme only. Also flagged the orbital-sender limitation explicitly.

Ver 1.2
Feature-gated DLC recipes (Ruby/Uranium Rod/Ren) using Metadata.RequiredFeatureLevel: DangerousHorizons - they no longer register on non-DLC installs. Added DLC requirement note to each DLC kit's tooltip (REMOVED in v1.3 - was breaking display).

Ver 1.1
Added 3 DLC kit recipes (Ruby, Uranium Rod, Ren) - require Dangerous Horizons. Exposed every recipe at all player crafting benches plus handcrafting (Character).

Ver 1.0
Initial release. 18 repack recipes covering Basic, Metal, and Exotic resource kits. Neutral 1:1 input/yield ratios.

## Files Modified:
  Crafting-D_ProcessorRecipes  (21 entries - repack recipes)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Resource_Repacker.EXMODZ
  3. Import via Mod Manager

## Notes:
  - Recipe input quantity matches the VANILLA kit yield. Stack-size mods do not change this.
  - Recipe row names match the kit name 1:1. Safe - no vanilla recipe row collision.

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods
