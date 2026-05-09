# AutoResearch-Style Experiment Pack

This folder contains a lightweight experiment for the CMPE 258 short story project on time-series foundation models.

## What it does

The experiment compares several forecasting baselines on a real daily temperature dataset using a strict chronological split.

It is designed to support the article's main point:

> Time-series forecasting models should be judged under clean temporal evaluation, because weak or leaky evaluation can exaggerate generalization.

## How to run

```bash
pip install -r requirements.txt
python autoresearch/scripts/run_experiments.py
python autoresearch/scripts/create_figures.py
```

## Outputs

After running, check:

- `results/tables/final_results.csv`
- `results/tables/final_results.md`
- `results/charts/mae_comparison.png`
- `results/charts/rmse_comparison.png`
- `results/charts/mape_comparison.png`
- `results/charts/forecast_vs_actual.png`
- `results/summary.md`
- `figures/architecture/tsfm_pipeline.png`
- `figures/benchmarks/clean_temporal_split.png`
- `figures/benchmarks/leakage_modes.png`
- `figures/custom_visuals/promise_vs_reality.png`

## Important wording for your report

Do not claim that this code reproduces a full TSFM benchmark. It is a small reproduction-style demonstration focused on clean evaluation.

Use this wording:

> I implemented a lightweight AutoResearch-style forecasting comparison with strict chronological splits. The experiment compares classical baselines and a patch-feature TSFM-style proxy to demonstrate why evaluation design matters in time-series foundation model research.

## How to improve it

For a stronger final version, replace the included dataset with one of these:

- ETT / ETTh / ETTm
- Weather
- Electricity
- Traffic

Then update `autoresearch/configs/experiment_config.json` with the new file path and column names.
