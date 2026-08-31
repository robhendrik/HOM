import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from pathlib import Path

OUT_PNG = Path("HOM_figure2_two_histories_v2.png")

BLUE = "#1f77b4"
RED = "#d62728"
BS_EDGE = "black"
LW_BEAM = 3.0
LW_BS = 1.8
FS = 13

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
    # Same / orientation as Figure 1
    ax.plot(
        [x0 - size/2, x0 + size/2],
        [y0 - size/2, y0 + size/2],
        color=BS_EDGE,
        linewidth=LW_BS,
        zorder=4
    )

def line(ax, x1, y1, x2, y2, color, lw=LW_BEAM):
    ax.plot(
        [x1, x2], [y1, y2],
        color=color,
        lw=lw,
        solid_capstyle="round",
        zorder=2
    )

def arrow(ax, x1, y1, x2, y2, color):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>",
            mutation_scale=17,
            linewidth=LW_BEAM,
            color=color,
            shrinkA=0,
            shrinkB=0,
            zorder=2
        )
    )

def draw_inputs(ax):
    # Blue photon from left
    line(ax, -2.2, 0, -0.15, 0, BLUE)

    # Red photon from below
    line(ax, 0, -2.0, 0, -0.15, RED)

def history_transmitted(ax):
    draw_inputs(ax)

    # Both transmitted
    line(ax, -0.15, 0, 1.75, 0, BLUE)
    arrow(ax, 1.75, 0, 2.15, 0, BLUE)

    line(ax, 0, -0.15, 0, 1.65, RED)
    arrow(ax, 0, 1.65, 0, 2.05, RED)

    draw_beamsplitter(ax)

    ax.text(
        0, 2.43,
        "Both transmitted",
        ha="center", va="bottom",
        fontsize=FS+1
    )
    ax.text(
        0, 2.10,
        "Amplitude  1/√2 × 1/√2 = 1/2",
        ha="center", va="bottom",
        fontsize=FS
    )

def history_reflected(ax):
    draw_inputs(ax)

    # Both reflected
    line(ax, -0.15, 0, 0, 0, BLUE)
    line(ax, 0, 0, 0, 1.65, BLUE)
    arrow(ax, 0, 1.65, 0, 2.05, BLUE)

    line(ax, 0, -0.15, 0, 0, RED)
    line(ax, 0, 0, 1.75, 0, RED)
    arrow(ax, 1.75, 0, 2.15, 0, RED)

    draw_beamsplitter(ax)

    ax.text(
        0, 2.43,
        "Both reflected",
        ha="center", va="bottom",
        fontsize=FS+1
    )
    ax.text(
        0, 2.10,
        "Amplitude  1/√2 × (−1/√2) = −1/2",
        ha="center", va="bottom",
        fontsize=FS
    )

def style_ax(ax):
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.25, 2.75)
    ax.set_aspect("equal")
    ax.axis("off")

fig, axes = plt.subplots(1, 2, figsize=(10.5, 5.0))

history_transmitted(axes[0])
history_reflected(axes[1])

for ax in axes:
    style_ax(ax)

fig.text(
    0.5, 0.045,
    "Equal outcomes, opposite amplitude, the contributions cancel",
    ha="center",
    va="bottom",
    fontsize=15
)

plt.subplots_adjust(
    left=0.035,
    right=0.965,
    top=0.92,
    bottom=0.13,
    wspace=0.22
)

fig.savefig(
    OUT_PNG,
    dpi=220,
    bbox_inches="tight",
    facecolor="white"
)
plt.show()
