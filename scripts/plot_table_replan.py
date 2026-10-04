"""Figure for the Replan table: total replan time, replans/run, avg replan
duration, replan failures - across cycle and event x horizon (no "once": it
never replans by definition). Source: results/acra-sweep-patrol/runs.csv.

Same shared-x-axis idea as the other two table figures: RQ2 reads "cycle" vs
"event h=0", RQ3 reads "event" across h=0/50/150.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

CONDITIONS = ["cycle", "event\nh=0", "event\nh=50", "event\nh=150"]
X = list(range(len(CONDITIONS)))

PLANNER_STYLE = {
    "voronoi": dict(color="#1f77b4", marker="o", label="Voronoi"),
    "prm": dict(color="#2ca02c", marker="^", label="PRM"),
    "visibility": dict(color="#d62728", marker="s", label="Visibility"),
}

total_replan_time_ms = {
    "voronoi": [166.20, 25.43, 28.53, 43.39],
    "prm": [230.27, 25.28, 27.30, 29.63],
    "visibility": [437.88, 88.79, 87.99, 72.44],
}
replans_mean = {
    "voronoi": [42.645, 5.905, 9.950, 22.730],
    "prm": [29.975, 2.925, 3.220, 3.540],
    "visibility": [47.455, 8.905, 9.200, 7.855],
}
avg_replan_duration_ms = {
    "voronoi": [3.897, 4.306, 2.867, 1.909],
    "prm": [7.682, 8.643, 8.478, 8.369],
    "visibility": [9.227, 9.971, 9.564, 9.222],
}
replan_failures = {
    "voronoi": [297, 147, 150, 383],
    "prm": [1659, 1256, 1794, 4110],
    "visibility": [2408, 2086, 3237, 5956],
}

PANELS = [
    (total_replan_time_ms, "Total replan time (ms/run)", "↓ lower is better", False),
    (replans_mean, "Replans (mean/run)", "↓ lower is better", False),
    (avg_replan_duration_ms, "Avg. replan duration (ms)", "↓ lower is better", False),
    (replan_failures, "Replan failures (total)", "↓ lower is better (log scale)", True),
]


def plot() -> Path:
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))
    axes = axes.flatten()

    for i, (data, ylabel, direction_label, log_scale) in enumerate(PANELS):
        ax = axes[i]
        for planner, style in PLANNER_STYLE.items():
            ax.plot(X, data[planner], linewidth=2, markersize=7, **style)
        ax.set_xticks(X)
        ax.set_xticklabels(CONDITIONS)
        ax.set_ylabel(f"{ylabel}\n({direction_label})")
        ax.grid(True, alpha=0.3, which="both")
        if log_scale:
            ax.set_yscale("log")
        ax.axvline(0.5, color="gray", linestyle=":", alpha=0.5, linewidth=1)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.01), fontsize=10)
    fig.suptitle(
        "Replan table - one figure, every condition ('once' excluded - it never replans)\n"
        "RQ2: read 'cycle' vs 'event h=0' | RQ3: read 'event' across h=0/50/150 "
        "(period=20ms, n=200 runs per condition)",
        fontsize=11,
    )
    fig.tight_layout(rect=[0, 0.05, 1, 0.90])

    out_path = OUT_DIR / "table_replan.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"wrote {plot()}")


if __name__ == "__main__":
    main()
