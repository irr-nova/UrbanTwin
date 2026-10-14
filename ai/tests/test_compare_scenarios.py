import sys
from pathlib import Path

import pandas as pd
import pytest

AI_DIRECTORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AI_DIRECTORY))

from ripple.compare_scenarios import compare_scenarios


def make_edge_data(rows):
    """Create a DataFrame from simple edge test records."""
    return pd.DataFrame(rows)


def test_matches_common_edges_in_selected_interval():
    baseline = make_edge_data([
        {
            "edge_id": "A",
            "interval_begin": 0,
            "interval_end": 3600,
            "sampled_seconds": 100,
            "flow": 100,
            "speed": 10,
            "travel_time": 20,
            "waiting_time": 2,
            "time_loss": 5,
            "density": 10,
            "occupancy": 20,
        },
        {
            "edge_id": "B",
            "interval_begin": 0,
            "interval_end": 3600,
            "sampled_seconds": 100,
            "flow": 200,
            "speed": 20,
            "travel_time": 30,
            "waiting_time": 3,
            "time_loss": 6,
            "density": 15,
            "occupancy": 25,
        },
        {
            "edge_id": "C",
            "interval_begin": 3600,
            "interval_end": 7200,
            "sampled_seconds": 100,
            "flow": 300,
            "speed": 30,
            "travel_time": 40,
            "waiting_time": 4,
            "time_loss": 7,
            "density": 20,
            "occupancy": 30,
        },
    ])

    scenario = make_edge_data([
        {
            "edge_id": "A",
            "interval_begin": 0,
            "interval_end": 3600,
            "sampled_seconds": 100,
            "flow": 120,
            "speed": 12,
            "travel_time": 18,
            "waiting_time": 1,
            "time_loss": 4,
            "density": 12,
            "occupancy": 22,
        },
        {
            "edge_id": "B",
            "interval_begin": 0,
            "interval_end": 3600,
            "sampled_seconds": 0,
            "flow": 250,
            "speed": 22,
            "travel_time": 28,
            "waiting_time": 2,
            "time_loss": 5,
            "density": 16,
            "occupancy": 26,
        },
        {
            "edge_id": "D",
            "interval_begin": 0,
            "interval_end": 3600,
            "sampled_seconds": 100,
            "flow": 400,
            "speed": 40,
            "travel_time": 50,
            "waiting_time": 5,
            "time_loss": 8,
            "density": 25,
            "occupancy": 35,
        },
    ])

    result = compare_scenarios(baseline, scenario)

    assert len(result) == 1
    assert result.iloc[0]["edge_id"] == "A"
    assert result.iloc[0]["flow_change_pct"] == pytest.approx(20.0)
    assert result.iloc[0]["speed_change_pct"] == pytest.approx(20.0)


def test_zero_baseline_produces_undefined_percentage_change():
    baseline = make_edge_data([
        {
            "edge_id": "A",
            "interval_begin": 0,
            "interval_end": 3600,
            "sampled_seconds": 100,
            "flow": 0,
            "speed": 10,
            "travel_time": 20,
            "waiting_time": 2,
            "time_loss": 5,
            "density": 10,
            "occupancy": 20,
        }
    ])

    scenario = make_edge_data([
        {
            "edge_id": "A",
            "interval_begin": 0,
            "interval_end": 3600,
            "sampled_seconds": 100,
            "flow": 100,
            "speed": 12,
            "travel_time": 18,
            "waiting_time": 1,
            "time_loss": 4,
            "density": 12,
            "occupancy": 22,
        }
    ])

    result = compare_scenarios(baseline, scenario)

    assert pd.isna(result.iloc[0]["flow_change_pct"])


def test_duplicate_edge_interval_records_are_rejected():
    row = {
        "edge_id": "A",
        "interval_begin": 0,
        "interval_end": 3600,
        "sampled_seconds": 100,
        "flow": 100,
        "speed": 10,
        "travel_time": 20,
        "waiting_time": 2,
        "time_loss": 5,
        "density": 10,
        "occupancy": 20,
    }

    baseline = make_edge_data([row, row.copy()])
    scenario = make_edge_data([row.copy()])

    with pytest.raises(ValueError, match="duplicate"):
        compare_scenarios(baseline, scenario)
