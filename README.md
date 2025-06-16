# PyQt5 Roguelike Game

A classic roguelike dungeon crawler built with pygame for the game engine and PyQt5 for the GUI interface.

## New Features

- **Key repeat functionality**: Hold down movement keys to continuously move in that direction
- **Improved stair controls**: Use 'd' to go down stairs and 'a' to go up stairs
- **Responsive layout**: Automatically adjusts to your screen size
- **Centered interface**: Uses 80% of screen space for optimal visibility

### Level Progression System
- **Infinite dungeon levels** with increasing difficulty
- **Themed environments** that change every few levels:
  - Surface Caves (Levels 1-4)
  - Underground Tunnels (Levels 5-9)
  - Ancient Crypts (Levels 10-14)
  - Molten Depths (Levels 15-19)
  - Crystal Caverns (Levels 20-24)
  - Shadow Realm (Levels 25-29)
  - Dragon's Lair (Levels 30-49)
  - Abyss Gates (Levels 50+)

### Special Level Features
- **Boss Rooms** (Every 10th level) - Powerful enemies with greater rewards
- **Treasure Rooms** (Every 7th level) - Extra gold and items
- **Magic Portals** (Every 5th level from level 5) - Skip 5 levels ahead
- **Rest Areas** (Every 15th level) - Safe zones for planning

### Enemy Types
- **Giant Rats** (Level 1-2): Weak but numerous
- **Goblins** (Level 1-5): Basic humanoid enemies  
- **Orcs** (Level 3-8): Stronger warriors
- **Trolls** (Level 6-10): Tough regenerating enemies
- **Dragons** (Level 9+): Powerful boss-level creatures
- **Boss Variants** - Enhanced versions with 2.5x HP and increased rewards

### Items & Rewards
- **Health Potions**: Restore HP (scales with level)
- **Gold**: Currency that increases in value with depth
- **Treasure Rooms**: Special high-value loot areas
- **Scaling Rewards**: Items become more valuable at deeper levels

### GUI Features
- **Real-time stats display**: HP, Level, XP, Gold, Playtime
- **Level progression tracking**: Current level and deepest reached
- **Message log**: Combat and game events with atmospheric descriptions
- **Save/Load system**: Complete game state persistence
- **Control reference**: Built-in help
- **Dark theme**: Easy on the eyes
- **Responsive layout**: Clean, organized interface
- **Menu system**: Easy access to game functions

## Installation

1. **Install dependencies**:
   ```bash
   ./setup.sh
   ```
   Or manually:
   ```bash
   pip3 install pygame PyQt5
   ```

2. **Run the game**:
   ```bash
   python3 main_gui.py
   ```

## Controls

### Movement
- **Arrow Keys** or **hjkl**: Move in cardinal directions
- **yubn**: Diagonal movement (roguelike standard)

### Actions
- **. (period)**: Wait/Rest (skip turn)
- **, (comma)**: Pick up item
- **d**: Go down stairs
- **a**: Go up stairs
- **p**: Use magic portal (when available)
- **Ctrl+S**: Quick save
- **Ctrl+L**: Load game
- **Ctrl+N**: New game

### GUI
- **New Game**: Restart with a fresh character
- **Save Game**: Save current progress
- **Load Game**: Load a previously saved game
- **Quit**: Exit the game

## Game Mechanics

### Combat
- **Turn-based**: Player moves, then all enemies move
- **Melee combat**: Move into an enemy to attack
- **Damage calculation**: Attack - Defense (minimum 1)
- **Death**: Game over when player HP reaches 0
- **Boss encounters**: Special powerful enemies every 10 levels

### Character Progression
- **Experience**: Gained by defeating enemies
- **Leveling**: Increases HP, attack, and defense
- **Scaling**: Higher level enemies give more XP
- **Boss rewards**: Triple XP from boss enemies

### Level Generation & Progression
- **Guaranteed exits**: Every level has at least one way to progress
- **Multiple exit types**:
  - Stairs down (standard progression)
  - Stairs up (return to previous levels)
  - Magic portals (skip 5 levels ahead)
- **Procedural rooms**: Each level is randomly generated
- **Connected layout**: Rooms linked by corridors
- **Increasing difficulty**: Deeper levels have stronger enemies
- **Thematic progression**: Environment changes based on depth

### Field of View
- **Line of sight**: Can only see what's directly visible
- **Exploration**: Areas remain visible once explored
- **Tactical gameplay**: Use walls and corners strategically

## File Structure

- `main_gui.py`: Main application and PyQt5 GUI
- `game_engine.py`: Core game logic and pygame integration
- `game_entities.py`: Player, enemies, and items
- `game_map.py`: Dungeon generation and map handling
- `level_manager.py`: Level progression and special features
- `save_manager.py`: Save/Load game state management
- `save_load_dialog.py`: GUI dialogs for save/load operations
- `requirements.txt`: Python dependencies
- `setup.sh`: Installation script

## Technical Details

### Architecture
- **Pygame**: Handles game rendering and input
- **PyQt5**: Provides GUI framework and widgets
- **Modular design**: Separate concerns for maintainability
- **Level Manager**: Handles progression, themes, and special features

### Performance
- **Efficient rendering**: Only updates when needed
- **Smart FOV**: Optimized line-of-sight calculations
- **Memory management**: Proper cleanup and resource handling
- **Level caching**: Optimized level generation

## Advanced Features

### Level Progression
- **Infinite depth**: No level cap - see how deep you can go
- **Difficulty scaling**: Enemies become progressively stronger
- **Reward scaling**: Better loot at deeper levels
- **Progress tracking**: Game remembers your deepest level reached

### Special Encounters
- **Boss fights**: Every 10th level features powerful boss enemies
- **Treasure hunting**: Special rooms with enhanced loot
- **Portal magic**: Rapid progression through portal jumps
- **Environmental storytelling**: Each theme has unique descriptions

## Tips for Playing

1. **Explore systematically**: Check every room for items and exits
2. **Manage resources**: Health potions become more valuable at deeper levels
3. **Fight strategically**: Don't rush into groups, especially boss rooms
4. **Level progression**: Fight enemies to grow stronger before descending
5. **Use portals wisely**: Magic portals can help you skip difficult sections
6. **Track your progress**: Remember your deepest level for bragging rights
7. **Boss preparation**: Every 10th level has boss enemies - be ready!
8. **Treasure hunting**: Look for treasure rooms every 7 levels

## Victory Conditions

- **Escape**: Return to level 1 and use the up stairs to escape
- **Depth Challenge**: See how deep you can venture into the abyss
- **Boss Hunter**: Defeat boss enemies for maximum XP and rewards
- **Treasure Seeker**: Accumulate wealth from treasure rooms

Enjoy your infinite dungeon crawling adventure!
