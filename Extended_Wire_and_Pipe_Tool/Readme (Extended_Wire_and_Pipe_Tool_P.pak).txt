Extended_Wire_and_Pipe_Tool_P.pak
----------------------------------------------------------------------
Mod Version: 1.1.2

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD + Blueprint Overrides

## Description:
Extends power cable and water/fuel pipe connection range by 10x. Power cables reach 60m, water pipes 60m, biofuel pipes 60m, crude oil pipes 100m. Also extends tool trace distance for aiming at distant connection points. PAK mod - modifies BP_ActionableBehaviour_CurvedSplinePlace Blueprint.
Also makes the game's unfinished Road Kit craftable: it unlocks with the Water Pipe Tool and
lays wide asphalt roads in pieces of up to 8m. Hold R to switch between curved and straight.


Ver 1.1.2
Road pieces capped at 8m (was 400m; the game's value is 40m). Each piece between two points
carries one 3m copy of the asphalt texture, so long pieces stretched it; at 8m it is stretched
at most 2.7x, and curved joins no longer swing wide and twist. Hold R to switch the Road Kit
between curved and straight; use straight to join an existing road at an angle.

Ver 1.1.1
Roads fixed. The game draws roads with an unfinished 1.9m cobblestone path mesh that players
fall through. Roads now use the game's own 9.6m asphalt road mesh (SM_SplineRoad) in its place,
lowered 65cm so the surface sits at ground level, and road pieces block players with the game's
BlockAll collision. Cables and pipes are unchanged. Place road points every 10-20m: each stretch
between two points is one road piece, so very long stretches stretch the asphalt texture.

Ver 1.1
Craftable Road Kit. The game's unfinished Kit_Road gets a recipe at the Machining Bench,
Fabricator and Manufacturer (50 Copper Wire, 50 Gold Wire, 4 Platinum Sheath, the Water Pipe
Tool's cost) that unlocks with the Water Pipe Tool blueprint. It gets a new asphalt-road icon
drawn from the game's road texture, the game's Tier 3 kit model instead of an invisible
placeholder, and the quickbar and wire-tool tags, so it can be equipped and shows its
curved/straight mode. Its "To do." flavour text is removed. Roads use the game's own road mesh,
with this mod's 400m range (game 40m).

Ver 1.0.2
Rebuilt BP_ActionableBehaviour_CurvedSplinePlace from the 19 November 2026 game files with the
same changes: every spline type's maximum length x10 (road, outdoor and indoor power, outdoor
and indoor water, item, fuel and crude oil), tool trace 30m -> 300m and inspector range
200m -> 2000m. The old copy dated from February 2026. Its logic still matched the game, but it
lacked one dependency the game has added since (the spline actor's nav modifier component).

Ver 1.0.1
New icon and banner, drawn from the mod's live data. No gameplay change.

Ver 1.0
Initial release. 10x range extension for all cable and pipe types.

## Installation:
  1. Install JimK72's Icarus Mod Manager
     https://github.com/jimk72/IcarusModManager
  2. Download Extended_Wire_and_Pipe_Tool.EXMODZ
  3. Import via Mod Manager

----------------------------------------------------------------------
Made by AgentKush
https://github.com/AgentKush/Icarus-mods