# Wrapper: forward to canonical script in db_tools/ps/
$script = Join-Path (Split-Path -Parent $PSScriptRoot) '..\db_tools\ps\run_with_postgres.ps1' -Resolve
& $script @Args
