$ErrorActionPreference = "Stop"
$taskName = "AIHub-Startup"
$scriptPath = Join-Path $PSScriptRoot "run-startup.ps1"
schtasks /Create /TN $taskName /TR "powershell -ExecutionPolicy Bypass -File `"$scriptPath`"" /SC ONLOGON /RL LIMITED /F
