param(
    [Parameter(Mandatory = $true)]
    [ValidateRange(0, 1000)]
    [int]$Percent
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$scenarioDir = Join-Path $projectRoot "simulation\scenarios"
$routesDir = Join-Path $projectRoot "simulation\routes"

if ($Percent -eq 0) {
    $configFile = Join-Path $scenarioDir "osm.sumocfg"
    $routeFile = Join-Path $routesDir "osm.passenger.trips.xml"
    $edgeFile = Join-Path $scenarioDir "edgeData.xml"
    $tripInfoFile = Join-Path $scenarioDir "tripinfos.xml"
    $statsFile = Join-Path $scenarioDir "stats.xml"
}
else {
    $label = "$Percent"

    $configFile = Join-Path $scenarioDir "osm.increased$label.sumocfg"
    $routeFile = Join-Path $routesDir "osm.passenger.trips.increased$label.xml"
    $edgeFile = Join-Path $scenarioDir "edgeData.increased$label.xml"
    $tripInfoFile = Join-Path $scenarioDir "tripinfos.increased$label.xml"
    $statsFile = Join-Path $scenarioDir "stats.increased$label.xml"

    if (-not (Test-Path $routeFile)) {
        throw "Route file not found: $routeFile. Generate it first."
    }

    if (-not (Test-Path $configFile)) {
        throw "SUMO configuration not found: $configFile."
    }
}

foreach ($file in @($configFile, $routeFile)) {
    if (-not (Test-Path $file)) {
        throw "Required input file not found: $file"
    }
}

Write-Host "`n=== UrbanTwin SUMO Scenario ==="
Write-Host "Traffic increase: $Percent%"
Write-Host "Configuration: $configFile"
Write-Host "Route input: $routeFile"

Push-Location $scenarioDir
try {
    & sumo -c $configFile
    if ($LASTEXITCODE -ne 0) {
        throw "SUMO failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}

foreach ($file in @($edgeFile, $tripInfoFile, $statsFile)) {
    if (-not (Test-Path $file)) {
        throw "Expected output was not created: $file"
    }

    if ((Get-Item $file).Length -eq 0) {
        throw "Output file is empty: $file"
    }
}

Write-Host "`nSimulation completed successfully."
Write-Host "Edge data: $edgeFile"
Write-Host "Trip information: $tripInfoFile"
Write-Host "Statistics: $statsFile"