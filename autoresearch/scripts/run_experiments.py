"""
CMPE 258 Short Story - Time-Series Foundation Models
AutoResearch-style clean evaluation experiment

This script compares simple forecasting baselines under a strict chronological split.
It is intentionally lightweight so it can run on a normal laptop without a GPU.

Models included:
1. Naive Last Value
2. Moving Average
3. Seasonal Naive
4. Ridge Window Regressor
5. Random Forest Window Regressor
6. Patch-Feature Ridge Regressor, a lightweight TSFM-inspired proxy

Important note:
The Patch-Feature Ridge model is NOT a real pretrained foundation model. It is included
as a small, reproducible proxy for the patch/tokenization idea used in many TSFMs.
For the final report, describe it as a TSFM-inspired baseline, not as an actual TSFM.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler


@dataclass
class Config:
    project_name: str
    dataset_path: str
    date_column: str
    value_column: str
    input_window: int
    forecast_horizon: int
    train_fraction: float
    validation_fraction: float
    test_fraction: float
    moving_average_window: int
    seasonal_lag: int
    random_seed: int


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_config(root: Path) -> Config:
    config_path = root / "autoresearch" / "configs" / "experiment_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return Config(**raw)


def load_dataset(root: Path, cfg: Config) -> pd.DataFrame:
    path = root / cfg.dataset_path
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Add a CSV file or update experiment_config.json."
        )

    df = pd.read_csv(path)
    if cfg.date_column not in df.columns or cfg.value_column not in df.columns:
        raise ValueError(
            f"Expected columns {cfg.date_column!r} and {cfg.value_column!r}. Found {list(df.columns)}"
        )

    df = df[[cfg.date_column, cfg.value_column]].copy()
    df[cfg.date_column] = pd.to_datetime(df[cfg.date_column])
    df[cfg.value_column] = pd.to_numeric(df[cfg.value_column], errors="coerce")
    df = df.dropna().sort_values(cfg.date_column).reset_index(drop=True)
    return df


def make_supervised(values: np.ndarray, input_window: int, horizon: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    X, y, target_starts = [], [], []
    for i in range(input_window, len(values) - horizon + 1):
        X.append(values[i - input_window : i])
        y.append(values[i : i + horizon])
        target_starts.append(i)
    return np.asarray(X), np.asarray(y), np.asarray(target_starts)


def chronological_split(
    X: np.ndarray,
    y: np.ndarray,
    starts: np.ndarray,
    train_fraction: float,
    validation_fraction: float,
) -> Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    n = len(X)
    train_end = int(n * train_fraction)
    val_end = int(n * (train_fraction + validation_fraction))

    return {
        "train": (X[:train_end], y[:train_end], starts[:train_end]),
        "val": (X[train_end:val_end], y[train_end:val_end], starts[train_end:val_end]),
        "test": (X[val_end:], y[val_end:], starts[val_end:]),
    }


def mape_safe(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    denom = np.maximum(np.abs(y_true), 1e-8)
    return float(np.mean(np.abs((y_true - y_pred) / denom)) * 100)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    return {
        "MAE": float(mean_absolute_error(y_true.ravel(), y_pred.ravel())),
        "RMSE": float(math.sqrt(mean_squared_error(y_true.ravel(), y_pred.ravel()))),
        "MAPE": mape_safe(y_true, y_pred),
    }


def predict_naive_last(X: np.ndarray, horizon: int) -> np.ndarray:
    last = X[:, -1]
    return np.repeat(last[:, None], horizon, axis=1)


def predict_moving_average(X: np.ndarray, horizon: int, window: int) -> np.ndarray:
    avg = X[:, -window:].mean(axis=1)
    return np.repeat(avg[:, None], horizon, axis=1)


def predict_seasonal_naive(values: np.ndarray, starts: np.ndarray, horizon: int, seasonal_lag: int) -> np.ndarray:
    preds = []
    for start in starts:
        seasonal_start = start - seasonal_lag
        seasonal_end = seasonal_start + horizon
        if seasonal_start >= 0 and seasonal_end <= len(values):
            preds.append(values[seasonal_start:seasonal_end])
        else:
            fallback = values[start - 1]
            preds.append(np.repeat(fallback, horizon))
    return np.asarray(preds)


def patch_features(X: np.ndarray, n_patches: int = 6) -> np.ndarray:
    """Create compact patch-level features inspired by patch/token TSFM preprocessing."""
    features: List[np.ndarray] = []
    for row in X:
        patches = np.array_split(row, n_patches)
        row_features: List[float] = []
        for patch in patches:
            idx = np.arange(len(patch))
            slope = np.polyfit(idx, patch, deg=1)[0] if len(patch) > 1 else 0.0
            row_features.extend([
                float(np.mean(patch)),
                float(np.std(patch)),
                float(np.min(patch)),
                float(np.max(patch)),
                float(slope),
            ])
        global_idx = np.arange(len(row))
        global_slope = np.polyfit(global_idx, row, deg=1)[0]
        row_features.extend([
            float(row[-1]),
            float(np.mean(row)),
            float(np.std(row)),
            float(global_slope),
        ])
        features.append(np.asarray(row_features))
    return np.vstack(features)


def train_ridge_window(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray) -> np.ndarray:
    scaler_x = StandardScaler()
    scaler_y = StandardScaler()
    X_train_scaled = scaler_x.fit_transform(X_train)
    y_train_scaled = scaler_y.fit_transform(y_train)

    model = Ridge(alpha=1.0)
    model.fit(X_train_scaled, y_train_scaled)
    pred_scaled = model.predict(scaler_x.transform(X_test))
    return scaler_y.inverse_transform(pred_scaled)


def train_patch_ridge(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray) -> np.ndarray:
    X_train_feat = patch_features(X_train)
    X_test_feat = patch_features(X_test)

    scaler_x = StandardScaler()
    scaler_y = StandardScaler()
    X_train_scaled = scaler_x.fit_transform(X_train_feat)
    y_train_scaled = scaler_y.fit_transform(y_train)

    model = Ridge(alpha=1.0)
    model.fit(X_train_scaled, y_train_scaled)
    pred_scaled = model.predict(scaler_x.transform(X_test_feat))
    return scaler_y.inverse_transform(pred_scaled)


def train_random_forest(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, random_seed: int) -> np.ndarray:
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=random_seed,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model.predict(X_test)


def save_result_table(root: Path, metrics: List[Dict[str, object]]) -> pd.DataFrame:
    df_metrics = pd.DataFrame(metrics).sort_values("MAE").reset_index(drop=True)

    tables_dir = root / "results" / "tables"
    outputs_dir = root / "autoresearch" / "outputs"
    tables_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    df_metrics.to_csv(tables_dir / "final_results.csv", index=False)
    df_metrics.to_markdown(tables_dir / "final_results.md", index=False)

    with open(outputs_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return df_metrics


def plot_metrics(root: Path, df_metrics: pd.DataFrame) -> None:
    charts_dir = root / "results" / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    for metric in ["MAE", "RMSE", "MAPE"]:
        plt.figure(figsize=(10, 5))
        plt.bar(df_metrics["model"], df_metrics[metric])
        plt.title(f"{metric} Comparison - Strict Chronological Test Split")
        plt.ylabel(metric)
        plt.xlabel("Model")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.savefig(charts_dir / f"{metric.lower()}_comparison.png", dpi=200)
        plt.close()


def plot_forecast_example(
    root: Path,
    dates: pd.Series,
    values: np.ndarray,
    starts_test: np.ndarray,
    y_test: np.ndarray,
    predictions_by_model: Dict[str, np.ndarray],
    best_model_name: str,
) -> None:
    charts_dir = root / "results" / "charts"
    outputs_dir = root / "autoresearch" / "outputs"
    charts_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    idx = 0
    start = starts_test[idx]
    horizon = y_test.shape[1]
    context_start = max(0, start - 60)
    forecast_dates = dates.iloc[start : start + horizon]
    context_dates = dates.iloc[context_start:start]

    pred = predictions_by_model[best_model_name][idx]

    plt.figure(figsize=(11, 5))
    plt.plot(context_dates, values[context_start:start], label="Context history")
    plt.plot(forecast_dates, y_test[idx], marker="o", label="Actual future")
    plt.plot(forecast_dates, pred, marker="o", linestyle="--", label=f"Forecast: {best_model_name}")
    plt.title("Forecast vs Actual Example")
    plt.xlabel("Date")
    plt.ylabel("Temperature")
    plt.legend()
    plt.tight_layout()
    plt.savefig(charts_dir / "forecast_vs_actual.png", dpi=200)
    plt.close()

    prediction_rows = []
    for step in range(horizon):
        prediction_rows.append({
            "date": str(forecast_dates.iloc[step].date()),
            "actual": float(y_test[idx, step]),
            "prediction": float(pred[step]),
            "model": best_model_name,
        })
    pd.DataFrame(prediction_rows).to_csv(outputs_dir / "example_forecast_predictions.csv", index=False)


def write_summary(root: Path, cfg: Config, df_metrics: pd.DataFrame, dataset_name: str) -> None:
    best = df_metrics.iloc[0]
    summary = f"""# Results Summary

