"""T12 · Grouped bars (methods x benchmarks) next to a horizontal leaderboard, 1x2 row.
Colour = role, not identity: baselines in GRAY / REDS light-to-dark, "ours" = BLUE, so the
contribution is the only saturated blue in the figure. Value labels via label_values(), no
ticks on the categorical axis, grid only along the value axis. Records drawn numbers in STATS."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
import style
from style import REDS, BLUE, BLUES, INK2, GRAY, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATS = {}

bench = ["MMLU", "GSM8K", "HumanEval"]
methods = {"baseline A": [61.2, 48.0, 30.5], "baseline B": [63.0, 52.4, 33.1], "ours": [64.1, 55.9, 35.0]}
colors = {"baseline A": REDS[0], "baseline B": REDS[1], "ours": BLUE}

fig, axes = plt.subplots(1, 2, figsize=(FULL_W, 2.6), gridspec_kw=dict(wspace=0.45, width_ratios=[1.35, 1]))
ax = axes[0]
x = np.arange(len(bench)); n = len(methods); w = 0.78 / n
for i, (m, v) in enumerate(methods.items()):
    xs = x + (i - (n - 1) / 2) * w
    ax.bar(xs, v, w * 0.92, color=colors[m], label=m)
    style.label_values(ax, xs, v, fmt="{:.1f}", dy=0.6, fontsize=6.3)
ax.set_xticks(x); ax.set_xticklabels(bench)
ax.tick_params(axis="x", length=0); ax.grid(axis="x", visible=False)
ax.set_ylim(0, 75); ax.set_ylabel("score")
ax.set_xlabel("benchmark")
ax.set_title("(a) Per-benchmark scores")
ax.legend(loc="upper right", fontsize=6.6, ncol=3, columnspacing=0.9, handlelength=1.2)

ax = axes[1]
board = {"model 1": 41.3, "model 2": 44.9, "model 3": 46.0, "ours": 51.7, "model 4": 47.8}
names = sorted(board, key=board.get, reverse=True)
vals = [board[k] for k in names]
y = np.arange(len(names))
ax.barh(y, vals, height=0.58, color=[BLUE if k == "ours" else GRAY for k in names])
for yi, v in zip(y, vals):
    ax.text(v + 0.6, yi, "%.1f" % v, va="center", fontsize=7, color=INK2)
ax.set_yticks(y); ax.set_yticklabels(names); ax.invert_yaxis()
ax.tick_params(axis="y", length=0); ax.grid(axis="y", visible=False)
ax.set_xlim(0, 60); ax.set_xlabel("average score")
ax.set_title("(b) Leaderboard")
STATS["ours_avg"] = round(float(np.mean(methods["ours"])), 2)
STATS["ours_board"] = board["ours"]

style.align_xlabels(fig, axes)
STATS["row_misalignment_pt"] = style.check_row(fig, axes)
style.save(fig, "t12_grouped_bars", str(pathlib.Path(__file__).parent / "figs"))
plt.close(fig)
for k_, v_ in STATS.items():
    print(k_, v_)
