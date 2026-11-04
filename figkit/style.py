"""research-figures house style (matplotlib). Core: apply, tint_cmap, align_xlabels,
no_grid, save, check_row, diverging_cmap. Helpers: bb, infobox, dot, repel, shade_interp,
label_values, break_marks."""
import os
import numpy as np
import matplotlib as mpl

REDS = ["#f5957f", "#d83611", "#711c09"]     # baseline / failure / before / early
BLUES = ["#91b4ee", "#3879e0", "#154084"]    # method / gain / after / late
ORANGE = "#ed9455"
GREEN = "#2e8b57"
RED, BLUE = REDS[1], BLUES[1]
INK = "#262626"
INK2 = "#5a5650"
GRAY = "#8c8780"

THEMES = {
    "warm": dict(face="#eee7dd", dark="#b3a58f", legend_face="#f4f0ea", legend_edge="#cccccc"),
    "cool": dict(face="#eaeaf2", dark="#a3a3b8", legend_face="#f4f4f8", legend_edge="#cccccc"),
}
THEME = THEMES["warm"]
FULL_W = 7.0
HALF_W = 3.4
# text widths in inches: (one column, full width). Blog default is FULL_W / HALF_W above.
VENUE_W = {
    "neurips": (5.5, 5.5), "iclr": (5.5, 5.5), "icml": (3.25, 6.75),
    "acl": (3.3, 6.8), "emnlp": (3.3, 6.8), "aaai": (3.3, 7.0), "cvpr": (3.25, 6.875),
}
DASH = (0, (4, 2.5))     # reference / chord line
DASH_S = (0, (3, 2))     # event markers, baselines
DOT = (0, (1, 1.5))      # secondary analytic term


def apply(theme="warm"):
    global THEME
    THEME = THEMES[theme]
    mpl.rcParams.update({
        "font.family": ["cmr10", "STIXGeneral"],
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": True,
        "font.size": 9, "axes.titlesize": 9.5, "axes.titleweight": "normal",
        "axes.titlepad": 5, "axes.labelsize": 9, "axes.labelpad": 3,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5,
        "text.color": INK, "axes.labelcolor": INK,
        "axes.facecolor": THEME["face"], "axes.edgecolor": "black", "axes.linewidth": 0.9,
        "axes.spines.top": True, "axes.spines.right": True, "axes.axisbelow": True,
        "axes.grid": True, "grid.color": "white", "grid.linewidth": 0.8, "grid.alpha": 1.0,
        "xtick.color": "black", "ytick.color": "black", "xtick.labelcolor": INK, "ytick.labelcolor": INK,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.size": 3.5, "ytick.major.size": 3.5, "xtick.major.width": 0.8, "ytick.major.width": 0.8,
        "xtick.minor.size": 2, "ytick.minor.size": 2, "xtick.minor.width": 0.6, "ytick.minor.width": 0.6,
        "lines.linewidth": 1.8, "lines.markersize": 4.5,
        "lines.solid_capstyle": "round", "lines.dash_capstyle": "round", "patch.edgecolor": "none",
        "legend.frameon": True, "legend.framealpha": 0.85, "legend.facecolor": THEME["legend_face"],
        "legend.edgecolor": THEME["legend_edge"], "legend.fancybox": True, "legend.borderpad": 0.45,
        "legend.labelspacing": 0.35, "legend.handlelength": 1.9, "legend.handletextpad": 0.6,
        "legend.borderaxespad": 0.6,
        "figure.dpi": 150, "figure.facecolor": "white",
        "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.04, "savefig.facecolor": "white",
        "pdf.fonttype": 42,
    })
    import warnings
    warnings.filterwarnings("ignore", message="cmr10 font should ideally be used with mathtext")


def tint_cmap():
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list("tint", [THEME["face"], THEME["dark"]])


def diverging_cmap():
    """Signed values: dark red <- negative, panel face at 0, positive -> dark blue.
    Pair with matplotlib.colors.TwoSlopeNorm(0, -lim, lim)."""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list(
        "diverge", [REDS[2], REDS[1], REDS[0], THEME["legend_face"], BLUES[0], BLUES[1], BLUES[2]])


def align_xlabels(fig, axes):
    fig.canvas.draw()
    bottoms = [ax.xaxis.label.get_window_extent().y0 for ax in axes]
    lowest = min(bottoms)
    for ax, y0 in zip(axes, bottoms):
        ax.xaxis.labelpad += (y0 - lowest) / fig.dpi * 72


