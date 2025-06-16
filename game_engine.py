import pygame
import sys
import time
from game_entities import Player
from game_map import generate_dungeon, calculate_fov
from level_manager import LevelManager
from save_manager import SaveManager

class GameEngine:
    def __init__(self, width=80, height=50):
        # Don't initialize pygame here, it should be initialized before creating this class
        self.map_width = width
        self.map_height = height
        self.tile_size = 12
        self.screen_width = width * self.tile_size
        self.screen_height = height * self.tile_size
        
        self.screen = pygame.Surface((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, self.tile_size)
        
        # Game state
        self.player = None
        self.game_map = None
        self.dungeon_level = 1
        self.game_messages = []
        self.game_state = "playing"  # "playing", "dead", "won"
        self.level_manager = LevelManager()
        self.save_manager = SaveManager()
        self.start_time = time.time()
        self.playtime = 0
        
        self.initialize_game()
    
    def initialize_game(self):
        # Use level manager to generate level with guaranteed exits
        self.game_map = self.level_manager.generate_level_with_guaranteed_exits(
            self.map_width, self.map_height, self.dungeon_level)
        
        # Place player in first room
        if self.game_map.rooms:
            first_room = self.game_map.rooms[0]
            player_x = first_room.center_x
            player_y = first_room.center_y
        else:
            player_x, player_y = self.map_width // 2, self.map_height // 2
        
        if self.player is None:
            self.player = Player(player_x, player_y)
        else:
            self.player.x, self.player.y = player_x, player_y
            # Update player's current dungeon level
            self.player.current_dungeon_level = self.dungeon_level
            if self.dungeon_level > self.player.max_dungeon_level_reached:
                self.player.max_dungeon_level_reached = self.dungeon_level
        
        calculate_fov(self.game_map, self.player.x, self.player.y)
        
        # Enhanced level messages
        theme = self.level_manager.get_level_theme(self.dungeon_level)
        description = self.level_manager.get_level_description(self.dungeon_level)
        
        self.add_message(f"=== {theme} - Level {self.dungeon_level} ===")
        self.add_message(description)
        
        # Show level progression info
        if self.dungeon_level > 1:
            self.add_message(f"Deepest level reached: {self.player.max_dungeon_level_reached}")
            
        # Show special features
        features = self.level_manager.should_have_special_features(self.dungeon_level)
        if features.get('boss_room'):
            self.add_message("You sense a powerful presence nearby...")
        if features.get('treasure_room'):
            self.add_message("You smell the glint of treasure in the air.")
        if features.get('magic_portal'):
            self.add_message("Magical energies swirl around this place.")
        if features.get('rest_area'):
            self.add_message("This place feels safe and peaceful.")
    
    def add_message(self, message):
        self.game_messages.append(message)
        if len(self.game_messages) > 10:  # Keep only last 10 messages
            self.game_messages.pop(0)
    
    def handle_input(self, key):
        if self.game_state != "playing":
            return
        
        dx, dy = 0, 0
        
        # Movement keys
        if key == pygame.K_UP or key == pygame.K_k:
            dy = -1
        elif key == pygame.K_DOWN or key == pygame.K_j:
            dy = 1
        elif key == pygame.K_LEFT or key == pygame.K_h:
            dx = -1
        elif key == pygame.K_RIGHT or key == pygame.K_l:
            dx = 1
        elif key == pygame.K_y:  # diagonal up-left
            dx, dy = -1, -1
        elif key == pygame.K_u:  # diagonal up-right
            dx, dy = 1, -1
        elif key == pygame.K_b:  # diagonal down-left
            dx, dy = -1, 1
        elif key == pygame.K_n:  # diagonal down-right
            dx, dy = 1, 1
        elif key == pygame.K_PERIOD:  # wait/rest
            self.player_turn()
            return
        elif key == pygame.K_COMMA:  # pick up item
            self.pickup_item()
            return
        elif key == pygame.K_d:  # go down stairs (changed from GREATER)
            self.use_stairs_down()
            return
        elif key == pygame.K_a:  # go up stairs (changed from LESS)
            self.use_stairs_up()
            return
        elif key == pygame.K_p:  # use special portal
            self.use_special_portal()
            return
        elif key == pygame.K_s and pygame.key.get_pressed()[pygame.K_LCTRL]:  # Ctrl+S to save
            self.quick_save()
            return
        
        if dx != 0 or dy != 0:
            self.move_player(dx, dy)
    
    def move_player(self, dx, dy):
        new_x, new_y = self.player.x + dx, self.player.y + dy
        
        # Check for enemy at target position
        target_enemy = None
        for enemy in self.game_map.enemies:
            if enemy.x == new_x and enemy.y == new_y:
                target_enemy = enemy
                break
        
        if target_enemy:
            # Attack enemy
            damage = self.player.attack_enemy(target_enemy)
            self.add_message(f"You hit {target_enemy.name} for {damage} damage!")
            
            if target_enemy.hp <= 0:
                self.add_message(f"{target_enemy.name} dies!")
                self.player.gain_exp(target_enemy.exp_value)
                self.game_map.enemies.remove(target_enemy)
                
                # Check for level up
                if self.player.exp >= self.player.exp_to_next:
                    level_msg = self.player.level_up()
                    self.add_message(level_msg)
        else:
            # Try to move
            if self.player.move(dx, dy, self.game_map):
                pass  # Successful move
        
        # Update playtime before player turn
        self.update_playtime()
        self.player_turn()
    
    def player_turn(self):
        # Update field of view
        calculate_fov(self.game_map, self.player.x, self.player.y)
        
        # Enemy turns
        for enemy in self.game_map.enemies[:]:  # Copy list to avoid modification during iteration
            if enemy.hp <= 0:
                continue
                
            # Check if enemy is adjacent to player
            distance = abs(enemy.x - self.player.x) + abs(enemy.y - self.player.y)
            if distance == 1:
                # Attack player
                damage = enemy.attack_player(self.player)
                self.add_message(f"{enemy.name} hits you for {damage} damage!")
                
                if self.player.hp <= 0:
                    self.game_state = "dead"
                    self.add_message("You have died!")
            else:
                # AI movement
                enemy.ai_turn(self.player, self.game_map)
    
    def pickup_item(self):
        # Check for item at player position
        for item in self.game_map.items[:]:
            if item.x == self.player.x and item.y == self.player.y:
                message = item.use(self.player)
                self.add_message(f"You picked up {item.name}. {message}")
                self.game_map.items.remove(item)
                self.player_turn()
                return
        
        self.add_message("There's nothing here to pick up.")
    
    def use_stairs_down(self):
        if (self.game_map.stairs_down and 
            self.player.x == self.game_map.stairs_down[0] and 
            self.player.y == self.game_map.stairs_down[1]):
            
            self.dungeon_level += 1
            self.add_message(f"You descend to level {self.dungeon_level}!")
            self.initialize_game()
        else:
            self.add_message("There are no stairs here.")
    
    def use_stairs_up(self):
        if (self.game_map.stairs_up and 
            self.player.x == self.game_map.stairs_up[0] and 
            self.player.y == self.game_map.stairs_up[1]):
            
            if self.dungeon_level > 1:
                self.dungeon_level -= 1
                self.add_message(f"You ascend to level {self.dungeon_level}!")
                self.initialize_game()
            else:
                self.add_message("You escape the dungeon! You win!")
                self.game_state = "won"
        else:
            self.add_message("There are no stairs here.")
    
    def use_special_portal(self):
        if (self.game_map.special_portal and 
            self.player.x == self.game_map.special_portal[0] and 
            self.player.y == self.game_map.special_portal[1]):
            
            # Special portal jumps 5 levels deeper
            self.dungeon_level += 5
            self.add_message(f"The portal transports you to level {self.dungeon_level}!")
            self.add_message("You feel the magic energy coursing through you!")
            self.initialize_game()
        else:
            self.add_message("There is no portal here.")
    
    def quick_save(self):
        """Quick save the current game"""
        self.update_playtime()
        success, message = self.save_manager.save_game(self, "Hero", "quicksave")
        self.add_message(message)
        return success
    
    def save_game(self, character_name="Hero", slot_name=None):
        """Save the current game state"""
        self.update_playtime()
        success, message = self.save_manager.save_game(self, character_name, slot_name)
        self.add_message(message)
        return success, message
    
    def load_game(self, filepath):
        """Load a saved game state"""
        success, result = self.save_manager.load_game(filepath)
        if success:
            save_data = result
            self.save_manager.restore_game_state(self, save_data)
            self.start_time = time.time() - save_data.get('playtime', 0)
            return True, "Game loaded successfully"
        else:
            return False, result
    
    def update_playtime(self):
        """Update the total playtime"""
        self.playtime = time.time() - self.start_time
    
    def get_playtime_string(self):
        """Get formatted playtime string"""
        total_seconds = int(self.playtime)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def draw_char(self, x, y, char, color):
        pixel_x = x * self.tile_size
        pixel_y = y * self.tile_size
        text_surface = self.font.render(char, True, color)
        self.screen.blit(text_surface, (pixel_x, pixel_y))
    
    def render(self):
        self.screen.fill((0, 0, 0))  # Black background
        
        # Draw map
        for x in range(self.map_width):
            for y in range(self.map_height):
                tile = self.game_map.get_tile(x, y)
                if tile and tile.explored:
                    if tile.visible:
                        color = tile.color
                    else:
                        # Darken explored but not visible tiles
                        color = tuple(c // 3 for c in tile.color)
                    
                    self.draw_char(x, y, tile.char, color)
        
        # Draw stairs
        if self.game_map.stairs_down:
            x, y = self.game_map.stairs_down
            tile = self.game_map.get_tile(x, y)
            if tile and (tile.visible or tile.explored):
                # Show stairs in bright yellow if visible, dimmed yellow if just explored
                color = (255, 255, 0) if tile.visible else (128, 128, 0)
                self.draw_char(x, y, '>', color)
        
        if self.game_map.stairs_up:
            x, y = self.game_map.stairs_up
            tile = self.game_map.get_tile(x, y)
            if tile and (tile.visible or tile.explored):
                # Show stairs in bright yellow if visible, dimmed yellow if just explored
                color = (255, 255, 0) if tile.visible else (128, 128, 0)
                self.draw_char(x, y, '<', color)
        
        # Draw special portal
        if self.game_map.special_portal:
            x, y = self.game_map.special_portal
            tile = self.game_map.get_tile(x, y)
            if tile and (tile.visible or tile.explored):
                # Show portal in bright magenta if visible, dimmed magenta if just explored
                color = (255, 0, 255) if tile.visible else (128, 0, 128)
                self.draw_char(x, y, 'P', color)
        
        # Draw items
        for item in self.game_map.items:
            tile = self.game_map.get_tile(item.x, item.y)
            if tile and tile.visible:
                self.draw_char(item.x, item.y, item.char, item.color)
        
        # Draw enemies
        for enemy in self.game_map.enemies:
            tile = self.game_map.get_tile(enemy.x, enemy.y)
            if tile and tile.visible:
                self.draw_char(enemy.x, enemy.y, enemy.char, enemy.color)
        
        # Draw player
        self.draw_char(self.player.x, self.player.y, self.player.char, self.player.color)
        
        # No need for pygame.display.flip() in PyQt integration
    
    def get_game_state(self):
        self.update_playtime()
        return {
            'player_hp': self.player.hp,
            'player_max_hp': self.player.max_hp,
            'player_level': self.player.level,
            'player_exp': self.player.exp,
            'player_exp_to_next': self.player.exp_to_next,
            'player_gold': self.player.gold,
            'dungeon_level': self.dungeon_level,
            'max_dungeon_level': self.player.max_dungeon_level_reached,
            'messages': self.game_messages.copy(),
            'game_state': self.game_state,
            'has_portal': self.game_map.special_portal is not None,
            'playtime': self.get_playtime_string()
        }
    
    def process_events(self):
        # In PyQt integration, we don't process pygame events directly
        # This is handled by the PyQt event system
        return True
    
    def update(self):
        # Update playtime continuously
        self.update_playtime()
        return True
    
    def get_surface(self):
        return self.screen
