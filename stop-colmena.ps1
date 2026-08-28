# ============================================================================
#  Detiene los servicios de Colmena. PostgreSQL se deja corriendo por
#  defecto (es un servicio, no molesta). Usa -All para detenerlo tambien.
# ============================================================================
param([switch]$All)

$ErrorActionPreference = "SilentlyContinue"

$Order = @("colmena-tunnel", "colmena-frontend", "colmena-backend")
if ($All) { $Order += "colmena-postgres" }

foreach ($s in $Order) {
    $svc = Get-Service -Name $s -ErrorAction SilentlyContinue
    if (-not $svc) { Write-Host "$s no instalado"; continue }
    if ($svc.Status -eq 'Running') {
        Stop-Service $s -Force
        Write-Host "Detenido $s"
    } else {
        Write-Host "$s ya estaba detenido"
    }
}
