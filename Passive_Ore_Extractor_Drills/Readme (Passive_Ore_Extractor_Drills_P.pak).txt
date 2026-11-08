Passive_Ore_Extractor_Drills_P.pak
----------------------------------------------------------------------
Mod Version: 7.8.1

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD

## Description:
23 passive ore extractors - one per ore type. Place anywhere, connect power, load Stone. Uses drill-visual processor for passive mining.


Ver 7.8.1
New icon and banner, drawn from the mod's live data. No gameplay change.

Ver 7.8
Fixed the drills mining in silence - their recipes pointed at a sound entry that does
not exist; they now use the default sound like the vanilla extractor. Removed data the
game was ignoring (display text on the item templates - the real names are unchanged -
and extra fields on recipe inputs). Known issue: a placed drill can duplicate when the
save is reloaded; that is in the drill's blueprint, not the data. 23 passive ore
extractors - one per ore type.

Ver 7.7
Fixed placement failure - dropped missing custom BP_PassiveMiner entirely. All 23 D_DeployableSetup entries now use vanilla BP_Deep_Mining_Drill_Electric. Miners can now be placed again.

Ver 7.6
Attempted to fix placement by bundling BP_PassiveMiner PAK - PAK still missing from EXMODZ, placement still broken.

Ver 7.5
Fixed broken Fabricator recipes - Iron_Ingot/Copper_Ingot replaced with correct Refined_Metal/Refined_Copper. Fixed Aluminium miner - was outputting ingots (Aluminium), now correctly outputs Bauxite ore with proper icon. Added Manufacturer bench as crafting station for all miner kits.

Ver 7.4
Added Fabricator crafting recipes - all 23 miners craftable in-game without Workshop. Tiered material costs: common (Steel+Electronics), uncommon (+Glass), rare (+Titanium+Carbon Fiber), exotic (+Composite Paste).

Ver 7.3
Fixed collision/interaction - machines are now solid and interactable again. DeployableSM set to bVisible=false (invisible) but keeps StaticMesh for collision hitbox. DeployableSK renders the animated drill visual - no double mesh, working physics.

Ver 7.2
Fixed double mesh rendering - removed static mesh from DeployableSM so only the animated skeletal mesh renders. BROKEN: Removing StaticMesh also removed collision - machines became ghost objects.

Ver 7.1
Fixed broken drill textures - swapped furnace materials to drill materials (M_DEP_DeepMiningDrill_Electric Off/On). Fixed sounds - swapped furnace FMOD audio to drill sounds (SFX_DEP_ELECTRIC_DRILL_ACTIVE/STOP). Added drill animation - skeletal mesh with Anim_DEP_DeepMiningDrill_Electric_Active.

Ver 7.0
Complete rewrite using BP_PassiveMiner (renamed Electric Furnace with drill mesh swap). No longer overrides any vanilla blueprints - unique BP at /Game/BP/../PassiveMiners/BP_PassiveMiner. Processor functionality via BP_ResourceNetworkProcessor inheritance (place anywhere, no ore deposit needed).

Ver 6.0
Attempted re-parenting drill BP from BP_Drill_Base to BP_ProcessorBase. Crashed with 'Could not find SuperStruct ActiveStateUpdated' - BP_Drill_Base functions not in BP_ProcessorBase.

Ver 1.0
Initial development - experimented with Electric Furnace approach, ore node spawners, and data-only configs.

## Files Modified:
  Talents-D_TalentArchetypes    (1 entries)
  Talents-D_TalentTrees         (1 entries)
  Crafting-D_RecipeSets         (23 entries)
  Traits-D_Processing           (23 entries)
  Traits-D_Deployable           (23 entries)
  Deployables-D_DeployableSetup (23 entries)
  Traits-D_Itemable             (46 entries)
  Traits-D_Consumable           (23 entries)
  Items-D_ItemsStatic           (46 entries)
  Items-D_ItemTemplate          (46 entries)
  MetaWorkshop-D_WorkshopItems  (23 entries)
  Talents-D_Talents             (23 entries)
  Crafting-D_ProcessorRecipes   (46 entries)

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Passive_Ore_Extractor_Drills.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods