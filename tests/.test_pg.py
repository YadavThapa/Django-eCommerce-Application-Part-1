import os
import importlib
import socket
import pathlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.ecommerce_project.settings')
try:
    mod = importlib.import_module('main.ecommerce_project.settings')
except Exception as e:
    print('Failed to import settings module:', repr(e))
    raise

DB = getattr(mod, 'DATABASES', {}).get('default', {})
ENGINE = DB.get('ENGINE')
NAME = DB.get('NAME')
USER = DB.get('USER')
PASSWORD = DB.get('PASSWORD')
HOST = DB.get('HOST') or '127.0.0.1'
PORT = DB.get('PORT') or 5432

print('Using DB engine:', ENGINE)
print('DB name:', NAME)
print('DB user:', USER)
print('DB host:', HOST)
print('DB port:', PORT)
print('db.sqlite3 exists:', pathlib.Path('db.sqlite3').exists())

# TCP reachability test
print('\n== TCP reachability test ==')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3.0)
try:
    sock.connect((HOST, int(PORT)))
    print(f'TCP connect to {HOST}:{PORT} OK')
    sock.close()
    tcp_ok = True
except Exception as e:
    print(f'TCP connect to {HOST}:{PORT} failed: {e!r}')
    tcp_ok = False

# Attempt a psycopg2 connection if available
print('\n== psycopg2 connection attempt ==')
try:
    import psycopg2
    from psycopg2 import OperationalError
    try:
        conn = psycopg2.connect(host=HOST, port=PORT, dbname=NAME, user=USER, password=PASSWORD, connect_timeout=5)
        print('psycopg2: connected successfully')
        conn.close()
    except OperationalError as e:
        print('psycopg2: connection failed (OperationalError):', repr(e))
    except Exception as e:
        print('psycopg2: connection attempt raised:', repr(e))
except ImportError:
    print('psycopg2 is not installed in this environment.')

print('\nTest finished.')
