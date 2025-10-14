import os
import sys
import pprint
import urllib.request
import urllib.error
import socket

# Ensure project root is on path
PROJECT_ROOT = os.getcwd()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Use top-level ecommerce_project.settings (keeps previous behavior)
# The DJANGO_SETTINGS_MODULE must be set before importing django; linters
# will normally flag imports not at top of file (E402). We keep this order
# intentionally and silence E402 locally where needed below.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')

try:
    # pylint: disable=import-outside-toplevel
    import django

    django.setup()
except Exception:  # pylint: disable=broad-except
    print('Failed to set up Django')
    raise

# These imports intentionally come after DJANGO_SETTINGS_MODULE is set.
# ruff/flake8 may report E402; it is acceptable here because Django
# requires settings to be configured before importing these modules.
from django.conf import settings  # noqa: E402
from django.db import connections  # noqa: E402

print('\n== Django settings.DATABASES ==')
pprint.pprint(settings.DATABASES)

# Test DB connection via Django
print('\n== DB connection test (django.connections) ==')
try:
    conn = connections['default']
    conn.ensure_connection()
    print('Django DB connection: SUCCESS')
except Exception:  # pylint: disable=broad-except
    print('Django DB connection: FAILED')
    import traceback

    traceback.print_exc()

# ORM read test: count users if available
print('\n== ORM test: user count ==')
try:
    from django.contrib.auth import get_user_model  # type: ignore[import]

    User = get_user_model()
    print('User model:', User)
    print('User count:', User.objects.count())
except Exception:  # pylint: disable=broad-except
    print('ORM test failed')

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
            # read small preview
            body = resp.read(512)
            print('Preview:', body[:200])
    except urllib.error.HTTPError as e:
        print(f'{url} -> HTTPError {e.code}')
    except urllib.error.URLError as e:
        print(f'{url} -> URLError {e.reason}')
    except socket.timeout:
        print(f'{url} -> timeout')
    except Exception as exc:  # pylint: disable=broad-except
        print(f'{url} -> other error:', exc)

print('\n== Test complete ==')
