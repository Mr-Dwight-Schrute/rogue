# Save & Load System Guide

## 💾 Overview

The PyQt5 Roguelike game features a comprehensive save and load system that preserves your entire game state, allowing you to continue your adventure exactly where you left off.

## 🎮 How to Save Your Game

### Quick Save (Recommended)
- **Keyboard**: Press `Ctrl+S` during gameplay
- **Result**: Instantly saves your game as "quicksave.json"
- **Use Case**: Quick saves during exploration

### Custom Save
1. Click **"Save Game"** button or use **Game → Save Game** menu
2. Enter a custom save name in the dialog
3. Optionally change your character name
4. Click **"Save"** to confirm
5. **Result**: Creates a named save file you can easily identify

## 📂 How to Load Your Game

### Load Game Dialog
1. Click **"Load Game"** button or use **Game → Load Game** menu
2. Browse through your saved games in the list
3. Click on a save to see detailed information
4. Click **"Load"** to restore that game state
5. **Result**: Game continues from the exact saved state

### Save File Information
Each save file shows:
- **Character Name**: Your hero's name
- **Character Level**: Current player level
- **Dungeon Level**: How deep you've ventured
- **Deepest Level**: Maximum depth reached
- **Gold**: Current wealth
- **Save Date**: When the game was saved
- **Playtime**: Total time played

## 🗂️ Save File Management

### Multiple Saves
- Create as many save files as you want
- Use descriptive names like "Before Boss Fight" or "Level 20 Run"
- Keep backup saves for different strategies

### Deleting Saves
1. Open the **Load Game** dialog
2. Select the save file you want to delete
3. Click **"Delete"** button
4. Confirm the deletion
5. **Result**: Save file is permanently removed

### Save File Location
- Saves are stored in the `saves/` directory
- Files are in JSON format for reliability
- Each save is completely self-contained

## 💡 What Gets Saved

### Complete Game State
- **Player Stats**: HP, Level, XP, Attack, Defense, Gold
- **Player Position**: Exact location in the dungeon
- **Inventory**: All items carried by the player
- **Current Level**: Complete dungeon layout, enemies, items
- **Game Progress**: Dungeon level, deepest level reached
- **Game Messages**: Recent message history
- **Playtime**: Total time spent playing

### Level State Preservation
- **Map Layout**: Every room, corridor, and wall
- **Enemy Positions**: Location and health of all enemies
- **Item Locations**: All treasure, potions, and gold
- **Stairs & Portals**: Exit locations preserved
- **Exploration**: Which areas you've already seen
- **Field of View**: Current visibility state

## 🎯 Save Strategy Tips

### When to Save
1. **Before Boss Fights**: Save before every 10th level
2. **After Major Progress**: When you reach a new depth record
3. **Before Risky Moves**: When low on health or resources
4. **Regular Intervals**: Every 15-30 minutes of play
5. **Before Portals**: Save before using magic portals

### Save Naming Conventions
- `"Level_10_Boss"` - Before boss encounters
- `"Depth_25_Record"` - New depth records
- `"Full_Health_L15"` - Good states to return to
- `"Portal_Ready"` - Before using magic portals
- `"Treasure_Hunt"` - Before treasure room levels

### Multiple Save Strategy
- **Main Save**: Your primary progression save
- **Backup Save**: Safety save from a few levels back
- **Experiment Save**: For trying risky strategies
- **Achievement Save**: Before attempting specific goals

## 🔧 Technical Details

### Save File Format
- **Format**: JSON (human-readable text)
- **Size**: Typically 500KB - 1MB per save
- **Compatibility**: Forward and backward compatible
- **Reliability**: Includes error checking and validation

### Performance
- **Save Speed**: Instant (< 1 second)
- **Load Speed**: Very fast (< 2 seconds)
- **Storage**: Minimal disk space usage
- **Memory**: Efficient memory management

### Error Handling
- **Corruption Protection**: Validates save files before loading
- **Backup Creation**: Temporary backups during save operations
- **Error Messages**: Clear feedback if save/load fails
- **Recovery**: Graceful handling of damaged save files

## 🚨 Important Notes

### Save File Safety
- **Backup Important Saves**: Copy save files to another location
- **Don't Edit Manually**: Save files are complex - use the game interface
- **Regular Cleanup**: Delete old saves you no longer need
- **Version Compatibility**: Saves work across game updates

### Limitations
- **One Level Only**: Only current level is saved (not entire dungeon history)
- **No Multiplayer**: Saves are single-player only
- **Platform Specific**: Save files are tied to your system
- **Game Version**: Best compatibility with same game version

## 🎮 Quick Reference

### Keyboard Shortcuts
- `Ctrl+S` - Quick Save
- `Ctrl+L` - Load Game
- `Ctrl+N` - New Game (with save warning)
- `Ctrl+Q` - Quit Game

### Menu Options
- **Game → Save Game** - Custom save dialog
- **Game → Load Game** - Load game dialog
- **Game → New Game** - Start fresh (with save warning)

### Save Dialog Controls
- **Double-click** save file to load quickly
- **Delete** button to remove unwanted saves
- **Refresh** button to update save list
- **Details** panel shows save information

---

**Remember**: Your adventure is valuable - save often and keep backups! 🗡️⚔️
