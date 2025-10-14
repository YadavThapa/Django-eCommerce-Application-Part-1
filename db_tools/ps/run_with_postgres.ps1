# Temporarily set Postgres env vars for this PowerShell process and run the Python check script
$env:USE_POSTGRES = '1'
$env:POSTGRES_DB = 'testdb'
$env:POSTGRES_USER = 'testuser'
$env:POSTGRES_PASSWORD = 'testpass'
$env:POSTGRES_HOST = 'localhost'
$env:POSTGRES_PORT = '5432'

Write-Host "Set temporary environment variables for this session:" -ForegroundColor Cyan
Write-Host "USE_POSTGRES=$env:USE_POSTGRES"
Write-Host "POSTGRES_DB=$env:POSTGRES_DB"
Write-Host "POSTGRES_USER=$env:POSTGRES_USER"
Write-Host "POSTGRES_PASSWORD=$env:POSTGRES_PASSWORD"
Write-Host "POSTGRES_HOST=$env:POSTGRES_HOST"
Write-Host "POSTGRES_PORT=$env:POSTGRES_PORT"

# Run the Python check script with the modified environment (these env vars live only for this process)
python3.10 "c:\Users\hemja\OneDrive\Desktop\Last Cleanup\scripts\print_db_config.py"

# Exit; env vars are not persistent beyond this script