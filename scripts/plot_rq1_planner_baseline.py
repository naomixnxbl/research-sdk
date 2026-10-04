"""RQ1: which planner has the least planning time?

Isolated slice: replan_policy="once", prediction_horizon_ms=0 only - no
replanning, no prediction, so planner identity is the only thing varying.
Source: results/acra-sweep-patrol/summary.csv.

Two panels: planning time (mean + p95, the "least planning time" question)
and completion/collision-free rate (the reliability/safety context needed so
"fastest" isn't read as "best" in isolation).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

PLANNERS = ["voronoi", "prm", "visibility"]
TITLES = {"voronoi": "Voronoi", "prm": "PRM", "visibility": "Visibility"}

planning_time_mean_ms = {"voronoi": 3.278429, "prm": 5.204248, "visibility": 7.530860}
planning_time_p95_ms = {"voronoi": 8.190955, "prm": 13.746652, "visibility": 19.341326}
# completion rate dropped: 99.5/97.5/97.5% - no meaningful difference, not
# worth a panel. collision_episodes (total bump count) replaces it - it
# differentiates the planners more than max_collision does (7/7/6, flat).
collision_free_rate_pct = {"voronoi": 33.0, "prm": 39.5, "visibility": 39.0}
collision_episodes_total = {"voronoi": 260, "prm": 226, "visibility": 205}


def plot() -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    x = list(range(len(PLANNERS)))
    width = 0.35

    # Dot = mean, whisker = upward-only to p95. Not a symmetric CI: p95 is a
    # tail/worst-case statistic, not an uncertainty band on the mean, so a
    # two-sided error bar here would misrepresent it as something it isn't.
    ax = axes[0]
    means = [planning_time_mean_ms[p] for p in PLANNERS]
    p95s = [planning_time_p95_ms[p] for p in PLANNERS]
    upper_err = [p95 - mean for mean, p95 in zip(means, p95s)]
    ax.errorbar(
        x, means, yerr=[[0] * len(x), upper_err],
        fmt="o", markersize=10, color="#1f77b4", ecolor="#1f77b4",
        elinewidth=2, capsize=6, capthick=2, label="mean (whisker to p95)",
    )
    for xi, p95 in zip(x, p95s):
        ax.annotate(f"p95={p95:.1f}", (xi, p95), textcoords="offset points",
                    xytext=(8, 0), fontsize=8, color="#1f77b4", va="center")
    ax.set_xticks(x)
    ax.set_xticklabels([TITLES[p] for p in PLANNERS])
    ax.set_xlim(-0.5, len(PLANNERS) - 0.5)
    ax.set_ylabel("Planning time (ms)\n(↓ lower is better)")
    ax.set_title("Planning time: mean, whisker to p95 (worst case)")
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(fontsize=9, loc="upper left")

    ax = axes[1]
    bars = ax.bar(x, [collision_free_rate_pct[p] for p in PLANNERS], width=0.5,
                   color="#7f7f7f", label="collision-free rate (%)")
    ax.set_xticks(x)
    ax.set_xticklabels([TITLES[p] for p in PLANNERS])
    ax.set_ylabel("Collision-free rate (%)\n(↑ higher is better)")
    ax.set_ylim(0, 100)
    ax.grid(True, axis="y", alpha=0.3)

    ax2 = ax.twinx()
    ax2.plot(x, [collision_episodes_total[p] for p in PLANNERS], color="#d62728",
              marker="o", markersize=8, linewidth=2, label="collision episodes (total)")
    ax2.set_ylabel("Collision episodes, total n=200\n(↓ lower is better)", color="#d62728")
    ax2.tick_params(axis="y", colors="#d62728")
    ax2.set_ylim(0, max(collision_episodes_total.values()) * 1.2)

    ax.set_title("Collision-free rate & episode count (context)")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=9, loc="upper center")

    fig.suptitle(
        "Planner baseline: planning time and collision safety\n"
        "policy=once, horizon=0, n=200 runs per planner",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.90])

    out_path = OUT_DIR / "rq1_planner_baseline.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"wrote {plot()}")


if __name__ == "__main__":
    main()
