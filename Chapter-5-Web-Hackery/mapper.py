#!/usr/bin/env python
"""
Mapping Open Source Web App Installations (Mapping Wordpress)
BHP: page 77

Note: uses local list of directories to search
URL for testing:
https://wordpress.org/showcase/category/publication/

##################################################
## Made short list of files to look for
└─$ find /tmp/wordpress-dirs
/tmp/wordpress-dirs
/tmp/wordpress-dirs/publication
/tmp/wordpress-dirs/images
/tmp/wordpress-dirs/home
/tmp/wordpress-dirs/index.htm
/tmp/wordpress-dirs/index.html
/tmp/wordpress-dirs/file.txt
/tmp/wordpress-dirs/tmp
/tmp/wordpress-dirs/category
/tmp/wordpress-dirs/category/publication

##################################################
# Example output
└─$ python wordpress-mapper.py
Working on:  index.htm
/index.htm
Working on:  index.html
/index.html
Working on:  file.txt
/file.txt
Press return to continue.
"""

import contextlib
import os
import queue
# import requests
# import sys
# import threading
# import time

FILTERED = [".jpg", ".gif", ".png", ".css"]
TARGET   = "https://wordpress.org/showcase"
THREADS  = 10

answers   = queue.Queue()
web_paths = queue.Queue()

def gather_paths():
    for root, _, files in os.walk('.'):
        for fname in files:
            print("Working on: ", fname)
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
            print('\t', path)
            web_paths.put(path)

@contextlib.contextmanager
def chdir(path):
    """
    On enter, change directory to specified path
    On exit, change directory back to original.
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)

if __name__ == '__main__':
    with chdir("/tmp/wordpress-dirs/"):
        gather_paths()
    input('Press return to continue. ')