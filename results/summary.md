# Results Summary

## Experiment goal

This experiment is a small AutoResearch-style reproduction component for the CMPE 258 short story on time-series foundation models.

The goal is not to reproduce a full large-scale TSFM benchmark. Instead, it demonstrates the paper's key evaluation message in a simple, reproducible setting:

> Forecasting results should be evaluated with strict chronological splits and strong baselines, because weak or leaky evaluation can exaggerate generalization.

## Dataset

- Dataset: Daily Minimum Temperatures in Melbourne
- Input window: 60 time steps
- Forecast horizon: 7 time steps
- Split: 70% train, 15% validation, 15% test
- Split type: strict chronological split

## Models compared

1. **Naive Last Value**: repeats the most recent observed value.
2. **Moving Average**: repeats the average of the recent window.
3. **Seasonal Naive**: uses the value from the same season in the previous year when available.
4. **Ridge Window Regressor**: learns a multi-step forecast from lag windows.
5. **Random Forest Window Regressor**: nonlinear lag-window baseline.
6. **Patch-Feature Ridge**: a lightweight TSFM-inspired proxy using patch-level features.

Important note: Patch-Feature Ridge is not a true pretrained foundation model. It is used only as a small reproducible proxy for patch/token-style time-series representation.

## Best model in this run

- Best model by MAE: **Random Forest Window Regressor**
- MAE: **1.9549**
- RMSE: **2.5337**
- MAPE: **21.91%**

## Interpretation

The key lesson is not simply which model wins. The important point is that every model is evaluated under the same chronological split. This avoids a common problem in time-series evaluation: allowing information from the future or from overlapping temporal windows to leak into the test setup.

This supports the main article's argument: time-series foundation models are promising, but benchmark design must be handled carefully before making strong claims about generalization.

## Files generated

- `results/tables/final_results.csv`
- `results/tables/final_results.md`
- `results/charts/mae_comparison.png`
- `results/charts/rmse_comparison.png`
- `results/charts/mape_comparison.png`
- `results/charts/forecast_vs_actual.png`
- `autoresearch/outputs/metrics.json`
- `autoresearch/outputs/example_forecast_predictions.csv`
