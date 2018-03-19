import sys
from cx_Freeze import setup, Executable
includefiles = []
includes = []
packages = ['os', 'time', 'socket']


setup(name = "SCPSL Monitor" ,
      version = "1.1" ,
      description = "SIMPLE SSH SENDER FOR SCPSL" ,
      executables = [Executable("shell.py")])