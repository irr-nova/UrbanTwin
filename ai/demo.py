from preprocessing.parse_sumo import parse_edge_data
from ripple.compare_scenarios import compare_scenarios
from ripple.ripple_analysis import summarize_ripple_effects


BASELINE_FILE = "simulation/scenarios/edgeData.xml"
SCENARIO_FILE = "simulation/scenarios/edgeData.increased20.xml"


def main():
    print("UrbanTwin - AI/Data Module Demo")
    print("=" * 40)

    print("\n1. Reading SUMO simulation data...")

    baseline_df = parse_edge_data(BASELINE_FILE)
    scenario_df = parse_edge_data(SCENARIO_FILE)

    print(f"Baseline rows: {len(baseline_df)}")
    print(f"Scenario rows: {len(scenario_df)}")

    print("\n2. Comparing baseline and +20% traffic scenario...")

    comparison_df = compare_scenarios(
        baseline_df,
        scenario_df
    )

    print(f"Matched edge-interval rows: {len(comparison_df)}")

    print("\n3. Ripple-effect analysis...")

    summary = summarize_ripple_effects(comparison_df)

    print("\nBaseline:")
    for metric, value in summary["baseline"].items():
        print(f"  {metric}: {value:.2f}")

    print("\nScenario (+20% traffic):")
    for metric, value in summary["scenario"].items():
        print(f"  {metric}: {value:.2f}")

    print("\nChanges:")
    for metric, value in summary["changes"].items():
        if value is None:
            print(f"  {metric}: undefined")
        else:
            print(f"  {metric}: {value:.2f}%")

    print("\nRipple Chain:")
    for step in summary["ripple_chain"]:
        change = step["change_pct"]

        if change is None:
            change_text = "undefined"
        else:
            change_text = f"{change:.2f}%"

        print(
            f"  {step['stage']} "
            f"({step['metric']}): {change_text}"
        )

    print("\nAI/Data module demo completed successfully.")


if __name__ == "__main__":
    main()