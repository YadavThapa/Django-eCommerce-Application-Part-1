# Wrapper: forward to the canonical script in db_tools/ps/
$script = Join-Path (Split-Path -Parent $PSScriptRoot) '..\db_tools\ps\print_env.ps1' -Resolve
& $script @Args
