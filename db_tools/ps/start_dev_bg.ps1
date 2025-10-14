param(
    [string]$Host = '0.0.0.0',
    [int]$Port = 8000
)

$env:USE_POSTGRES = '1'
$env:POSTGRES_DB = 'ecommerce_db'
$env:POSTGRES_USER = 'postgres'
$env:POSTGRES_PASSWORD = 'postgres'
$env:POSTGRES_HOST = '127.0.0.1'
$env:POSTGRES_PORT = '15433'
$repoRoot = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = "$repoRoot;$repoRoot\main"

if (-not (Test-Path -Path (Join-Path $repoRoot 'logs'))) { New-Item -ItemType Directory -Path (Join-Path $repoRoot 'logs') | Out-Null }

$log = Join-Path $repoRoot 'logs\dev_server.log'
Write-Host "Starting dev server; logs -> $log"
Start-Process -FilePath python -ArgumentList "3.10","manage.py","runserver","$Host`:$Port" -WorkingDirectory $repoRoot -RedirectStandardOutput $log -RedirectStandardError $log -NoNewWindow -WindowStyle Hidden -PassThru