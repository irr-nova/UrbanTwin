# Simulation Module

The Simulation module handles the traffic simulation component of UrbanTwin.

## Technologies

- OpenStreetMap
- SUMO (Simulation of Urban MObility)

## Responsibilities

- Build and prepare the Kathipara Junction road network.
- Generate and validate the SUMO network.
- Prepare baseline traffic demand.
- Run the baseline simulation.
- Run the selected what-if scenario.
- Extract traffic and vehicle-related simulation results.
- Provide standardized output for the AI and analysis modules.

## Initial Scenario

The initial scenario increases traffic demand by 20% on a selected road approach.

## Expected Output

The simulation module should provide results containing:

- edge_id
- vehicle_count
- average_speed
- travel_time
- fuel_consumption
- co2_emissions

During development, mock data may be used. Final outputs must clearly distinguish simulated results from real or publicly observed data.

## Folder Structure

- network/ — SUMO network files
- routes/ — Traffic route and demand files
- scenarios/ — Scenario configurations
- scripts/ — Simulation and processing scripts