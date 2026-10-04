"""Figure for the Execution time table: mean planning time per run, across
every condition used in the paper (once, cycle, event x horizon), one line
per planner. Source: results/acra-sweep-patrol/runs.csv.

Same shared-x-axis idea as plot_table_collision.py: RQ1 reads "once", RQ2
reads "cycle" vs "event h=0", RQ3 reads "event" across horizon.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "acra-sweep-patrol" / "figures"

CONDITIONS = ["once", "cycle", "event\nh=0", "event\nh=50", "event\nh=150"]
X = list(range(len(CONDITIONS)))

PLANNER_STYLE = {
    "voronoi": dict(color="#1f77b4", marker="o", label="Voronoi"),
    "prm": dict(color="#2ca02c", marker="^", label="PRM"),
    "visibility": dict(color="#d62728", marker="s", label="Visibility"),
}

exec_time_ms = {
    "voronoi": [3.28, 169.44, 28.65, 32.30, 47.96],
    "prm": [5.20, 235.74, 30.39, 33.31, 36.40],
    "visibility": [7.53, 445.45, 96.36, 96.52, 82.04],
}


def plot() -> Path:
    fig, ax = plt.subplots(1, 1, figsize=(7, 5.5))

    for planner, style in PLANNER_STYLE.items():
        ax.plot(X, exec_time_ms[planner], linewidth=2, markersize=7, **style)
    ax.set_xticks(X)
    ax.set_xticklabels(CONDITIONS)
    ax.set_ylabel("Execution time (ms, mean/run)\n(↓ lower is better, log scale)")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3, which="both")
    ax.axvline(1.5, color="gray", linestyle=":", alpha=0.5, linewidth=1)
    ax.legend(fontsize=10)

    fig.suptitle(
        "Execution time table - one figure, every condition\n"
        "RQ1: read 'once' | RQ2: read 'cycle' vs 'event h=0' | RQ3: read 'event' across h=0/50/150 "
        "(period=20ms, n=200 runs per condition)",
        fontsize=11,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.85])

    out_path = OUT_DIR / "table_exectime.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"wrote {plot()}")


if __name__ == "__main__":
    main()
