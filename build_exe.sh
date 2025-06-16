#!/bin/bash
echo "Building PyQt5 Roguelike Windows Executable using Wine..."
echo

# Install wine if not already installed
if ! command -v wine &> /dev/null; then
    echo "Wine is not installed. Installing wine..."
    sudo apt-get update
    sudo apt-get install -y wine
fi

# Install Python for Windows using wine
if [ ! -d "$HOME/.wine/drive_c/Python312" ]; then
    echo "Installing Python 3.12 for Windows..."
    wget https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe -O /tmp/python-installer.exe
    wine /tmp/python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
fi

# Create a temporary script to install packages and build
cat > /tmp/build_script.bat << EOF
@echo off
C:\\Python312\\python.exe -m pip install pygame PyQt5 cx_Freeze
C:\\Python312\\python.exe setup.py build
EOF

# Run the build script with wine
wine cmd /c /tmp/build_script.bat

echo
echo "Build complete! The executable can be found in the build directory."
