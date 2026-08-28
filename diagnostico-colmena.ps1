#Requires -Version 5.1

<#
Diagnostico de solo lectura para Colmena en Windows.
No inicia, detiene ni modifica servicios o bases de datos.

Uso recomendado desde PowerShell como administrador:
  Set-ExecutionPolicy -Scope Process Bypass
  .\diagnostico-colmena.ps1

El resultado se guarda junto al script como diagnostico-colmena.txt.
#>

[CmdletBinding()]
param(
    [string]$ProjectRoot = "D:\Colmena2.0",
    [string]$PostgresRoot = "D:\APPTHESIS\.tools\pgsql"
)

$ErrorActionPreference = "Continue"
$OutputFile = Join-Path $PSScriptRoot "diagnostico-colmena.txt"
$ServiceNames = @(
    "colmena-postgres",
    "colmena-backend",
    "colmena-frontend",
    "colmena-tunnel"
)

function Write-Section {
    param([string]$Title)
    Write-Output ""
    Write-Output ("=" * 72)
    Write-Output $Title
    Write-Output ("=" * 72)
}

function Protect-Secrets {
    process {
        $line = [string]$_
        $line = $line -replace '(?i)(--token\s+)[^\s"]+', '$1<REDACTED>'
        $line = $line -replace '(?i)(token=)[^\s&"]+', '$1<REDACTED>'
        $line = $line -replace '(?i)(password=)[^\s&"]+', '$1<REDACTED>'
        Write-Output $line
    }
}

& {
    Write-Section "INFORMACION GENERAL"
    Write-Output "Fecha:        $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')"
    Write-Output "Equipo:       $env:COMPUTERNAME"
    Write-Output "Usuario:      $env:USERDOMAIN\$env:USERNAME"
    Write-Output "PowerShell:   $($PSVersionTable.PSVersion)"
    Write-Output "ProjectRoot:  $ProjectRoot"
    Write-Output "PostgresRoot: $PostgresRoot"

    Write-Section "SERVICIOS COLMENA"
    $services = Get-CimInstance Win32_Service -ErrorAction SilentlyContinue |
        Where-Object { $ServiceNames -contains $_.Name }

    if ($services) {
        $services |
            Select-Object Name, State, StartMode, StartName, ProcessId, PathName |
            Format-List |
            Out-String -Width 4096 |
            Protect-Secrets
    } else {
        Write-Output "No se encontraron servicios colmena-* instalados."
    }

    Write-Section "PROCESOS"
    $processes = Get-Process cloudflared, postgres, python, node -ErrorAction SilentlyContinue
    if ($processes) {
        $processes |
            Select-Object ProcessName, Id, SessionId, Path |
            Format-Table -AutoSize |
            Out-String -Width 4096
    } else {
        Write-Output "No se encontraron procesos cloudflared/postgres/python/node."
    }

    Write-Section "PUERTOS EN ESCUCHA"
    $connections = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
        Where-Object { $_.LocalPort -in @(5432, 8001, 5174) }
    if ($connections) {
        $connections |
            Select-Object LocalAddress, LocalPort, OwningProcess |
            Sort-Object LocalPort |
            Format-Table -AutoSize |
            Out-String -Width 4096
    } else {
        Write-Output "No hay procesos escuchando en 5432, 8001 o 5174."
    }

    Write-Section "POSTGRESQL Y ALMACENAMIENTO"
    $PgCtl = Join-Path $PostgresRoot "bin\pg_ctl.exe"
    $Psql = Join-Path $PostgresRoot "bin\psql.exe"
    $PgData = Join-Path $PostgresRoot "data"

    Write-Output "pg_ctl existe: $(Test-Path $PgCtl)"
    Write-Output "psql existe:   $(Test-Path $Psql)"
    Write-Output "PGDATA existe: $(Test-Path $PgData)"
    Write-Output "PG_VERSION:    $(Test-Path (Join-Path $PgData 'PG_VERSION'))"

    if (Test-Path $PgCtl) {
        Write-Output ""
        Write-Output "Estado reportado por pg_ctl:"
        & $PgCtl -D $PgData status 2>&1 | Protect-Secrets
    }

    if (Test-Path (Join-Path $PgData "postmaster.opts")) {
        Write-Output ""
        Write-Output "Parametros de la instancia activa:"
        Get-Content (Join-Path $PgData "postmaster.opts") -ErrorAction SilentlyContinue |
            Protect-Secrets
    }

    Write-Output ""
    Write-Output "Consulta SQL (puede pedir la clave del usuario colmena):"
    if (Test-Path $Psql) {
        $sql = @"
SHOW data_directory;
SELECT current_database(), pg_size_pretty(pg_database_size(current_database()));
SELECT COUNT(*) AS tablas_colmena
FROM information_schema.tables
WHERE table_schema = 'colmena';
"@
        & $Psql -U colmena -d colmena -h localhost -p 5432 -X -c $sql 2>&1 |
            Protect-Secrets
    } else {
        Write-Output "No se ejecuto: no existe $Psql"
    }

    Write-Section "ARCHIVOS Y CONFIGURACION"
    foreach ($path in @(
        $ProjectRoot,
        (Join-Path $ProjectRoot "backend"),
        (Join-Path $ProjectRoot "frontend"),
        (Join-Path $ProjectRoot "backend\.venv\Scripts\python.exe"),
        (Join-Path $ProjectRoot "backend\.env"),
        (Join-Path $ProjectRoot "frontend\node_modules\vite\bin\vite.js")
    )) {
        Write-Output ("{0,-7} {1}" -f (Test-Path $path), $path)
    }

    Write-Section "LOGS RECIENTES"
    $LogDir = Join-Path $ProjectRoot "logs"
    Write-Output "Directorio de logs: $LogDir"

    foreach ($logName in @(
        "colmena-postgres.log",
        "colmena-backend.log",
        "colmena-frontend.log",
        "colmena-tunnel.log"
    )) {
        $logPath = Join-Path $LogDir $logName
        Write-Output ""
        Write-Output "--- $logPath ---"
        if (Test-Path $logPath) {
            Get-Content $logPath -Tail 40 -ErrorAction SilentlyContinue |
                Protect-Secrets
        } else {
            Write-Output "NO EXISTE"
        }
    }

    Write-Section "RESUMEN RAPIDO"
    foreach ($serviceName in $ServiceNames) {
        $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
        if ($service) {
            Write-Output ("{0,-20} {1}" -f $serviceName, $service.Status)
        } else {
            Write-Output ("{0,-20} NO INSTALADO" -f $serviceName)
        }
    }

    Write-Output ""
    Write-Output "Diagnostico terminado. No se modifico el servidor."
} 2>&1 | Tee-Object -FilePath $OutputFile

Write-Host ""
Write-Host "Resultado guardado en:" -ForegroundColor Green
Write-Host $OutputFile -ForegroundColor Green
