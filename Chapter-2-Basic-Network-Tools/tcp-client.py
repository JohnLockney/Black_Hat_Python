#!/usr/bin/env python
'''
tcp client

Example output:

HTTP/1.1 301 Moved Permanently
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>
'''

import socket

target_host  = "www.google.com"
target_port = 80

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))

# send some data
client.send(b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')

# receive some data
response = client.recv(4096)

print(response.decode())
client.close()
