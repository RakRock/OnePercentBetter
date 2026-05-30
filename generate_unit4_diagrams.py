"""
Generate matplotlib diagrams for Course 3 Unit 4 (Activities 27–31).

Usage:
    python generate_unit4_diagrams.py
    python generate_unit4_diagrams.py --activity 30 --force
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunCourse3", "images", "unit_4")
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


def _save(fig, name: str) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"  saved {path}")


def _line_ax(ax, xlim=(-6, 6), ylim=(-6, 6)):
    ax.set_facecolor(BG)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axhline(0, color=GRID, lw=1)
    ax.axvline(0, color=GRID, lw=1)
    ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color(GRID)


# Activity 27
def activity_27_function_mapping():
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_facecolor(BG)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    # domain oval
    ax.add_patch(plt.Circle((2.5, 2.5), 1.8, fill=False, edgecolor=BLUE, lw=2))
    ax.add_patch(plt.Circle((7.5, 2.5), 1.8, fill=False, edgecolor=ORANGE, lw=2))
    ax.text(2.5, 4.2, "Domain (inputs)", ha="center", fontsize=10, fontweight="bold", color=BLUE)
    ax.text(7.5, 4.2, "Range (outputs)", ha="center", fontsize=10, fontweight="bold", color=ORANGE)
    for y, lab in [(3.2, "1"), (2.5, "2"), (1.8, "3")]:
        ax.plot([3.8, 6.2], [y, y], color=TEAL, lw=1.2)
        ax.text(1.8, y, lab, fontsize=11, color=BLUE)
        ax.text(8.2, y, lab, fontsize=11, color=ORANGE)
    ax.text(5, 0.4, "Each input maps to exactly ONE output", ha="center", fontsize=10, color=TEAL)
    fig.suptitle("Function: one output per input", fontsize=13, fontweight="bold")
    _save(fig, "activity_27_function_mapping.png")


def activity_27_domain_range():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.set_facecolor(BG)
    ax.axis("off")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 3.5)
    ax.text(0.4, 2.6, "Domain: all allowed x-values (inputs)", fontsize=11, color=BLUE, fontweight="bold")
    ax.text(0.4, 1.8, "Range: all possible y-values (outputs)", fontsize=11, color=ORANGE, fontweight="bold")
    ax.text(0.4, 0.9, "Function test: no x repeats with different y", fontsize=10, color=TEAL)
    fig.suptitle("Domain and range", fontsize=13, fontweight="bold")
    _save(fig, "activity_27_domain_range.png")


# Activity 28
def activity_28_comparing_graphs():
    fig, ax = plt.subplots(figsize=(6, 5))
    _line_ax(ax, (-1, 8), (-2, 14))
    x = np.linspace(0, 7, 50)
    ax.plot(x, 4 * x, color=BLUE, lw=2, label="y = 4x")
    ax.plot(x, 4 * x + 1, color=ORANGE, lw=2, label="y = 4x + 1")
    ax.plot(x, 2 * x + 2, color=GREEN, lw=2, label="y = 2x + 2")
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("Compare linear models", fontsize=11, fontweight="bold")
    fig.suptitle("Different slopes and y-intercepts", fontsize=13, fontweight="bold")
    _save(fig, "activity_28_comparing_graphs.png")


def activity_28_rate_of_change():
    fig, ax = plt.subplots(figsize=(6, 4))
    _line_ax(ax, (0, 10), (0, 12))
    ax.plot([0, 5], [75, 115], color=BLUE, lw=2.5, marker="o")
    ax.annotate("slope = 8 $/hr", xy=(3, 99), fontsize=10, color=TEAL)
    ax.text(5, 2, "y = 8x + 75 (pay vs hours)", ha="center", fontsize=10, color=TEXT)
    fig.suptitle("Rate of change = slope", fontsize=13, fontweight="bold")
    _save(fig, "activity_28_rate_of_change.png")


# Activity 29
def activity_29_plant_growth():
    fig, ax = plt.subplots(figsize=(6, 5))
    _line_ax(ax, (0, 10), (0, 100))
    days = np.arange(0, 9)
    ax.plot(days, 12 * days, color=GREEN, lw=2, marker="o", label="12 mm/day")
    ax.plot(days, 20 + 6 * days, color=BLUE, lw=2, marker="s", label="20 + 6 mm/day")
    ax.set_xlabel("Days")
    ax.set_ylabel("Height (mm)")
    ax.legend(fontsize=9)
    fig.suptitle("Constructing linear growth functions", fontsize=13, fontweight="bold")
    _save(fig, "activity_29_plant_growth.png")


def activity_29_pattern_perimeter():
    fig, ax = plt.subplots(figsize=(7, 4))
    _line_ax(ax, (0, 8), (0, 20))
    n = np.array([1, 2, 3, 4, 5])
    ax.plot(n, 4 * n, "o-", color=BLUE, lw=2, label="squares: P = 4n")
    ax.plot(n, 2 * n + 2, "s-", color=ORANGE, lw=2, label="touching: P = 2n + 2")
    ax.set_xlabel("Number of tiles")
    ax.set_ylabel("Perimeter")
    ax.legend(fontsize=9)
    fig.suptitle("Pattern → table → equation", fontsize=13, fontweight="bold")
    _save(fig, "activity_29_pattern_perimeter.png")


# Activity 30
def activity_30_linear_graph():
    fig, ax = plt.subplots(figsize=(6, 5))
    _line_ax(ax)
    x = np.linspace(-4, 4, 50)
    ax.plot(x, 2 * x + 1, color=BLUE, lw=2, label="y = 2x + 1")
    ax.plot(x, x**2, color=ORANGE, lw=2, label="y = x^2 (non-linear)")
    ax.legend(fontsize=9)
    fig.suptitle("Linear vs non-linear graphs", fontsize=13, fontweight="bold")
    _save(fig, "activity_30_linear_graph.png")


def activity_30_rate_of_change():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_facecolor(BG)
    ax.axis("off")
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 3.5)
    ax.text(0.4, 2.5, "Linear: rate of change is CONSTANT", fontsize=11, color=BLUE, fontweight="bold")
    ax.text(0.4, 1.6, "From table: (y2 - y1) / (x2 - x1) same every step", fontsize=10)
    ax.text(0.4, 0.7, "From equation y = mx + b: slope m = rate of change", fontsize=10, color=TEAL)
    fig.suptitle("Constant rate of change", fontsize=13, fontweight="bold")
    _save(fig, "activity_30_rate_of_change.png")


# Activity 31
def activity_31_scatter_plot():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_facecolor(BG)
    minutes = np.array([1, 2, 3, 4, 5, 6])
    gallons = 2.25 * minutes
    ax.scatter(minutes, gallons, color=BLUE, s=60, zorder=3)
    ax.plot(minutes, gallons, color=TEAL, lw=2, label="trend")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 16)
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Water (gallons)")
    ax.grid(True, color=GRID, alpha=0.7)
    fig.suptitle("Scatter plot with linear trend", fontsize=13, fontweight="bold")
    _save(fig, "activity_31_scatter_plot.png")


def activity_31_linear_vs_nonlinear():
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    x = np.linspace(0, 5, 40)
    axes[0].set_facecolor(BG)
    axes[0].plot(x, 2.25 * x, color=BLUE, lw=2)
    axes[0].scatter(x[::5], 2.25 * x[::5], color=BLUE)
    axes[0].set_title("Linear (constant rate)", fontsize=10, fontweight="bold")
    axes[0].set_xlabel("time")
    axes[0].grid(True, color=GRID, alpha=0.5)
    axes[1].set_facecolor(BG)
    y_nl = 0.5 * x**1.5 + 0.5
    axes[1].plot(x, y_nl, color=ORANGE, lw=2)
    axes[1].scatter(x[::5], y_nl[::5], color=ORANGE)
    axes[1].set_title("Non-linear (changing rate)", fontsize=10, fontweight="bold")
    axes[1].set_xlabel("time")
    axes[1].grid(True, color=GRID, alpha=0.5)
    fig.suptitle("Linear vs non-linear data", fontsize=13, fontweight="bold")
    fig.subplots_adjust(wspace=0.3)
    _save(fig, "activity_31_linear_vs_nonlinear.png")


GENERATORS: dict[int, list[tuple[str, callable]]] = {
    27: [
        ("activity_27_function_mapping.png", activity_27_function_mapping),
        ("activity_27_domain_range.png", activity_27_domain_range),
    ],
    28: [
        ("activity_28_comparing_graphs.png", activity_28_comparing_graphs),
        ("activity_28_rate_of_change.png", activity_28_rate_of_change),
    ],
    29: [
        ("activity_29_plant_growth.png", activity_29_plant_growth),
        ("activity_29_pattern_perimeter.png", activity_29_pattern_perimeter),
    ],
    30: [
        ("activity_30_linear_graph.png", activity_30_linear_graph),
        ("activity_30_rate_of_change.png", activity_30_rate_of_change),
    ],
    31: [
        ("activity_31_scatter_plot.png", activity_31_scatter_plot),
        ("activity_31_linear_vs_nonlinear.png", activity_31_linear_vs_nonlinear),
    ],
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
