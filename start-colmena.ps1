$ErrorActionPreference = "Stop"

# ============================================================================
#  Arranca los servicios de Colmena y muestra la URL publica del tunnel.
#  Requiere haber corrido install-colmena-services.ps1 UNA vez (como admin).
#  Los servicios corren fuera de tu sesion: puedes cerrar SSH sin problema.
# ============================================================================

$LogDir  = "D:\Colmena2.0\logs"
$Tunnel  = "colmena-tunnel"
$Order   = @("colmena-postgres", "colmena-backend", "colmena-frontend", "colmena-tunnel")

foreach ($s in $Order) {
    $svc = Get-Service -Name $s -ErrorAction SilentlyContinue
    if (-not $svc) {
        Write-Host "Servicio '$s' no instalado." -ForegroundColor Red
        Write-Host "Corre primero (como administrador):  .\install-colmena-services.ps1" -ForegroundColor Red
        exit 1
    }
}

# reiniciar el tunnel para forzar una URL fresca de trycloudflare
$t = Get-Service -Name $Tunnel
if ($t.Status -eq 'Running') { Stop-Service $Tunnel; Start-Sleep -Seconds 1 }
if (Test-Path "$LogDir\$Tunnel.log") { Clear-Content "$LogDir\$Tunnel.log" -ErrorAction SilentlyContinue }

foreach ($s in $Order) {
    $svc = Get-Service -Name $s
    if ($svc.Status -ne 'Running') {
        Start-Service $s
        Write-Host "Iniciado  $s" -ForegroundColor Green
    } else {
        Write-Host "Ya activo $s"
    }
}

Write-Host ""
Write-Host "Esperando la URL publica del tunnel..."
$log = "$LogDir\$Tunnel.log"
$tunnelUrl = $null
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    if (Test-Path $log) {
        $m = Select-String -Path $log -Pattern 'https://[a-zA-Z0-9\-]+\.trycloudflare\.com' -ErrorAction SilentlyContinue |
             Select-Object -Last 1
        if ($m) { $tunnelUrl = $m.Matches[0].Value; break }
    }
}

Write-Host ""
if ($tunnelUrl) {
    Write-Host "=====================================================" -ForegroundColor Green
    Write-Host " Colmena corriendo como servicios de Windows."
    Write-Host " URL publica:    $tunnelUrl"
    Write-Host " Backend local:  http://localhost:8001/docs"
    Write-Host " Frontend local: http://localhost:5174"
    Write-Host "=====================================================" -ForegroundColor Green
} else {
    Write-Host "No se detecto la URL del tunnel a tiempo. Revisa $log" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "Logs en: $LogDir     Detener: .\stop-colmena.ps1"
