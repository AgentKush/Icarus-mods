Extended_Wire_and_Pipe_Tool_P.pak
----------------------------------------------------------------------
Mod Version: 1.2

Author: AgentKush

Compatible with Icarus: All Weeks

Mod Type: EXMOD + Blueprint Overrides

## Description:
Extends power cable and water/fuel pipe connection range by 10x. Power cables reach 60m, water pipes 60m, biofuel pipes 60m, crude oil pipes 100m. Also extends tool trace distance for aiming at distant connection points. PAK mod - modifies BP_ActionableBehaviour_CurvedSplinePlace Blueprint.
Also makes the game's unfinished Road Kit craftable: it unlocks with the Water Pipe Tool and
lays wide asphalt roads in pieces of up to 400m. It starts in straight mode; hold R for curved.
Road pieces may twist where a straight piece joins a curved one.


Ver 1.2
Roads use the game's own road texture again, repeated instead of stretched. The game draws one
3m road mesh per piece and stretches it over the whole piece. Each road piece is now drawn as
copies of the game's road laid every 3m along it, so the asphalt, its cracks and the yellow line
keep their real size on pieces of any length, including roads already placed. The road piece
component (BP_IcarusSplineMesh_NavModifier) is rebuilt with this logic; the copies
(BP_AK_RoadTile) have no collision, navigation or shadow, and the pieces keep their collision.
Removing a piece removes its copies, and the cable, pipe and road tools' hover highlight is
drawn on the copies.
The v1.1.4 and v1.1.5 road textures are removed. A 400m piece is about 130 copies, so very long
road networks draw more.

Ver 1.1.5
Roads no longer look like plastic. v1.1.4 averaged the road texture flat, which also wiped out
the asphalt's surface relief. The cross-section now comes from three of the game's own rows of
asphalt, so it keeps the real grain in colour, relief and roughness (1.2x, softened by a pixel).
It still doesn't stretch. Matte, weathered finish: roughness +0.09, asphalt a little lighter.
The Road Kit's description now warns that road pieces may twist where a straight piece joins a
curved one. The game points each join along the previous piece, and the longer that piece, the
further a following curved piece runs on before it turns, so it can fold the road over itself.

Ver 1.1.4
New road texture that doesn't stretch. The game paints one 3m copy of its asphalt texture along
each road piece, so long pieces smeared the cracks into streaks. The three road textures are now
one averaged cross-section of the game's road (asphalt lanes, yellow centre line, dirt verges)
repeated along the whole length, so a piece looks the same at any length. Road pieces are back
to 400m (10x the game's 40m; 8m in Ver 1.1.2). Place points closer on hills.

Ver 1.1.3
The Road Kit starts in straight mode, so joins to an existing road no longer swing wide and
twist; hold R to switch to curved for bends. It uses a new road-only child of the game's spline
placement tool (BP_ActionableBehaviour_CurvedSplinePlace_Road) that only sets the starting mode
to straight. Cables and pipes still start curved.

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