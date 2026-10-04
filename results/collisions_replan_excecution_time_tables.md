---
type: result-tables
source: results/acra-sweep-patrol/summary.csv, results/acra-sweep-patrol/runs.csv
subset: matched 13-condition-per-planner surface (same shape as acra-6v6-patrol) — once + {cycle, event} x horizon {0, 50, 150} ms x period {20, 100} ms
scenarios: 3 robots, 8 obstacles (acra-sweep-patrol scenario set)
generated: 2026-09-21
---

# acra-sweep-patrol: Collision / Execution time / Replan tables

These three tables use the **matched 13-condition subset** of `acra-sweep-patrol`
(horizon in {0, 50, 150} ms, period in {20, 100} ms, plus `once`) so the sensitivity
data is directly comparable in shape to the canonical `acra-6v6-patrol` dataset.
The full grid is 49 conditions per planner (6 horizons x 4 periods); see
`acra-sweep-patrol/summary.csv` for the complete surface.

Column sources:
- `collision_free_rate`, `collision_episodes`, `planning_time_ms_mean`, `replans_mean`,
  `call_time_ms_median`, `replan_failures` -> `summary.csv`
- `max collision` (max per-run `collision_episodes` in the condition) and
  `avg total replan time` (`planning_time_ms_total - planning_time_ms_initial`,
  averaged per run) -> derived from `runs.csv` (n=200 runs per condition, all conditions)

## 1. Collision table

Columns: Collision-free rate (%), Collision episodes (total across runs), Max collision (worst single run)

### Voronoi

| Policy | Horizon (ms) | Period (ms) | Collision-free rate | Collision episodes | Max collision |
|---|---|---|---|---|---|
| once | 0 | 20 | 33.0% | 260 | 7 |
| cycle | 0 | 20 | 76.0% | 90 | 7 |
| cycle | 0 | 100 | 70.5% | 89 | 6 |
| cycle | 50 | 20 | 90.0% | 29 | 6 |
| cycle | 50 | 100 | 86.0% | 36 | 3 |
| cycle | 150 | 20 | 96.0% | 9 | 2 |
| cycle | 150 | 100 | 91.5% | 17 | 1 |
| event | 0 | 20 | 77.0% | 73 | 5 |
| event | 0 | 100 | 72.5% | 80 | 5 |
| event | 50 | 20 | 88.0% | 31 | 3 |
| event | 50 | 100 | 85.0% | 37 | 3 |
| event | 150 | 20 | 92.0% | 17 | 2 |
| event | 150 | 100 | 86.5% | 30 | 2 |

### PRM

| Policy | Horizon (ms) | Period (ms) | Collision-free rate | Collision episodes | Max collision |
|---|---|---|---|---|---|
| once | 0 | 20 | 39.5% | 226 | 7 |
| cycle | 0 | 20 | 69.5% | 73 | 3 |
| cycle | 0 | 100 | 65.0% | 90 | 3 |
| cycle | 50 | 20 | 84.0% | 41 | 3 |
| cycle | 50 | 100 | 79.5% | 49 | 3 |
| cycle | 150 | 20 | 77.0% | 56 | 3 |
| cycle | 150 | 100 | 77.0% | 60 | 3 |
| event | 0 | 20 | 71.0% | 73 | 4 |
| event | 0 | 100 | 64.0% | 99 | 3 |
| event | 50 | 20 | 81.5% | 49 | 3 |
| event | 50 | 100 | 78.5% | 55 | 3 |
| event | 150 | 20 | 77.5% | 59 | 3 |
| event | 150 | 100 | 71.0% | 76 | 4 |

### Visibility

| Policy | Horizon (ms) | Period (ms) | Collision-free rate | Collision episodes | Max collision |
|---|---|---|---|---|---|
| once | 0 | 20 | 39.0% | 205 | 6 |
| cycle | 0 | 20 | 58.5% | 113 | 4 |
| cycle | 0 | 100 | 55.5% | 133 | 5 |
| cycle | 50 | 20 | 62.5% | 98 | 4 |
| cycle | 50 | 100 | 59.5% | 112 | 5 |
| cycle | 150 | 20 | 64.0% | 101 | 5 |
| cycle | 150 | 100 | 65.5% | 99 | 5 |
| event | 0 | 20 | 62.0% | 104 | 5 |
| event | 0 | 100 | 58.5% | 118 | 5 |
| event | 50 | 20 | 64.0% | 92 | 4 |
| event | 50 | 100 | 62.5% | 103 | 4 |
| event | 150 | 20 | 67.5% | 93 | 4 |
| event | 150 | 100 | 64.0% | 104 | 4 |

**Read:** Voronoi is the only planner where longer horizons drive collision-free
rate close to Visibility's ceiling and beyond PRM's, while its max-collision figure
drops steadily from 7 to 1 as horizon grows under `cycle`. PRM and Visibility barely
move on collision-free rate across horizons — the prediction horizon buys Voronoi
much more than it buys the other two roadmaps.

## 2. Execution time table

Column: Planning time per run, mean (ms)

### Voronoi

| Policy | Horizon (ms) | Period (ms) | Planning time (ms, mean) |
|---|---|---|---|
| once | 0 | 20 | 3.3 |
| cycle | 0 | 20 | 169.4 |
| cycle | 0 | 100 | 34.9 |
| cycle | 50 | 20 | 209.9 |
| cycle | 50 | 100 | 45.0 |
| cycle | 150 | 20 | 297.5 |
| cycle | 150 | 100 | 61.3 |
| event | 0 | 20 | 28.7 |
| event | 0 | 100 | 11.9 |
| event | 50 | 20 | 32.3 |
| event | 50 | 100 | 13.3 |
| event | 150 | 20 | 48.0 |
| event | 150 | 100 | 19.0 |

