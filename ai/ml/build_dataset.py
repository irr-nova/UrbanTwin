import argparse
import sys
from pathlib import Path

import pandas as pd


# Make the existing SUMO parser available to this script.
AI_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AI_DIR / "preprocessing"))

from parse_sumo import parse_edge_data


SCENARIOS = [
    ("baseline", 0, "edgeData.xml"),
    ("traffic_10", 10, "edgeData.increased10.xml"),
    ("traffic_20", 20, "edgeData.increased20.xml"),
    ("traffic_30", 30, "edgeData.increased30.xml"),
    ("traffic_90", 90, "edgeData.increased90.xml"),
]

START_TIME = 0
END_TIME = 3600

REQUIRED_COLUMNS = [
    "flow",
    "speed",
    "density",
    "occupancy",
    "sampled_seconds",
]


def build_dataset(input_dir):
    """Combine valid observations from all traffic scenarios."""

    datasets = []

    for scenario_name, traffic_change_percent, filename in SCENARIOS:
        file_path = input_dir / filename

        if not file_path.is_file():
            raise FileNotFoundError(
                f"Missing scenario XML file: {file_path}"
            )

        df = parse_edge_data(file_path)

        # Use the common one-hour interval in every scenario.
        df = df[
            (df["interval_begin"] == START_TIME)
            & (df["interval_end"] == END_TIME)
        ].copy()

        # Keep only rows with all required measurements available.
        df = df.dropna(subset=REQUIRED_COLUMNS)

        # Remove invalid measurement values.
        valid_rows = (
            (df["sampled_seconds"] > 0)
            & (df["speed"] >= 0)
            & (df["flow"] >= 0)
            & (df["density"] >= 0)
            & (df["occupancy"] >= 0)
        )
        df = df[valid_rows].copy()

        # Each road edge should appear at most once in this interval.
        if df["edge_id"].duplicated().any():
            raise ValueError(
                f"Duplicate edge IDs found in {filename}"
            )

        # Preserve scenario metadata for evaluation and grouping.
        df["scenario"] = scenario_name
        df["traffic_change_percent"] = traffic_change_percent

        datasets.append(df)

    dataset = pd.concat(datasets, ignore_index=True)

    # Keep the columns needed for analysis and model evaluation.
    columns = [
        "scenario",
        "traffic_change_percent",
        "edge_id",
        "interval_begin",
        "interval_end",
        "flow",
        "density",
        "occupancy",
        "sampled_seconds",
        "speed",
    ]

    return dataset[columns]


def main():
    parser = argparse.ArgumentParser(
        description="Build the UrbanTwin ML speed dataset."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path(".git/urbantwin-ml-input"),
        help="Directory containing the five scenario XML files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("ai/ml/data/speed_dataset.csv"),
        help="Path where the combined CSV will be saved.",
    )

    args = parser.parse_args()

    dataset = build_dataset(args.input_dir)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(args.output, index=False)

    print("UrbanTwin ML dataset created successfully.")
    print(f"Output file: {args.output}")
    print(f"Total observations: {len(dataset)}")
    print(f"Unique road edges: {dataset['edge_id'].nunique()}")
    print("\nObservations per scenario:")
    print(dataset.groupby("scenario").size().to_string())

    print("\nMissing values:")
    print(dataset[REQUIRED_COLUMNS].isna().sum().to_string())

    print("\nTarget variable: speed")
    print(f"Minimum speed: {dataset['speed'].min():.3f}")
    print(f"Maximum speed: {dataset['speed'].max():.3f}")
    print(f"Mean speed: {dataset['speed'].mean():.3f}")

    print("\nNote: speed and traffic features come from the same")
    print("simulation interval. This dataset supports initial")
    print("speed estimation, not future-speed forecasting.")


if __name__ == "__main__":
    main()
