"""T9 · Categorical dot plot on a log axis with two shaded regions.
Region = axvspan in legend_face (lighter) vs. the default face, split by an INK2 dashed line,
captions in INK2 at the top. Category labels: up to 3 short lines, never rotated."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
import style
from style import REDS, BLUES, INK, INK2, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
cats = [  # tick label, value, colour, value text          <- replace
    ("readout\nonly\n(Method-A)", 1e12, BLUES[2], "1T"),
    ("extrapolated\nreadout\n(Method-B)", 2e9, BLUES[1], "2B"),
    ("data order\n\n(Method-C)", 1.5e9, REDS[1], "1.5B"),
    ("no fixed\nhorizon\n(Method-D)", 3e8, REDS[1], "300M"),
    ("averaging in\nthe optimizer\n(Method-E)", 8e9, REDS[1], "8B"),
]
split = 1.5                                      # boundary between the two groups
fig, ax = plt.subplots(figsize=(FULL_W, 3.0))
x = np.arange(len(cats))
ax.axvspan(-0.5, split, color=style.THEME["legend_face"], lw=0, zorder=0)
ax.axvline(split, color=INK2, lw=1.0, ls=style.DASH_S)
for xx, (_, v, c, t) in zip(x, cats):
    ax.plot([xx], [v], **style.dot(c, ms=8, zorder=4))
    ax.text(xx, v * 1.6, t, ha="center", va="bottom", fontsize=9, color=INK)
ax.text(0.5 * (-0.5 + split), 2.4e13, "trajectory unchanged", ha="center", va="top", fontsize=9, color=INK2)
ax.text(0.5 * (split + len(cats) - 0.5), 2.4e13, "trajectory changed", ha="center", va="top", fontsize=9, color=INK2)
ax.set_yscale("log"); ax.set_ylim(1e8, 3e13)
ax.set_yticks([1e8, 1e9, 1e10, 1e11, 1e12]); ax.set_yticklabels(["100M", "1B", "10B", "100B", "1T"])
ax.set_xlim(-0.5, len(cats) - 0.5)
ax.set_xticks(x); ax.set_xticklabels([c[0] for c in cats], fontsize=8)
ax.tick_params(axis="x", length=0)
ax.set_ylabel("largest model in\npublic evidence")
ax.set_title("Only readout-only merging has evidence beyond 10B")
style.save(fig, "t9_category_log", str(pathlib.Path(__file__).parent / "figs"))
