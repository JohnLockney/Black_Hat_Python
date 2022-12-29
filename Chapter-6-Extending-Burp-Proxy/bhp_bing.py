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

    def bing_menu(self,event):
        '''grab teh details of what the user clicked
        :return: None
        '''
        http_traffic = self.context.getSelectedMessages()

        print("%d requests highlighted" % len(http_traffic))

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host         = http_service.getHost()

            print("User selected host: %s" % host)
            self.bing_search(host)

        return

    def bing_search(self,host):
        ''' check if we have an IP or hostname '''
        try:
            is_ip = bool(socket.inet_aton(host))
        except socket.error:
            is_ip = False

        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain =  True

        start_new_thread(self.bing_query, ('ip:%s' % ip_address,))

        if domain:
            start_new_thread(self.bing_query, ('domain:%s' % host,))

    def bing_query(self,bing_query_string):
        print('Performing Bing search: %s' % bing_query_string)
        http_request = 'Get https://%s/bing/v7.0/search?' % API_HOST
        # encode our query
        http_request += 'q=%s HTTP/1.1\r\n' % urllib.quote(bing_query_string)
        http_request += 'host: %\r\r' % API_HOST
        http_request += 'Connection:close\r\n'
        http_request += 'Ocp-Apim-Subscription_key: %s\r\n' % API_KEY
        http_request += 'User-Agent: Black Hat Python \r\n\r\n'

        json_body = self.callbacks.makeHttpRequest(
            API_HOST, 443, True, http_request).tostring()
        json_body = json_body.split('\r\n\r\n', 1)[1]

        try:
            response = json.loads(json_body)
        except (TypeError, ValueError) as err:
            print('No Results from Bing: %s' % err)
        else:
            sites = list()
            if response.get('webPages'):
                sites = response['webPages']['value']
            if len(sites):
                for site in sites:
                    print('*'*100)
                    print('Name %s       ' % site['name'])
                    print('URL: %s       ' % site['url'])
                    print('Descripion: %r' % site['snippet'])
                    print('*'*100)

                    java_url = URL(site['url'])
                    if not self.callbacks.isInScope(java_url):
                        print('Adding %s to Burp scope' % site['url'])
                        self.callbacks.includeInScope(java_url)
                    else:
                        print('Empty response from Bing. : %s'
                              % bing_query_string)
        return





