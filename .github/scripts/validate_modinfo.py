#!/usr/bin/env python3
"""
Icarus EXMOD / modinfo.json Validator
Validates mod files for JimK72's Mod Manager compatibility.

Checks:
  - JSON syntax and encoding
  - Required top-level fields (name, author, version, etc.)
  - Version format (semver or week-based)
  - Row/data table structure and naming conventions
  - File references (CurrentFile table names)
  - README presence and content quality
  - Mod naming conventions
  - EXMODZ packaging structure
  - Blueprint (BP) asset validation (uasset/uexp pairs)
  - PAK file validation (naming convention, location, packaging)

Usage:
  python validate_modinfo.py path/to/ModName.EXMOD
  python validate_modinfo.py path/to/ModName.EXMODZ
  python validate_modinfo.py path/to/directory  (scans for all EXMOD/EXMODZ)

Exit codes:
  0 = all checks passed
  1 = errors found (mod will likely fail to load)
  2 = warnings only (mod may work but has issues)
"""

import gzip
import json
import os
import re
import sys
import zipfile
from pathlib import Path


# ── Game asset reference (loaded lazily) ──────────────────────────────────────

_KNOWN_GAME_ASSETS = None


def _load_game_assets():
    """Load known game assets from game_assets.json.gz (or .json fallback)."""
    global _KNOWN_GAME_ASSETS
    if _KNOWN_GAME_ASSETS is not None:
        return _KNOWN_GAME_ASSETS

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Try gzipped first, then plain JSON fallback
    gz_file = os.path.join(script_dir, "game_assets.json.gz")
    json_file = os.path.join(script_dir, "bp_assets.json")

    data = None
    try:
        if os.path.isfile(gz_file):
            with gzip.open(gz_file, "rt", encoding="utf-8") as f:
                data = json.load(f)
        elif os.path.isfile(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
    except Exception:
        pass

    if data is None:
        _KNOWN_GAME_ASSETS = set()
        return _KNOWN_GAME_ASSETS

    # Build a flat set of asset stems (lowercase) for matching
    all_assets = set()
    assets = data.get("assets", {})
    if isinstance(assets, dict):
        # Category-grouped format: {"BP": ["BP/AI/Foo", ...], ...}
        for stems in assets.values():
            for stem in stems:
                # Store the filename part (lowercase) for quick matching
                name = stem.rsplit("/", 1)[-1].lower()
                all_assets.add(name)
                # Also store full relative path (lowercase) for path matching
                all_assets.add(stem.lower())
    elif isinstance(assets, list):
        # Flat list format
        for name in assets:
            all_assets.add(name.lower())

    _KNOWN_GAME_ASSETS = all_assets
    return _KNOWN_GAME_ASSETS


# ── Schema ────────────────────────────────────────────────────────────────────

REQUIRED_FIELDS = {
    "name": str,
    "author": str,
    "version": str,
    "description": str,
    "fileName": str,
}

OPTIONAL_FIELDS = {
    "week": str,
    "Level2": str,
    "Rows": list,
}

# Valid data table file patterns: Category-D_TableName.json
# Sourced from Icarus game exports (78 categories, 292 tables)
VALID_TABLE_CATEGORIES = {
    "AI", "Accolades", "Alterations", "Animation", "Armour", "Assets", "Attachments",
    "Audio", "Bestiary", "Blueprints", "Building", "Challenges", "Character", "Config",
    "Crafting", "CriticalHit", "Currency", "DLC", "Damage", "Deployables", "Development",
    "Dialogue", "DropShip", "Engine", "Errors", "Events", "Experience", "FLOD",
    "Factions", "Farming", "FieldGuide", "Fish", "Flags", "GreatHunt", "Hints", "Horde",
    "Icarus", "Input", "InstancedMap", "Interactions", "Inventory", "Items",
    "LivingItems", "Localization", "Logging", "MetaResource", "MetaWorkshop",
    "Modifiers", "NationalFlags", "Notes", "Online", "Orchestration", "Outpost",
    "Paintings", "Perks", "PlayerTracker", "Prebuilt", "Prospects", "Quests", "RTXGI",
    "Resources", "Rulesets", "Scaling", "Settings", "Sorting", "Spawn", "Statistics",
    "Stats", "Tags", "Talents", "TimeOfDay", "Tools", "Traits", "UI", "ValidHits",
    "Vehicles", "Weather", "World",
}

VALID_TABLE_NAMES = {
    "D_AIAudioData", "D_AICreatureType", "D_AIDescriptors", "D_AIEvents", "D_AIGrowth",
    "D_AIRelationships", "D_AISetup", "D_AISpawnConfig", "D_AISpawnRules",
    "D_AISpawnZones", "D_Accolades", "D_AccountFlags", "D_Actionable", "D_Actions",
    "D_AfflictionChance", "D_AlterationModifiers", "D_Alterations", "D_AmmoTypes",
    "D_Armour", "D_ArmourSetBonus", "D_ArmourSets", "D_AssetReferences", "D_Atmospheres",
    "D_AttachmentIcons", "D_AutonomousSpawns", "D_BagPriority", "D_Ballistic",
    "D_BestiaryData", "D_BestiaryPoints", "D_BestiaryTraitTypes", "D_BestiaryTraits",
    "D_BiomeAudioData", "D_Biomes", "D_BlueprintUnlocks", "D_BreakableRockData",
    "D_Buildable", "D_BuildableAudioData", "D_BuildingLookup", "D_BuildingPieces",
    "D_BuildingSkins", "D_BuildingStability", "D_BuildingTypes", "D_Challenges",
    "D_CharacterCreationData", "D_CharacterFlags", "D_CharacterGrowth",
    "D_CharacterPerks", "D_CharacterStartingStats", "D_CharacterTimeline",
    "D_CharacterVoices", "D_ChargedModifiers", "D_CollectableNotes", "D_Combustible",
    "D_Consumable", "D_ContextMenuGroupTypes", "D_CraftingAudioData",
    "D_CraftingModifications", "D_CraftingTags", "D_CreatureAudioThreatData",
    "D_CriticalHitAreaAudioData", "D_CriticalHitAreas", "D_CriticalHitSetup",
    "D_CrudeOil", "D_CurrencyConversions", "D_CustomGameStats", "D_DLCPackageData",
    "D_DamageTypeInfo", "D_Decayable", "D_Deployable", "D_DeployableSetup",
    "D_DeployableTypes", "D_Dialogue", "D_DialoguePool", "D_DialogueSpeaker",
    "D_DirtMoundModifications", "D_DropGroups", "D_DropShipActions", "D_DropShipParts",
    "D_DropShipSequences", "D_Durable", "D_DynamicQuestRewardItems",
    "D_DynamicQuestRewards", "D_DynamicQuests", "D_Energy", "D_EpicCreatures",
    "D_Equippable", "D_ErrorCodes", "D_ExoticSpawn", "D_Experience",
    "D_ExperienceEvents", "D_ExtractorRecipes", "D_FLODDescriptions", "D_FactionInfo",
    "D_FactionMissions", "D_Factions", "D_Farmable", "D_FarmingGrowthStates",
    "D_FarmingSeeds", "D_FeatureLevels", "D_FieldGuideCategories",
    "D_FieldGuideMetaData", "D_FieldGuideRedirect", "D_FieldGuideSets", "D_Fillable",
    "D_FirearmAudioData", "D_FirearmData", "D_FirearmScopeData", "D_FishData",
    "D_FishSetup", "D_FishSpawnConfig", "D_FishSpawnZones", "D_Flammable", "D_Floatable",
    "D_Focusable", "D_FoodTypes", "D_Fuel", "D_GOAPActions", "D_GOAPGoals",
    "D_GOAPMotivations", "D_GOAPProperties", "D_GOAPSetup", "D_GameplayConfig",
    "D_Generator", "D_GeneticLineages", "D_GeneticValues", "D_GrantedAuras",
    "D_GraphicsTierDescription", "D_GraphicsTierDescriptionMods",
    "D_GreatHuntCreatureInfo", "D_GreatHunts", "D_GroupedInstancedMapData",
    "D_Harvestable", "D_Highlightable", "D_Hints", "D_Hitable", "D_Horde", "D_HordeWave",
    "D_HuntingClueSetup", "D_HuntingSetup", "D_IcarusAttachments", "D_IcarusResources",
    "D_InstancedMapData", "D_Interactable", "D_Interactions", "D_Inventory",
    "D_InventoryContainer", "D_InventoryID", "D_InventoryInfo", "D_ItemAnimations",
    "D_ItemAttachment", "D_ItemAttachments", "D_ItemAudioData",
    "D_ItemClassificationsIcons", "D_ItemRanks", "D_ItemRewards", "D_ItemTemplate",
    "D_ItemTraitMasks", "D_ItemWeightStatQueries", "D_Itemable", "D_ItemsStatic",
    "D_KeyIcons", "D_KeybindContexts", "D_Keybindings", "D_Keys", "D_Languages",
    "D_LevelSequences", "D_LivingItem", "D_LivingItemShopItems", "D_LivingItemUpgrades",
    "D_LogCategories", "D_MapIcons", "D_MapSearchArea", "D_Meshable", "D_MetaCurrency",
    "D_MetaResourceNodes", "D_MissionNPC", "D_MissionTypes", "D_ModifierStateAudioData",
    "D_ModifierStates", "D_Mounts", "D_MusicLocationConditions",
    "D_MusicQuestConditions", "D_MusicTrackStateGroups", "D_MusicTracks",
    "D_NationalFlags", "D_OptionalResourceFlows", "D_OrchestrationEvents",
    "D_OrchestrationStateFlags", "D_OreDeposit", "D_Outposts", "D_Oxygen", "D_Paintings",
    "D_PlayerAccoladeCategories", "D_PlayerFootstepAudioData", "D_PlayerIdentity",
    "D_PlayerTalentModifiers", "D_PlayerTrackerCategories", "D_PlayerTrackers",
    "D_PrebuiltStructures", "D_PreviewCameraSettings", "D_Processing",
    "D_ProcessorRecipes", "D_ProjectileTypes", "D_ProspectDifficulty",
    "D_ProspectForecast", "D_ProspectList", "D_ProspectPinStates", "D_ProspectStats",
    "D_QuestEnemyModifiers", "D_QuestEvents", "D_QuestQueries",
    "D_QuestVocalisationModifiers", "D_QuestWeatherModifiers", "D_Quests", "D_QuickMove",
    "D_RCONCommand", "D_RTXGIVolumes", "D_RadialMenuData", "D_RadialOptions",
    "D_RangedWeaponData", "D_RecipeSets", "D_RecoveryBeacons", "D_RefinedOil",
    "D_RepGraphClassPolicies", "D_RepGraphClassSettings", "D_Resource",
    "D_ResourceNodeAudioData", "D_RichImages", "D_RichTextStyle", "D_RiverAudioData",
    "D_Rocketable", "D_Rulesets", "D_Saddles", "D_ScalingRules", "D_ScriptedEvents",
    "D_SeedModifications", "D_SessionFlags", "D_Slotable", "D_SortTypePriority",
    "D_StaminaActionCosts", "D_StasisBag", "D_StatAfflictions", "D_StatCategories",
    "D_StatGameplayTags", "D_Statistics", "D_Stats", "D_Surfaces", "D_SurvivalTriggers",
    "D_TagQueries", "D_TalentArchetypes", "D_TalentModelViews", "D_TalentModels",
    "D_TalentRanks", "D_TalentTrees", "D_TalentViews", "D_Talents",
    "D_TamedCreatureModifiers", "D_Tames", "D_TerrainZoneAudioData", "D_Terrains",
    "D_Thermal", "D_TimeOfDay", "D_TimelineRanks", "D_ToolDamage", "D_ToolTypes",
    "D_Transmutable", "D_TreeAudioData", "D_Turret", "D_Usable", "D_Uses",
    "D_ValidAmmoTypes", "D_ValidHitQueries", "D_ValidHitTypes", "D_ValidInteractQueries",
    "D_VehicleSetups", "D_Vehicular", "D_VocalisationSettings", "D_Vocalisations",
    "D_VoxelDistributionRegion", "D_VoxelMaterialMap", "D_VoxelSetupData", "D_Water",
    "D_WaterSetup", "D_WeatherActions", "D_WeatherBiomeGroups", "D_WeatherEvents",
    "D_WeatherPools", "D_WeatherTierIcon", "D_Weight", "D_WorkshopItems",
    "D_WorldBosses", "D_WorldData",
}

VERSION_PATTERNS = [
    re.compile(r"^\d+\.\d+(\.\d+)?$"),          # semver: 1.0, 1.0.0
    re.compile(r"^v?\d+\.\d+(\.\d+)?$"),         # v-prefix: v1.0, v1.0.0
    re.compile(r"^[wW]\d+$"),                     # week: w132, W132
    re.compile(r"^\d+\.\d+\.\d+[-+].+$"),        # semver+meta: 1.0.0-beta
]

NSLOCTEXT_PATTERN = re.compile(
    # each argument is a C-style string; the game's own data uses escaped quotes inside
    # them, e.g. "Shengong \"Heike\" Axe"
    r'^NSLOCTEXT\(\s*"(?:[^"\\]|\\.)*"\s*,\s*"(?:[^"\\]|\\.)*"\s*,\s*"(?:[^"\\]|\\.)*"\s*\)$'
)

ICON_PATH_PATTERN = re.compile(r"^/Game/Assets/")


# ── Result classes ────────────────────────────────────────────────────────────

class Issue:
    def __init__(self, level, message, location=None):
        self.level = level  # "error", "warning", "info"
        self.message = message
        self.location = location

    def __str__(self):
        icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(self.level, "?")
        loc = f" [{self.location}]" if self.location else ""
        return f"  {icon} {self.level.upper()}{loc}: {self.message}"


class ValidationResult:
    def __init__(self, file_path):
        self.file_path = file_path
        self.issues = []

    def error(self, msg, location=None):
        self.issues.append(Issue("error", msg, location))

    def warning(self, msg, location=None):
        self.issues.append(Issue("warning", msg, location))

    def info(self, msg, location=None):
        self.issues.append(Issue("info", msg, location))

    @property
    def errors(self):
        return [i for i in self.issues if i.level == "error"]

    @property
    def warnings(self):
        return [i for i in self.issues if i.level == "warning"]

    @property
    def passed(self):
        return len(self.errors) == 0

    def summary(self):
        errs = len(self.errors)
        warns = len(self.warnings)
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        return f"{status} — {errs} error(s), {warns} warning(s)"


# ── Validators ────────────────────────────────────────────────────────────────

def validate_json_syntax(content, result):
    """Check JSON is valid and parseable."""
    # Strip UTF-8 BOM if present (common in Windows-created files)
    if content.startswith("\ufeff"):
        content = content[1:]
    try:
        data = json.loads(content)
        if not isinstance(data, dict):
            result.error("Root element must be a JSON object, not " + type(data).__name__)
            return None
        return data
    except json.JSONDecodeError as e:
        result.error(f"Invalid JSON syntax: {e}")
        return None


def validate_encoding(content_bytes, result):
    """Check file uses UTF-8 encoding."""
    try:
        content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        result.error("File is not valid UTF-8. Mod Manager requires UTF-8 encoding.")
        # Try to decode anyway for further validation
    # Check for BOM
    if content_bytes[:3] == b"\xef\xbb\xbf":
        result.warning("File has UTF-8 BOM marker. This usually works but is unnecessary.")


def validate_required_fields(data, result):
    """Check all required top-level fields exist with correct types."""
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            result.error(f'Missing required field: "{field}"')
        elif not isinstance(data[field], expected_type):
            result.error(
                f'Field "{field}" must be {expected_type.__name__}, '
                f"got {type(data[field]).__name__}"
            )

    for field, expected_type in OPTIONAL_FIELDS.items():
        if field in data and not isinstance(data[field], expected_type):
            result.warning(
                f'Optional field "{field}" should be {expected_type.__name__}, '
                f"got {type(data[field]).__name__}"
            )


def validate_mod_name(data, result):
    """Check mod name conventions."""
    name = data.get("name", "")
    filename = data.get("fileName", "")

    if not name:
        return  # Already caught by required fields check

    if len(name) < 2:
        result.warning("Mod name is very short (less than 2 characters)")

    if len(name) > 100:
        result.warning("Mod name is very long (over 100 characters)")

    # Check name matches fileName (normalize for comparison)
    if filename and name:
        # Normalize: remove special chars, spaces, underscores, lowercase
        norm_name = re.sub(r"[^a-z0-9]", "", name.lower())
        norm_file = re.sub(r"[^a-z0-9]", "", filename.lower())
        if norm_name != norm_file and norm_name not in norm_file and norm_file not in norm_name:
            result.warning(
                f'"name" ({name}) differs from "fileName" ({filename}). '
                "These should usually match for Mod Manager compatibility."
            )

    # Check for invalid characters in fileName
    if filename:
        invalid_chars = re.findall(r'[<>:"/\\|?*]', filename)
        if invalid_chars:
            result.error(
                f'"fileName" contains invalid characters: {invalid_chars}. '
                "This will cause file system errors."
            )

        if " " in filename:
            result.warning(
                '"fileName" contains spaces. Consider using underscores or '
                "camelCase for better cross-platform compatibility."
            )


def validate_author(data, result):
    """Check author field."""
    author = data.get("author", "")
    if not author:
        return

    if len(author) < 2:
        result.warning("Author name is very short")

    if author.lower() in ("author", "your name", "unknown", "anonymous", "test"):
        result.warning(f'Author appears to be a placeholder: "{author}"')


def validate_version(data, result):
    """Check version string format."""
    version = data.get("version", "")
    if not version:
        return  # Already caught by required fields

    if not any(p.match(version) for p in VERSION_PATTERNS):
        result.warning(
            f'Version "{version}" doesn\'t match expected formats: '
            "semver (1.0, 1.0.0), week (w132), or v-prefix (v1.0)"
        )


def validate_week(data, result):
    """Check week compatibility field."""
    week = data.get("week", "")
    if not week:
        return  # Week is optional

    # "All" means compatible with all versions
    if week.lower() == "all":
        return

    if not re.match(r"^[wW]?\d+$", week):
        result.warning(
            f'Week field "{week}" doesn\'t match expected format (e.g., "132", "w132", or "All")'
        )


def validate_description(data, result):
    """Check description quality."""
    desc = data.get("description", "")
    if not desc:
        return

    if len(desc) < 10:
        result.warning("Description is very short. Consider adding more detail for users.")

    if desc.lower() in ("description", "a mod", "my mod", "test", "todo"):
        result.warning(f'Description appears to be a placeholder: "{desc}"')


def validate_rows(data, result):
    """Validate the Rows array structure and content."""
    rows = data.get("Rows", [])
    if not rows:
        result.info("Mod has no Rows — it won't modify any game data tables.")
        return

    if not isinstance(rows, list):
        result.error('"Rows" must be an array')
        return

    seen_tables = set()

    for i, row in enumerate(rows):
        loc = f"Rows[{i}]"

        if not isinstance(row, dict):
            result.error(f"Row entry must be an object, got {type(row).__name__}", loc)
            continue

        # Check CurrentFile
        current_file = row.get("CurrentFile")
        if not current_file:
            result.error('Missing "CurrentFile" in row entry', loc)
            continue

        if not isinstance(current_file, str):
            result.error('"CurrentFile" must be a string', loc)
            continue

        # Skip EndOfMod sentinel rows (valid Mod Manager terminator)
        if current_file == "EndOfMod":
            continue

        # Validate table file naming: Category-D_TableName.json
        # Also handles multi-segment categories like Items-Types-D_BuildingTypes.json
        table_match = re.match(r"^(.+)-(D_\w+)\.json$", current_file)
        if not table_match:
            result.warning(
                f'"{current_file}" doesn\'t match expected format: '
                "Category-D_TableName.json",
                loc,
            )
        else:
            category_full = table_match.group(1)
            # Use the first segment for category validation
            category = category_full.split("-")[0]
            table_name = table_match.group(2)

            if category not in VALID_TABLE_CATEGORIES:
                result.info(
                    f'Table category "{category}" is not in common categories. '
                    "This may be a custom or newer table.",
                    loc,
                )

            if table_name not in VALID_TABLE_NAMES:
                result.info(
                    f'Table "{table_name}" is not in common tables. '
                    "This may be a custom or newer table.",
                    loc,
                )

        # Check for duplicate table references
        if current_file in seen_tables:
            result.warning(
                f'Table "{current_file}" appears multiple times in Rows. '
                "Consider merging File_Items into a single entry.",
                loc,
            )
        seen_tables.add(current_file)

        # Check File_Items
        file_items = row.get("File_Items")
        if file_items is None:
            result.error('Missing "File_Items" in row entry', loc)
            continue

        if not isinstance(file_items, list):
            result.error('"File_Items" must be an array', loc)
            continue

        if len(file_items) == 0:
            result.warning('"File_Items" is empty — this row does nothing', loc)

        # Validate individual items
        for j, item in enumerate(file_items):
            item_loc = f"{loc}.File_Items[{j}]"
            validate_file_item(item, current_file, item_loc, result)


def validate_file_item(item, table_file, loc, result):
    """Validate an individual File_Items entry."""
    if not isinstance(item, dict):
        result.error(f"Item must be an object, got {type(item).__name__}", loc)
        return

    # Every item needs a Name (row identifier)
    name = item.get("Name")
    if not name:
        result.error('Missing "Name" field — every row needs a unique identifier', loc)
    elif not isinstance(name, str):
        result.error('"Name" must be a string', loc)

    # Check NSLOCTEXT format for display strings
    for field in ("DisplayName", "Description"):
        value = item.get(field)
        if value and isinstance(value, str):
            if "NSLOCTEXT" in value and not NSLOCTEXT_PATTERN.match(value):
                result.warning(
                    f'"{field}" has malformed NSLOCTEXT. Expected: '
                    'NSLOCTEXT("Table", "Key", "Display Text")',
                    loc,
                )

    # Check RowName references
    for field in ("Item", "ItemStaticData", "TalentTree", "Archetype", "Model"):
        value = item.get(field)
        if isinstance(value, dict):
            if "RowName" not in value:
                result.warning(
                    f'"{field}" object is missing "RowName" reference',
                    loc,
                )
            elif not isinstance(value["RowName"], str):
                result.error(f'"{field}.RowName" must be a string', loc)
            elif not value["RowName"]:
                result.warning(f'"{field}.RowName" is empty', loc)

    # Check Icon paths
    icon = item.get("Icon")
    if icon and isinstance(icon, str):
        if not ICON_PATH_PATTERN.match(icon):
            result.warning(
                f'Icon path doesn\'t start with /Game/Assets/: "{icon[:60]}..."',
                loc,
            )

    # Check Position/Size for talent grid items
    if "Talents-D_Talents.json" in table_file:
        pos = item.get("Position")
        size = item.get("Size")
        if pos and isinstance(pos, dict):
            if "X" not in pos or "Y" not in pos:
                result.warning("Position should have X and Y coordinates", loc)
        if size and isinstance(size, dict):
            if "X" not in size or "Y" not in size:
                result.warning("Size should have X and Y dimensions", loc)

    # Check cost arrays for workshop items
    if "MetaWorkshop-D_WorkshopItems.json" in table_file:
        for cost_field in ("ResearchCost", "ReplicationCost"):
            costs = item.get(cost_field)
            if costs is not None:
                if not isinstance(costs, list):
                    result.error(f'"{cost_field}" must be an array', loc)
                else:
                    for k, cost in enumerate(costs):
                        if isinstance(cost, dict):
                            if "Amount" not in cost:
                                result.warning(
                                    f'{cost_field}[{k}] missing "Amount"', loc
                                )
                            elif not isinstance(cost["Amount"], (int, float)):
                                result.error(
                                    f'{cost_field}[{k}].Amount must be a number',
                                    loc,
                                )


def validate_readme(mod_dir, result):
    """Check for README presence and quality."""
    readme_candidates = ["README.md", "readme.md", "README.txt", "readme.txt"]
    readme_path = None

    for candidate in readme_candidates:
        path = os.path.join(mod_dir, candidate)
        if os.path.isfile(path):
            readme_path = path
            break

    if not readme_path:
        result.warning(
            "No README file found. A README.md helps users understand your mod."
        )
        return

    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        result.warning(f"Could not read {os.path.basename(readme_path)}")
        return

    if len(content.strip()) < 50:
        result.warning("README is very short (under 50 characters). Consider adding more detail.")

    # Check for common sections
    content_lower = content.lower()
    if "install" not in content_lower:
        result.info("README doesn't mention installation instructions.")
    if "compat" not in content_lower and "week" not in content_lower:
        result.info("README doesn't mention compatibility or game week version.")
    if "changelog" not in content_lower and "change" not in content_lower:
        result.info("README doesn't include a changelog section.")


def validate_exmodz_structure(exmodz_path, result):
    """Validate EXMODZ zip structure matches Mod Manager expectations."""
    if not zipfile.is_zipfile(exmodz_path):
        result.error("File is not a valid ZIP archive")
        return None

    with zipfile.ZipFile(exmodz_path, "r") as zf:
        names = zf.namelist()

        # Check for EXMOD in Extracted Mods/ folder
        exmod_files = [n for n in names if n.startswith("Extracted Mods/") and n.endswith(".EXMOD")]
        if not exmod_files:
            result.error(
                'No EXMOD file found in "Extracted Mods/" folder. '
                "Mod Manager requires the EXMOD at: Extracted Mods/ModName.EXMOD"
            )
            # Check if it's in the wrong location
            all_exmods = [n for n in names if n.endswith(".EXMOD")]
            if all_exmods:
                result.info(
                    f"Found EXMOD at wrong location: {all_exmods[0]}. "
                    "Move it to Extracted Mods/ folder."
                )
            return None
        elif len(exmod_files) > 1:
            result.warning(f"Multiple EXMOD files found: {exmod_files}. Expected one.")

        # Derive mod name from EXMOD filename
        exmod_name = exmod_files[0].replace("Extracted Mods/", "").replace(".EXMOD", "")

        # ── Blueprint (BP) validation ──────────────────────────────────
        bp_files = [n for n in names if "/BP/" in n and not n.endswith("/")]
        if bp_files:
            uasset_files = [n for n in bp_files if n.endswith(".uasset")]
            uexp_files = [n for n in bp_files if n.endswith(".uexp")]

            result.info(f"BP folder found: {len(uasset_files)} .uasset, {len(uexp_files)} .uexp files")

            # Every .uasset should have a matching .uexp (and vice versa)
            uasset_stems = {n.rsplit(".", 1)[0] for n in uasset_files}
            uexp_stems = {n.rsplit(".", 1)[0] for n in uexp_files
                          if not n.endswith(".vanilla.bak")}

            orphan_uassets = uasset_stems - uexp_stems
            orphan_uexps = uexp_stems - uasset_stems

            for stem in orphan_uassets:
                basename = stem.rsplit("/", 1)[-1]
                result.error(
                    f'BP asset "{basename}.uasset" has no matching .uexp file. '
                    "Both files are required for Unreal Engine to load the blueprint."
                )
            for stem in orphan_uexps:
                basename = stem.rsplit("/", 1)[-1]
                result.error(
                    f'BP asset "{basename}.uexp" has no matching .uasset file. '
                    "Both files are required for Unreal Engine to load the blueprint."
                )

            # Cross-reference BP assets against known game assets
            known_assets = _load_game_assets()
            if known_assets:
                for stem in uasset_stems:
                    # Extract the path relative to BP/ folder
                    # e.g. "ModName/BP/AI/GOAP/BP_Foo" -> "AI/GOAP/BP_Foo"
                    parts = stem.split("/BP/", 1)
                    if len(parts) == 2:
                        bp_rel = parts[1]
                        bp_name = bp_rel.rsplit("/", 1)[-1]
                        # Check by full path (BP/subpath) and by filename alone
                        full_check = f"BP/{bp_rel}".lower()
                        name_check = bp_name.lower()
                        if full_check in known_assets or name_check in known_assets:
                            result.info(
                                f'BP asset "{bp_name}" matches known game asset — '
                                "valid override."
                            )
                        else:
                            result.info(
                                f'BP asset "{bp_name}" is not a known game asset. '
                                "Custom blueprint (fine) or check the name for typos."
                            )

            # BP files must be inside the ModName/ folder, not Extracted Mods/
            wrong_location_bp = [n for n in bp_files if n.startswith("Extracted Mods/")]
            if wrong_location_bp:
                result.error(
                    "BP files found inside Extracted Mods/ — they must be in "
                    f'"{exmod_name}/BP/" folder instead.'
                )

        # ── PAK file validation ────────────────────────────────────────
        pak_files = [n for n in names if n.lower().endswith(".pak")]
        if pak_files:
            result.info(f"PAK file(s) found: {', '.join(pak_files)}")

            for pak in pak_files:
                # PAK files should be in ModName/ folder, not Extracted Mods/
                if pak.startswith("Extracted Mods/"):
                    result.error(
                        f'PAK file "{pak}" is inside Extracted Mods/ — '
                        f'move it to "{exmod_name}/" folder.'
                    )

                # PAK naming convention: should end with _P.pak
                pak_basename = pak.rsplit("/", 1)[-1]
                if not pak_basename.endswith("_P.pak"):
                    result.warning(
                        f'PAK file "{pak_basename}" does not follow the _P.pak naming '
                        "convention (e.g. ModName_P.pak). Icarus may not load it."
                    )

                # Warn that PAK mods require server-side install
                result.info(
                    f'PAK mod detected ({pak_basename}). Remember: all players and '
                    "the server must install .pak files to Icarus/Content/Paks/mods/"
                )

        # ── Check for BP on disk but missing from EXMODZ ──────────────
        # Scope to the mod's OWN folder (ModName/) not the parent directory
        # This avoids false positives when multiple mods share a parent folder
        mod_dir = os.path.dirname(exmodz_path)
        mod_own_dir = os.path.join(mod_dir, exmod_name)
        disk_bp_dir = os.path.join(mod_own_dir, "BP") if os.path.isdir(os.path.join(mod_own_dir, "BP")) else os.path.join(mod_dir, "BP")
        if os.path.isdir(disk_bp_dir):
            if not bp_files:
                result.error(
                    'BP/ folder exists on disk but is NOT included in the EXMODZ package. '
                    "Blueprint assets must be packaged inside the EXMODZ for the mod to work."
                )
            else:
                # Per-file cross-check: detect individual BP files on disk missing from package
                packaged_bp_names = {n.rsplit("/", 1)[-1] for n in bp_files}
                for root, dirs, files in os.walk(disk_bp_dir):
                    for f in files:
                        if f.endswith('.vanilla.bak'):
                            continue
                        if f not in packaged_bp_names:
                            result.error(
                                f'BP file "{f}" exists on disk but is NOT in the EXMODZ '
                                "package. Missing assets cause Unreal Engine load failures."
                            )

        # Check for .pak on disk but missing from EXMODZ
        # Only check the mod's own folder (ModName/) to avoid false positives
        # when multiple mods share a parent directory
        pak_check_dir = mod_own_dir if os.path.isdir(mod_own_dir) else None
        if pak_check_dir:
            disk_paks = [f for f in os.listdir(pak_check_dir) if f.lower().endswith(".pak")]
            packaged_pak_names = {p.rsplit("/", 1)[-1] for p in pak_files}
            for dp in disk_paks:
                if dp not in packaged_pak_names:
                    result.warning(
                        f'PAK file "{dp}" exists on disk but is NOT in the EXMODZ package. '
                        "If this PAK is required, it should be included."
                    )

        # ── Documentation / support file checks ────────────────────────
        # EXMODZ packages should include these files in ModName/ folder
        readme_md = [n for n in names
                     if n.lower() == f"{exmod_name.lower()}/readme.md"
                     or (n.count("/") == 1
                         and n.lower().endswith("/readme.md")
                         and not n.startswith("Extracted Mods/"))]
        banner_png = [n for n in names
                      if n.lower() == f"{exmod_name.lower()}/banner.png"
                      or (n.count("/") == 1
                          and n.lower().endswith("/banner.png")
                          and not n.startswith("Extracted Mods/"))]
        # Readme .txt — the main info body displayed in Icarus Mod Manager
        readme_txt = [n for n in names
                      if n.count("/") == 1
                      and n.lower().endswith(".txt")
                      and n.lower().startswith(f"{exmod_name.lower()}/")
                      and "readme" in n.lower()]

        if not readme_md:
            result.warning(
                f'No README.md found in "{exmod_name}/" folder. '
                "A README helps users understand what the mod does and how to install it."
            )
        if not banner_png:
            result.info(
                f'No Banner.png found in "{exmod_name}/" folder. '
                "A banner image makes the mod look polished in Mod Manager."
            )
        if not readme_txt:
            result.warning(
                f'No Readme .txt found in "{exmod_name}/" folder. '
                "This file provides the main info body displayed in Icarus Mod Manager."
            )

        # Disk cross-check: doc files on disk but missing from EXMODZ
        # Check the mod's own folder first, fall back to parent dir
        doc_check_dir = mod_own_dir if os.path.isdir(mod_own_dir) else mod_dir
        if doc_check_dir:
            for doc_file in ["README.md", "Banner.png"]:
                disk_doc = os.path.join(doc_check_dir, doc_file)
                if os.path.isfile(disk_doc):
                    packaged_names_lower = {n.lower() for n in names}
                    expected = f"{exmod_name}/{doc_file}".lower()
                    if expected not in packaged_names_lower:
                        result.warning(
                            f'"{doc_file}" exists on disk but is NOT in the EXMODZ package.'
                        )
            # Check for Readme .txt files on disk
            for f in os.listdir(doc_check_dir):
                if f.lower().endswith(".txt") and "readme" in f.lower():
                    packaged_txt_lower = {n.rsplit("/", 1)[-1].lower() for n in names}
                    if f.lower() not in packaged_txt_lower:
                        result.warning(
                            f'"{f}" exists on disk but is NOT in the EXMODZ package.'
                        )

        # Read and return the EXMOD content
        exmod_path = exmod_files[0]
        try:
            content_bytes = zf.read(exmod_path)
            validate_encoding(content_bytes, result)
            return content_bytes.decode("utf-8-sig", errors="replace")
        except Exception as e:
            result.error(f"Failed to read {exmod_path}: {e}")
            return None


# ── Main runner ───────────────────────────────────────────────────────────────

def validate_file(file_path):
    """Run all validations on a single file."""
    result = ValidationResult(file_path)
    file_path = str(file_path)

    if not os.path.exists(file_path):
        result.error(f"File not found: {file_path}")
        return result

    # Handle EXMODZ (zip)
    if file_path.upper().endswith(".EXMODZ"):
        content = validate_exmodz_structure(file_path, result)
        if content is None:
            return result
        mod_dir = os.path.dirname(file_path)
    # Handle EXMOD (plain JSON)
    elif file_path.upper().endswith((".EXMOD", ".JSON")):
        try:
            with open(file_path, "rb") as f:
                content_bytes = f.read()
            validate_encoding(content_bytes, result)
            content = content_bytes.decode("utf-8-sig", errors="replace")
        except Exception as e:
            result.error(f"Failed to read file: {e}")
            return result
        mod_dir = os.path.dirname(file_path)
    else:
        result.error(f"Unsupported file type: {file_path}")
        return result

    # Parse JSON
    data = validate_json_syntax(content, result)
    if data is None:
        return result

    # Run all validators
    validate_required_fields(data, result)
    validate_mod_name(data, result)
    validate_author(data, result)
    validate_version(data, result)
    validate_week(data, result)
    validate_description(data, result)
    validate_rows(data, result)

    # Check for README in the mod's directory
    if mod_dir:
        validate_readme(mod_dir, result)

    return result


def find_mod_files(directory):
    """Recursively find all EXMOD/EXMODZ files in a directory."""
    mod_files = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.upper().endswith((".EXMOD", ".EXMODZ")):
                mod_files.append(os.path.join(root, f))
    return sorted(mod_files)


def print_github_annotations(result):
    """Output GitHub Actions annotations for CI integration."""
    for issue in result.issues:
        if issue.level == "error":
            loc = f" ({issue.location})" if issue.location else ""
            print(f"::error file={result.file_path}::{issue.message}{loc}")
        elif issue.level == "warning":
            loc = f" ({issue.location})" if issue.location else ""
            print(f"::warning file={result.file_path}::{issue.message}{loc}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    github_mode = "--github" in sys.argv or os.environ.get("GITHUB_ACTIONS") == "true"
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not args:
        print("Error: No target file or directory specified.")
        print(__doc__)
        sys.exit(1)

    target = args[0]

    # Collect files to validate
    if os.path.isdir(target):
        files = find_mod_files(target)
        if not files:
            print(f"No EXMOD/EXMODZ files found in {target}")
            sys.exit(1)
    else:
        files = [target]

    all_passed = True
    total_errors = 0
    total_warnings = 0

    for filepath in files:
        print(f"\n{'═' * 60}")
        print(f"  Validating: {os.path.basename(filepath)}")
        print(f"{'═' * 60}")

        result = validate_file(filepath)

        # Print issues
        for issue in result.issues:
            print(str(issue))

        # Print summary
        print(f"\n  {result.summary()}")

        # GitHub annotations
        if github_mode:
            print_github_annotations(result)

        if not result.passed:
            all_passed = False
        total_errors += len(result.errors)
        total_warnings += len(result.warnings)

    # Final summary
    if len(files) > 1:
        print(f"\n{'═' * 60}")
        print(f"  TOTAL: {len(files)} file(s), {total_errors} error(s), {total_warnings} warning(s)")
        status = "✅ ALL PASSED" if all_passed else "❌ SOME FAILED"
        print(f"  {status}")
        print(f"{'═' * 60}")

    if total_errors > 0:
        sys.exit(1)
    elif total_warnings > 0:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
