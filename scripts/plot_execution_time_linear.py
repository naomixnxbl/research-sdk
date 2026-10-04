"""Linear-scale ("raw") companion to plot_execution_time_sweep.py.

Same data, same panel layout, but plotted on a linear y-axis instead of log.
Kept alongside the log version rather than replacing it: log is better for
seeing the shape of `event`'s (near-flat) and `once`'s (tiny) trends, since
they'd otherwise be crushed near zero by `cycle`'s much larger values. This
linear version is useful when the absolute gap in ms is what matters (e.g.
"cycle costs ~300ms more than event"), not the relative/shape comparison.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

planning_time_ms = {
    "voronoi": {
        "once": {0: 3.3},
        "cycle_20": {0: 169.4, 50: 209.9, 150: 297.5},
        "cycle_100": {0: 34.9, 50: 45.0, 150: 61.3},
        "event_20": {0: 28.7, 50: 32.3, 150: 48.0},
        "event_100": {0: 11.9, 50: 13.3, 150: 19.0},
    },
    "prm": {
        "once": {0: 5.2},
        "cycle_20": {0: 235.7, 50: 312.1, 150: 344.7},
        "cycle_100": {0: 49.8, 50: 62.7, 150: 73.6},
        "event_20": {0: 30.4, 50: 33.3, 150: 36.4},
        "event_100": {0: 15.5, 50: 19.0, 150: 20.4},
    },
    "visibility": {
        "once": {0: 7.5},
        "cycle_20": {0: 445.4, 50: 497.3, 150: 514.3},
        "cycle_100": {0: 86.7, 50: 103.8, 150: 104.5},
        "event_20": {0: 96.4, 50: 96.5, 150: 82.0},
        "event_100": {0: 40.6, 50: 45.1, 150: 43.5},
    },
}

PLANNERS = ["voronoi", "prm", "visibility"]
TITLES = {"voronoi": "Voronoi", "prm": "PRM", "visibility": "Visibility"}
SERIES_STYLE = {
    "cycle_20": dict(color="#1f77b4", linestyle="-", marker="o", label="cycle, period 20ms"),
    "cycle_100": dict(color="#2ca02c", linestyle="-", marker="^", label="cycle, period 100ms"),
    "event_20": dict(color="#d62728", linestyle="-", marker="s", label="event, period 20ms"),
    "event_100": dict(color="#9467bd", linestyle="-", marker="D", label="event, period 100ms"),
}
JITTER = {"cycle_20": -3, "cycle_100": -1, "event_20": 1, "event_100": 3}
HORIZONS = [0, 50, 150]


def plot_combined() -> Path:
    fig, axes = plt.subplots(1, len(PLANNERS), figsize=(15, 5), sharex=True, sharey=True)

    all_vals = [
        v
        for planner in PLANNERS
        for series in planning_time_ms[planner].values()
        for v in series.values()
    ]
    row_min, row_max = 0, max(all_vals) * 1.1  # linear: start at 0, never truncate

    for col, planner in enumerate(PLANNERS):
        ax = axes[col]
        for key, style in SERIES_STYLE.items():
            xs = [h + JITTER[key] for h in HORIZONS]
            ys = [planning_time_ms[planner][key][h] for h in HORIZONS]
            ax.plot(xs, ys, **style, linewidth=2, markersize=6)
        once_val = planning_time_ms[planner]["once"][0]
        ax.set_xticks(HORIZONS)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(row_min, row_max)

        ax.axhline(
            once_val, color="black", linestyle=(0, (6, 3)), linewidth=2, label="once (baseline)", zorder=1
        )
        ax.text(
            HORIZONS[-1] - 2, once_val, f"once={once_val:g}",
            color="black", fontsize=8, va="bottom", ha="right", fontweight="bold",
        )

        ax.set_title(TITLES[planner], fontsize=13, fontweight="bold")
        ax.set_xlabel("Prediction horizon (ms)")
        if col == 0:
            ax.set_ylabel("Planning time per run, mean (ms)\n(linear scale)")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.05), fontsize=9)
    fig.suptitle(
        "Planning time (mean) vs. prediction horizon — linear scale\n"
        "(n=200 runs per condition)",
        fontsize=13,
    )
    fig.tight_layout(rect=[0, 0.06, 1, 0.93])

    out_path = OUT_DIR / "execution_time_combined_linear.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    combined_path = plot_combined()
    print(f"wrote {combined_path}")


if __name__ == "__main__":
    main()
