"""T1 · 1x3 row of line plots.
(a) noisy iterate + running mean + event line; (b) curves with marked optimum + analytic
terms dashed/dotted; (c) log-log comparison with a reference line."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
import style
from style import REDS, BLUES, INK, INK2, GRAY, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATS = {}
rng = np.random.default_rng(0)

fig, axes = plt.subplots(1, 3, figsize=(FULL_W, 2.4), gridspec_kw=dict(wspace=0.42))

# (a) iterate (light) + mean (dark) from the same family-pair; event = INK2 short dash + bb() label
ax = axes[0]
T, T0, K = 2600, 1600, 200
y = np.zeros(T + 1)
for t in range(T):
    lr = 1.0 if t < T0 else max(0.0, 1 - (t - T0) / (T - T0))
    y[t + 1] = (1 - 0.05 * lr) * y[t] + 0.2 * np.sqrt(lr) * rng.standard_normal()
ybar = np.convolve(y, np.ones(K) / K, mode="valid")
t = np.arange(T + 1)
sd = 0.2 / np.sqrt(1 - 0.95 ** 2)                       # stationary sd -> white band
ax.axhspan(-sd, sd, color="white", alpha=0.55, lw=0)
ax.plot(t, y, color=REDS[0], lw=0.7, label="iterate $y_2$")
ax.plot(t[K - 1:], ybar, color=BLUES[2], lw=1.4, label="mean of last %d steps" % K)
ax.axvline(T0, color=INK2, lw=0.8, ls=style.DASH_S)
ax.text(T0 + 50, 2.3, "LR decay\nstarts", ha="left", va="top", fontsize=7, color=INK2, bbox=style.bb())
ax.set_xlim(0, T); ax.set_ylim(-3.2, 2.6)
ax.set_xlabel("step"); ax.set_ylabel("flat hill coordinate $y_2$")
ax.set_title("(a) Stochastic (SGD noise)")
ax.legend(loc="lower left", fontsize=6.6, framealpha=0.92)
STATS["a_sd_iterate"] = float(y[400:T0].std()); STATS["a_sd_mean"] = float(ybar[400:T0 - K].std())

# (b) total = gain + lag; optimum = white-edged dot; components in INK2 dash / dot.
# Curves fill the panel -> direct labels in the family's dark shade + bb(), no legend.
ax = axes[1]
W = np.linspace(1, 4000, 800); tau = 20
for r, col in [(1 / 4000, BLUES[1]), (1 / 800, REDS[1])]:
    tot = -(1 - 1 / np.maximum(1, W / (2 * tau))) + r * W / 2
    ax.plot(W, tot, color=col)
    i = int(np.argmin(tot)); ax.plot(W[i], tot[i], **style.dot(col, ms=5.5))
    STATS["b_optW_r=%g" % r] = float(W[i])
ax.plot(W, -(1 - 1 / np.maximum(1, W / (2 * tau))), color=INK2, lw=0.9, ls=style.DASH_S)
ax.plot(W, W / 1600, color=INK2, lw=0.9, ls=style.DOT)
ax.axhline(0, color=INK, lw=0.7)
lab = dict(fontsize=7, bbox=style.bb())
ax.text(2300, 0.30, "fast drift (mid)", color=REDS[2], ha="left", va="top", **lab)
ax.text(1200, -0.62, "slow drift (late)", color=BLUES[2], ha="left", va="bottom", **lab)
ax.text(3950, -0.95, r"$-\mathbb{E}\mathcal{D}$", color=INK2, ha="right", va="bottom", **lab)
ax.text(1100, 0.85, r"$\mathbb{E}\mathcal{A}$ (fast)", color=INK2, ha="right", va="top", **lab)
ax.set_xlim(0, 4000); ax.set_ylim(-1.05, 0.9)
ax.set_xlabel("window $W$ (steps)"); ax.set_ylabel(r"$L(\bar\theta)-L(\theta_K)$")
ax.set_title("(b) Gain minus lag")

# (c) log-log, line+marker series, theory in INK2 dashed
ax = axes[2]
ell = np.logspace(-1, 1, 12)
early = 0.02 * ell ** 2 + 0.01; late = 0.002 * ell + 0.006
ax.plot(ell, 0.02 * ell ** 2, color=INK2, lw=1.0, ls=style.DASH_S, label=r"$\kappa\ell^2/24$")
ax.plot(ell, early, "-o", color=REDS[1], ms=3.2, mec="white", mew=0.5, lw=1.5, label="early window")
ax.plot(ell, late, "-o", color=BLUES[1], ms=3.2, mec="white", mew=0.5, lw=1.5, label="late window")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_ylim(4e-3, 3)
ax.set_xlabel(r"path length covered, $\ell$"); ax.set_ylabel("distance from the path")
ax.set_title("(c) Off-path error")
ax.legend(loc="upper left", fontsize=6.6)

style.align_xlabels(fig, axes)
STATS["row_misalignment_pt"] = style.check_row(fig, axes)
style.save(fig, "t1_curve_row", str(pathlib.Path(__file__).parent / "figs"))
for k, v in STATS.items():
    print(k, v)
