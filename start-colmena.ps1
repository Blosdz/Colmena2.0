$ErrorActionPreference = "Stop"

$PgCtl    = "D:\APPTHESIS\.tools\pgsql\bin\pg_ctl.exe"
$PgData   = "D:\APPTHESIS\.tools\pgsql\data"
$Backend  = "D:\Colmena2.0\backend"
$Frontend = "D:\Colmena2.0\frontend"
$LogDir   = "D:\Colmena2.0\logs"
$PidDir   = "D:\Colmena2.0\run"

New-Item -ItemType Directory -Force -Path $LogDir, $PidDir | Out-Null

if (-not (Get-Command cloudflared -ErrorAction SilentlyContinue)) {
    Write-Host "cloudflared no esta instalado o no esta en el PATH." -ForegroundColor Red
    Write-Host "Descargalo de:"
    Write-Host "  https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    Write-Host "Renombralo a cloudflared.exe y ponlo en una carpeta que este en el PATH."
    exit 1
}

Write-Host "[1/4] PostgreSQL..." -ForegroundColor Cyan
& $PgCtl -D $PgData status | Out-Null
if ($LASTEXITCODE -ne 0) {
    & $PgCtl -D $PgData start
    Start-Sleep -Seconds 3
} else {
    Write-Host "  ya estaba corriendo."
}

Write-Host "[2/4] Backend (uvicorn, puerto 8000)..." -ForegroundColor Cyan
$backendProc = Start-Process -FilePath "cmd.exe" `
    -ArgumentList "/c", "poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 > `"$LogDir\backend.log`" 2>&1" `
    -WorkingDirectory $Backend `
    -WindowStyle Hidden `
    -PassThru
$backendProc.Id | Out-File "$PidDir\backend.pid"

Write-Host "[3/4] Frontend (vite, puerto 5174)..." -ForegroundColor Cyan
$frontendProc = Start-Process -FilePath "cmd.exe" `
    -ArgumentList "/c", "npm run dev > `"$LogDir\frontend.log`" 2>&1" `
    -WorkingDirectory $Frontend `
    -WindowStyle Hidden `
    -PassThru
$frontendProc.Id | Out-File "$PidDir\frontend.pid"

Write-Host "  esperando a que backend/frontend levanten (8s)..."
Start-Sleep -Seconds 8

Write-Host "[4/4] Cloudflare Tunnel (frontend, puerto 5174)..." -ForegroundColor Cyan
$tunnelProc = Start-Process -FilePath "cmd.exe" `
    -ArgumentList "/c", "cloudflared tunnel --url http://localhost:5174 > `"$LogDir\cloudflared.log`" 2>&1" `
    -WindowStyle Hidden `
    -PassThru
$tunnelProc.Id | Out-File "$PidDir\cloudflared.pid"

Write-Host "  esperando la URL publica..."
$tunnelUrl = $null
for ($i = 0; $i -lt 25; $i++) {
    Start-Sleep -Seconds 1
    $log = Get-Content "$LogDir\cloudflared.log" -Raw -ErrorAction SilentlyContinue
    if ($log -match 'https://[a-zA-Z0-9\-]+\.trycloudflare\.com') {
        $tunnelUrl = $Matches[0]
        break
    }
}

Write-Host ""
if ($tunnelUrl) {
    Write-Host "=====================================================" -ForegroundColor Green
    Write-Host " Colmena corriendo en background."
    Write-Host " URL publica: $tunnelUrl"
    Write-Host " Backend local:  http://localhost:8000/docs"
    Write-Host " Frontend local: http://localhost:5174"
    Write-Host "=====================================================" -ForegroundColor Green
} else {
    Write-Host "No se detecto la URL del tunnel a tiempo. Revisa $LogDir\cloudflared.log" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Logs en: $LogDir"
Write-Host "Para detener todo: powershell -File D:\Colmena2.0\stop-colmena.ps1"
