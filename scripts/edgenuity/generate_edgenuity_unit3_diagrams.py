"""
Generate matplotlib diagrams for Edgenuity Course 3 Unit 3 (lesson + practice).

Usage:
    python generate_edgenuity_unit3_diagrams.py
    python generate_edgenuity_unit3_diagrams.py --practice-only
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

OUT_DIR = os.path.join(str(Path(__file__).resolve().parents[2]), ArjunEdgenuityCourse3", "images", "unit_3"
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


def _plot_line(ax, slope, y_int, xlim, color=BLUE, lw=2.5, label=""):
    x = np.linspace(xlim[0], xlim[1], 100)
    y = slope * x + y_int
    ax.plot(x, y, color=color, lw=lw, label=label)


def _draw_rise_run(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color=BLUE, lw=2.5)
    ax.plot(x1, y1, "o", color=BLUE, ms=10)
    ax.plot(x2, y2, "o", color=BLUE, ms=10)
    ax.plot([x1, x1], [y1, y2], "--", color=GREEN, lw=2)
    ax.plot([x1, x2], [y2, y2], "--", color=ORANGE, lw=2)
    rise = y2 - y1
    run = x2 - x1
    ax.text(x1 - 0.4, (y1 + y2) / 2, f"rise\n{rise}", ha="right", fontsize=9, color=GREEN, fontweight="bold")
    ax.text((x1 + x2) / 2, y2 + 0.35, f"run {run}", ha="center", fontsize=9, color=ORANGE, fontweight="bold")
    if run != 0:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.8, f"slope = {rise}/{run}", fontsize=10, color=TEAL, fontweight="bold")


def _inez_phone_ax(ax, title="Inez's phone card balance"):
    _axes_style_real(ax, (-0.5, 18), (-50, 900), "Days", "Balance (¢)", title)
    d = np.linspace(0, 17, 50)
    bal = 850 - 50 * d
    ax.plot(d, bal, color=PURPLE, lw=2.5)
    ax.plot(0, 850, "o", color=RED, ms=10, zorder=5)
    ax.plot(17, 0, "o", color=RED, ms=10, zorder=5)
    ax.annotate("(0, 850)", (0, 850), xytext=(2, 750), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1))
    ax.annotate("(17, 0)", (17, 0), xytext=(12, 150), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1))
    ax.text(8, 500, "slope = −50 ¢/day", fontsize=10, color=TEAL, fontweight="bold")


# ── Activity 1 ──
def activity_1_slope_intercept_line():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-2, 8), (-2, 10), "Slope-intercept form: y = mx + b")
    _plot_line(ax, 1.5, 2, (-2, 8))
    ax.plot(0, 2, "o", color=RED, ms=12, zorder=5)
    ax.annotate("y-intercept\n(0, 2)", (0, 2), xytext=(1.5, 5), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    _draw_rise_run(ax, 2, 5, 4, 8)
    ax.text(5.5, 1, "y = 1.5x + 2", fontsize=11, color=TEAL, fontweight="bold")
    _save(fig, "activity_1_slope_intercept_line.png")


def activity_1_table_to_slope():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis("off")
    ax.set_title("Find slope from a table", fontsize=12, fontweight="bold", pad=12)
    rows = [("x", "y"), ("1", "3"), ("2", "7"), ("3", "11"), ("4", "15")]
    col_x = [0.3, 0.7]
    for i, (xv, yv) in enumerate(rows):
        y = 0.82 - i * 0.13
        weight = "bold" if i == 0 else "normal"
        ax.text(col_x[0], y, xv, ha="center", fontsize=11, fontweight=weight, transform=ax.transAxes)
        ax.text(col_x[1], y, yv, ha="center", fontsize=11, fontweight=weight, transform=ax.transAxes)
        if i == 0:
            ax.plot([0.12, 0.88], [y - 0.04, y - 0.04], color=GRID, lw=1.5, transform=ax.transAxes)
    ax.text(0.5, 0.22, "slope = (7 − 3) / (2 − 1) = 4/1 = 4", ha="center", fontsize=10,
            color=TEAL, fontweight="bold", transform=ax.transAxes)
    ax.text(0.5, 0.1, "Rate of change: +4 for each +1 in x", ha="center", fontsize=10,
            color=ORANGE, transform=ax.transAxes)
    rect = Rectangle((0.12, 0.18), 0.76, 0.72, fill=False, edgecolor=GRID, lw=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    _save(fig, "activity_1_table_to_slope.png")


# ── Activity 2 ──
def activity_2_two_points_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-4, 2), (-6, 2), "Slope from two points")
    pts = {"B": (-2, -2), "C": (-1, -4)}
    x = np.linspace(-4, 2, 50)
    ax.plot(x, -2 * x - 6, color=BLUE, lw=2.5, alpha=0.5)
    for label, (px, py) in pts.items():
        ax.plot(px, py, "o", color=RED, ms=12, zorder=5)
        ax.text(px + 0.25, py + 0.5, f"{label}({px}, {py})", fontsize=10, color=RED, fontweight="bold")
    _draw_rise_run(ax, -2, -2, -1, -4)
    ax.text(-3.5, 0.5, "slope = (−4 − (−2)) / (−1 − (−2)) = −2", fontsize=9, color=TEAL)
    _save(fig, "activity_2_two_points_graph.png")


def activity_2_equation_from_points():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-1, 4), (-1, 8), "Equation from two points")
    _plot_line(ax, -3, 6, (-1, 4))
    ax.plot(0, 6, "o", color=RED, ms=12, zorder=5)
    ax.plot(2, 0, "o", color=RED, ms=12, zorder=5)
    ax.annotate("(0, 6)", (0, 6), xytext=(0.8, 7), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.annotate("(2, 0)", (2, 0), xytext=(2.3, 2), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.text(2.5, 5, "slope = (0−6)/(2−0) = −3\ny = −3x + 6", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "activity_2_equation_from_points.png")


# ── Activity 3 ──
def activity_3_point_slope_convert():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.axis("off")
    ax.set_title("Convert point-slope form to slope-intercept form", fontsize=12, fontweight="bold", pad=12)
    steps = [
        ("Point-slope form", "y − 3 = 2(x − 1)", TEAL),
        ("Distribute 2", "y − 3 = 2x − 2", TEXT),
        ("Add 3 to both sides", "y = 2x + 1", GREEN),
        ("Slope-intercept form", "y = 2x + 1  →  m = 2, b = 1", PURPLE),
    ]
    for i, (label, eq, color) in enumerate(steps):
        y = 0.82 - i * 0.18
        ax.text(0.05, y, f"{i + 1}. {label}:", fontsize=10, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.55, y, eq, fontsize=11, color=color, transform=ax.transAxes)
    ax.text(0.5, 0.08, "Start with point (1, 3) and slope 2", ha="center", fontsize=10,
            color=ORANGE, transform=ax.transAxes)
    rect = Rectangle((0.03, 0.05), 0.94, 0.88, fill=False, edgecolor=GRID, lw=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    _save(fig, "activity_3_point_slope_convert.png")


def activity_3_line_through_point():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-1, 4), (-2, 14), "Line with slope 4 through (1, 6)")
    _plot_line(ax, 4, 2, (-1, 4))
    ax.plot(1, 6, "o", color=RED, ms=12, zorder=5)
    ax.annotate("(1, 6)", (1, 6), xytext=(1.8, 10), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    _draw_rise_run(ax, 1, 6, 2, 10)
    ax.text(2.5, 2, "y − 6 = 4(x − 1)\ny = 4x + 2", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "activity_3_line_through_point.png")


# ── Activity 4 ──
def activity_4_standard_to_slope():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.axis("off")
    ax.set_title("Convert standard form to slope-intercept form", fontsize=12, fontweight="bold", pad=12)
    steps = [
        ("Standard form", "15x − 4y = −2", TEAL),
        ("Subtract 15x", "−4y = −15x − 2", TEXT),
        ("Divide by −4", "y = (15/4)x + 1/2", GREEN),
        ("Slope-intercept", "m = 15/4,  b = 1/2", PURPLE),
    ]
    for i, (label, eq, color) in enumerate(steps):
        y = 0.82 - i * 0.18
        ax.text(0.05, y, f"{i + 1}. {label}:", fontsize=10, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.55, y, eq, fontsize=11, color=color, transform=ax.transAxes)
    rect = Rectangle((0.03, 0.12), 0.94, 0.78, fill=False, edgecolor=GRID, lw=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    _save(fig, "activity_4_standard_to_slope.png")


def activity_4_jill_error_steps():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.axis("off")
    ax.set_title("Jill's work — find the error", fontsize=12, fontweight="bold", pad=12)
    steps = [
        ("Start", "3x + 6y = 12", TEXT),
        ("Step 1 ✓", "6y = −3x + 12", GREEN),
        ("Step 2 ✗", "y = −3x + 12", RED),
        ("Correct", "y = −(1/2)x + 2", TEAL),
    ]
    for i, (label, eq, color) in enumerate(steps):
        y = 0.82 - i * 0.16
        ax.text(0.05, y, label + ":", fontsize=10, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.35, y, eq, fontsize=11, color=color, transform=ax.transAxes)
    ax.annotate(
        "Forgot to divide\nevery term by 6!",
        xy=(0.35, 0.5), xycoords="axes fraction",
        xytext=(0.65, 0.55), textcoords="axes fraction",
        fontsize=10, color=RED, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.5),
    )
    rect = Rectangle((0.03, 0.12), 0.94, 0.78, fill=False, edgecolor=GRID, lw=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    _save(fig, "activity_4_jill_error_steps.png")


# ── Activity 5 ──
def activity_5_inez_phone_card():
    fig, ax = plt.subplots(figsize=(6, 4))
    _inez_phone_ax(ax)
    _save(fig, "activity_5_inez_phone_card.png")


def activity_5_washing_machine_model():
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _axes_style_real(
        ax, (-0.5, 6), (0, 300),
        "Years owned", "Repair cost ($)",
        "Washing machine repair costs",
    )
    yrs = np.linspace(0, 5, 50)
    cost = 45 * yrs + 35
    ax.plot(yrs, cost, color=TEAL, lw=2.5)
    ax.plot(0, 35, "o", color=RED, ms=10, zorder=5)
    ax.annotate("$35 base", (0, 35), xytext=(1.2, 80), fontsize=9, color=TEAL,
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1))
    ax.text(3, 220, "+$45/year\ny = 45x + 35", fontsize=10, color=PURPLE, fontweight="bold")
    _save(fig, "activity_5_washing_machine_model.png")


# ── Activity 6 ──
def activity_6_compare_two_lines():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-1, 6), (-2, 12), "Compare two linear models")
    x = np.linspace(-1, 6, 50)
    ax.plot(x, 2 * x + 1, color=BLUE, lw=2.5, label="Line A: slope 2")
    ax.plot(x, 0.5 * x + 4, color=ORANGE, lw=2.5, label="Line B: slope 0.5")
    ax.plot(0, 1, "o", color=BLUE, ms=8)
    ax.plot(0, 4, "o", color=ORANGE, ms=8)
    ax.text(4.5, 10, "Steeper slope\n= faster rate", fontsize=9, color=TEAL)
    ax.legend(fontsize=9)
    _save(fig, "activity_6_compare_two_lines.png")


def activity_6_same_y_intercept():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-4, 6), (-4, 6), "Same y-intercept?")
    x = np.linspace(-4, 6, 50)
    ax.plot(x, 0.5 * x - 1, color=BLUE, lw=2.5, label="y = ½x − 1")
    ax.plot(x, -x + 2, color=ORANGE, lw=2.5, label="y = −x + 2 (counterexample)")
    ax.plot(0, -1, "o", color=BLUE, ms=10)
    ax.plot(0, 2, "o", color=ORANGE, ms=10)
    ax.text(3, -3, "y-intercepts:\n(0, −1) vs (0, 2)", fontsize=10, color=RED, fontweight="bold")
    ax.legend(fontsize=9)
    _save(fig, "activity_6_same_y_intercept.png")


# ── Practice images ──
def practice_u3_bc_points():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-4, 2), (-7, 2), "Points on a line — find slope from B and C")
    pts = {"A": (-3, 0), "B": (-2, -2), "C": (-1, -4), "D": (0, -6)}
    x = np.linspace(-4, 2, 50)
    ax.plot(x, -2 * x - 6, color=BLUE, lw=2, alpha=0.4)
    for label, (px, py) in pts.items():
        color = RED if label in ("B", "C") else TEXT
        size = 12 if label in ("B", "C") else 8
        ax.plot(px, py, "o", color=color, ms=size, zorder=5)
        offset = 0.4 if label in ("B", "C") else 0.3
        ax.text(px + 0.2, py + offset, f"{label}({px}, {py})", fontsize=9, color=color,
                fontweight="bold" if label in ("B", "C") else "normal")
    ax.plot([-2, -1], [-2, -4], color=RED, lw=2.5, zorder=4)
    ax.text(-3.5, -5.5, "Use B and C to find slope", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "practice_u3_bc_points.png", practice=True)


def practice_u3_two_points_line():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-1, 4), (-1, 8), "Line through (0, 6) and (2, 0)")
    _plot_line(ax, -3, 6, (-1, 4))
    ax.plot(0, 6, "o", color=RED, ms=12, zorder=5)
    ax.plot(2, 0, "o", color=RED, ms=12, zorder=5)
    ax.annotate("(0, 6)", (0, 6), xytext=(0.8, 7), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.annotate("(2, 0)", (2, 0), xytext=(2.3, 2), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.text(2.5, 5, "y = −3x + 6", fontsize=11, color=TEAL, fontweight="bold")
    _save(fig, "practice_u3_two_points_line.png", practice=True)


def practice_u3_inez_phone():
    fig, ax = plt.subplots(figsize=(6, 4))
    _inez_phone_ax(ax, "Inez's prepaid phone card")
    _save(fig, "practice_u3_inez_phone.png", practice=True)


def practice_u3_yint_match_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (0, 8), (-1, 12), "Which y-intercept matches this line?")
    pts = [(3, 4), (4, 2), (5, 0)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, "o-", color=BLUE, lw=2.5, ms=10)
    x_ext = np.linspace(0, 8, 50)
    ax.plot(x_ext, -2 * x_ext + 10, "--", color=TEAL, lw=1.5, alpha=0.6)
    ax.plot(0, 10, "o", color=RED, ms=12, zorder=5)
    ax.annotate("y-int = 10", (0, 10), xytext=(1.5, 8), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    for px, py in pts:
        ax.text(px + 0.15, py + 0.4, f"({px}, {py})", fontsize=9, color=TEXT)
    _save(fig, "practice_u3_yint_match_graph.png", practice=True)


def practice_u3_jeremy_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-4, 6), (-4, 4), "Jeremy's line")
    _plot_line(ax, 0.5, -1, (-4, 6))
    ax.plot(0, -1, "o", color=RED, ms=10)
    ax.plot(4, 1, "o", color=RED, ms=10)
    ax.text(3, -3, "y = ½x − 1\nslope = ½, y-int = −1", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "practice_u3_jeremy_graph.png", practice=True)


def practice_u3_compare_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-1, 4), (-1, 10), "Compare the two lines")
    x = np.linspace(-1, 4, 50)
    ax.plot(x, 3 * x + 1, color=BLUE, lw=2.5, label="Through (0,1) and (1,4)")
    ax.plot(x, 2 * x + 2, color=ORANGE, lw=2.5, label="y = 2x + 2")
    ax.plot(0, 1, "o", color=BLUE, ms=10)
    ax.plot(1, 4, "o", color=BLUE, ms=10)
    ax.plot(0, 2, "o", color=ORANGE, ms=10)
    ax.legend(fontsize=9)
    ax.text(2, 8, "Different slopes\nand y-intercepts", fontsize=9, color=TEAL)
    _save(fig, "practice_u3_compare_graph.png", practice=True)


def practice_u3_slope_from_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-1, 5), (-1, 5), "Find the slope from the graph")
    _draw_rise_run(ax, 0, 3, 4, 0)
    ax.text(4.5, 3.5, "slope = −3/4", fontsize=11, color=TEAL, fontweight="bold")
    _save(fig, "practice_u3_slope_from_graph.png", practice=True)


def practice_u3_graph_fractions():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-1, 5), (-4, 2), "Line with fractional slope")
    _plot_line(ax, 2 / 3, -2, (-1, 5))
    ax.plot(0, -2, "o", color=RED, ms=10)
    ax.plot(3, 0, "o", color=RED, ms=10)
    ax.annotate("y-int = −2", (0, -2), xytext=(1, -3), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.annotate("x-int = 3", (3, 0), xytext=(3.5, 1), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="->", color=ORANGE))
    ax.text(3.5, -3, "slope = 2/3", fontsize=11, color=TEAL, fontweight="bold")
    _save(fig, "practice_u3_graph_fractions.png", practice=True)


def practice_u3_graph_yint12():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-5, 0), (-6, 14), "Find slope and y-intercept")
    pts = [(-4, -4), (-3, 0), (-2, 4)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, "o-", color=BLUE, lw=2.5, ms=10)
    x_ext = np.linspace(-5, 0, 50)
    ax.plot(x_ext, 4 * x_ext + 12, "--", color=TEAL, lw=1.5, alpha=0.6)
    ax.plot(0, 12, "o", color=RED, ms=12, zorder=5)
    ax.annotate("y-int = 12", (0, 12), xytext=(-4, 10), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    for px, py in pts:
        ax.text(px + 0.15, py + 0.5, f"({px}, {py})", fontsize=9, color=TEXT)
    ax.text(-4.5, -5, "slope = 4", fontsize=11, color=TEAL, fontweight="bold")
    _save(fig, "practice_u3_graph_yint12.png", practice=True)


LESSON_FUNCS = [
    activity_1_slope_intercept_line, activity_1_table_to_slope,
    activity_2_two_points_graph, activity_2_equation_from_points,
    activity_3_point_slope_convert, activity_3_line_through_point,
    activity_4_standard_to_slope, activity_4_jill_error_steps,
    activity_5_inez_phone_card, activity_5_washing_machine_model,
    activity_6_compare_two_lines, activity_6_same_y_intercept,
]

PRACTICE_FUNCS = [
    practice_u3_bc_points, practice_u3_two_points_line, practice_u3_inez_phone,
    practice_u3_yint_match_graph, practice_u3_jeremy_graph, practice_u3_compare_graph,
    practice_u3_slope_from_graph, practice_u3_graph_fractions, practice_u3_graph_yint12,
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
