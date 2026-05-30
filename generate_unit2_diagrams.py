"""
Generate clean matplotlib diagrams for Course 3 Unit 2 (Activities 9–15).

Usage:
    python generate_unit2_diagrams.py              # all
    python generate_unit2_diagrams.py --activity 10
    python generate_unit2_diagrams.py --activity 10 --force
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunCourse3", "images", "unit_2")
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


def _line_ax(ax, xlim=(-1, 8), ylim=(-1, 8)):
    ax.set_facecolor(BG)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axhline(0, color=GRID, lw=1)
    ax.axvline(0, color=GRID, lw=1)
    ax.grid(True, color=GRID, alpha=0.5, linestyle="--")
    ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color(GRID)


# ── Activity 10 ──────────────────────────────────────────────────────────────

def activity_10_balance_scale():
    fig, ax = plt.subplots(figsize=(8, 3.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    # beam
    ax.plot([1, 9], [3, 3], color=TEXT, lw=3)
    ax.plot([5, 5], [1.5, 3], color=TEXT, lw=3)
    # left pan
    ax.add_patch(FancyBboxPatch((1.5, 3.2), 2.5, 0.5, boxstyle="round", facecolor=GRID, edgecolor=TEXT))
    ax.text(2.75, 3.45, "3x + 4", ha="center", fontsize=12, fontweight="bold")
    # right pan
    ax.add_patch(FancyBboxPatch((6, 3.2), 2.5, 0.5, boxstyle="round", facecolor=GRID, edgecolor=TEXT))
    ax.text(7.25, 3.45, "16", ha="center", fontsize=12, fontweight="bold")
    ax.text(5, 3.85, "Balance: do the same to BOTH sides", ha="center", fontsize=11, color=TEAL)
    ax.annotate("", xy=(5, 2.2), xytext=(2.75, 2.2), arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
    ax.text(3.8, 2.45, "−4", fontsize=11, color=GREEN, fontweight="bold")
    ax.annotate("", xy=(5, 2.2), xytext=(7.25, 2.2), arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
    ax.text(6.2, 2.45, "−4", fontsize=11, color=GREEN, fontweight="bold")
    fig.suptitle("Solving like a balance scale", fontsize=13, fontweight="bold", color=TEXT)
    _save(fig, "activity_10_balance_scale.png")


def activity_10_solve_steps():
    fig, ax = plt.subplots(figsize=(8, 3.2))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    steps = [
        ("Start", "3x + 4 = 16", BLUE),
        ("Subtract 4", "3x = 12", TEAL),
        ("Divide by 3", "x = 4", GREEN),
        ("Check", "3(4)+4 = 16 ✓", ORANGE),
    ]
    for i, (label, eq, color) in enumerate(steps):
        x = 1.2 + i * 2.2
        ax.add_patch(FancyBboxPatch((x - 0.9, 1.2), 1.8, 1.6, boxstyle="round,pad=0.05", facecolor=color, alpha=0.15, edgecolor=color, lw=2))
        ax.text(x, 2.35, label, ha="center", fontsize=10, color=MUTED)
        ax.text(x, 1.75, eq, ha="center", fontsize=11, fontweight="bold", color=TEXT)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 1.1, 2), xytext=(x + 0.7, 2), arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.5))
    fig.suptitle("Example: Solve 3x + 4 = 16", fontsize=13, fontweight="bold", color=TEXT)
    _save(fig, "activity_10_solve_steps.png")


def activity_10_solution_types():
    fig, axes = plt.subplots(1, 3, figsize=(9, 3))
    titles = ["One solution", "No solution", "Infinitely many"]
    examples = ["x = 3", "1 = 5 ✗", "Always true ✓"]
    colors = [GREEN, RED, BLUE]
    for ax, title, ex, c in zip(axes, titles, examples, colors):
        _off(ax)
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 3)
        ax.add_patch(FancyBboxPatch((0.4, 0.8), 3.2, 1.6, boxstyle="round", facecolor=c, alpha=0.12, edgecolor=c, lw=2))
        ax.text(2, 2.1, title, ha="center", fontsize=11, fontweight="bold", color=TEXT)
        ax.text(2, 1.35, ex, ha="center", fontsize=10, color=c)
    fig.suptitle("Types of equation outcomes", fontsize=13, fontweight="bold", color=TEXT)
    fig.subplots_adjust(wspace=0.25)
    _save(fig, "activity_10_solution_types.png")


# ── Activity 11 ──────────────────────────────────────────────────────────────

def activity_11_change_in_y_x():
    fig, ax = plt.subplots(figsize=(5.5, 5))
    _line_ax(ax, (0, 8), (0, 8))
    x1, y1, x2, y2 = 2, 3, 6, 11
    ax.plot([x1, x2], [y1, y2], color=BLUE, lw=2.5)
    ax.plot(x1, y1, "o", color=BLUE, markersize=10)
    ax.plot(x2, y2, "o", color=BLUE, markersize=10)
    ax.plot([x1, x1], [y1, y2], "--", color=GREEN, lw=2)
    ax.plot([x1, x2], [y2, y2], "--", color=ORANGE, lw=2)
    ax.text(x1 - 0.55, (y1 + y2) / 2, "vertical\nchange 8", ha="right", fontsize=9, color=GREEN, fontweight="bold")
    ax.text((x1 + x2) / 2, y2 + 0.45, "horizontal change 4", ha="center", fontsize=9, color=ORANGE, fontweight="bold")
    ax.text(2, 7.0, "slope = Δy/Δx = 8/4 = 2", fontsize=11, color=TEXT, bbox=dict(boxstyle="round", facecolor="#eff6ff", edgecolor=BLUE))
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel("y", fontsize=10)
    fig.suptitle("Slope from two points", fontsize=13, fontweight="bold")
    _save(fig, "activity_11_change_in_y_x.png")


def activity_11_rate_context():
    fig, ax = plt.subplots(figsize=(6, 4))
    hours = [0, 1, 2]
    miles = [0, 15, 30]
    ax.set_facecolor(BG)
    ax.bar(hours, miles, color=BLUE, edgecolor=TEXT, width=0.5)
    ax.plot(hours, miles, "o-", color=ORANGE, lw=2, markersize=8)
    ax.set_xlabel("Time (hours)", fontsize=10)
    ax.set_ylabel("Distance (miles)", fontsize=10)
    ax.set_xticks(hours)
    ax.set_ylim(0, 35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.text(1, 28, "slope = 30/2 = 15 mi/hr", ha="center", fontsize=11, color=TEAL, fontweight="bold")
    fig.suptitle("Slope as rate: 30 miles in 2 hours", fontsize=13, fontweight="bold")
    _save(fig, "activity_11_rate_context.png")


# ── Activity 12 ──────────────────────────────────────────────────────────────

def activity_12_y_mx_b():
    fig, ax = plt.subplots(figsize=(6, 5))
    _line_ax(ax, (-1, 6), (-1, 8))
    m, b = 2, 3
    x = np.linspace(-0.5, 4, 50)
    y = m * x + b
    ax.plot(x, y, color=BLUE, lw=2.5)
    ax.plot(0, b, "o", color=ORANGE, markersize=12, zorder=5)
    ax.plot(1, m + b, "o", color=BLUE, markersize=8)
    ax.annotate("", xy=(1, m + b), xytext=(0, b), arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
    ax.text(-0.6, b, f"b = {b}", fontsize=11, color=ORANGE, fontweight="bold")
    ax.text(1.15, 4.5, "Δy = 2", fontsize=9, color=GREEN)
    ax.text(0.5, 3.8, "Δx = 1", fontsize=9, color=GREEN)
    ax.text(3.5, 7, "y = 2x + 3", fontsize=12, color=BLUE, fontweight="bold")
    ax.text(3.2, 6.3, "m = slope", fontsize=10, color=MUTED)
    fig.suptitle("Slope-intercept form: y = mx + b", fontsize=13, fontweight="bold")
    _save(fig, "activity_12_y_mx_b.png")


def activity_12_graph_example():
    fig, ax = plt.subplots(figsize=(6, 5))
    _line_ax(ax, (-3, 5), (-4, 6))
    m, b = 0.5, -2
    x = np.linspace(-2, 4, 50)
    ax.plot(x, m * x + b, color=PURPLE, lw=2.5)
    ax.plot(0, b, "o", color=ORANGE, markersize=12)
    ax.plot(2, m * 2 + b, "o", color=PURPLE, markersize=8)
    ax.text(0.2, b - 0.5, "(0, −2)", fontsize=10, color=ORANGE)
    ax.text(2.1, m * 2 + b + 0.3, "(2, −1)", fontsize=10, color=PURPLE)
    ax.text(-2.5, 5, "y = ½x − 2\nstart at b, slope ½", fontsize=11, color=TEXT)
    fig.suptitle("Graph using y-intercept + slope", fontsize=13, fontweight="bold")
    _save(fig, "activity_12_graph_example.png")


# ── Activity 13 ──────────────────────────────────────────────────────────────

def activity_13_proportional_vs_not():
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, title, m, b, through_origin in zip(
        axes,
        ["Proportional: y = 3x", "Not proportional: y = 3x + 4"],
        [3, 3],
        [0, 4],
        [True, False],
    ):
        _line_ax(ax, (-1, 4), (-1, 14))
        x = np.linspace(0, 3.5, 50)
        ax.plot(x, m * x + b, color=BLUE if through_origin else ORANGE, lw=2.5)
        if through_origin:
            ax.plot(0, 0, "o", color=GREEN, markersize=10)
            ax.text(0.3, 0.5, "(0, 0)", fontsize=9, color=GREEN)
        else:
            ax.plot(0, b, "o", color=RED, markersize=10)
            ax.text(0.3, b + 0.5, f"(0, {b})", fontsize=9, color=RED)
        ax.set_title(title, fontsize=11, fontweight="bold")
    fig.suptitle("Proportional vs nonproportional", fontsize=13, fontweight="bold")
    fig.subplots_adjust(wspace=0.3)
    _save(fig, "activity_13_proportional_vs_not.png")


def activity_13_table_constant():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    _off(ax)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5)
    headers = ["x", "y", "y/x"]
    rows = [("2", "7", "3.5"), ("4", "14", "3.5"), ("6", "21", "3.5")]
    col_w = [1.0, 1.0, 1.2]
    y0 = 3.8
    rh = 0.55
    for j, h in enumerate(headers):
        ax.add_patch(Rectangle((1 + sum(col_w[:j]), y0 - rh), col_w[j], rh, facecolor=TEAL, edgecolor=TEXT))
        ax.text(1 + sum(col_w[:j]) + col_w[j] / 2, y0 - rh / 2, h, ha="center", va="center", color="white", fontweight="bold")
    for i, row in enumerate(rows):
        y = y0 - (i + 2) * rh
        for j, cell in enumerate(row):
            ax.add_patch(Rectangle((1 + sum(col_w[:j]), y), col_w[j], rh, facecolor="#f0fdfa" if i % 2 == 0 else BG, edgecolor=GRID))
            ax.text(1 + sum(col_w[:j]) + col_w[j] / 2, y + rh / 2, cell, ha="center", va="center", fontsize=11)
    ax.text(4, 0.5, "Same ratio → y = 3.5x (proportional)", ha="center", fontsize=11, color=TEAL, fontweight="bold")
    fig.suptitle("Check proportionality with y/x", fontsize=13, fontweight="bold")
    _save(fig, "activity_13_table_constant.png")


# ── Activity 14 ──────────────────────────────────────────────────────────────

def activity_14_intersection():
    fig, ax = plt.subplots(figsize=(6, 5))
    _line_ax(ax, (-1, 6), (-1, 8))
    x = np.linspace(-0.5, 5, 50)
    ax.plot(x, x + 1, color=BLUE, lw=2, label="y = x + 1")
    ax.plot(x, -x + 5, color=ORANGE, lw=2, label="y = −x + 5")
    ax.plot(2, 3, "o", color=GREEN, markersize=14, zorder=5)
    ax.annotate("Solution (2, 3)", xy=(2, 3), xytext=(3, 5), fontsize=11, color=GREEN, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=GREEN))
    ax.legend(loc="upper right", fontsize=9)
    fig.suptitle("System solution = intersection point", fontsize=13, fontweight="bold")
    _save(fig, "activity_14_intersection.png")


def activity_14_parallel():
    fig, ax = plt.subplots(figsize=(6, 5))
    _line_ax(ax, (-2, 6), (-2, 10))
    x = np.linspace(-1, 5, 50)
    ax.plot(x, 3 * x + 2, color=BLUE, lw=2, label="y = 3x + 2")
    ax.plot(x, 3 * x - 1, color=ORANGE, lw=2, linestyle="--", label="y = 3x − 1")
    ax.text(2, 8, "Same slope,\nparallel\n→ no solution", fontsize=11, color=RED, fontweight="bold", ha="center")
    ax.legend(fontsize=9)
    fig.suptitle("Parallel lines: no solution", fontsize=13, fontweight="bold")
    _save(fig, "activity_14_parallel.png")


def activity_14_three_cases():
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))

    def _one(ax):
        _line_ax(ax, (-1, 5), (-1, 7))
        ax.plot([0, 4], [1, 5], color=BLUE)
        ax.plot([0, 4], [5, 1], color=ORANGE)
        ax.plot(2, 3, "o", color=GREEN, ms=8)

    def _none(ax):
        _line_ax(ax, (-1, 5), (-1, 7))
        ax.plot([0, 4], [1, 9], color=BLUE)
        ax.plot([0, 4], [0, 8], color=ORANGE, ls="--")

    def _many(ax):
        _line_ax(ax, (-1, 5), (-1, 7))
        ax.plot([0, 4], [1, 5], color=BLUE)
        ax.plot([0, 4], [1, 5], color=BLUE, ls="--", alpha=0.5)

    for ax, (title, draw) in zip(
        axes,
        [("One solution", _one), ("No solution", _none), ("Infinitely many", _many)],
    ):
        draw(ax)
        ax.set_title(title, fontsize=10, fontweight="bold")
    fig.suptitle("Systems: three possible outcomes", fontsize=13, fontweight="bold")
    fig.subplots_adjust(wspace=0.35)
    _save(fig, "activity_14_three_cases.png")


# ── Activity 15 ──────────────────────────────────────────────────────────────

def _flow_steps(ax, steps: list[tuple[str, str, str]], x0: float = 0.6, y0: float = 3.0, dy: float = 0.72):
    """Draw labeled steps (label, equation, color) top to bottom."""
    for i, (label, eq, color) in enumerate(steps):
        y = y0 - i * dy
        ax.text(x0, y + 0.22, label, fontsize=9, color=MUTED, fontweight="bold")
        ax.text(x0, y - 0.08, eq, fontsize=11, color=color, fontweight="bold", family="sans-serif")


def activity_15_substitution():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    ax_steps, ax_graph = axes
    _off(ax_steps)
    ax_steps.set_xlim(0, 5.5)
    ax_steps.set_ylim(0, 4)
    _flow_steps(
        ax_steps,
        [
            ("System", "y = 4x - 3", TEXT),
            ("System", "2x + y = 13", TEXT),
            ("Substitute", "2x + (4x - 3) = 13", TEAL),
            ("Simplify", "6x - 3 = 13  ->  x = 8/3", TEAL),
            ("Back-sub", "y = 4(8/3) - 3 = 23/3", GREEN),
            ("Answer", "(8/3, 23/3)", GREEN),
        ],
        x0=0.4,
        y0=3.6,
        dy=0.58,
    )
    ax_steps.set_title("Substitution steps", fontsize=11, fontweight="bold", pad=8)

    _line_ax(ax_graph, (-0.5, 4), (-1, 12))
    x = np.linspace(-0.2, 3.2, 80)
    ax_graph.plot(x, 4 * x - 3, color=BLUE, lw=2.5, label="y = 4x - 3")
    ax_graph.plot(x, 13 - 2 * x, color=ORANGE, lw=2.5, label="2x + y = 13")
    xs, ys = 8 / 3, 23 / 3
    ax_graph.plot(xs, ys, "o", color=GREEN, ms=12, zorder=5)
    ax_graph.annotate(
        f"({xs:.2f}, {ys:.2f})",
        xy=(xs, ys),
        xytext=(xs + 0.35, ys + 1.2),
        fontsize=10,
        color=GREEN,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5),
    )
    ax_graph.legend(loc="upper left", fontsize=8)
    ax_graph.set_title("Graph: one solution = intersection", fontsize=11, fontweight="bold", pad=8)
    fig.suptitle("Substitution method", fontsize=13, fontweight="bold", y=1.02)
    fig.subplots_adjust(wspace=0.28, top=0.88)
    _save(fig, "activity_15_substitution.png")


def activity_15_elimination():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ax_work, ax_after = axes
    _off(ax_work)
    ax_work.set_xlim(0, 6)
    ax_work.set_ylim(0, 4.5)
    ax_work.text(0.4, 3.85, "Equation 1:", fontsize=9, color=MUTED, fontweight="bold")
    ax_work.text(0.4, 3.45, "3x + 2y = 16", fontsize=12, color=TEXT, fontweight="bold")
    ax_work.text(0.4, 2.85, "Equation 2:", fontsize=9, color=MUTED, fontweight="bold")
    ax_work.text(0.4, 2.45, "3x -  y =  4", fontsize=12, color=TEXT, fontweight="bold")
    ax_work.plot([0.3, 4.8], [2.05, 2.05], color=TEAL, lw=2)
    ax_work.text(5.0, 2.05, "subtract", fontsize=9, color=TEAL, va="center", fontweight="bold")
    ax_work.text(0.4, 1.55, "3y = 12", fontsize=12, color=TEAL, fontweight="bold")
    ax_work.text(0.4, 1.05, "y = 4", fontsize=12, color=GREEN, fontweight="bold")
    ax_work.text(0.4, 0.45, "3x - 4 = 4  ->  x = 8/3", fontsize=11, color=GREEN, fontweight="bold")
    ax_work.set_title("Elimination: cancel x", fontsize=11, fontweight="bold", pad=8)

    _off(ax_after)
    ax_after.set_xlim(0, 5)
    ax_after.set_ylim(0, 4)
    _flow_steps(
        ax_after,
        [
            ("System", "x + 2y = 7", TEXT),
            ("System", "3x - 2y = 5", TEXT),
            ("Add equations", "4x = 12  ->  x = 3", TEAL),
            ("Back-sub", "3 + 2y = 7  ->  y = 2", GREEN),
        ],
        x0=0.35,
        y0=3.5,
        dy=0.78,
    )
    ax_after.set_title("Sometimes multiply first", fontsize=11, fontweight="bold", pad=8)
    fig.suptitle("Elimination method", fontsize=13, fontweight="bold", y=1.02)
    fig.subplots_adjust(wspace=0.25, top=0.88)
    _save(fig, "activity_15_elimination.png")


def activity_15_tickets_example():
    fig = plt.figure(figsize=(8, 5))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.1, 1.4], hspace=0.35)
    ax_top = fig.add_subplot(gs[0])
    ax_bot = fig.add_subplot(gs[1])
    _off(ax_top)
    ax_top.set_xlim(0, 10)
    ax_top.set_ylim(0, 3)
    _flow_steps(
        ax_top,
        [
            ("Define variables", "c = child tickets,  a = adult tickets", TEXT),
            ("Equation 1 (quantity)", "c + a = 10", BLUE),
            ("Equation 2 (cost)", "8c + 12a = 100", ORANGE),
            ("Substitute c = 10 - a", "8(10-a) + 12a = 100", TEAL),
            ("Solve", "a = 5,  c = 5", GREEN),
        ],
        x0=0.5,
        y0=2.7,
        dy=0.52,
    )

    labels = ["Child ($8)", "Adult ($12)"]
    counts = [5, 5]
    ax_bot.set_facecolor(BG)
    bars = ax_bot.bar(labels, counts, color=[BLUE, ORANGE], edgecolor=TEXT, width=0.45)
    ax_bot.set_ylabel("Tickets", fontsize=10)
    ax_bot.set_ylim(0, 7)
    for bar, c in zip(bars, counts):
        ax_bot.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.25,
            str(c),
            ha="center",
            fontsize=12,
            fontweight="bold",
        )
    ax_bot.text(0.5, 6.5, "Check: 5(8) + 5(12) = 40 + 60 = 100", ha="center", fontsize=10, color=TEAL)
    ax_bot.set_title("Solution: 5 child and 5 adult", fontsize=11, fontweight="bold")
    fig.suptitle("Real-world system: ticket problem", fontsize=13, fontweight="bold", y=0.98)
    _save(fig, "activity_15_tickets_example.png")


GENERATORS: dict[int, list[tuple[str, callable]]] = {
    10: [
        ("activity_10_balance_scale.png", activity_10_balance_scale),
        ("activity_10_solve_steps.png", activity_10_solve_steps),
        ("activity_10_solution_types.png", activity_10_solution_types),
    ],
    11: [
        ("activity_11_change_in_y_x.png", activity_11_change_in_y_x),
        ("activity_11_rate_context.png", activity_11_rate_context),
    ],
    12: [
        ("activity_12_y_mx_b.png", activity_12_y_mx_b),
        ("activity_12_graph_example.png", activity_12_graph_example),
    ],
    13: [
        ("activity_13_proportional_vs_not.png", activity_13_proportional_vs_not),
        ("activity_13_table_constant.png", activity_13_table_constant),
    ],
    14: [
        ("activity_14_intersection.png", activity_14_intersection),
        ("activity_14_parallel.png", activity_14_parallel),
        ("activity_14_three_cases.png", activity_14_three_cases),
    ],
    15: [
        ("activity_15_substitution.png", activity_15_substitution),
        ("activity_15_elimination.png", activity_15_elimination),
        ("activity_15_tickets_example.png", activity_15_tickets_example),
    ],
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--activity", type=int, default=None, help="Generate one activity (10–15)")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    acts = [args.activity] if args.activity else list(range(10, 16))
    for act in acts:
        if act not in GENERATORS:
            print(f"No generators for activity {act}")
            continue
        print(f"\nActivity {act}:")
        for name, fn in GENERATORS[act]:
            path = os.path.join(OUT_DIR, name)
            if os.path.exists(path) and not args.force:
                print(f"  skip {name}")
                continue
            fn()


if __name__ == "__main__":
    main()
