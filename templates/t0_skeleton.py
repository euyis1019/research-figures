"""T0 · make_figs.py skeleton. Copy to <project>/<chapter>/make_figs.py; run `python3 make_figs.py [warm|cool]`.
One function per figure; every function records the numbers it draws into STATS."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import numpy as np
import matplotlib.pyplot as plt
import style
from style import REDS, BLUES, RED, BLUE, INK, INK2, GRAY, FULL_W, HALF_W
# import toy                      # optional: shared simulation code, one module for all figures

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
OUT = "figs"
STATS = {}


def fig_example():
    fig, axes = plt.subplots(1, 2, figsize=(FULL_W, 2.4), gridspec_kw=dict(wspace=0.38))
    x = np.linspace(0, 1, 50)
    for ax, fam, title in zip(axes, (REDS, BLUES), ("(a) Early", "(b) Late")):
        ax.plot(x, x ** 2, color=fam[1], label="series")
        ax.set_xlabel("step"); ax.set_title(title)
    axes[0].set_ylabel("loss (toy)")
    axes[0].legend(loc="upper left")
    STATS["example_max"] = float((x ** 2).max())            # every drawn number -> STATS
    style.align_xlabels(fig, axes)
    STATS["example_row_misalignment_pt"] = style.check_row(fig, axes)   # must be 0
    style.save(fig, "fig0_example", OUT)
    plt.close(fig)


if __name__ == "__main__":
    fig_example()
    for k_, v_ in STATS.items():
        print(k_, v_)
