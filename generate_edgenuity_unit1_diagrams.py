"""
Generate matplotlib diagrams for Edgenuity Course 3 Unit 1 (lesson + practice).

Usage:
    python generate_edgenuity_unit1_diagrams.py
    python generate_edgenuity_unit1_diagrams.py --practice-only
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunEdgenuityCourse3", "images", "unit_1")
PRACTICE_DIR = os.path.join(OUT_DIR, "practice")
DPI = 150
BG = "#ffffff"
BLUE = "#3b82f6"
ORANGE = "#f97316"
GREEN = "#22c55e"
RED = "#ef4444"
TEAL = "#0d9488"
PURPLE = "#8b5cf6"
TEXT = "#1f2937"
GRID = "#e5e7eb"


def _save(fig, name: str, practice: bool = False) -> None:
    base = PRACTICE_DIR if practice else OUT_DIR
    os.makedirs(base, exist_ok=True)
    path = os.path.join(base, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"  saved {path}")


def _axes_style(ax, xlim, ylim, title=""):
    ax.set_facecolor(BG)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.axhline(0, color=TEXT, lw=1)
    ax.axvline(0, color=TEXT, lw=1)
    ax.grid(True, color=GRID, ls="--", alpha=0.7)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    if title:
        ax.set_title(title, fontsize=12, fontweight="bold")


def _axes_style_real(ax, xlim, ylim, xlabel: str, ylabel: str, title: str = ""):
    """Practice graphs with real-world axis labels (not generic x/y)."""
    ax.set_facecolor(BG)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    if xlim[0] <= 0 <= xlim[1]:
        ax.axhline(0, color=TEXT, lw=1)
    if ylim[0] <= 0 <= ylim[1]:
        ax.axvline(0, color=TEXT, lw=1)
    ax.grid(True, color=GRID, ls="--", alpha=0.7)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    if title:
        ax.set_title(title, fontsize=11, fontweight="bold")


# ── Activity 1 ──
def activity_1_quadrants():
    fig, ax = plt.subplots(figsize=(6, 6))
    _axes_style(ax, (-5, 5), (-5, 5), "Quadrants")
    colors = ["#dbeafe", "#fef3c7", "#fee2e2", "#dcfce7"]
    labels = ["I (+,+)", "II (−,+)", "III (−,−)", "IV (+,−)"]
    rects = [(0, 0, 5, 5), (-5, 0, 5, 5), (-5, -5, 5, 5), (0, -5, 5, 5)]
    for (x, y, w, h), c, lab in zip(rects, colors, labels):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=c, alpha=0.5, edgecolor=GRID))
        ax.text(x + w / 2, y + h / 2, lab, ha="center", va="center", fontsize=10)
    _save(fig, "activity_1_quadrants.png")


def activity_1_read_point():
    fig, ax = plt.subplots(figsize=(6, 6))
    _axes_style(ax, (-7, 7), (-7, 7), "Reading coordinates")
    ax.plot(-4, 3, "o", color=RED, ms=12)
    ax.annotate("P (−4, 3)", (-4, 3), xytext=(-2, 5), fontsize=11, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.plot([-4, -4], [0, 3], "--", color=TEAL, lw=1)
    ax.plot([0, -4], [3, 3], "--", color=TEAL, lw=1)
    _save(fig, "activity_1_read_point.png")


# ── Activity 2 ──
def activity_2_vertical_line_test():
    fig, ax = plt.subplots(figsize=(6, 6))
    _axes_style(ax, (-5, 5), (-5, 5), "Vertical line test")
    pts = [(-4, 3), (-2, 1), (-2, -3), (0, 4), (1, 1), (2, 3)]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], c=BLUE, s=80, zorder=3)
    ax.axvline(-2, color=RED, ls="--", lw=2, label="x = −2 hits twice")
    ax.legend()
    _save(fig, "activity_2_vertical_line_test.png")


def activity_2_mapping_diagram():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.text(1.5, 3.2, "Input\n(Package #)", ha="center", fontsize=11, fontweight="bold")
    ax.text(8, 3.2, "Output\n(Price $)", ha="center", fontsize=11, fontweight="bold")
    for y, lab in [(2.2, "Pkg 1"), (1.2, "Pkg 2")]:
        ax.add_patch(FancyArrowPatch((2.5, y), (6.5, 2.5), arrowstyle="->", color=BLUE, lw=2))
        ax.add_patch(FancyArrowPatch((2.5, y), (6.5, 1.5), arrowstyle="->", color=RED, lw=2))
        ax.text(1.2, y, lab, fontsize=10)
    ax.text(7, 2.5, "$160", fontsize=10, color=BLUE)
    ax.text(7, 1.5, "$110", fontsize=10, color=RED)
    ax.text(5, 0.3, "Same input → two outputs = NOT a function", ha="center", fontsize=10, color=RED)
    fig.suptitle("Weekend vs weekday prices", fontsize=12, fontweight="bold")
    _save(fig, "activity_2_mapping_diagram.png")


def activity_2_function_equations():
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.axis("off")
    eqs = ["x = y² + 9  ✗", "x² = y  ✓ (y = x²)", "x = 5  ✗", "x² = y² + 16  ✗"]
    for i, e in enumerate(eqs):
        ax.text(0.5, 0.75 - i * 0.2, e, fontsize=12, transform=ax.transAxes)
    ax.set_title("Which defines y as a function of x?", fontsize=12, fontweight="bold")
    _save(fig, "activity_2_function_equations.png")


# ── Activity 3 ──
def activity_3_segment_graph():
    fig, ax = plt.subplots(figsize=(7, 4))
    _axes_style(ax, (-1, 8), (-2, 6), "Graph behavior A → F")
    xs = [0, 2, 4, 5, 7, 8]
    ys = [0, 4, 4, 1, 0, -1]
    ax.plot(xs, ys, "o-", color=BLUE, lw=2, ms=8)
    labels = "ABCDEF"
    for i, (x, y) in enumerate(zip(xs, ys)):
        ax.text(x, y + 0.3, labels[i], fontsize=10, fontweight="bold")
    ax.text(1, 5, "increasing", color=GREEN, fontsize=9)
    ax.text(3.5, 5, "constant", color=ORANGE, fontsize=9)
    ax.text(6, 3, "decreasing", color=RED, fontsize=9)
    _save(fig, "activity_3_segment_graph.png")


def activity_3_parabola_behavior():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-4, 4), (-1, 8), "Parabola y = x²")
    x = np.linspace(-3, 3, 100)
    ax.plot(x, x ** 2, color=PURPLE, lw=2)
    ax.text(-2.5, 6, "decreasing", color=RED, fontsize=9)
    ax.text(1.5, 6, "increasing", color=GREEN, fontsize=9)
    ax.plot(0, 0, "o", color=ORANGE, ms=10)
    ax.text(0.3, 0.5, "vertex", fontsize=9)
    _save(fig, "activity_3_parabola_behavior.png")


def activity_3_distance_time():
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_facecolor(BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_xlabel("Time")
    ax.set_ylabel("Distance")
    ax.set_title("Mary's trip — distance vs time", fontweight="bold")
    ax.grid(True, color=GRID, ls="--", alpha=0.7)
    t = [0, 2, 4, 5, 6, 8, 10]
    d = [0, 1, 2, 2, 2.5, 3, 4]
    ax.plot(t, d, "o-", color=TEAL, lw=2, ms=8)
    ax.annotate("stopped\n(flat)", (4.5, 2), fontsize=9, color=ORANGE)
    _save(fig, "activity_3_distance_time.png")


# ── Activity 4 ──
def activity_4_unit_rate():
    fig, ax = plt.subplots(figsize=(6, 4))
    _axes_style(ax, (-1, 10), (-5, 80), "Tickets vs profit")
    xs = [2, 4, 6, 8]
    ys = [18, 36, 54, 72]
    ax.plot(xs, ys, "o-", color=GREEN, lw=2, ms=10)
    ax.text(5, 60, "slope = $9/ticket", fontsize=10, color=TEAL)
    _save(fig, "activity_4_unit_rate.png")


def activity_4_perimeter_equation():
    fig, ax = plt.subplots(figsize=(6, 4))
    _axes_style(ax, (0, 15), (0, 60), "Square side vs perimeter")
    xs = [4.5, 8.5, 10.25, 13.75]
    ys = [18, 34, 41, 55]
    ax.plot(xs, ys, "o-", color=BLUE, lw=2, ms=10)
    ax.text(8, 45, "y = 4x", fontsize=12, color=TEAL, fontweight="bold")
    _save(fig, "activity_4_perimeter_equation.png")


def activity_4_jaxon_change():
    fig, ax = plt.subplots(figsize=(6, 4))
    _axes_style(ax, (-1, 10), (-1, 12), "Jaxon's change")
    xs = list(range(10))
    ys = [10 - x for x in xs]
    ax.plot(xs, ys, "o-", color=ORANGE, lw=2, ms=8)
    ax.set_xlabel("Cost of item ($)")
    ax.set_ylabel("Change ($)")
    ax.text(4, 8, "y = 10 − x", fontsize=12, fontweight="bold", color=TEAL)
    _save(fig, "activity_4_jaxon_change.png")


# ── Activity 5 ──
def activity_5_table_to_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-4, 3), (-3, 4), "y = x + 1")
    pts = [(-3, -2), (-1, 0), (1, 2)]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], c=RED, s=100, zorder=3)
    x = np.linspace(-4, 2, 50)
    ax.plot(x, x + 1, "--", color=BLUE, alpha=0.6)
    for p in pts:
        ax.text(p[0] + 0.2, p[1], str(p), fontsize=9)
    _save(fig, "activity_5_table_to_graph.png")


def activity_5_evaluate_equation():
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis("off")
    ax.text(0.5, 0.7, "r = 3c + 5", ha="center", fontsize=16, fontweight="bold", transform=ax.transAxes)
    ax.text(0.5, 0.45, "c = 12  →  r = 3(12) + 5 = 41", ha="center", fontsize=12, transform=ax.transAxes)
    ax.text(0.5, 0.2, "Missing table value: 41", ha="center", fontsize=11, color=GREEN, transform=ax.transAxes)
    _save(fig, "activity_5_evaluate_equation.png")


def activity_5_gas_tank():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_facecolor(BG)
    ax.set_xlim(-10, 260)
    ax.set_ylim(0, 14)
    ax.set_xlabel("Distance (miles)")
    ax.set_ylabel("Gas (gallons)")
    ax.set_title("Gas remaining vs distance", fontweight="bold")
    ax.grid(True, color=GRID, ls="--", alpha=0.7)
    xs = [0, 20, 60, 100, 240]
    ys = [12, 11, 9, 7, 0]
    ax.plot(xs, ys, "o-", color=BLUE, lw=2, ms=8)
    ax.annotate("full tank → 240 mi", (240, 0), xytext=(150, 2), arrowprops=dict(arrowstyle="->"))
    _save(fig, "activity_5_gas_tank.png")


# ── Activity 6 ──
def activity_6_movie_rentals():
    fig, ax = plt.subplots(figsize=(7, 4))
    _axes_style(ax, (-1, 16), (-5, 50), "Movie rental cost")
    x = np.linspace(0, 15, 50)
    ax.plot(x, 10 + 2 * x, label="Movies Plus", color=BLUE, lw=2)
    ax.plot(x, 3 * x, label="Movies For Less", color=ORANGE, lw=2)
    ax.axvline(15, color=GRID, ls=":")
    ax.plot(15, 40, "o", color=BLUE, ms=10)
    ax.plot(15, 45, "o", color=ORANGE, ms=10)
    ax.legend()
    ax.text(15.5, 42, "15 movies: $40 vs $45", fontsize=9)
    _save(fig, "activity_6_movie_rentals.png")


def activity_6_bank_deposits():
    fig, ax = plt.subplots(figsize=(6, 4))
    _axes_style(ax, (-1, 8), (0, 420), "Bank balance")
    x = np.arange(0, 8)
    y = 125 + 45 * x
    ax.plot(x, y, "o-", color=GREEN, lw=2, ms=10)
    ax.axhline(360, color=RED, ls="--", label="Goal $360")
    ax.axvline(6, color=TEAL, ls=":", label="6 months")
    ax.legend(fontsize=9)
    _save(fig, "activity_6_bank_deposits.png")


def activity_6_inverse_lookup():
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis("off")
    rows = [(5, 15), (8, 18), (10, 20), (15, 25), ("?", 60)]
    ax.text(0.5, 0.9, "Sarah's craft demo: cost = people + 10", ha="center", fontsize=12,
            fontweight="bold", transform=ax.transAxes)
    for i, (p, c) in enumerate(rows):
        ax.text(0.3, 0.7 - i * 0.12, f"People: {p}", fontsize=11, transform=ax.transAxes)
        ax.text(0.6, 0.7 - i * 0.12, f"Cost: ${c}", fontsize=11, transform=ax.transAxes)
    ax.text(0.5, 0.05, "60 = x + 10  →  x = 50", ha="center", fontsize=11, color=GREEN, transform=ax.transAxes)
    _save(fig, "activity_6_inverse_lookup.png")


# ── Practice images ──
def practice_segment_graph():
    activity_3_segment_graph()
    import shutil
    src = os.path.join(OUT_DIR, "activity_3_segment_graph.png")
    dst = os.path.join(PRACTICE_DIR, "practice_segment_graph.png")
    os.makedirs(PRACTICE_DIR, exist_ok=True)
    shutil.copy(src, dst)
    print(f"  saved {dst}")


def _plot_point(ax, x, y, label="P", color=RED, *, show_coords: bool = False, guides: bool = True):
    """Plot a point for practice graphs. Never show_coords on quiz diagrams."""
    ax.plot(x, y, "o", color=color, ms=12, zorder=5)
    if guides:
        ax.plot([x, x], [0, y], "--", color=TEAL, lw=1, alpha=0.8)
        ax.plot([0, x], [y, y], "--", color=TEAL, lw=1, alpha=0.8)
    caption = f"{label} ({x}, {y})" if show_coords else label
    ax.text(x, y + 0.6, caption, ha="center", fontsize=10, color=color, fontweight="bold")


def practice_coord_read_p():
    """Exam Q3 — read coordinates of P."""
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    _axes_style(ax, (-7, 7), (-7, 7), "What are the coordinates of P?")
    _plot_point(ax, -4, 3)
    _save(fig, "practice_coord_read_p.png", practice=True)


def practice_coord_q2_ii():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    _axes_style(ax, (-7, 7), (-7, 7), "Which quadrant is the point in?")
    _plot_point(ax, -3, 5, color=PURPLE, guides=False)
    _save(fig, "practice_coord_q2_ii.png", practice=True)


def practice_coord_q4():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    _axes_style(ax, (-7, 7), (-7, 7), "Which quadrant is the point in?")
    _plot_point(ax, 2, -4, color=ORANGE, guides=False)
    _save(fig, "practice_coord_q4.png", practice=True)


def practice_coord_xaxis():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    _axes_style(ax, (-6, 6), (-6, 6), "Which labeled point is on the x-axis?")
    for x, y, lab, c in [(-5, 1, "A", BLUE), (0, -5, "B", ORANGE), (2, 2, "C", GREEN), (1, 0, "D", RED)]:
        ax.plot(x, y, "o", color=c, ms=10)
        ax.text(x + 0.25, y + 0.35, lab, fontsize=11, fontweight="bold", color=c)
    _save(fig, "practice_coord_xaxis.png", practice=True)


def practice_vlt_remove():
    """Exam Q4 — duplicate x = -2."""
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    _axes_style(ax, (-5, 5), (-5, 5), "Removing which point makes this a function?")
    pts = [(-4, 3), (-2, 1), (-2, -3), (0, 4), (1, 1), (2, 3)]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], c=BLUE, s=90, zorder=3)
    for x, y in pts:
        ax.text(x + 0.15, y + 0.25, f"({x},{y})", fontsize=8)
    ax.axvline(-2, color=RED, ls="--", lw=1.5, alpha=0.7)
    _save(fig, "practice_vlt_remove.png", practice=True)


def practice_vlt_scatter():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    _axes_style(ax, (-5, 5), (-5, 5), "Is this relation a function of x?")
    pts = [(-3, -1), (-2, 5), (4, 0), (7, -1)]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], c=GREEN, s=100)
    _save(fig, "practice_vlt_scatter.png", practice=True)


def practice_vlt_fail():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    _axes_style(ax, (-5, 5), (-5, 5), "Does this graph pass the vertical line test?")
    pts = [(-2, 1), (-2, -3), (1, 2), (3, -1)]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], c=RED, s=100)
    ax.axvline(-2, color=RED, ls="--", lw=2)
    _save(fig, "practice_vlt_fail.png", practice=True)


def practice_segment_cd():
    fig, ax = plt.subplots(figsize=(6, 4))
    _axes_style(ax, (-1, 8), (-2, 6), "How does the graph change from C to D?")
    xs = [0, 2, 4, 5, 7]
    ys = [0, 4, 4, 1, 0]
    ax.plot(xs, ys, "o-", color=BLUE, lw=2, ms=8)
    for i, (x, y) in enumerate(zip(xs, ys)):
        ax.text(x, y + 0.35, "ABCDE"[i], fontsize=11, fontweight="bold")
    ax.annotate("C → D", (4.5, 2.5), fontsize=10, color=RED)
    _save(fig, "practice_segment_cd.png", practice=True)


def practice_segment_bc():
    fig, ax = plt.subplots(figsize=(6, 4))
    _axes_style(ax, (-1, 8), (-2, 6), "How does the graph change from B to C?")
    xs = [0, 2, 4, 5, 7]
    ys = [0, 4, 4, 1, 0]
    ax.plot(xs, ys, "o-", color=BLUE, lw=2, ms=8)
    for i, (x, y) in enumerate(zip(xs, ys)):
        ax.text(x, y + 0.35, "ABCDE"[i], fontsize=11, fontweight="bold")
    _save(fig, "practice_segment_bc.png", practice=True)


def practice_distance_time():
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.set_facecolor(BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Distance (miles)")
    ax.set_title("Distance vs time — which segment shows no change in distance?", fontweight="bold")
    ax.grid(True, color=GRID, ls="--", alpha=0.7)
    t = [0, 2, 4, 5, 6, 8, 10]
    d = [0, 1, 2, 2, 2.5, 3, 4]
    ax.plot(t, d, "o-", color=TEAL, lw=2.5, ms=8)
    ax.axvspan(4, 5, alpha=0.15, color=ORANGE)
    ax.text(4.5, 3.2, "stopped here", ha="center", fontsize=9, color=ORANGE)
    _save(fig, "practice_distance_time.png", practice=True)


def practice_table_line():
    """Exam Q17 — y = x + 1. Points unlabeled so student reads the graph."""
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    _axes_style_real(
        ax, (-4, 3), (-3, 4),
        "Input value", "Output value",
        "Which data table matches this line?",
    )
    pts = [(-3, -2), (-1, 0), (1, 2)]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], c=RED, s=120, zorder=3)
    x = np.linspace(-4, 2, 50)
    ax.plot(x, x + 1, "--", color=BLUE, alpha=0.5)
    _save(fig, "practice_table_line.png", practice=True)


def practice_tickets_graph():
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _axes_style_real(
        ax, (-0.5, 10), (-5, 80),
        "Tickets sold", "Profit ($)",
        "School fundraiser — tickets vs profit",
    )
    xs = [2, 4, 6, 8]
    ys = [18, 36, 54, 72]
    ax.plot(xs, ys, "o-", color=GREEN, lw=2, ms=10)
    _save(fig, "practice_tickets_graph.png", practice=True)


def practice_perimeter_graph():
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _axes_style_real(
        ax, (0, 15), (0, 60),
        "Side length (inches)", "Perimeter (inches)",
        "Square garden bed — side vs perimeter",
    )
    xs = [4.5, 8.5, 10.25, 13.75]
    ys = [18, 34, 41, 55]
    ax.plot(xs, ys, "o-", color=BLUE, lw=2, ms=10)
    _save(fig, "practice_perimeter_graph.png", practice=True)


def practice_movie_compare():
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _axes_style_real(
        ax, (-1, 16), (-5, 55),
        "Movies rented", "Total cost ($)",
        "Movie rental plans — cost comparison",
    )
    x = np.linspace(0, 15, 50)
    ax.plot(x, 10 + 2 * x, label="Movies Plus", color=BLUE, lw=2)
    ax.plot(x, 3 * x, label="Movies For Less", color=ORANGE, lw=2)
    ax.axvline(15, color=GRID, ls=":")
    ax.legend(fontsize=9)
    _save(fig, "practice_movie_compare.png", practice=True)


def practice_gas_tank_graph():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_facecolor(BG)
    ax.set_xlim(-10, 260)
    ax.set_ylim(0, 14)
    ax.set_xlabel("Distance traveled (miles)")
    ax.set_ylabel("Gas left (gallons)")
    ax.set_title("Gas remaining vs distance", fontweight="bold")
    ax.grid(True, color=GRID, ls="--", alpha=0.7)
    xs = [0, 20, 60, 100, 240]
    ys = [12, 11, 9, 7, 0]
    ax.plot(xs, ys, "o-", color=BLUE, lw=2, ms=8)
    _save(fig, "practice_gas_tank_graph.png", practice=True)


def practice_bank_graph():
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _axes_style_real(
        ax, (-0.5, 8), (0, 420),
        "Months saving", "Account balance ($)",
        "Li's savings account",
    )
    x = np.arange(0, 8)
    y = 125 + 45 * x
    ax.plot(x, y, "o-", color=GREEN, lw=2, ms=10)
    ax.axhline(360, color=RED, ls="--", label="Goal $360")
    ax.legend(fontsize=9)
    _save(fig, "practice_bank_graph.png", practice=True)


def practice_slope_line():
    fig, ax = plt.subplots(figsize=(5.5, 5))
    _axes_style_real(
        ax, (-0.5, 6), (-2, 14),
        "Hours worked", "Total pay ($)",
        "Part-time job — hours vs pay",
    )
    pts = [(0, 5), (1, 7), (2, 9), (3, 11)]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], c=PURPLE, s=100)
    x = np.linspace(-1, 5, 50)
    ax.plot(x, 2 * x + 5, "--", color=BLUE, alpha=0.4)
    _save(fig, "practice_slope_line.png", practice=True)


def practice_carey_graph():
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _axes_style_real(
        ax, (-0.5, 5), (-5, 35),
        "Hours worked", "Amount earned ($)",
        "Carey's weekend job — $9.75 per hour",
    )
    xs = [0, 1, 2, 3]
    ys = [0, 9.75, 19.5, 29.25]
    ax.plot(xs, ys, "o-", color=TEAL, lw=2, ms=10)
    _save(fig, "practice_carey_graph.png", practice=True)


def practice_coordinate_point():
    fig, ax = plt.subplots(figsize=(5, 5))
    _axes_style(ax, (-7, 7), (-7, 7), "Which quadrant is the point in?")
    _plot_point(ax, -3, 5, color=PURPLE, guides=False)
    _save(fig, "practice_coord_q2.png", practice=True)


def practice_parabola():
    fig, ax = plt.subplots(figsize=(5, 5))
    _axes_style(ax, (-4, 4), (-1, 8))
    x = np.linspace(-3, 3, 100)
    ax.plot(x, x ** 2, color=PURPLE, lw=2)
    _save(fig, "practice_parabola.png", practice=True)


def practice_linear_graph():
    fig, ax = plt.subplots(figsize=(5.5, 5))
    _axes_style_real(
        ax, (-0.5, 10), (-1, 12),
        "Cost of item ($)", "Change received ($)",
        "Paying with a $10 bill — Jaxon's change",
    )
    xs = list(range(10))
    ys = [10 - x for x in xs]
    ax.plot(xs, ys, "o-", color=ORANGE, lw=2)
    _save(fig, "practice_jaxon_graph.png", practice=True)


def practice_scatter_function():
    fig, ax = plt.subplots(figsize=(5, 5))
    _axes_style(ax, (-5, 5), (-5, 5))
    pts = [(-3, -1), (-2, 5), (4, 0), (7, -1)]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], c=GREEN, s=100)
    _save(fig, "practice_function_scatter.png", practice=True)


def practice_increasing_curve():
    fig, ax = plt.subplots(figsize=(5, 5))
    _axes_style(ax, (-1, 8), (-4, 6))
    x = np.linspace(0, 6, 50)
    ax.plot(x, np.sqrt(x), color=BLUE, lw=2)
    ax.plot(1, 1, "o", color=RED, ms=10, label="A")
    ax.plot(3, np.sqrt(3), "o", color=RED, ms=10, label="B")
    ax.legend()
    _save(fig, "practice_increasing_curve.png", practice=True)


LESSON_FUNCS = [
    activity_1_quadrants, activity_1_read_point,
    activity_2_vertical_line_test, activity_2_mapping_diagram, activity_2_function_equations,
    activity_3_segment_graph, activity_3_parabola_behavior, activity_3_distance_time,
    activity_4_unit_rate, activity_4_perimeter_equation, activity_4_jaxon_change,
    activity_5_table_to_graph, activity_5_evaluate_equation, activity_5_gas_tank,
    activity_6_movie_rentals, activity_6_bank_deposits, activity_6_inverse_lookup,
]

PRACTICE_FUNCS = [
    practice_coordinate_point, practice_parabola, practice_linear_graph,
    practice_scatter_function, practice_increasing_curve, practice_segment_graph,
    practice_coord_read_p, practice_coord_q2_ii, practice_coord_q4, practice_coord_xaxis,
    practice_vlt_remove, practice_vlt_scatter, practice_vlt_fail,
    practice_segment_cd, practice_segment_bc, practice_distance_time,
    practice_table_line, practice_tickets_graph, practice_perimeter_graph,
    practice_movie_compare, practice_gas_tank_graph, practice_bank_graph, practice_slope_line,
    practice_carey_graph,
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--practice-only", action="store_true")
    args = parser.parse_args()
    if not args.practice_only:
        print("Lesson diagrams:")
        for fn in LESSON_FUNCS:
            fn()
    print("Practice diagrams:")
    for fn in PRACTICE_FUNCS:
        fn()
    print("Done.")


if __name__ == "__main__":
    main()
