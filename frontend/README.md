# Frontend Module

The Frontend module provides the web interface for UrbanTwin.

## Technologies

- React
- Vite
- JavaScript

## Responsibilities

- Provide the UrbanTwin dashboard.
- Allow users to select a road approach and define a what-if scenario.
- Send scenario requests to the backend.
- Display baseline and scenario results.
- Visualize traffic, speed, travel time, fuel consumption and CO2 emissions.
- Display the ripple-effect chain in an understandable format.
- Provide charts, cards and map-based visualization where appropriate.

## Initial Dashboard

The initial dashboard should include:

- Scenario selection
- Traffic change input
- Baseline results
- Scenario results
- Percentage changes
- Ripple-effect visualization
- Map or network visualization

## Development

The frontend may initially use mock JSON responses so development can continue independently of the backend, simulation and AI modules.

Mock data must be clearly identified and replaced with actual API responses during integration.

## Folder Structure

- src/components/ — Reusable UI components
- src/pages/ — Application pages
- src/services/ — API communication
- src/charts/ — Data visualization components
- src/map/ — Map and network visualization