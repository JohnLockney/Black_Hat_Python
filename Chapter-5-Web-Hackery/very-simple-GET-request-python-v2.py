#!/usr/bin/env python
"""
Black Hat Python: Chapter 5, page 72
very simple GET request

Fine print: this is for "Python version 2"

"""

import urllib2
url = 'https://www.nostarch.com'
response = urllib2.urlopen(url) # GET request
print(response.read())
response.close()
