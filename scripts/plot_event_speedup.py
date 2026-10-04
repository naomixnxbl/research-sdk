"""How much cheaper is `event` than `cycle`, at the same horizon/period?

Ratio chart (cycle_time_ms / event_time_ms), one panel per planner, computed
from the same numbers as `plot_execution_time_sweep.py`. Complements that
log-scale trend plot: the log plot shows *how cost scales* with horizon, this
one directly answers "how many times cheaper is event" without making the
reader do log-axis subtraction in their head.

Kept honest on purpose: linear y-axis starting at 0 (never truncate a bar
axis - it exaggerates differences), and a dashed reference line at 1x so
"no benefit" has a visible baseline to compare against.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

# same source numbers as plot_execution_time_sweep.py
planning_time_ms = {
    "voronoi": {
        "cycle_20": {0: 169.4, 50: 209.9, 150: 297.5},
        "cycle_100": {0: 34.9, 50: 45.0, 150: 61.3},
        "event_20": {0: 28.7, 50: 32.3, 150: 48.0},
        "event_100": {0: 11.9, 50: 13.3, 150: 19.0},
    },
    "prm": {
        "cycle_20": {0: 235.7, 50: 312.1, 150: 344.7},
        "cycle_100": {0: 49.8, 50: 62.7, 150: 73.6},
        "event_20": {0: 30.4, 50: 33.3, 150: 36.4},
        "event_100": {0: 15.5, 50: 19.0, 150: 20.4},
    },
    "visibility": {
        "cycle_20": {0: 445.4, 50: 497.3, 150: 514.3},
        "cycle_100": {0: 86.7, 50: 103.8, 150: 104.5},
        "event_20": {0: 96.4, 50: 96.5, 150: 82.0},
        "event_100": {0: 40.6, 50: 45.1, 150: 43.5},
    },
}

PLANNERS = ["voronoi", "prm", "visibility"]
TITLES = {"voronoi": "Voronoi", "prm": "PRM", "visibility": "Visibility"}
HORIZONS = [0, 50, 150]
PERIOD_STYLE = {
    20: dict(color="#1f77b4", label="period 20ms"),
    100: dict(color="#2ca02c", label="period 100ms"),
}


def speedup(planner: str, period: int, horizon: int) -> float:
    cycle = planning_time_ms[planner][f"cycle_{period}"][horizon]
    event = planning_time_ms[planner][f"event_{period}"][horizon]
    return cycle / event


def plot() -> Path:
    fig, axes = plt.subplots(1, len(PLANNERS), figsize=(13, 5), sharey=True)

    x = range(len(HORIZONS))
    width = 0.35

    # sharey=True means whatever ylim is set last wins for every panel, so
    # compute one ceiling up front (with headroom for the bar_label text)
    # instead of calling set_ylim per-axis - otherwise the tallest bars in
    # non-last panels get silently clipped off the top.
    all_ratios = [speedup(p, period, h) for p in PLANNERS for period in [20, 100] for h in HORIZONS]
    y_max = max(all_ratios) * 1.15

    for col, planner in enumerate(PLANNERS):
        ax = axes[col]
        for i, period in enumerate([20, 100]):
            offsets = [xi + (i - 0.5) * width for xi in x]
            vals = [speedup(planner, period, h) for h in HORIZONS]
            bars = ax.bar(offsets, vals, width=width, **PERIOD_STYLE[period])
            ax.bar_label(bars, fmt="%.1fx", fontsize=8, padding=2)

        ax.axhline(1.0, color="black", linestyle="--", linewidth=1, zorder=1)
        ax.set_xticks(list(x))
        ax.set_xticklabels(HORIZONS)
        ax.set_xlabel("Prediction horizon (ms)")
        ax.set_ylim(0, y_max)  # shared, with headroom - never truncate a bar axis
        ax.set_title(TITLES[planner], fontsize=13, fontweight="bold")
        ax.grid(True, axis="y", alpha=0.3)
        if col == 0:
            ax.set_ylabel("Planning time ratio, cycle / event\n(higher = event saves more)")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.05), fontsize=9)
    fig.suptitle(
        "How much cheaper is event-triggered replanning than cycle replanning?\n"
        "(dashed line = 1x, i.e. no difference; n=200 runs per condition)",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0.08, 1, 0.90])

    out_path = OUT_DIR / "event_speedup.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = plot()
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
