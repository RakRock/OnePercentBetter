"""
Generate matplotlib diagrams for Course 3 Unit 1 (Activities 1–8).

Usage:
    python generate_unit1_diagrams.py
    python generate_unit1_diagrams.py --activity 3 --force
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunCourse3", "images", "unit_1")
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


# Activity 1
def activity_1_sequence_pattern():
    fig, ax = plt.subplots(figsize=(8, 3))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    terms = [3, 7, 11, 15, 19]
    for i, v in enumerate(terms):
        x = 1 + i * 1.8
        ax.add_patch(Circle((x, 1.5), 0.35, facecolor=BLUE, alpha=0.2, edgecolor=BLUE, lw=2))
        ax.text(x, 1.5, str(v), ha="center", va="center", fontsize=12, fontweight="bold")
        if i < len(terms) - 1:
            ax.annotate("+4", xy=(x + 0.9, 2.2), fontsize=10, color=TEAL, ha="center")
    ax.text(5, 2.6, "Constant difference: +4 each term", ha="center", fontsize=11, color=TEXT)
    fig.suptitle("Arithmetic sequence: 3, 7, 11, 15, …", fontsize=13, fontweight="bold")
    _save(fig, "activity_1_sequence_pattern.png")


def activity_1_fibonacci():
    fig, ax = plt.subplots(figsize=(8, 3))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    fib = [1, 1, 2, 3, 5, 8, 13]
    for i, v in enumerate(fib):
        x = 0.6 + i * 1.25
        ax.add_patch(FancyBboxPatch((x - 0.4, 0.9), 0.8, 0.9, boxstyle="round", facecolor=ORANGE, alpha=0.15, edgecolor=ORANGE))
        ax.text(x, 1.35, str(v), ha="center", fontsize=11, fontweight="bold")
    ax.text(5, 2.5, "Each term = sum of previous two", ha="center", fontsize=11, color=TEAL)
    fig.suptitle("Fibonacci sequence", fontsize=13, fontweight="bold")
    _save(fig, "activity_1_fibonacci.png")


# Activity 2
def activity_2_add_fractions():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    _off(ax)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 4)
    ax.text(0.5, 3.2, "3/5 + 4/6", fontsize=12, fontweight="bold")
    ax.text(0.5, 2.5, "LCD = 6  ->  9/6 + 4/6 = 13/6", fontsize=11, color=TEAL)
    ax.text(0.5, 1.8, "13/6 = 2 1/6", fontsize=11, color=GREEN, fontweight="bold")
    for i, (w, c, lab) in enumerate([(0.5, 0.5, "3/5"), (1.2, 0.33, "4/6"), (2.1, 0.83, "13/6")]):
        ax.barh(0.6, w, left=2.5 + i * 1.1, height=0.5, color=[BLUE, ORANGE, GREEN][i], alpha=0.6)
        ax.text(2.5 + i * 1.1 + w / 2, 0.35, lab, ha="center", fontsize=9)
    fig.suptitle("Add fractions: common denominator", fontsize=13, fontweight="bold")
    _save(fig, "activity_2_add_fractions.png")


def activity_2_multiply_fractions():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    _off(ax)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 4)
    ax.text(0.5, 3.0, "2/5 x 7/12", fontsize=12, fontweight="bold")
    ax.text(0.5, 2.3, "Multiply tops: 2 x 7 = 14", fontsize=10, color=BLUE)
    ax.text(0.5, 1.8, "Multiply bottoms: 5 x 12 = 60", fontsize=10, color=ORANGE)
    ax.text(0.5, 1.2, "14/60 = 7/30", fontsize=11, color=GREEN, fontweight="bold")
    fig.suptitle("Multiply fractions", fontsize=13, fontweight="bold")
    _save(fig, "activity_2_multiply_fractions.png")


# Activity 3
def activity_3_square_area():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_facecolor(BG)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_aspect("equal")
    for i in range(7):
        for j in range(7):
            ax.add_patch(Rectangle((i, j), 1, 1, facecolor=BLUE, alpha=0.25, edgecolor=BLUE))
    ax.text(3.5, -0.8, "side = 7  ->  area = 7^2 = 49", ha="center", fontsize=11, fontweight="bold")
    fig.suptitle("Square area = side squared", fontsize=13, fontweight="bold")
    _save(fig, "activity_3_square_area.png")


def activity_3_cube_volume():
    fig, ax = plt.subplots(figsize=(6, 4))
    _off(ax)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.text(0.5, 3.0, "Cube: edge c", fontsize=12, fontweight="bold")
    ax.text(0.5, 2.3, "Volume = c x c x c = c^3", fontsize=11, color=TEAL)
    ax.text(0.5, 1.6, "Example: c = 5  ->  V = 125", fontsize=11, color=GREEN, fontweight="bold")
    ax.add_patch(FancyBboxPatch((3.2, 0.8), 2.2, 2.2, boxstyle="round", facecolor=PURPLE, alpha=0.12, edgecolor=PURPLE, lw=2))
    ax.text(4.3, 1.9, "5^3", ha="center", fontsize=16, fontweight="bold", color=PURPLE)
    fig.suptitle("Cube volume", fontsize=13, fontweight="bold")
    _save(fig, "activity_3_cube_volume.png")


# Activity 4
def activity_4_frac_decimal_percent():
    fig, ax = plt.subplots(figsize=(8, 3))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.text(1, 2.2, "3/5", fontsize=14, fontweight="bold", color=BLUE)
    ax.annotate("", xy=(4, 2.2), xytext=(2, 2.2), arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.text(4.2, 2.2, "0.6", fontsize=14, fontweight="bold", color=TEAL)
    ax.annotate("", xy=(7, 2.2), xytext=(5, 2.2), arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.text(7.2, 2.2, "60%", fontsize=14, fontweight="bold", color=GREEN)
    ax.text(5, 0.8, "Divide: fraction -> decimal   Multiply by 100: -> percent", ha="center", fontsize=10, color=MUTED)
    fig.suptitle("Fraction, decimal, percent", fontsize=13, fontweight="bold")
    _save(fig, "activity_4_frac_decimal_percent.png")


def activity_4_repeating_decimal():
    fig, ax = plt.subplots(figsize=(7, 3))
    _off(ax)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 3)
    ax.text(0.5, 2.2, "1/3 = 0.3333... = 0.3 bar", fontsize=12, fontweight="bold")
    ax.text(0.5, 1.4, "Repeating decimal = rational number", fontsize=11, color=TEAL)
    ax.text(0.5, 0.6, "Non-terminating, NON-repeating = irrational", fontsize=11, color=RED)
    fig.suptitle("Repeating vs non-repeating decimals", fontsize=13, fontweight="bold")
    _save(fig, "activity_4_repeating_decimal.png")


# Activity 5
def activity_5_sqrt_number_line():
    fig, ax = plt.subplots(figsize=(8, 2.5))
    ax.set_facecolor(BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axhline(1, color=GRID, lw=1)
    for v, lab in [(0, "0"), (2, "sqrt(4)=2"), (2.45, "sqrt(6)"), (3, "sqrt(9)=3"), (4, "sqrt(16)=4")]:
        ax.plot(v * 2, 1, "o", color=BLUE if "sqrt" in lab else TEXT, ms=8)
        ax.text(v * 2, 0.5, lab, ha="center", fontsize=8, rotation=15)
    ax.text(5, 1.7, "sqrt(6) is between sqrt(4)=2 and sqrt(9)=3", ha="center", fontsize=10, color=TEAL)
    ax.axis("off")
    fig.suptitle("Estimate square roots on a number line", fontsize=13, fontweight="bold")
    _save(fig, "activity_5_sqrt_number_line.png")


def activity_5_rational_irrational():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    _off(ax)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 4)
    ax.add_patch(FancyBboxPatch((0.4, 1.2), 3, 2.2, boxstyle="round", facecolor=BLUE, alpha=0.1, edgecolor=BLUE, lw=2))
    ax.text(1.9, 2.6, "Rational", ha="center", fontweight="bold")
    ax.text(1.9, 2.0, "p/q, terminating or\nrepeating decimals", ha="center", fontsize=9)
    ax.add_patch(FancyBboxPatch((3.6, 1.2), 3, 2.2, boxstyle="round", facecolor=ORANGE, alpha=0.1, edgecolor=ORANGE, lw=2))
    ax.text(5.1, 2.6, "Irrational", ha="center", fontweight="bold")
    ax.text(5.1, 2.0, "pi, sqrt(2), sqrt(3)...\nnon-repeating decimals", ha="center", fontsize=9)
    fig.suptitle("Rational vs irrational", fontsize=13, fontweight="bold")
    _save(fig, "activity_5_rational_irrational.png")


# Activity 6
def activity_6_product_rule():
    fig, ax = plt.subplots(figsize=(7, 3))
    _off(ax)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 3.5)
    ax.text(0.5, 2.6, "Same base: multiply", fontsize=12, fontweight="bold")
    ax.text(0.5, 1.9, "3^5 x 3^4 = 3^(5+4) = 3^9", fontsize=12, color=TEAL)
    ax.text(0.5, 1.1, "Add exponents when multiplying", fontsize=11, color=GREEN)
    fig.suptitle("Product rule for exponents", fontsize=13, fontweight="bold")
    _save(fig, "activity_6_product_rule.png")


def activity_6_negative_exponent():
    fig, ax = plt.subplots(figsize=(7, 3))
    _off(ax)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 3.5)
    ax.text(0.5, 2.6, "Negative exponent = reciprocal", fontsize=12, fontweight="bold")
    ax.text(0.5, 1.8, "3^-2 = 1 / 3^2 = 1/9", fontsize=12, color=TEAL)
    ax.text(0.5, 1.0, "a^-n = 1 / a^n  (a not 0)", fontsize=11, color=GREEN)
    fig.suptitle("Negative exponents", fontsize=13, fontweight="bold")
    _save(fig, "activity_6_negative_exponent.png")


# Activity 7
def activity_7_sci_notation_form():
    fig, ax = plt.subplots(figsize=(8, 3))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.text(0.5, 2.3, "25,000,000,000  =  2.5 x 10^10", fontsize=12, fontweight="bold", color=BLUE)
    ax.text(0.5, 1.5, "1 <= |coefficient| < 10", fontsize=11, color=TEAL)
    ax.text(0.5, 0.7, "Power of 10 shows how far to move the decimal", fontsize=10, color=MUTED)
    fig.suptitle("Scientific notation form", fontsize=13, fontweight="bold")
    _save(fig, "activity_7_sci_notation_form.png")


def activity_7_standard_form():
    fig, ax = plt.subplots(figsize=(7, 3))
    _off(ax)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 3)
    ax.text(0.5, 2.2, "8.92 x 10^8", fontsize=12, fontweight="bold")
    ax.text(0.5, 1.4, "Move decimal 8 places right", fontsize=11, color=TEAL)
    ax.text(0.5, 0.6, "= 892,000,000", fontsize=12, color=GREEN, fontweight="bold")
    fig.suptitle("Scientific notation to standard form", fontsize=13, fontweight="bold")
    _save(fig, "activity_7_standard_form.png")


# Activity 8
def activity_8_multiply_sci():
    fig, ax = plt.subplots(figsize=(8, 3))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.5)
    ax.text(0.5, 2.7, "(2.2 x 10^5)(4 x 10^7)", fontsize=11, fontweight="bold")
    ax.text(0.5, 2.0, "Multiply coefficients: 2.2 x 4 = 8.8", fontsize=10, color=BLUE)
    ax.text(0.5, 1.4, "Add exponents: 5 + 7 = 12", fontsize=10, color=ORANGE)
    ax.text(0.5, 0.7, "= 8.8 x 10^12", fontsize=12, color=GREEN, fontweight="bold")
    fig.suptitle("Multiply in scientific notation", fontsize=13, fontweight="bold")
    _save(fig, "activity_8_multiply_sci.png")


def activity_8_add_sci():
    fig, ax = plt.subplots(figsize=(8, 3))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.5)
    ax.text(0.5, 2.7, "3.4 x 10^5 + 9.1 x 10^5", fontsize=11, fontweight="bold")
    ax.text(0.5, 1.8, "Same power of 10 -> add coefficients", fontsize=10, color=TEAL)
    ax.text(0.5, 1.0, "(3.4 + 9.1) x 10^5 = 12.5 x 10^5 = 1.25 x 10^6", fontsize=10, color=GREEN)
    fig.suptitle("Add/subtract: match exponents first", fontsize=13, fontweight="bold")
    _save(fig, "activity_8_add_sci.png")


GENERATORS: dict[int, list[tuple[str, callable]]] = {
    1: [("activity_1_sequence_pattern.png", activity_1_sequence_pattern), ("activity_1_fibonacci.png", activity_1_fibonacci)],
    2: [("activity_2_add_fractions.png", activity_2_add_fractions), ("activity_2_multiply_fractions.png", activity_2_multiply_fractions)],
    3: [("activity_3_square_area.png", activity_3_square_area), ("activity_3_cube_volume.png", activity_3_cube_volume)],
    4: [("activity_4_frac_decimal_percent.png", activity_4_frac_decimal_percent), ("activity_4_repeating_decimal.png", activity_4_repeating_decimal)],
    5: [("activity_5_sqrt_number_line.png", activity_5_sqrt_number_line), ("activity_5_rational_irrational.png", activity_5_rational_irrational)],
    6: [("activity_6_product_rule.png", activity_6_product_rule), ("activity_6_negative_exponent.png", activity_6_negative_exponent)],
    7: [("activity_7_sci_notation_form.png", activity_7_sci_notation_form), ("activity_7_standard_form.png", activity_7_standard_form)],
    8: [("activity_8_multiply_sci.png", activity_8_multiply_sci), ("activity_8_add_sci.png", activity_8_add_sci)],
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