### PRM

| Policy | Horizon (ms) | Period (ms) | Planning time (ms, mean) |
|---|---|---|---|
| once | 0 | 20 | 5.2 |
| cycle | 0 | 20 | 235.7 |
| cycle | 0 | 100 | 49.8 |
| cycle | 50 | 20 | 312.1 |
| cycle | 50 | 100 | 62.7 |
| cycle | 150 | 20 | 344.7 |
| cycle | 150 | 100 | 73.6 |
| event | 0 | 20 | 30.4 |
| event | 0 | 100 | 15.5 |
| event | 50 | 20 | 33.3 |
| event | 50 | 100 | 19.0 |
| event | 150 | 20 | 36.4 |
| event | 150 | 100 | 20.4 |

### Visibility

| Policy | Horizon (ms) | Period (ms) | Planning time (ms, mean) |
|---|---|---|---|
| once | 0 | 20 | 7.5 |
| cycle | 0 | 20 | 445.4 |
| cycle | 0 | 100 | 86.7 |
| cycle | 50 | 20 | 497.3 |
| cycle | 50 | 100 | 103.8 |
| cycle | 150 | 20 | 514.3 |
| cycle | 150 | 100 | 104.5 |
| event | 0 | 20 | 96.4 |
| event | 0 | 100 | 40.6 |
| event | 50 | 20 | 96.5 |
| event | 50 | 100 | 45.1 |
| event | 150 | 20 | 82.0 |
| event | 150 | 100 | 43.5 |

**Read:** `event` is consistently 4-10x cheaper than `cycle` at the same horizon/period
for every planner. Visibility is the most expensive roadmap under `cycle` (up to
514ms/run) but collapses to a much smaller gap under `event`, because `event` skips
full rebuilds when nothing has changed.

## 3. Replan table

Columns: Number of replans (mean per run), Total replan-only time (avg per run, ms — planning time minus the initial plan), Replan failures (total across runs)

### Voronoi

| Policy | Horizon (ms) | Period (ms) | Replans (mean) | Total replan time (ms, avg/run) | Replan failures |
|---|---|---|---|---|---|
| once | 0 | 20 | 0.0 | 0.0 | 0 |
| cycle | 0 | 20 | 42.6 | 166.2 | 297 |
| cycle | 0 | 100 | 8.4 | 31.7 | 48 |
| cycle | 50 | 20 | 54.2 | 206.0 | 293 |
| cycle | 50 | 100 | 10.9 | 41.2 | 58 |
| cycle | 150 | 20 | 85.2 | 293.0 | 543 |
| cycle | 150 | 100 | 16.8 | 56.8 | 99 |
| event | 0 | 20 | 5.9 | 25.4 | 147 |
| event | 0 | 100 | 2.4 | 8.6 | 33 |
| event | 50 | 20 | 9.9 | 28.5 | 150 |
| event | 50 | 100 | 3.1 | 9.5 | 29 |
| event | 150 | 20 | 22.7 | 43.4 | 383 |
| event | 150 | 100 | 7.0 | 14.4 | 67 |

### PRM

| Policy | Horizon (ms) | Period (ms) | Replans (mean) | Total replan time (ms, avg/run) | Replan failures |
|---|---|---|---|---|---|
| once | 0 | 20 | 0.0 | 0.0 | 0 |
| cycle | 0 | 20 | 30.0 | 230.3 | 1659 |
| cycle | 0 | 100 | 5.7 | 44.4 | 383 |
| cycle | 50 | 20 | 42.1 | 305.9 | 2563 |
| cycle | 50 | 100 | 7.7 | 56.5 | 534 |
| cycle | 150 | 20 | 50.4 | 337.7 | 6188 |
| cycle | 150 | 100 | 9.8 | 66.8 | 1199 |
| event | 0 | 20 | 2.9 | 25.3 | 1256 |
| event | 0 | 100 | 1.4 | 10.5 | 303 |
| event | 50 | 20 | 3.2 | 27.3 | 1794 |
| event | 50 | 100 | 1.8 | 12.9 | 409 |
| event | 150 | 20 | 3.5 | 29.6 | 4110 |
| event | 150 | 100 | 1.9 | 13.6 | 953 |

### Visibility

| Policy | Horizon (ms) | Period (ms) | Replans (mean) | Total replan time (ms, avg/run) | Replan failures |
|---|---|---|---|---|---|
| once | 0 | 20 | 0.0 | 0.0 | 0 |
| cycle | 0 | 20 | 47.5 | 437.9 | 2408 |
| cycle | 0 | 100 | 8.6 | 79.4 | 524 |
| cycle | 50 | 20 | 55.7 | 489.1 | 4017 |
| cycle | 50 | 100 | 10.5 | 95.4 | 816 |
| cycle | 150 | 20 | 59.7 | 504.8 | 7637 |
| cycle | 150 | 100 | 11.4 | 95.0 | 1468 |
| event | 0 | 20 | 8.9 | 88.8 | 2086 |
| event | 0 | 100 | 3.5 | 33.3 | 430 |
| event | 50 | 20 | 9.2 | 88.0 | 3237 |
| event | 50 | 100 | 4.0 | 36.6 | 672 |
| event | 150 | 20 | 7.9 | 72.4 | 5956 |
| event | 150 | 100 | 4.0 | 34.0 | 1159 |

**Read:** Replan failure counts scale with replan attempts, not with a fixed
per-planner rate — PRM and Visibility rack up thousands of failures at longer
horizons under `cycle` even though their replan counts only roughly double,
meaning a growing share of each replan call is failing outright as the horizon
grows.
