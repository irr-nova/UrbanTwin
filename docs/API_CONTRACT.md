# UrbanTwin API and Data Contract

This document defines the data formats and interfaces between the UrbanTwin simulation, AI/Data, backend, and frontend modules.

## 1. Scenario Request

The frontend sends a scenario request to the backend.

Example:

```json
{
  "approach": "airport_road",
  "traffic_change_percent": 20
}
```

The approach name is an example. Actual approach identifiers will depend on the finalized Kathipara road network.

## 2. Simulation Input

The simulation module uses SUMO to generate traffic simulation results.

The AI/Data module currently reads the original SUMO edgeData XML files directly.

Example file paths, relative to the project root:

- Baseline: `simulation/scenarios/edgeData.xml`
- Increased-traffic scenario: `simulation/scenarios/edgeData.increased20.xml`

These files contain simulated results, not live traffic observations.

### 2.1 Fields Extracted from SUMO XML

| Field | Meaning | Unit |
|---|---|---|
| `edge_id` | Identifier of a road segment | None |
| `interval_begin` | Start of the measurement interval | s |
| `interval_end` | End of the measurement interval | s |
| `sampled_seconds` | Total vehicle-seconds sampled on an edge | s |
| `flow` | Edge-level traffic flow rate | veh/h |
| `speed` | Mean speed on the edge | m/s |
| `travel_time` | Estimated edge travel time | s |
| `waiting_time` | Accumulated waiting time | s |
| `time_loss` | Accumulated time lost relative to desired speed | s |
| `density` | Traffic density | veh/km |
| `occupancy` | Percentage of edge occupancy | % |

Fuel consumption and CO₂ emissions are not currently included in the implemented analysis output.

### 2.2 Simulation Output Validation

Before the AI/Data module processes a scenario, the simulation module should confirm that:

- The SUMO process completed successfully.
- The expected edgeData XML file exists and contains valid interval data.
- The scenario-specific output corresponds to the intended configuration.
- The increased-traffic scenario did not terminate with a simulation error.

The AI/Data module should not interpret stale or failed-simulation output as a validated result for the requested scenario.

During development, the team should record the scenario configuration and output file paths used for each comparison.

## 3. Preprocessing and Comparison Rules

The initial comparison uses the common interval from simulation time 0 to 3600 seconds.

The preprocessing and comparison pipeline follows these rules:

1. Parse SUMO edgeData XML into Pandas DataFrames.
2. Keep records whose interval boundaries are exactly `0` and `3600` seconds.
3. Exclude records with missing `sampled_seconds` or `sampled_seconds` less than or equal to zero.
4. Match baseline and scenario records using `edge_id`, `interval_begin`, and `interval_end`.
5. Use an inner join for the comparison, so only matching observed edges are included.
6. Reject duplicate edge-interval records instead of silently comparing ambiguous observations.
7. Treat percentage changes with a zero or missing baseline as undefined.

Unmatched records are excluded from the comparison. The number of matched records should be reported so the comparison coverage is visible.

## 4. Analysis Output

The AI/Data module currently returns a Python dictionary that can be serialized as JSON by the backend.

Example structure:

```json
{
  "comparison_interval": {
    "begin_seconds": 0,
    "end_seconds": 3600
  },
  "matched_edge_count": 350,
  "baseline": {
    "edge_flow_sum": 7571.7,
    "average_speed": 12.25,
    "weighted_edge_travel_time": 10.09,
    "edge_time_loss_sum": 11816.45
  },
  "scenario": {
    "edge_flow_sum": 9049.8,
    "average_speed": 12.57,
    "weighted_edge_travel_time": 9.51,
    "edge_time_loss_sum": 13219.85
  },
  "changes": {
    "edge_flow_sum_change_pct": 19.52,
    "average_speed_change_pct": 2.58,
    "weighted_edge_travel_time_change_pct": -5.77,
    "edge_time_loss_sum_change_pct": 11.88
  },
  "ripple_chain": [
    {
      "stage": "Aggregated Edge Flow",
      "metric": "edge_flow_sum",
      "change_pct": 19.52
    },
    {
      "stage": "Average Speed",
      "metric": "average_speed",
      "change_pct": 2.58
    },
    {
      "stage": "Weighted Edge Travel Time",
      "metric": "weighted_edge_travel_time",
      "change_pct": -5.77
    },
    {
      "stage": "Summed Edge Time Loss",
      "metric": "edge_time_loss_sum",
      "change_pct": 11.88
    }
  ]
}
```

