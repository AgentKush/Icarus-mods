<div align="center">

# Resource Repacker

[![Version](https://img.shields.io/badge/v1.4-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Pack raw resources back into unopened UDA kits so they can be shipped to space and redeployed at another base. **Neutral conversion ratios** — recipes cost exactly what the kit gives back when opened, so this is purely a logistics mod, not a duplication exploit. Available at **30 crafting stations plus handcrafting (player Character)**.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

## Why

Repacks raw resources back into the standard UDA kit format. Useful for **cutting carry weight** — 100 Titanium Ore weighs 40,000, the kit weighs 10,000, so it's 4× lighter for the same resources — and for **sharing kits with teammates on the same drop**. Note that kits are `MaxStack 1` in vanilla, so repacking does not save inventory slots.

> **⚠ Known limitation: orbital sender currently rejects crafted kits.** The game's "send to orbit" check apparently does more than tag-matching — workshop-purchased kits go up fine, but freshly crafted ones get routed to a surplus overflow bag with the message *"Some items weren't able to be returned."* The kits are valid items in every other respect (display, decay, stacking, consume-to-open all work). I'm investigating a Blueprint-side workaround for a future release. Until then, treat this mod as **inventory consolidation + teammate sharing**, not orbital logistics.

## Features

- **20 repack recipes** — one per vanilla resource kit that still has item data, including 5 DLC kits
- **Available everywhere** — every crafting bench, plus handcrafting in your inventory (Character recipe set)
- **Neutral ratios** — the recipe input matches the kit's vanilla yield (e.g. 100 Titanium_Ore → 1 Titanium kit). No duping.
- **Vanilla stack sizes** — recipe quantities exactly match base-game kit yields, regardless of any stack-size mods you have running
- Pure data-table mod — no PAK file required

## Repack Recipes

### Basic Resources

| Kit | Cost |
|-----|------|
| Wood Kit | 250 Wood |
| Stone Kit | 250 Stone |
| Dirt Kit | 50 Dirt |
| Limestone Kit | 100 Limestone |
| Sulfur Kit | 100 Sulfur |
| Oxite Kit | 100 Oxite |
| Silica Kit | 100 Silica |
| Clay Kit | 100 Clay |

### Metal Ores

| Kit | Cost |
|-----|------|
| Iron Kit | 100 Iron Ore (Metal_Ore) |
| Copper Kit | 100 Copper Ore |
| Aluminium Kit | 100 Bauxite |
| Gold Kit | 100 Gold Ore |
| Platinum Kit | 100 Platinum Ore |
| Titanium Kit | 100 Titanium Ore |
| Lithium Kit | 100 Lithium Ore |

### Advanced / Exotic

| Kit | Cost |
|-----|------|
| Scoria Kit | 100 Scoria |
| Obsidian Kit | 100 Obsidian |
| Synthetic Enzymes Kit | 100 Synthetic Enzymes |

### DLC — Dangerous Horizons

| Kit | Cost |
|-----|------|
| Ruby Kit | 50 Ruby Ore |
| Limestone Kit | 100 Limestone |
| Lithium Kit | 100 Lithium Ore |

### DLC — New Frontiers

| Kit | Cost |
|-----|------|
| Clay Kit | 100 Clay |
| Scoria Kit | 100 Scoria |
| Obsidian Kit | 100 Obsidian |

> **DLC note:** all five of these are feature-gated via `Metadata.RequiredFeatureLevel`, so on a base-game install they don't register at all — no broken-icon recipes, no failed crafts. The other 15 work for everyone. Before v1.5, only Ruby was gated; Limestone, Lithium, Clay, Scoria and Obsidian registered on base-game installs and pointed at items that build strips out.
>
> **Removed in v1.5:** the Uranium Rod and Ren kits. The Sept-2026 game update deleted their `D_ItemsStatic` rows, so the kit those recipes produced has no mesh, icon or use. Vanilla's own workshop entries for them are broken the same way — nothing a mod can repair.

## Available At

30 crafting stations plus your inventory (handcrafting):

- **Handcrafting** — `Character` (player inventory)
- **Tier 1+** — Crafting Bench, Anvil Bench (T1/T3/T4), Armor Bench (+ Advanced / Electric)
- **Tier 2+** — Carpentry Bench (T1/T4), Masonry Bench (T1/T3/T4), Machining Bench
- **Late game** — Fabricator, Manufacturer
- **Specialty** — Alteration Bench (+ Advanced), Chemistry, Glassworking, Herbalism, Medicine, Animal, Butchery (+ Advanced), Kitchen (+ Advanced), Trophy, Rustic Decorations, Fishing Bench

30 recipe sets in total. Not included: Skinning Bench, Mortar and Pestle, Cement Mixer, Material Processor, Cleaning Device, Seed Extractor, Exotic Processor, and the Fishing Bench's rod-crafting set.

## Notes

- **Custom stack sizes:** the recipe input quantity matches the *vanilla* kit yield. If you run a stack-size mod (Stack_Size_Overhaul, etc.), the input cost still reflects the base kit yield, so a single repack always produces one base-stack-density kit.
- **Recipe row names use the kit name directly** (e.g. `Meta_Resource_Pack_Titanium`). No collision with vanilla recipes — these names aren't used as recipes in base game, only as workshop items.
- **Power cost** is modest (2,000–8,000 mJ). Handcrafting is power-free.

## Installation

1. Download `Resource_Repacker.EXMODZ`
2. Import into **Icarus Mod Manager** (JimK72's IMM)
3. Enable and merge mods as usual

## Changelog

### v1.4
- **Fix**: all 21 recipes crafted silently. They set `Audio` to a `D_CraftingAudioData` row called `Fabricator`, but that table has no such row — `Fabricator` is a **`D_RecipeSets`** name, and the two tables use different keys. With the reference dangling the game played no craft-completed sound, which reads like a failed craft even though the kit was produced. Now set to `Default`, which has a real `RecipeCraftedSound`, so repacking finishes with the generic craft-complete sound at every station and in handcrafting instead of silence. (`Default`'s `ProcessorOverrideSounds` map has only one entry, for the Carpentry Bench — genuinely per-bench audio would need a separate recipe row per bench, since `Audio` is a single row reference.)
- Fixed the same hardcoded value in `build_mod.py` so a rebuild can't reintroduce it.

### v1.3
- Removed the v1.2 `D_Itemable` tooltip override on the three DLC kits; the DLC requirement is documented in this README instead. *(Corrected in v1.5: this entry used to say EXMOD merges replace whole rows and that the override was wiping DisplayName and Icon. Neither is true — EXMOD rows merge per property, and the v1.2 override set the same icon paths vanilla uses. The override was unnecessary, but it was not the cause of any icon problem.)*
- **Docs**: explicitly flagged the orbital-sender limitation in the README (was previously buried in a "known issue" section).

### v1.2
- Feature-gated the 3 DLC recipes (Ruby / Uranium Rod / Ren) using `Metadata.RequiredFeatureLevel: DangerousHorizons` — they don't register on non-DLC installs.
- Added a DLC requirement note to each DLC kit's tooltip *(removed in v1.3 — see above)*.

### v1.1
- Added 3 DLC kit recipes (Ruby, Uranium Rod, Ren) — require Dangerous Horizons
- Exposed every recipe at all player crafting benches plus handcrafting (Character)

### v1.0
- Initial release
- 18 repack recipes covering Basic / Metal / Exotic resource kits
- Neutral 1:1 input/yield ratios

---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
