import pandas as pd


def compare_scenarios(baseline_df, scenario_df):
    baseline = baseline_df.copy()
    scenario = scenario_df.copy()

    baseline = baseline.rename(
        columns={
            "flow": "baseline_flow",
            "speed": "baseline_speed",
            "travel_time": "baseline_travel_time",
            "waiting_time": "baseline_waiting_time",
            "time_loss": "baseline_time_loss",
            "density": "baseline_density",
            "occupancy": "baseline_occupancy",
            "sampled_seconds": "baseline_sampled_seconds",
        }
    )

    scenario = scenario.rename(
        columns={
            "flow": "scenario_flow",
            "speed": "scenario_speed",
            "travel_time": "scenario_travel_time",
            "waiting_time": "scenario_waiting_time",
            "time_loss": "scenario_time_loss",
            "density": "scenario_density",
            "occupancy": "scenario_occupancy",
            "sampled_seconds": "scenario_sampled_seconds",
        }
    )

    comparison = pd.merge(
        baseline,
        scenario,
        on=["edge_id", "interval_begin"],
        how="inner",
    )

    comparison["flow_change_pct"] = (
        (comparison["scenario_flow"] - comparison["baseline_flow"])
        / comparison["baseline_flow"]
    ) * 100

    comparison["speed_change_pct"] = (
        (comparison["scenario_speed"] - comparison["baseline_speed"])
        / comparison["baseline_speed"]
    ) * 100

    comparison["travel_time_change_pct"] = (
        (comparison["scenario_travel_time"] - comparison["baseline_travel_time"])
        / comparison["baseline_travel_time"]
    ) * 100

    comparison["waiting_time_change_pct"] = (
        (comparison["scenario_waiting_time"] - comparison["baseline_waiting_time"])
        / comparison["baseline_waiting_time"].replace(0, pd.NA)
    ) * 100

    comparison["time_loss_change_pct"] = (
        (comparison["scenario_time_loss"] - comparison["baseline_time_loss"])
        / comparison["baseline_time_loss"]
    ) * 100

    return comparison