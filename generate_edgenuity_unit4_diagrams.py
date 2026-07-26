"""
Generate matplotlib diagrams for Edgenuity Course 3 Unit 4 (lesson + practice).

Usage:
    python generate_edgenuity_unit4_diagrams.py
    python generate_edgenuity_unit4_diagrams.py --practice-only
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunEdgenuityCourse3", "images", "unit_4")
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


def _scatter_style(ax, xlim, ylim, xlabel: str, ylabel: str, title: str = ""):
    ax.set_facecolor(BG)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    if xlim[0] <= 0 <= xlim[1]:
        ax.axhline(0, color=TEXT, lw=0.8, alpha=0.5)
    if ylim[0] <= 0 <= ylim[1]:
        ax.axvline(0, color=TEXT, lw=0.8, alpha=0.5)
    ax.grid(True, color=GRID, ls="--", alpha=0.7)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    if title:
        ax.set_title(title, fontsize=11, fontweight="bold")


def _scatter_pts(ax, xs, ys, color=BLUE, ms=70, zorder=3):
    ax.scatter(xs, ys, c=color, s=ms, edgecolors=TEXT, linewidths=0.5, zorder=zorder)


def _trend_line(ax, slope, y_int, xlim, color=RED, lw=2.5, label=""):
    x = np.linspace(xlim[0], xlim[1], 100)
    y = slope * x + y_int
    ax.plot(x, y, color=color, lw=lw, label=label, zorder=2)


def _draw_rise_run(ax, x1, y1, x2, y2, color=RED):
    ax.plot([x1, x2], [y1, y2], color=color, lw=2.5, zorder=4)
    ax.plot(x1, y1, "o", color=color, ms=10, zorder=5)
    ax.plot(x2, y2, "o", color=color, ms=10, zorder=5)
    ax.plot([x1, x1], [y1, y2], "--", color=GREEN, lw=2)
    ax.plot([x1, x2], [y2, y2], "--", color=ORANGE, lw=2)
    rise = y2 - y1
    run = x2 - x1
    ax.text(x1 - 0.3, (y1 + y2) / 2, f"rise\n{rise:g}", ha="right", fontsize=9,
            color=GREEN, fontweight="bold")
    ax.text((x1 + x2) / 2, y2 + (ylim_span := abs(ax.get_ylim()[1] - ax.get_ylim()[0])) * 0.04,
            f"run {run:g}", ha="center", fontsize=9, color=ORANGE, fontweight="bold")
    if run != 0:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + ylim_span * 0.08,
                f"slope = {rise:g}/{run:g}", fontsize=10, color=TEAL, fontweight="bold")


def _pay_line_data():
    """Line through (4, 35) and (16, 134): slope 8.25, y-int 2."""
    return 8.25, 2


def _travel_line_data():
    """Travel model y = 1.04x − 7.15 (miles vs hours)."""
    return 1.04, -7.15


def _roommates_rent_pts():
    xs = np.array([1, 2, 3, 4, 5, 2])
    ys = np.array([820, 100, 650, 580, 520, 100])
    return xs, ys


def _roommates_rent_trend(exclude_outlier: bool = True):
    xs, ys = _roommates_rent_pts()
    if exclude_outlier:
        mask = ~((xs == 2) & (ys == 100))
        xs, ys = xs[mask], ys[mask]
    z = np.polyfit(xs, ys, 1)
    return z[0], z[1]


# ── Activity 1 ──
def activity_1_scatterplot_basics():
    fig, ax = plt.subplots(figsize=(6, 5))
    _scatter_style(ax, (0, 10), (0, 12), "Hours studied", "Test score", "Scatter plot basics")
    pts = [(2, 4), (4, 5), (5, 7), (7, 8), (8, 10), (9, 11)]
    _scatter_pts(ax, [p[0] for p in pts], [p[1] for p in pts])
    for px, py in pts[:3]:
        ax.annotate(f"({px}, {py})", (px, py), xytext=(px + 0.3, py + 0.8), fontsize=8, color=TEXT)
    ax.text(0.5, 11, "Each point = one student\n(x, y) pair", fontsize=9, color=TEAL)
    _save(fig, "activity_1_scatterplot_basics.png")


def activity_1_correlation_types():
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    rng = np.random.default_rng(42)
    configs = [
        ("Positive", lambda x: 1.2 * x + 2 + rng.normal(0, 0.8, len(x)), GREEN),
        ("Negative", lambda x: -1.1 * x + 14 + rng.normal(0, 0.8, len(x)), RED),
        ("No correlation", lambda x: 6 + rng.normal(0, 2.5, len(x)), PURPLE),
    ]
    for ax, (label, fn, color) in zip(axes, configs):
        x = np.linspace(1, 9, 12)
        y = fn(x)
        _scatter_style(ax, (0, 10), (0, 14), "Variable x", "Variable y", label)
        _scatter_pts(ax, x, y, color=color, ms=55)
        if label != "No correlation":
            z = np.polyfit(x, y, 1)
            ax.plot(x, np.polyval(z, x), color=color, lw=2, alpha=0.7)
    fig.suptitle("Types of correlation", fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "activity_1_correlation_types.png")


# ── Activity 2 ──
def activity_2_strong_vs_weak():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    rng = np.random.default_rng(7)
    x = np.linspace(2, 10, 14)
    for ax, noise, title in zip(
        axes,
        [0.4, 2.2],
        ["Strong positive", "Weak positive"],
    ):
        y = 1.5 * x + 3 + rng.normal(0, noise, len(x))
        _scatter_style(ax, (0, 12), (0, 20), "Advertising ($100s)", "Sales ($100s)", title)
        _scatter_pts(ax, x, y)
        z = np.polyfit(x, y, 1)
        ax.plot(x, np.polyval(z, x), color=RED, lw=2)
    fig.suptitle("Strong vs weak correlation", fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "activity_2_strong_vs_weak.png")


def activity_2_linear_vs_nonlinear():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    x = np.linspace(1, 9, 14)
    rng = np.random.default_rng(3)
    y_lin = 2 * x + 1 + rng.normal(0, 0.5, len(x))
    y_cur = 0.35 * (x - 5) ** 2 + 2 + rng.normal(0, 0.4, len(x))
    for ax, y, title, color in zip(
        axes,
        [y_lin, y_cur],
        ["Linear pattern", "Nonlinear (curved) pattern"],
        [BLUE, ORANGE],
    ):
        _scatter_style(ax, (0, 10), (0, 16), "Input", "Output", title)
        _scatter_pts(ax, x, y, color=color)
        if title.startswith("Linear"):
            z = np.polyfit(x, y, 1)
            ax.plot(x, np.polyval(z, x), color=RED, lw=2)
        else:
            xp = np.linspace(1, 9, 50)
            ax.plot(xp, 0.35 * (xp - 5) ** 2 + 2, color=RED, lw=2, ls="--")
    fig.suptitle("Linear vs nonlinear association", fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "activity_2_linear_vs_nonlinear.png")


# ── Activity 3 ──
def activity_3_trend_line_slope():
    fig, ax = plt.subplots(figsize=(6, 5))
    x = np.array([1, 2, 3, 4, 5, 6, 7])
    y = np.array([3, 5, 6, 9, 10, 12, 14])
    _scatter_style(ax, (0, 8), (0, 16), "Hours worked", "Earnings ($)", "Trend line & slope")
    _scatter_pts(ax, x, y)
    m, b = np.polyfit(x, y, 1)
    _trend_line(ax, m, b, (0, 8), color=RED, label="trend line")
    _draw_rise_run(ax, 2, 5, 6, 14, color=RED)
    ax.legend(fontsize=9, loc="upper left")
    _save(fig, "activity_3_trend_line_slope.png")


def activity_3_slope_from_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    m, b = _pay_line_data()
    _scatter_style(ax, (0, 18), (0, 145), "Hours worked", "Pay ($)", "Slope from two points")
    x_pts = np.array([4, 8, 12, 16])
    y_pts = m * x_pts + b
    _scatter_pts(ax, x_pts, y_pts)
    _trend_line(ax, m, b, (0, 18), color=RED)
    ax.plot(4, 35, "o", color=RED, ms=12, zorder=5)
    ax.plot(16, 134, "o", color=RED, ms=12, zorder=5)
    ax.annotate("(4, 35)", (4, 35), xytext=(6, 50), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.annotate("(16, 134)", (16, 134), xytext=(10, 120), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    _draw_rise_run(ax, 4, 35, 16, 134, color=RED)
    ax.text(1, 130, f"y = {m}x + {b:g}", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "activity_3_slope_from_graph.png")


# ── Activity 4 ──
def activity_4_interpolation_extrapolation():
    fig, ax = plt.subplots(figsize=(6.5, 5))
    x = np.array([2, 4, 6, 8, 10])
    y = np.array([5, 9, 12, 16, 19])
    _scatter_style(ax, (0, 14), (0, 24), "Age (years)", "Height (in.)", "Interpolation vs extrapolation")
    _scatter_pts(ax, x, y)
    m, b = np.polyfit(x, y, 1)
    _trend_line(ax, m, b, (0, 14), color=RED)
    ax.axvspan(2, 10, alpha=0.15, color=GREEN, label="Interpolation\n(within data range)")
    ax.axvspan(10, 13, alpha=0.15, color=ORANGE, label="Extrapolation\n(beyond data)")
    ax.axvline(2, color=GREEN, ls=":", lw=1.5)
    ax.axvline(10, color=ORANGE, ls=":", lw=1.5)
    ax.plot(11.5, m * 11.5 + b, "x", color=ORANGE, ms=12, mew=2)
    ax.text(11.5, m * 11.5 + b + 1.2, "predicted", fontsize=8, color=ORANGE, ha="center")
    ax.legend(fontsize=8, loc="upper left")
    _save(fig, "activity_4_interpolation_extrapolation.png")


def activity_4_prediction_from_equation():
    fig, ax = plt.subplots(figsize=(6, 5))
    m, b = _travel_line_data()
    hours = np.array([10, 15, 20, 25, 30, 35])
    miles = m * hours + b + np.array([0, 2, -1, 1, -2, 0])
    _scatter_style(ax, (5, 40), (0, 35), "Time (hours)", "Distance (miles)", "Travel distance model")
    _scatter_pts(ax, hours, miles)
    _trend_line(ax, m, b, (5, 40), color=RED, label="y = 1.04x − 7.15")
    ax.text(22, 8, "y = 1.04x − 7.15\nslope ≈ 1.04 mi/hr", fontsize=10, color=TEAL, fontweight="bold")
    ax.legend(fontsize=9)
    _save(fig, "activity_4_prediction_from_equation.png")


# ── Activity 5 ──
def activity_5_two_way_table():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.set_facecolor(BG)
    ax.axis("off")
    ax.set_title("Two-way frequency table", fontsize=12, fontweight="bold", pad=12)
    table = [
        ["", "Team A", "Team B", "Total"],
        ["Win", "18", "12", "30"],
        ["Loss", "7", "13", "20"],
        ["Total", "25", "25", "50"],
    ]
    tbl = ax.table(cellText=table, loc="center", cellLoc="center")
    tbl.scale(1.2, 1.8)
    for (i, j), cell in tbl.get_celld().items():
        cell.set_facecolor(BG if i == 0 or j == 0 else "#eff6ff")
        cell.set_edgecolor(GRID)
        cell.set_text_props(fontsize=10)
    ax.text(0.5, 0.08, "Rows: game result  •  Columns: team", ha="center", fontsize=9,
            color=TEAL, transform=ax.transAxes)
    _save(fig, "activity_5_two_way_table.png")


def activity_5_table_variables():
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_facecolor(BG)
    ax.axis("off")
    ax.set_title("Assign variables to a two-way table", fontsize=12, fontweight="bold", pad=12)
    table = [
        ["", "Group 1", "Group 2", "Total"],
        ["Condition A", "14", "22", "36"],
        ["Condition B", "26", "18", "44"],
        ["Total", "40", "40", "80"],
    ]
    tbl = ax.table(cellText=table, loc="center", cellLoc="center", bbox=[0.08, 0.35, 0.84, 0.55])
    tbl.scale(1.1, 1.6)
    for (i, j), cell in tbl.get_celld().items():
        cell.set_facecolor(BG if i == 0 or j == 0 else "#f0fdf4")
        cell.set_edgecolor(GRID)
        cell.set_text_props(fontsize=10)
    labels = [
        ("Row variable:", "Treatment group (A or B)", 0.22),
        ("Column variable:", "Outcome category (1 or 2)", 0.14),
        ("Cell value:", "Frequency count for that pair", 0.06),
    ]
    for text, desc, y in labels:
        ax.text(0.06, y, text, fontsize=10, fontweight="bold", color=BLUE, transform=ax.transAxes)
        ax.text(0.32, y, desc, fontsize=10, color=TEXT, transform=ax.transAxes)
    _save(fig, "activity_5_table_variables.png")


# ── Activity 6 ──
def activity_6_outlier_effect():
    fig, ax = plt.subplots(figsize=(6, 5))
    xs, ys = _roommates_rent_pts()
    _scatter_style(ax, (0, 6), (0, 900), "Number of roommates", "Monthly rent ($)",
                   "Outlier effect on trend line")
    colors = [RED if (x == 2 and y == 100) else BLUE for x, y in zip(xs, ys)]
    for x, y, c in zip(xs, ys, colors):
        ax.scatter(x, y, c=c, s=80, edgecolors=TEXT, linewidths=0.5, zorder=3)
    ax.annotate("Outlier\n(2, 100)", (2, 100), xytext=(3.5, 250), fontsize=9, color=RED,
                fontweight="bold", arrowprops=dict(arrowstyle="->", color=RED))
    m_all, b_all = _roommates_rent_trend(exclude_outlier=False)
    m_clean, b_clean = _roommates_rent_trend(exclude_outlier=True)
    _trend_line(ax, m_all, b_all, (0.5, 5.5), color=ORANGE, lw=2, label="with outlier")
    _trend_line(ax, m_clean, b_clean, (0.5, 5.5), color=TEAL, lw=2, label="without outlier")
    ax.legend(fontsize=8)
    _save(fig, "activity_6_outlier_effect.png")


def activity_6_no_correlation_scatter():
    fig, ax = plt.subplots(figsize=(6, 5))
    rng = np.random.default_rng(99)
    reading = rng.integers(10, 60, 16)
    chores = rng.integers(1, 8, 16)
    _scatter_style(ax, (5, 65), (0, 9), "Reading minutes per day", "Chores per week",
                   "No clear correlation")
    _scatter_pts(ax, reading, chores, color=PURPLE)
    ax.text(12, 7.5, "Points scattered\n→ no association", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "activity_6_no_correlation_scatter.png")


# ── Practice images ──
def practice_u4_trend_negative():
    fig, ax = plt.subplots(figsize=(6, 5))
    rng = np.random.default_rng(11)
    x = np.linspace(1, 10, 14)
    y = -2.5 * x + 28 + rng.normal(0, 1.2, len(x))
    _scatter_style(ax, (0, 11), (0, 30), "Hours on phone", "Exercise (min/day)", "Amani's data")
    _scatter_pts(ax, x, y)
    z = np.polyfit(x, y, 1)
    ax.plot(x, np.polyval(z, x), color=RED, lw=2.5)
    ax.text(1, 26, "Negative trend", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "practice_u4_trend_negative.png", practice=True)


def practice_u4_wyatt_horizontal():
    fig, ax = plt.subplots(figsize=(6, 5))
    rng = np.random.default_rng(22)
    siblings = rng.integers(0, 5, 15)
    gpa = 2.8 + rng.normal(0, 0.35, 15)
    _scatter_style(ax, (-0.5, 5), (1.5, 4.2), "Number of siblings", "GPA", "Wyatt's scatter plot")
    _scatter_pts(ax, siblings, gpa)
    z = np.polyfit(siblings, gpa, 1)
    ax.plot(np.linspace(0, 4.5, 20), np.polyval(z, np.linspace(0, 4.5, 20)), color=RED, lw=2.5)
    ax.text(0.2, 3.9, "Nearly flat →\nno association", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "practice_u4_wyatt_horizontal.png", practice=True)


def practice_u4_trend_fit():
    fig, ax = plt.subplots(figsize=(6, 5))
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([2, 4, 5, 7, 8, 10, 11, 13])
    _scatter_style(ax, (0, 9), (0, 15), "Practice sessions", "Free-throw %", "Choose the trend line")
    _scatter_pts(ax, x, y)
    m, b = np.polyfit(x, y, 1)
    _trend_line(ax, m, b, (0, 9), color=RED, lw=2.5)
    ax.plot([0, 9], [1, 14], color=ORANGE, lw=1.5, ls="--", alpha=0.6, label="too steep")
    ax.plot([0, 9], [8, 8], color=PURPLE, lw=1.5, ls="--", alpha=0.6, label="too flat")
    ax.legend(fontsize=8)
    _save(fig, "practice_u4_trend_fit.png", practice=True)


def practice_u4_naomi_apples():
    fig, ax = plt.subplots(figsize=(6, 5))
    count = np.array([2, 4, 6, 8, 10, 12])
    weight = np.array([0.7, 1.4, 2.1, 2.8, 3.5, 4.2])
    _scatter_style(ax, (0, 14), (0, 5), "Number of apples", "Weight (lb)", "Naomi's apple stand")
    _scatter_pts(ax, count, weight)
    _trend_line(ax, 0.35, 0, (0, 14), color=RED, label="through origin")
    ax.plot(0, 0, "o", color=RED, ms=8)
    ax.text(8, 1, "y = 0.35x\n(proportional)", fontsize=10, color=TEAL, fontweight="bold")
    ax.legend(fontsize=9)
    _save(fig, "practice_u4_naomi_apples.png", practice=True)


def practice_u4_roommates_rent():
    fig, ax = plt.subplots(figsize=(6, 5))
    xs, ys = _roommates_rent_pts()
    _scatter_style(ax, (0, 6), (0, 900), "Number of roommates", "Monthly rent ($)",
                   "Rent vs roommates")
    colors = [RED if (x == 2 and y == 100) else BLUE for x, y in zip(xs, ys)]
    for x, y, c in zip(xs, ys, colors):
        ax.scatter(x, y, c=c, s=80, edgecolors=TEXT, linewidths=0.5, zorder=3)
    m, b = _roommates_rent_trend(exclude_outlier=True)
    _trend_line(ax, m, b, (0.5, 5.5), color=RED)
    ax.annotate("(2, 100)", (2, 100), xytext=(3.2, 220), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    _save(fig, "practice_u4_roommates_rent.png", practice=True)


def practice_u4_slope_line():
    fig, ax = plt.subplots(figsize=(6, 5))
    m, b = _pay_line_data()
    _scatter_style(ax, (0, 18), (0, 145), "Hours worked", "Pay ($)", "Line of best fit")
    x_pts = np.array([4, 8, 12, 16])
    _scatter_pts(ax, x_pts, m * x_pts + b)
    _trend_line(ax, m, b, (0, 18), color=RED)
    ax.plot(4, 35, "o", color=RED, ms=12, zorder=5)
    ax.plot(16, 134, "o", color=RED, ms=12, zorder=5)
    ax.text(1, 130, f"slope = 99/12 = 8.25", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "practice_u4_slope_line.png", practice=True)


def practice_u4_travel_line():
    fig, ax = plt.subplots(figsize=(6, 5))
    m, b = _travel_line_data()
    hours = np.array([10, 15, 20, 25, 30, 35])
    miles = m * hours + b + np.array([0, 2, -1, 1, -2, 0])
    _scatter_style(ax, (5, 40), (0, 35), "Time (hours)", "Distance (miles)", "Travel data")
    _scatter_pts(ax, hours, miles)
    _trend_line(ax, m, b, (5, 40), color=RED)
    ax.text(22, 8, "y = 1.04x − 7.15", fontsize=11, color=TEAL, fontweight="bold")
    _save(fig, "practice_u4_travel_line.png", practice=True)


def practice_u4_study_hours():
    fig, ax = plt.subplots(figsize=(6, 5))
    hours = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    score = np.array([55, 62, 68, 74, 78, 85, 88, 94])
    _scatter_style(ax, (0, 9), (50, 100), "Study hours", "Test score", "Mackenzie's study data")
    _scatter_pts(ax, hours, score)
    m, b = np.polyfit(hours, score, 1)
    _trend_line(ax, m, b, (0, 9), color=RED)
    ax.text(1, 96, "Positive association", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "practice_u4_study_hours.png", practice=True)


def practice_u4_hot_chocolate():
    fig, ax = plt.subplots(figsize=(6, 5))
    temp = np.array([20, 25, 30, 35, 40, 45, 50, 55])
    cups = np.array([48, 42, 38, 32, 28, 22, 18, 12])
    _scatter_style(ax, (15, 60), (0, 55), "Temperature (°F)", "Cups sold", "Hot chocolate sales")
    _scatter_pts(ax, temp, cups, color=ORANGE)
    m, b = np.polyfit(temp, cups, 1)
    _trend_line(ax, m, b, (15, 60), color=RED)
    ax.text(18, 50, "Negative trend:\ncolder → more cups", fontsize=9, color=TEAL, fontweight="bold")
    _save(fig, "practice_u4_hot_chocolate.png", practice=True)


def practice_u4_candle_height():
    fig, ax = plt.subplots(figsize=(6, 5))
    hours = np.array([0, 1, 2, 3, 4, 5, 6])
    height = np.array([12, 10.5, 9, 7.5, 6, 4.5, 3])
    _scatter_style(ax, (-0.5, 7), (0, 14), "Time (hours)", "Candle height (in.)", "Candle burning")
    _scatter_pts(ax, hours, height)
    _trend_line(ax, -1.5, 12, (-0.5, 7), color=RED)
    ax.text(0.5, 12.5, "y = −1.5x + 12\nlinear decrease", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "practice_u4_candle_height.png", practice=True)


def practice_u4_ticket_outlier():
    fig, ax = plt.subplots(figsize=(6, 5))
    games = np.array([3, 5, 7, 9, 11, 13, 1])
    tickets = np.array([120, 180, 240, 290, 350, 400, 60])
    _scatter_style(ax, (0, 15), (0, 450), "Games played", "Ticket sales", "Season ticket sales")
    colors = [RED if (g == 1 and t == 60) else BLUE for g, t in zip(games, tickets)]
    for g, t, c in zip(games, tickets, colors):
        ax.scatter(g, t, c=c, s=80, edgecolors=TEXT, linewidths=0.5, zorder=3)
    mask = ~((games == 1) & (tickets == 60))
    m, b = np.polyfit(games[mask], tickets[mask], 1)
    _trend_line(ax, m, b, (0, 15), color=RED)
    ax.annotate("Outlier (1, 60)", (1, 60), xytext=(4, 120), fontsize=9, color=RED,
                fontweight="bold", arrowprops=dict(arrowstyle="->", color=RED))
    _save(fig, "practice_u4_ticket_outlier.png", practice=True)


def practice_u4_negative_slope_pick():
    fig, ax = plt.subplots(figsize=(6, 5))
    rng = np.random.default_rng(16)
    x = np.linspace(2, 12, 15)
    y = -1.8 * x + 32 + rng.normal(0, 1.5, len(x))
    _scatter_style(ax, (0, 14), (0, 35), "Screen time (hrs)", "Sleep (hrs)", "Pick the trend line")
    _scatter_pts(ax, x, y)
    z = np.polyfit(x, y, 1)
    ax.plot(x, np.polyval(z, x), color=RED, lw=2.5, label="correct (negative)")
    ax.plot([0, 14], [5, 30], color=ORANGE, lw=1.5, ls="--", alpha=0.6, label="positive")
    ax.plot([0, 14], [15, 15], color=PURPLE, lw=1.5, ls="--", alpha=0.6, label="horizontal")
    ax.legend(fontsize=8, loc="upper right")
    _save(fig, "practice_u4_negative_slope_pick.png", practice=True)


LESSON_FUNCS = [
    activity_1_scatterplot_basics, activity_1_correlation_types,
    activity_2_strong_vs_weak, activity_2_linear_vs_nonlinear,
    activity_3_trend_line_slope, activity_3_slope_from_graph,
    activity_4_interpolation_extrapolation, activity_4_prediction_from_equation,
    activity_5_two_way_table, activity_5_table_variables,
    activity_6_outlier_effect, activity_6_no_correlation_scatter,
]

PRACTICE_FUNCS = [
    practice_u4_trend_negative, practice_u4_wyatt_horizontal, practice_u4_trend_fit,
    practice_u4_naomi_apples, practice_u4_roommates_rent, practice_u4_slope_line,
    practice_u4_travel_line, practice_u4_study_hours, practice_u4_hot_chocolate,
    practice_u4_candle_height, practice_u4_ticket_outlier, practice_u4_negative_slope_pick,
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
