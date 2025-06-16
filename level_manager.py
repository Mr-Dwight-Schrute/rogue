import random
from game_map import generate_dungeon

class LevelManager:
    def __init__(self):
        self.generated_levels = {}  # Cache generated levels
        self.level_themes = {
            1: "Surface Caves",
            5: "Underground Tunnels", 
            10: "Ancient Crypts",
            15: "Molten Depths",
            20: "Crystal Caverns",
            25: "Shadow Realm",
            30: "Dragon's Lair",
            50: "Abyss Gates"
        }
        
    def get_level_theme(self, level):
        """Get the theme name for a given level"""
        theme_level = max([l for l in self.level_themes.keys() if l <= level])
        return self.level_themes[theme_level]
    
    def get_level_description(self, level):
        """Get a description for the current level"""
        theme = self.get_level_theme(level)
        
        descriptions = {
            "Surface Caves": [
                "Damp stone walls glisten in the torchlight.",
                "You hear the dripping of water echoing through the cavern.",
                "Moss grows on the ancient stone blocks."
            ],
            "Underground Tunnels": [
                "Carved passages wind deeper into the earth.",
                "The air grows thick and musty.",
                "Strange symbols are etched into the walls."
            ],
            "Ancient Crypts": [
                "Dusty tombs line the corridors.",
                "The smell of decay fills the air.",
                "Ancient bones crunch underfoot."
            ],
            "Molten Depths": [
                "Heat radiates from glowing cracks in the walls.",
                "Lava bubbles in distant chambers.",
                "The air shimmers with intense heat."
            ],
            "Crystal Caverns": [
                "Brilliant crystals illuminate the cavern.",
                "Light refracts in rainbow patterns.",
                "The walls hum with magical energy."
            ],
            "Shadow Realm": [
                "Darkness seems to move with a life of its own.",
                "Whispers echo from unseen sources.",
                "Reality feels unstable here."
            ],
            "Dragon's Lair": [
                "Massive claw marks scar the walls.",
                "The scent of sulfur is overwhelming.",
                "Treasure glints in the shadows."
            ],
            "Abyss Gates": [
                "The very fabric of reality tears here.",
                "Otherworldly energies crackle in the air.",
                "You sense immense power beyond comprehension."
            ]
        }
        
        return random.choice(descriptions.get(theme, ["You venture deeper into the unknown."]))
    
    def should_have_special_features(self, level):
        """Determine if a level should have special features"""
        features = {}
        
        # Boss rooms every 10 levels
        if level % 10 == 0:
            features['boss_room'] = True
            
        # Treasure rooms every 7 levels
        if level % 7 == 0:
            features['treasure_room'] = True
            
        # Magic portals every 5 levels starting from level 5
        if level >= 5 and level % 5 == 0:
            features['magic_portal'] = True
            
        # Rest areas every 15 levels
        if level % 15 == 0:
            features['rest_area'] = True
            
        return features
    
    def get_level_difficulty_multiplier(self, level):
        """Get difficulty multiplier for enemies and rewards"""
        base_multiplier = 1.0
        
        # Gradual increase
        if level <= 10:
            return base_multiplier + (level - 1) * 0.15
        elif level <= 25:
            return base_multiplier + 1.5 + (level - 10) * 0.25
        elif level <= 50:
            return base_multiplier + 5.25 + (level - 25) * 0.4
        else:
            return base_multiplier + 15.25 + (level - 50) * 0.5
    
    def generate_level_with_guaranteed_exits(self, width, height, level):
        """Generate a level ensuring it always has proper exits"""
        game_map = generate_dungeon(width, height, level)
        
        # Ensure every level has at least one exit
        if not game_map.stairs_down and not game_map.stairs_up and not game_map.special_portal:
            # Force create stairs in a random room if none exist
            if game_map.rooms:
                room = random.choice(game_map.rooms)
                stairs_x = random.randint(room.x + 1, room.x + room.width - 2)
                stairs_y = random.randint(room.y + 1, room.y + room.height - 2)
                game_map.stairs_down = (stairs_x, stairs_y)
        
        # Add special features based on level
        features = self.should_have_special_features(level)
        
        if features.get('boss_room') and len(game_map.rooms) >= 2:
            # Mark the last room as a boss room (more enemies)
            boss_room = game_map.rooms[-1]
            self._populate_boss_room(game_map, boss_room, level)
            
        if features.get('treasure_room') and len(game_map.rooms) >= 3:
            # Add extra treasure to a random room
            treasure_room = random.choice(game_map.rooms[1:-1])  # Not first or last
            self._populate_treasure_room(game_map, treasure_room, level)
            
        return game_map
    
    def _populate_boss_room(self, game_map, room, level):
        """Add boss enemies to a room"""
        from game_entities import create_enemy
        
        # Determine boss type based on level
        if level <= 10:
            boss_types = ['orc', 'troll']
        elif level <= 25:
            boss_types = ['troll', 'dragon']
        else:
            boss_types = ['dragon']
            
        # Add 1-2 boss enemies
        num_bosses = random.randint(1, 2)
        for _ in range(num_bosses):
            x = random.randint(room.x + 1, room.x + room.width - 2)
            y = random.randint(room.y + 1, room.y + room.height - 2)
            
            if not any(enemy.x == x and enemy.y == y for enemy in game_map.enemies):
                boss_type = random.choice(boss_types)
                boss = create_enemy(boss_type, x, y)
                
                # Make it a boss - stronger stats
                boss.hp = int(boss.hp * 2.5)
                boss.max_hp = boss.hp
                boss.attack = int(boss.attack * 1.8)
                boss.defense = int(boss.defense * 1.5)
                boss.exp_value = int(boss.exp_value * 3)
                boss.name = f"Boss {boss.name}"
                
                game_map.enemies.append(boss)
    
    def _populate_treasure_room(self, game_map, room, level):
        """Add extra treasure to a room"""
        from game_entities import create_item
        
        # Add 3-5 treasure items
        num_treasures = random.randint(3, 5)
        for _ in range(num_treasures):
            x = random.randint(room.x + 1, room.x + room.width - 2)
            y = random.randint(room.y + 1, room.y + room.height - 2)
            
            if (not any(item.x == x and item.y == y for item in game_map.items) and
                not any(enemy.x == x and enemy.y == y for enemy in game_map.enemies)):
                
                # Better treasure based on level
                if level <= 5:
                    item_type = random.choice(['health_potion', 'gold_large'])
                else:
                    item_type = 'gold_large'
                
                treasure = create_item(item_type, x, y)
                
                # Increase treasure value
                if treasure.item_type == 'gold':
                    treasure.value = int(treasure.value * (2 + level * 0.1))
                
                game_map.items.append(treasure)
