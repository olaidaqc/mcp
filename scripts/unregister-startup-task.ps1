$ErrorActionPreference = "Stop"
$taskName = "AIHub-Startup"
schtasks /Delete /TN $taskName /F
