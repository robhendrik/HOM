from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

OUT_PNG = Path("HOM_figure1_beamsplitter_phase_v2.png")

BLUE = "#1f77b4"
RED = "#d62728"
BS_EDGE = "black"
LW_BEAM = 3.2
LW_BS = 1.8
FS = 14

def draw_beamsplitter(ax, x0=0, y0=0, size=1.25):
    ax.add_patch(
        Rectangle(
            (x0 - size/2, y0 - size/2),
            size, size,
            fill=False,
            edgecolor=BS_EDGE,
            linewidth=LW_BS,
            zorder=3
        )
    )
    ax.plot(
        [x0 - size/2, x0 + size/2],
        [y0 - size/2, y0 + size/2],
        color=BS_EDGE,
        linewidth=LW_BS,
        zorder=4
    )

def beam_line(ax, x1, y1, x2, y2, color):
    ax.plot([x1, x2], [y1, y2], color=color, lw=LW_BEAM,
            solid_capstyle="round", zorder=2)

def output_arrow(ax, x1, y1, x2, y2, color):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=LW_BEAM,
            color=color,
            shrinkA=0,
            shrinkB=0,
            zorder=2
        )
    )

def panel_blue(ax):
    s = 1.25

    # Input/transmitted beam continues through the square
    beam_line(ax, -2.2, 0, 1.85, 0, BLUE)
    output_arrow(ax, 1.85, 0, 2.2, 0, BLUE)

    # Reflected output
    beam_line(ax, 0, 0, 0, 1.75, BLUE)
    output_arrow(ax, 0, 1.75, 0, 2.1, BLUE)

    draw_beamsplitter(ax, 0, 0, s)

    ax.text(-2.25, 0.18, "1", fontsize=FS, ha="left", va="bottom", color=BLUE)
    ax.text(1.20, 0.18, "1/√2", fontsize=FS, ha="center", va="bottom", color=BLUE)
    ax.text(0.18, 1.45, "1/√2", fontsize=FS, ha="left", va="center", color=BLUE)

def panel_red(ax):
    s = 1.25

    # Input/transmitted beam continues through the square
    beam_line(ax, 0, -2.1, 0, 1.75, RED)
    output_arrow(ax, 0, 1.75, 0, 2.1, RED)

    # Reflected output, carrying the minus sign
    beam_line(ax, 0, 0, 1.85, 0, RED)
    output_arrow(ax, 1.85, 0, 2.2, 0, RED)

    draw_beamsplitter(ax, 0, 0, s)

    ax.text(0.18, -1.55, "1", fontsize=FS, ha="left", va="center", color=RED)
    ax.text(0.18, 1.45, "1/√2", fontsize=FS, ha="left", va="center", color=RED)
    ax.text(1.25, 0.18, "−1/√2", fontsize=FS, ha="center", va="bottom", color=RED)

def style_ax(ax):
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.35, 2.35)
    ax.set_aspect("equal")
    ax.axis("off")

fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))

panel_blue(axes[0])
panel_red(axes[1])

for ax in axes:
    style_ax(ax)

plt.subplots_adjust(left=0.03, right=0.97, top=0.97, bottom=0.03, wspace=0.20)
fig.savefig(OUT_PNG, dpi=220, bbox_inches="tight", facecolor="white")
plt.show()
