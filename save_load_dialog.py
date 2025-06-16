from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                            QListWidgetItem, QPushButton, QLabel, QLineEdit,
                            QMessageBox, QInputDialog, QFrame, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from save_manager import SaveManager
import os

class SaveLoadDialog(QDialog):
    def __init__(self, parent=None, mode="save"):
        super().__init__(parent)
        self.mode = mode  # "save" or "load"
        self.save_manager = SaveManager()
        self.selected_save = None
        self.init_ui()
        self.refresh_save_list()
    
    def init_ui(self):
        self.setWindowTitle("Save Game" if self.mode == "save" else "Load Game")
        self.setModal(True)
        self.resize(600, 500)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QListWidget {
                background-color: #1e1e1e;
                border: 1px solid #555555;
                color: #ffffff;
                selection-background-color: #404040;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333333;
            }
            QListWidget::item:selected {
                background-color: #404040;
            }
            QPushButton {
                background-color: #404040;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 8px 16px;
                color: #ffffff;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #353535;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666666;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 8px;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #555555;
                color: #ffffff;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Save Game" if self.mode == "save" else "Load Game")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Save list
        list_label = QLabel("Saved Games:")
        list_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(list_label)
        
        self.save_list = QListWidget()
        self.save_list.itemClicked.connect(self.on_save_selected)
        self.save_list.itemDoubleClicked.connect(self.on_double_click)
        layout.addWidget(self.save_list)
        
        # Save details
        details_label = QLabel("Save Details:")
        details_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(details_label)
        
        self.details_text = QTextEdit()
        self.details_text.setMaximumHeight(100)
        self.details_text.setReadOnly(True)
        layout.addWidget(self.details_text)
        
        # Save name input (for save mode)
        if self.mode == "save":
            name_layout = QHBoxLayout()
            name_layout.addWidget(QLabel("Save Name:"))
            self.name_input = QLineEdit()
            self.name_input.setPlaceholderText("Enter save name...")
            name_layout.addWidget(self.name_input)
            layout.addLayout(name_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_save_list)
        button_layout.addWidget(self.refresh_btn)
        
        if self.mode == "load":
            self.delete_btn = QPushButton("Delete")
            self.delete_btn.clicked.connect(self.delete_save)
            self.delete_btn.setEnabled(False)
            button_layout.addWidget(self.delete_btn)
        
        button_layout.addStretch()
        
        self.action_btn = QPushButton("Save" if self.mode == "save" else "Load")
        self.action_btn.clicked.connect(self.perform_action)
        if self.mode == "load":
            self.action_btn.setEnabled(False)
        button_layout.addWidget(self.action_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def refresh_save_list(self):
        """Refresh the list of save files"""
        self.save_list.clear()
        save_files = self.save_manager.get_save_files()
        
        if not save_files:
            item = QListWidgetItem("No saved games found")
            item.setFlags(Qt.NoItemFlags)
            self.save_list.addItem(item)
            return
        
        for save_info in save_files:
            # Create display text
            display_text = f"{save_info['character_name']} - Level {save_info['level']}"
            display_text += f" (Dungeon {save_info['dungeon_level']})"
            display_text += f" - {save_info['gold']} gold"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, save_info)
            self.save_list.addItem(item)
    
    def on_save_selected(self, item):
        """Handle save file selection"""
        save_info = item.data(Qt.UserRole)
        if save_info:
            self.selected_save = save_info
            self.update_details(save_info)
            
            if self.mode == "load":
                self.action_btn.setEnabled(True)
                self.delete_btn.setEnabled(True)
            elif self.mode == "save":
                # Pre-fill save name with existing name
                base_name = save_info['filename'].replace('.json', '')
                self.name_input.setText(base_name)
    
    def on_double_click(self, item):
        """Handle double-click on save file"""
        if self.mode == "load" and item.data(Qt.UserRole):
            self.perform_action()
    
    def update_details(self, save_info):
        """Update the details display"""
        details = f"Character: {save_info['character_name']}\n"
        details += f"Level: {save_info['level']}\n"
        details += f"Dungeon Level: {save_info['dungeon_level']}\n"
        details += f"Deepest Level: {save_info['max_dungeon_level']}\n"
        details += f"Gold: {save_info['gold']}\n"
        details += f"Saved: {save_info['timestamp']}\n"
        
        if save_info['playtime'] > 0:
            hours = save_info['playtime'] // 3600
            minutes = (save_info['playtime'] % 3600) // 60
            if hours > 0:
                details += f"Playtime: {int(hours)}h {int(minutes)}m"
            else:
                details += f"Playtime: {int(minutes)}m"
        
        self.details_text.setText(details)
    
    def perform_action(self):
        """Perform save or load action"""
        if self.mode == "save":
            self.save_game()
        else:
            self.load_game()
    
    def save_game(self):
        """Save the current game"""
        save_name = self.name_input.text().strip()
        if not save_name:
            QMessageBox.warning(self, "Warning", "Please enter a save name.")
            return
        
        # Check if file already exists
        filename = save_name if save_name.endswith('.json') else save_name + '.json'
        filepath = os.path.join(self.save_manager.save_directory, filename)
        
        if os.path.exists(filepath):
            reply = QMessageBox.question(
                self, "Overwrite Save",
                f"A save file named '{save_name}' already exists. Overwrite it?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        # Get character name
        character_name, ok = QInputDialog.getText(
            self, "Character Name", "Enter character name:", text="Hero"
        )
        if not ok:
            character_name = "Hero"
        
        self.result_data = {
            'action': 'save',
            'save_name': save_name,
            'character_name': character_name
        }
        self.accept()
    
    def load_game(self):
        """Load the selected game"""
        if not self.selected_save:
            QMessageBox.warning(self, "Warning", "Please select a save file to load.")
            return
        
        self.result_data = {
            'action': 'load',
            'filepath': self.selected_save['filepath'],
            'save_info': self.selected_save
        }
        self.accept()
    
    def delete_save(self):
        """Delete the selected save file"""
        if not self.selected_save:
            return
        
        reply = QMessageBox.question(
            self, "Delete Save",
            f"Are you sure you want to delete '{self.selected_save['character_name']}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.save_manager.delete_save(self.selected_save['filepath'])
            if success:
                QMessageBox.information(self, "Success", "Save file deleted successfully.")
                self.refresh_save_list()
                self.details_text.clear()
                self.action_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
            else:
                QMessageBox.critical(self, "Error", message)
    
    def get_result(self):
        """Get the result of the dialog"""
        return getattr(self, 'result_data', None)
