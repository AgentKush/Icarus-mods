# Culinex Food Boost Fix

![Version](https://img.shields.io/badge/version-1.0-blue)
![Author](https://img.shields.io/badge/author-AgentKush-green)
![Compatibility](https://img.shields.io/badge/compatibility-All%20DLCs-brightgreen)

## Overview

Fixes the Chef's Backpack (Culinex) 25% food effectiveness boost to work on ALL cooked foods. Also adds a butchery recipe to convert raw meat into raw chicken.

## The Problem

The Chef's Backpack grants `BaseCookedFoodModifierEffectiveness_+%: 25` but many food items in the game are missing the corresponding `CookedFoodModifierEffectiveness_+%` affector in their modifier data. This means foods like cakes, pies, and many other dishes don't receive the 25% effectiveness boost they should.

## The Fix

This mod adds the `CookedFoodModifierEffectiveness_+%` affector to **158 food modifiers**, ensuring all cooked foods properly benefit from the Chef's Backpack bonus.

## Features

### Food Boost Fix

| Category | Foods Fixed |
|----------|-------------|
| Cakes | Chocolate, Carrot, Coconut Cake Pieces |
| Pies | Meat, Fruit, Vegetable, Pumpkin, Shepherds, Fish Fillet |
| Meats | All cooked, dried, and smoked meats |
| Fish | All cooked, grilled, fried, and dried fish |
| Vegetables | All cooked vegetables and salads |
| Soups | Corn, Mushroom, Tomato, French Onion |
| Breads | All bread types, flatbread, rolls |
| Desserts | Cookies, pastries, pavlova, sorbets |
| Alcohol | Beer, Wine, Mead, Vodka, Tequila |

### Bonus: Raw Chicken Recipe

New butchery bench recipe:
- **Input:** 1x Raw Meat
- **Output:** 2x Raw Chicken
- **Stations:** Butchery Bench, Advanced Butchery Bench

## Technical Specifications

| Metric | Value |
|--------|-------|
| Food Modifiers Fixed | 158 |
| New Recipes Added | 1 |
| Effectiveness Boost | +25% (with Chef's Backpack) |

### Files Modified
- `Modifiers-D_ModifierStates.json` (158 entries)
- `Processors-D_ProcessorRecipes.json` (1 entry)

## Installation

1. Download the `.EXMODZ` file from this repository
2. Open JimK72's Icarus Mod Manager
3. Import the mod file
4. Enable and launch Icarus

## Gameplay Notes

- Requires the Chef's Backpack to be equipped for the boost
- The 25% boost applies to food buff effectiveness (stats granted)
- Combines with the existing duration boost from the backpack
- Raw chicken recipe provides an alternative source of chicken meat

## Compatibility

| Mod | Status |
|-----|--------|
| All AgentKush mods | ✅ Compatible |
| Other D_ModifierStates mods | ⚠️ May conflict if modifying same foods |
| Modular Buff Enhancer | ✅ Stacks with buff enhancements |

## Version History

| Version | Changes |
|---------|---------|
| 1.0 | Initial release - 158 foods fixed, raw chicken recipe added |

---

*Part of the [AgentKush Icarus Mods](https://github.com/AgentKush/Icarus-mods) collection*