## Experiment goal

This experiment is a small AutoResearch-style reproduction component for the CMPE 258 short story on time-series foundation models.

The goal is not to reproduce a full large-scale TSFM benchmark. Instead, it demonstrates the paper's key evaluation message in a simple, reproducible setting:

> Forecasting results should be evaluated with strict chronological splits and strong baselines, because weak or leaky evaluation can exaggerate generalization.

## Dataset

- Dataset: {dataset_name}
- Input window: {cfg.input_window} time steps
- Forecast horizon: {cfg.forecast_horizon} time steps
- Split: {int(cfg.train_fraction * 100)}% train, {int(cfg.validation_fraction * 100)}% validation, {int(cfg.test_fraction * 100)}% test
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

- Best model by MAE: **{best['model']}**
- MAE: **{best['MAE']:.4f}**
- RMSE: **{best['RMSE']:.4f}**
- MAPE: **{best['MAPE']:.2f}%**

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
"""
    (root / "results" / "summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    root = get_repo_root()
    cfg = load_config(root)

    df = load_dataset(root, cfg)
    dates = df[cfg.date_column]
    values = df[cfg.value_column].to_numpy(dtype=float)

    X, y, starts = make_supervised(values, cfg.input_window, cfg.forecast_horizon)
    splits = chronological_split(X, y, starts, cfg.train_fraction, cfg.validation_fraction)

    X_train, y_train, starts_train = splits["train"]
    X_test, y_test, starts_test = splits["test"]

    predictions_by_model: Dict[str, np.ndarray] = {}
    predictions_by_model["Naive Last Value"] = predict_naive_last(X_test, cfg.forecast_horizon)
    predictions_by_model["Moving Average"] = predict_moving_average(
        X_test, cfg.forecast_horizon, cfg.moving_average_window
    )
    predictions_by_model["Seasonal Naive"] = predict_seasonal_naive(
        values, starts_test, cfg.forecast_horizon, cfg.seasonal_lag
    )
    predictions_by_model["Ridge Window Regressor"] = train_ridge_window(X_train, y_train, X_test)
    predictions_by_model["Random Forest Window Regressor"] = train_random_forest(
        X_train, y_train, X_test, cfg.random_seed
    )
    predictions_by_model["Patch-Feature Ridge TSFM-Style Proxy"] = train_patch_ridge(
        X_train, y_train, X_test
    )

    metrics = []
    for model_name, pred in predictions_by_model.items():
        row = {"model": model_name}
        row.update(compute_metrics(y_test, pred))
        metrics.append(row)

    df_metrics = save_result_table(root, metrics)
    plot_metrics(root, df_metrics)

    best_model_name = str(df_metrics.iloc[0]["model"])
    plot_forecast_example(root, dates, values, starts_test, y_test, predictions_by_model, best_model_name)

    write_summary(root, cfg, df_metrics, "Daily Minimum Temperatures in Melbourne")

    log_text = [
        f"Project: {cfg.project_name}",
        f"Dataset rows: {len(df)}",
        f"Supervised examples: {len(X)}",
        f"Train examples: {len(X_train)}",
        f"Test examples: {len(X_test)}",
        "",
        "Final results:",
        df_metrics.to_string(index=False),
    ]
    (root / "autoresearch" / "outputs" / "run_log.txt").write_text("\n".join(log_text), encoding="utf-8")

    print("Experiment complete.")
    print(df_metrics.to_string(index=False))
    print("\nGenerated files in results/ and autoresearch/outputs/.")


if __name__ == "__main__":
    main()
