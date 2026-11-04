"""T7 · LR-schedule schematic.
Main run = INK solid, alternative = RED dashed, "no decay" = INK dotted, merge window = BLUES[0]
axvspan. Panels share y; the right panel hides its y tick labels."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import style
from style import RED, BLUES, INK, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
SPAN = dict(color=BLUES[0], alpha=0.35, lw=0)

fig, axes = plt.subplots(1, 2, figsize=(FULL_W, 2.5), sharey=True, gridspec_kw=dict(wspace=0.2))
x = np.linspace(0, 1, 400); wu = 0.03
const = np.minimum(1.0, x / wu)

ax = axes[0]
ax.plot(x, const, color=INK, lw=1.8, zorder=3)
for f in (0.30, 0.55, 0.80):                                   # forked decays + merge windows
    ax.axvspan(f - 0.08, f, **SPAN)
    ax.plot([f, f + 0.08], [1, 0], color=RED, lw=1.6, ls=(0, (5, 2.5)), zorder=3)
ax.set_title("(a) Evaluating intermediate checkpoints")
ax.set_ylabel("learning rate (relative)")
ax.legend(handles=[Line2D([], [], color=INK, lw=1.8, label="main run (constant LR)"),
                   Line2D([], [], color=RED, lw=1.6, ls=(0, (5, 2.5)), label="forked decay (extra compute)"),
                   Patch(**SPAN, label="merge window (free)")], loc="lower left")

ax = axes[1]
t0 = 0.85
wsd = np.where(x < t0, const, 1 - (x - t0) / (1 - t0))
ax.axvspan(t0, 1.0, **SPAN)
ax.plot(x, wsd, color=RED, lw=1.8, zorder=3)
ax.plot(x, const, color=INK, lw=1.8, ls=(0, (1, 1.5)), zorder=4)
ax.set_title("(b) Producing the released model")
ax.tick_params(labelleft=False)
ax.legend(handles=[Line2D([], [], color=RED, lw=1.8, label="WSD: decay before release"),
                   Line2D([], [], color=INK, lw=1.8, ls=(0, (1, 1.5)), label="WSM: no decay"),
                   Patch(**SPAN, label="WSM: merge window")], loc="lower left")

for ax in axes:
    ax.set_xlim(0, 1); ax.set_ylim(-0.04, 1.18); ax.set_xticks([0, 0.5, 1]); ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel("training progress")
style.align_xlabels(fig, axes)
print("row_misalignment_pt", style.check_row(fig, axes))
style.save(fig, "t7_schedule", str(pathlib.Path(__file__).parent / "figs"))
