<div align="center">

# Waste Not

[![Version](https://img.shields.io/badge/v2.3.1-Version-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=github&logoColor=white)]()
[![Author](https://img.shields.io/badge/CritFail%20%28Updated%20by%20AgentKush%29-Author-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=steam&logoColor=white)]()
[![Type](https://img.shields.io/badge/EXMOD-Type-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=databricks&logoColor=white)]()
[![Compatibility](https://img.shields.io/badge/All%20DLCs-Compatibility-0d1117?style=for-the-badge&labelColor=1a1e2e&logo=opensourceinitiative&logoColor=white)]()

Mining yields useful secondary resources instead of Stone. Normal ores give bonus of the same type, dense metal ores drop Exotics.

Requires **[JimK72's Icarus Mod Manager](https://github.com/Jimk72/Icarus_Software)**

</div>

---

Better secondary resources from mining in Icarus.

**Author:** CritFail (Updated by AgentKush)  
**Version:** 2.3  

---

## Features

Most mineable deposits now drop something useful as a secondary resource instead of Stone (or nothing). Exotic, Frozen Ore, Research, Limestone and Salt deposits keep their vanilla values. The "Waste Not" talent affects secondary resource drop chance.

### Dense Metal Ores → Exotics
| Deposit | Secondary |
|---------|-----------|
| Gold (Dense) | Exotics |
| Iron (Dense) | Exotics |
| Copper (Dense) | Exotics |
| Bauxite (Dense) | Exotics |
| Lithium (Dense) | Exotics |
| Ruby (Dense) | Exotics |

### Normal Ores → Bonus of Same Type
| Deposit | Secondary |
|---------|-----------|
| Gold (Normal) | Gold Ore |
| Iron (Normal) | Iron Ore |
| Copper (Normal) | Copper Ore |
| Bauxite (Normal) | Bauxite |
| Oxite (Normal) | Oxite |
| Sulfur (Normal) | Sulfur |
| Silica (Normal) | Silica |

### Rare Ores → Exotics
| Deposit | Secondary |
|---------|-----------|
| Titanium (Normal) | Exotics |
| Platinum (Normal) | Exotics |
| Lithium (Normal) | Exotics |
| Ruby (Normal) | Exotics |

### Coal & Ice (Previously No Secondary)
| Deposit | Secondary |
|---------|-----------|
| Coal (Normal) | Charcoal |
| Coal (Dense) | Charcoal |
| Ice (Normal) | Oxite |
| Ice (Dense) | Oxite |

### Other Changes
| Deposit | Secondary |
|---------|-----------|
| Stone (Normal) | Silica |
| Stone (Dense) | Silica |
| Oxite (Dense) | Oxite |
| Sulfur (Dense) | Sulfur |
| Silica (Dense) | Silica |

**Total: 26 deposit types given a new secondary resource** (of the game's 33)

---

## Installation

1. Download `Waste_Not.EXMODZ`
2. Import into Icarus Mod Manager
3. Enable the mod and merge

## Changelog

### v2.3.1 (2026-11-08)
- New icon and banner, drawn from the mod's live data. No gameplay change.

### v2.3
- **Fix**: Dense Stone set the *primary* yield (`ResourceType`) to Silica instead of the secondary. Mod rows merge field by field, so vanilla's Stone secondary survived and dense stone gave Silica first and Stone second - the opposite of this mod's purpose, and the game's main stone deposit stopped yielding stone. It now sets `SecondaryResourceType`, exactly like Normal Stone.
- Removed the `Random_Normal` row: it gave the random-resource deposit a Stone primary that vanilla leaves unset and was not listed anywhere. That deposit is back to vanilla.

### v2.2
- Current release at the time: originally by CritFail, updated by AgentKush for the current game build. Earlier version history was not recorded.

---

<div align="center">

**Made by CritFail (Updated by AgentKush)** · [All Mods](https://github.com/AgentKush/Icarus-mods) · [Report a Bug](https://github.com/AgentKush/Icarus-mods/issues) · [Mod Manager](https://github.com/Jimk72/Icarus_Software)

*All mods are free. If you enjoy them, leave a star on the repo!*

</div>
