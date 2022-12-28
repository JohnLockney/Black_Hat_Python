#!/usr/bin/env python
'''
Turning website content into password gold
Page: 110

# Requires: pip install HTMLParser
'''

from burp import IBurpExtender
from burp import IContextMenuFactory

from java.util import ArrayList
from javax.swing import JMenuItem

from datetime import datetime
from HTMLParser import HTMLParser

import re

class TagStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = []

        def handle_data(self, data):
            self.page_text.append(data)

        def handle_comment(self, data):
            self.page_text.append(data)

        def strip(self, html):
            self.feed(html)
            return " ".join(self.page_text)

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):  # type: (IBurpExtenderCallbacks) -> None

        self._callbacks = callbacks
        self._helpers   = callbacks.getHelpers()
        self.context    = None
        self.hosts      = set()

        # start with something we know is common
        self.wordlist = set(["password"])

        # we setup our extension
        callbacks.setExtensionName("BHP Wordlist")
        callbacks.registerContextMenuFactory(self)

        return

    def createMenuItems(self, context_menu):
        self.content = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem(
            "Create Wordlist", actionPerformed=self.wordlist_menu))

        return menu_list

