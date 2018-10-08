#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 19:06:24 2018

@author: ft
"""

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "LinkedInAssist",
        version = "1.1",
        description = "Asystent Jana",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])