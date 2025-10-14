<#
Temporary helper to run the Django development server with Postgres env vars for this PowerShell process.
This script sets the env vars for the current session only, then runs `python manage.py runserver`.
If you don't have a reachable Postgres instance, Django may fail to connect; the script demonstrates how to start with Postgres.
#>

param(
    [string]$DB_NAME = 'testdb',
    [string]$DB_USER = 'testuser',
    [string]$DB_PASS = 'testpass',
    [string]$DB_HOST = 'localhost',
    [string]$DB_PORT = '5432'
)

$env:USE_POSTGRES = '1'
$env:POSTGRES_DB = $DB_NAME
$env:POSTGRES_USER = $DB_USER
$env:POSTGRES_PASSWORD = $DB_PASS
$env:POSTGRES_HOST = $DB_HOST
$env:POSTGRES_PORT = $DB_PORT

Write-Host "Starting Django dev server with temporary Postgres env vars:" -ForegroundColor Cyan
Write-Host "POSTGRES_DB=$env:POSTGRES_DB"
Write-Host "POSTGRES_USER=$env:POSTGRES_USER"
Write-Host "POSTGRES_HOST=$env:POSTGRES_HOST"
Write-Host "POSTGRES_PORT=$env:POSTGRES_PORT"

# Add repo root to PYTHONPATH to improve imports
$repoRoot = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = if ($env:PYTHONPATH) { $repoRoot + ';' + $env:PYTHONPATH } else { $repoRoot }
Write-Host "PYTHONPATH set to: $env:PYTHONPATH"

# Run manage.py runserver (this will run in the foreground)
python3.10 "${repoRoot}\manage.py" runserver

# When the script exits, the environment changes are gone (they were only in this process)