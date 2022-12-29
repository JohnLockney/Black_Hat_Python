#!/usr/bin/env python
'''
Using Bing for Burp
BHP: Page 105

Update: API_KEY="YOURKEY"
'''

from burp import IBurpExtender
from burp import IContextMenuFactory

from java.net import URL
from java.util import  ArrayList
from javax.swing import JMenuItem
from thread import start_new_thread

import json
import socket
import urllib

API_KEY  = "YOURKEY"
API_HOST = 'api.coginitive.microsoft.com'

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):  # type: (IBurpExtenderCallbacks) -> None
        self.callbacks = callbacks
        self.helpers   = callbacks.GetHelpers()
        self.context   = None

        # we setup our extension
        callbacks.setExtensionName("BHP Bing")
        callbacks.registerContextMenuFactory(self)

        return

    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem(
            "Send to Bing", actionPerformed=self.bing_menu))
        return menu_list

