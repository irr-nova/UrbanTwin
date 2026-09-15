# UrbanTwin

## AI-Assisted Urban Digital Twin for What-If Scenario Analysis

UrbanTwin is an urban digital twin prototype designed to analyze hypothetical interventions in an urban road network and visualize their cross-domain effects.

### Study Area

Kathipara Junction and its surrounding road network, Chennai.

### MVP

The initial UrbanTwin prototype focuses on:

Traffic Volume → Speed/Congestion → Travel Time → Fuel Consumption → CO₂ Emissions

The primary scenario is:

> Increase traffic demand by 20% on a selected approach.

The system compares baseline and scenario conditions and visualizes the resulting ripple effects.

## Project Modules

### Simulation

OpenStreetMap + SUMO based traffic simulation.

### AI

Data processing, prediction models and ripple-effect analysis.

### Backend

FastAPI-based API for scenario management and results.

### Frontend

React + Vite dashboard for scenario selection and visualization.

## Repository Structure

simulation/   → SUMO traffic simulation
ai/           → AI, data processing and ripple analysis
backend/      → FastAPI backend
frontend/     → React + Vite frontend
data/         → Sample/processed data
docs/         → Project documentation


## Team

- Member 1 — SUMO / Traffic Simulation
- Member 2 — AI / Data / Ripple Analysis
- Member 3 — Frontend / Backend / Visualization