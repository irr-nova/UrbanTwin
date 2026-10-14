import math
import pandas as pd


def percentage_change(baseline, scenario):
    """Return percentage change, or None if it cannot be calculated."""
    if pd.isna(baseline) or pd.isna(scenario):
        return None

    if baseline == 0:
        return None

    result = ((scenario - baseline) / baseline) * 100

    if not math.isfinite(float(result)):
        return None

    return float(result)


def weighted_average(values, weights):
    """Calculate a weighted average using only valid positive weights."""
    valid = (
        values.notna()
        & weights.notna()
        & (weights > 0)
    )

    valid_values = values[valid]
    valid_weights = weights[valid]

    if valid_weights.empty or valid_weights.sum() == 0:
        return None

    result = (
        (valid_values * valid_weights).sum()
        / valid_weights.sum()
    )

    if not math.isfinite(float(result)):
        return None

    return float(result)


def safe_sum(values):
    """Sum available values; return None if no valid values exist."""
    valid_values = values.dropna()

    if valid_values.empty:
        return None

    result = valid_values.sum()

    if not math.isfinite(float(result)):
        return None

    return float(result)


def summarize_ripple_effects(comparison_df):
    """Summarize baseline vs scenario metrics for matched edge records."""

    if comparison_df.empty:
        raise ValueError(
            "Cannot summarize scenarios because there are no "
            "matching edge records in the selected interval."
        )

    baseline_sampled = comparison_df["baseline_sampled_seconds"]
    scenario_sampled = comparison_df["scenario_sampled_seconds"]

    baseline_speed = weighted_average(
        comparison_df["baseline_speed"],
        baseline_sampled,
    )

    scenario_speed = weighted_average(
        comparison_df["scenario_speed"],
        scenario_sampled,
    )

    baseline_travel_time = weighted_average(
        comparison_df["baseline_travel_time"],
        baseline_sampled,
    )

    scenario_travel_time = weighted_average(
        comparison_df["scenario_travel_time"],
        scenario_sampled,
    )

    # These are sums of edge-level flow rates, not unique vehicle counts.
    baseline_flow_sum = safe_sum(comparison_df["baseline_flow"])
    scenario_flow_sum = safe_sum(comparison_df["scenario_flow"])

    # These are sums of edge-level time-loss values, not unique-vehicle
    # network-wide delay totals.
    baseline_time_loss_sum = safe_sum(
        comparison_df["baseline_time_loss"]
    )
    scenario_time_loss_sum = safe_sum(
        comparison_df["scenario_time_loss"]
    )

    baseline = {
        "edge_flow_sum": baseline_flow_sum,
        "average_speed": baseline_speed,
        "weighted_edge_travel_time": baseline_travel_time,
        "edge_time_loss_sum": baseline_time_loss_sum,
    }

    scenario = {
        "edge_flow_sum": scenario_flow_sum,
        "average_speed": scenario_speed,
        "weighted_edge_travel_time": scenario_travel_time,
        "edge_time_loss_sum": scenario_time_loss_sum,
    }

    changes = {
        "edge_flow_sum_change_pct": percentage_change(
            baseline_flow_sum,
            scenario_flow_sum,
        ),
        "average_speed_change_pct": percentage_change(
            baseline_speed,
            scenario_speed,
        ),
        "weighted_edge_travel_time_change_pct": percentage_change(
            baseline_travel_time,
            scenario_travel_time,
        ),
        "edge_time_loss_sum_change_pct": percentage_change(
            baseline_time_loss_sum,
            scenario_time_loss_sum,
        ),
    }

    ripple_chain = [
        {
            "stage": "Aggregated Edge Flow",
            "metric": "edge_flow_sum",
            "change_pct": changes["edge_flow_sum_change_pct"],
        },
        {
            "stage": "Average Speed",
            "metric": "average_speed",
            "change_pct": changes["average_speed_change_pct"],
        },
        {
            "stage": "Weighted Edge Travel Time",
            "metric": "weighted_edge_travel_time",
            "change_pct": changes[
                "weighted_edge_travel_time_change_pct"
            ],
        },
        {
            "stage": "Summed Edge Time Loss",
            "metric": "edge_time_loss_sum",
            "change_pct": changes["edge_time_loss_sum_change_pct"],
        },
    ]

    return {
        "comparison_interval": {
            "begin_seconds": 0,
            "end_seconds": 3600,
        },
        "matched_edge_count": int(len(comparison_df)),
        "baseline": baseline,
        "scenario": scenario,
        "changes": changes,
        "ripple_chain": ripple_chain,
    }