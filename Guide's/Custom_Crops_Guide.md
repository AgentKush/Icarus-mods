# Custom Crops in Icarus — Modding Guide

**DRAFT.** Steps marked 🧪 are being tested in game right now (AK_Crop_Test). Don't treat
those as fact until this banner is gone. Written against the **September 2026** build.

How far a **data-only** mod goes (JimK72's Mod Manager, EXMOD — no Unreal editor): you can
give a plant its own name, icon, growth times, growth models, biomes, sounds and harvest.
What you **cannot** do without shipping a cooked `.pak` is add a *new* 3D model or texture.
You can only re-use models already in the game.

**Status marks used below**
- ✅ **Shipped** — a released mod already does this and nobody has reported it broken.
  That's field evidence, not a controlled test.
- 🧪 **Untested** — nobody has done it yet, as far as this repo and its issue tracker show.

---

## How farming actually works

Every seed in the game is the **same item**: `D_ItemsStatic:Seed`. What makes one seed Corn
and another Pumpkin is a single number on the item, `SeedType_Enum`, and that number is the
crop's **row position** in `D_FarmingSeeds`.

```
D_ItemTemplate: Corn_Seed      -> ItemStaticData "Seed" + SeedType_Enum 1
D_FarmingSeeds row 1: Corn     -> the crop definition:
    Stage1..Stage4, Mature, Decayed -> D_FarmingGrowthStates  (seconds per stage + the model)
    CropRewards / DecayedRewards    -> D_ItemRewards          (harvest / withered drops)
    Itemable                        -> D_Itemable             (seed name, icon, stack size)
    Deployable                      -> D_Deployable -> D_DeployableSetup   (the planted mound)
    OptimalBiomes                   -> D_Atmospheres          (where it grows best)
    Audio                           -> sow / harvest / clear sounds
    FatigueModifier                 -> D_ModifierStates       (all 35 crops share Seed_Fatigue)
```

Note the **mound is two hops**: the crop points at a `D_Deployable` row, which points at a
`D_DeployableSetup` row, and the two often have *different* names (Corn uses
`Farming_Mound_Corn` for both; `Test_Seed` uses `Farming_Mound_Test_Seed` →
`Farming_Mound_Test`).

Two things to know before you start:

- **A seed only comes back from a harvest if you have the `CanHarvestSeeds_?` stat.** No
  talent grants it. The sources are Seed Fertilizer and the Inaris sickle
  (`D_ItemsStatic: Seed_Fertilizer`, `Meta_Sickle_Inaris_00`), the Farmer's Backpack
  (`D_Equippable`), and three alterations: `Plough_Steel`, `Threshing_1`, `Seed_Harvester`.
  The Platinum and Titanium ploughs do **not** grant it.
- **`D_Farmable.AllowedSeeds`** lists 27 crops, the same list for the Dirt Mound and every
  crop plot. Seven shipped crops (Kiwi Fruit, Banana, Truffle, Onion, Agave, Prickly Pear,
  Garlic) are absent from it, along with `Invalid` and `Test_Seed`. That suggests it isn't
  what allows planting — 🧪 being tested.

### ⚠️ Row names don't follow one pattern

`<Crop>_Crops`, `Item_<Crop>_Seed`, `Farming_Mound_<Crop>`, `<Crop>_Growth_01` hold for most
crops but **15 crops break them**, so always open the crop's own `D_FarmingSeeds` row and
copy the literal `RowName` out of each field. Examples:

| Crop | Actual row names |
|---|---|
| ReedFlower | `Reed_Flower_Crops`, `Item_Reed_Flower_Seed`, `Farming_Mound_Reed` |
| BerryBush | `Item_Berry_Seed`, `Farming_Mound_Berry` |
| Beans | `Item_Bean_Seed` |
| Sugar_Cane | `Item_Seed_SugarCane`, `Spoiled_Crops_SugarCane`, `Sugar_Growth_01` |
| Kiwi_Fruit | `KiwiFruit_Crops`, `Spoiled_Crops_KiwiFruit` |
| Red_Exotic_Seed | `Red_Exotics_Raw`, `Farming_Mound_Exotic_Seed`, `Red_Exotic_Growth_01` |
| Strawberry | `Stawberry_Growth_01`, `Stawberry_Dead` — vanilla's own typo, keep it |
| Rhubarb, Kumara, Avocado, Fiber, Coconut, Bramble, Banana, Kiwi_Fruit | dead stage is `<Crop>_Dead`, not `<Crop>_Growth_Dead` |

**A wrong name doesn't error — it silently creates a new, unused row.** That's the most
common way a crop mod does nothing at all.

### Text fields

`DisplayName`, `Description` and `FlavorText` are not plain strings. The middle argument
must be `<RowName>-DisplayName` (or `-Description`, `-FlavorText`):

```json
"DisplayName": "NSLOCTEXT(\"D_Itemable\", \"Item_Corn_Seed-DisplayName\", \"Moonfruit Seed\")"
```

---

## Route A — re-dress an existing crop (the safe one)

Take a crop you don't mind losing and make it yours. The trade-off: it **replaces** that
crop for everyone running the mod. Watermelon becomes Moonfruit; there is no Watermelon.

| Step | Table | Field | Status |
|---|---|---|---|
| Rename the seed | `Traits-D_Itemable`, the row in `Itemable` | `DisplayName`, `Description`, `Icon` | 🧪 |
| Growth speed | `Farming-D_FarmingGrowthStates`, the 6 stage rows | `TimeToNextState` (seconds) | ✅ Fish & Farming Boost retimes 175 of the game's 210 crop stage rows |
| Growth models | the same 6 rows | `StageMesh` | 🧪 |
| Harvest drops | `Items-D_ItemRewards`, the row in `CropRewards` | `Rewards` | ✅ Fish & Farming Boost rewrites all 34 harvest tables |
| Withered drops | the row in `DecayedRewards` | `Rewards` | ✅ same, all 34 withered tables |
| Planting preview | `Deployables-D_DeployableSetup`, via the `D_Deployable` row | `PreviewStaticMesh` | 🧪 |
| Biomes / sounds | `Farming-D_FarmingSeeds`, the crop row | `OptimalBiomes`, `Audio` | 🧪 |

**Renaming the seed doesn't rename the produce.** The harvested item is its own
`D_ItemsStatic` / `D_Itemable` pair. Either rename that too, or point `Rewards` at a
different existing item instead.

**On models.** Vanilla's unused `Test_Seed` crop wears Avocado models, so the data clearly
can point one crop's stage at another crop's mesh. What nobody has confirmed is a *mod*
doing it. There's one field report worth knowing: in issue #9 a player's crops turned
invisible while running Fish & Farming Boost, the suspected cause was a growth row losing
its `StageMesh` during a merge, and v1.2 started shipping `StageMesh` on every row as a fix
— but the reporter never confirmed it, and that mechanism sits awkwardly with the
field-level merge rule below. Treat models as 🧪.

**A complete minimal mod** — this is the whole `.EXMOD` file, not a fragment. It re-dresses
Watermelon: 30-second stages wearing Pumpkin models, harvest drops 5 Sulfur.

```json
{
  "name": "Moonfruit", "author": "YourName", "version": "1.0",
  "description": "v1.0: Re-dresses Watermelon into Moonfruit.",
  "fileName": "Moonfruit", "week": "All", "Level2": "True",
  "Rows": [
    { "CurrentFile": "Farming-D_FarmingGrowthStates.json", "File_Items": [
      { "Name": "Watermelon_Growth_01", "TimeToNextState": 30, "StageMesh": "/Game/ASS/ENV/HRB/Crop_Pumpkin/v02/SM_HRB_Crop_Pumpkin_Stage1_Var1.SM_HRB_Crop_Pumpkin_Stage1_Var1" },
      { "Name": "Watermelon_Growth_02", "TimeToNextState": 30, "StageMesh": "/Game/ASS/ENV/HRB/Crop_Pumpkin/v02/SM_HRB_Crop_Pumpkin_Stage2_Var1.SM_HRB_Crop_Pumpkin_Stage2_Var1" },
      { "Name": "Watermelon_Growth_03", "TimeToNextState": 30, "StageMesh": "/Game/ASS/ENV/HRB/Crop_Pumpkin/v02/SM_HRB_Crop_Pumpkin_Stage3_Var1.SM_HRB_Crop_Pumpkin_Stage3_Var1" },
      { "Name": "Watermelon_Growth_04", "TimeToNextState": 30, "StageMesh": "/Game/ASS/ENV/HRB/Crop_Pumpkin/v02/SM_HRB_Crop_Pumpkin_Stage4_Var1.SM_HRB_Crop_Pumpkin_Stage4_Var1" },
      { "Name": "Watermelon_Growth_05", "TimeToNextState": 3600, "StageMesh": "/Game/ASS/ENV/HRB/Crop_Pumpkin/v02/SM_HRB_Crop_Pumpkin_Stage5_Var1.SM_HRB_Crop_Pumpkin_Stage5_Var1" },
      { "Name": "Watermelon_Growth_Dead", "TimeToNextState": 1, "StageMesh": "/Game/ASS/ENV/HRB/Crop_Pumpkin/v02/SM_HRB_Crop_Pumpkin_Dead_Var1.SM_HRB_Crop_Pumpkin_Dead_Var1" }
    ]},
    { "CurrentFile": "Traits-D_Itemable.json", "File_Items": [
      { "Name": "Item_Watermelon_Seed", "DisplayName": "NSLOCTEXT(\"D_Itemable\", \"Item_Watermelon_Seed-DisplayName\", \"Moonfruit Seed\")" }
    ]},
    { "CurrentFile": "Items-D_ItemRewards.json", "File_Items": [
      { "Name": "Watermelon_Crops", "Rewards": [
        { "Item": { "RowName": "Sulfur", "DataTableName": "D_ItemTemplate" }, "DropChance": 100,
          "DropChanceAdditiveStat": { "RowName": "None", "DataTableName": "D_Stats" },
          "RequiredStatToDrop": { "RowName": "None", "DataTableName": "D_Stats" },
          "MinRandomStackCount": 5, "MaxRandomStackCount": 5, "bRewardsScale": false,
          "StackAdditiveStat": { "RowName": "None", "DataTableName": "D_Stats" },
          "StackMultiplicativeStat": { "RowName": "None", "DataTableName": "D_Stats" } },
        { "Item": { "RowName": "Watermelon_Seed", "DataTableName": "D_ItemTemplate" }, "DropChance": 100,
          "DropChanceAdditiveStat": { "RowName": "None", "DataTableName": "D_Stats" },
          "RequiredStatToDrop": { "RowName": "CanHarvestSeeds_?", "DataTableName": "D_Stats" },
          "MinRandomStackCount": 1, "MaxRandomStackCount": 2, "bRewardsScale": true,
          "StackAdditiveStat": { "RowName": "None", "DataTableName": "D_Stats" },
          "StackMultiplicativeStat": { "RowName": "None", "DataTableName": "D_Stats" } }
      ]}
    ]}
  ]
}
```

---

## Route B — vanilla's unused crop slot 🧪

`D_FarmingSeeds` row 22 is `Test_Seed`, a leftover dev crop with a complete chain: six
growth stages wearing Avocado models, its own `Item_Test_Seed`, and a working mound
(`D_Deployable: Farming_Mound_Test_Seed` → `D_DeployableSetup: Farming_Mound_Test`). What it
lacks is a **seed item carrying number 22**, which is why nothing in game can plant it. Take
it over and no real crop is lost.

Three catches:

1. **Its harvest tables belong to another crop.** `CropRewards` is `Avocado_Crops` and
   `DecayedRewards` is `Spoiled_Crops`, both shared. Edit those and you change Avocado (and
   Volatile Exotic Bulb) too. Point `Test_Seed` at two new reward rows of your own instead.
2. **It withers 60 seconds after maturing** — raise `Test_Growth_05`'s `TimeToNextState`.
3. It isn't in `AllowedSeeds` (which may not matter — 🧪).

Give it a seed, in `Items-D_ItemTemplate.json`:

```json
{ "Name": "My_Seed", "ItemStaticData": { "RowName": "Seed" },
  "ItemCustomStats": [ { "Stat": { "Value": "SeedType_Enum" }, "Value": 22 } ] }
```

…and a recipe, or there is no way to obtain it (see below).

---

## Route C — a genuinely new crop 🧪

Append a row to `D_FarmingSeeds` and give its seed the next number (36 today). Whether the
game accepts a number past 35 is decided in compiled code, so only an in-game test settles
it. Evidence both ways: the game exe holds no compiled list of crop names, which points at a
plain row lookup; but `D_FarmingSeeds` is flagged `GenerateEnum`, and no mod has ever added
a crop row.

A new crop needs **13 rows**, all clonable from an existing crop:

1 × `D_FarmingSeeds`, 6 × `D_FarmingGrowthStates`, 1 × `D_Itemable` (the seed),
1 × `D_ItemTemplate` (the seed item + its number), 2 × `D_ItemRewards` (harvest + withered),
1 × `D_Deployable` + 1 × `D_DeployableSetup` (the mound).

Plus **a way to obtain the seed**, and possibly an `AllowedSeeds` entry.

### Getting the seed into players' hands (required for Routes B and C)

A seed nobody can obtain is a crop nobody can plant. Add a `D_ProcessorRecipes` row — this
one costs 1 Fiber in the character crafting menu with no tech unlock:

```json
{ "Name": "My_Seed_Recipe",
  "Requirement": { "RowName": "None", "DataTableName": "D_Talents" },
  "RequiredMillijoules": 250,
  "RecipeSets": [ { "RowName": "Character", "DataTableName": "D_RecipeSets" } ],
  "Inputs": [ { "Element": { "RowName": "Fiber", "DataTableName": "D_ItemsStatic" }, "Count": 1 } ],
  "Outputs": [ { "Element": { "RowName": "My_Seed", "DataTableName": "D_ItemTemplate" }, "Count": 10,
                 "DynamicProperties": [], "Alterations": [] } ],
  "Audio": { "RowName": "Default" } }
```

Vanilla's own route is a Seed Extractor recipe (produce → seeds); copy `Corn_Seeds` for that
shape. The workshop seed packet, the talent and the field guide entry are genuinely optional.

---

## Rules that will bite you

- **Never insert a row into `D_FarmingSeeds` — only append.** Seed numbers are row
  positions, so inserting renumbers every later crop, and seeds sitting in people's saves
  become a different plant. Vanilla follows this: `Test_Seed` stayed at row 22 while crops
  were added from 23 up.
- **Custom seed numbers aren't save-safe.** Tell players to harvest or clear your crops
  before removing the mod, and re-check your number after every game update — if the devs
  append a 36th crop, your row moves and your seeds change identity.
- **Fields merge one at a time; arrays don't.** Omit a field and the vanilla value stays,
  but any array you send (like `AllowedSeeds`) **replaces** the whole vanilla array, so send
  the existing entries plus yours. (Merge behaviour is from the Mod Manager's own release
  notes and visible in merged paks.)
- **Same row, same field, two mods = a conflict.** The Mod Manager asks you to pick a
  winner; take the default and the mod merged last wins.
- **Row names are case-insensitive** (Unreal FName behaviour — inferred, not tested here), so
  a name differing only in case overwrites instead of adding.
- **DLC gating** lives in `Metadata.RequiredFeatureLevel`. Re-dress a DLC crop (Route A) and
  you inherit its gate, because omitting the field keeps vanilla's value. A brand-new row
  (Route C) inherits nothing — only add `Metadata` if you *want* the gate.
- **New models or textures need a cooked `.pak`** shipped with the EXMOD. Data alone can
  only re-use what's already in the game.

---

## Crop numbers (September 2026 build)

| # | Row | # | Row | # | Row | # | Row |
|---|---|---|---|---|---|---|---|
| 0 | Invalid\* | 9 | Squash | 18 | Kumara | 27 | Coconut |
| 1 | Corn | 10 | Watermelon | 19 | Avocado | 28 | Bramble |
| 2 | Wheat | 11 | Cocoa | 20 | Strawberry | 29 | Kiwi_Fruit\* |
| 3 | ReedFlower | 12 | Coffee | 21 | Fiber | 30 | Banana\* |
| 4 | Yeast | 13 | GreenTea | 22 | Test_Seed\* (unused) | 31 | Truffle\* |
| 5 | Lily | 14 | WildTea | 23 | Tomato† | 32 | Onion\*† |
| 6 | BerryBush | 15 | Carrot | 24 | Potato† | 33 | Agave\*† |
| 7 | Pumpkin | 16 | Mushroom | 25 | Red_Exotic_Seed† | 34 | PricklyPear\*† |
| 8 | Beans | 17 | Rhubarb | 26 | Sugar_Cane | 35 | Garlic\*† |

\* absent from `AllowedSeeds`  † DLC-gated

---

*By AgentKush. Mods and full changelogs: [repo](https://github.com/AgentKush/Icarus-mods) ·
[JimK72's Mod Manager](https://github.com/Jimk72/Icarus_Software)*
