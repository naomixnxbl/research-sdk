"""RQ3: does velocity-profiling prediction reduce replans and collisions?

Isolated slice: replan_policy=event only (the RQ2 winner), replan_period_ms=20,
prediction_horizon_ms in {0, 50, 150} - so the only thing varying is
foresight. Source: results/acra-sweep-patrol/runs.csv, filtered to the same
matched (scenario, planner) set used everywhere else in this paper (drop any
pair that failed to plan under *any* tested policy/setting - n=191 Voronoi,
167 PRM, 167 Visibility). horizon=0 here is the identical condition reported
as the "event" column of Table tab:event, and matches it exactly (77.5/
71.3/64.1% collision-free; this figure previously read from summary.csv,
which is unfiltered (n=200) and did not match Table tab:event - fixed).

3 panels, one line per planner: collision-free rate (the safety half of
the RQ), rebuild failure rate (%, pooled across matched runs - total
failed rebuilds / total requested rebuilds, i.e. what fraction of the
trigger's requests came back with no route at all - the number actually
quoted in "What prediction costs"), replans median/run (the typical-case
cost, same statistic as Table tab:event, deliberately - replan_count is
heavily right-skewed, so a mean here would tell a different, tail-driven
story than the median). Framed to show the trade-off honestly rather than
assume the RQ's premise holds.

A 4th panel (raw total replan failures, log scale) was tried and dropped:
it's the same underlying counts as the failure-rate panel, just
unnormalized, and the prose cites the rate ("68.7% of the time"), not the
raw total - so the panel added a line to read without adding information.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

PLANNERS = ["voronoi", "prm", "visibility"]
TITLES = {"voronoi": "Voronoi", "prm": "PRM", "visibility": "Visibility"}
HORIZONS = [0, 50, 150]

PLANNER_STYLE = {
    "voronoi": dict(color="#1f77b4", marker="o", label="Voronoi"),
    "prm": dict(color="#2ca02c", marker="^", label="PRM"),
    "visibility": dict(color="#d62728", marker="s", label="Visibility"),
}

collision_free_pct = {
    "voronoi": {0: 77.5, 50: 88.0, 150: 92.1},
    "prm": {0: 71.3, 50: 83.8, 150: 79.6},
    "visibility": {0: 64.1, 50: 66.5, 150: 68.3},
}
replans_median = {
    "voronoi": {0: 2.0, 50: 4.0, 150: 14.0},
    "prm": {0: 2.0, 50: 2.0, 150: 2.0},
    "visibility": {0: 6.0, 50: 6.0, 150: 6.0},
}
# Pooled failure rate = 100 * sum(replan_failures) / sum(replan_count +
# replan_failures) across the matched set, summed before dividing (not a
# per-run median of the ratio) - per-run attempt counts range from 0 to
# 200+, so a per-run ratio is dominated by small-denominator runs; pooling
# first was checked against the underlying per-run distribution (e.g. PRM
# h=150/period=20: median denom=16, failures spread smoothly across
# 5-95%, not bimodal at 0/100 - a real rate, not a small-sample artifact).
# Recomputed directly from runs.csv this session; backs the numbers quoted
# in "What prediction costs".
failure_rate_pct = {
    "voronoi": {0: 10.3, 50: 6.6, 150: 7.8},
    "prm": {0: 68.7, 50: 72.7, 150: 85.3},
    "visibility": {0: 52.8, 50: 63.4, 150: 78.7},
}

PANELS = [
    (collision_free_pct, "Collision-free rate (%)", "↑ higher is better", False),
    (failure_rate_pct, "Rebuild failure rate (%)", "↓ lower is better (pooled)", False),
    (replans_median, "Replans (median/run)", "↓ lower is better", False),
]


def plot() -> Path:
    fig, axes = plt.subplots(1, len(PANELS), figsize=(15, 5))

    for col, (data, ylabel, direction_label, log_scale) in enumerate(PANELS):
        ax = axes[col]
        for planner in PLANNERS:
            ys = [data[planner][h] for h in HORIZONS]
            ax.plot(HORIZONS, ys, linewidth=2, markersize=7, **PLANNER_STYLE[planner])
        # h=0 is not just "the smallest horizon tested" - it's the no-prediction
        # baseline (the exact RQ2 event@period=20 condition). Padding the left
        # of the axis and marking it explicitly keeps that reading obvious
        # without needing a second, redundant "prediction vs. none" figure.
        ax.set_xlim(-18, 165)
        ax.axvline(0, color="gray", linestyle=":", alpha=0.6, linewidth=1.2, zorder=0)
        ax.set_xticks(HORIZONS)
        ax.set_xticklabels(["0\n(no prediction)", "50", "150"])
        ax.set_xlabel("Prediction horizon (ms)")
        ax.set_ylabel(f"{ylabel}\n({direction_label})")
        ax.grid(True, alpha=0.3)
        if log_scale:
            ax.set_yscale("log")
        if col == 0:
            # PRM's 83.8->79.6 dip at h=150 is real (verified against
            # runs.csv) but easy to miss on a 0-100 scale, where Voronoi's
            # 77.5->92.1 climb dominates the eye. Zooming to the range the
            # data actually occupies makes the reversal visible without
            # changing a single plotted value.
            ax.set_ylim(55, 100)
        elif col == 1:
            ax.set_ylim(0, 100)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.03), fontsize=10)
    fig.suptitle(
        "Prediction horizon effect on safety and replanning\n"
        "policy=event, period=20ms, matched n=191 (Voronoi) / 167 (PRM, Visibility)",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0.08, 1, 0.90])

    out_path = OUT_DIR / "rq3_prediction_tradeoff.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"wrote {plot()}")


if __name__ == "__main__":
    main()
