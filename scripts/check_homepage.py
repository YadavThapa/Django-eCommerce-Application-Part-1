import os
import sys
import time
import urllib.request

# Assumes the dev server is running on http://127.0.0.1:8000/
URL = os.environ.get('CHECK_URL', 'http://127.0.0.1:8000/')

try:
    with urllib.request.urlopen(URL, timeout=5) as resp:
        print('HTTP', resp.status)
        body = resp.read(200)
        print('Body (first 200 bytes):')
        print(body.decode(errors='replace'))
except Exception as e:
    print('Request failed:', e)
    sys.exit(2)
