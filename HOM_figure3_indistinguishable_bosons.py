import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from pathlib import Path

OUT_PNG = Path("HOM_figure3_indistinguishable_bosons.png")

BLUE = "#1f77b4"
RED = "#d62728"
EDGE = "black"
FS = 14

def photon(ax, x, y, color=None, radius=0.18, label=None):
    face = "white" if color is None else color
    edge = EDGE if color is None else color
    ax.add_patch(Circle((x, y), radius, facecolor=face, edgecolor=edge, lw=2))
    if label:
        ax.text(x, y - 0.34, label, ha="center", va="top", fontsize=FS-1)

def mode_box(ax, x, y, width=1.4, height=0.72):
    ax.add_patch(Rectangle((x-width/2, y-height/2), width, height,
                           fill=False, edgecolor=EDGE, lw=1.8))

def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                 arrowstyle="-|>",
                                 mutation_scale=18,
                                 linewidth=1.8,
                                 color="black"))

fig, ax = plt.subplots(figsize=(11, 5.2))
ax.set_xlim(0, 11)
ax.set_ylim(0, 5.2)
ax.axis("off")

ax.text(2.0, 4.55, "Assignment 1", ha="center", va="center", fontsize=FS+1)
ax.text(4.7, 4.55, "Assignment 2", ha="center", va="center", fontsize=FS+1)

mode_box(ax, 2.0, 3.2)
mode_box(ax, 4.7, 3.2)

photon(ax, 1.78, 3.2, BLUE)
photon(ax, 2.22, 3.2, RED)
ax.text(2.0, 2.55, "blue, red", ha="center", fontsize=FS)

photon(ax, 4.48, 3.2, RED)
photon(ax, 4.92, 3.2, BLUE)
ax.text(4.7, 2.55, "red, blue", ha="center", fontsize=FS)

ax.text(3.35, 3.2, "+", ha="center", va="center", fontsize=26)

arrow(ax, 5.75, 3.2, 7.05, 3.2)
ax.text(6.4, 3.55, "remove temporary labels", ha="center", fontsize=FS-1)

ax.text(8.6, 4.55, "Same physical state", ha="center", va="center", fontsize=FS+1)
mode_box(ax, 8.6, 3.2)

photon(ax, 8.38, 3.2, None)
photon(ax, 8.82, 3.2, None)
ax.text(8.6, 2.55, "two identical photons", ha="center", fontsize=FS)

ax.text(5.5, 1.35,
        "Same state, same sign  →  contributions reinforce",
        ha="center", va="center", fontsize=FS+1)

ax.text(5.5, 0.72,
        "a† a† |0⟩ = √2 |2⟩",
        ha="center", va="center", fontsize=18)

plt.tight_layout()
fig.savefig(OUT_PNG, dpi=220, bbox_inches="tight", facecolor="white")
plt.show()
