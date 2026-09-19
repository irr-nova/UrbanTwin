def percentage_change(baseline, scenario):
    if baseline == 0:
        return None

    return ((scenario - baseline) / baseline) * 100


def summarize_ripple_effects(comparison_df):
    baseline_sampled = comparison_df["baseline_sampled_seconds"]
    scenario_sampled = comparison_df["scenario_sampled_seconds"]

    baseline_speed = (
        comparison_df["baseline_speed"] * baseline_sampled
    ).sum() / baseline_sampled.sum()

    scenario_speed = (
        comparison_df["scenario_speed"] * scenario_sampled
    ).sum() / scenario_sampled.sum()

    # Sum of edge-level flow values across the matched road edges.
    # This is not a count of unique vehicles in the network.
    baseline_flow = comparison_df["baseline_flow"].sum()
    scenario_flow = comparison_df["scenario_flow"].sum()

    baseline_travel_time = (
        comparison_df["baseline_travel_time"] * baseline_sampled
    ).sum() / baseline_sampled.sum()

    scenario_travel_time = (
        comparison_df["scenario_travel_time"] * scenario_sampled
    ).sum() / scenario_sampled.sum()

    baseline_time_loss = comparison_df["baseline_time_loss"].sum()
    scenario_time_loss = comparison_df["scenario_time_loss"].sum()

    summary = {
        "baseline": {
            "traffic_volume": baseline_flow,
            "average_speed": baseline_speed,
            "travel_time": baseline_travel_time,
            "time_loss": baseline_time_loss,
        },
        "scenario": {
            "traffic_volume": scenario_flow,
            "average_speed": scenario_speed,
            "travel_time": scenario_travel_time,
            "time_loss": scenario_time_loss,
        },
    }

    summary["changes"] = {
        "traffic_volume_change_pct": percentage_change(
            baseline_flow, scenario_flow
        ),
        "average_speed_change_pct": percentage_change(
            baseline_speed, scenario_speed
        ),
        "travel_time_change_pct": percentage_change(
            baseline_travel_time, scenario_travel_time
        ),
        "time_loss_change_pct": percentage_change(
            baseline_time_loss, scenario_time_loss
        ),
    }

    summary["ripple_chain"] = [
        {
            "stage": "Traffic Volume",
            "metric": "traffic_volume",
            "change_pct": summary["changes"]["traffic_volume_change_pct"],
        },
        {
            "stage": "Average Speed",
            "metric": "average_speed",
            "change_pct": summary["changes"]["average_speed_change_pct"],
        },
        {
            "stage": "Travel Time",
            "metric": "travel_time",
            "change_pct": summary["changes"]["travel_time_change_pct"],
        },
        {
            "stage": "Time Loss",
            "metric": "time_loss",
            "change_pct": summary["changes"]["time_loss_change_pct"],
        },
    ]

    return summary