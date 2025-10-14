import os
import sys
import pprint
import urllib.request
import urllib.error
import socket
import traceback
import django  # type: ignore[import]
# If you want stricter local typing for Django modules, install `django-stubs`
# into the workspace virtualenv; otherwise narrow mypy ignores are used here.
from django.conf import settings  # type: ignore[import]
from django.db import connections  # type: ignore[import]

# Ensure project root is on path
PROJECT_ROOT = os.getcwd()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Use the same settings module as manage.py uses (main.ecommerce_project.settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.ecommerce_project.settings')

try:
    django.setup()
except ImportError:
    print('Django is not installed in this environment')
    raise
except Exception:  # pylint: disable=broad-except
    # Keep a broad except here so the helper script can print a usable
    # traceback for debugging in environments where Django setup fails.
    print('Failed to set up Django:')
    traceback.print_exc()
    raise

print('\n== Django settings.DATABASES ==')
pprint.pprint(settings.DATABASES)

# Test DB connection via Django
print('\n== DB connection test (django.connections) ==')
try:
    conn = connections['default']
    conn.ensure_connection()
    print('Django DB connection: SUCCESS')
except Exception:  # pylint: disable=broad-except
    # Keep broad except to give a clear diagnostic when DB connect fails.
    print('Django DB connection: FAILED')
    traceback.print_exc()

# ORM read test: count users if available
print('\n== ORM test: user count ==')
try:
    from django.contrib.auth import get_user_model  # type: ignore[import]

    User = get_user_model()  # type: ignore
    print('User model:', User)
    print('User count:', User.objects.count())
except Exception:  # pylint: disable=broad-except
    # Accept broad exceptions here because the environment may not have
    # auth configured; we want a readable traceback rather than crashing.
    print('ORM test failed:')
    traceback.print_exc()

# HTTP smoke tests
print('\n== HTTP smoke tests ==')
base = 'http://127.0.0.1:8000'
paths = ['/', '/admin/', '/shop/']
for p in paths:
    url = base.rstrip('/') + p
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'test-agent'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = getattr(resp, 'status', None) or resp.getcode()
            print(f'{url} -> {status}')
            body = resp.read(512)
            print('Preview:', body[:200])
    except urllib.error.HTTPError as e:
        print(f'{url} -> HTTPError {e.code}')
    except urllib.error.URLError as e:
        print(f'{url} -> URLError {e.reason}')
    except socket.timeout:
        print(f'{url} -> timeout')
    except Exception:  # pylint: disable=broad-except
        # Catch-all for unexpected errors during HTTP smoke tests; keep
        # traceback for debugging but silence linter warning explicitly.
        print(f'{url} -> other error:')
        traceback.print_exc()

print('\n== Test complete ==')
