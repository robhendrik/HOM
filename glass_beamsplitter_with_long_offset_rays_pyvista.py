"""
Glass cube beamsplitter with red and blue beams visible in BOTH output ports.

The two colours are offset slightly in z so they do not visually overlap.
This keeps the optical paths essentially identical while making both
reflection/transmission possibilities readable.

Requires:
    pip install pyvista vtk
"""

from pathlib import Path
import numpy as np
import pyvista as pv

# ---------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------
SIDE = 2.0

GLASS_COLOR = "#d9eef7"
COATING_COLOR = "#aab9c2"
EDGE_COLOR = "#606870"
BACKGROUND = "white"

GLASS_OPACITY = 0.13
COATING_OPACITY = 0.34

RAY_RADIUS = 0.022
RAY_OFFSET = 0.055      # vertical separation red/blue
RED = "#d62728"
BLUE = "#1f77b4"

OUT_PNG = Path("glass_beamsplitter_with_long_offset_rays.png")

h = SIDE / 2.0

# ---------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------
def triangular_prism(points_xy, z0, z1):
    pts = [
        (points_xy[0][0], points_xy[0][1], z0),
        (points_xy[1][0], points_xy[1][1], z0),
        (points_xy[2][0], points_xy[2][1], z0),
        (points_xy[0][0], points_xy[0][1], z1),
        (points_xy[1][0], points_xy[1][1], z1),
        (points_xy[2][0], points_xy[2][1], z1),
    ]
    faces = [
        3, 0, 2, 1,
        3, 3, 4, 5,
        4, 0, 1, 4, 3,
        4, 1, 2, 5, 4,
        4, 2, 0, 3, 5,
    ]
    return pv.PolyData(pts, faces)


def add_ray(plotter, p0, p1, color, radius=RAY_RADIUS):
    p0 = np.asarray(p0, dtype=float)
    p1 = np.asarray(p1, dtype=float)
    vec = p1 - p0
    length = np.linalg.norm(vec)

    tube = pv.Cylinder(
        center=0.5 * (p0 + p1),
        direction=vec,
        radius=radius,
        height=length,
        resolution=32,
    )
    plotter.add_mesh(
        tube,
        color=color,
        smooth_shading=True,
    )


tri_a = [(-h, -h), (+h, -h), (+h, +h)]
tri_b = [(-h, -h), (+h, +h), (-h, +h)]

prism_a = triangular_prism(tri_a, -h, +h)
prism_b = triangular_prism(tri_b, -h, +h)

plane_pts = [
    (-h, -h, -h),
    (+h, +h, -h),
    (+h, +h, +h),
    (-h, -h, +h),
]
split_plane = pv.PolyData(plane_pts, [4, 0, 1, 2, 3])

# ---------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------
plotter = pv.Plotter(off_screen=True, window_size=(1200, 900))
plotter.set_background(BACKGROUND)

for prism in (prism_a, prism_b):
    plotter.add_mesh(
        prism,
        color=GLASS_COLOR,
        opacity=GLASS_OPACITY,
        show_edges=True,
        edge_color=EDGE_COLOR,
        line_width=1.0,
        lighting=True,
    )

plotter.add_mesh(
    split_plane,
    color=COATING_COLOR,
    opacity=COATING_OPACITY,
    show_edges=True,
    edge_color="#50575d",
    line_width=1.3,
    lighting=True,
)

cube_edges = pv.Cube(
    center=(0, 0, 0),
    x_length=SIDE,
    y_length=SIDE,
    z_length=SIDE,
).extract_feature_edges(
    boundary_edges=True,
    feature_edges=True,
    manifold_edges=False,
)

plotter.add_mesh(
    cube_edges,
    color="#4f565c",
    line_width=1.0,
    opacity=0.65,
)

# ---------------------------------------------------------------------
# Rays
# ---------------------------------------------------------------------
# Inputs meet the coating at almost the same location.
# We separate red and blue slightly in z only for readability.

zr = +RAY_OFFSET / 2
zb = -RAY_OFFSET / 2

red_hit = np.array([0.0, 0.0, zr])
blue_hit = np.array([0.0, 0.0, zb])

# Red input from -x.
add_ray(plotter, (-3.00, 0.0, zr), red_hit, RED)

# Blue input from -y.
add_ray(plotter, (0.0, -3.00, zb), blue_hit, BLUE)

# +x output port: transmitted red + reflected blue
add_ray(plotter, red_hit, (+3.00, 0.0, zr), RED)
add_ray(plotter, blue_hit, (+3.00, 0.0, zb), BLUE)

# +y output port: reflected red + transmitted blue
add_ray(plotter, red_hit, (0.0, +3.00, zr), RED)
add_ray(plotter, blue_hit, (0.0, +3.00, zb), BLUE)

plotter.camera_position = [
    (4.2, -5.2, 3.6),
    (0.0, 0.0, 0.0),
    (0.0, 0.0, 1.0),
]
plotter.camera.zoom(1.18)

plotter.show(
    screenshot=str(OUT_PNG),
    auto_close=True,
)

print(f"Saved {OUT_PNG.resolve()}")
