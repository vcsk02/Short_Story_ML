"""
Create simple custom visuals for the Medium article and slide deck.
These are original diagrams, not copied from the papers.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def rounded_box(ax, xy, width, height, text, fontsize=11):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.5,
        edgecolor="black",
        facecolor="white",
    )
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=fontsize)


def arrow(ax, start, end):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=18, linewidth=1.5))


def save_tsfm_pipeline(root: Path) -> None:
    out = root / "figures" / "architecture" / "tsfm_pipeline.png"
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    rounded_box(ax, (0.04, 0.35), 0.16, 0.28, "Raw\nTime Series")
    rounded_box(ax, (0.28, 0.35), 0.16, 0.28, "Patches /\nTokens")
    rounded_box(ax, (0.52, 0.35), 0.16, 0.28, "Sequence\nEncoder")
    rounded_box(ax, (0.76, 0.35), 0.16, 0.28, "Forecast /\nTask Output")

    arrow(ax, (0.20, 0.49), (0.28, 0.49))
    arrow(ax, (0.44, 0.49), (0.52, 0.49))
    arrow(ax, (0.68, 0.49), (0.76, 0.49))

    ax.text(0.5, 0.88, "Time-Series Foundation Model Pipeline", ha="center", fontsize=18, weight="bold")
    ax.text(0.5, 0.15, "The core idea: convert temporal signals into reusable representations for downstream forecasting.", ha="center", fontsize=11)
    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def save_clean_split(root: Path) -> None:
    out = root / "figures" / "benchmarks" / "clean_temporal_split.png"
    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.plot([0.08, 0.92], [0.45, 0.45], linewidth=2)
    rounded_box(ax, (0.08, 0.55), 0.45, 0.25, "Train\nPast data only")
    rounded_box(ax, (0.55, 0.55), 0.16, 0.25, "Validation\nLater data")
    rounded_box(ax, (0.74, 0.55), 0.18, 0.25, "Test\nFuture data")

    for x in [0.08, 0.53, 0.71, 0.92]:
        ax.plot([x, x], [0.38, 0.52], linewidth=1.5)

    arrow(ax, (0.08, 0.25), (0.92, 0.25))
    ax.text(0.5, 0.16, "Time moves left to right. No future data should leak into training.", ha="center", fontsize=11)
    ax.text(0.5, 0.9, "Leakage-Aware Chronological Evaluation", ha="center", fontsize=18, weight="bold")
    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def save_promise_vs_reality(root: Path) -> None:
    out = root / "figures" / "custom_visuals" / "promise_vs_reality.png"
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.25, 0.92, "The Promise", ha="center", fontsize=20, weight="bold")
    ax.text(0.75, 0.92, "The Reality Check", ha="center", fontsize=20, weight="bold")

    promise = [
        "One model transfers everywhere",
        "Zero-shot forecasting is reliable",
        "Scale always wins",
        "Benchmark wins prove generalization",
    ]
    reality = [
        "Transfer depends on domain match",
        "Zero-shot can be fragile",
        "Smaller tuned models can compete",
        "Leakage can inflate results",
    ]

    y = 0.75
    for p, r in zip(promise, reality):
        rounded_box(ax, (0.07, y - 0.055), 0.36, 0.09, p, fontsize=11)
        rounded_box(ax, (0.57, y - 0.055), 0.36, 0.09, r, fontsize=11)
        arrow(ax, (0.44, y), (0.56, y))
        y -= 0.16

    ax.text(0.5, 0.08, "Main takeaway: TSFMs are promising, but the evidence is conditional.", ha="center", fontsize=12, weight="bold")
    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def save_leakage_diagram(root: Path) -> None:
    out = root / "figures" / "benchmarks" / "leakage_modes.png"
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    rounded_box(ax, (0.06, 0.60), 0.25, 0.18, "Pretraining\nCorpus")
    rounded_box(ax, (0.68, 0.60), 0.25, 0.18, "Evaluation\nBenchmark")
    rounded_box(ax, (0.06, 0.22), 0.25, 0.18, "Correlated\nTemporal Series")
    rounded_box(ax, (0.68, 0.22), 0.25, 0.18, "Test Period\nForecasting")

    arrow(ax, (0.31, 0.69), (0.68, 0.69))
    arrow(ax, (0.31, 0.31), (0.68, 0.31))

    ax.text(0.5, 0.74, "Leakage Mode 1: sample overlap", ha="center", fontsize=12)
    ax.text(0.5, 0.36, "Leakage Mode 2: temporal/correlated overlap", ha="center", fontsize=12)
    ax.text(0.5, 0.92, "Why TSFM Evaluation Can Look Too Good", ha="center", fontsize=18, weight="bold")
    ax.text(0.5, 0.08, "If the test data is not truly unfamiliar, the model may appear more general than it is.", ha="center", fontsize=11)
    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def main() -> None:
    root = repo_root()
    for sub in ["figures/architecture", "figures/benchmarks", "figures/custom_visuals"]:
        (root / sub).mkdir(parents=True, exist_ok=True)
    save_tsfm_pipeline(root)
    save_clean_split(root)
    save_promise_vs_reality(root)
    save_leakage_diagram(root)
    print("Custom figures created.")


if __name__ == "__main__":
    main()
