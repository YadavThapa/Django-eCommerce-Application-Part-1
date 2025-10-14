# Wrapper: forward to canonical script in db_tools/ps/
$script = Join-Path (Split-Path -Parent $PSScriptRoot) '..\db_tools\ps\start_dev_bg.ps1' -Resolve
& $script @Args
