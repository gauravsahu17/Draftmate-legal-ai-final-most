$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root 'backend'
$frontend = Join-Path $root 'frontend'
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python 3.11+ is required.' }
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw 'Node.js 20+ is required.' }
if (-not (Test-Path (Join-Path $backend '.venv'))) { python -m venv --without-pip (Join-Path $backend '.venv') }
$py = Join-Path $backend '.venv\Scripts\python.exe'
$temp = Join-Path $backend '.pip-tmp'
New-Item -ItemType Directory -Force $temp | Out-Null
$env:TEMP = $temp
$env:TMP = $temp
python -m pip --python $py install -r (Join-Path $backend 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Backend dependency installation failed.' }
if (-not (Test-Path (Join-Path $frontend 'node_modules'))) { Push-Location $frontend; npm install; if ($LASTEXITCODE -ne 0) { Pop-Location; throw 'Frontend dependency installation failed.' }; Pop-Location }
$api = Start-Process -FilePath $py -ArgumentList @('-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8000') -WorkingDirectory $backend -PassThru
$node = (Get-Command node).Source
$vite = Join-Path $frontend 'node_modules/vite/bin/vite.js'
$web = Start-Process -FilePath $node -ArgumentList ('"{0}" --host 127.0.0.1' -f $vite) -WorkingDirectory $frontend -PassThru
Set-Content -Path (Join-Path $root '.draftmate-pids') -Value "$($api.Id),$($web.Id)"
Start-Sleep -Seconds 3
if ($api.HasExited) { throw 'Backend failed to start. Check the backend terminal output.' }
if ($web.HasExited) { throw 'Frontend failed to start. Check Node.js and frontend dependencies.' }
Write-Host 'Frontend: http://127.0.0.1:5173' -ForegroundColor Green
Write-Host 'Backend:  http://127.0.0.1:8000/health' -ForegroundColor Green
Write-Host 'Stop with .\stop.ps1' -ForegroundColor Yellow
