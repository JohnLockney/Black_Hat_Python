#!/usr/bin/env python
"""
Stealing Email Credentials
BHP Page: 54

"""

from scapy.all import sniff

def packet_callback(packet):
    print(packet.show())

def main():
    sniff(prn=packet_callback, count=25)

if __name__ == '__main__':
    main()