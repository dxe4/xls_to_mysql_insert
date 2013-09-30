import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name = "xtsi",
        version = "1",
        description = "xtsi",
        options = {"build_exe" : {"includes" : "atexit" }},
        executables = [Executable("xtsi.py", base = base)])
