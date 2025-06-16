# Quick Start Guide - PyQt5 Roguelike

## 🚀 Getting Started

### 1. Run the Game
```bash
cd /home/rooty/q
python3 main_gui.py
```

### 2. Basic Controls
- **Move**: Arrow keys or `hjkl` (vi-style)
- **Diagonal**: `yubn` keys
- **Attack**: Move into enemies
- **Pick up**: `,` (comma) when on items
- **Stairs down**: `>` 
- **Stairs up**: `<`
- **Magic portal**: `p` (when available)
- **Wait/Rest**: `.` (period)
- **Quick save**: `Ctrl+S`
- **Load game**: `Ctrl+L`
- **New game**: `Ctrl+N`

## 🎯 Game Objectives

### Primary Goals
1. **Survive** - Don't let your HP reach 0
2. **Explore** - Find stairs to progress deeper
3. **Level up** - Fight enemies to gain XP
4. **Collect treasure** - Gold and health potions

### Victory Conditions
- **Escape**: Return to level 1 and go up stairs
- **Depth Challenge**: See how deep you can go
- **High Score**: Accumulate XP, gold, and reach max depth

## 🗺️ Level Progression

### Guaranteed Exits
- **Every level has at least one exit**
- **Stairs down**: Progress to next level
- **Stairs up**: Return to previous level (if not level 1)
- **Magic portals**: Skip 5 levels ahead (every 5th level)

### Level Themes
- **Levels 1-4**: Surface Caves
- **Levels 5-9**: Underground Tunnels
- **Levels 10-14**: Ancient Crypts
- **Levels 15-19**: Molten Depths
- **Levels 20-24**: Crystal Caverns
- **Levels 25-29**: Shadow Realm
- **Levels 30-49**: Dragon's Lair
- **Levels 50+**: Abyss Gates

### Special Features
- **Boss Rooms** (Every 10th level): Powerful enemies, great rewards
- **Treasure Rooms** (Every 7th level): Extra gold and items
- **Magic Portals** (Every 5th level): Fast travel deeper
- **Rest Areas** (Every 15th level): Safe planning zones

## ⚔️ Combat Tips

### Basic Combat
- Move into enemies to attack
- Damage = Your Attack - Enemy Defense (minimum 1)
- Turn-based: You move, then all enemies move

### Strategy
1. **Use walls** - Fight enemies one at a time in corridors
2. **Manage HP** - Use health potions when needed
3. **Level up** - Fight weaker enemies before going deeper
4. **Boss preparation** - Stock up on potions before level 10, 20, etc.

## 📊 Character Progression

### Stats
- **HP**: Health points - don't let this reach 0!
- **Level**: Character level - increases all stats
- **XP**: Experience points - fight enemies to gain
- **Gold**: Currency - collect from defeated enemies and treasure

### Leveling Up
- Gain XP by defeating enemies
- Level up increases HP, Attack, and Defense
- Higher level enemies give more XP
- Boss enemies give triple XP

## 💾 Save & Load System

### Saving Your Game
- **Quick Save**: Press `Ctrl+S` during gameplay
- **Save Menu**: Click "Save Game" button or use Game → Save Game
- **Multiple Saves**: Create multiple save files with custom names
- **Character Names**: Give your hero a custom name

### Loading Games
- **Load Menu**: Click "Load Game" button or use Game → Load Game
- **Save Browser**: View all saved games with details
- **Save Details**: See character level, dungeon depth, gold, playtime
- **Delete Saves**: Remove unwanted save files

### Save Information
Each save file contains:
- Character name and stats
- Current dungeon level and position
- Inventory and gold
- Game progress and achievements
- Total playtime
- Complete level state (enemies, items, map)

## 🎮 GUI Features

### Stats Panel
- Real-time HP, Level, XP display
- Current dungeon level
- Deepest level reached
- Gold counter
- Playtime tracker

### Message Log
- Combat results
- Level descriptions
- Special event notifications
- Atmospheric flavor text

### Controls Reference
- Built-in control help
- Legend for game symbols
- New Game, Save, Load, and Quit buttons
- Menu system with keyboard shortcuts

## 🏆 Pro Tips

1. **Explore systematically** - Check every room for items and exits
2. **Resource management** - Save health potions for tough fights
3. **Strategic retreat** - Use stairs to escape if overwhelmed
4. **Portal timing** - Use magic portals to skip difficult sections
5. **Boss preparation** - Every 10th level has boss enemies
6. **Treasure hunting** - Look for special rooms every 7 levels
7. **Progress tracking** - Game remembers your deepest level
8. **Save frequently** - Use Ctrl+S to save your progress
9. **Multiple saves** - Keep backup saves for different strategies

## 🐛 Troubleshooting

### Game Won't Start
```bash
# Install dependencies
./setup.sh

# Or manually
pip3 install pygame PyQt5
```

### Performance Issues
- The Qt warnings are normal and don't affect gameplay
- Game runs at 20 FPS for smooth turn-based play

## 🎯 Challenge Modes

### Speedrun
- How fast can you reach level 10?
- Use portals for rapid progression

### Survival
- How deep can you go?
- Focus on leveling up and resource management

### Treasure Hunter
- Maximize gold collection
- Hit every treasure room (levels 7, 14, 21, etc.)

### Boss Hunter
- Defeat all boss enemies
- Levels 10, 20, 30, 40, 50...

---

**Have fun exploring the infinite dungeon!** 🗡️⚔️
