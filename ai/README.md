# AI Module

The AI module handles data processing, prediction and ripple-effect analysis for UrbanTwin.

## Responsibilities

- Prepare and preprocess simulation and reference data.
- Train baseline machine learning models.
- Evaluate model performance.
- Compare baseline and scenario results.
- Calculate percentage changes between baseline and scenario conditions.
- Generate the interpretable ripple-effect chain.
- Provide standardized analysis results to the backend.

## Initial Prediction Pipeline

The initial pipeline focuses on the following relationships:

Traffic Volume → Average Speed → Travel Time → Fuel Consumption → CO2 Emissions

The first models may include:

- Linear Regression
- Random Forest
- Gradient Boosting

Model selection will depend on data availability and evaluation results.

## Evaluation

Models should be evaluated using appropriate metrics such as:

- MAE
- RMSE
- R²

## Ripple Analysis

The ripple-analysis component compares baseline and scenario values and identifies how changes propagate across the selected variables.

The initial ripple chain is:

Traffic Volume
↓
Average Speed / Congestion
↓
Travel Time
↓
Fuel Consumption
↓
CO2 Emissions

The relationships are intended to remain interpretable and should not automatically be presented as proof of direct causality.

## Development Data

Mock or sample data may be used during independent development.

All mock data must be clearly identified and must not be presented as real-world measurements.

## Folder Structure

- data/ — Input and processed datasets
- preprocessing/ — Data cleaning and preprocessing
- models/ — Machine learning models
- evaluation/ — Model evaluation
- ripple/ — Ripple-effect analysis