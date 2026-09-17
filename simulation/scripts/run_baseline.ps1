# UrbanTwin - Baseline SUMO Simulation
# Member 1: SUMO / Traffic Simulation

$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

$configFile = Join-Path `
    $projectRoot `
    "simulation\scenarios\osm.sumocfg"

Write-Host "Starting UrbanTwin baseline simulation..."
Write-Host "Configuration: $configFile"

sumo -c $configFile

Write-Host "Baseline simulation completed."