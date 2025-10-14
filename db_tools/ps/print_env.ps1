# Print Postgres-related environment variables for this project
$names = @('USE_POSTGRES','POSTGRES_DB','POSTGRES_USER','POSTGRES_PASSWORD','POSTGRES_HOST','POSTGRES_PORT')
foreach ($n in $names) {
    $v = [Environment]::GetEnvironmentVariable($n)
    if ($v -and $v -ne "") {
        Write-Host "$n=$v"
    } else {
        Write-Host "$n is not set"
    }
}
# Also show DJANGO_SETTINGS_MODULE if present
$jsm = [Environment]::GetEnvironmentVariable('DJANGO_SETTINGS_MODULE')
if ($jsm) { Write-Host "DJANGO_SETTINGS_MODULE=$jsm" } else { Write-Host "DJANGO_SETTINGS_MODULE is not set" }