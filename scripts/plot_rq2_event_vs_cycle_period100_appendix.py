"""RQ2: does the event trigger reduce unnecessary replanning while keeping
the path usable?

Isolated slice: prediction_horizon_ms=0 only (prediction is RQ3's variable,
held out here). Two rows, one per replan_period_ms (20 the primary
operating point matching Table tab:event; 100 the secondary check), same
three metrics in both. Source: results/acra-sweep-patrol/runs.csv, filtered
to drop any (scenario, planner) pair that failed to produce a plan under
any policy - the same matched set used for Table tab:event and
rq2_once_vs_replan.png, so all four rows/metrics agree exactly.

Planner is on the x-axis within each metric panel (not a separate subplot
per planner) so Voronoi/PRM/Visibility sit side by side on one shared scale
and can be compared directly, with cycle vs. event as grouped bars.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

PLANNERS = ["voronoi", "prm", "visibility"]
TITLES = {"voronoi": "Voronoi", "prm": "PRM", "visibility": "Visibility"}

# horizon=0, matched n (Voronoi=191, PRM/Visibility=167) - see
# scripts/analyse_sweep.py / runs.csv for the exclusion.
PERIODS = [20, 100]

replans_mean = {
    20: {"voronoi": {"cycle": 43.115, "event": 5.948}, "prm": {"cycle": 29.635, "event": 2.934}, "visibility": {"cycle": 46.856, "event": 8.569}},
    100: {"voronoi": {"cycle": 8.461, "event": 2.361}, "prm": {"cycle": 5.593, "event": 1.407}, "visibility": {"cycle": 8.413, "event": 3.377}},
}
planning_time_ms = {
    20: {"voronoi": {"cycle": 170.745, "event": 28.292}, "prm": {"cycle": 233.697, "event": 30.536}, "visibility": {"cycle": 441.732, "event": 94.109}},
    100: {"voronoi": {"cycle": 35.156, "event": 11.691}, "prm": {"cycle": 49.587, "event": 15.398}, "visibility": {"cycle": 85.641, "event": 39.079}},
}
collision_free_pct = {
    20: {"voronoi": {"cycle": 75.9, "event": 77.5}, "prm": {"cycle": 70.1, "event": 71.3}, "visibility": {"cycle": 60.5, "event": 64.1}},
    100: {"voronoi": {"cycle": 70.16, "event": 72.77}, "prm": {"cycle": 64.67, "event": 64.07}, "visibility": {"cycle": 56.89, "event": 59.88}},
}

POLICY_STYLE = {
    "cycle": dict(color="#1f77b4", label="cycle"),
    "event": dict(color="#d62728", label="event"),
}

METRICS = [
    (replans_mean, "Replans (mean/run)", "↓ lower = less unnecessary work"),
    (planning_time_ms, "Planning time (ms, mean/run)", "↓ lower is better"),
    (collision_free_pct, "Collision-free rate (%)", "↑ parity with cycle = path still usable"),
]


def plot() -> Path:
    fig, axes = plt.subplots(len(PERIODS), len(METRICS), figsize=(14, 9.5))

    width = 0.32
    x = list(range(len(PLANNERS)))

    for row, period in enumerate(PERIODS):
        for col, (data, ylabel, direction_label) in enumerate(METRICS):
            ax = axes[row][col]
            for i, policy in enumerate(("cycle", "event")):
                offsets = [xi + (i - 0.5) * width for xi in x]
                vals = [data[period][p][policy] for p in PLANNERS]
                ax.bar(offsets, vals, width=width, **POLICY_STYLE[policy])
                for xi, v in zip(offsets, vals):
                    ax.annotate(f"{v:.0f}" if v >= 10 else f"{v:.1f}", (xi, v),
                                textcoords="offset points", xytext=(0, 3),
                                ha="center", fontsize=8)
            ax.set_xticks(x)
            ax.set_xticklabels([TITLES[p] for p in PLANNERS])
            row_label = f"period={period}ms\n" if col == 0 else ""
            ax.set_ylabel(f"{row_label}{ylabel}\n({direction_label})")
            ax.grid(True, axis="y", alpha=0.3)
            if "%" in ylabel:
                ax.set_ylim(0, 100)

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.01), fontsize=10)
    fig.suptitle(
        "Cycle vs. event by planner, horizon=0\n"
        "top: period=20ms (primary) — bottom: period=100ms (check)",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0.05, 1, 0.93])

    out_path = OUT_DIR / "rq2_event_vs_cycle.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"wrote {plot()}")


if __name__ == "__main__":
    main()
