"""
Generate matplotlib diagrams for Course 3 Unit 3 (Activities 16–26).

Usage:
    python generate_unit3_diagrams.py
    python generate_unit3_diagrams.py --activity 22 --force
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyBboxPatch, Polygon, Rectangle, Wedge

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunCourse3", "images", "unit_3")
DPI = 150
BG = "#ffffff"
BLUE = "#3b82f6"
ORANGE = "#f97316"
PURPLE = "#8b5cf6"
GREEN = "#22c55e"
TEAL = "#0d9488"
RED = "#ef4444"
GRID = "#e5e7eb"
TEXT = "#1f2937"
MUTED = "#6b7280"


def _save(fig, name: str) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"  saved {path}")


def _off(ax):
    ax.set_facecolor(BG)
    ax.axis("off")


def _line_ax(ax, xlim=(-6, 6), ylim=(-6, 6)):
    ax.set_facecolor(BG)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axhline(0, color=GRID, lw=1)
    ax.axvline(0, color=GRID, lw=1)
    ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color(GRID)


# Activity 16
def activity_16_complementary():
    fig, ax = plt.subplots(figsize=(6, 4))
    _off(ax)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.plot([1, 3], [1, 3], color=BLUE, lw=2)
    ax.plot([3, 4.5], [3, 1.5], color=ORANGE, lw=2)
    ax.text(2, 3.3, "50°", fontsize=11, color=BLUE, fontweight="bold")
    ax.text(3.8, 2.2, "40°", fontsize=11, color=ORANGE, fontweight="bold")
    ax.text(3, 0.5, "50° + 40° = 90° (complementary)", ha="center", fontsize=10, color=TEAL)
    fig.suptitle("Complementary angles sum to 90°", fontsize=13, fontweight="bold")
    _save(fig, "activity_16_complementary.png")


def activity_16_transversal():
    fig, ax = plt.subplots(figsize=(7, 4))
    _off(ax)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5)
    ax.plot([0.5, 7.5], [2, 2], color=BLUE, lw=2)
    ax.plot([0.5, 7.5], [3.5, 3.5], color=BLUE, lw=2)
    ax.plot([2, 6], [0.5, 4.5], color=ORANGE, lw=2)
    ax.text(4, 4.7, "Transversal", ha="center", fontsize=9, color=ORANGE)
    ax.text(4, 1.5, "Parallel lines -> matching angles equal", ha="center", fontsize=10, color=TEAL)
    fig.suptitle("Parallel lines and a transversal", fontsize=13, fontweight="bold")
    _save(fig, "activity_16_transversal.png")


# Activity 17
def activity_17_triangle_sum():
    fig, ax = plt.subplots(figsize=(5, 4.5))
    tri = Polygon([[1, 1], [5, 1], [3, 4.5]], closed=True, fill=BLUE, alpha=0.15, edgecolor=BLUE, lw=2)
    ax.add_patch(tri)
    ax.text(1, 0.5, "32°", fontsize=11, fontweight="bold")
    ax.text(4.7, 0.5, "70°", fontsize=11, fontweight="bold")
    ax.text(2.7, 4.8, "78°", fontsize=11, fontweight="bold", color=GREEN)
    ax.text(3, -0.3, "32 + 70 + 78 = 180°", ha="center", fontsize=10, color=TEAL)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    fig.suptitle("Triangle angle sum = 180°", fontsize=13, fontweight="bold")
    _save(fig, "activity_17_triangle_sum.png")


def activity_17_quadrilateral():
    fig, ax = plt.subplots(figsize=(6, 4))
    quad = Polygon([[1, 1], [5, 1], [5.5, 3], [0.5, 3]], closed=True, fill=PURPLE, alpha=0.12, edgecolor=PURPLE, lw=2)
    ax.add_patch(quad)
    ax.text(3, 0.4, "Four angles sum to 360°", ha="center", fontsize=11, color=TEAL)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.axis("off")
    fig.suptitle("Quadrilateral angle sum = 360°", fontsize=13, fontweight="bold")
    _save(fig, "activity_17_quadrilateral.png")


# Activity 18
def activity_18_transformations():
    fig, axes = plt.subplots(1, 3, figsize=(9, 3))
    titles = ["Translation", "Reflection", "Rotation"]
    for ax, title in zip(axes, titles):
        _line_ax(ax, (-3, 3), (-3, 3))
        ax.plot([-1, 1, 0], [-1, -1, 1], color=BLUE, lw=2)
        if title == "Translation":
            ax.plot([0, 2, 1, -1 + 2], [-1, -1, 1, 1], "--", color=ORANGE, lw=2)
        elif title == "Reflection":
            ax.axvline(0, color=ORANGE, ls="--", lw=1)
            ax.plot([1, -1, 0], [-1, -1, 1], "--", color=ORANGE, lw=2)
        else:
            ax.plot([-1, 0, 1], [1, -1, -1], "--", color=ORANGE, lw=2)
        ax.set_title(title, fontsize=10, fontweight="bold")
    fig.suptitle("Types of transformations", fontsize=13, fontweight="bold")
    fig.subplots_adjust(wspace=0.35)
    _save(fig, "activity_18_transformations.png")


def activity_18_coordinate():
    fig, ax = plt.subplots(figsize=(5, 5))
    _line_ax(ax)
    ax.plot([1, 2, 3], [1, 3, 2], color=BLUE, lw=2, marker="o")
    ax.plot([1 + 2, 2 + 2, 3 + 2], [1, 3, 2], "--", color=ORANGE, lw=2, marker="o")
    ax.annotate("", xy=(4, 2), xytext=(2, 2), arrowprops=dict(arrowstyle="->", color=TEAL))
    ax.text(3, -4.5, "Translate right 2 units", ha="center", fontsize=10, color=TEAL)
    fig.suptitle("Translation on the coordinate plane", fontsize=13, fontweight="bold")
    _save(fig, "activity_18_coordinate.png")


# Activity 19
def activity_19_rigid():
    fig, ax = plt.subplots(figsize=(6, 3))
    _off(ax)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 3.5)
    props = ["Same size and shape", "Angles congruent", "Sides congruent", "Distance preserved"]
    for i, p in enumerate(props):
        ax.text(0.5, 2.8 - i * 0.65, f"  {p}", fontsize=11, color=TEXT if i else TEAL, fontweight="bold" if i == 0 else "normal")
    fig.suptitle("Rigid transformations (isometries)", fontsize=13, fontweight="bold")
    _save(fig, "activity_19_rigid.png")


def activity_19_rotation():
    fig, ax = plt.subplots(figsize=(5, 5))
    _line_ax(ax)
    ax.plot([2, 3, 2.5], [1, 2, 3], color=BLUE, lw=2, marker="o")
    ax.plot([-1, -2, -1.5], [2, 1, -1], "--", color=GREEN, lw=2, marker="o")
    ax.text(0, -5, "90° rotation about origin", ha="center", fontsize=10, color=TEAL)
    fig.suptitle("Rotation about the origin", fontsize=13, fontweight="bold")
    _save(fig, "activity_19_rotation.png")


# Activity 20
def activity_20_similar():
    fig, ax = plt.subplots(figsize=(7, 4))
    _off(ax)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4)
    t1 = Polygon([[1, 1], [4, 1], [2.5, 3]], closed=True, fill=BLUE, alpha=0.2, edgecolor=BLUE, lw=2)
    t2 = Polygon([[4.5, 1], [7, 1], [5.75, 2.2]], closed=True, fill=ORANGE, alpha=0.2, edgecolor=ORANGE, lw=2)
    ax.add_patch(t1)
    ax.add_patch(t2)
    ax.text(2.5, 0.4, "Large triangle", ha="center", fontsize=9)
    ax.text(5.75, 0.4, "Similar (same angles)", ha="center", fontsize=9)
    fig.suptitle("Similar triangles: same shape, proportional sides", fontsize=13, fontweight="bold")
    _save(fig, "activity_20_similar.png")


def activity_20_aa():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    _off(ax)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 3.5)
    ax.text(0.5, 2.5, "AA Similarity", fontsize=12, fontweight="bold")
    ax.text(0.5, 1.8, "If two angles of one triangle", fontsize=10)
    ax.text(0.5, 1.4, "equal two angles of another,", fontsize=10)
    ax.text(0.5, 1.0, "the triangles are similar.", fontsize=10, color=TEAL)
    fig.suptitle("Angle-Angle (AA) criterion", fontsize=13, fontweight="bold")
    _save(fig, "activity_20_aa.png")


# Activity 21
def activity_21_dilation():
    fig, ax = plt.subplots(figsize=(7, 4))
    _off(ax)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4)
    ax.add_patch(Rectangle((1, 1), 2, 1.5, fill=BLUE, alpha=0.3, edgecolor=BLUE, lw=2, linestyle="--"))
    ax.add_patch(Rectangle((4.5, 0.5), 3, 2.25, fill=ORANGE, alpha=0.2, edgecolor=ORANGE, lw=2))
    ax.text(2, 0.3, "Pre-image", ha="center", fontsize=9)
    ax.text(6, 0.1, "Image (scale factor 1.5)", ha="center", fontsize=9)
    fig.suptitle("Dilation: enlarge or shrink from a center", fontsize=13, fontweight="bold")
    _save(fig, "activity_21_dilation.png")


def activity_21_scale_factor():
    fig, ax = plt.subplots(figsize=(6, 3))
    _off(ax)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 3)
    ax.text(0.4, 2.2, "k > 1  ->  enlargement", fontsize=11, color=GREEN)
    ax.text(0.4, 1.4, "0 < k < 1  ->  reduction", fontsize=11, color=ORANGE)
    ax.text(0.4, 0.6, "k = 1  ->  same size", fontsize=11, color=BLUE)
    fig.suptitle("Scale factor k", fontsize=13, fontweight="bold")
    _save(fig, "activity_21_scale_factor.png")


# Activity 22
def activity_22_pythagorean():
    fig, ax = plt.subplots(figsize=(5.5, 5))
    tri = Polygon([[1, 1], [5, 1], [1, 4]], closed=True, fill=BLUE, alpha=0.1, edgecolor=BLUE, lw=2)
    ax.add_patch(tri)
    ax.add_patch(Rectangle((1, 1), 4, 3, fill=ORANGE, alpha=0.08, edgecolor=ORANGE, lw=1.5, linestyle="--"))
    ax.text(3, 0.4, "a", fontsize=12, ha="center")
    ax.text(0.4, 2.5, "b", fontsize=12)
    ax.text(3.5, 2.5, "c", fontsize=12, color=GREEN, fontweight="bold")
    ax.text(3, -0.5, "a^2 + b^2 = c^2", ha="center", fontsize=12, color=TEAL, fontweight="bold")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 5)
    ax.axis("off")
    fig.suptitle("Pythagorean Theorem (right triangle)", fontsize=13, fontweight="bold")
    _save(fig, "activity_22_pythagorean.png")


def activity_22_solve_triangle():
    fig, ax = plt.subplots(figsize=(5, 5))
    tri = Polygon([[0.5, 1], [4.5, 1], [0.5, 4.2]], closed=True, fill=GREEN, alpha=0.1, edgecolor=GREEN, lw=2)
    ax.add_patch(tri)
    ax.text(2.5, 0.5, "leg = 5", ha="center", fontsize=10)
    ax.text(0.2, 2.5, "leg = 8", fontsize=10)
    ax.text(2.8, 2.8, "c = ?", fontsize=11, fontweight="bold", color=RED)
    ax.text(2.5, -0.3, "c^2 = 5^2 + 8^2 = 89", ha="center", fontsize=10, color=TEAL)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.axis("off")
    fig.suptitle("Find hypotenuse: c = sqrt(89)", fontsize=13, fontweight="bold")
    _save(fig, "activity_22_solve_triangle.png")


# Activity 23
def activity_23_ladder():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_facecolor(BG)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.plot([0, 4], [0, 0], color=TEXT, lw=2)
    ax.plot([0, 0], [0, 4], color=TEXT, lw=2)
    ax.plot([0, 4], [4, 0], color=ORANGE, lw=2.5)
    ax.text(2, -0.4, "15 ft", ha="center", fontsize=10)
    ax.text(-0.5, 2, "20 ft", fontsize=10)
    ax.text(2.2, 2.2, "ladder?", fontsize=11, fontweight="bold", color=TEAL)
    ax.text(3, 5.2, "15^2 + 20^2 = 625 -> 25 ft", fontsize=10, color=GREEN)
    ax.axis("off")
    fig.suptitle("Ladder problem (Pythagorean Theorem)", fontsize=13, fontweight="bold")
    _save(fig, "activity_23_ladder.png")


def activity_23_diagonal():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.add_patch(Rectangle((1, 1), 3, 3, fill=BLUE, alpha=0.15, edgecolor=BLUE, lw=2))
    ax.plot([1, 4], [1, 4], color=ORANGE, lw=2.5)
    ax.text(2.5, 2.8, "diagonal 20 m", fontsize=10, color=ORANGE, fontweight="bold")
    ax.text(2.5, 0.3, "side = 20/sqrt(2) ~ 14.1 m", ha="center", fontsize=10, color=TEAL)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.axis("off")
    fig.suptitle("Diagonal of a square", fontsize=13, fontweight="bold")
    _save(fig, "activity_23_diagonal.png")


# Activity 24
def activity_24_converse():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    _off(ax)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 3.5)
    ax.text(0.4, 2.5, "If a^2 + b^2 = c^2", fontsize=11, fontweight="bold")
    ax.text(0.4, 1.8, "then the triangle is a RIGHT triangle", fontsize=11, color=GREEN)
    ax.text(0.4, 1.0, "Test: 3-4-5  ->  9+16=25  OK", fontsize=10, color=TEAL)
    fig.suptitle("Converse of the Pythagorean Theorem", fontsize=13, fontweight="bold")
    _save(fig, "activity_24_converse.png")


def activity_24_test_triangle():
    fig, ax = plt.subplots(figsize=(6, 3))
    _off(ax)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 3)
    cases = [("3, 4, 5", "9+16=25", True), ("5, 4, 6", "25+16=41", False)]
    for i, (sides, check, ok) in enumerate(cases):
        color = GREEN if ok else RED
        ax.text(0.5, 2.2 - i * 0.9, f"{sides}: {check}  {'Right triangle' if ok else 'Not right'}", fontsize=10, color=color)
    fig.suptitle("Is it a right triangle?", fontsize=13, fontweight="bold")
    _save(fig, "activity_24_test_triangle.png")


# Activity 25
def activity_25_prism_net():
    fig, ax = plt.subplots(figsize=(7, 4))
    _off(ax)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4)
    # net sketch
    for x, y, w, h in [(1, 2, 2, 1.5), (3.2, 2, 2, 1.5), (1, 0.3, 2, 1.5), (3.2, 0.3, 2, 1.5), (1, 3.7, 2, 1)]:
        ax.add_patch(Rectangle((x, y), w, h, fill=BLUE, alpha=0.15, edgecolor=BLUE, lw=1.5))
    ax.text(4, 0.1, "Net folds into rectangular prism", ha="center", fontsize=10, color=TEAL)
    fig.suptitle("Surface area from a net", fontsize=13, fontweight="bold")
    _save(fig, "activity_25_prism_net.png")


def activity_25_surface_area():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax = fig.add_subplot(111, projection="3d")
    ax.bar3d(0, 0, 0, 2, 1.5, 1, color=BLUE, alpha=0.5, edgecolor=BLUE)
    ax.set_title("SA = 2(lw + lh + wh)", fontsize=11, fontweight="bold")
    ax.set_axis_off()
    fig.suptitle("Rectangular prism surface area", fontsize=13, fontweight="bold")
    _save(fig, "activity_25_surface_area.png")


# Activity 26
def activity_26_volume_prism():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax = fig.add_subplot(111, projection="3d")
    ax.bar3d(0, 0, 0, 2, 1.5, 1.2, color=TEAL, alpha=0.55, edgecolor=TEAL)
    ax.set_title("V = l x w x h", fontsize=11, fontweight="bold")
    ax.set_axis_off()
    fig.suptitle("Volume of a rectangular prism", fontsize=13, fontweight="bold")
    _save(fig, "activity_26_volume_prism.png")


def activity_26_volume_solids():
    fig, ax = plt.subplots(figsize=(8, 3))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    formulas = [
        ("Prism / cylinder", "V = Bh"),
        ("Pyramid / cone", "V = (1/3)Bh"),
        ("Sphere", "V = (4/3)pi r^3"),
    ]
    for i, (name, form) in enumerate(formulas):
        ax.text(0.5, 2.3 - i * 0.75, f"{name}:  {form}", fontsize=11, color=[BLUE, ORANGE, PURPLE][i], fontweight="bold")
    fig.suptitle("Volume formulas", fontsize=13, fontweight="bold")
    _save(fig, "activity_26_volume_solids.png")


GENERATORS: dict[int, list[tuple[str, callable]]] = {
    16: [("activity_16_complementary.png", activity_16_complementary), ("activity_16_transversal.png", activity_16_transversal)],
    17: [("activity_17_triangle_sum.png", activity_17_triangle_sum), ("activity_17_quadrilateral.png", activity_17_quadrilateral)],
    18: [("activity_18_transformations.png", activity_18_transformations), ("activity_18_coordinate.png", activity_18_coordinate)],
    19: [("activity_19_rigid.png", activity_19_rigid), ("activity_19_rotation.png", activity_19_rotation)],
    20: [("activity_20_similar.png", activity_20_similar), ("activity_20_aa.png", activity_20_aa)],
    21: [("activity_21_dilation.png", activity_21_dilation), ("activity_21_scale_factor.png", activity_21_scale_factor)],
    22: [("activity_22_pythagorean.png", activity_22_pythagorean), ("activity_22_solve_triangle.png", activity_22_solve_triangle)],
    23: [("activity_23_ladder.png", activity_23_ladder), ("activity_23_diagonal.png", activity_23_diagonal)],
    24: [("activity_24_converse.png", activity_24_converse), ("activity_24_test_triangle.png", activity_24_test_triangle)],
    25: [("activity_25_prism_net.png", activity_25_prism_net), ("activity_25_surface_area.png", activity_25_surface_area)],
    26: [("activity_26_volume_prism.png", activity_26_volume_prism), ("activity_26_volume_solids.png", activity_26_volume_solids)],
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--activity", type=int, choices=list(GENERATORS))
    p.add_argument("--force", action="store_true")
    args = p.parse_args()
    acts = [args.activity] if args.activity else sorted(GENERATORS)
    for act in acts:
        print(f"\nActivity {act}:")
        for name, fn in GENERATORS[act]:
            path = os.path.join(OUT_DIR, name)
            if args.force or not os.path.isfile(path):
                fn()
            else:
                print(f"  skip {name} (exists)")


if __name__ == "__main__":
    main()
