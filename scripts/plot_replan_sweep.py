"""Replan count / total replan time / replan failures vs. prediction horizon,
one panel per planner, for the matched 13-condition subset of
`results/acra-sweep-patrol` (Table 3 in
`results/collisions_replan_excecution_time_tables.md`).

Framed around foresight rather than "static vs. replan": `once` always
replans 0 times by definition (it never replans), so it's omitted here as an
uninformative flat-zero baseline. The interesting question this figure
answers is whether giving `event` more prediction horizon (more foresight
about where obstacles will be) reduces how often/how expensively it still
has to react - i.e. does foresight substitute for reaction.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

replans_mean = {
    "voronoi": {
        "cycle_20": {0: 42.6, 50: 54.2, 150: 85.2},
        "cycle_100": {0: 8.4, 50: 10.9, 150: 16.8},
        "event_20": {0: 5.9, 50: 9.9, 150: 22.7},
        "event_100": {0: 2.4, 50: 3.1, 150: 7.0},
    },
    "prm": {
        "cycle_20": {0: 30.0, 50: 42.1, 150: 50.4},
        "cycle_100": {0: 5.7, 50: 7.7, 150: 9.8},
        "event_20": {0: 2.9, 50: 3.2, 150: 3.5},
        "event_100": {0: 1.4, 50: 1.8, 150: 1.9},
    },
    "visibility": {
        "cycle_20": {0: 47.5, 50: 55.7, 150: 59.7},
        "cycle_100": {0: 8.6, 50: 10.5, 150: 11.4},
        "event_20": {0: 8.9, 50: 9.2, 150: 7.9},
        "event_100": {0: 3.5, 50: 4.0, 150: 4.0},
    },
}

replan_time_ms = {
    "voronoi": {
        "cycle_20": {0: 166.2, 50: 206.0, 150: 293.0},
        "cycle_100": {0: 31.7, 50: 41.2, 150: 56.8},
        "event_20": {0: 25.4, 50: 28.5, 150: 43.4},
        "event_100": {0: 8.6, 50: 9.5, 150: 14.4},
    },
    "prm": {
        "cycle_20": {0: 230.3, 50: 305.9, 150: 337.7},
        "cycle_100": {0: 44.4, 50: 56.5, 150: 66.8},
        "event_20": {0: 25.3, 50: 27.3, 150: 29.6},
        "event_100": {0: 10.5, 50: 12.9, 150: 13.6},
    },
    "visibility": {
        "cycle_20": {0: 437.9, 50: 489.1, 150: 504.8},
        "cycle_100": {0: 79.4, 50: 95.4, 150: 95.0},
        "event_20": {0: 88.8, 50: 88.0, 150: 72.4},
        "event_100": {0: 33.3, 50: 36.6, 150: 34.0},
    },
}

replan_failures = {
    "voronoi": {
        "cycle_20": {0: 297, 50: 293, 150: 543},
        "cycle_100": {0: 48, 50: 58, 150: 99},
        "event_20": {0: 147, 50: 150, 150: 383},
        "event_100": {0: 33, 50: 29, 150: 67},
    },
    "prm": {
        "cycle_20": {0: 1659, 50: 2563, 150: 6188},
        "cycle_100": {0: 383, 50: 534, 150: 1199},
        "event_20": {0: 1256, 50: 1794, 150: 4110},
        "event_100": {0: 303, 50: 409, 150: 953},
    },
    "visibility": {
        "cycle_20": {0: 2408, 50: 4017, 150: 7637},
        "cycle_100": {0: 524, 50: 816, 150: 1468},
        "event_20": {0: 2086, 50: 3237, 150: 5956},
        "event_100": {0: 430, 50: 672, 150: 1159},
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

METRICS = [
    (replans_mean, "Replans (mean per run)", "↓ lower = less reliance on reacting", False),
    (replan_time_ms, "Total replan time (ms, avg/run)", "↓ lower is better", False),
    (replan_failures, "Replan failures (total)", "↓ lower is better", False),
]


def plot_combined() -> Path:
    fig, axes = plt.subplots(len(METRICS), len(PLANNERS), figsize=(15, 13), sharex=True)

    for row, (data, ylabel, direction_label, _is_rate) in enumerate(METRICS):
        row_vals = [
            v
            for planner in PLANNERS
            for series in data[planner].values()
            for v in series.values()
        ]
        span = max(row_vals) - min(row_vals)
        pad = span * 0.08 if span else 1
        row_min, row_max = max(0, min(row_vals) - pad), max(row_vals) + pad

        for col, planner in enumerate(PLANNERS):
            ax = axes[row][col]
            for key, style in SERIES_STYLE.items():
                xs = [h + JITTER[key] for h in HORIZONS]
                ys = [data[planner][key][h] for h in HORIZONS]
                ax.plot(xs, ys, **style, linewidth=2, markersize=6)
            ax.set_xticks(HORIZONS)
            ax.grid(True, alpha=0.3)
            ax.set_ylim(row_min, row_max)

            if row == 0:
                ax.set_title(TITLES[planner], fontsize=13, fontweight="bold")
            if col == 0:
                ax.set_ylabel(f"{ylabel}\n({direction_label})")
            if row == len(METRICS) - 1:
                ax.set_xlabel("Prediction horizon (ms) — foresight")

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.02), fontsize=9)
    fig.suptitle(
        "Does more foresight (prediction horizon) reduce how much a planner still has to react?\n"
        "Replan count, replan time, and replan failures vs. horizon "
        "(n=200 runs per condition; \"once\" omitted - it never replans, so is always 0/0/0)",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0.05, 1, 0.93])

    out_path = OUT_DIR / "replan_combined.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    combined_path = plot_combined()
    print(f"wrote {combined_path}")


if __name__ == "__main__":
    main()
