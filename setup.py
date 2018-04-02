application_title = "CICCUDB"
main_python_file = "pyqt.py"
include_files = ["logo.jpg","exit.png","tcl86t.dll","tk86t.dll"]
packages = ["pyqt","os","pyperclip","tkinter","sys","PyQt5"]
your_name = "Louis Davies"
program_description = "DB App"
icon = "icon.ico"
import sys, os

from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = "C:\\Users\\Louis\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Louis\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

base = None
if sys.platform == "win32":
	base = "Win32GUI"

executables = [Executable(main_python_file,base=base)]

setup(name = application_title,
	version = "0",
	description = program_description,
	author = your_name,
	options = {"build_exe":{"include_files":include_files,"packages":packages}},
		executables=executables)