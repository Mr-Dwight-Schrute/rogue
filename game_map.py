import random
from game_entities import create_enemy, create_item

class Tile:
    def __init__(self, walkable=True, transparent=True, char='.', color=(128, 128, 128)):
        self.walkable = walkable
        self.transparent = transparent
        self.char = char
        self.color = color
        self.explored = False
        self.visible = False

class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.dungeon_level = dungeon_level
        self.tiles = [[Tile(walkable=False, transparent=False, char='#', color=(100, 100, 100)) 
                      for _ in range(height)] for _ in range(width)]
        self.rooms = []
        self.enemies = []
        self.items = []
        self.stairs_down = None
        self.stairs_up = None
        self.special_portal = None  # For special level transitions
        
    def is_walkable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y].walkable
        return False
    
    def is_transparent(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y].transparent
        return False
    
    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y]
        return None

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center_x = x + width // 2
        self.center_y = y + height // 2
    
    def intersects(self, other):
        return (self.x <= other.x + other.width and
                self.x + self.width >= other.x and
                self.y <= other.y + other.height and
                self.y + self.height >= other.y)

def generate_dungeon(width, height, dungeon_level=1):
    game_map = GameMap(width, height, dungeon_level)
    
    # Generate rooms
    rooms = []
    max_rooms = 15 + dungeon_level * 2
    min_room_size = 4
    max_room_size = 8 + min(dungeon_level // 2, 4)  # Cap room size growth
    
    for _ in range(max_rooms):
        room_width = random.randint(min_room_size, max_room_size)
        room_height = random.randint(min_room_size, max_room_size)
        x = random.randint(1, width - room_width - 1)
        y = random.randint(1, height - room_height - 1)
        
        new_room = Room(x, y, room_width, room_height)
        
        # Check if room intersects with existing rooms
        if not any(new_room.intersects(room) for room in rooms):
            create_room(game_map, new_room)
            
            if rooms:  # Connect to previous room
                connect_rooms(game_map, rooms[-1], new_room)
            
            rooms.append(new_room)
    
    game_map.rooms = rooms
    
    # Always place stairs - ensure every level has exits
    if rooms:
        # Stairs down in the last room (always present)
        last_room = rooms[-1]
        stairs_x = random.randint(last_room.x + 1, last_room.x + last_room.width - 2)
        stairs_y = random.randint(last_room.y + 1, last_room.y + last_room.height - 2)
        game_map.stairs_down = (stairs_x, stairs_y)
        
        # Stairs up in the first room (if not level 1)
        if dungeon_level > 1:
            first_room = rooms[0]
            stairs_x = random.randint(first_room.x + 1, first_room.x + first_room.width - 2)
            stairs_y = random.randint(first_room.y + 1, first_room.y + first_room.height - 2)
            game_map.stairs_up = (stairs_x, stairs_y)
        
        # Special exits for deeper levels
        if dungeon_level >= 5 and len(rooms) >= 3:
            # Add a special portal room every 5 levels
            if dungeon_level % 5 == 0:
                portal_room = rooms[len(rooms) // 2]  # Middle room
                portal_x = random.randint(portal_room.x + 1, portal_room.x + portal_room.width - 2)
                portal_y = random.randint(portal_room.y + 1, portal_room.y + portal_room.height - 2)
                game_map.special_portal = (portal_x, portal_y)
    
    # Populate with enemies and items
    populate_dungeon(game_map, dungeon_level)
    
    return game_map

def create_room(game_map, room):
    for x in range(room.x, room.x + room.width):
        for y in range(room.y, room.y + room.height):
            game_map.tiles[x][y] = Tile(walkable=True, transparent=True, char='.', color=(64, 64, 64))

def connect_rooms(game_map, room1, room2):
    # Create L-shaped corridor between rooms
    x1, y1 = room1.center_x, room1.center_y
    x2, y2 = room2.center_x, room2.center_y
    
    # Horizontal then vertical
    if random.choice([True, False]):
        create_horizontal_tunnel(game_map, x1, x2, y1)
        create_vertical_tunnel(game_map, y1, y2, x2)
    else:
        create_vertical_tunnel(game_map, y1, y2, x1)
        create_horizontal_tunnel(game_map, x1, x2, y2)

def create_horizontal_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        if 0 <= x < game_map.width and 0 <= y < game_map.height:
            game_map.tiles[x][y] = Tile(walkable=True, transparent=True, char='.', color=(64, 64, 64))

def create_vertical_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        if 0 <= x < game_map.width and 0 <= y < game_map.height:
            game_map.tiles[x][y] = Tile(walkable=True, transparent=True, char='.', color=(64, 64, 64))

def populate_dungeon(game_map, dungeon_level):
    # Determine enemy types based on dungeon level with more variety
    if dungeon_level <= 2:
        enemy_types = ['rat', 'goblin']
        enemy_weights = [0.7, 0.3]
    elif dungeon_level <= 5:
        enemy_types = ['rat', 'goblin', 'orc']
        enemy_weights = [0.3, 0.5, 0.2]
    elif dungeon_level <= 10:
        enemy_types = ['goblin', 'orc', 'troll']
        enemy_weights = [0.2, 0.6, 0.2]
    elif dungeon_level <= 15:
        enemy_types = ['orc', 'troll', 'dragon']
        enemy_weights = [0.3, 0.5, 0.2]
    else:
        enemy_types = ['troll', 'dragon']
        enemy_weights = [0.4, 0.6]
    
    # Place enemies (skip first room for player spawn)
    for room in game_map.rooms[1:]:
        if random.random() < 0.8:  # 80% chance for enemies in room
            num_enemies = random.randint(1, min(4, 1 + dungeon_level // 3))
            for _ in range(num_enemies):
                x = random.randint(room.x + 1, room.x + room.width - 2)
                y = random.randint(room.y + 1, room.y + room.height - 2)
                
                # Make sure position is empty
                if not any(enemy.x == x and enemy.y == y for enemy in game_map.enemies):
                    enemy_type = random.choices(enemy_types, weights=enemy_weights)[0]
                    enemy = create_enemy(enemy_type, x, y)
                    
                    # Scale enemy stats with dungeon level
                    level_multiplier = 1 + (dungeon_level - 1) * 0.2
                    enemy.hp = int(enemy.hp * level_multiplier)
                    enemy.max_hp = enemy.hp
                    enemy.attack = int(enemy.attack * level_multiplier)
                    enemy.defense = int(enemy.defense * level_multiplier)
                    enemy.exp_value = int(enemy.exp_value * level_multiplier)
                    
                    game_map.enemies.append(enemy)
    
    # Place items with better distribution
    for room in game_map.rooms:
        if random.random() < 0.6:  # 60% chance for items in room
            num_items = random.randint(1, 3)
            for _ in range(num_items):
                x = random.randint(room.x + 1, room.x + room.width - 2)
                y = random.randint(room.y + 1, room.y + room.height - 2)
                
                # Make sure position is empty
                if (not any(item.x == x and item.y == y for item in game_map.items) and
                    not any(enemy.x == x and enemy.y == y for enemy in game_map.enemies) and
                    (game_map.stairs_down is None or (x, y) != game_map.stairs_down) and
                    (game_map.stairs_up is None or (x, y) != game_map.stairs_up)):
                    
                    # Better item distribution based on level
                    if dungeon_level <= 3:
                        item_type = random.choice(['health_potion', 'gold_small'])
                    elif dungeon_level <= 8:
                        item_type = random.choice(['health_potion', 'gold_small', 'gold_large'])
                    else:
                        item_type = random.choice(['health_potion', 'gold_large', 'gold_large'])
                    
                    item = create_item(item_type, x, y)
                    
                    # Scale item values with dungeon level
                    if item.item_type == 'gold':
                        item.value = int(item.value * (1 + dungeon_level * 0.3))
                    elif item.item_type == 'potion':
                        item.value = int(item.value * (1 + dungeon_level * 0.1))
                    
                    game_map.items.append(item)

def calculate_fov(game_map, player_x, player_y, radius=8):
    # Reset visibility
    for x in range(game_map.width):
        for y in range(game_map.height):
            game_map.tiles[x][y].visible = False
    
    # Simple circular FOV
    for x in range(max(0, player_x - radius), min(game_map.width, player_x + radius + 1)):
        for y in range(max(0, player_y - radius), min(game_map.height, player_y + radius + 1)):
            distance = ((x - player_x) ** 2 + (y - player_y) ** 2) ** 0.5
            if distance <= radius:
                if has_line_of_sight(game_map, player_x, player_y, x, y):
                    game_map.tiles[x][y].visible = True
                    game_map.tiles[x][y].explored = True

def has_line_of_sight(game_map, x1, y1, x2, y2):
    # Bresenham's line algorithm for line of sight
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    n = 1 + dx + dy
    x_inc = 1 if x2 > x1 else -1
    y_inc = 1 if y2 > y1 else -1
    error = dx - dy
    
    dx *= 2
    dy *= 2
    
    for _ in range(n):
        if x == x2 and y == y2:
            return True
        if not game_map.is_transparent(x, y):
            return False
        if error > 0:
            x += x_inc
            error -= dy
        else:
            y += y_inc
            error += dx
    
    return True
