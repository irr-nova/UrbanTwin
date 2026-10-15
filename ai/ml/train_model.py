from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.metrics import mean_absolute_error, mean_squared_error


DATA_PATH = Path("ai/ml/data/speed_dataset.csv")
MODEL_PATH = Path("ai/ml/speed_model.joblib")

FEATURES = [
    "flow",
    "density",
    "occupancy",
    "sampled_seconds",
    "traffic_change_percent",
]
TARGET = "speed"


def evaluate_model(model, X, y, groups):
    """Evaluate using held-out scenarios rather than random rows."""

    cv = GroupKFold(n_splits=groups.nunique())

    predictions = cross_val_predict(
        model,
        X,
        y,
        groups=groups,
        cv=cv,
    )

    mae = mean_absolute_error(y, predictions)
    rmse = np.sqrt(mean_squared_error(y, predictions))

    return mae, rmse


def main():
    if not DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}. "
            "Run ai/ml/build_dataset.py first."
        )

    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]
    groups = df["scenario"]

    baseline = DummyRegressor(strategy="mean")

    model = RandomForestRegressor(
        n_estimators=200,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    )

    print("UrbanTwin ML - Road Speed Estimation")
    print("=" * 42)
    print(f"Observations: {len(df)}")
    print(f"Scenarios: {groups.nunique()}")
    print(f"Features: {', '.join(FEATURES)}")
    print("Target: observed road-segment speed")
    print("Evaluation: five-fold scenario-grouped cross-validation")
    print()

    baseline_mae, baseline_rmse = evaluate_model(
        baseline, X, y, groups
    )
    model_mae, model_rmse = evaluate_model(
        model, X, y, groups
    )

    print("HELD-OUT SCENARIO RESULTS")
    print("-" * 42)
    print(
        f"Mean-speed baseline | MAE: {baseline_mae:.3f} | "
        f"RMSE: {baseline_rmse:.3f}"
    )
    print(
        f"Random Forest       | MAE: {model_mae:.3f} | "
        f"RMSE: {model_rmse:.3f}"
    )

    print("\nMAE is the average absolute prediction error.")
    print("RMSE penalizes larger prediction errors more heavily.")

    if model_mae < baseline_mae:
        print("\nThe model improves on the baseline MAE.")
    else:
        print(
            "\nThe model did not beat the baseline MAE. "
            "Do not claim an improvement."
        )

    # Fit a final model on all available observations for later use.
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)

    print(f"\nFinal model saved to: {MODEL_PATH}")
    print(
        "Note: evaluation scores come from held-out scenarios; "
        "the saved model is subsequently fitted on all five."
    )
    print(
        "This estimates speed from same-interval traffic features; "
        "it is not future-speed forecasting."
    )


if __name__ == "__main__":
    main()
