"""T10 · Closed-form curve vs. simulation, single panel.
Theory = INK2 dashed line; simulation = BLUES[1] dots with white edge and thin error bars
(no caps); limiting values = DASH_S reference lines, labelled in the family's dark shade
with bb(). A point that cannot sit on a log axis (x = 0) is drawn at the left edge and says so.
Records the worst theory-vs-simulation gap in STATS."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
import style
from style import REDS, BLUES, INK, INK2

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATS = {}

# synthetic: cos between successive differences of (drift + white noise), theory (q-1)/(q+2)
rng = np.random.default_rng(0)
D, n = 2000, 24
ratios = np.array([0, 0.1, 0.3, 1, 2, 3, 10, 30, 100])
sim = []
for q in ratios:
    d = np.zeros(D); d[0] = np.sqrt(q * D)
    pts = np.cumsum(np.tile(d, (n, 1)), axis=0) + rng.standard_normal((n, D))
    dl = np.diff(pts, axis=0)
    c = [dl[i] @ dl[i + 1] / np.linalg.norm(dl[i]) / np.linalg.norm(dl[i + 1]) for i in range(len(dl) - 1)]
    sim.append((np.mean(c), np.std(c)))
sim = np.array(sim)
qq = np.logspace(-2, 2.2, 300)

fig, ax = plt.subplots(figsize=(4.8, 3.2))
ax.axhline(1, color=INK2, lw=0.8, ls=style.DASH_S); ax.axhline(-0.5, color=INK2, lw=0.8, ls=style.DASH_S)
ax.axhline(0, color=INK, lw=0.6)
ax.plot(qq, (qq - 1) / (qq + 2), color=INK2, lw=1.0, ls=style.DASH, label=r"theory: $(q-1)/(q+2)$")
x = np.where(ratios == 0, 0.01, ratios)
ax.errorbar(x, sim[:, 0], yerr=sim[:, 1], fmt="o", color=BLUES[1], ms=4.5, mec="white", mew=0.8,
            elinewidth=0.8, capsize=0, label="simulation (2000-dim)")
ax.text(0.3, -0.54, "pure noise: $-1/2$", fontsize=7, color=REDS[2], ha="left", va="top", bbox=style.bb())
ax.text(0.012, 0.97, "pure drift: $1$", fontsize=7, color=BLUES[2], ha="left", va="top", bbox=style.bb())
ax.text(0.012, 0.02, "no drift: plotted at $q=0.01$", fontsize=6.4, color=INK2, ha="left", va="bottom")
ax.set_xscale("log"); ax.set_xlim(0.008, 160); ax.set_ylim(-0.7, 1.1)
ax.set_xlabel(r"drift-to-noise ratio $q$")
ax.set_ylabel(r"$\cos(\Delta_i,\Delta_{i+1})$")
ax.legend(loc="lower right", fontsize=6.8)
STATS["max_abs_err"] = round(float(np.max(np.abs(sim[:, 0] - (ratios - 1) / (ratios + 2)))), 3)
style.save(fig, "t10_theory_vs_sim", str(pathlib.Path(__file__).parent / "figs"))
plt.close(fig)
for k_, v_ in STATS.items():
    print(k_, v_)
