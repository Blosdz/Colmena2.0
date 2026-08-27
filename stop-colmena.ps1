$Root   = $PSScriptRoot
$PidDir = Join-Path $Root "run"
$PgCtl  = "D:\APPTHESIS\.tools\pgsql\bin\pg_ctl.exe"
$PgData = "D:\APPTHESIS\.tools\pgsql\data"

foreach ($name in "cloudflared", "frontend", "backend") {
    $pidFile = "$PidDir\$name.pid"
    if (Test-Path $pidFile) {
        $procId = Get-Content $pidFile
        & taskkill /PID $procId /T /F 2>$null | Out-Null
        Write-Host "Detenido $name (PID $procId)"
        Remove-Item $pidFile
    } else {
        Write-Host "$name no tenia pid file (ya estaba detenido)"
    }
}

Write-Host "Deteniendo PostgreSQL..."
& $PgCtl -D $PgData stop
