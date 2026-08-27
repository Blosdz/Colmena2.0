$ErrorActionPreference = "Stop"

$Root     = $PSScriptRoot
$Backend  = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$LogDir   = Join-Path $Root "logs"
$PidDir   = Join-Path $Root "run"
$PgCtl    = "D:\APPTHESIS\.tools\pgsql\bin\pg_ctl.exe"
$PgData   = "D:\APPTHESIS\.tools\pgsql\data"
$Python   = Join-Path $Backend ".venv\Scripts\python.exe"

New-Item -ItemType Directory -Force -Path $LogDir, $PidDir | Out-Null

function Stop-StaleProcess([string]$Name) {
    $pidFile = Join-Path $PidDir "$Name.pid"
    if (Test-Path $pidFile) {
        $oldPid = [int](Get-Content $pidFile -ErrorAction SilentlyContinue)
        if (Get-Process -Id $oldPid -ErrorAction SilentlyContinue) { taskkill.exe /PID $oldPid /T /F 2>$null | Out-Null }
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    }
}

function Wait-Http([string]$Url, [int]$TimeoutSeconds = 30) {
    for ($i = 0; $i -lt $TimeoutSeconds; $i++) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) { return $true }
        } catch { Start-Sleep -Seconds 1 }
    }
    return $false
}

if (-not (Get-Command cloudflared -ErrorAction SilentlyContinue)) { throw "cloudflared no está instalado o no está disponible en PATH." }
if (-not (Test-Path $PgCtl)) { throw "No se encontró pg_ctl.exe en $PgCtl" }
if (-not (Test-Path $Python)) { throw "No se encontró el entorno Python en $Python" }

Write-Host "[1/5] PostgreSQL..." -ForegroundColor Cyan
& $PgCtl -D $PgData status 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { & $PgCtl -D $PgData start; Start-Sleep -Seconds 3 } else { Write-Host "  ya estaba corriendo." }

Stop-StaleProcess "cloudflared"
Stop-StaleProcess "frontend"
Stop-StaleProcess "backend"

Write-Host "[2/5] Migraciones Alembic..." -ForegroundColor Cyan
Push-Location $Backend
try { & $Python -m alembic upgrade head } finally { Pop-Location }

Write-Host "[3/5] Backend (FastAPI, puerto 8000)..." -ForegroundColor Cyan
$backendCommand = "`"$Python`" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > `"$LogDir\backend.log`" 2>&1"
$backendProc = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $backendCommand -WorkingDirectory $Backend -WindowStyle Hidden -PassThru
$backendProc.Id | Set-Content (Join-Path $PidDir "backend.pid")
if (-not (Wait-Http "http://127.0.0.1:8000/health")) { throw "FastAPI no respondió. Revisa $LogDir\backend.log" }

Write-Host "[4/5] Frontend (Vite, puerto 5174)..." -ForegroundColor Cyan
$frontendCommand = "npm run dev -- --host 0.0.0.0 --port 5174 > `"$LogDir\frontend.log`" 2>&1"
$frontendProc = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $frontendCommand -WorkingDirectory $Frontend -WindowStyle Hidden -PassThru
$frontendProc.Id | Set-Content (Join-Path $PidDir "frontend.pid")
if (-not (Wait-Http "http://127.0.0.1:5174/")) { throw "Vite no respondió. Revisa $LogDir\frontend.log" }

Write-Host "[5/5] Cloudflare Tunnel → Vite :5174..." -ForegroundColor Cyan
$tunnelCommand = "cloudflared tunnel --url http://127.0.0.1:5174 > `"$LogDir\cloudflared.log`" 2>&1"
$tunnelProc = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $tunnelCommand -WindowStyle Hidden -PassThru
$tunnelProc.Id | Set-Content (Join-Path $PidDir "cloudflared.pid")

$tunnelUrl = $null
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    $log = Get-Content (Join-Path $LogDir "cloudflared.log") -Raw -ErrorAction SilentlyContinue
    if ($log -match 'https://[a-zA-Z0-9-]+\.trycloudflare\.com') { $tunnelUrl = $Matches[0]; break }
}

Write-Host ""
if ($tunnelUrl) {
    Write-Host "=====================================================" -ForegroundColor Green
    Write-Host " Colmena corriendo en background."
    Write-Host " URL pública:     $tunnelUrl"
    Write-Host " Backend local:   http://127.0.0.1:8000/docs"
    Write-Host " Frontend local:  http://127.0.0.1:5174"
    Write-Host " Proxy API:       $tunnelUrl/api/* → FastAPI :8000"
    Write-Host "=====================================================" -ForegroundColor Green
} else { Write-Host "No se detectó la URL del tunnel. Revisa $LogDir\cloudflared.log" -ForegroundColor Yellow }
Write-Host "Logs: $LogDir"
Write-Host "Detener: powershell -ExecutionPolicy Bypass -File `"$(Join-Path $Root 'stop-colmena.ps1')`""
