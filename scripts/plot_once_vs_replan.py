"""Once vs. replanning summary: collision-free rate and planning time,
averaged across the 6 cycle/event sweep conditions per planner, for the
matched 13-condition subset of `results/acra-sweep-patrol`.

This is the "does replanning help at all" comparison — it sits upstream of
the horizon/period sensitivity plots (`plot_collision_sweep.py`,
`plot_execution_time_sweep.py`), which only compare within the replanning
policies. Source data: `results/collisions_replan_excecution_time_tables.md`.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

PLANNERS = ["voronoi", "prm", "visibility"]
TITLES = {"voronoi": "Voronoi", "prm": "PRM", "visibility": "Visibility"}

# once = single value; cycle/event = mean across the 6 horizon x period
# sweep conditions, so this is a fair "replanning helps" summary rather than
# a best-case cherry-pick.
collision_free_rate = {
    "voronoi": {"once": 33.0, "cycle": 85.0, "event": 83.5},
    "prm": {"once": 39.5, "cycle": 75.3, "event": 73.9},
    "visibility": {"once": 39.0, "cycle": 60.9, "event": 63.1},
}
planning_time_ms = {
    "voronoi": {"once": 3.3, "cycle": 136.3, "event": 25.5},
    "prm": {"once": 5.2, "cycle": 179.8, "event": 25.8},
    "visibility": {"once": 7.5, "cycle": 292.0, "event": 67.4},
}

POLICY_STYLE = {
    "once": dict(color="#7f7f7f", label="once"),
    "cycle": dict(color="#1f77b4", label="cycle (mean over sweep)"),
    "event": dict(color="#d62728", label="event (mean over sweep)"),
}
POLICIES = ["once", "cycle", "event"]


def plot() -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = range(len(PLANNERS))
    width = 0.25

    ax = axes[0]
    for i, policy in enumerate(POLICIES):
        offsets = [xi + (i - 1) * width for xi in x]
        vals = [collision_free_rate[p][policy] for p in PLANNERS]
        ax.bar(offsets, vals, width=width, **POLICY_STYLE[policy])
    ax.set_xticks(list(x))
    ax.set_xticklabels([TITLES[p] for p in PLANNERS])
    ax.set_ylabel("Collision-free rate (%)\n(↑ higher is better)")
    ax.set_title("Collision-free rate: once vs. replanning")
    ax.grid(True, axis="y", alpha=0.3)

    ax = axes[1]
    for i, policy in enumerate(POLICIES):
        offsets = [xi + (i - 1) * width for xi in x]
        vals = [planning_time_ms[p][policy] for p in PLANNERS]
        ax.bar(offsets, vals, width=width, **POLICY_STYLE[policy])
    ax.set_xticks(list(x))
    ax.set_xticklabels([TITLES[p] for p in PLANNERS])
    ax.set_ylabel("Planning time per run, mean (ms)\n(↓ lower is better)")
    ax.set_yscale("log")
    ax.set_title("Planning time: once vs. replanning")
    ax.grid(True, axis="y", which="both", alpha=0.3)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.05), fontsize=9)
    fig.suptitle(
        "Static planning vs. replanning\n(n=200 runs per condition; cycle/event bars are means over the 6-condition sweep)",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0.06, 1, 0.90])

    out_path = OUT_DIR / "once_vs_replan.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = plot()
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
