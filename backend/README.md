# Backend Module

The Backend module provides the API layer connecting the UrbanTwin frontend with the simulation and AI modules.

## Technologies

- Python
- FastAPI

## Responsibilities

- Receive scenario requests from the frontend.
- Validate scenario parameters.
- Manage scenario information.
- Trigger or communicate with the simulation and AI modules.
- Process standardized simulation and analysis results.
- Return results to the frontend through API endpoints.

## Initial API Flow

The basic flow is:

Frontend  
↓  
FastAPI Backend  
↓  
Simulation / AI Modules  
↓  
Processed Results  
↓  
Frontend

## Scenario Request

The backend accepts scenario information such as:

- Selected road approach
- Traffic change percentage

Example scenario:

- Approach: airport_road
- Traffic change: 20%

The example values are placeholders for development.

## Development

The backend may initially use mock responses so that frontend development can proceed independently of the simulation and AI modules.

Mock responses must be clearly identified and replaced with actual module outputs during integration.

## Folder Structure

- app/ — Main FastAPI application
- routes/ — API route definitions
- services/ — Simulation and AI integration logic
- schemas/ — Request and response schemas