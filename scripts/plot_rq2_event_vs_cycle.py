"""RQ2: does the event trigger reduce unnecessary replanning while keeping
the path usable?

Isolated slice: prediction_horizon_ms=0 only (prediction is RQ3's variable,
held out here), replan_period_ms=20 (the primary operating point used
throughout this section, matching Table tab:event). Source:
results/acra-sweep-patrol/runs.csv, filtered to drop any (scenario, planner)
pair that failed to produce a plan under any policy - the same matched set
used for Table tab:event and rq2_once_vs_replan.png, so all three agree
exactly. The period=100 check (same matched set) is reported in prose
rather than a second row here - see plot_rq2_event_vs_cycle_period100_appendix.py
for that two-row version if it's ever needed for an appendix/rebuttal figure.

Replans and planning time use the MEDIAN per run (not the mean) - same
statistic as Table tab:event, deliberately, so this figure is a direct
visualisation of the table's own numbers rather than a second, different
summary of the same column (replan_count / planning_time_ms_total are both
heavily right-skewed by a handful of hard scenarios, so the mean sits well
above the median and the two would otherwise look like they disagree).

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

# period=20ms, horizon=0, matched n (Voronoi=191, PRM/Visibility=167) - see
# scripts/analyse_sweep.py / runs.csv for the exclusion. Medians match
# Table tab:event exactly (rebuilds: 27/2, 20/2, 30/6; planning time:
# 113.7/22.3, 177.6/22.0, 294.9/66.5, rounded to 114/22, 178/22, 295/67
# in the table).
replans_median = {"voronoi": {"cycle": 27.0, "event": 2.0}, "prm": {"cycle": 20.0, "event": 2.0}, "visibility": {"cycle": 30.0, "event": 6.0}}
planning_time_ms = {"voronoi": {"cycle": 113.741, "event": 22.281}, "prm": {"cycle": 177.646, "event": 21.956}, "visibility": {"cycle": 294.896, "event": 66.515}}
collision_free_pct = {"voronoi": {"cycle": 75.9, "event": 77.5}, "prm": {"cycle": 70.1, "event": 71.3}, "visibility": {"cycle": 60.5, "event": 64.1}}

POLICY_STYLE = {
    "cycle": dict(color="#1f77b4", label="cycle"),
    "event": dict(color="#d62728", label="event"),
}

METRICS = [
    # (data, ylabel, direction_label, decimals) - decimals matches how each
    # quantity is stated in Table tab:event exactly (replans/planning-time:
    # whole numbers; collision-free %: one decimal place), not a magnitude
    # threshold, so a bar label never implies more or less precision than
    # the table row it's a picture of.
    (replans_median, "Replans (median/run)", "↓ lower = less unnecessary work", 0),
    (planning_time_ms, "Planning time (ms, median/run)", "↓ lower is better", 0),
    (collision_free_pct, "Collision-free rate (%)", "↑ parity with cycle = path still usable", 1),
]


def plot() -> Path:
    fig, axes = plt.subplots(1, len(METRICS), figsize=(14, 5))

    width = 0.32
    x = list(range(len(PLANNERS)))

    for col, (data, ylabel, direction_label, decimals) in enumerate(METRICS):
        ax = axes[col]
        for i, policy in enumerate(("cycle", "event")):
            offsets = [xi + (i - 0.5) * width for xi in x]
            vals = [data[p][policy] for p in PLANNERS]
            bars = ax.bar(offsets, vals, width=width, **POLICY_STYLE[policy])
            for xi, v in zip(offsets, vals):
                ax.annotate(f"{v:.{decimals}f}", (xi, v),
                            textcoords="offset points", xytext=(0, 3),
                            ha="center", fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels([TITLES[p] for p in PLANNERS])
        ax.set_ylabel(f"{ylabel}\n({direction_label})")
        ax.grid(True, axis="y", alpha=0.3)
        if "%" in ylabel:
            ax.set_ylim(0, 100)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.02), fontsize=10)
    fig.suptitle(
        "Cycle vs. event by planner\n"
        "horizon=0, period=20ms",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0.08, 1, 0.90])

    out_path = OUT_DIR / "rq2_event_vs_cycle.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"wrote {plot()}")


if __name__ == "__main__":
    main()
