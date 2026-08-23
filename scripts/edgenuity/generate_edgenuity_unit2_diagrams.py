"""
Generate matplotlib diagrams for Edgenuity Course 3 Unit 2 (lesson + practice).

Usage:
    python generate_edgenuity_unit2_diagrams.py
    python generate_edgenuity_unit2_diagrams.py --practice-only
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

OUT_DIR = os.path.join(str(Path(__file__).resolve().parents[2]), ArjunEdgenuityCourse3", "images", "unit_2"
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


def _wilson_watering_ax(ax, title="Wilson's watering can"):
    _axes_style_real(ax, (-0.5, 6), (-0.5, 3.5), "Time (seconds)", "Water (gallons)", title)
    t = np.linspace(0, 5, 50)
    w = 2.5 - 0.5 * t
    ax.plot(t, w, color=TEAL, lw=2.5)
    ax.plot(0, 2.5, "o", color=RED, ms=10, zorder=5)
    ax.plot(5, 0, "o", color=RED, ms=10, zorder=5)
    ax.annotate("(0, 2.5)", (0, 2.5), xytext=(0.8, 2.8), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1))
    ax.annotate("(5, 0)", (5, 0), xytext=(3.5, 0.6), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1))


def _brenda_phone_ax(ax, title="Brenda's phone bill"):
    _axes_style_real(ax, (-0.5, 6), (0, 70), "Hours used", "Bill ($)", title)
    h = np.linspace(0, 5, 50)
    bill = 12 + 9 * h
    ax.plot(h, bill, color=PURPLE, lw=2.5)
    ax.plot(0, 12, "o", color=RED, ms=10, zorder=5)
    ax.annotate("$12 base fee", (0, 12), xytext=(1.2, 22), fontsize=9, color=TEAL,
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1))
    ax.text(3.5, 55, "+$9/hour", fontsize=10, color=PURPLE, fontweight="bold")


# ── Activity 1 ──
def activity_1_slope_rise_run():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (0, 8), (0, 10), "Slope: rise over run")
    _draw_rise_run(ax, 2, 3, 6, 11)
    _save(fig, "activity_1_slope_rise_run.png")


def activity_1_wilson_watering():
    fig, ax = plt.subplots(figsize=(6, 4))
    _wilson_watering_ax(ax)
    _save(fig, "activity_1_wilson_watering.png")


# ── Activity 2 ──
def activity_2_y_intercept_line():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-4, 6), (-2, 8), "y-intercept at (0, 3)")
    _plot_line(ax, 0.75, 3, (-4, 6))
    ax.plot(0, 3, "o", color=RED, ms=12, zorder=5)
    ax.annotate("(0, 3)", (0, 3), xytext=(1.5, 5), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.text(4, 2, "y-intercept", fontsize=10, color=TEAL)
    _save(fig, "activity_2_y_intercept_line.png")


def activity_2_initial_value_table():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.axis("off")
    ax.set_title("Tip jar — hours worked vs money collected", fontsize=12, fontweight="bold", pad=12)
    rows = [("Hours", "Tip jar ($)"), ("0", "5"), ("1", "12"), ("2", "19"), ("3", "26"), ("4", "33")]
    col_x = [0.25, 0.65]
    for i, (h, m) in enumerate(rows):
        y = 0.82 - i * 0.14
        weight = "bold" if i == 0 else "normal"
        color = TEXT if i == 0 else TEXT
        ax.text(col_x[0], y, h, ha="center", fontsize=11, fontweight=weight, color=color, transform=ax.transAxes)
        ax.text(col_x[1], y, m, ha="center", fontsize=11, fontweight=weight, color=color, transform=ax.transAxes)
        if i == 0:
            ax.plot([0.08, 0.92], [y - 0.04, y - 0.04], color=GRID, lw=1.5, transform=ax.transAxes)
    ax.text(0.5, 0.08, "Initial value at 0 hours = $5", ha="center", fontsize=10, color=TEAL, transform=ax.transAxes)
    rect = Rectangle((0.08, 0.12), 0.84, 0.78, fill=False, edgecolor=GRID, lw=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    _save(fig, "activity_2_initial_value_table.png")


# ── Activity 3 ──
def activity_3_direct_vs_not():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-1, 8), (-1, 10), "Direct variation vs not")
    x = np.linspace(0, 8, 50)
    ax.plot(x, 1.5 * x, color=GREEN, lw=2.5, label="Through origin (direct)")
    ax.plot(x, 1.5 * x + 3, color=ORANGE, lw=2.5, label="y-intercept ≠ 0 (not direct)")
    ax.plot(0, 0, "o", color=GREEN, ms=8)
    ax.plot(0, 3, "o", color=ORANGE, ms=8)
    ax.legend(fontsize=9)
    _save(fig, "activity_3_direct_vs_not.png")


def activity_3_proportional_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-1, 8), (-1, 10), "Proportional relationship")
    x = np.linspace(0, 8, 50)
    ax.plot(x, 2 * x, color=GREEN, lw=2.5)
    ax.plot(0, 0, "o", color=RED, ms=10)
    ax.text(4, 6, "y = 2x\n(passes through origin)", fontsize=10, color=TEAL)
    _save(fig, "activity_3_proportional_graph.png")


# ── Activity 4 ──
def activity_4_horizontal_vertical():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-2, 8), (-2, 8), "Horizontal and vertical lines")
    ax.axhline(2, color=BLUE, lw=2.5, label="y = 2 (horizontal)")
    ax.axvline(3, color=ORANGE, lw=2.5, label="x = 3 (vertical)")
    ax.text(6.5, 2.3, "y = 2", fontsize=10, color=BLUE, fontweight="bold")
    ax.text(3.2, 6.5, "x = 3", fontsize=10, color=ORANGE, fontweight="bold")
    ax.legend(fontsize=9)
    _save(fig, "activity_4_horizontal_vertical.png")


def activity_4_zero_undefined_slope():
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, title, fn, note, color in [
        (axes[0], "Slope = 0", lambda a: a.axhline(2, color=BLUE, lw=2.5), "Horizontal line\nrise = 0", BLUE),
        (axes[1], "Undefined slope", lambda a: a.axvline(3, color=RED, lw=2.5), "Vertical line\nrun = 0", RED),
    ]:
        _axes_style(ax, (-2, 6), (-2, 6), title)
        fn(ax)
        ax.text(3, 4.5, note, ha="center", fontsize=10, color=color, fontweight="bold")
    fig.suptitle("Zero slope vs undefined slope", fontsize=12, fontweight="bold")
    fig.subplots_adjust(wspace=0.3)
    _save(fig, "activity_4_zero_undefined_slope.png")


# ── Activity 5 ──
def activity_5_equation_from_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-4, 8), (-2, 10), "Write an equation from the graph")
    _plot_line(ax, 0.5, 4, (-4, 8))
    ax.plot(0, 4, "o", color=RED, ms=10)
    ax.plot(8, 8, "o", color=RED, ms=10)
    ax.text(4, 2, "slope = 0.5\ny-intercept = 4", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "activity_5_equation_from_graph.png")


def activity_5_point_on_line():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-8, 4), (-4, 4), "Does the point lie on the line?")
    pts = [(2, -2), (-6, 2)]
    x = np.linspace(-8, 4, 50)
    ax.plot(x, -0.5 * x - 1, color=BLUE, lw=2.5)
    for px, py in pts:
        ax.plot(px, py, "o", color=RED, ms=10, zorder=5)
        ax.text(px + 0.3, py + 0.4, f"({px}, {py})", fontsize=9, color=RED)
    _save(fig, "activity_5_point_on_line.png")


# ── Activity 6 ──
def activity_6_shake_shack_model():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.axis("off")
    ax.set_title("Shake Shack — shake size vs cost", fontsize=12, fontweight="bold", pad=12)
    rows = [("Size", "Cost ($)"), ("Small", "3.50"), ("Medium", "4.25"), ("Large", "5.00")]
    col_x = [0.3, 0.7]
    for i, (size, cost) in enumerate(rows):
        y = 0.78 - i * 0.16
        weight = "bold" if i == 0 else "normal"
        ax.text(col_x[0], y, size, ha="center", fontsize=11, fontweight=weight, transform=ax.transAxes)
        ax.text(col_x[1], y, cost, ha="center", fontsize=11, fontweight=weight, transform=ax.transAxes)
        if i == 0:
            ax.plot([0.1, 0.9], [y - 0.05, y - 0.05], color=GRID, lw=1.5, transform=ax.transAxes)
    ax.text(0.5, 0.1, "Cost increases by $0.75 per size step", ha="center", fontsize=10, color=TEAL, transform=ax.transAxes)
    rect = Rectangle((0.1, 0.15), 0.8, 0.72, fill=False, edgecolor=GRID, lw=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    _save(fig, "activity_6_shake_shack_model.png")


def activity_6_brenda_phone_bill():
    fig, ax = plt.subplots(figsize=(6, 4))
    _brenda_phone_ax(ax)
    _save(fig, "activity_6_brenda_phone_bill.png")


# ── Practice images ──
def practice_u2_wilson_can():
    fig, ax = plt.subplots(figsize=(6, 4))
    _wilson_watering_ax(ax, "Wilson's watering can — water remaining")
    _save(fig, "practice_u2_wilson_can.png", practice=True)


def practice_u2_baseball():
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _axes_style_real(
        ax, (-5, 110), (-20, 520),
        "Speed (mph)", "Distance (feet)",
        "Baseball distance vs speed",
    )
    mph = np.linspace(0, 100, 50)
    dist = 5 * mph
    ax.plot(mph, dist, color=BLUE, lw=2.5)
    ax.plot(0, 0, "o", color=RED, ms=10)
    ax.plot(100, 500, "o", color=RED, ms=10)
    ax.annotate("(100, 500)", (100, 500), xytext=(60, 450), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1))
    ax.text(40, 120, "Through origin\n~5 ft per mph", fontsize=10, color=TEAL)
    _save(fig, "practice_u2_baseball.png", practice=True)


def practice_u2_maricella():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-8, 4), (-12, 2), "Maricella's line graph")
    pts = [(-6, -10), (-4, -8), (-2, -6), (0, -4)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, "o-", color=BLUE, lw=2.5, ms=10, zorder=4)
    x_ext = np.linspace(-6, 0, 50)
    ax.plot(x_ext, x_ext - 4, "--", color=TEAL, lw=1.5, alpha=0.6)
    ax.plot(0, -10, "o", color=RED, ms=12, zorder=5)
    ax.plot([-6, 0], [-10, -10], ":", color=ORANGE, lw=1.5, alpha=0.8)
    ax.annotate("y-axis (0, −10)", (0, -10), xytext=(1.5, -7.5), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    for px, py in pts:
        ax.text(px + 0.2, py + 0.5, f"({px}, {py})", fontsize=8, color=TEXT)
    _save(fig, "practice_u2_maricella.png", practice=True)


def practice_u2_brenda_phone():
    fig, ax = plt.subplots(figsize=(6, 4))
    _brenda_phone_ax(ax, "Brenda's monthly phone bill")
    _save(fig, "practice_u2_brenda_phone.png", practice=True)


def practice_u2_direct_graphs():
    fig, axes = plt.subplots(2, 2, figsize=(8, 7))
    configs = [
        ("A", 2, 0, (-1, 5), (-1, 10)),
        ("B", -1.5, 0, (-1, 5), (-1, 8)),
        ("C", 1, 4, (-1, 5), (-1, 10)),
        ("D", 0.5, 2, (-1, 6), (-1, 8)),
    ]
    for ax, (label, slope, y_int, xlim, ylim) in zip(axes.flat, configs):
        _axes_style(ax, xlim, ylim, f"Graph {label}")
        _plot_line(ax, slope, y_int, xlim)
        if y_int == 0:
            ax.plot(0, 0, "o", color=GREEN, ms=8)
        else:
            ax.plot(0, y_int, "o", color=ORANGE, ms=8)
    fig.suptitle("Which graphs show direct variation?", fontsize=12, fontweight="bold")
    fig.subplots_adjust(hspace=0.35, wspace=0.3)
    _save(fig, "practice_u2_direct_graphs.png", practice=True)


def practice_u2_zero_lines():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style(ax, (-2, 8), (-2, 8), "Which line has slope 0?")
    lines = [
        ("P", 1, 1, BLUE),
        ("Q", 0, 3, RED),
        ("R", -0.5, 6, GREEN),
        ("S", 2, -2, PURPLE),
    ]
    x = np.linspace(-2, 8, 50)
    for label, slope, y_int, color in lines:
        ax.plot(x, slope * x + y_int, color=color, lw=2, label=f"Line {label}")
        ax.text(7, slope * 7 + y_int + 0.25, label, fontsize=11, fontweight="bold", color=color)
    ax.legend(fontsize=9, loc="upper left")
    _save(fig, "practice_u2_zero_lines.png", practice=True)


def practice_u2_vertical_line():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    _axes_style(ax, (-2, 6), (-4, 6), "Which line has undefined slope?")
    ax.axvline(2, color=RED, lw=2.5, label="x = 2")
    x = np.linspace(-2, 6, 50)
    ax.plot(x, 0.5 * x + 1, color=BLUE, lw=2, label="Line A")
    ax.plot(x, -x + 4, color=GREEN, lw=2, label="Line B")
    ax.text(2.15, 4.5, "x = 2", fontsize=10, color=RED, fontweight="bold")
    ax.legend(fontsize=9)
    _save(fig, "practice_u2_vertical_line.png", practice=True)


def practice_u2_ladder():
    fig, ax = plt.subplots(figsize=(6, 5))
    _axes_style_real(
        ax, (0, 14), (0, 14),
        "Distance from wall (ft)", "Height on wall (ft)",
        "Ladder leaning against a wall",
    )
    dist = np.linspace(3, 12, 50)
    height = np.sqrt(13 ** 2 - dist ** 2)
    ax.plot(dist, height, color=TEAL, lw=2.5)
    ax.plot(3, 12.49, "o", color=RED, ms=8)
    ax.plot(12, 5, "o", color=RED, ms=8)
    ax.text(8, 11, "13-ft ladder", fontsize=10, color=TEAL, fontweight="bold")
    ax.text(5, 2, "As distance ↑,\nheight ↓", fontsize=9, color=ORANGE)
    _save(fig, "practice_u2_ladder.png", practice=True)


def practice_u2_equation_graph():
    fig, ax = plt.subplots(figsize=(5.5, 5))
    _axes_style(ax, (-3, 5), (-10, 6), "Match the equation to the graph")
    _plot_line(ax, 2, -4, (-3, 5))
    ax.plot(0, -4, "o", color=RED, ms=10)
    ax.plot(2, 0, "o", color=RED, ms=10)
    ax.text(3, -8, "slope = 2\ny-int = −4", fontsize=10, color=TEAL, fontweight="bold")
    _save(fig, "practice_u2_equation_graph.png", practice=True)


def practice_u2_tip_jar():
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _axes_style_real(
        ax, (-0.5, 5), (0, 40),
        "Hours worked", "Tip jar ($)",
        "Tip jar — initial value and rate",
    )
    hrs = [0, 1, 2, 3, 4]
    tips = [5, 12, 19, 26, 33]
    ax.plot(hrs, tips, "o-", color=GREEN, lw=2, ms=10)
    ax.plot(0, 5, "o", color=RED, ms=10)
    ax.annotate("$5 start", (0, 5), xytext=(1.2, 10), fontsize=9, color=TEAL,
                arrowprops=dict(arrowstyle="->", color=TEAL))
    ax.text(2.5, 30, "+$7/hour", fontsize=10, color=GREEN, fontweight="bold")
    _save(fig, "practice_u2_tip_jar.png", practice=True)


def practice_u2_slope_table():
    fig, ax = plt.subplots(figsize=(5.5, 5))
    _axes_style_real(
        ax, (-1, 7), (-2, 14),
        "Input", "Output",
        "Find the slope from the graph",
    )
    _draw_rise_run(ax, 1, 2, 3, 6)
    ax.plot(5, 10, "o", color=BLUE, ms=10)
    _save(fig, "practice_u2_slope_table.png", practice=True)


LESSON_FUNCS = [
    activity_1_slope_rise_run, activity_1_wilson_watering,
    activity_2_y_intercept_line, activity_2_initial_value_table,
    activity_3_direct_vs_not, activity_3_proportional_graph,
    activity_4_horizontal_vertical, activity_4_zero_undefined_slope,
    activity_5_equation_from_graph, activity_5_point_on_line,
    activity_6_shake_shack_model, activity_6_brenda_phone_bill,
]

PRACTICE_FUNCS = [
    practice_u2_wilson_can, practice_u2_baseball, practice_u2_maricella,
    practice_u2_brenda_phone, practice_u2_direct_graphs, practice_u2_zero_lines,
    practice_u2_vertical_line, practice_u2_ladder, practice_u2_equation_graph,
    practice_u2_tip_jar, practice_u2_slope_table,
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
