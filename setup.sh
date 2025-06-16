#!/bin/bash

echo "Setting up PyQt5 Roguelike Game..."

# Check if pygame is installed
python3 -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing pygame..."
    pip3 install pygame
else
    echo "pygame is already installed!"
fi

# Check if PyQt5 is installed
python3 -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing PyQt5..."
    pip3 install PyQt5
else
    echo "PyQt5 is already installed!"
fi

echo "Setup complete! Run the game with: python3 main_gui.py"
