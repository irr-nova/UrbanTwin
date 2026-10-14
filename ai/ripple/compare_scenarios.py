import pandas as pd


COMPARISON_START = 0
COMPARISON_END = 3600


def compare_scenarios(baseline_df, scenario_df):
    baseline = baseline_df.copy()
    scenario = scenario_df.copy()

    # Keep only the common 0–3600 second interval.
    baseline = baseline[
        (baseline["interval_begin"] == COMPARISON_START)
        & (baseline["interval_end"] == COMPARISON_END)
    ].copy()

    scenario = scenario[
        (scenario["interval_begin"] == COMPARISON_START)
        & (scenario["interval_end"] == COMPARISON_END)
    ].copy()

    # Exclude records without valid observations.
    baseline = baseline[
        baseline["sampled_seconds"].notna()
        & (baseline["sampled_seconds"] > 0)
    ].copy()

    scenario = scenario[
        scenario["sampled_seconds"].notna()
        & (scenario["sampled_seconds"] > 0)
    ].copy()

    # Prevent ambiguous matches if an edge appears more than once
    # within the selected interval.
    keys = ["edge_id", "interval_begin", "interval_end"]

    if baseline.duplicated(keys).any():
        raise ValueError(
            "Baseline data contains duplicate edge-interval records."
        )

    if scenario.duplicated(keys).any():
        raise ValueError(
            "Scenario data contains duplicate edge-interval records."
        )

    # Rename metrics to distinguish baseline and scenario values.
    metrics = [
        "flow",
        "speed",
        "travel_time",
        "waiting_time",
        "time_loss",
        "density",
        "occupancy",
        "sampled_seconds",
    ]

    baseline = baseline.rename(
        columns={metric: f"baseline_{metric}" for metric in metrics}
    )

    scenario = scenario.rename(
        columns={metric: f"scenario_{metric}" for metric in metrics}
    )

    # Compare only matching edges and matching interval boundaries.
    comparison = pd.merge(
        baseline,
        scenario,
        on=keys,
        how="inner",
        validate="one_to_one",
    )

    # Percentage changes are undefined when the baseline is zero
    # or missing. Represent these cases as NaN in the DataFrame.
    percentage_metrics = [
        "flow",
        "speed",
        "travel_time",
        "waiting_time",
        "time_loss",
    ]

    for metric in percentage_metrics:
        baseline_values = comparison[f"baseline_{metric}"]
        scenario_values = comparison[f"scenario_{metric}"]

        valid_baseline = (
            baseline_values.notna()
            & (baseline_values != 0)
            & scenario_values.notna()
        )

        comparison[f"{metric}_change_pct"] = pd.NA

        comparison.loc[valid_baseline, f"{metric}_change_pct"] = (
            (
                scenario_values[valid_baseline]
                - baseline_values[valid_baseline]
            )
            / baseline_values[valid_baseline]
        ) * 100

        comparison[f"{metric}_change_pct"] = pd.to_numeric(
            comparison[f"{metric}_change_pct"],
            errors="coerce",
        )

    return comparison