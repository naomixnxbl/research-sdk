"""Supporting figure for the RQ2 "Safety" paragraph: is replanning (of either
kind) actually necessary, or would a single plan do?

Source: results/acra-sweep-patrol/analysis/stats.json (once_collision_free_%)
and analysis/event_vs_cycle.csv (collision_free_event_%/collision_free_cycle_%
at prediction_horizon_ms=0, replan_period_ms=20), both produced by
scripts/analyse_sweep.py from runs.csv. All three conditions share the same
per-planner matched scenario set (the scenario,planner pairs excluded because
they failed to produce a plan under *some* tested policy/setting are dropped
globally before any of these percentages are computed), so once/cycle/event
are directly comparable within a planner: n=191 (Voronoi), 167 (PRM),
167 (Visibility).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

PLANNERS = ["voronoi", "prm", "visibility"]
TITLES = {"voronoi": "Voronoi\n(n=191)", "prm": "PRM\n(n=167)", "visibility": "Visibility\n(n=167)"}

collision_free_pct = {
    "voronoi": {"once": 33.5, "cycle": 75.9, "event": 77.5},
    "prm": {"once": 38.9, "cycle": 70.1, "event": 71.3},
    "visibility": {"once": 40.1, "cycle": 60.5, "event": 64.1},
}

POLICY_STYLE = {
    "once": dict(color="#7f7f7f", label="once (never revisited)"),
    "cycle": dict(color="#1f77b4", label="cycle"),
    "event": dict(color="#d62728", label="event"),
}


def plot() -> Path:
    fig, ax = plt.subplots(figsize=(8, 5.5))

    width = 0.26
    x = list(range(len(PLANNERS)))

    for i, policy in enumerate(("once", "cycle", "event")):
        offsets = [xi + (i - 1) * width for xi in x]
        vals = [collision_free_pct[p][policy] for p in PLANNERS]
        ax.bar(offsets, vals, width=width, **POLICY_STYLE[policy])
        for xi, v in zip(offsets, vals):
            ax.annotate(f"{v:.0f}", (xi, v), textcoords="offset points",
                        xytext=(0, 3), ha="center", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels([TITLES[p] for p in PLANNERS])
    ax.set_ylabel("Collision-free rate (%)")
    ax.set_ylim(0, 100)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(fontsize=9, loc="upper left")
    fig.suptitle(
        "Once vs. cycle vs. event: collision-free rate\n"
        "horizon=0, period=20ms",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.90])

    out_path = OUT_DIR / "rq2_once_vs_replan.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"wrote {plot()}")


if __name__ == "__main__":
    main()