The numerical values above illustrate the current local baseline-versus-+20% demo. They are simulated results and may change when the input files or simulation settings change. The increased-traffic outputs must be validated after the simulation completes successfully before these figures are treated as verified scenario results.

### 4.1 Output Metrics and Interpretation

| Output field | Interpretation | Unit |
|---|---|---|
| `edge_flow_sum` | Sum of flow rates over the matched edges | Sum of veh/h edge values |
| `average_speed` | Sampled-seconds-weighted mean of edge speeds | m/s |
| `weighted_edge_travel_time` | Sampled-seconds-weighted mean of edge travel-time estimates | s |
| `edge_time_loss_sum` | Sum of edge-level time-loss values | Sum of s edge values |
| `*_change_pct` | Relative change from baseline to scenario | % |

The sums of edge flow and edge time loss must not be interpreted as unique-vehicle counts or exact network-wide totals. A vehicle may traverse multiple edges.

The weighted travel-time result is a summary of edge-level estimates, not the total journey time of a unique vehicle through the entire network.

## 5. Percentage-Change Formula

For a metric with a valid, nonzero baseline:

\[
\text{Percentage Change}
=
\frac{\text{Scenario Value}-\text{Baseline Value}}
{\text{Baseline Value}}
\times 100
\]

A positive result indicates an increase, and a negative result indicates a decrease.

If the baseline is zero or either value is missing, the percentage change is undefined. The analysis represents it as `None` in Python; the backend must serialize this as JSON `null`, not `NaN` or infinity.

## 6. Ripple-Effect Chain

The current implemented chain is:

1. Aggregated Edge Flow
2. Average Speed
3. Weighted Edge Travel Time
4. Summed Edge Time Loss

This chain organizes the metrics for comparison and interpretation. It does not establish that each observed change directly caused the next one.

Fuel consumption and CO₂ emissions are potential future extensions and must not be presented as currently calculated metrics.

## 7. Module Responsibilities

### Simulation Module

- Prepare the road network and traffic demand.
- Execute baseline and scenario simulations in SUMO.
- Generate scenario-specific XML outputs.
- Validate simulation completion and output files.

### AI/Data Module

- Parse SUMO edgeData XML.
- Filter and match comparable edge-interval observations.
- Calculate percentage changes.
- Generate weighted summaries and ripple-analysis results.
- Return a structured analysis result for backend integration.

### Backend Module

- Receive scenario requests.
- Coordinate simulation execution and AI/Data processing.
- Return results in a consistent JSON format.

### Frontend Module

- Allow scenario selection.
- Display baseline-versus-scenario comparisons and ripple-analysis results.
- Distinguish simulated, observed, calibrated, and predicted values.

## 8. Future ML Prediction

The current AI/Data implementation performs data preprocessing, comparison, and ripple analysis. It does not yet train or use a machine-learning prediction model.

A future prediction module may use data from multiple SUMO scenarios to train and evaluate models. Predicted values must be identified separately from SUMO-simulated values and evaluated against held-out simulation results.

## 9. Data Provenance

All results must be identified appropriately as one of the following:

- Real or publicly observed data
- Calibrated or reference data
- Simulated data
- Model-predicted data

Mock data must be clearly identified and must never be presented as real-world measurements.
