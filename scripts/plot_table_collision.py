"""Figure for the Collision table: collision-free rate, collision episodes,
max collision, across every condition used in the paper (once, cycle,
event x horizon), one line per planner. Source: results/acra-sweep-patrol/runs.csv.

One shared x-axis (the condition list) serves all three RQs - RQ1 reads the
"once" point, RQ2 reads "cycle" vs "event h=0", RQ3 reads the three "event"
points across horizon. No separate per-RQ figure needed.
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

collision_free_rate = {
    "voronoi": [33.0, 76.0, 77.0, 88.0, 92.0],
    "prm": [39.5, 69.5, 71.0, 81.5, 77.5],
    "visibility": [39.0, 58.5, 62.0, 64.0, 67.5],
}
collision_episodes = {
    "voronoi": [260, 90, 73, 31, 17],
    "prm": [226, 73, 73, 49, 59],
    "visibility": [205, 113, 104, 92, 93],
}
max_collision = {
    "voronoi": [7, 7, 5, 3, 2],
    "prm": [7, 3, 4, 3, 3],
    "visibility": [6, 4, 5, 4, 4],
}

PANELS = [
    (collision_free_rate, "Collision-free rate (%)", "↑ higher is better", False),
    (collision_episodes, "Collision episodes (total, n=200)", "↓ lower is better", False),
    (max_collision, "Max collision (worst single run)", "↓ lower is better", False),
]


def plot() -> Path:
    fig, axes = plt.subplots(1, len(PANELS), figsize=(15, 5))

    for col, (data, ylabel, direction_label, log_scale) in enumerate(PANELS):
        ax = axes[col]
        for planner, style in PLANNER_STYLE.items():
            ax.plot(X, data[planner], linewidth=2, markersize=7, **style)
        ax.set_xticks(X)
        ax.set_xticklabels(CONDITIONS)
        ax.set_ylabel(f"{ylabel}\n({direction_label})")
        ax.grid(True, alpha=0.3)
        if log_scale:
            ax.set_yscale("log")
        if col == 0:
            ax.set_ylim(0, 100)
        ax.axvline(1.5, color="gray", linestyle=":", alpha=0.5, linewidth=1)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.03), fontsize=10)
    fig.suptitle(
        "Collision table - one figure, every condition\n"
        "RQ1: read 'once' | RQ2: read 'cycle' vs 'event h=0' | RQ3: read 'event' across h=0/50/150 "
        "(period=20ms, n=200 runs per condition)",
        fontsize=11,
    )
    fig.tight_layout(rect=[0, 0.08, 1, 0.88])

    out_path = OUT_DIR / "table_collision.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"wrote {plot()}")


if __name__ == "__main__":
    main()
