import pygame
import random
import math

class Entity:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.hp = 100
        self.max_hp = 100
        
    def move(self, dx, dy, game_map):
        new_x, new_y = self.x + dx, self.y + dy
        if game_map.is_walkable(new_x, new_y):
            self.x, self.y = new_x, new_y
            return True
        return False

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '@', (255, 255, 255))
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        self.attack = 10
        self.defense = 5
        self.inventory = []
        self.gold = 0
        self.current_dungeon_level = 1
        self.max_dungeon_level_reached = 1
        
    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 3
        self.defense += 2
        return f"Level up! Now level {self.level}"
    
    def attack_enemy(self, enemy):
        damage = max(1, self.attack - enemy.defense)
        enemy.hp -= damage
        return damage

class Enemy(Entity):
    def __init__(self, x, y, name, char, color, hp, attack, defense, exp_value):
        super().__init__(x, y, char, color)
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.exp_value = exp_value
        self.ai_state = "patrol"
        self.target = None
        
    def can_see_player(self, player, game_map, sight_range=8):
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        if distance > sight_range:
            return False
        
        # Simple line of sight check
        dx = abs(player.x - self.x)
        dy = abs(player.y - self.y)
        x, y = self.x, self.y
        n = 1 + dx + dy
        x_inc = 1 if player.x > self.x else -1
        y_inc = 1 if player.y > self.y else -1
        error = dx - dy
        
        dx *= 2
        dy *= 2
        
        for _ in range(n):
            if not game_map.is_transparent(x, y):
                return False
            if x == player.x and y == player.y:
                return True
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
        return True
    
    def ai_turn(self, player, game_map):
        if self.can_see_player(player, game_map):
            self.ai_state = "chase"
            self.target = (player.x, player.y)
        
        if self.ai_state == "chase" and self.target:
            # Move towards player
            dx = 0 if self.target[0] == self.x else (1 if self.target[0] > self.x else -1)
            dy = 0 if self.target[1] == self.y else (1 if self.target[1] > self.y else -1)
            
            # Try to move towards player
            if not self.move(dx, dy, game_map):
                # If direct path blocked, try alternative moves
                if dx != 0 and self.move(dx, 0, game_map):
                    pass
                elif dy != 0 and self.move(0, dy, game_map):
                    pass
        else:
            # Random patrol movement
            if random.random() < 0.3:  # 30% chance to move
                dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
                self.move(dx, dy, game_map)
    
    def attack_player(self, player):
        damage = max(1, self.attack - player.defense)
        player.hp -= damage
        return damage

class Item:
    def __init__(self, x, y, name, char, color, item_type, value=0):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.item_type = item_type  # 'potion', 'weapon', 'armor', 'gold'
        self.value = value
    
    def use(self, player):
        if self.item_type == 'potion':
            player.hp = min(player.max_hp, player.hp + self.value)
            return f"Restored {self.value} HP"
        elif self.item_type == 'gold':
            player.gold += self.value
            return f"Found {self.value} gold"
        return "Used item"

# Enemy templates
ENEMY_TYPES = {
    'rat': {'name': 'Giant Rat', 'char': 'r', 'color': (139, 69, 19), 
            'hp': 15, 'attack': 5, 'defense': 1, 'exp': 10},
    'goblin': {'name': 'Goblin', 'char': 'g', 'color': (0, 128, 0), 
               'hp': 25, 'attack': 8, 'defense': 2, 'exp': 20},
    'orc': {'name': 'Orc', 'char': 'O', 'color': (0, 100, 0), 
            'hp': 40, 'attack': 12, 'defense': 4, 'exp': 35},
    'troll': {'name': 'Troll', 'char': 'T', 'color': (0, 80, 0), 
              'hp': 60, 'attack': 15, 'defense': 6, 'exp': 50},
    'dragon': {'name': 'Dragon', 'char': 'D', 'color': (255, 0, 0), 
               'hp': 100, 'attack': 25, 'defense': 10, 'exp': 100}
}

def create_enemy(enemy_type, x, y):
    template = ENEMY_TYPES[enemy_type]
    return Enemy(x, y, template['name'], template['char'], template['color'],
                template['hp'], template['attack'], template['defense'], template['exp'])

# Item templates
ITEM_TYPES = {
    'health_potion': {'name': 'Health Potion', 'char': '!', 'color': (255, 0, 0), 
                     'type': 'potion', 'value': 30},
    'gold_small': {'name': 'Gold Coins', 'char': '$', 'color': (255, 215, 0), 
                   'type': 'gold', 'value': 25},
    'gold_large': {'name': 'Gold Pile', 'char': '$', 'color': (255, 215, 0), 
                   'type': 'gold', 'value': 100}
}

def create_item(item_type, x, y):
    template = ITEM_TYPES[item_type]
    return Item(x, y, template['name'], template['char'], template['color'],
               template['type'], template['value'])
