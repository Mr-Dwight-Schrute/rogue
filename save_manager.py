import json
import os
import pickle
from datetime import datetime
from game_entities import Player, Enemy, Item, ENEMY_TYPES, ITEM_TYPES

class SaveManager:
    def __init__(self):
        self.save_directory = "saves"
        self.ensure_save_directory()
    
    def ensure_save_directory(self):
        """Create saves directory if it doesn't exist"""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    def get_save_files(self):
        """Get list of available save files"""
        save_files = []
        if os.path.exists(self.save_directory):
            for filename in os.listdir(self.save_directory):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.save_directory, filename)
                    try:
                        with open(filepath, 'r') as f:
                            save_data = json.load(f)
                            save_info = {
                                'filename': filename,
                                'filepath': filepath,
                                'character_name': save_data.get('character_name', 'Unknown'),
                                'level': save_data.get('player_level', 1),
                                'dungeon_level': save_data.get('dungeon_level', 1),
                                'max_dungeon_level': save_data.get('max_dungeon_level', 1),
                                'gold': save_data.get('player_gold', 0),
                                'timestamp': save_data.get('timestamp', 'Unknown'),
                                'playtime': save_data.get('playtime', 0)
                            }
                            save_files.append(save_info)
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        # Sort by timestamp (newest first)
        save_files.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return save_files
    
    def save_game(self, game_engine, character_name="Hero", slot_name=None):
        """Save the current game state"""
        if slot_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            slot_name = f"save_{timestamp}.json"
        
        if not slot_name.endswith('.json'):
            slot_name += '.json'
        
        save_data = {
            'version': '1.0',
            'timestamp': datetime.now().isoformat(),
            'character_name': character_name,
            'playtime': getattr(game_engine, 'playtime', 0),
            
            # Player data
            'player_x': game_engine.player.x,
            'player_y': game_engine.player.y,
            'player_hp': game_engine.player.hp,
            'player_max_hp': game_engine.player.max_hp,
            'player_level': game_engine.player.level,
            'player_exp': game_engine.player.exp,
            'player_exp_to_next': game_engine.player.exp_to_next,
            'player_attack': game_engine.player.attack,
            'player_defense': game_engine.player.defense,
            'player_gold': game_engine.player.gold,
            'player_inventory': [self._serialize_item(item) for item in game_engine.player.inventory],
            
            # Game state
            'dungeon_level': game_engine.dungeon_level,
            'max_dungeon_level': game_engine.player.max_dungeon_level_reached,
            'game_state': game_engine.game_state,
            'game_messages': game_engine.game_messages[-20:],  # Save last 20 messages
            
            # Current level data
            'map_width': game_engine.map_width,
            'map_height': game_engine.map_height,
            'current_level': self._serialize_level(game_engine.game_map)
        }
        
        filepath = os.path.join(self.save_directory, slot_name)
        try:
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)
            return True, f"Game saved as {slot_name}"
        except Exception as e:
            return False, f"Failed to save game: {str(e)}"
    
    def load_game(self, filepath):
        """Load a saved game state"""
        try:
            with open(filepath, 'r') as f:
                save_data = json.load(f)
            
            return True, save_data
        except Exception as e:
            return False, f"Failed to load game: {str(e)}"
    
    def delete_save(self, filepath):
        """Delete a save file"""
        try:
            os.remove(filepath)
            return True, "Save file deleted successfully"
        except Exception as e:
            return False, f"Failed to delete save: {str(e)}"
    
    def _serialize_item(self, item):
        """Convert item to serializable format"""
        return {
            'x': item.x,
            'y': item.y,
            'name': item.name,
            'char': item.char,
            'color': item.color,
            'item_type': item.item_type,
            'value': item.value
        }
    
    def _deserialize_item(self, item_data):
        """Convert serialized data back to Item object"""
        item = Item(
            item_data['x'], item_data['y'],
            item_data['name'], item_data['char'],
            item_data['color'], item_data['item_type'],
            item_data['value']
        )
        return item
    
    def _serialize_enemy(self, enemy):
        """Convert enemy to serializable format"""
        return {
            'x': enemy.x,
            'y': enemy.y,
            'name': enemy.name,
            'char': enemy.char,
            'color': enemy.color,
            'hp': enemy.hp,
            'max_hp': enemy.max_hp,
            'attack': enemy.attack,
            'defense': enemy.defense,
            'exp_value': enemy.exp_value,
            'ai_state': enemy.ai_state,
            'target': enemy.target
        }
    
    def _deserialize_enemy(self, enemy_data):
        """Convert serialized data back to Enemy object"""
        from game_entities import Enemy
        enemy = Enemy(
            enemy_data['x'], enemy_data['y'],
            enemy_data['name'], enemy_data['char'],
            enemy_data['color'], enemy_data['hp'],
            enemy_data['attack'], enemy_data['defense'],
            enemy_data['exp_value']
        )
        enemy.max_hp = enemy_data['max_hp']
        enemy.ai_state = enemy_data['ai_state']
        enemy.target = enemy_data['target']
        return enemy
    
    def _serialize_tile(self, tile):
        """Convert tile to serializable format"""
        return {
            'walkable': tile.walkable,
            'transparent': tile.transparent,
            'char': tile.char,
            'color': tile.color,
            'explored': tile.explored,
            'visible': tile.visible
        }
    
    def _deserialize_tile(self, tile_data):
        """Convert serialized data back to Tile object"""
        from game_map import Tile
        tile = Tile(
            tile_data['walkable'],
            tile_data['transparent'],
            tile_data['char'],
            tile_data['color']
        )
        tile.explored = tile_data['explored']
        tile.visible = tile_data['visible']
        return tile
    
    def _serialize_level(self, game_map):
        """Convert current level to serializable format"""
        return {
            'width': game_map.width,
            'height': game_map.height,
            'dungeon_level': game_map.dungeon_level,
            'tiles': [[self._serialize_tile(game_map.tiles[x][y]) 
                      for y in range(game_map.height)] 
                     for x in range(game_map.width)],
            'enemies': [self._serialize_enemy(enemy) for enemy in game_map.enemies],
            'items': [self._serialize_item(item) for item in game_map.items],
            'stairs_down': game_map.stairs_down,
            'stairs_up': game_map.stairs_up,
            'special_portal': game_map.special_portal
        }
    
    def _deserialize_level(self, level_data):
        """Convert serialized data back to GameMap object"""
        from game_map import GameMap
        game_map = GameMap(level_data['width'], level_data['height'], level_data['dungeon_level'])
        
        # Restore tiles
        for x in range(game_map.width):
            for y in range(game_map.height):
                game_map.tiles[x][y] = self._deserialize_tile(level_data['tiles'][x][y])
        
        # Restore enemies
        game_map.enemies = [self._deserialize_enemy(enemy_data) for enemy_data in level_data['enemies']]
        
        # Restore items
        game_map.items = [self._deserialize_item(item_data) for item_data in level_data['items']]
        
        # Restore special locations
        game_map.stairs_down = level_data['stairs_down']
        game_map.stairs_up = level_data['stairs_up']
        game_map.special_portal = level_data['special_portal']
        
        return game_map
    
    def restore_game_state(self, game_engine, save_data):
        """Restore game engine state from save data"""
        # Restore player
        game_engine.player.x = save_data['player_x']
        game_engine.player.y = save_data['player_y']
        game_engine.player.hp = save_data['player_hp']
        game_engine.player.max_hp = save_data['player_max_hp']
        game_engine.player.level = save_data['player_level']
        game_engine.player.exp = save_data['player_exp']
        game_engine.player.exp_to_next = save_data['player_exp_to_next']
        game_engine.player.attack = save_data['player_attack']
        game_engine.player.defense = save_data['player_defense']
        game_engine.player.gold = save_data['player_gold']
        game_engine.player.current_dungeon_level = save_data['dungeon_level']
        game_engine.player.max_dungeon_level_reached = save_data['max_dungeon_level']
        
        # Restore inventory
        game_engine.player.inventory = [
            self._deserialize_item(item_data) 
            for item_data in save_data['player_inventory']
        ]
        
        # Restore game state
        game_engine.dungeon_level = save_data['dungeon_level']
        game_engine.game_state = save_data['game_state']
        game_engine.game_messages = save_data['game_messages']
        
        # Restore current level
        game_engine.game_map = self._deserialize_level(save_data['current_level'])
        
        # Restore field of view
        from game_map import calculate_fov
        calculate_fov(game_engine.game_map, game_engine.player.x, game_engine.player.y)
        
        # Add load message
        character_name = save_data.get('character_name', 'Hero')
        game_engine.add_message(f"Welcome back, {character_name}!")
        game_engine.add_message(f"Resumed at dungeon level {game_engine.dungeon_level}")
        
        return True
