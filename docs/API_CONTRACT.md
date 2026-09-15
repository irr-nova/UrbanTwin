# UrbanTwin API and Data Contract

This document defines the common data formats used between the UrbanTwin modules.

## 1. Scenario Request

The frontend sends a scenario request to the backend.

```json
{
  "approach": "airport_road",
  "traffic_change_percent": 20
}