from cx_Freeze import setup, Executable
includefiles = []
includes = []
packages = ['os', 'time', 'socket']


setup(name = "SCPSL Monitor",
      version = "1.3.1",
      description = "SCP:SL Monitor Application File",
      executables = [Executable("shell.py")])