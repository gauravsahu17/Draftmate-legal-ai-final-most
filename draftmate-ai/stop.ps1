$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $root '.draftmate-pids'
if (-not (Test-Path $pidFile)) { Write-Host 'No DraftMate PID file found.'; exit 0 }
$ids = (Get-Content $pidFile -Raw).Split(',') | ForEach-Object { [int]$_.Trim() }
$pythonPath = Join-Path $root 'backend/.venv/Scripts/python.exe'
$nodePath = (Get-Command node -ErrorAction SilentlyContinue).Source
$vitePath = Join-Path $root 'frontend/node_modules/vite/bin/vite.js'
foreach ($id in $ids) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $id" -ErrorAction SilentlyContinue
    if (-not $process) { continue }
    $isBackend = $process.ExecutablePath -eq $pythonPath
    $isFrontend = $process.ExecutablePath -eq $nodePath -and $process.CommandLine -like "*$vitePath*"
    if ($isBackend -or $isFrontend) {
        Stop-Process -Id $id -Force
        Write-Host "Stopped DraftMate process $id"
    } else {
        Write-Host "Skipped process $id because it does not match this DraftMate project."
    }
}
Remove-Item -LiteralPath $pidFile -Force
