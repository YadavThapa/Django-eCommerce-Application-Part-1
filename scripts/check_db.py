import os
import sys
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.ecommerce_project.settings')

try:
    import django

    django.setup()
    from django.db import connections

    conn = connections['default']
    print('Attempting DB connection...')
    conn.ensure_connection()
    print('DB connection OK')
    from django.conf import settings

    print('DB engine:', settings.DATABASES['default'].get('ENGINE'))
    print('DB name:', settings.DATABASES['default'].get('NAME'))
except Exception:
    print('DB connection FAILED')
    traceback.print_exc()
    sys.exit(2)
