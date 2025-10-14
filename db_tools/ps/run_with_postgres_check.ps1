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

Write-Host "Using temporary env vars:" -ForegroundColor Cyan
Write-Host "POSTGRES_DB=$env:POSTGRES_DB"
Write-Host "POSTGRES_USER=$env:POSTGRES_USER"
Write-Host "POSTGRES_HOST=$env:POSTGRES_HOST"
Write-Host "POSTGRES_PORT=$env:POSTGRES_PORT"

$repoRoot = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = if ($env:PYTHONPATH) { $repoRoot + ';' + $env:PYTHONPATH } else { $repoRoot }
Write-Host "PYTHONPATH set to: $env:PYTHONPATH"

python3.10 "${repoRoot}\manage.py" check --database default