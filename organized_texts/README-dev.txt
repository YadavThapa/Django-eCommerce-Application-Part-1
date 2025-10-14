Dev notes: running with PostgreSQL

1) Temporary (per-session) helper
- Use the provided PowerShell helper to run the dev server with Postgres env vars for that session only:

  powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\start_dev_with_postgres.ps1"

  You can supply parameters if needed, for example:

  powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\start_dev_with_postgres.ps1" -DB_NAME mydb -DB_USER myuser -DB_PASS mypass -DB_HOST dbhost -DB_PORT 5432

2) Permanent (PowerShell profile)
- To persist variables for all interactive PowerShell sessions, add lines like the following to your PowerShell profile (open with `notepad $PROFILE`):

  $env:USE_POSTGRES = '1'
  $env:POSTGRES_DB = 'mydb'
  $env:POSTGRES_USER = 'myuser'
  $env:POSTGRES_PASSWORD = 'mypassword'
  $env:POSTGRES_HOST = 'db.example.com'
  $env:POSTGRES_PORT = '5432'

3) Notes
- Ensure the Postgres server is reachable from your machine and credentials are valid before attempting to run migrations or the dev server with Postgres.
- The helper script adds the project root to PYTHONPATH to reduce import issues when running from the scripts folder.
- If you want me to run the helper script now and try to start the dev server, say so — but if Postgres isn't running or reachable you'll get a DB connection error from Django.
