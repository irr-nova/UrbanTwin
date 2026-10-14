import json
import sys
from pathlib import Path

import pandas as pd
import pytest

AI_DIRECTORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AI_DIRECTORY))

from ripple.ripple_analysis import summarize_ripple_effects


def make_comparison_data():
    """Create artificial matched-edge data for testing."""

    return pd.DataFrame([
        {
            "baseline_sampled_seconds": 100,
            "scenario_sampled_seconds": 100,
            "baseline_flow": 100,
            "scenario_flow": 120,
            "baseline_speed": 10,
            "scenario_speed": 12,
            "baseline_travel_time": 20,
            "scenario_travel_time": 18,
            "baseline_time_loss": 5,
            "scenario_time_loss": 4,
        },
        {
            "baseline_sampled_seconds": 300,
            "scenario_sampled_seconds": 300,
            "baseline_flow": 200,
            "scenario_flow": 220,
            "baseline_speed": 20,
            "scenario_speed": 18,
            "baseline_travel_time": 40,
            "scenario_travel_time": 36,
            "baseline_time_loss": 15,
            "scenario_time_loss": 16,
        },
    ])


def test_weighted_summaries_and_percentage_changes():
    comparison = make_comparison_data()

    result = summarize_ripple_effects(comparison)

    assert result["matched_edge_count"] == 2

    assert result["baseline"]["average_speed"] == pytest.approx(17.5)
    assert result["scenario"]["average_speed"] == pytest.approx(16.5)

    assert result["baseline"]["weighted_edge_travel_time"] == pytest.approx(35)
    assert result["scenario"]["weighted_edge_travel_time"] == pytest.approx(31.5)

    assert result["baseline"]["edge_flow_sum"] == pytest.approx(300)
    assert result["scenario"]["edge_flow_sum"] == pytest.approx(340)

    assert result["changes"]["edge_flow_sum_change_pct"] == pytest.approx(
        13.3333333333
    )
    assert result["changes"]["average_speed_change_pct"] == pytest.approx(
        -5.7142857143
    )
    assert result["changes"]["weighted_edge_travel_time_change_pct"] == pytest.approx(
        -10
    )
    assert result["changes"]["edge_time_loss_sum_change_pct"] == pytest.approx(0)


def test_zero_baseline_produces_none_for_percentage_change():
    comparison = make_comparison_data()

    comparison["baseline_flow"] = 0
    comparison["scenario_flow"] = 10

    result = summarize_ripple_effects(comparison)

    assert result["changes"]["edge_flow_sum_change_pct"] is None


def test_empty_comparison_is_rejected():
    with pytest.raises(ValueError, match="no matching edge records"):
        summarize_ripple_effects(pd.DataFrame())


def test_ripple_chain_contains_four_current_stages():
    comparison = make_comparison_data()

    result = summarize_ripple_effects(comparison)

    stages = [item["stage"] for item in result["ripple_chain"]]

    assert stages == [
        "Aggregated Edge Flow",
        "Average Speed",
        "Weighted Edge Travel Time",
        "Summed Edge Time Loss",
    ]


def test_summary_serializes_as_strict_json():
    comparison = make_comparison_data()
    comparison["baseline_flow"] = 0
    comparison["scenario_flow"] = 10

    result = summarize_ripple_effects(comparison)

    json_output = json.dumps(result, allow_nan=False)
    decoded = json.loads(json_output)

    assert decoded["changes"]["edge_flow_sum_change_pct"] is None
    assert "null" in json_output
