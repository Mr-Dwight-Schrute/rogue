@echo off
echo Building PyQt5 Roguelike Windows Executable...
echo.

REM Create a virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install required packages
pip install pygame PyQt5 cx_Freeze

REM Build the executable
python setup.py build

echo.
echo Build complete! The executable can be found in the build directory.
pause
