#!/usr/bin/env python
"""
##################################################################
# Black Hat Python: page 75
# Find all "a" anchor elements in target page, parse using BeautifulSoup

##################################################################
# Errors: (works OK on Linux, error on Windows?)
# From cached_properties import Property as property
# ModuleNotFoundError: No module named 'cached_properties'

##################################################################
# Example Output:

/images?FORM=Z9LH -> Images
/videos?FORM=Z9LH1 -> Videos
/shop?FORM=Z9LHS4 -> Shopping
/maps?FORM=Z9LH2 -> Maps
/videos?FORM=Z9LH1 -> Videos
/shop?FORM=Z9LHS4 -> Shopping
/search?q=Bing+translate&FORM=TTAHP1 -> Translate
/maps?FORM=Z9LH2 -> Maps
"""

from b64 import BeautifulSoup as bs
import requests

url = 'http://bing.com'
r   = requests.get(url)

tree= bs(r.text, 'html.parser')  # Parse into tree
for link in tree.find.all('a'):  # Print all 'a' anchor elements
    print(f"{link.get ('href')} --> {link.text}")
