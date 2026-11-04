"""T2 · Interpolation panels: curve vs. chord between endpoint
losses, blue fill = below (averaging gains), red fill = above (barrier), double arrow = B."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import style
from style import REDS, BLUES, INK, INK2, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATS = {}

a = np.linspace(0, 1, 81)
L_late = 1.30 - 0.10 * a - 0.22 * a * (1 - a)      # convex: dips below the chord
L_early = 1.60 - 0.25 * a + 1.10 * a * (1 - a)     # bump: barrier
panels = [(L_late, BLUES[1], "(a) Same run, late"), (L_early, REDS[1], "(b) Same run, early")]

fig, axes = plt.subplots(1, 2, figsize=(0.67 * FULL_W, 2.35), gridspec_kw=dict(wspace=0.36))
for ax, (L, col, title) in zip(axes, panels):
    ch = (1 - a) * L[0] + a * L[-1]
    style.shade_interp(ax, a, L, ch)
    ax.plot(a, ch, color=INK2, lw=1.0, ls=style.DASH)
    ax.plot(a, L, color=col)
    ax.plot([0, 1], [L[0], L[-1]], **style.dot(col, zorder=5))
    ax.set_title(title)
    ax.set_xlim(-0.03, 1.03); ax.set_xticks([0, 0.5, 1])
    ax.set_xlabel(r"interpolation coefficient $\alpha$")
    lo, hi = min(L.min(), ch.min()), max(L.max(), ch.max()); pad = 0.12 * (hi - lo)
    ax.set_ylim(lo - pad, hi + pad * 1.8)
axes[0].set_ylabel("loss (toy)")

mid = L_late[40] - 0.5 * (L_late[0] + L_late[-1]); STATS["late_mid_excess"] = float(mid)
axes[0].text(0.96, 0.93, r"$\Delta_{\rm mid}=%.2f$" % mid, transform=axes[0].transAxes,
             ha="right", va="top", fontsize=8.5)

ch = (1 - a) * L_early[0] + a * L_early[-1]
k = int(np.argmax(L_early - ch)); B = float((L_early - ch)[k]); STATS["early_barrier"] = B
axes[1].annotate("", xy=(a[k], L_early[k]), xytext=(a[k], ch[k]),
                 arrowprops=dict(arrowstyle="<->", color=INK, lw=0.8, shrinkA=0, shrinkB=0))
axes[1].text(a[k] + 0.05, ch[k] + 0.12 * B, r"$\mathcal{B}=%.2f$" % B, fontsize=8)

handles = [Line2D([], [], color=INK2, lw=1.0, ls=style.DASH, label="line between endpoint losses"),
           Patch(color=BLUES[0], alpha=0.6, label="below: averaging gains"),
           Patch(color=REDS[0], alpha=0.6, label="above: barrier")]
lo, hi = axes[1].get_ylim(); axes[1].set_ylim(lo, hi + 0.30)       # make room for the legend
axes[1].legend(handles=handles, loc="upper right", fontsize=6.3, borderaxespad=0.3)

style.align_xlabels(fig, axes)
STATS["row_misalignment_pt"] = style.check_row(fig, axes)
style.save(fig, "t2_interp", str(pathlib.Path(__file__).parent / "figs"))
for k_, v_ in STATS.items():
    print(k_, v_)
