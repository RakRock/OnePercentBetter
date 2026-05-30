"""
Generate matplotlib diagrams for Course 3 Unit 5 (Activities 32–35).

Usage:
    python generate_unit5_diagrams.py
    python generate_unit5_diagrams.py --activity 33 --force
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunCourse3", "images", "unit_5")
DPI = 150
BG = "#ffffff"
BLUE = "#3b82f6"
ORANGE = "#f97316"
GREEN = "#22c55e"
TEAL = "#0d9488"
RED = "#ef4444"
GRID = "#e5e7eb"


def _save(fig, name: str) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"  saved {path}")


# Activity 32
def activity_32_scatter_association():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_facecolor(BG)
    hw = np.array([11, 13, 15, 19, 21, 28, 32])
    score = np.array([100, 90, 85, 85, 88, 75, 66])
    ax.scatter(hw, score, color=BLUE, s=70, zorder=3)
    z = np.polyfit(hw, score, 1)
    x = np.linspace(10, 34, 30)
    ax.plot(x, np.polyval(z, x), color=TEAL, lw=2)
    ax.set_xlabel("Hours of TV per week")
    ax.set_ylabel("Test score")
    ax.grid(True, color=GRID, alpha=0.6)
    ax.text(22, 95, "Negative association", fontsize=10, color=ORANGE, fontweight="bold")
    fig.suptitle("Scatter plot: TV hours vs test score", fontsize=13, fontweight="bold")
    _save(fig, "activity_32_scatter_association.png")


def activity_32_association_types():
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    x = np.linspace(0, 10, 30)
    axes[0].set_facecolor(BG)
    axes[0].scatter(x, 2 * x + 3, color=GREEN, s=25)
    axes[0].plot(x, 2 * x + 3, color=GREEN, lw=2)
    axes[0].set_title("Positive association", fontsize=10, fontweight="bold")
    axes[0].grid(True, color=GRID, alpha=0.5)
    axes[1].set_facecolor(BG)
    axes[1].scatter(x, -x + 12, color=RED, s=25)
    axes[1].plot(x, -x + 12, color=RED, lw=2)
    axes[1].set_title("Negative association", fontsize=10, fontweight="bold")
    axes[1].grid(True, color=GRID, alpha=0.5)
    fig.suptitle("Direction of association", fontsize=13, fontweight="bold")
    fig.subplots_adjust(wspace=0.3)
    _save(fig, "activity_32_association_types.png")


# Activity 33
def activity_33_bivariate_scatter():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_facecolor(BG)
    bands = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    jump = np.array([12, 18, 24, 30, 36, 42, 48, 54])
    ax.scatter(bands, jump, color=BLUE, s=70)
    ax.plot(bands, jump, color=TEAL, lw=2)
    ax.set_xlabel("Rubber bands")
    ax.set_ylabel("Bungee jump length")
    ax.grid(True, color=GRID, alpha=0.6)
    fig.suptitle("Bivariate data: two variables per observation", fontsize=13, fontweight="bold")
    _save(fig, "activity_33_bivariate_scatter.png")


def activity_33_trend_line():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_facecolor(BG)
    age = np.array([10, 20, 30, 40, 50, 60])
    calls = np.array([8, 6, 5, 4, 3, 2])
    ax.scatter(age, calls, color=BLUE, s=70)
    z = np.polyfit(age, calls, 1)
    x = np.linspace(8, 62, 30)
    ax.plot(x, np.polyval(z, x), color=ORANGE, lw=2.5, label="trend line")
    ax.set_xlabel("Age (years)")
    ax.set_ylabel("Cell phone calls per day")
    ax.legend(fontsize=9)
    ax.grid(True, color=GRID, alpha=0.6)
    fig.suptitle("Trend line for prediction", fontsize=13, fontweight="bold")
    _save(fig, "activity_33_trend_line.png")


# Activity 34
def activity_34_median_median():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_facecolor(BG)
    x = np.array([0, 2, 5, 9, 12, 16, 20])
    y = np.array([80, 85, 99, 120, 130, 171, 196])
    ax.scatter(x, y, color=BLUE, s=60)
    # illustrative median-median line
    ax.plot([0, 20], [82, 188], color=ORANGE, lw=2.5, label="median-median line")
    ax.set_xlabel("Hours playing video games")
    ax.set_ylabel("Score on new game")
    ax.legend(fontsize=9)
    ax.grid(True, color=GRID, alpha=0.6)
    fig.suptitle("Median-median line on a scatter plot", fontsize=13, fontweight="bold")
    _save(fig, "activity_34_median_median.png")


def activity_34_three_groups():
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_facecolor(BG)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.text(0.5, 3.2, "1. Divide data into 3 groups by x-values", fontsize=11, fontweight="bold", color=BLUE)
    ax.text(0.5, 2.3, "2. Find median (x, y) in each group -> L, M, G", fontsize=10)
    ax.text(0.5, 1.4, "3. Line through L and G; adjust to pass near M", fontsize=10)
    ax.text(0.5, 0.5, "4. Write equation y = mx + b", fontsize=10, color=TEAL)
    fig.suptitle("Steps for median-median line", fontsize=13, fontweight="bold")
    _save(fig, "activity_34_three_groups.png")


# Activity 35
def activity_35_two_way_table():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.set_facecolor(BG)
    ax.axis("off")
    table = [
        ["", "Burger", "Pizza", "Total"],
        ["Offense", "21", "23", "44"],
        ["Defense", "9", "35", "44"],
        ["Total", "30", "58", "88"],
    ]
    tbl = ax.table(cellText=table, loc="center", cellLoc="center")
    tbl.scale(1.2, 1.8)
    for (i, j), cell in tbl.get_celld().items():
        cell.set_facecolor(BG if i == 0 or j == 0 else "#eff6ff")
        cell.set_edgecolor(GRID)
    fig.suptitle("Two-way table: two categorical variables", fontsize=13, fontweight="bold")
    _save(fig, "activity_35_two_way_table.png")


def activity_35_segmented_bar():
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_facecolor(BG)
    grades = ["6th", "7th", "8th"]
    participate = [64, 50, 25]
    not_part = [36, 50, 75]
    x = np.arange(len(grades))
    ax.bar(x, participate, color=GREEN, label="Participate")
    ax.bar(x, not_part, bottom=participate, color=ORANGE, label="Do not participate")
    ax.set_xticks(x)
    ax.set_xticklabels(grades)
    ax.set_ylabel("Row percent (%)")
    ax.set_ylim(0, 100)
    ax.legend(fontsize=9)
    fig.suptitle("Segmented bar graph (row percentages)", fontsize=13, fontweight="bold")
    _save(fig, "activity_35_segmented_bar.png")


GENERATORS: dict[int, list[tuple[str, callable]]] = {
    32: [
        ("activity_32_scatter_association.png", activity_32_scatter_association),
        ("activity_32_association_types.png", activity_32_association_types),
    ],
    33: [
        ("activity_33_bivariate_scatter.png", activity_33_bivariate_scatter),
        ("activity_33_trend_line.png", activity_33_trend_line),
    ],
    34: [
        ("activity_34_median_median.png", activity_34_median_median),
        ("activity_34_three_groups.png", activity_34_three_groups),
    ],
    35: [
        ("activity_35_two_way_table.png", activity_35_two_way_table),
        ("activity_35_segmented_bar.png", activity_35_segmented_bar),
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
