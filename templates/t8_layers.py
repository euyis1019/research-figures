"""T8 · Status / layer diagram.
One framed axis, no grid, no ticks; each row = a coloured bar with white text, evidence in
INK2 to its right; colour = status (GRAY / RED / BLUE / tan); footer text = reading direction."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import style
from style import RED, BLUE, GRAY, INK, INK2, FULL_W

style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATUS = {"holds": (GRAY, 0.9, "white", "holds by construction"),
          "worse": (RED, 0.9, "white", "decay still ahead"),
          "better": (BLUE, 0.9, "white", "merge on par or better"),
          "open": (style.THEME["dark"], 0.55, INK, "little evidence yet")}
rows = [  # label, status, evidence          <- replace
    ("weight identity, fixed updates", "holds", "Paper-A"),
    ("same trajectory, local quadratic", "holds", "Paper-B"),
    ("validation loss", "worse", "Paper-C, Paper-D"),
    ("benchmarks", "better", "Paper-E, Paper-F, Paper-G"),
    ("after SFT / continued training", "open", "Paper-H"),
    ("deployment (quantization)", "open", "Paper-I, Paper-J"),
]
fig, ax = plt.subplots(figsize=(FULL_W, 3.0))
style.no_grid(ax); ax.set_facecolor(style.THEME["face"])
BAR_W, H = 0.375, 0.66
for i, (lab, st, ev) in enumerate(rows):
    col, a, tc, _ = STATUS[st]; y = len(rows) - 1 - i
    ax.barh(y, BAR_W, height=H, left=0, color=col, alpha=a)
    ax.text(0.008, y, f"{i + 1}  {lab}", va="center", ha="left", fontsize=9, color=tc)
    ax.text(BAR_W + 0.012, y, ev, va="center", ha="left", fontsize=9, color=INK2)
ax.set_xlim(0, 1); ax.set_ylim(-0.6, len(rows) - 0.4)
ax.set_xticks([]); ax.set_yticks([])
ax.legend(handles=[Patch(color=c, alpha=a, label=l) for c, a, _, l in STATUS.values()],
          loc="upper right", fontsize=8)
ax.set_title(r"Six layers of ``merge $\approx$ decay''")
ax.set_xlabel(r"closer to what users care about  $\longrightarrow$  less evidence")
style.save(fig, "t8_layers", str(pathlib.Path(__file__).parent / "figs"))
