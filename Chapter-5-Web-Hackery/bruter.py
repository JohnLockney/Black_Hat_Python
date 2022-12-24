#!/usr/bin/env python
"""
Brute Forcing Directories and File Locations
BHP: page 82

#######################################################
Note: wordlist recommended in the book is not found at
wget https://www.netsparker.com/s/research/SVNDigger.zip
site has been renamed: https://www.invicti.com/blog/web-security/svn-digger-better-lists-for-forced-browsing/
but, file is not available

For testing, modified to use dirbuster small list: = "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"

#######################################################
# Test Results:

Success (200: http://testphp.vulnweb.com/#.php
Success (200: http://testphp.vulnweb.com/#.bak
Success (200: http://testphp.vulnweb.com/#/
Success (200: http://testphp.vulnweb.com/#.orig..
Success (200: http://testphp.vulnweb.com/#.inc
Success (200: http://testphp.vulnweb.com/#/
Success (200: http://testphp.vulnweb.com/#.php
Success (200: http://testphp.vulnweb.com/#.inc
Success (200: http://testphp.vulnweb.com/index.php
Success (200: http://testphp.vulnweb.com/#.bak.
Success (200: http://testphp.vulnweb.com/#.orig
Success (200: http://testphp.vulnweb.com/index.bak.....
Success (200: http://testphp.vulnweb.com/images/

"""

import queue
import requests
import threading
import sys

AGENT      = 'Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0'
EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
TARGET     = "http://testphp.vulnweb.com"
THREADS    = 50
#WORDLIST   = "./wordlist/wordlist.txt"
WORDLIST   = "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"

def get_words(resume=None):
    ''' stub '''
    def extended_words(word):
        if "." in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}/')

        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')

    with open(WORDLIST) as f:
        raw_words = f.read()

    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extended_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
        else:
            print(word)
            extended_words(word)
    return words

def dir_bruter(words):
    headers = {'User-Agent': AGENT}
    while not words.empty():
        url = f'{TARGET}{words.get()}'
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x');sys.stderr.flush()
            continue

        if r.status_code == 200:
            print(f'\nSuccess ({r.status_code}: {url}')
        elif r.status_code == 404:
            sys.stderr.write('.');sys.stderr.flush()
        else:
            print(f'{r.status_code} => {url}')

if __name__ == '__main__':
    words = get_words()
    print('Press return to continue.')
    sys.stdin.readline()
    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words,))
        t.start()