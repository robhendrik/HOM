import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT_PNG = Path("HOM_figure4_distinguishability_dip_v3.png")

BLUE = "#1f77b4"
RED = "#d62728"
FS = 13

def gaussian_packet(x, center, width=0.32, amp=0.22):
    """Simple Gaussian wave-packet envelope."""
    return amp * np.exp(-0.5 * ((x - center) / width) ** 2)

def draw_packet_pair(ax, x_center, y_base, delay, width=0.28):
    """
    Draw two Gaussian wave-packet envelopes around x_center.

    delay < 0: red arrives earlier than blue
    delay = 0: maximum overlap
    delay > 0: red arrives later than blue
    """
    x = np.linspace(-1.0, 1.0, 250)

    blue = gaussian_packet(x, -delay / 2, width=width)
    red = gaussian_packet(x, +delay / 2, width=width)

    scale = 0.72

    ax.plot(x_center + scale * x, y_base + blue, color=BLUE, lw=2.5)
    ax.plot(x_center + scale * x, y_base - red, color=RED, lw=2.5)

    ax.plot(
        [x_center - 0.72, x_center + 0.72],
        [y_base, y_base],
        color="0.75",
        lw=1.0,
        zorder=0
    )

fig, ax = plt.subplots(figsize=(10.5, 6.3))

ax.set_xlim(-3.3, 3.3)
ax.set_ylim(0.0, 1.42)

tau = np.linspace(-3.2, 3.2, 600)
sigma = 0.72
p_split = 0.5 * (1 - np.exp(-(tau**2) / (2 * sigma**2)))

ax.plot(tau, p_split, color="black", lw=2.4)
ax.axhline(0.5, color="0.65", lw=1.0, ls="--")

packet_y = 1.08
draw_packet_pair(ax, -2.15, packet_y, delay=-1.1)
draw_packet_pair(ax,  0.00, packet_y, delay=0.0)
draw_packet_pair(ax,  2.15, packet_y, delay=+1.1)

ax.text(-2.15, 1.34, "Different arrival times",
        ha="center", va="center", fontsize=FS)
ax.text(0.00, 1.34, "Maximum overlap",
        ha="center", va="center", fontsize=FS)
ax.text(2.15, 1.34, "Different arrival times",
        ha="center", va="center", fontsize=FS)

ax.text(0.00, 0.84, "indistinguishable",
        ha="center", va="center", fontsize=FS, style="italic")

ax.set_xlabel("Relative arrival time", fontsize=FS+1, labelpad=10)
ax.set_ylabel("Probability of one photon\nin each output", fontsize=FS+1)

ax.set_xticks([-2, 0, 2])
ax.set_xticklabels(["−delay", "0", "+delay"], fontsize=FS)

ax.set_yticks([0, 0.5])
ax.set_yticklabels(["0", "1/2"], fontsize=FS)

ax.spines["bottom"].set_position(("data", 0))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.annotate(
    "photon states overlap",
    xy=(0, 0.0),
    xytext=(0.72, 0.17),
    fontsize=FS-1,
    arrowprops=dict(arrowstyle="->", lw=1.2)
)

fig.text(
    0.5, 0.025,
    "The dip measures indistinguishability: more overlap means fewer one-photon-per-output events.",
    ha="center",
    va="bottom",
    fontsize=14
)

plt.subplots_adjust(left=0.13, right=0.97, top=0.95, bottom=0.16)
fig.savefig(OUT_PNG, dpi=220, bbox_inches="tight", facecolor="white")
plt.show()
