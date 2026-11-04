"""T4 · Slope chart with repelled labels. Single panel, size set by
content. Left = RED (before), right = BLUE (after), optional middle = white diamond.
Labels collide -> repel() + thin leader lines; never shrink the font to fix overlaps."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
import style
from style import RED, BLUE, INK, INK2

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")

rows = [  # name, before, middle (or None), after   <- replace with the paper's table
    ("model-A", 9.9, 8.2, 0.9), ("model-B", 5.9, None, 0.1), ("model-C", 6.3, 6.0, 0.2),
    ("model-D", 5.0, 5.7, 0.4), ("model-E", 4.6, 4.8, 0.2), ("model-F", 7.5, None, 0.6),
]
fig, ax = plt.subplots(figsize=(4.8, 3.4))
X0, X1, X2 = 0.0, 0.5, 1.0
for name, b, m, a in rows:
    ax.plot([X0, X2], [b, a], color=INK2, lw=1.0, alpha=0.55, zorder=2)
    if m is not None:
        ax.plot([X0, X1], [b, m], color=INK2, lw=0.7, ls=(0, (1.5, 2)), alpha=0.7, zorder=2)
        ax.scatter([X1], [m], s=28, marker="D", facecolor="white", edgecolor=INK, linewidth=0.8, zorder=4)
ax.scatter([X0] * len(rows), [r[1] for r in rows], s=36, color=RED, edgecolor="white", linewidth=0.8, zorder=5)
ax.scatter([X2] * len(rows), [r[3] for r in rows], s=36, color=BLUE, edgecolor="white", linewidth=0.8, zorder=5)
ax.axhline(0, color=INK, lw=0.9, ls=style.DASH, zorder=1)

gap = 0.42
ly = style.repel([r[1] for r in rows], gap); ry = style.repel([r[3] for r in rows], gap)
ry = ry + max(0.0, 0.3 - ry.min())                  # keep the right-hand fan inside the axes
for (name, b, m, a), yl, yr in zip(rows, ly, ry):
    ax.plot([X0 - 0.04, X0 - 0.09], [b, yl], color=INK2, lw=0.5, alpha=0.6)
    ax.text(X0 - 0.11, yl, f"{name}  {b:.2f}", ha="right", va="center", fontsize=7.5, color=INK)
    ax.plot([X2 + 0.04, X2 + 0.09], [a, yr], color=INK2, lw=0.5, alpha=0.6)
    ax.text(X2 + 0.11, yr, f"{a:.2f}", ha="left", va="center", fontsize=7.5, color=INK)

ax.set_xlim(-0.95, 1.35); ax.set_ylim(-0.35, 10.6)
ax.set_xticks([X0, X1, X2]); ax.set_xticklabels(["raw\ninterpolation", "weight\nmatching", "learned\nsymmetries"])
ax.tick_params(axis="x", length=0); ax.grid(axis="x", visible=False)
ax.set_ylabel(r"loss barrier $\mathcal{B}$")
ax.set_title("Independently trained LMs (Author, Year)")
fig.tight_layout()
style.save(fig, "t4_slope", str(pathlib.Path(__file__).parent / "figs"))
