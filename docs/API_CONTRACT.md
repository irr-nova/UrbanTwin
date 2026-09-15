# UrbanTwin API and Data Contract

This document defines the common data formats used between the UrbanTwin modules.

## 1. Scenario Request

The frontend sends a scenario request to the backend.

Example:

{
  "approach": "airport_road",
  "traffic_change_percent": 20
}

The values above are examples for development. The actual approach names will depend on the final Kathipara network.

## 2. Simulation Output

The simulation module provides traffic results in CSV format.

Example:

edge_id,vehicle_count,average_speed,travel_time,fuel_consumption,co2_emissions

edge_001,800,31.2,42.1,10.5,25.4

edge_002,620,27.4,51.3,12.1,29.7

The values above are placeholders for development only and are not real Kathipara measurements.

### Fields

- edge_id
- vehicle_count
- average_speed
- travel_time
- fuel_consumption
- co2_emissions

## 3. Analysis Output

The AI and ripple-analysis module provides results in JSON format.

Example:

{
  "scenario_id": "scenario_001",
  "baseline": {
    "traffic_volume": 0,
    "average_speed": 0,
    "travel_time": 0,
    "fuel_consumption": 0,
    "co2_emissions": 0
  },
  "scenario": {
    "traffic_volume": 0,
    "average_speed": 0,
    "travel_time": 0,
    "fuel_consumption": 0,
    "co2_emissions": 0
  },
  "changes": {
    "traffic_volume": 0,
    "average_speed": 0,
    "travel_time": 0,
    "fuel_consumption": 0,
    "co2_emissions": 0
  },
  "ripple_chain": [
    "Traffic Volume",
    "Average Speed",
    "Travel Time",
    "Fuel Consumption",
    "CO2 Emissions"
  ]
}

## 4. Ripple-Effect Chain

The initial MVP uses the following interpretable relationship chain:

Traffic Volume
↓
Average Speed / Congestion
↓
Travel Time
↓
Fuel Consumption
↓
CO2 Emissions

These relationships are intended to represent interpretable cross-domain effects. They should not automatically be treated as proof that every relationship is purely causal.

## 5. Development Rule

Mock data can be used so that team members can develop their modules independently.

Mock data must be clearly identified and must not be presented as real-world measurements.

Final results should distinguish between:

- Real/publicly observed data
- Calibrated/reference data
- Simulated data
- Model-predicted data