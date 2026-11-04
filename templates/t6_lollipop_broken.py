"""T6 · Lollipop + broken-axis dot plot in one row.
Alignment rule 3: the right side has "ticks + x-label" (two lines), so the left side's
category labels are also two lines (names / grouped dataset), line 2 placed on the right
x-label's baseline. Prints the measured gap (should be 0 pt)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory
import style
from style import REDS, BLUES, RED, BLUE, INK, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATS = {}

fig = plt.figure(figsize=(FULL_W, 2.6))
gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 1], height_ratios=[1, 1], wspace=0.3, hspace=0.12)
axA = fig.add_subplot(gs[:, 0])
axT = fig.add_subplot(gs[0, 1]); axL = fig.add_subplot(gs[1, 1], sharex=axT)

# (a) lollipop
items = [("net-1", 0.0), ("net-2", 1.5), ("net-3", 3.0), ("net-4", 16.0), ("net-5", 20.0)]   # <- data
x = np.arange(len(items))
for xx, (name, v) in zip(x, items):
    axA.plot([xx, xx], [0, v], color=BLUE, lw=2.2, solid_capstyle="butt", zorder=3)
    axA.plot([xx], [v], **style.dot(BLUE, ms=6, zorder=4, clip_on=False))
    axA.text(xx, v + 0.9, f"{v:g}%", ha="center", va="bottom", fontsize=7.8, color=INK)
axA.set_xticks(x); axA.set_xticklabels([n for n, _ in items], fontsize=6.6)      # line 1
axA.tick_params(axis="x", length=0); axA.grid(axis="x", visible=False)
axA.set_xlim(-0.6, len(items) - 0.4); axA.set_ylim(0, 25)
axA.set_ylabel("training done before stability (%)")
axA.set_title("(a) Stability onset (Author, Year)")

# (b) broken y-axis: singles = light dots, merges = dark diamond + bracket over the merged span
singles = [(220, 23.9), (2200, 55.0), (2420, 54.8)]                                # <- data
merges = [((1980, 2200), 56.7, BLUES[2], "adjacent"), ((220, 2200), 25.3, RED, "far apart")]
for ax in (axT, axL):
    ax.scatter(*zip(*singles), s=36, color=BLUES[0], edgecolor=INK, linewidth=0.6, zorder=4, label="single checkpoint")
    for (ta, tb), v, c, lab in merges:
        ax.plot([ta, ta, tb, tb], [v - 0.5, v, v, v - 0.5], color=c, lw=1.0, zorder=3)
        ax.scatter([0.5 * (ta + tb)], [v], s=52, marker="D", color=c, edgecolor="white", linewidth=0.9,
                   zorder=5, label=f"merged, {lab}")
axT.set_ylim(53.0, 58.6); axL.set_ylim(22.0, 27.6); axT.set_xlim(0, 2600)
axT.set_yticks([54, 56, 58]); axL.set_yticks([22, 24, 26])
style.break_marks(axT, axL)
axL.set_xlabel("training tokens (B)")
axL.set_xticks([220, 1000, 2000, 2420])
fig.text(0.5 * (axT.get_position().x0 + axL.get_position().x0) - 0.055,
         0.5 * (axT.get_position().y0 + axL.get_position().y1),
         "accuracy (%)", rotation=90, ha="center", va="center", fontsize=9)     # shared y-label
axT.set_title("(b) Merging checkpoints (Author, Year)")
axT.legend(loc="upper left", fontsize=6.8)

# line 2 under (a): grouped dataset names on (b)'s x-label baseline
fig.canvas.draw()
b_bot = axL.xaxis.label.get_window_extent().y0
y_ax = axA.transAxes.inverted().transform((0, b_bot))[1]
tr = blended_transform_factory(axA.transData, axA.transAxes)
groups = [("data-1", 0.0), ("data-2", 1.5), ("data-3", 3.5)]
texts = [axA.text(gx, y_ax, g, transform=tr, ha="center", va="bottom", fontsize=9, color=INK) for g, gx in groups]
fig.canvas.draw()
STATS["text_bottom_gap_pt"] = round(float((min(t.get_window_extent().y0 for t in texts) - b_bot) * 72 / fig.dpi), 2)
style.save(fig, "t6_lollipop_broken", str(pathlib.Path(__file__).parent / "figs"))
for k_, v_ in STATS.items():
    print(k_, v_)
