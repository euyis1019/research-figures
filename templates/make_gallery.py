"""Run every template (t1-t11) and stitch their PNGs into figs/gallery.png.
Run: python3 make_gallery.py [warm|cool]"""
import sys, pathlib, subprocess
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

HERE = pathlib.Path(__file__).resolve().parent
theme = sys.argv[1] if len(sys.argv) > 1 else "warm"
scripts = sorted(HERE.glob("t[0-9]*_*.py"), key=lambda p: int(p.name[1:].split("_")[0]))
scripts = [s for s in scripts if not s.name.startswith("t0_")]
for s in scripts:
    r = subprocess.run([sys.executable, str(s), theme], capture_output=True, text=True)
    print("%-28s %s" % (s.name, "ok" if r.returncode == 0 else "FAILED\n" + r.stderr[-800:]))
    if r.stdout.strip():
        print("    " + r.stdout.strip().replace("\n", "\n    "))

pngs = [HERE / "figs" / (s.stem + ".png") for s in scripts]
pngs = [p for p in pngs if p.exists()]
cols = 2
rows = (len(pngs) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(14, 3.3 * rows))
for ax in axes.flat:
    ax.axis("off")
for ax, p in zip(axes.flat, pngs):
    ax.imshow(mpimg.imread(p))
    ax.set_title(p.stem, fontsize=10, loc="left")
fig.tight_layout()
fig.savefig(HERE / "figs" / "gallery.png", dpi=110)
print("wrote", HERE / "figs" / "gallery.png")
