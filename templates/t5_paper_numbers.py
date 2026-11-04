"""T5 · Redrawing numbers from a paper's table.
(a) categorical bars: light-to-dark within a family = order/size, BLUE = the "it works" bar;
(b) score vs. #ckpts with value labels and a RED dashed baseline labelled at its right end."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
import style
from style import REDS, BLUES, INK2, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATS = {}

fig, axes = plt.subplots(1, 2, figsize=(FULL_W * 0.8, 2.5), gridspec_kw=dict(width_ratios=[0.9, 1.1], wspace=0.4))

ax = axes[0]
vals = np.array([1.00, 1.03, 0.97, 0.04])                      # <- table values
labels = ["SGD", "SGD\n+M", "EMA\nreset", "offline\nmean"]       # short, grouped, never rotated
ax.bar(np.arange(4), vals, color=[REDS[0], REDS[1], REDS[2], BLUES[1]], width=0.62)
style.label_values(ax, np.arange(4), vals, dy=0.03)
ax.set_xticks(np.arange(4)); ax.set_xticklabels(labels, fontsize=7)
ax.set_ylim(0, 1.25); ax.grid(axis="x", visible=False)
ax.set_ylabel("stationary excess (rel.)")
ax.set_xlabel("averaging scheme")
ax.set_title("(a) Absorbed in the loop")

ax = axes[1]
N = np.array([1, 2, 4, 8, 16]); score = np.array([60.3, 62.8, 63.4, 63.8, 63.6])   # <- table values
base = 62.7
ax.plot(N, score, "-o", color=BLUES[1], mec="white", mew=0.8, ms=6, lw=1.4)
style.label_values(ax, N, score, dy=[-0.3, 0.28, 0.28, 0.28, 0.28])   # first label below: avoids the steep segment
ax.axhline(base, color=REDS[1], lw=1.0, ls=style.DASH_S)
ax.text(16, base - 0.25, "baseline %.1f" % base, ha="right", va="top", fontsize=7, color=REDS[2])
ax.set_xscale("log", base=2); ax.set_xticks(N); ax.set_xticklabels([str(n) for n in N]); ax.minorticks_off()
ax.set_xlim(0.8, 20); ax.set_ylim(59.3, 64.8)
ax.set_xlabel("checkpoints in the window"); ax.set_ylabel("benchmark average")
ax.set_title("(b) Method, model (Table N)")
STATS["best_N"] = int(N[np.argmax(score)]); STATS["best_minus_base"] = float(score.max() - base)

style.align_xlabels(fig, axes)
STATS["row_misalignment_pt"] = style.check_row(fig, axes)
style.save(fig, "t5_paper_numbers", str(pathlib.Path(__file__).parent / "figs"))
for k_, v_ in STATS.items():
    print(k_, v_)
