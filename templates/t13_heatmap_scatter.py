"""T13 · Annotated heatmap next to a scatter with a fitted line, 1x2 row.
Heatmap: signed values use style.diverging_cmap() (REDS <- face -> BLUES, centred at 0 with
TwoSlopeNorm); unsigned values use style.tint_cmap(). no_grid(), white cell borders, numbers
in INK on light cells and white on dark ones, slim colorbar. Scatter: BLUES[1] dots with white
edge, fit = INK2 dashed, fit statistic in an infobox() at a free corner. The heatmap is drawn
with set_box_aspect(1) and so is the scatter (alignment rule 1)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import style
from style import BLUES, INK, INK2, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATS = {}
rng = np.random.default_rng(3)

fig, axes = plt.subplots(1, 2, figsize=(FULL_W, 3.0), gridspec_kw=dict(wspace=0.5))
# (a) signed matrix, e.g. score difference vs. a baseline for layer x setting
ax = axes[0]
M = np.round(rng.normal(0, 1.2, (5, 5)) + np.linspace(-1, 1.5, 5)[None, :], 1) + 0.0  # +0.0 clears -0.0
style.no_grid(ax)
lim = float(np.abs(M).max())
im = ax.imshow(M, cmap=style.diverging_cmap(), norm=TwoSlopeNorm(0, -lim, lim))
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        ax.text(j, i, "%+.1f" % M[i, j], ha="center", va="center", fontsize=7,
                color="white" if abs(M[i, j]) > 0.6 * lim else INK)
ax.set_xticks(range(5)); ax.set_xticklabels(["s%d" % k for k in range(1, 6)])
ax.set_yticks(range(5)); ax.set_yticklabels(["L%d" % k for k in range(1, 6)])
ax.tick_params(length=0)
for s in range(6):
    ax.axhline(s - 0.5, color="white", lw=1.2); ax.axvline(s - 0.5, color="white", lw=1.2)
ax.set_xlabel("setting")
ax.set_title("(a) Difference vs. baseline")
cax = ax.inset_axes([1.04, 0, 0.05, 1])          # inset colorbar: does not shrink the box (rule 1)
cb = fig.colorbar(im, cax=cax)
cb.outline.set_linewidth(0.6); cb.ax.tick_params(labelsize=7)

# (b) scatter + least-squares fit
ax = axes[1]
xv = rng.uniform(0, 1, 40); yv = 0.8 * xv + 0.1 + rng.normal(0, 0.08, 40)
k, b = np.polyfit(xv, yv, 1); r = np.corrcoef(xv, yv)[0, 1]
xx = np.linspace(0, 1, 2)
ax.plot(xx, k * xx + b, color=INK2, lw=1.0, ls=style.DASH, label="least-squares fit")
ax.plot(xv, yv, **style.dot(BLUES[1], ms=4.5, label="runs"))
ax.text(0.96, 0.05, "$r=%.2f$" % r, transform=ax.transAxes, ha="right", va="bottom",
        fontsize=7.5, bbox=style.infobox())
ax.set_box_aspect(1)
ax.set_xlim(-0.03, 1.03); ax.set_xlabel("proxy metric"); ax.set_ylabel("target metric")
ax.set_title("(b) Proxy vs. target")
ax.legend(loc="upper left", fontsize=6.8)
STATS["fit_slope"] = round(float(k), 3); STATS["pearson_r"] = round(float(r), 3)

style.align_xlabels(fig, axes)
STATS["row_misalignment_pt"] = style.check_row(fig, axes)
style.save(fig, "t13_heatmap_scatter", str(pathlib.Path(__file__).parent / "figs"))
plt.close(fig)
for k_, v_ in STATS.items():
    print(k_, v_)