def no_grid(ax):
    ax.grid(False)
    ax.set_facecolor("white")


def save(fig, name, outdir="figs"):
    os.makedirs(outdir, exist_ok=True)
    fig.savefig(os.path.join(outdir, f"{name}.png"))
    fig.savefig(os.path.join(outdir, f"{name}.pdf"))


def check_row(fig, axes, tol_pt=1.0):
    """Axes boxes share top/bottom and x-labels share one baseline. Returns worst
    mismatch in pt; warns above tol_pt. Call right before save()."""
    fig.canvas.draw()
    to_pt = 72.0 / fig.dpi
    boxes = [ax.get_window_extent() for ax in axes]
    tops = [b.y1 for b in boxes]; bots = [b.y0 for b in boxes]
    has_label = [bool(ax.get_xlabel()) for ax in axes]
    worst = max(max(tops) - min(tops), max(bots) - min(bots)) * to_pt
    if any(has_label) and not all(has_label):
        print("check_row: some panels have an x-label and some do not")
        worst = max(worst, 99.0)
    if all(has_label):
        lab = [ax.xaxis.label.get_window_extent().y0 for ax in axes]
        worst = max(worst, (max(lab) - min(lab)) * to_pt)
    if worst > tol_pt:
        print("check_row: row misaligned by %.1f pt" % worst)
    return round(float(worst), 2)


# ---------------------------------------------------------------- helpers ----
def bb():
    """Borderless tinted background for in-panel annotations."""
    return dict(boxstyle="round,pad=0.2", fc=THEME["legend_face"], ec="none", alpha=0.9)


def infobox():
    """Framed box for a one-line panel readout."""
    return dict(boxstyle="round,pad=0.25", fc=THEME["legend_face"], ec=THEME["legend_edge"], lw=0.5)


def dot(color, ms=4.5, **kw):
    """Marker kwargs for highlighted points: filled, white edge."""
    return dict(marker="o", ls="none", ms=ms, color=color, mec="white", mew=0.9, **kw)


def repel(vals, min_gap):
    """Push label positions apart so neighbours are >= min_gap apart (keeps order)."""
    order = np.argsort(vals); pos = np.array(vals, dtype=float)[order]
    for _ in range(50):
        moved = False
        for i in range(1, len(pos)):
            if pos[i] - pos[i - 1] < min_gap:
                mid = 0.5 * (pos[i] + pos[i - 1])
                pos[i - 1], pos[i] = mid - min_gap / 2, mid + min_gap / 2
                moved = True
        if not moved:
            break
    out = np.empty_like(pos); out[order] = pos
    return out


def shade_interp(ax, a, L, chord, alpha=0.45):
    """Blue where the curve is below the chord (gain), red above (barrier / loss)."""
    ax.fill_between(a, L, chord, where=L <= chord, color=BLUES[0], alpha=alpha, lw=0, interpolate=True)
    ax.fill_between(a, L, chord, where=L > chord, color=REDS[0], alpha=alpha, lw=0, interpolate=True)


def label_values(ax, xs, ys, fmt="{:.2f}", dy=0.0, fontsize=7, color=INK2, **kw):
    """Value labels above points/bars; dy scalar or per-point, negative = below."""
    dys = np.broadcast_to(np.asarray(dy, float), np.shape(ys))
    for x, y, d in zip(xs, ys, dys):
        ax.text(x, y + d, fmt.format(y), ha="center", va="bottom" if d >= 0 else "top",
                fontsize=fontsize, color=color, **kw)


def break_marks(ax_top, ax_bot, size=7):
    """Diagonal cut marks for a broken y-axis (top panel above bottom panel)."""
    kw = dict(marker=[(-1, -0.5), (1, 0.5)], markersize=size, linestyle="none",
              color="black", mec="black", mew=0.9, clip_on=False)
    ax_top.spines["bottom"].set_visible(False); ax_bot.spines["top"].set_visible(False)
    ax_top.tick_params(axis="x", labelbottom=False, length=0)
    ax_top.plot([0, 1], [0, 0], transform=ax_top.transAxes, **kw)
    ax_bot.plot([0, 1], [1, 1], transform=ax_bot.transAxes, **kw)