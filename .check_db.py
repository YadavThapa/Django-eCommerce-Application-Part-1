import os
import sys
import pathlib
print('PWD=', pathlib.Path.cwd())
print('ENV DB_ENGINE=', os.environ.get('DB_ENGINE'))
print('ENV DB_NAME=', os.environ.get('DB_NAME'))
print('ENV DB_USER=', os.environ.get('DB_USER'))
print('ENV DB_PASSWORD=', os.environ.get('DB_PASSWORD'))
print('ENV DB_HOST=', os.environ.get('DB_HOST'))
print('ENV DB_PORT=', os.environ.get('DB_PORT'))
print('ENV DJANGO_SETTINGS_MODULE=', os.environ.get('DJANGO_SETTINGS_MODULE'))
# Use the default settings module used by manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE','main.ecommerce_project.settings')
try:
    import django
    django.setup()
    from django.conf import settings
    print('DJANGO settings module:', settings.SETTINGS_MODULE)
    print('DATABASES=', settings.DATABASES)
except Exception as e:
    print('Django import/setup failed:', repr(e))
    # Fallback: import settings module directly
    try:
        import importlib
        mod = importlib.import_module('main.ecommerce_project.settings')
        print('Loaded module main.ecommerce_project.settings')
        print('Module DB_ENGINE:', getattr(mod, 'DB_ENGINE', None))
        print('Module DB_NAME:', getattr(mod, 'DB_NAME', None))
        print('Module DB_USER:', getattr(mod, 'DB_USER', None))
        print('Module DB_PASSWORD:', getattr(mod, 'DB_PASSWORD', None))
        print('Module DB_HOST:', getattr(mod, 'DB_HOST', None))
        print('Module DB_PORT:', getattr(mod, 'DB_PORT', None))
        if hasattr(mod, 'DATABASES'):
            print('Module DATABASES:', mod.DATABASES)
        else:
            print('Module has no DATABASES attribute')
    except Exception as e2:
        print('Fallback import failed:', repr(e2))
print('db.sqlite3 exists at repo root:', pathlib.Path('db.sqlite3').exists())
print('db.sqlite3 exists at explicit path:', pathlib.Path(r'C:/Users/hemja/OneDrive/Desktop/Last Cleanup/db.sqlite3').exists())
