"""Collision-free rate / episodes / max-collision vs. prediction horizon,
one panel per planner, for the matched 13-condition subset of
`results/acra-sweep-patrol` (same horizon x period shape as `acra-6v6-patrol`).

Source data was hand-extracted from `acra-sweep-patrol/summary.csv` and
`runs.csv` (see `results/acra_sweep_patrol_result_tables.md` for the tables
this reproduces). Outputs three PNGs plus a merged PDF into
`results/acra-sweep-patrol/figures/`.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

collision_free_rate = {
    "voronoi": {
        "once": {0: 33.0},
        "cycle_20": {0: 76.0, 50: 90.0, 150: 96.0},
        "cycle_100": {0: 70.5, 50: 86.0, 150: 91.5},
        "event_20": {0: 77.0, 50: 88.0, 150: 92.0},
        "event_100": {0: 72.5, 50: 85.0, 150: 86.5},
    },
    "prm": {
        "once": {0: 39.5},
        "cycle_20": {0: 69.5, 50: 84.0, 150: 77.0},
        "cycle_100": {0: 65.0, 50: 79.5, 150: 77.0},
        "event_20": {0: 71.0, 50: 81.5, 150: 77.5},
        "event_100": {0: 64.0, 50: 78.5, 150: 71.0},
    },
    "visibility": {
        "once": {0: 39.0},
        "cycle_20": {0: 58.5, 50: 62.5, 150: 64.0},
        "cycle_100": {0: 55.5, 50: 59.5, 150: 65.5},
        "event_20": {0: 62.0, 50: 64.0, 150: 67.5},
        "event_100": {0: 58.5, 50: 62.5, 150: 64.0},
    },
}

collision_episodes = {
    "voronoi": {
        "once": {0: 260},
        "cycle_20": {0: 90, 50: 29, 150: 9},
        "cycle_100": {0: 89, 50: 36, 150: 17},
        "event_20": {0: 73, 50: 31, 150: 17},
        "event_100": {0: 80, 50: 37, 150: 30},
    },
    "prm": {
        "once": {0: 226},
        "cycle_20": {0: 73, 50: 41, 150: 56},
        "cycle_100": {0: 90, 50: 49, 150: 60},
        "event_20": {0: 73, 50: 49, 150: 59},
        "event_100": {0: 99, 50: 55, 150: 76},
    },
    "visibility": {
        "once": {0: 205},
        "cycle_20": {0: 113, 50: 98, 150: 101},
        "cycle_100": {0: 133, 50: 112, 150: 99},
        "event_20": {0: 104, 50: 92, 150: 93},
        "event_100": {0: 118, 50: 103, 150: 104},
    },
}

max_collision = {
    "voronoi": {
        "once": {0: 7},
        "cycle_20": {0: 7, 50: 6, 150: 2},
        "cycle_100": {0: 6, 50: 3, 150: 1},
        "event_20": {0: 5, 50: 3, 150: 2},
        "event_100": {0: 5, 50: 3, 150: 2},
    },
    "prm": {
        "once": {0: 7},
        "cycle_20": {0: 3, 50: 3, 150: 3},
        "cycle_100": {0: 3, 50: 3, 150: 3},
        "event_20": {0: 4, 50: 3, 150: 3},
        "event_100": {0: 3, 50: 3, 150: 4},
    },
    "visibility": {
        "once": {0: 6},
        "cycle_20": {0: 4, 50: 4, 150: 5},
        "cycle_100": {0: 5, 50: 5, 150: 5},
        "event_20": {0: 5, 50: 4, 150: 4},
        "event_100": {0: 5, 50: 4, 150: 4},
    },
}

PLANNERS = ["voronoi", "prm", "visibility"]
TITLES = {"voronoi": "Voronoi", "prm": "PRM", "visibility": "Visibility"}
# Each series gets its own colour + marker (not just linestyle) so two series
# with identical values don't fully hide one another; JITTER nudges each
# series a little left/right of its true horizon for the same reason.
SERIES_STYLE = {
    "cycle_20": dict(color="#1f77b4", linestyle="-", marker="o", label="cycle, period 20ms"),
    "cycle_100": dict(color="#2ca02c", linestyle="-", marker="^", label="cycle, period 100ms"),
    "event_20": dict(color="#d62728", linestyle="-", marker="s", label="event, period 20ms"),
    "event_100": dict(color="#9467bd", linestyle="-", marker="D", label="event, period 100ms"),
}
JITTER = {"cycle_20": -3, "cycle_100": -1, "event_20": 1, "event_100": 3}
HORIZONS = [0, 50, 150]


METRICS = [
    (collision_free_rate, "Collision-free rate (%)", "↑ higher is better", True),
    (collision_episodes, "Collision episodes (total)", "↓ lower is better", False),
    (max_collision, "Max collision (worst run)", "↓ lower is better", False),
]


def plot_combined() -> Path:
    """One figure: rows = metric, columns = planner, so collision-free rate,
    collision episodes, and max collision are all visible together without
    forcing three very different scales onto one shared axis."""
    fig, axes = plt.subplots(len(METRICS), len(PLANNERS), figsize=(15, 13), sharex=True)

    for row, (data, ylabel, direction_label, is_rate) in enumerate(METRICS):
        # Zoom to the cycle/event series only — "once" sits far outside the
        # interesting range (e.g. ~35% collision-free vs. 55-96% for the
        # policies that actually replan) and forcing it into the axis would
        # flatten out the differences we're trying to show. It's still drawn
        # as a dotted baseline and may run off the top/bottom of the panel.
        policy_vals = [
            v
            for planner in PLANNERS
            for key, series in data[planner].items()
            if key != "once"
            for v in series.values()
        ]
        span = max(policy_vals) - min(policy_vals)
        pad = span * 0.08 if span else 1
        row_min, row_max = min(policy_vals) - pad, max(policy_vals) + pad
        if is_rate:
            row_max = min(row_max, 100)

        for col, planner in enumerate(PLANNERS):
            ax = axes[row][col]
            for key, style in SERIES_STYLE.items():
                xs = [h + JITTER[key] for h in HORIZONS]
                ys = [data[planner][key][h] for h in HORIZONS]
                ax.plot(xs, ys, **style, linewidth=2, markersize=6)
            once_val = data[planner]["once"][0]
            ax.set_xticks(HORIZONS)
            ax.grid(True, alpha=0.3)
            ax.set_ylim(row_min, row_max)

            if row_min <= once_val <= row_max:
                ax.axhline(
                    once_val, color="black", linestyle=(0, (6, 3)), linewidth=2, label="once (baseline)", zorder=1
                )
                ax.text(
                    HORIZONS[-1] - 2, once_val, f"once={once_val:g}",
                    color="black", fontsize=8, va="top", ha="right", fontweight="bold",
                )
            else:
                # baseline sits outside the zoomed range — call it out with an
                # arrow pointing off the edge of the panel instead of a hidden line.
                edge = row_max if once_val > row_max else row_min
                va = "top" if once_val > row_max else "bottom"
                ax.annotate(
                    f"once={once_val:g} (off-chart)",
                    xy=(HORIZONS[-1], edge), xytext=(HORIZONS[-1] - 2, edge),
                    color="black", fontsize=8, fontweight="bold", ha="right", va=va,
                )
            if row == 0:
                ax.set_title(TITLES[planner], fontsize=13, fontweight="bold")
            if col == 0:
                ax.set_ylabel(f"{ylabel}\n({direction_label})")
            if row == len(METRICS) - 1:
                ax.set_xlabel("Prediction horizon (ms)")

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.02), fontsize=9)
    fig.suptitle(
        "Collision-free rate, collision episodes and max collision vs. prediction horizon\n"
        "(n=200 runs per condition)",
        fontsize=13,
    )
    fig.tight_layout(rect=[0, 0.04, 1, 0.95])

    out_path = OUT_DIR / "collision_combined.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    combined_path = plot_combined()
    print(f"wrote {combined_path}")


if __name__ == "__main__":
    main()
