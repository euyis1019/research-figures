"""T3 · Loss-landscape panels next to an ordinary axis.
Shows the alignment rules: equal-aspect landscapes + set_box_aspect(1) on the plot axis;
every panel has a bottom text line (landscapes say the window, not a placeholder)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
import style
from style import REDS, BLUES, INK2, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATS = {}
rng = np.random.default_rng(1)


def river(x, bend):              # valley floor z = g(x)
    return bend * np.sin(1.4 * x)


def loss(X, Z, bend):
    return 1.5 * np.exp(-X / 2.5) + 1.0 * (Z - river(X, bend)) ** 2


def landscape(ax, bend, x0, fam, title, window):
    xs = x0 + np.cumsum(np.full(16, 0.06)) + 0.01 * rng.standard_normal(16)
    zs = river(xs, bend) + 0.05 * rng.standard_normal(16)
    mx, mz = xs.mean(), zs.mean()
    cx, cz = 0.5 * (xs.min() + xs.max()), 0.5 * (zs.min() + zs.max())
    half = 0.5 * max(np.ptp(xs), np.ptp(zs)) + 0.15
    half *= 1.25; cz += 0.22 * half                # leave the top band free for the legend
    GX, GZ = np.meshgrid(np.linspace(cx - half, cx + half, 170), np.linspace(cz - half, cz + half, 170))
    GL = loss(GX, GZ, bend); LL = np.log(GL - GL.min() + 1e-3)
    style.no_grid(ax)
    ax.contourf(GX, GZ, LL, levels=14, cmap=style.tint_cmap())
    ax.contour(GX, GZ, LL, levels=14, colors="white", linewidths=0.5)
    rx = np.linspace(cx - half, cx + half, 200)
    ax.plot(rx, river(rx, bend), color="black", lw=0.9, ls=(0, (3, 2)), label="low-loss valley")
    ax.plot(xs, zs, color=fam[1], lw=0.5, alpha=0.6)                                   # trajectory
    ax.scatter(xs, zs, s=10, color=fam[0], edgecolor=fam[2], linewidth=0.5, zorder=3, label="checkpoints")
    ax.scatter([mx], [mz], s=55, marker="D", color=fam[2], edgecolor="white", linewidth=1.0, zorder=6,
               label="average")
    off = abs(mz - river(mx, bend))
    ax.plot([mx, mx], [mz, river(mx, bend)], color="black", lw=1.0, zorder=5)            # off-path gap
    ax.set_xlim(cx - half, cx + half); ax.set_ylim(cz - half, cz + half)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title)
    ax.set_xlabel(window)                                                              # informative
    ax.text(0.04, 0.05, "average is %.3f off the path" % off, transform=ax.transAxes,
            fontsize=7.5, bbox=style.infobox())
    ax.legend(loc="upper left", fontsize=6.8)                                            # empty corner
    return float(off)


fig = plt.figure(figsize=(FULL_W, 2.6))
gs = fig.add_gridspec(1, 3, wspace=0.42)
axA, axB, axC = (fig.add_subplot(gs[i]) for i in range(3))
STATS["early_offpath"] = landscape(axA, 0.9, 0.0, REDS, "(a) Early: the path bends", "window: steps 20$-$180")
STATS["late_offpath"] = landscape(axB, 0.05, 3.0, BLUES, "(b) Late: the path is straight", "window: steps 2000$-$3000")

ell = np.logspace(-1, 0.6, 10)
axC.plot(ell, 0.03 * ell ** 2 + 0.004, "-o", color=REDS[1], ms=3.2, mec="white", mew=0.5, lw=1.5, label="early window")
axC.plot(ell, 0.004 * ell + 0.003, "-o", color=BLUES[1], ms=3.2, mec="white", mew=0.5, lw=1.5, label="late window")
axC.set_xscale("log"); axC.set_yscale("log")
axC.set_xlabel(r"path length covered, $\ell$"); axC.set_ylabel("distance from the path")
axC.set_title("(c) Off-path error vs. window")
axC.legend(loc="upper left", fontsize=6.8)
axC.set_box_aspect(1)                       # same box shape as the equal-aspect landscapes
axC.yaxis.set_label_position("right"); axC.yaxis.tick_right()   # landscapes have no y-axis: put it outside

style.align_xlabels(fig, [axA, axB, axC])
STATS["row_misalignment_pt"] = style.check_row(fig, [axA, axB, axC])
style.save(fig, "t3_landscape_row", str(pathlib.Path(__file__).parent / "figs"))
for k_, v_ in STATS.items():
    print(k_, v_)
