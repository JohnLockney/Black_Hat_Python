#!/usr/bin/env python
"""
##################################################################
# Black Hat Python: page 75
# Find all "a" anchor elements in target page

##################################################################
# Example Output:
#
# main-content -> Skip to main content
# / -> None
# /catalog.htm -> Catalog
# https://nostarch.com/merchandise-0 -> Merchandise
# /blog -> Blog
# https://nostarch.com/early-access-program -> Early Access
# /writeforus -> Write for Us
# /about -> About Us
# /contactus -> Contact Us
# / ->
#
# /catalog.htm -> Catalog
# https://nostarch.com/merchandise-0 -> Merchandise
# /blog -> Blog
# https://nostarch.com/early-access-program -> Early Access
##################################################################
"""

from io import BytesIO
from lxml import etree

import requests

url = 'https://nostarch.com'
r = requests.get(url) # GET
content = r.content # content is of type 'bytes'

parser = etree.HTMLParser()
content = etree.parse(BytesIO(content), parser=parser) # Parse into tree
for link in content.findall('//a'): # find all "a" anchor elements
    print(f"{link.get('href')} -> {link.text}")