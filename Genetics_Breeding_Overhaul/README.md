<div align="center">

# Genetics & Breeding Overhaul

[![Version](https://img.shields.io/badge/v1.0.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/AgentKush-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/Homestead%20DLC-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Makes the **Mendel genetics & selective-breeding** system (Week 220 / Homestead) far less grindy — higher mutation rates, more twins, faster breeding, and better odds at the bloodlines worth chasing.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)** and the genetics talent tree.

</div>

---

## Features

All values come from the in-game **Genetics talent tree** — this mod doubles the rewards those talents grant, so every point you spend goes twice as far:

- **2x genotype mutation** — `Genetics_GenotypeMutation` line (now up to +70% mutation chance fully specced) for faster stat-point gains.
- **2x phenotype mutation** — `Genetics_PhenotypeMutation` line, for rarer cosmetics/colours.
- **2x twin births** — `Genetics_Twins` (now up to +60%), doubling your offspring per pregnancy.
- **2x faster gestation & recovery** — `Genetics_GestationSpeed` and `Genetics_RecoverySpeed`.
- **2x lineage mutation** — `Genetics_Lineage`, for faster bloodline shifts.
- **2x better wild stock** — `Genetics_WildGenome` / `WildBloodline` / `WildPhenome`, so wild-caught creatures start with better genes.

Plus a **bloodline rarity rebalance** so selective breeding actually pays off:

- **Wild** bloodline weighting `300 -> 75` — the plain baseline shows up far less, so trait bloodlines appear more often.
- **Alpha** bloodline weighting `10 -> 25` — the prestige `+20% size` bloodline is rare but now actually achievable.

## What it does NOT change

No base creature combat stats and no genotype value curves — so it layers cleanly with **Taming & Tames Overhaul**, **Creature Difficulty Scaling**, and **Hardcore Rebalance Pack**.

## Files Modified

- `Talents-D_Talents` (11 genetics talents — boosted rewards)
- `AI-D_GeneticLineages` (2 entries — Wild + Alpha rarity)

## Version History

- **v1.0.1** - New icon and banner, drawn from the mod's live data. No gameplay change.
- **v1.0** - Initial release. 2x genetics talent rewards (mutation / twins / gestation / recovery / lineage / wild genetics) + bloodline rarity rebalance.

---

<div align="center">

**Made by AgentKush** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
