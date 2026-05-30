"""
Generate clean, student-friendly Activity 9 diagrams (matplotlib).
No Hugging Face — crisp grids and labels for Writing Expressions.

Usage:
    python generate_activity9_diagrams.py
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunCourse3", "images", "unit_2")
DPI = 150
BG = "#ffffff"
BLUE = "#3b82f6"
ORANGE = "#f97316"
PURPLE = "#8b5cf6"
GREEN = "#22c55e"
TEAL = "#0d9488"
GRID = "#e5e7eb"
TEXT = "#1f2937"
MUTED = "#6b7280"


def _save(fig, name: str) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"  saved {path}")


def _style_ax(ax):
    ax.set_facecolor(BG)
    ax.axis("off")


def constant_difference():
    """Figure 1, 2, 3 tile stacks with +3 between."""
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.2))
    counts = [2, 5, 8]
    labels = ["Figure 1", "Figure 2", "Figure 3"]
    for ax, n, lab in zip(axes, counts, labels):
        _style_ax(ax)
        ax.set_xlim(0, 4)
        ax.set_ylim(0, n + 1)
        for row in range(n):
            rect = FancyBboxPatch(
                (1.2, row + 0.3),
                1.6,
                0.75,
                boxstyle="round,pad=0.02",
                facecolor=BLUE,
                edgecolor="#1d4ed8",
                linewidth=1.2,
            )
            ax.add_patch(rect)
        ax.text(2, n + 0.85, f"{n} tiles", ha="center", fontsize=11, color=TEXT, fontweight="bold")
        ax.text(2, -0.35, lab, ha="center", fontsize=12, color=TEXT, fontweight="bold")
    fig.suptitle("Constant difference: +3 tiles each step", fontsize=13, color=TEXT, fontweight="bold", y=1.02)
    fig.text(0.5, 0.02, "Expression: 2 + 3(n − 1)", ha="center", fontsize=11, color=TEAL, style="italic")
    # arrows between subplots
    fig.text(0.33, 0.55, "+3", ha="center", fontsize=14, color=GREEN, fontweight="bold")
    fig.text(0.66, 0.55, "+3", ha="center", fontsize=14, color=GREEN, fontweight="bold")
    fig.subplots_adjust(wspace=0.35, top=0.82, bottom=0.12)
    _save(fig, "activity_9_constant_difference.png")


def square_numbers():
    fig, axes = plt.subplots(1, 3, figsize=(9, 3))
    sizes = [1, 2, 3]
    for ax, n in zip(axes, sizes):
        _style_ax(ax)
        ax.set_aspect("equal")
        ax.set_xlim(-0.5, n + 0.5)
        ax.set_ylim(-0.5, n + 0.5)
        for r in range(n):
            for c in range(n):
                ax.add_patch(
                    Rectangle(
                        (c, n - 1 - r),
                        0.92,
                        0.92,
                        facecolor=ORANGE,
                        edgecolor="#c2410c",
                        linewidth=1,
                    )
                )
        ax.text(n / 2 - 0.46, -0.9, f"n = {n}  →  {n}² = {n*n}", ha="center", fontsize=11, color=TEXT)
    fig.suptitle("Square numbers: n × n grid", fontsize=13, color=TEXT, fontweight="bold", y=1.02)
    fig.subplots_adjust(wspace=0.3, top=0.85)
    _save(fig, "activity_9_square_numbers.png")


def rectangular_numbers():
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.2))
    dims = [(1, 2), (2, 3), (3, 4)]
    for ax, (rows, cols) in zip(axes, dims):
        _style_ax(ax)
        ax.set_aspect("equal")
        ax.set_xlim(-0.5, cols + 0.5)
        ax.set_ylim(-0.5, rows + 0.5)
        for r in range(rows):
            for c in range(cols):
                ax.add_patch(
                    Rectangle(
                        (c, rows - 1 - r),
                        0.92,
                        0.92,
                        facecolor=PURPLE,
                        edgecolor="#6d28d9",
                        linewidth=1,
                    )
                )
        total = rows * cols
        ax.text(cols / 2 - 0.46, -0.85, f"{rows}×{cols} = {total}", ha="center", fontsize=10, color=TEXT)
    fig.suptitle("Rectangular numbers: n × (n + 1)", fontsize=13, color=TEXT, fontweight="bold", y=1.02)
    fig.text(0.5, 0.02, "Expression: n(n + 1)", ha="center", fontsize=11, color=TEAL, style="italic")
    fig.subplots_adjust(wspace=0.3, top=0.82, bottom=0.14)
    _save(fig, "activity_9_rectangular_numbers.png")


def triangular_numbers():
    fig, axes = plt.subplots(1, 4, figsize=(10, 3))
    counts = [1, 3, 6, 10]
    for ax, n_rows, total in zip(axes, [1, 2, 3, 4], counts):
        _style_ax(ax)
        ax.set_aspect("equal")
        w = 4
        ax.set_xlim(-0.5, w + 0.5)
        ax.set_ylim(-0.5, n_rows + 1)
        idx = 0
        for row in range(n_rows):
            row_w = row + 1
            offset = (w - row_w) / 2
            for col in range(row_w):
                ax.add_patch(
                    mpatches.Circle(
                        (offset + col + 0.5, n_rows - row - 0.5),
                        0.28,
                        facecolor=GREEN,
                        edgecolor="#15803d",
                        linewidth=1,
                    )
                )
                idx += 1
        ax.text(w / 2, -0.35, f"n={n_rows}\n{total} dots", ha="center", fontsize=9, color=TEXT)
    fig.suptitle("Triangular numbers", fontsize=13, color=TEXT, fontweight="bold", y=1.02)
    fig.text(0.5, 0.02, "Expression: n(n + 1) / 2", ha="center", fontsize=11, color=TEAL, style="italic")
    fig.subplots_adjust(wspace=0.25, top=0.82, bottom=0.16)
    _save(fig, "activity_9_triangular_numbers.png")


def table_to_expression():
    fig, ax = plt.subplots(figsize=(8, 3.5))
    _style_ax(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)

    # Table
    headers = ["Step n", "Tiles"]
    rows = [("1", "4"), ("2", "9"), ("3", "14"), ("4", "19")]
    table_left, table_top = 0.5, 4.2
    col_w = [1.2, 1.2]
    row_h = 0.65
    for j, h in enumerate(headers):
        ax.add_patch(
            Rectangle(
                (table_left + sum(col_w[:j]), table_top - row_h),
                col_w[j],
                row_h,
                facecolor=TEAL,
                edgecolor=TEXT,
                linewidth=1,
            )
        )
        ax.text(
            table_left + sum(col_w[:j]) + col_w[j] / 2,
            table_top - row_h / 2,
            h,
            ha="center",
            va="center",
            fontsize=11,
            color="white",
            fontweight="bold",
        )
    for i, row in enumerate(rows):
        y = table_top - (i + 2) * row_h
        for j, cell in enumerate(row):
            ax.add_patch(
                Rectangle(
                    (table_left + sum(col_w[:j]), y),
                    col_w[j],
                    row_h,
                    facecolor="#f0fdfa" if i % 2 == 0 else BG,
                    edgecolor=GRID,
                    linewidth=1,
                )
            )
            ax.text(
                table_left + sum(col_w[:j]) + col_w[j] / 2,
                y + row_h / 2,
                cell,
                ha="center",
                va="center",
                fontsize=11,
                color=TEXT,
            )

    # Difference annotation
    ax.annotate(
        "",
        xy=(3.0, 2.8),
        xytext=(3.0, 3.45),
        arrowprops=dict(arrowstyle="<->", color=GREEN, lw=2),
    )
    ax.text(3.35, 3.12, "difference\n= 5", fontsize=10, color=GREEN, fontweight="bold", va="center")

    # Formula box
    formula_box = FancyBboxPatch(
        (5.2, 1.2),
        4.2,
        2.8,
        boxstyle="round,pad=0.08",
        facecolor="#eff6ff",
        edgecolor=BLUE,
        linewidth=2,
    )
    ax.add_patch(formula_box)
    ax.text(7.3, 3.3, "From the table", ha="center", fontsize=11, color=MUTED)
    ax.text(7.3, 2.65, "first term = 4", ha="center", fontsize=12, color=TEXT)
    ax.text(7.3, 2.15, "difference = 5", ha="center", fontsize=12, color=TEXT)
    ax.text(7.3, 1.55, "4 + 5(n − 1)", ha="center", fontsize=14, color=BLUE, fontweight="bold")

    fig.suptitle("Table → expression", fontsize=13, color=TEXT, fontweight="bold", y=0.98)
    _save(fig, "activity_9_table_to_expression.png")


def example_1():
    """Example 1: 4 tiles, +5 each figure; highlight figure 6 = 29."""
    first, diff = 4, 5
    figures = list(range(1, 7))
    counts = [first + diff * (n - 1) for n in figures]

    fig = plt.figure(figsize=(10, 4.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1], wspace=0.28)

    # Left: tile stacks for figures 1–3 (readable sizes)
    ax_stacks = fig.add_subplot(gs[0, 0])
    _style_ax(ax_stacks)
    ax_stacks.set_xlim(0, 10)
    ax_stacks.set_ylim(0, 12)
    show_figs = [1, 2, 3]
    x_positions = [1.5, 4.5, 7.5]
    for x0, n in zip(x_positions, show_figs):
        cnt = counts[n - 1]
        for row in range(min(cnt, 10)):
            ax_stacks.add_patch(
                FancyBboxPatch(
                    (x0 - 0.55, row * 0.55 + 0.4),
                    1.1,
                    0.48,
                    boxstyle="round,pad=0.02",
                    facecolor=BLUE,
                    edgecolor="#1d4ed8",
                    linewidth=1,
                )
            )
        if cnt > 10:
            ax_stacks.text(x0, 6.2, f"+{cnt - 10} more", ha="center", fontsize=8, color=MUTED)
        ax_stacks.text(x0, -0.15, f"Figure {n}", ha="center", fontsize=11, fontweight="bold", color=TEXT)
        ax_stacks.text(x0, min(cnt, 10) * 0.55 + 0.95, f"{cnt} tiles", ha="center", fontsize=10, color=TEAL)
    ax_stacks.text(3.0, 11.2, "+5 each figure", ha="center", fontsize=11, color=GREEN, fontweight="bold")
    ax_stacks.annotate("", xy=(3.0, 5.5), xytext=(1.5, 5.5), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
    ax_stacks.annotate("", xy=(6.0, 7.0), xytext=(4.5, 7.0), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
    ax_stacks.text(2.25, 5.8, "+5", fontsize=10, color=GREEN, fontweight="bold")
    ax_stacks.text(5.25, 7.3, "+5", fontsize=10, color=GREEN, fontweight="bold")

    # Right: bar chart figures 1–6, highlight figure 6
    ax_bar = fig.add_subplot(gs[0, 1])
    ax_bar.set_facecolor(BG)
    colors = [BLUE] * 5 + [ORANGE]
    bars = ax_bar.bar(figures, counts, color=colors, edgecolor=TEXT, linewidth=1, width=0.65)
    ax_bar.set_xticks(figures)
    ax_bar.set_xticklabels([f"Fig {n}" for n in figures], fontsize=10)
    ax_bar.set_ylabel("Number of tiles", fontsize=10, color=TEXT)
    ax_bar.set_ylim(0, 34)
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)
    for bar, val in zip(bars, counts):
        ax_bar.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.6,
            str(val),
            ha="center",
            fontsize=10,
            fontweight="bold",
            color=TEXT,
        )
    ax_bar.annotate(
        "Figure 6\n4 + 5(6−1) = 29",
        xy=(6, 29),
        xytext=(4.2, 31),
        fontsize=10,
        color="#c2410c",
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5),
    )
    for i in range(5):
        ax_bar.text(i + 1.5, counts[i] + 2.5, "+5", ha="center", fontsize=8, color=GREEN)

    fig.suptitle(
        "Example 1: Start with 4 tiles, add 5 each figure",
        fontsize=13,
        color=TEXT,
        fontweight="bold",
        y=1.02,
    )
    fig.text(
        0.5,
        0.02,
        "Expression: 4 + 5(n − 1)   •   Figure 6: 4 + 5(5) = 29 tiles",
        ha="center",
        fontsize=11,
        color=TEAL,
        style="italic",
    )
    fig.subplots_adjust(top=0.88, bottom=0.14, left=0.06, right=0.98)
    _save(fig, "activity_9_example_1.png")


def main():
    print("Generating Activity 9 diagrams (matplotlib)...\n")
    constant_difference()
    square_numbers()
    rectangular_numbers()
    triangular_numbers()
    table_to_expression()
    example_1()
    print(f"\nDone → {OUT_DIR}/")


if __name__ == "__main__":
    main()
