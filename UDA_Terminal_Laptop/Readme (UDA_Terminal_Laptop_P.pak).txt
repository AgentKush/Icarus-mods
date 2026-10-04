UDA Terminal Laptop  -  v2.2
============================

Mod Version: 2.2

Reskins the vanilla Orbital Exchange Interface into a laptop, makes it craftable
for FREE (no tech unlock), and lets you place it indoors and on benches / tables
/ shelves.

WHAT'S IN THIS PACKAGE
----------------------
1. UDA_Terminal_Laptop.EXMOD   (data: free recipe, rename, placement, laptop ghost)
2. UDA_Terminal_Laptop_P.pak   (mesh: swaps the deployed model to a laptop)

Both are required. Import the EXMODZ through JimK72's Icarus Mod Manager and it
installs both automatically.

CRAFTING
--------
Crafted for free (no tech unlock) at the Crafting Bench, Machining Bench,
Fabricator, or Manufacturer. Look for "UDA Terminal Laptop":
    Steel Ingot x5, Electronics x5, Glass x3, Epoxy x2

WHAT THE PAK DOES
-----------------
Edits ONE asset - the deployable blueprint BP_Exotic_Delivery_Interface -
repointing its static-mesh import from:
    /Game/ASS/DEP/SM_DEP_ExoticDeliveryRadio_T2     (wooden exchange radio)
to:
    /Game/ASS/ORB/SM/ICA_HabC1/SM_ORB_PRP_Laptop_01 (ICA hab laptop)

Only that single mesh reference changes. The exchange behaviour, the UI, and
every other item in the game are untouched. No deer trophy.

Mounts at: ../../../Icarus/Content/BP/Objects/World/Items/Deployables/MissionCommunication/

INSTALL
-------
Import UDA_Terminal_Laptop.EXMODZ in the Mod Manager, enable, merge, launch.
Craft "UDA Terminal Laptop" at a bench - it looks like a laptop, opens the
Orbital Exchange, and places on floors and furniture.

Built with UAssetAPI (UE4.27) + UnrealPak. Round-trip verified before packing.

CHANGELOG
---------
Ver 2.1
Now craftable for free - a recipe with no tech requirement at the Crafting Bench,
Machining Bench, Fabricator and Manufacturer, using the original build's resources
(Steel Ingot 5, Electronics 5, Glass 3, Epoxy 2). Renamed in-game to "UDA Terminal
Laptop" with a laptop inventory icon.

Ver 2.0
Complete rebuild. Reskins the vanilla Orbital Exchange Interface into a laptop instead
of building a new deployable from scratch. The PAK is now bundled in the EXMODZ - the
v1.x packages never included one, so importing them only installed data and never
changed the model. Added indoor / bench / table placement and a laptop placement ghost.
Removed all BP_Deer_Trophy references and the old custom item and recipe.

Ver 1.x (deprecated)
Earlier attempts built a new craftable laptop from a generic deployable blueprint placed
in the wrong setup slot, so it never deployed, and shipped no pak. Superseded by 2.0.
