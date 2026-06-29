UDA Terminal Laptop  -  v2.1
============================

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
