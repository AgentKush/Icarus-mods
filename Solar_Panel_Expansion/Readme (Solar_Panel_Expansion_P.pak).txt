Solar_Panel_Expansion_P.pak
----------------------------------------------------------------------
Mod Version: 1.2

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
Adds all solar panels and the solar backpack to a dedicated Workshop tab with fair pricing. Includes Solar Panel, Flat Solar Panel, Lithium variants, and Solar Backpack.


Ver 1.2
MAJOR FIX - all 4 kits granted nothing when used. They described their payload with
"ConsumeType" and "Recipes", which are not properties of D_Consumable (the struct is
only Stats, Modifier, DescriptionText, Byproducts), so the game discarded them at load.
Using a kit consumed it and produced no panel, with the Ren - and on the backpack the
Exotic Uranium - already spent. Rewritten to the vanilla Byproducts form, so each kit
now yields its real item. Also fixed the Bunker Solar Panel Kit showing the plain Solar
Panel icon.

Ver 1.1
Added the Bunker Solar Panel as a 4th workshop kit (the game variant the mod was missing).

Ver 1.0
Initial release. Added Solar Energy workshop tab. Added 3 solar item kits with fair pricing.

## Files Modified:
  Talents-D_TalentArchetypes   (1 entries)
  Talents-D_TalentTrees        (1 entries)
  Items-D_ItemsStatic          (3 entries)
  Traits-D_Itemable            (3 entries)
  Traits-D_Consumable          (3 entries)
  Items-D_ItemTemplate         (3 entries)
  MetaWorkshop-D_WorkshopItems (3 entries)
  Talents-D_Talents            (3 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Solar_Panel_Expansion.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods