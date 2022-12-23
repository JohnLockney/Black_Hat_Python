#!/usr/bin/env python
"""
Black Hat Python: Chapter 5, page 73
very simple GET request

Fine print: this is for "Python version 3"

"""

import urllib.parse
import urllib.request

url = 'http://boodelyboo.com'
with urllib.requet.urlopen(url) as response: # GET request
    content = response. read()

print(content)
