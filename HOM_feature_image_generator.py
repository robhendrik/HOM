"""
Reproducible PyVista render of a glass cube beamsplitter.

This is the fixed, non-interactive version:
- smaller beamsplitter
- longer red/blue beams
- black background
- fixed glass/coating material settings
- PyVista default lighting plus fixed key/fill/rim lights
- fixed camera position, focal point, up vector, and field of view
- fixed output resolution
- no interactive camera controls
- no camera.zoom()

Requires:
    pip install pyvista vtk
"""

from pathlib import Path
import numpy as np
import pyvista as pv
import os
os.chdir("HOM")
print(os.getcwd())


# =====================================================================
# USER SETTINGS
# =====================================================================

# Geometry
SIDE = 1.45
RAY_LENGTH = 5.0

# Glass / coating
GLASS_COLOR = "#b9dce8"
COATING_COLOR = "#cbd6dc"
EDGE_COLOR = "#a9bac2"
BACKGROUND = "black"

GLASS_OPACITY = 0.20
COATING_OPACITY = 0.33

# Rays
RAY_RADIUS = 0.025
RAY_OFFSET = 0.060

RED = "#ff3b30"
BLUE = "#2997ff"

# Output
WINDOW_SIZE = (1600, 1100)
OUT_PNG = Path("feature_image.png")

# Camera
CAMERA_POSITION = (5.5, -7.5, 5.0)
CAMERA_FOCAL_POINT = (0.0, 0.0, 0.0)
CAMERA_UP = (-0.24, 0.31, 0.9)
CAMERA_VIEW_ANGLE = 30.0
CAMERA_CLIPPING_RANGE = (0.1, 30.0)

# Lighting
KEY_LIGHT_POSITION = (4.5, -4.5, 5.5)
KEY_LIGHT_INTENSITY = 1.15

FILL_LIGHT_POSITION = (-4.0, -2.0, 2.5)
FILL_LIGHT_COLOR = "#b9e8ff"
FILL_LIGHT_INTENSITY = 0.55

RIM_LIGHT_POSITION = (1.0, 5.0, 4.5)
RIM_LIGHT_INTENSITY = 0.75


# =====================================================================
# GEOMETRY HELPERS
# =====================================================================

h = SIDE / 2.0


def triangular_prism(points_xy, z0, z1):
    """Return a triangular prism as PyVista PolyData."""
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
    """Add a cylindrical light ray."""
    p0 = np.asarray(p0, dtype=float)
    p1 = np.asarray(p1, dtype=float)

    vec = p1 - p0
    length = np.linalg.norm(vec)

    tube = pv.Cylinder(
        center=0.5 * (p0 + p1),
        direction=vec,
        radius=radius,
        height=length,
        resolution=40,
    )

    plotter.add_mesh(
        tube,
        color=color,
        smooth_shading=True,
        ambient=0.35,
        diffuse=0.75,
        specular=0.80,
        specular_power=30,
    )


# =====================================================================
# BEAMSPLITTER GEOMETRY
# =====================================================================

# Two triangular prisms forming the cube
tri_a = [
    (-h, -h),
    (+h, -h),
    (+h, +h),
]

tri_b = [
    (-h, -h),
    (+h, +h),
    (-h, +h),
]

prism_a = triangular_prism(tri_a, -h, +h)
prism_b = triangular_prism(tri_b, -h, +h)

# Internal diagonal splitting plane: x = y
plane_pts = [
    (-h, -h, -h),
    (+h, +h, -h),
    (+h, +h, +h),
    (-h, -h, +h),
]

split_plane = pv.PolyData(
    plane_pts,
    [4, 0, 1, 2, 3],
)


# =====================================================================
# SCENE
# =====================================================================

plotter = pv.Plotter(
    off_screen=True,
    window_size=WINDOW_SIZE,
)

plotter.set_background(BACKGROUND)

# Better edge quality for the final image
plotter.enable_anti_aliasing("ssaa")


# ---------------------------------------------------------------------
# Glass halves
# ---------------------------------------------------------------------

