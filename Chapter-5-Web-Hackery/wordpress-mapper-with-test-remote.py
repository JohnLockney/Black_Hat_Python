#!/usr/bin/env python
"""
mapper.py (with remote function: testing a live target)
BHP: page  80

##########################################################################
# Test output
$ python wordpress-mapper-with-test-remote.py
Working on:  index.htm
         /index.htm
Working on:  index.html
         /index.html
Working on:  file.txt
         /file.txt
Press return to continue.
Spawning thread 0
Spawning thread 1
Spawning thread 2
Spawning thread 3
Spawning thread 4
Spawning thread 5
Spawning thread 6
Spawning thread 7
Spawning thread 8
Spawning thread 9
x++done

└─$ ls -tlr
-rw-r--r-- 1 kali kali 1786 Dec 24 15:11 wordpress-mapper.py
-rw-r--r-- 1 kali kali 2559 Dec 24 15:18 wordpress-mapper-with-test-remote.py
-rw-r--r-- 1 kali kali   83 Dec 24 15:18 myanswers.txt

└─$ cat myanswers.txt
https://wordpress.org/showcase/index.html
https://wordpress.org/showcase/index.htm
"""

import contextlib
import os
import queue
import requests
import sys
import threading
import time

#FILTERED = [".jpg", ".gif", ".png", "css"]
FILTERED = ['.test']
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


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{TARGET}{path}'
        time.sleep(2) # your target may have throttling/lockout
        r = requests.get(url)
        if r.status_code == 200:
            answers.put(url)
            sys.stdout.write('+')
        else:
            sys.stdout.write('x')
        sys.stdout.flush()

def run():
    mythreads = list()
    for i in range(THREADS):
        print(f'Spawning thread {i}')
        t = threading.Thread(target=test_remote)
        mythreads.append(t)
        t.start()

    for thread in mythreads:
        thread.join()


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

    run()
    with open('myanswers.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
    print('done')