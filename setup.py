import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["pygame", "PyQt5"],
    "excludes": [],
    "include_files": [],
}

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="PyQt5Roguelike",
    version="1.0",
    description="PyQt5 Roguelike Game",
    options={"build_exe": build_exe_options},
    executables=[Executable("main_gui.py", base=base, icon="icon.ico", target_name="PyQt5Roguelike.exe")]
)
