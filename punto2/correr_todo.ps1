# Ejecuta el benchmark completo del Punto 2 en Java y en Python (PowerShell).
# Uso: .\correr_todo.ps1 [-que java|python|ambos]
param(
    [string]$que = "ambos"
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$algs = @("linear", "binary", "ternary", "jump", "interpolation", "exponential")
New-Item -ItemType Directory -Path "resultados" -Force | Out-Null

if ($que -eq "java" -or $que -eq "ambos") {
    Write-Host "Compilando clases Java..." -ForegroundColor Cyan
    javac -encoding UTF-8 java/Busquedas.java java/Benchmark.java
    $csvJava = "resultados/resultados_java.csv"
    if (Test-Path $csvJava) { Remove-Item $csvJava }
    foreach ($a in $algs) {
        java -Xmx4g -cp java Benchmark $a ../punto1/datos datos $csvJava
    }
}

if ($que -eq "python" -or $que -eq "ambos") {
    $csvPy = "resultados/resultados_python.csv"
    if (Test-Path $csvPy) { Remove-Item $csvPy }
    foreach ($a in $algs) {
        python -u python/benchmark.py $a ../punto1/datos datos $csvPy
    }
}

Write-Host "Benchmark del Punto 2 completado con éxito." -ForegroundColor Green
