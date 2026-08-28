#Requires -RunAsAdministrator

# ============================================================================
#  Elimina los servicios de Colmena. Correr como administrador.
#  Usa -KeepPostgres para conservar el servicio de PostgreSQL.
# ============================================================================
param([switch]$KeepPostgres)

$ErrorActionPreference = "SilentlyContinue"

$PgCtl  = "D:\APPTHESIS\.tools\pgsql\bin\pg_ctl.exe"
$PgData = "D:\APPTHESIS\.tools\pgsql\data"
$Nssm   = (Get-Command nssm -ErrorAction SilentlyContinue).Source

foreach ($s in @("colmena-tunnel", "colmena-frontend", "colmena-backend")) {
    if (Get-Service -Name $s -ErrorAction SilentlyContinue) {
        & $Nssm stop $s confirm | Out-Null
        & $Nssm remove $s confirm | Out-Null
        Write-Host "Eliminado $s"
    }
}

if (-not $KeepPostgres -and (Get-Service -Name "colmena-postgres" -ErrorAction SilentlyContinue)) {
    Stop-Service "colmena-postgres" -Force
    & $PgCtl unregister -N "colmena-postgres"
    Write-Host "Eliminado colmena-postgres"
}

Write-Host "Listo."
