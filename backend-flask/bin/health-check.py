#!/usr/bin/env python3

import urllib.request

try:
    response = urllib.request.urlopen("http://localhost:4567/api/health-check")
except Exception as ex:
    print(ex)
    exit(1)


if response.getcode() == 200:
    print("Flask server is running")
else:
    print("Flask server is not running")
    exit(1)
