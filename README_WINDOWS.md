# Building PyQt5 Roguelike for Windows

This document explains how to build a Windows executable for the PyQt5 Roguelike game.

## Option 1: Building on Windows

If you're on a Windows machine, follow these steps:

1. Make sure you have Python 3.8 or newer installed
2. Run the `build_exe.bat` script by double-clicking it
3. Wait for the build process to complete
4. The executable will be in the `build\exe.win-amd64-3.x` directory (where 3.x is your Python version)
5. Copy the entire directory to distribute the game

## Option 2: Building with PyInstaller

PyInstaller is an alternative that might work better in some environments:

1. Run: `python pyinstaller_build.py`
2. The executable will be created in the `dist` directory
3. This creates a single executable file that contains everything needed

## Option 3: Building on Linux for Windows (Cross-compilation)

If you're on Linux and want to build a Windows executable:

1. Make sure you have Wine installed
2. Make the build script executable: `chmod +x build_exe.sh`
3. Run the script: `./build_exe.sh`
4. The executable will be in the `build\exe.win-amd64-3.x` directory

## Running the Game

Once built, you can run the game by:

1. Double-clicking the `PyQt5Roguelike.exe` file
2. The game should start without requiring Python to be installed

## Troubleshooting

If you encounter issues:

1. Make sure all dependencies are installed: `pip install pygame PyQt5 cx_Freeze`
2. Try the PyInstaller method if cx_Freeze doesn't work
3. Check that your Python version is compatible (3.8 or newer recommended)
4. If using Wine, ensure you have a recent version installed

## Distribution

To distribute the game:

1. For cx_Freeze: Copy the entire build directory
2. For PyInstaller: Just share the single .exe file in the dist directory
3. Users don't need to install Python or any dependencies
