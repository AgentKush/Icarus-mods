# Turret Variants Mod

**Version:** 2.3  
**Author:** AgentKush  
**Compatible with:** Icarus (JimK72's Mod Manager)

## Description

This mod adds **15 new automated turret variants** to Icarus, each with unique characteristics, firing patterns, and ammo types to fit any defensive strategy.

## All Turrets Overview

| Turret | Ammo | Range | Burst | Cooldown | Role |
|--------|------|-------|-------|----------|------|
| **Rock Thrower** | Pistol | 40m | 1 | 2.0s | Budget defense |
| **Bow** | Pistol | 60m | 1 | 2.0s | Primitive option |
| **Crossbow** | Pistol | 55m | 1 | 2.5s | Silent defense |
| **Rapid Crossbow** | Pistol | 45m | 3 | 1.5s | Silent burst fire |
| **Pistol** | Pistol | 40m | 3 | 1.2s | Cheap & fast |
| **SMG** | Pistol | 35m | 8 | 1.0s | Close quarters |
| **Assault Rifle** | Rifle | 50m | 5 | 1.5s | All-rounder |
| **Storm** | Rifle | 40m | 12 | 1.8s | Rapid suppression |
| **Minigun** | Rifle | 45m | 20 | 2.0s | Maximum dakka |
| **Rifle** | Rifle | 75m | 3 | 2.5s | Precision burst |
| **Javelin** | Rifle | 70m | 1 | 4.0s | High damage |
| **Shotblaster** | Shotgun | 25m | 2 | 2.5s | Close devastation |
| **Flamethrower** | Shotgun | 15m | 40 | 2.0s | Area denial |
| **Sniper** | Rifle | 100m | 1 | 6.0s | Long range |
| **Heavy Sniper** | Rifle | 150m | 1 | 10.0s | Extreme range |

---

## Turret Categories

### Budget/Early Game
| Turret | Cost Tier | Best For |
|--------|-----------|----------|
| Rock Thrower | Steel | Cheap pistol ammo |
| Bow | Steel | Use excess arrows |
| Pistol | Steel | Affordable pistol ammo |

### Mid Game
| Turret | Cost Tier | Best For |
|--------|-----------|----------|
| Crossbow | Steel | Silent kills |
| Rapid Crossbow | Steel | Silent burst damage |
| SMG | Steel | Door/choke defense |
| Assault Rifle | Titanium | Balanced defense |
| Shotblaster | Titanium | Close range obliteration |

### Late Game
| Turret | Cost Tier | Best For |
|--------|-----------|----------|
| Rifle | Titanium | Precision long range |
| Javelin | Titanium | High damage single targets |
| Storm | Titanium | Swarm suppression |
| Minigun | Titanium | Maximum firepower |
| Flamethrower | Titanium | Area denial |
| Sniper | Titanium | Long range elimination |
| Heavy Sniper | Titanium | Extreme range picks |

---

## Crafting Requirements

All turrets require the **Pistol Turret blueprint** to be unlocked first.

### Steel-Tier Turrets
| Turret | Materials |
|--------|-----------|
| **Rock Thrower** | 30 Steel Ingot, 10 Electronics, 15 Stick, 10 Rope |
| **Bow** | 30 Steel Ingot, 15 Electronics, 20 Stick, 10 Rope |
| **Crossbow** | 40 Steel Ingot, 20 Electronics, 10 Carbon Fiber, 8 Epoxy |
| **Rapid Crossbow** | 45 Steel Ingot, 25 Electronics, 15 Carbon Fiber, 12 Epoxy |
| **Pistol** | 30 Steel Ingot, 15 Electronics, 5 Carbon Fiber, 10 Steel Screw |
| **SMG** | 35 Steel Ingot, 20 Electronics, 8 Carbon Fiber, 15 Steel Screw |

### Titanium-Tier Turrets
| Turret | Materials |
|--------|-----------|
| **Javelin** | 35 Titanium Ingot, 20 Electronics, 25 Stick, 15 Rope |
| **Assault Rifle** | 40 Titanium Ingot, 25 Electronics, 15 Carbon Fiber, 20 Steel Screw |
| **Rifle** | 45 Titanium Ingot, 25 Electronics, 15 Carbon Fiber, 5 Glass |
| **Storm** | 50 Titanium Ingot, 35 Electronics, 20 Carbon Fiber, 25 Steel Screw |
| **Minigun** | 60 Titanium Ingot, 40 Electronics, 25 Carbon Fiber, 30 Steel Screw |
| **Sniper** | 50 Titanium Ingot, 30 Electronics, 20 Carbon Fiber, 10 Glass |
| **Heavy Sniper** | 70 Titanium Ingot, 45 Electronics, 30 Carbon Fiber, 15 Glass |
| **Shotblaster** | 40 Titanium Ingot, 20 Electronics, 25 Steel Ingot, 15 Steel Screw |
| **Flamethrower** | 45 Titanium Ingot, 25 Electronics, 30 Steel Ingot, 20 Composites |

---

## Tactical Combinations

### Perimeter Defense
- **Outer Ring:** Heavy Sniper + Sniper (pick off distant threats)
- **Mid Ring:** Rifle + Assault Rifle (suppress approaching enemies)
- **Inner Ring:** Shotblaster + Flamethrower (last line devastation)

### Choke Point Defense
- **SMG + Storm** - Wall of bullets at doorways
- **Shotblaster** - Nothing gets through

### Silent Base
- **Crossbow + Rapid Crossbow** - Silent kills, no attention drawn

### Budget Defense Network
- **Rock Thrower + Bow + Pistol** - All cheap ammo options

---

## Installation

1. Download `Turret_Variants.EXMODZ`
2. Place in Icarus Mod Manager's mods folder
3. Enable in Mod Manager
4. Launch Icarus

## Changelog

### Version 2.3
- Fixed broken recipes with invalid ingredient names:
  - `Refined_Wood` → `Stick` (Bow, Javelin, Rock turrets)
  - `Rubber` → `Composites` (Flamethrower turret)
  - `Iron_Ingot` → `Steel_Ingot` (Rock turret)

### Version 2.2
- Tightened targeting parameters to reduce wasted shots on obscured targets
- Reduced `PermitBeginFireAngle` across all turrets for more precise aiming
- Reduced `CheckTargetPeriod` for faster target re-evaluation

### Version 2.1
- Technical improvements to turret data structure

### Version 1.2
- Added Rifle Turret (7.62mm, 3-round precision bursts)
- Added Pistol Turret (9mm, fast tracking, wide arc)
- Added Shotblaster Turret (double-barrel devastation)
- Added Rapid Crossbow Turret (silent 3-bolt bursts)
- Added Storm Turret (12-round rapid fire)
- Added Heavy Sniper Turret (15,000m range!)

### Version 1.1
- Added SMG, Javelin, Flamethrower, Rock, Minigun turrets

### Version 1.0
- Initial release with Crossbow, Bow, Sniper, Assault Rifle turrets

---

## Known Limitations

- Turrets use base game blueprints (BP_Pistol_Turret, BP_Rifle_Turret, BP_Shotgun_Turret) which means:
  - Line-of-sight validation is handled by the blueprint, not data tables
  - Targeting behavior (hostile creatures only) is blueprint-controlled
- These are cosmetic/balance mods only - full AI behavior changes require Unreal Engine blueprint modifications
