"""
Alternative build script using PyInstaller instead of cx_Freeze
This might work better in some environments
"""

import os
import subprocess
import sys
import platform

def main():
    print("Building PyQt5 Roguelike Windows Executable using PyInstaller...")
    
    # Install PyInstaller if not already installed
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build the executable
    subprocess.call([
        sys.executable, 
        "-m", 
        "PyInstaller",
        "--name=PyQt5Roguelike",
        "--onefile",
        "--windowed",
        "--add-data=README.md;.",
        "main_gui.py"
    ])
    
    print("\nBuild complete! The executable can be found in the dist directory.")

if __name__ == "__main__":
    main()