for prism in (prism_a, prism_b):
    plotter.add_mesh(
        prism,
        color=GLASS_COLOR,
        opacity=GLASS_OPACITY,
        show_edges=False,
        smooth_shading=True,
        ambient=0.18,
        diffuse=0.45,
        specular=0.95,
        specular_power=60,
    )


# ---------------------------------------------------------------------
# Internal beamsplitter coating
# ---------------------------------------------------------------------

plotter.add_mesh(
    split_plane,
    color=COATING_COLOR,
    opacity=COATING_OPACITY,
    show_edges=False,
    smooth_shading=True,
    ambient=0.15,
    diffuse=0.40,
    specular=1.00,
    specular_power=80,
)


# ---------------------------------------------------------------------
# Outer cube edges
# ---------------------------------------------------------------------

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
    color=EDGE_COLOR,
    line_width=1.5,
    opacity=0.92,
)


# =====================================================================
# LIGHTING
# =====================================================================

# Keep PyVista's default light kit. This is the key difference from the
# darker first fixed-render version: the default lights give the transparent
# glass enough broad illumination to remain visible against black.
#
# The three explicit lights below are then added to shape the highlights.

key_light = pv.Light(
    position=KEY_LIGHT_POSITION,
    focal_point=(0.0, 0.0, 0.0),
    color="white",
    intensity=KEY_LIGHT_INTENSITY,
)
plotter.add_light(key_light)

fill_light = pv.Light(
    position=FILL_LIGHT_POSITION,
    focal_point=(0.0, 0.0, 0.0),
    color=FILL_LIGHT_COLOR,
    intensity=FILL_LIGHT_INTENSITY,
)
plotter.add_light(fill_light)

rim_light = pv.Light(
    position=RIM_LIGHT_POSITION,
    focal_point=(0.0, 0.0, 0.0),
    color="white",
    intensity=RIM_LIGHT_INTENSITY,
)
plotter.add_light(rim_light)


# =====================================================================
# RAYS
# =====================================================================

# Slight z offsets keep red and blue visible when they share the same port.
zr = +RAY_OFFSET / 2
zb = -RAY_OFFSET / 2

red_hit = np.array([0.0, 0.0, zr])
blue_hit = np.array([0.0, 0.0, zb])

# Red input from -x
add_ray(
    plotter,
    (-RAY_LENGTH, 0.0, zr),
    red_hit,
    RED,
)

# Blue input from -y
add_ray(
    plotter,
    (0.0, -RAY_LENGTH, zb),
    blue_hit,
    BLUE,
)

# +x output:
# transmitted red + reflected blue
add_ray(
    plotter,
    red_hit,
    (+RAY_LENGTH, 0.0, zr),
    RED,
)

add_ray(
    plotter,
    blue_hit,
    (+RAY_LENGTH, 0.0, zb),
    BLUE,
)

# +y output:
# reflected red + transmitted blue
add_ray(
    plotter,
    red_hit,
    (0.0, +RAY_LENGTH, zr),
    RED,
)

add_ray(
    plotter,
    blue_hit,
    (0.0, +RAY_LENGTH, zb),
    BLUE,
)


# =====================================================================
# FIXED CAMERA
# =====================================================================

plotter.camera.position = CAMERA_POSITION
plotter.camera.focal_point = CAMERA_FOCAL_POINT
plotter.camera.up = CAMERA_UP

plotter.camera.parallel_projection = False
plotter.camera.view_angle = CAMERA_VIEW_ANGLE
plotter.camera.clipping_range = CAMERA_CLIPPING_RANGE


# =====================================================================
# RENDER
# =====================================================================

plotter.show(
    screenshot=str(OUT_PNG),
    auto_close=True,
)

print(f"Saved: {OUT_PNG.resolve()}")

print("\nReproducible camera settings:")
print(f"position       = {CAMERA_POSITION}")
print(f"focal_point    = {CAMERA_FOCAL_POINT}")
print(f"up             = {CAMERA_UP}")
print(f"view_angle     = {CAMERA_VIEW_ANGLE}")
print(f"clipping_range = {CAMERA_CLIPPING_RANGE}")
