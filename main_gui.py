import sys
import pygame
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QTextEdit, QProgressBar, 
                            QPushButton, QFrame, QGridLayout, QScrollArea,
                            QMessageBox, QMenuBar, QAction, QDialog)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QImage, QPalette, QColor, QKeySequence
from game_engine import GameEngine
from save_load_dialog import SaveLoadDialog

class PygameWidget(QWidget):
    keyPressed = pyqtSignal(int)
    
    def __init__(self, game_engine):
        super().__init__()
        self.game_engine = game_engine
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(game_engine.screen_width, game_engine.screen_height)
        
        # Key repeat functionality
        self.active_keys = set()  # Track currently pressed keys
        self.key_repeat_timer = QTimer(self)
        self.key_repeat_timer.timeout.connect(self.process_active_keys)
        self.key_repeat_timer.setInterval(300)  # 300ms repeat rate (increased from 100ms)
        self.initial_delay = 300  # 300ms initial delay before repeating
        self.key_first_press_time = {}  # Track when keys were first pressed
        
        # Disable Qt's built-in key compression
        self.setAttribute(Qt.WA_KeyCompression, False)
        
        # Suppress QWidget::paintEngine warnings
        import os
        os.environ['QT_LOGGING_RULES'] = "qt.widgets.paintengine=false"
        
    def paintEvent(self, event):
        if self.game_engine:
            # Render the pygame surface
            self.game_engine.render()
            
            # Convert pygame surface to QImage and display
            surface = self.game_engine.get_surface()
            w, h = surface.get_size()
            raw = pygame.image.tostring(surface, 'RGB')
            qimg = QImage(raw, w, h, QImage.Format_RGB888)
            qpixmap = QPixmap.fromImage(qimg)
            
            # Draw on the widget using QPainter instead of paintEngine
            from PyQt5.QtGui import QPainter
            painter = QPainter(self)
            painter.drawPixmap(0, 0, qpixmap)
            painter.end()
    
    def keyPressEvent(self, event):
        # Convert Qt key to pygame key
        qt_to_pygame = {
            Qt.Key_Up: pygame.K_UP,
            Qt.Key_Down: pygame.K_DOWN,
            Qt.Key_Left: pygame.K_LEFT,
            Qt.Key_Right: pygame.K_RIGHT,
            Qt.Key_K: pygame.K_k,
            Qt.Key_J: pygame.K_j,
            Qt.Key_H: pygame.K_h,
            Qt.Key_L: pygame.K_l,
            Qt.Key_Y: pygame.K_y,
            Qt.Key_U: pygame.K_u,
            Qt.Key_B: pygame.K_b,
            Qt.Key_N: pygame.K_n,
            Qt.Key_Period: pygame.K_PERIOD,
            Qt.Key_Comma: pygame.K_COMMA,
            Qt.Key_D: pygame.K_d,  # New key for going down stairs
            Qt.Key_A: pygame.K_a,  # New key for going up stairs
            Qt.Key_P: pygame.K_p,
            Qt.Key_S: pygame.K_s,
        }
        
        pygame_key = qt_to_pygame.get(event.key())
        if pygame_key:
            # Only set up key repeat for movement keys
            movement_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                            pygame.K_k, pygame.K_j, pygame.K_h, pygame.K_l,
                            pygame.K_y, pygame.K_u, pygame.K_b, pygame.K_n]
            
            # Send the key press immediately
            self.keyPressed.emit(pygame_key)
            
            # Set up key repeat for movement keys
            if pygame_key in movement_keys:
                import time
                current_time = time.time()
                self.key_first_press_time[pygame_key] = current_time
                self.active_keys.add(pygame_key)
                if not self.key_repeat_timer.isActive():
                    self.key_repeat_timer.start()
                    
        # Let the parent class handle the event
        super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        # Convert Qt key to pygame key
        qt_to_pygame = {
            Qt.Key_Up: pygame.K_UP,
            Qt.Key_Down: pygame.K_DOWN,
            Qt.Key_Left: pygame.K_LEFT,
            Qt.Key_Right: pygame.K_RIGHT,
            Qt.Key_K: pygame.K_k,
            Qt.Key_J: pygame.K_j,
            Qt.Key_H: pygame.K_h,
            Qt.Key_L: pygame.K_l,
            Qt.Key_Y: pygame.K_y,
            Qt.Key_U: pygame.K_u,
            Qt.Key_B: pygame.K_b,
            Qt.Key_N: pygame.K_n,
        }
        
        pygame_key = qt_to_pygame.get(event.key())
        if pygame_key in self.active_keys:
            self.active_keys.remove(pygame_key)
            if pygame_key in self.key_first_press_time:
                del self.key_first_press_time[pygame_key]
            
        # Stop timer if no keys are pressed
        if not self.active_keys and self.key_repeat_timer.isActive():
            self.key_repeat_timer.stop()
            
        # Don't call the parent implementation to avoid auto-repeat
        # super().keyReleaseEvent(event)
    
    def process_active_keys(self):
        """Process all currently active keys"""
        import time
        current_time = time.time()
        
        for key in list(self.active_keys):  # Use list to avoid modification during iteration
            # Check if the initial delay has passed
            if key in self.key_first_press_time:
                elapsed = current_time - self.key_first_press_time[key]
                if elapsed >= (self.initial_delay / 1000.0):  # Convert ms to seconds
                    self.keyPressed.emit(key)

class GameStatsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # Create a scroll area to contain all the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Container widget for the scroll area
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Create a horizontal layout for the two columns
        columns_layout = QHBoxLayout()
        
        # Left column - Player stats and controls
        left_column = QVBoxLayout()
        
        # Player stats
        stats_frame = QFrame()
        stats_frame.setFrameStyle(QFrame.Box)
        stats_layout = QGridLayout(stats_frame)
        
        # HP Bar
        self.hp_label = QLabel("HP:")
        self.hp_bar = QProgressBar()
        self.hp_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")
        stats_layout.addWidget(self.hp_label, 0, 0)
        stats_layout.addWidget(self.hp_bar, 0, 1)
        
        # Level and XP
        self.level_label = QLabel("Level: 1")
        self.exp_label = QLabel("EXP:")
        self.exp_bar = QProgressBar()
        self.exp_bar.setStyleSheet("QProgressBar::chunk { background-color: blue; }")
        stats_layout.addWidget(self.level_label, 1, 0)
        stats_layout.addWidget(self.exp_label, 2, 0)
        stats_layout.addWidget(self.exp_bar, 2, 1)
        
        # Gold
        self.gold_label = QLabel("Gold: 0")
        stats_layout.addWidget(self.gold_label, 3, 0, 1, 2)
        
        # Dungeon level
        self.dungeon_label = QLabel("Dungeon Level: 1")
        stats_layout.addWidget(self.dungeon_label, 4, 0, 1, 2)
        
        # Max level reached
        self.max_level_label = QLabel("Deepest: 1")
        stats_layout.addWidget(self.max_level_label, 5, 0, 1, 2)
        
        # Playtime
        self.playtime_label = QLabel("Time: 00:00")
        stats_layout.addWidget(self.playtime_label, 6, 0, 1, 2)
        
        left_column.addWidget(stats_frame)
        
        # Controls help
        controls_frame = QFrame()
        controls_frame.setFrameStyle(QFrame.Box)
        controls_layout = QVBoxLayout(controls_frame)
        
        controls_title = QLabel("Controls:")
        controls_title.setFont(QFont("Arial", 10, QFont.Bold))
        controls_layout.addWidget(controls_title)
        
        controls_text = QLabel("""
Arrow Keys / hjkl: Move
yubn: Diagonal movement
.: Wait/Rest
,: Pick up item
d: Go down stairs
a: Go up stairs
p: Use portal (if available)
Ctrl+S: Quick save
        """)
        controls_text.setFont(QFont("Courier", 8))
        controls_layout.addWidget(controls_text)
        
        left_column.addWidget(controls_frame)
        
        # Right column - Game info and legend
        right_column = QVBoxLayout()
        
        # Game info
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Box)
        info_layout = QVBoxLayout(info_frame)
        
        info_title = QLabel("Legend:")
        info_title.setFont(QFont("Arial", 10, QFont.Bold))
        info_layout.addWidget(info_title)
        
        legend_text = QLabel("""
@: Player
r: Rat    g: Goblin
O: Orc    T: Troll
D: Dragon
!: Health Potion
$: Gold
>: Stairs Down (use 'd')
<: Stairs Up (use 'a')
P: Magic Portal
        """)
        legend_text.setFont(QFont("Courier", 8))
        info_layout.addWidget(legend_text)
        
        right_column.addWidget(info_frame)
        right_column.addStretch()
        
        # Add columns to the horizontal layout
        columns_layout.addLayout(left_column)
        columns_layout.addLayout(right_column)
        
        # Add the columns layout to the main layout
        layout.addLayout(columns_layout)
        
        # Set the container as the scroll area's widget
        scroll_area.setWidget(container)
        
        # Main layout for this widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
    
    def update_stats(self, game_state):
        # Update HP
        hp_percent = int((game_state['player_hp'] / game_state['player_max_hp']) * 100)
        self.hp_bar.setValue(hp_percent)
        self.hp_label.setText(f"HP: {game_state['player_hp']}/{game_state['player_max_hp']}")
        
        # Update level and XP
        self.level_label.setText(f"Level: {game_state['player_level']}")
        exp_percent = int((game_state['player_exp'] / game_state['player_exp_to_next']) * 100)
        self.exp_bar.setValue(exp_percent)
        self.exp_label.setText(f"EXP: {game_state['player_exp']}/{game_state['player_exp_to_next']}")
        
        # Update gold
        self.gold_label.setText(f"Gold: {game_state['player_gold']}")
        
        # Update dungeon level
        self.dungeon_label.setText(f"Dungeon Level: {game_state['dungeon_level']}")
        
        # Update max level reached
        self.max_level_label.setText(f"Deepest: {game_state['max_dungeon_level']}")
        
        # Update playtime
        self.playtime_label.setText(f"Time: {game_state['playtime']}")
        
        # Show portal status
        if game_state['has_portal']:
            self.max_level_label.setText(f"Deepest: {game_state['max_dungeon_level']} (Portal!)")

class MessageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("Messages:")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(title)
        
        self.message_area = QTextEdit()
        self.message_area.setReadOnly(True)
        self.message_area.setMaximumHeight(150)
        self.message_area.setFont(QFont("Courier", 9))
        layout.addWidget(self.message_area)
        
        self.setLayout(layout)
    
    def update_messages(self, messages):
        self.message_area.clear()
        for message in messages:
            self.message_area.append(message)
        
        # Scroll to bottom
        scrollbar = self.message_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize pygame first
        pygame.init()
        self.game_engine = GameEngine()
        self.init_ui()
        self.setup_timer()
    
    def init_ui(self):
        # Get screen size information
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()
        
        # Calculate 80% of screen dimensions
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Center the window on screen
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        # Set window size and position
        self.setWindowTitle("PyQt5 Roguelike Game")
        self.setGeometry(x_position, y_position, window_width, window_height)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QFrame {
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
                margin: 2px;
            }
            QLabel {
                color: #ffffff;
            }
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 3px;
                text-align: center;
                color: #ffffff;
            }
            QProgressBar::chunk {
                border-radius: 3px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #555555;
                color: #ffffff;
            }
            QPushButton {
                background-color: #404040;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QScrollBar:vertical {
                border: none;
                background: #333333;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #666666;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Main container widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with proper spacing
        main_layout = QHBoxLayout(central_widget)
        
        # Calculate the game area and sidebar proportions (70% game, 30% sidebar)
        game_width = int(window_width * 0.7)
        sidebar_width = int(window_width * 0.3)
        
        # Game area (pygame widget)
        self.pygame_widget = PygameWidget(self.game_engine)
        self.pygame_widget.keyPressed.connect(self.handle_key_press)
        self.pygame_widget.setMinimumWidth(game_width)
        main_layout.addWidget(self.pygame_widget, 7)
        
        # Right panel with scroll area
        right_panel_widget = QWidget()
        right_panel = QVBoxLayout(right_panel_widget)
        right_panel.setSpacing(5)
        right_panel.setContentsMargins(0, 0, 0, 0)
        
        # Stats widget
        self.stats_widget = GameStatsWidget()
        right_panel.addWidget(self.stats_widget)
        
        # Messages widget
        self.message_widget = MessageWidget()
        right_panel.addWidget(self.message_widget)
        
        # Control buttons in horizontal layout
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(5)
        
        self.new_game_btn = QPushButton("New Game")
        self.new_game_btn.clicked.connect(self.new_game)
        button_layout.addWidget(self.new_game_btn)
        
        self.save_btn = QPushButton("Save Game")
        self.save_btn.clicked.connect(self.save_game)
        button_layout.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("Load Game")
        self.load_btn.clicked.connect(self.load_game)
        button_layout.addWidget(self.load_btn)
        
        self.quit_btn = QPushButton("Quit")
        self.quit_btn.clicked.connect(self.close)
        button_layout.addWidget(self.quit_btn)
        
        right_panel.addWidget(button_frame)
        
        # Create a scroll area for the right panel
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(right_panel_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setMaximumWidth(sidebar_width)
        
        main_layout.addWidget(scroll_area, 3)
        
        # Set layout margins to create some padding around the entire UI
        main_layout.setContentsMargins(20, 20, 20, 20)
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # Game menu
        game_menu = menubar.addMenu('Game')
        
        new_action = QAction('New Game', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_game)
        game_menu.addAction(new_action)
        
        game_menu.addSeparator()
        
        save_action = QAction('Save Game', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_game)
        game_menu.addAction(save_action)
        
        load_action = QAction('Load Game', self)
        load_action.setShortcut('Ctrl+L')
        load_action.triggered.connect(self.load_game)
        game_menu.addAction(load_action)
        
        game_menu.addSeparator()
        
        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)
        game_menu.addAction(quit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        controls_action = QAction('Controls', self)
        controls_action.triggered.connect(self.show_controls_help)
        help_menu.addAction(controls_action)
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(50)  # 20 FPS
    
    def handle_key_press(self, pygame_key):
        self.game_engine.handle_input(pygame_key)
        # Always update UI after any player input
        self.update_ui()
    
    def update_game(self):
        if self.game_engine.update():
            self.pygame_widget.update()
            # Update UI after each game cycle to ensure stats are always current
            self.update_ui()
        else:
            self.close()
    
    def update_ui(self):
        game_state = self.game_engine.get_game_state()
        self.stats_widget.update_stats(game_state)
        self.message_widget.update_messages(game_state['messages'])
        
        # Handle game over states
        if game_state['game_state'] == 'dead':
            self.message_widget.message_area.append("\n=== GAME OVER ===")
        elif game_state['game_state'] == 'won':
            self.message_widget.message_area.append("\n=== YOU WIN! ===")
    
    def new_game(self):
        if self.game_engine.game_state == "playing":
            reply = QMessageBox.question(
                self, "New Game",
                "Start a new game? Current progress will be lost unless saved.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        self.game_engine = GameEngine()
        self.pygame_widget.game_engine = self.game_engine
        self.update_ui()
    
    def save_game(self):
        """Open save game dialog"""
        if self.game_engine.game_state != "playing":
            QMessageBox.warning(self, "Cannot Save", "Cannot save game when not playing.")
            return
        
        dialog = SaveLoadDialog(self, mode="save")
        if dialog.exec_() == QDialog.Accepted:
            result = dialog.get_result()
            if result:
                success, message = self.game_engine.save_game(
                    result['character_name'], 
                    result['save_name']
                )
                if success:
                    QMessageBox.information(self, "Success", message)
                else:
                    QMessageBox.critical(self, "Error", message)
    
    def load_game(self):
        """Open load game dialog"""
        dialog = SaveLoadDialog(self, mode="load")
        if dialog.exec_() == QDialog.Accepted:
            result = dialog.get_result()
            if result:
                success, message = self.game_engine.load_game(result['filepath'])
                if success:
                    self.pygame_widget.game_engine = self.game_engine
                    self.update_ui()
                    QMessageBox.information(self, "Success", message)
                else:
                    QMessageBox.critical(self, "Error", message)
    
    def show_controls_help(self):
        """Show controls help dialog"""
        help_text = """
MOVEMENT:
• Arrow Keys or hjkl: Move in cardinal directions
• yubn: Diagonal movement (roguelike standard)

ACTIONS:
• . (period): Wait/Rest (skip turn)
• , (comma): Pick up item
• d: Go down stairs
• a: Go up stairs
• p: Use magic portal (when available)

GAME CONTROLS:
• Ctrl+S: Quick save
• Ctrl+N: New game
• Ctrl+L: Load game
• Ctrl+Q: Quit

COMBAT:
• Move into enemies to attack
• Damage = Attack - Defense (minimum 1)
• Turn-based: You move, then all enemies move

TIPS:
• Use walls for protection in combat
• Save health potions for tough fights
• Every level has at least one exit
• Boss enemies appear every 10 levels
• Magic portals appear every 5 levels (skip 5 levels)
        """
        QMessageBox.information(self, "Controls Help", help_text)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
PyQt5 Roguelike Game v2.0

A classic roguelike dungeon crawler with infinite levels, 
boss battles, treasure rooms, and magic portals.

Features:
• Procedurally generated dungeons
• Turn-based combat system
• Character progression
• Save/Load functionality
• Multiple enemy types
• Special level features
• Themed environments

Built with Python, Pygame, and PyQt5.

Enjoy your dungeon crawling adventure!
        """
        QMessageBox.about(self, "About", about_text)
    
    def closeEvent(self, event):
        pygame.quit()
        event.accept()

def main():
    # Suppress QWidget::paintEngine warnings
    import os
    os.environ['QT_LOGGING_RULES'] = "qt.widgets.paintengine=false"
    
    app = QApplication(sys.argv)
    
    # Initialize pygame is now done in MainWindow.__init__
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
