"""
Generate matplotlib diagrams for Edgenuity Course 3 Unit 6 (lesson + practice).

Unit 6: Systems of Linear Equations

Usage:
    python generate_edgenuity_unit6_diagrams.py
    python generate_edgenuity_unit6_diagrams.py --practice-only
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunEdgenuityCourse3", "images", "unit_6")
PRACTICE_DIR = os.path.join(OUT_DIR, "practice")
DPI = 150
BG = "#ffffff"
BLUE = "#3b82f6"
ORANGE = "#f97316"
GREEN = "#22c55e"
RED = "#ef4444"
TEAL = "#0d9488"
PURPLE = "#8b5cf6"
YELLOW = "#eab308"
TEXT = "#1f2937"
GRID = "#e5e7eb"


def _save(fig, name: str, practice: bool = False) -> None:
    base = PRACTICE_DIR if practice else OUT_DIR
    os.makedirs(base, exist_ok=True)
    path = os.path.join(base, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"  saved {path}")


def _off(ax):
    ax.set_facecolor(BG)
    ax.axis("off")


def _axes_style(ax, xlim, ylim, title: str = ""):
    """Standard coordinate grid with x/y axes."""
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
    """Coordinate grid with real-world axis labels."""
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


def _plot_line(ax, slope, y_int, xlim, color=BLUE, lw=2.5, label="", ls="-"):
    """Plot y = mx + b over xlim."""
    x = np.linspace(xlim[0], xlim[1], 100)
    y = slope * x + y_int
    ax.plot(x, y, color=color, lw=lw, ls=ls, label=label)


def _plot_standard(ax, a, b, c, xlim, color=BLUE, lw=2.5, label=""):
    """Plot ax + by = c (assumes b != 0)."""
    slope = -a / b
    y_int = c / b
    _plot_line(ax, slope, y_int, xlim, color=color, lw=lw, label=label or f"{a:g}x + {b:g}y = {c:g}")


def _mark_point(ax, x, y, label="", color=RED, offset=(0.8, 0.8)):
    ax.plot(x, y, "o", color=color, ms=12, zorder=5)
    if label:
        ax.annotate(
            label, (x, y), xytext=(x + offset[0], y + offset[1]),
            fontsize=10, color=color, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=color, lw=1),
        )


def _draw_table(ax, headers, rows, x=0.55, y_top=0.85, col_w=0.12, row_h=0.1):
    """Draw a small values table in axes-fraction coordinates."""
    n_cols = len(headers)
    table_w = col_w * n_cols
    table_h = row_h * (len(rows) + 1)
    rect = Rectangle(
        (x, y_top - table_h), table_w, table_h,
        fill=False, edgecolor=GRID, lw=1.5, transform=ax.transAxes,
    )
    ax.add_patch(rect)
    for j, h in enumerate(headers):
        ax.text(
            x + col_w * j + col_w / 2, y_top - row_h * 0.55, h,
            ha="center", va="center", fontsize=10, fontweight="bold",
            transform=ax.transAxes,
        )
    ax.plot(
        [x, x + table_w], [y_top - row_h, y_top - row_h],
        color=GRID, lw=1.5, transform=ax.transAxes,
    )
    for i, row in enumerate(rows):
        y = y_top - row_h * (i + 1.55)
        for j, val in enumerate(row):
            ax.text(
                x + col_w * j + col_w / 2, y, val,
                ha="center", va="center", fontsize=10, transform=ax.transAxes,
            )


def _equation_steps(ax, steps, y=0.45, box_h=0.4):
    """Draw horizontal flow of equation steps."""
    n = len(steps)
    for i, (label, eq, color) in enumerate(steps):
        xc = 0.05 + i * (0.9 / max(n - 1, 1)) if n > 1 else 0.5
        ax.add_patch(FancyBboxPatch(
            (xc - 0.11, y), 0.22, box_h, boxstyle="round,pad=0.02",
            facecolor=color, alpha=0.12, edgecolor=color, lw=1.5, transform=ax.transAxes,
        ))
        ax.text(xc, y + box_h * 0.72, label, ha="center", fontsize=8, color=TEAL, transform=ax.transAxes)
        ax.text(xc, y + box_h * 0.28, eq, ha="center", fontsize=9, fontweight="bold",
                color=TEXT, transform=ax.transAxes)
        if i < n - 1:
            nx = 0.05 + (i + 1) * (0.9 / (n - 1))
            ax.annotate("", xy=(nx - 0.12, y + box_h * 0.5), xytext=(xc + 0.12, y + box_h * 0.5),
                        xycoords="axes fraction", textcoords="axes fraction",
                        arrowprops=dict(arrowstyle="->", color=GRID, lw=1.5))


# ── Activity 1 ──
def activity_1_system_intersection():
    fig, ax = plt.subplots(figsize=(6, 5))
    xlim = (-2, 6)
    ylim = (-6, 4)
    _axes_style(ax, xlim, ylim, "System solution: intersection point")
    _plot_line(ax, 1, -4, xlim, color=BLUE, lw=2.5, label="y = x − 4")
    _plot_line(ax, -2, 2, xlim, color=ORANGE, lw=2.5, label="y = −2x + 2")
    _mark_point(ax, 2, -2, "Solution\n(2, −2)", offset=(0.6, 1.2))
    ax.text(4.5, -5, "Lines cross at one point\n→ one solution", fontsize=9, color=TEAL, fontweight="bold")
    ax.legend(fontsize=9, loc="lower left")
    _save(fig, "activity_1_system_intersection.png")


def activity_1_graph_table_system():
    fig, ax = plt.subplots(figsize=(7, 5))
    xlim = (-2, 8)
    ylim = (-5, 5)
    _axes_style(ax, xlim, ylim, "Graph one equation, use a table for the other")
    _plot_line(ax, 0.5, -3, xlim, color=BLUE, lw=2.5, label="y = ½x − 3")
    rows = [("-2", "2"), ("0", "0"), ("2", "−2"), ("4", "−4")]
    _draw_table(ax, ["x", "y"], rows, x=0.02, y_top=0.98, col_w=0.08, row_h=0.08)
    ax.text(0.02, 0.52, "y = −x", fontsize=10, color=ORANGE, fontweight="bold", transform=ax.transAxes)
    ax.text(0.02, 0.46, "(from table)", fontsize=8, color=TEXT, transform=ax.transAxes)
    for xv, yv in rows:
        x, y = float(xv), float(yv.replace("−", "-"))
        ax.plot(x, y, "o", color=ORANGE, ms=8, zorder=4)
    _plot_line(ax, -1, 0, xlim, color=ORANGE, lw=2, ls="--", label="y = −x")
    _mark_point(ax, 2, -2, "(2, −2)", offset=(0.5, 0.8))
    ax.legend(fontsize=9, loc="lower right")
    _save(fig, "activity_1_graph_table_system.png")


# ── Activity 2 ──
def activity_2_convert_to_slope_intercept():
    fig, ax = plt.subplots(figsize=(8, 3.2))
    _off(ax)
    ax.set_title("Convert standard form to slope-intercept form", fontsize=12, fontweight="bold", pad=10)
    steps = [
        ("Start", "5x − 2y = 10", BLUE),
        ("Subtract 5x", "−2y = 10 − 5x", TEAL),
        ("Divide by −2", "y = −5 + (5/2)x", GREEN),
        ("Rewrite", "y = (5/2)x − 5", PURPLE),
    ]
    _equation_steps(ax, steps, y=0.45, box_h=0.42)
    ax.text(0.5, 0.12, "m = 5/2,  b = −5", ha="center", fontsize=10, color=TEAL,
            fontweight="bold", transform=ax.transAxes)
    _save(fig, "activity_2_convert_to_slope_intercept.png")


def activity_2_slope_intercept_form():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    _off(ax)
    ax.set_title("Forms of linear equations", fontsize=12, fontweight="bold", pad=10)
    forms = [
        ("Slope-intercept", "y = mx + b", "m = slope,  b = y-intercept", BLUE),
        ("Standard", "Ax + By = C", "A, B, C are integers", TEAL),
        ("Point-slope", "y − y₁ = m(x − x₁)", "uses a point and slope", GREEN),
    ]
    for i, (name, eq, note, color) in enumerate(forms):
        y = 0.78 - i * 0.28
        ax.add_patch(FancyBboxPatch(
            (0.08, y - 0.1), 0.84, 0.2, boxstyle="round,pad=0.02",
            facecolor=color, alpha=0.1, edgecolor=color, lw=2, transform=ax.transAxes,
        ))
        ax.text(0.12, y + 0.02, name + ":", ha="left", fontsize=10, fontweight="bold",
                color=color, transform=ax.transAxes)
        ax.text(0.42, y + 0.02, eq, ha="left", fontsize=12, fontweight="bold",
                transform=ax.transAxes)
        ax.text(0.42, y - 0.06, note, ha="left", fontsize=9, color=TEXT, transform=ax.transAxes)
    ax.text(0.5, 0.06, "Convert between forms to graph or solve systems", ha="center",
            fontsize=9, color=TEXT, transform=ax.transAxes)
    _save(fig, "activity_2_slope_intercept_form.png")


# ── Activity 3 ──
def activity_3_word_to_equations():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    _off(ax)
    ax.set_title("Word problem → system of equations", fontsize=12, fontweight="bold", pad=10)
    story = (
        "At a school carnival, adult tickets cost $4 and\n"
        "child tickets cost $2. 120 tickets were sold\n"
        "for a total of $360."
    )
    ax.text(0.5, 0.82, story, ha="center", fontsize=10, color=TEXT,
            bbox=dict(boxstyle="round", facecolor="#eff6ff", edgecolor=BLUE, pad=0.6),
            transform=ax.transAxes)
    ax.annotate("", xy=(0.5, 0.58), xytext=(0.5, 0.68),
                xycoords="axes fraction", textcoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
    ax.text(0.5, 0.52, "Let a = adult tickets,  c = child tickets", ha="center",
            fontsize=10, color=TEAL, fontweight="bold", transform=ax.transAxes)
    ax.text(0.5, 0.38, "a + c = 120", ha="center", fontsize=13, fontweight="bold",
            color=BLUE, bbox=dict(boxstyle="round", facecolor="#eff6ff", edgecolor=BLUE),
            transform=ax.transAxes)
    ax.text(0.5, 0.22, "4a + 2c = 360", ha="center", fontsize=13, fontweight="bold",
            color=ORANGE, bbox=dict(boxstyle="round", facecolor="#fff7ed", edgecolor=ORANGE),
            transform=ax.transAxes)
    ax.text(0.5, 0.06, "Two equations, two unknowns → solve the system", ha="center",
            fontsize=9, color=TEXT, transform=ax.transAxes)
    _save(fig, "activity_3_word_to_equations.png")


def activity_3_real_world_system():
    fig, ax = plt.subplots(figsize=(6.5, 5))
    xlim = (0, 16)
    ylim = (0, 14)
    _axes_style_real(ax, xlim, ylim, "Tickets", "Total cost ($)", "Movie plans: flat fee vs per-ticket")
    tickets = np.linspace(0, 16, 100)
    ax.plot(tickets, np.full_like(tickets, 10), color=BLUE, lw=2.5, label="Plan A: $10 flat fee")
    ax.plot(tickets, (4 / 5) * tickets, color=ORANGE, lw=2.5, label="Plan B: $4/5 per ticket")
    _mark_point(ax, 12.5, 10, "Break-even\n(12.5, $10)", color=RED, offset=(1.5, 1.5))
    ax.text(1, 12, "Plan A always $10", fontsize=9, color=BLUE, fontweight="bold")
    ax.text(8, 4, "slope = 4/5", fontsize=9, color=ORANGE, fontweight="bold")
    ax.legend(fontsize=9, loc="upper left")
    _save(fig, "activity_3_real_world_system.png")


# ── Activity 4 ──
def activity_4_parallel_lines():
    fig, ax = plt.subplots(figsize=(6, 5))
    xlim = (-3, 5)
    ylim = (-10, 12)
    _axes_style(ax, xlim, ylim, "Parallel lines — no solution")
    _plot_line(ax, -3, 5, xlim, color=BLUE, lw=2.5, label="y = −3x + 5")
    _plot_line(ax, -3, -6, xlim, color=ORANGE, lw=2.5, label="y = −3x − 6")
    ax.text(3, 8, "Same slope\nDifferent y-intercepts", fontsize=9, color=RED, fontweight="bold")
    ax.text(-2, -8, "Never intersect\n→ no solution", fontsize=9, color=TEAL, fontweight="bold")
    ax.legend(fontsize=9, loc="lower right")
    _save(fig, "activity_4_parallel_lines.png")


def activity_4_infinite_solutions():
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    xlim = (-4, 4)
    ylim = (-8, 10)
    _axes_style(ax, xlim, ylim, "Equivalent equations — infinitely many solutions")
    _plot_line(ax, -3, -6, xlim, color=BLUE, lw=3, label="y = −3x − 6")
    eqs = ["3x + y = −6", "6x + 2y = −12", "y = −3x − 6"]
    for i, eq in enumerate(eqs):
        ax.text(-3.8, 8 - i * 1.2, eq, fontsize=10, color=[TEAL, GREEN, PURPLE][i], fontweight="bold")
    ax.text(1, 4, "Same line →\ninfinite solutions", fontsize=10, color=RED, fontweight="bold",
            bbox=dict(boxstyle="round", facecolor="#fef2f2", edgecolor=RED))
    ax.legend(fontsize=9, loc="lower right")
    _save(fig, "activity_4_infinite_solutions.png")


# ── Activity 5 ──
def activity_5_four_lines_graph():
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    xlim = (-4, 4)
    ylim = (-6, 8)
    _axes_style(ax, xlim, ylim, "Match each system to its graph")
    lines = [
        (2, -1, -2, BLUE, "2x − y = −2"),
        (3, 2, 5, ORANGE, "3x + 2y = 5"),
        (1, 1, 1, GREEN, "x + y = 1"),
        (1, -1, 3, PURPLE, "x − y = 3"),
    ]
    for a, b, c, color, label in lines:
        _plot_standard(ax, a, b, c, xlim, color=color, lw=2.5, label=label)
    ax.legend(fontsize=8, loc="upper left")
    _save(fig, "activity_5_four_lines_graph.png")


def activity_5_match_system_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    xlim = (-5, 5)
    ylim = (-8, 4)
    _axes_style(ax, xlim, ylim, "System: x − 2y = 4  and  2x + y = −4")
    _plot_standard(ax, 1, -2, 4, xlim, color=BLUE, lw=2.5, label="x − 2y = 4")
    _plot_standard(ax, 2, 1, -4, xlim, color=ORANGE, lw=2.5, label="2x + y = −4")
    _mark_point(ax, -0.8, -2.4, "(−4/5, −12/5)", offset=(1.0, 1.5))
    ax.legend(fontsize=9, loc="lower right")
    _save(fig, "activity_5_match_system_graph.png")


# ── Activity 6 ──
def activity_6_substitution_check():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    _off(ax)
    ax.set_title("Check a solution: substitute (2, −2)", fontsize=12, fontweight="bold", pad=10)
    ax.text(0.5, 0.88, "Is (2, −2) a solution to the system?", ha="center", fontsize=11,
            fontweight="bold", transform=ax.transAxes)
    checks = [
        ("Eq 1: y = x − 4", "−2 = 2 − 4  →  −2 = −2  ✓", GREEN),
        ("Eq 2: 2x + y = 2", "2(2) + (−2) = 2  →  2 = 2  ✓", GREEN),
    ]
    for i, (label, work, color) in enumerate(checks):
        y = 0.62 - i * 0.28
        ax.add_patch(FancyBboxPatch(
            (0.08, y - 0.1), 0.84, 0.18, boxstyle="round,pad=0.02",
            facecolor=color, alpha=0.1, edgecolor=color, lw=2, transform=ax.transAxes,
        ))
        ax.text(0.12, y + 0.02, label, ha="left", fontsize=10, fontweight="bold",
                color=color, transform=ax.transAxes)
        ax.text(0.12, y - 0.05, work, ha="left", fontsize=10, transform=ax.transAxes)
    ax.text(0.5, 0.12, "(2, −2) satisfies BOTH equations → it is the solution", ha="center",
            fontsize=10, color=TEAL, fontweight="bold", transform=ax.transAxes)
    _save(fig, "activity_6_substitution_check.png")


def activity_6_verify_solution():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    _off(ax)
    ax.set_title("Dimitri uses substitution to verify a solution", fontsize=12, fontweight="bold", pad=10)
    steps = [
        ("Given system", "y = 3x − 8\nx + y = −4", BLUE),
        ("Substitute", "x + (3x − 8) = −4", TEAL),
        ("Solve for x", "4x − 8 = −4  →  x = 1", GREEN),
        ("Find y", "y = 3(1) − 8 = −5", ORANGE),
        ("Verify", "(1, −5) in both equations ✓", PURPLE),
    ]
    for i, (label, eq, color) in enumerate(steps):
        x = 0.9 + i * 1.75
        ax.add_patch(FancyBboxPatch(
            (x - 0.75, 0.55), 1.5, 1.8, boxstyle="round,pad=0.04",
            facecolor=color, alpha=0.1, edgecolor=color, lw=2,
        ))
        ax.text(x, 2.05, label, ha="center", fontsize=9, color=TEAL, fontweight="bold")
        ax.text(x, 1.35, eq, ha="center", fontsize=9, fontweight="bold")
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 0.85, 1.45), xytext=(x + 0.55, 1.45),
                        arrowprops=dict(arrowstyle="->", color=GRID, lw=1.5))
    ax.text(5, 0.35, "Substitution: replace y with 3x − 8 in the second equation", ha="center",
            fontsize=9, color=TEXT)
    _save(fig, "activity_6_verify_solution.png")


# ── Practice images ──
def practice_u6_graph_table():
    fig, ax = plt.subplots(figsize=(7, 5))
    xlim = (-2, 8)
    ylim = (-5, 5)
    _axes_style(ax, xlim, ylim, "Practice: graph y = ½x − 3")
    _plot_line(ax, 0.5, -3, xlim, color=BLUE, lw=2.5, label="y = ½x − 3")
    rows = [("0", "−3"), ("2", "−2"), ("4", "−1"), ("6", "0")]
    _draw_table(ax, ["x", "y"], rows, x=0.02, y_top=0.98, col_w=0.08, row_h=0.08)
    ax.plot(0, -3, "o", color=RED, ms=10, zorder=5)
    ax.annotate("(0, −3)", (0, -3), xytext=(1.5, -4), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.legend(fontsize=9, loc="lower right")
    _save(fig, "practice_u6_graph_table.png", practice=True)


def practice_u6_intersection():
    fig, ax = plt.subplots(figsize=(6, 5))
    xlim = (-8, 4)
    ylim = (-4, 8)
    _axes_style(ax, xlim, ylim, "Practice: find the intersection")
    _plot_line(ax, 1, 6, xlim, color=BLUE, lw=2.5, label="y = x + 6")
    _plot_line(ax, -2, -9, xlim, color=ORANGE, lw=2.5, label="y = −2x − 9")
    _mark_point(ax, -5, 1, "Solution\n(−5, 1)", offset=(0.8, 1.0))
    ax.legend(fontsize=9, loc="lower right")
    _save(fig, "practice_u6_intersection.png", practice=True)


def practice_u6_parallel():
    fig, ax = plt.subplots(figsize=(6, 5))
    xlim = (-3, 5)
    ylim = (-8, 10)
    _axes_style(ax, xlim, ylim, "Practice: parallel lines")
    _plot_line(ax, 2, 1, xlim, color=BLUE, lw=2.5, label="y = 2x + 1")
    _plot_line(ax, 2, -5, xlim, color=ORANGE, lw=2.5, label="y = 2x − 5")
    ax.text(2, 7, "Same slope (m = 2)\n→ no solution", fontsize=9, color=RED, fontweight="bold")
    ax.legend(fontsize=9, loc="lower right")
    _save(fig, "practice_u6_parallel.png", practice=True)


def practice_u6_movie():
    fig, ax = plt.subplots(figsize=(6.5, 5))
    xlim = (0, 20)
    ylim = (0, 18)
    _axes_style_real(ax, xlim, ylim, "Tickets", "Cost ($)", "Practice: Kedwin's movie plans")
    tickets = np.linspace(0, 20, 100)
    ax.plot(tickets, np.full_like(tickets, 8), color=BLUE, lw=2.5, label="Kedwin: $8 membership")
    ax.plot(tickets, 0.75 * tickets + 2, color=ORANGE, lw=2.5, label="Pay-as-you-go: $0.75/ticket + $2")
    _mark_point(ax, 8, 8, "(8, $8)", color=RED, offset=(2, 1.5))
    ax.legend(fontsize=9, loc="upper left")
    _save(fig, "practice_u6_movie.png", practice=True)


def practice_u6_fertilizer():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    _off(ax)
    ax.set_title("Practice: Adam's fertilizer mix", fontsize=11, fontweight="bold", pad=10)
    story = (
        "Adam needs 20 lb of fertilizer that is 30% nitrogen.\n"
        "He mixes Brand A (20% nitrogen) with Brand B (50% nitrogen)."
    )
    ax.text(0.5, 0.82, story, ha="center", fontsize=10, color=TEXT,
            bbox=dict(boxstyle="round", facecolor="#f0fdf4", edgecolor=GREEN, pad=0.6),
            transform=ax.transAxes)
    ax.text(0.5, 0.58, "Let a = pounds of Brand A,  b = pounds of Brand B", ha="center",
            fontsize=10, color=TEAL, fontweight="bold", transform=ax.transAxes)
    ax.text(0.5, 0.42, "a + b = 20", ha="center", fontsize=13, fontweight="bold",
            color=BLUE, transform=ax.transAxes)
    ax.text(0.5, 0.28, "0.20a + 0.50b = 0.30(20)", ha="center", fontsize=13, fontweight="bold",
            color=ORANGE, transform=ax.transAxes)
    ax.text(0.5, 0.12, "Simplify: 0.20a + 0.50b = 6", ha="center", fontsize=10,
            color=TEAL, transform=ax.transAxes)
    _save(fig, "practice_u6_fertilizer.png", practice=True)


def practice_u6_four_lines():
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    xlim = (-5, 5)
    ylim = (-6, 8)
    _axes_style(ax, xlim, ylim, "Practice: identify the correct system")
    lines = [
        (-1, 2, 4, BLUE, "−x + 2y = 4"),
        (2, 1, -2, ORANGE, "2x + y = −2"),
        (1, -1, 2, GREEN, "x − y = 2"),
        (3, 2, 6, PURPLE, "3x + 2y = 6"),
    ]
    for a, b, c, color, label in lines:
        _plot_standard(ax, a, b, c, xlim, color=color, lw=2.5, label=label)
    ax.legend(fontsize=8, loc="upper left")
    _save(fig, "practice_u6_four_lines.png", practice=True)


def practice_u6_system_neg():
    fig, ax = plt.subplots(figsize=(6, 5))
    xlim = (-8, 4)
    ylim = (-8, 8)
    _axes_style(ax, xlim, ylim, "Practice: y = 2x + 5  and  y = −3x − 15")
    _plot_line(ax, 2, 5, xlim, color=BLUE, lw=2.5, label="y = 2x + 5")
    _plot_line(ax, -3, -15, xlim, color=ORANGE, lw=2.5, label="y = −3x − 15")
    _mark_point(ax, -4, -3, "Solution\n(−4, −3)", offset=(0.8, 1.0))
    ax.legend(fontsize=9, loc="upper right")
    _save(fig, "practice_u6_system_neg.png", practice=True)


def practice_u6_word_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    xlim = (-1, 5)
    ylim = (-1, 10)
    _axes_style(ax, xlim, ylim, "Practice: two phone plans")
    _plot_line(ax, 3, 0, xlim, color=BLUE, lw=2.5, label="Plan A: y = 3x")
    _plot_line(ax, 1, 4, xlim, color=ORANGE, lw=2.5, label="Plan B: y = x + 4")
    _mark_point(ax, 2, 6, "Same cost at\n(2, 6)", offset=(0.6, 1.2))
    ax.text(3.5, 2, "x = minutes\ny = cost ($)", fontsize=9, color=TEXT)
    ax.legend(fontsize=9, loc="lower right")
    _save(fig, "practice_u6_word_graph.png", practice=True)


LESSON_FUNCS = [
    activity_1_system_intersection, activity_1_graph_table_system,
    activity_2_convert_to_slope_intercept, activity_2_slope_intercept_form,
    activity_3_word_to_equations, activity_3_real_world_system,
    activity_4_parallel_lines, activity_4_infinite_solutions,
    activity_5_four_lines_graph, activity_5_match_system_graph,
    activity_6_substitution_check, activity_6_verify_solution,
]

PRACTICE_FUNCS = [
    practice_u6_graph_table, practice_u6_intersection, practice_u6_parallel,
    practice_u6_movie, practice_u6_fertilizer, practice_u6_four_lines,
    practice_u6_system_neg, practice_u6_word_graph,
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
