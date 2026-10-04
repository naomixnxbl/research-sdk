"""Appendix figure for RQ3: does the horizon effect depend on replan period?

Triggered by a real finding, not a routine check: at period=100ms, PRM's
collision-free rate is an inverted-U over horizon (64.1 -> 80.8 -> 72.5),
and the h=150 point is no longer significantly different from no
prediction at all (McNemar p=0.07 vs. p=0.039 at period=20) - while its
planning time keeps rising significantly getting there (Wilcoxon
p=2.2e-8). That's a materially different story than "diminishing
returns", so it gets its own figure rather than a mention folded into
fig:rq3.

Design, 3rd attempt: a single overlay panel with 3 planners x 2 periods
(6 lines) was unreadable. Line+bar per planner cut it to 3 shapes but
still asked the reader to track 3 colours x 2 encodings x 3 panels at
once. This version drops to small multiples instead: one column per
planner, only 2 lines per subplot (period=20 vs. period=100, colour is
the only encoding, same two colours reused in every subplot) - so
"do these two lines move the same way" is a one-glance comparison per
planner, and PRM's column is visibly different from the other two rather
than something you have to isolate out of a shared, busy panel.

Row 1: collision-free rate (the safety half). Row 2: planning time
median/run (the cost half, the metric with the strongest, most
significant rise for PRM - see prose). Row 3: pooled rebuild failure rate
(%) - added alongside the period=20-only version in fig:rq3 so the
period=100 failure-rate numbers quoted in "Take-away"/"Why PRM reverses"
have the same table/figure backing as everything else, instead of being
prose-only. Same slice as fig:rq3 (replan_policy=event), same matched
(scenario, planner) set (n=191 Voronoi, 167 PRM, 167 Visibility). Source:
results/acra-sweep-patrol/runs.csv, recomputed directly (this cross-period
breakdown isn't in any of Emma's precomputed grid_*.csv files).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

PLANNERS = ["voronoi", "prm", "visibility"]
TITLES = {"voronoi": "Voronoi", "prm": "PRM", "visibility": "Visibility"}
HORIZONS = [0, 50, 150]
X = list(range(len(HORIZONS)))

PERIOD_STYLE = {
    20: dict(color="#1f77b4", marker="o", label="period=20ms (primary)"),
    100: dict(color="#ff7f0e", marker="s", label="period=100ms (check)"),
}

# period=20: matches fig:rq3 exactly. period=100: recomputed this session,
# matched exclusion, McNemar/Wilcoxon vs. h=0 reported in prose.
collision_free_pct = {
    "voronoi": {20: {0: 77.5, 50: 88.0, 150: 92.1}, 100: {0: 72.8, 50: 84.8, 150: 87.4}},
    "prm": {20: {0: 71.3, 50: 83.8, 150: 79.6}, 100: {0: 64.1, 50: 80.8, 150: 72.5}},
    "visibility": {20: {0: 64.1, 50: 66.5, 150: 68.3}, 100: {0: 59.9, 50: 65.3, 150: 64.7}},
}
planning_ms_median = {
    "voronoi": {20: {0: 22.28, 50: 26.65, 150: 40.96}, 100: {0: 10.21, 50: 10.99, 150: 17.32}},
    "prm": {20: {0: 21.96, 50: 25.61, 150: 31.85}, 100: {0: 14.00, 50: 15.78, 150: 18.74}},
    "visibility": {20: {0: 66.51, 50: 62.14, 150: 65.78}, 100: {0: 29.04, 50: 35.41, 150: 35.22}},
}
# Pooled rebuild failure rate (see plot_rq3_prediction_tradeoff.py for the
# definition and small-sample sanity check). period=20 matches fig:rq3's
# 4th panel exactly; period=100 recomputed this session directly from
# runs.csv (same matched set). Backs the "Take-away"/"Why PRM reverses"
# period-comparison numbers (72.7->85.3% at period=20 vs. 51.9->70.6% at
# period=100 for PRM).
failure_rate_pct = {
    "voronoi": {20: {0: 10.3, 50: 6.6, 150: 7.8}, 100: {0: 5.8, 50: 4.4, 150: 4.5}},
    "prm": {20: {0: 68.7, 50: 72.7, 150: 85.3}, 100: {0: 52.8, 50: 51.9, 150: 70.6}},
    "visibility": {20: {0: 52.8, 50: 63.4, 150: 78.7}, 100: {0: 37.3, 50: 44.3, 150: 58.6}},
}

ROWS = [
    (collision_free_pct, "Collision-free rate (%)", "↑ higher is better", (0, 100)),
    (planning_ms_median, "Planning time\n(ms, median/run)", "↓ lower is better", None),
    (failure_rate_pct, "Rebuild failure rate\n(%, pooled)", "↓ lower is better", (0, 100)),
]


def plot() -> Path:
    fig, axes = plt.subplots(len(ROWS), len(PLANNERS), figsize=(13, 10.5), sharex=True)

    for row, (data, ylabel, direction_label, ylim) in enumerate(ROWS):
        for col, planner in enumerate(PLANNERS):
            ax = axes[row][col]
            for period, style in PERIOD_STYLE.items():
                ys = [data[planner][period][h] for h in HORIZONS]
                ax.plot(X, ys, linewidth=2.5, markersize=8, **style)
            ax.grid(True, alpha=0.3)
            if ylim:
                ax.set_ylim(*ylim)
            if col == 0:
                ax.set_ylabel(f"{ylabel}\n({direction_label})")
            if row == 0:
                ax.set_title(TITLES[planner], fontsize=13)
            if row == len(ROWS) - 1:
                ax.set_xticks(X)
                ax.set_xticklabels(["0\n(no pred.)", "50", "150"])
                ax.set_xlabel("Prediction horizon (ms)")

    # Call out the finding directly on the one subplot that shows it: PRM's
    # collision-free rate, top row, middle column - the two lines converge
    # at h=50 then split apart again at h=150, the only place in the whole
    # grid that happens.
    ax = axes[0][1]
    ax.annotate(
        "period=100 peaks here,\nfalls back at h=150\n(n.s. vs. no prediction)",
        xy=(2, 72.5), xytext=(0.3, 35),
        fontsize=8.5, color="#ff7f0e",
        arrowprops=dict(arrowstyle="->", color="#ff7f0e", alpha=0.9),
    )

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.02), fontsize=10)
    fig.suptitle(
        "RQ3 appendix: does the horizon effect hold across replan period?\n"
        "policy=event, matched n=191 (Voronoi) / 167 (PRM, Visibility) — read each column top-to-bottom, "
        "then compare columns",
        fontsize=12, y=0.985,
    )
    fig.tight_layout(rect=[0, 0.035, 1, 0.955])

    out_path = OUT_DIR / "rq3_period_interaction_appendix.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"wrote {plot()}")


if __name__ == "__main__":
    main()
