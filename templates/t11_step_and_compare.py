"""T11 · Step-function schematic next to a log-log method comparison, 1x2 row.
(a) ax.step(where="post") in a light-to-dark family = small-to-large K; the continuous
counterpart is a RED dashed line. (b) "-o" series with white-edged small markers; the
reference law is an INK2 dotted line; y axis moved right because its meaning differs from (a).
Both panels have x-labels, aligned with align_xlabels + check_row (must print 0)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
import style
from style import REDS, BLUES, INK2, GRAY, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATS = {}

fig, axes = plt.subplots(1, 2, figsize=(FULL_W, 2.5), gridspec_kw=dict(wspace=0.32))
# (a) equivalent LR of a uniform average of K checkpoints
ax = axes[0]
u = np.linspace(0, 0.9999, 801)
for K, col in [(2, BLUES[0]), (4, BLUES[1]), (8, BLUES[2])]:
    tk = np.linspace(0, 1, K)
    ax.step(u, [np.sum(tk > x) / K for x in u], where="post", color=col, lw=1.5, label="average, $K=%d$" % K)
ax.plot(u, 1 - u, color=REDS[1], lw=1.4, ls=style.DASH, label="linear decay to 0")
ax.set_xlim(0, 1); ax.set_ylim(-0.03, 1.08)
ax.set_xlabel("position in the window"); ax.set_ylabel(r"equivalent LR $/\,\eta$")
ax.set_title("(a) Equivalent schedule")
ax.legend(loc="upper right", fontsize=6.6)

# (b) synthetic residuals: ~1/K, a lagging variant, and ~1/sqrt(K)
ax = axes[1]
Ks = np.array([1, 2, 3, 4, 6, 8, 12, 16])
rng = np.random.default_rng(1)
avg = 1 / Ks * np.exp(0.03 * rng.standard_normal(len(Ks)))
stair = np.minimum(1, 1.15 / Ks ** 0.8)
lin = np.minimum(1, 0.42 / np.sqrt(Ks - 0.999) + 0.0)
lin[0] = 1
ax.plot(Ks, 1 / Ks, color=INK2, lw=1.0, ls=style.DOT, label="$1/K$")
ax.plot(Ks, avg, "-o", color=BLUES[1], ms=3.6, mec="white", mew=0.6, lw=1.5, label="average $K$ checkpoints")
ax.plot(Ks, stair, "-o", color=GRAY, ms=3.6, mec="white", mew=0.6, lw=1.3, label="run the staircase")
ax.plot(Ks, lin, "-o", color=REDS[1], ms=3.6, mec="white", mew=0.6, lw=1.3, label="linear decay to 0")
ax.set_xscale("log", base=2); ax.set_xticks(Ks); ax.set_xticklabels([str(k) for k in Ks]); ax.minorticks_off()
ax.set_yscale("log"); ax.set_ylim(0.04, 1.35)
ax.set_xlabel("number of checkpoints $K$")
ax.set_ylabel(r"residual $/\,G$")
ax.yaxis.set_label_position("right"); ax.yaxis.tick_right()
ax.set_title("(b) What is left")
ax.legend(loc="lower left", fontsize=6.4)
STATS["K=16 avg/stair/linear"] = tuple(round(float(v[-1]), 3) for v in (avg, stair, lin))

style.align_xlabels(fig, axes)
STATS["row_misalignment_pt"] = style.check_row(fig, axes)
style.save(fig, "t11_step_and_compare", str(pathlib.Path(__file__).parent / "figs"))
plt.close(fig)
for k_, v_ in STATS.items():
    print(k_, v_)
