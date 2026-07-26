"""
Generate matplotlib diagrams for Edgenuity Course 3 Unit 5 (lesson + practice).

Usage:
    python generate_edgenuity_unit5_diagrams.py
    python generate_edgenuity_unit5_diagrams.py --practice-only
"""

from __future__ import annotations

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunEdgenuityCourse3", "images", "unit_5")
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
NEG = "#dc2626"


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


def _draw_x_tile(ax, x, y, w=1.4, h=0.45, color=GREEN, label="x", neg=False):
    fc = NEG if neg else color
    rect = Rectangle((x, y), w, h, facecolor=fc, edgecolor=TEXT, lw=1.5, alpha=0.85)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, f"{'−' if neg else ''}{label}", ha="center", va="center",
            fontsize=10, fontweight="bold", color=BG if neg else TEXT)


def _draw_unit_tile(ax, x, y, size=0.42, color=YELLOW, label="1", neg=False):
    fc = NEG if neg else color
    rect = Rectangle((x, y), size, size, facecolor=fc, edgecolor=TEXT, lw=1.5, alpha=0.85)
    ax.add_patch(rect)
    ax.text(x + size / 2, y + size / 2, f"{'−' if neg else ''}{label}", ha="center", va="center",
            fontsize=8, fontweight="bold", color=BG if neg else TEXT)


def _draw_tiles_row(ax, x_start, y, n_x=0, n_unit=0, neg_x=0, neg_unit=0, gap=0.15):
    x = x_start
    for _ in range(n_x):
        _draw_x_tile(ax, x, y)
        x += 1.4 + gap
    for _ in range(n_unit):
        _draw_unit_tile(ax, x, y + 0.015)
        x += 0.42 + gap
    for _ in range(neg_x):
        _draw_x_tile(ax, x, y, neg=True)
        x += 1.4 + gap
    for _ in range(neg_unit):
        _draw_unit_tile(ax, x, y + 0.015, neg=True)
        x += 0.42 + gap
    return x


def _balance_beam(ax, y_beam=3.0):
    ax.plot([1, 9], [y_beam, y_beam], color=TEXT, lw=3)
    ax.plot([5, 5], [y_beam - 1.5, y_beam], color=TEXT, lw=3)
    ax.plot([5, 5], [y_beam - 1.5, y_beam - 1.7], "v", color=TEXT, ms=12)


def _equation_steps(ax, steps, y=0.5, box_h=0.35):
    """Draw horizontal flow of equation steps."""
    n = len(steps)
    for i, (label, eq, color) in enumerate(steps):
        x = 0.05 + i * (0.9 / max(n - 1, 1)) if n > 1 else 0.5
        if n > 1:
            xc = 0.05 + i * (0.9 / (n - 1))
        else:
            xc = 0.5
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
def activity_1_algebra_tiles_balance():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("Algebra tiles: 2x = x + 3", fontsize=12, fontweight="bold", pad=10)
    _balance_beam(ax)
    ax.text(2.5, 3.55, "Left side", ha="center", fontsize=10, color=TEAL, fontweight="bold")
    ax.text(7.5, 3.55, "Right side", ha="center", fontsize=10, color=TEAL, fontweight="bold")
    _draw_tiles_row(ax, 1.5, 2.0, n_x=2)
    _draw_tiles_row(ax, 6.2, 2.0, n_x=1, n_unit=3)
    ax.annotate("", xy=(4.8, 1.3), xytext=(3.2, 1.3),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2))
    ax.annotate("", xy=(6.8, 1.3), xytext=(8.4, 1.3),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2))
    ax.text(4.0, 1.05, "remove 1 x-tile\nfrom each side", ha="center", fontsize=9, color=RED, fontweight="bold")
    ax.text(5, 0.35, "Balance: both sides represent the same value  →  x = 3", ha="center",
            fontsize=10, color=TEXT)
    _save(fig, "activity_1_algebra_tiles_balance.png")


def activity_1_completing_tile_model():
    fig, ax = plt.subplots(figsize=(8, 4.8))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.set_title("Tile model: 3x + 2 = −x + 6  (partial solution)", fontsize=12, fontweight="bold", pad=10)
    ax.text(2.5, 4.9, "Left: 3x + 2", ha="center", fontsize=10, color=BLUE, fontweight="bold")
    ax.text(7.5, 4.9, "Right: −x + 6", ha="center", fontsize=10, color=RED, fontweight="bold")
    _draw_tiles_row(ax, 0.8, 3.5, n_x=3, n_unit=2)
    _draw_tiles_row(ax, 6.0, 3.5, neg_x=1, n_unit=6)
    ax.annotate("", xy=(5.0, 2.6), xytext=(3.5, 2.6),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
    ax.annotate("", xy=(7.0, 2.6), xytext=(8.5, 2.6),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
    ax.text(5.0, 2.35, "+ x to both sides", ha="center", fontsize=9, color=GREEN, fontweight="bold")
    ax.text(2.5, 1.5, "After adding x:\n4x + 2 = 6", ha="center", fontsize=10, color=TEAL,
            bbox=dict(boxstyle="round", facecolor="#eff6ff", edgecolor=BLUE))
    ax.text(7.5, 1.5, "Next: subtract 2\nfrom both sides", ha="center", fontsize=10, color=ORANGE,
            bbox=dict(boxstyle="round", facecolor="#fff7ed", edgecolor=ORANGE))
    ax.text(5, 0.35, "Goal: same tiles on each side, then divide", ha="center", fontsize=9, color=TEXT)
    _save(fig, "activity_1_completing_tile_model.png")


# ── Activity 2 ──
def activity_2_properties_equality():
    fig, ax = plt.subplots(figsize=(8, 4.2))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("Properties of equality — balance both sides", fontsize=12, fontweight="bold", pad=10)
    _balance_beam(ax, y_beam=3.2)
    ax.add_patch(FancyBboxPatch((1.2, 3.45), 2.8, 0.55, boxstyle="round", facecolor=GRID, edgecolor=TEXT))
    ax.text(2.6, 3.72, "5x − 3", ha="center", fontsize=12, fontweight="bold")
    ax.add_patch(FancyBboxPatch((6.0, 3.45), 2.8, 0.55, boxstyle="round", facecolor=GRID, edgecolor=TEXT))
    ax.text(7.4, 3.72, "17", ha="center", fontsize=12, fontweight="bold")
    ax.annotate("", xy=(5, 2.3), xytext=(2.6, 2.3), arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
    ax.annotate("", xy=(5, 2.3), xytext=(7.4, 2.3), arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
    ax.text(3.8, 2.55, "+ 3", fontsize=11, color=GREEN, fontweight="bold")
    ax.text(6.2, 2.55, "+ 3", fontsize=11, color=GREEN, fontweight="bold")
    steps = [("Start", "5x − 3 = 17", BLUE), ("Add 3", "5x = 20", TEAL), ("÷ 5", "x = 4", GREEN)]
    for i, (label, eq, color) in enumerate(steps):
        x = 1.5 + i * 3.0
        ax.add_patch(FancyBboxPatch((x - 1.0, 0.3), 2.0, 1.2, boxstyle="round,pad=0.05",
                                    facecolor=color, alpha=0.12, edgecolor=color, lw=2))
        ax.text(x, 1.15, label, ha="center", fontsize=9, color=TEAL)
        ax.text(x, 0.7, eq, ha="center", fontsize=11, fontweight="bold")
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 1.3, 0.9), xytext=(x + 0.7, 0.9),
                        arrowprops=dict(arrowstyle="->", color=GRID, lw=1.5))
    _save(fig, "activity_2_properties_equality.png")


def activity_2_distributive_model():
    fig, ax = plt.subplots(figsize=(7, 4))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("Distributive property: 8(3x + 40)", fontsize=12, fontweight="bold", pad=10)
    ax.text(5, 4.3, "8(3x + 40)", ha="center", fontsize=14, fontweight="bold", color=BLUE)
    ax.annotate("", xy=(2.5, 3.0), xytext=(4.2, 3.8),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.5))
    ax.annotate("", xy=(7.5, 3.0), xytext=(5.8, 3.8),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.5))
    ax.text(2.5, 2.65, "8 · 3x", ha="center", fontsize=12, fontweight="bold", color=GREEN)
    ax.text(7.5, 2.65, "8 · 40", ha="center", fontsize=12, fontweight="bold", color=GREEN)
    ax.text(2.5, 1.8, "= 24x", ha="center", fontsize=13, fontweight="bold", color=TEAL)
    ax.text(7.5, 1.8, "= 320", ha="center", fontsize=13, fontweight="bold", color=TEAL)
    ax.text(5, 0.8, "8(3x + 40) = 24x + 320", ha="center", fontsize=13, fontweight="bold",
            color=TEXT, bbox=dict(boxstyle="round", facecolor="#f0fdf4", edgecolor=GREEN))
    _save(fig, "activity_2_distributive_model.png")


# ── Activity 3 ──
def activity_3_distribute_negatives():
    fig, ax = plt.subplots(figsize=(7, 4))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("Distributing a negative", fontsize=12, fontweight="bold", pad=10)
    ax.text(5, 4.2, "−(3x − 5)", ha="center", fontsize=14, fontweight="bold", color=RED)
    ax.annotate("", xy=(3.0, 2.8), xytext=(4.5, 3.7),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2.5))
    ax.annotate("", xy=(7.0, 2.8), xytext=(5.5, 3.7),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2.5))
    ax.text(3.0, 2.45, "−3x", ha="center", fontsize=12, fontweight="bold", color=BLUE)
    ax.text(7.0, 2.45, "+ 5", ha="center", fontsize=12, fontweight="bold", color=GREEN)
    ax.text(3.0, 1.7, "sign flips", ha="center", fontsize=9, color=RED, fontstyle="italic")
    ax.text(7.0, 1.7, "sign flips", ha="center", fontsize=9, color=RED, fontstyle="italic")
    ax.text(5, 0.7, "−(3x − 5) = −3x + 5", ha="center", fontsize=13, fontweight="bold",
            color=TEXT, bbox=dict(boxstyle="round", facecolor="#fef2f2", edgecolor=RED))
    _save(fig, "activity_3_distribute_negatives.png")


def activity_3_combine_like_terms():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_title("Combine like terms: 7b + 4b − 1b", fontsize=12, fontweight="bold", pad=10)
    terms = [("7b", BLUE), ("4b", GREEN), ("−1b", RED)]
    for i, (term, color) in enumerate(terms):
        x = 1.5 + i * 2.5
        ax.add_patch(FancyBboxPatch((x - 0.7, 1.5), 1.4, 1.0, boxstyle="round",
                                    facecolor=color, alpha=0.15, edgecolor=color, lw=2))
        ax.text(x, 2.0, term, ha="center", fontsize=14, fontweight="bold", color=color)
        if i < len(terms) - 1:
            ax.text(x + 1.25, 2.0, "+", ha="center", fontsize=16, fontweight="bold", color=TEXT)
    ax.annotate("", xy=(5, 1.0), xytext=(5, 1.4),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
    ax.text(5, 0.55, "= 10b", ha="center", fontsize=16, fontweight="bold", color=TEAL,
            bbox=dict(boxstyle="round", facecolor="#ecfdf5", edgecolor=TEAL))
    ax.text(5, 3.3, "Same variable → add coefficients: 7 + 4 − 1 = 10", ha="center",
            fontsize=10, color=TEXT)
    _save(fig, "activity_3_combine_like_terms.png")


# ── Activity 4 ──
def activity_4_one_solution():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_facecolor(BG)
    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 8)
    ax.axhline(0, color=TEXT, lw=0.8, alpha=0.5)
    ax.axvline(0, color=TEXT, lw=0.8, alpha=0.5)
    ax.grid(True, color=GRID, ls="--", alpha=0.7)
    ax.set_title("One solution", fontsize=12, fontweight="bold")
    x = np.linspace(-0.5, 5.5, 100)
    ax.plot(x, 2 * x - 1, color=BLUE, lw=2.5, label="y = 2x − 1")
    ax.plot(x, -x + 5, color=ORANGE, lw=2.5, label="y = −x + 5")
    ax.plot(2, 3, "o", color=RED, ms=14, zorder=5)
    ax.annotate("Solution\n(2, 3)\nx = 2", (2, 3), xytext=(3.2, 5.5), fontsize=10, color=RED,
                fontweight="bold", arrowprops=dict(arrowstyle="->", color=RED))
    ax.text(0.5, 7, "2x + 1 = 5  →  x = 2", fontsize=10, color=TEAL, fontweight="bold")
    ax.legend(fontsize=9, loc="lower right")
    _save(fig, "activity_4_one_solution.png")


def activity_4_no_solution_case():
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_title("No solution — false statement", fontsize=12, fontweight="bold", pad=10)
    steps = [
        ("Start", "2(3x + 4) = 6x + 5", BLUE),
        ("Distribute", "6x + 8 = 6x + 5", TEAL),
        ("Subtract 6x", "8 = 5", ORANGE),
        ("Result", "−24 = 7  ✗", RED),
    ]
    for i, (label, eq, color) in enumerate(steps):
        x = 1.2 + i * 2.2
        ax.add_patch(FancyBboxPatch((x - 0.95, 1.0), 1.9, 1.8, boxstyle="round,pad=0.05",
                                    facecolor=color, alpha=0.12, edgecolor=color, lw=2))
        ax.text(x, 2.45, label, ha="center", fontsize=9, color=TEAL)
        ax.text(x, 1.75, eq, ha="center", fontsize=10, fontweight="bold")
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 1.05, 1.9), xytext=(x + 0.65, 1.9),
                        arrowprops=dict(arrowstyle="->", color=GRID, lw=1.5))
    ax.text(5, 0.35, "Variables cancel → contradiction → NO SOLUTION", ha="center",
            fontsize=10, color=RED, fontweight="bold")
    _save(fig, "activity_4_no_solution_case.png")


# ── Activity 5 ──
def activity_5_multistep_flow():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_title("Multi-step solving flow", fontsize=12, fontweight="bold", pad=10)
    nodes = [
        ("Start", "3(2x − 1) + 4 = 19", BLUE),
        ("Distribute", "6x − 3 + 4 = 19", TEAL),
        ("Combine", "6x + 1 = 19", GREEN),
        ("Isolate", "6x = 18", ORANGE),
        ("Solve", "x = 3", PURPLE),
    ]
    for i, (label, eq, color) in enumerate(nodes):
        x = 0.8 + i * 2.0
        ax.add_patch(FancyBboxPatch((x - 0.85, 0.8), 1.7, 2.0, boxstyle="round,pad=0.05",
                                    facecolor=color, alpha=0.12, edgecolor=color, lw=2))
        ax.text(x, 2.35, label, ha="center", fontsize=9, color=TEAL, fontweight="bold")
        ax.text(x, 1.5, eq, ha="center", fontsize=9, fontweight="bold")
        if i < len(nodes) - 1:
            ax.annotate("", xy=(x + 1.05, 1.8), xytext=(x + 0.65, 1.8),
                        arrowprops=dict(arrowstyle="->", color=TEXT, lw=2))
    ax.text(5, 0.25, "Distribute → Combine like terms → Isolate variable → Check", ha="center",
            fontsize=10, color=TEXT)
    _save(fig, "activity_5_multistep_flow.png")


def activity_5_variables_both_sides():
    fig, ax = plt.subplots(figsize=(7, 4))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("Variables on both sides: 3x − 10 = 2x + 5", fontsize=12, fontweight="bold", pad=10)
    ax.text(2.5, 3.8, "Left: 3x − 10", ha="center", fontsize=11, color=BLUE, fontweight="bold")
    ax.text(7.5, 3.8, "Right: 2x + 5", ha="center", fontsize=11, color=ORANGE, fontweight="bold")
    ax.add_patch(FancyBboxPatch((0.8, 2.2), 3.4, 1.2, boxstyle="round", facecolor="#eff6ff", edgecolor=BLUE, lw=2))
    ax.text(2.5, 2.8, "3x − 10", ha="center", fontsize=14, fontweight="bold", color=BLUE)
    ax.add_patch(FancyBboxPatch((5.8, 2.2), 3.4, 1.2, boxstyle="round", facecolor="#fff7ed", edgecolor=ORANGE, lw=2))
    ax.text(7.5, 2.8, "2x + 5", ha="center", fontsize=14, fontweight="bold", color=ORANGE)
    ax.annotate("", xy=(5, 1.3), xytext=(3.2, 1.3), arrowprops=dict(arrowstyle="->", color=RED, lw=2))
    ax.annotate("", xy=(5, 1.3), xytext=(6.8, 1.3), arrowprops=dict(arrowstyle="->", color=RED, lw=2))
    ax.text(5, 1.0, "subtract 2x from both sides", ha="center", fontsize=9, color=RED, fontweight="bold")
    ax.text(5, 0.35, "x − 10 = 5  →  x = 15", ha="center", fontsize=12, fontweight="bold", color=GREEN)
    _save(fig, "activity_5_variables_both_sides.png")


# ── Activity 6 ──
def activity_6_solve_for_y():
    fig, ax = plt.subplots(figsize=(7, 4))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("Solve for y: 3x + 4y = 8", fontsize=12, fontweight="bold", pad=10)
    steps = [
        ("Start", "3x + 4y = 8", BLUE),
        ("Subtract 3x", "4y = 8 − 3x", TEAL),
        ("Divide by 4", "y = (8 − 3x) / 4", GREEN),
        ("Simplify", "y = 2 − (3/4)x", PURPLE),
    ]
    for i, (label, eq, color) in enumerate(steps):
        y = 3.6 - i * 0.85
        ax.add_patch(FancyBboxPatch((1.5, y - 0.3), 7.0, 0.65, boxstyle="round,pad=0.03",
                                    facecolor=color, alpha=0.1, edgecolor=color, lw=1.5))
        ax.text(1.8, y, label + ":", ha="left", fontsize=9, color=TEAL, fontweight="bold")
        ax.text(8.5, y, eq, ha="right", fontsize=11, fontweight="bold")
        if i < len(steps) - 1:
            ax.annotate("", xy=(5, y - 0.45), xytext=(5, y - 0.32),
                        arrowprops=dict(arrowstyle="->", color=GRID, lw=1.5))
    ax.text(5, 0.25, "Isolate the requested variable (y)", ha="center", fontsize=9, color=TEXT)
    _save(fig, "activity_6_solve_for_y.png")


def activity_6_word_problem_setup():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("Word problem: hockey league games", fontsize=12, fontweight="bold", pad=10)
    story = (
        "A hockey league has x teams.\n"
        "Each team plays every other team twice.\n"
        "Total games played: 156"
    )
    ax.text(5, 4.0, story, ha="center", fontsize=10, color=TEXT,
            bbox=dict(boxstyle="round", facecolor="#eff6ff", edgecolor=BLUE, pad=0.6))
    ax.annotate("", xy=(5, 2.2), xytext=(5, 3.2),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
    ax.text(5, 1.7, "Let x = number of teams", ha="center", fontsize=10, color=TEAL, fontweight="bold")
    ax.text(5, 1.0, "Games = x(x − 1)  (each pair plays twice)", ha="center", fontsize=10, color=ORANGE)
    ax.text(5, 0.35, "Equation: x(x − 1) = 156", ha="center", fontsize=12, fontweight="bold", color=GREEN)
    _save(fig, "activity_6_word_problem_setup.png")


# ── Practice images ──
def practice_u5_tiles_2x():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_title("Practice: tile model for 2x = x + 3", fontsize=11, fontweight="bold", pad=10)
    ax.text(2.5, 3.2, "2x", ha="center", fontsize=11, color=BLUE, fontweight="bold")
    ax.text(7.5, 3.2, "x + 3", ha="center", fontsize=11, color=ORANGE, fontweight="bold")
    _draw_tiles_row(ax, 1.0, 1.8, n_x=2)
    _draw_tiles_row(ax, 6.0, 1.8, n_x=1, n_unit=3)
    ax.text(5, 0.5, "Remove 1 x-tile from each side  →  x = 3", ha="center", fontsize=10, color=TEAL)
    _save(fig, "practice_u5_tiles_2x.png", practice=True)


def practice_u5_tiles_3x2():
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.set_title("Practice: Juanita's tile model — 3x + 2 = 14", fontsize=11, fontweight="bold", pad=10)
    ax.text(5, 4.0, "Juanita modeled 3x + 2 = 14 with algebra tiles", ha="center", fontsize=9, color=TEXT)
    _draw_tiles_row(ax, 0.8, 2.0, n_x=3, n_unit=2)
    ax.text(2.5, 1.4, "3x + 2", ha="center", fontsize=10, color=BLUE, fontweight="bold")
    ax.text(5, 2.25, "=", ha="center", fontsize=16, fontweight="bold")
    for i in range(14):
        col = i % 7
        row = i // 7
        _draw_unit_tile(ax, 5.5 + col * 0.5, 2.5 - row * 0.55, size=0.38)
    ax.text(7.5, 1.4, "14 ones", ha="center", fontsize=10, color=ORANGE, fontweight="bold")
    ax.text(5, 0.4, "Subtract 2 from both sides → 3x = 12 → x = 4", ha="center", fontsize=9, color=TEAL)
    _save(fig, "practice_u5_tiles_3x2.png", practice=True)


def practice_u5_distribute_graphic():
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_title("Practice: 8(3x + 40)", fontsize=11, fontweight="bold", pad=10)
    ax.text(5, 3.2, "8(3x + 40)", ha="center", fontsize=13, fontweight="bold", color=BLUE)
    ax.text(2.5, 2.0, "8·3x = 24x", ha="center", fontsize=11, color=GREEN, fontweight="bold")
    ax.text(7.5, 2.0, "8·40 = 320", ha="center", fontsize=11, color=GREEN, fontweight="bold")
    ax.text(5, 0.7, "= 24x + 320", ha="center", fontsize=12, fontweight="bold", color=TEAL)
    _save(fig, "practice_u5_distribute_graphic.png", practice=True)


def practice_u5_multistep():
    fig, ax = plt.subplots(figsize=(8, 3))
    _off(ax)
    ax.set_title("Practice: solve 4(x − 6) = 5", fontsize=11, fontweight="bold", pad=10)
    steps = [
        ("Distribute", "4x − 24 = 5", BLUE),
        ("Add 24", "4x = 29", TEAL),
        ("Divide by 4", "x = 29/4", GREEN),
    ]
    _equation_steps(ax, steps, y=0.45, box_h=0.4)
    _save(fig, "practice_u5_multistep.png", practice=True)


def practice_u5_variables_both():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_title("Practice: 3x − 10 = 2x + 5", fontsize=11, fontweight="bold", pad=10)
    ax.text(5, 3.3, "A number decreased by 10 equals another expression increased by 5", ha="center",
            fontsize=9, color=TEXT, wrap=True)
    ax.text(2.5, 2.2, "3x − 10", ha="center", fontsize=13, fontweight="bold", color=BLUE)
    ax.text(5, 2.2, "=", ha="center", fontsize=14, fontweight="bold")
    ax.text(7.5, 2.2, "2x + 5", ha="center", fontsize=13, fontweight="bold", color=ORANGE)
    ax.text(5, 1.0, "−2x both sides  →  x − 10 = 5  →  x = 15", ha="center",
            fontsize=10, color=TEAL, fontweight="bold")
    ax.text(5, 0.35, "Variables on both sides — collect x terms on one side", ha="center", fontsize=9, color=TEXT)
    _save(fig, "practice_u5_variables_both.png", practice=True)


def practice_u5_hockey():
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    _off(ax)
    ax.set_title("Practice: hockey league", fontsize=11, fontweight="bold", pad=10)
    lines = [
        "Teams: x",
        "Each pair of teams plays 2 games",
        "Total games: 156",
        "",
        "x(x − 1) = 156",
        "Expand: x² − x − 156 = 0",
    ]
    for i, line in enumerate(lines):
        weight = "bold" if "=" in line else "normal"
        color = GREEN if "=" in line else TEXT
        ax.text(0.5, 0.85 - i * 0.13, line, ha="center", fontsize=10, fontweight=weight,
                color=color, transform=ax.transAxes)
    _save(fig, "practice_u5_hockey.png", practice=True)


def practice_u5_perimeter():
    fig, ax = plt.subplots(figsize=(8, 3.8))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.set_title("Practice: perimeter — square vs triangle", fontsize=11, fontweight="bold", pad=10)
    sq = Rectangle((0.8, 1.5), 1.5, 1.5, facecolor="#eff6ff", edgecolor=BLUE, lw=2)
    ax.add_patch(sq)
    ax.text(1.55, 2.25, "x", ha="center", fontsize=11, fontweight="bold", color=BLUE)
    ax.text(1.55, 0.9, "Square side = x\nPerimeter = 4x", ha="center", fontsize=9, color=BLUE)
    tri_x = [5.5, 7.5, 6.5]
    tri_y = [1.5, 1.5, 3.3]
    ax.fill(tri_x, tri_y, facecolor="#fff7ed", edgecolor=ORANGE, lw=2)
    ax.text(6.5, 1.2, "Triangle sides: x, x, x + 2", ha="center", fontsize=9, color=ORANGE)
    ax.text(6.5, 0.5, "Perimeter = x + x + (x + 2) = 3x + 2", ha="center", fontsize=9, color=ORANGE)
    ax.text(5, 3.9, "Same perimeter: 4x = 3x + 2  →  x = 2", ha="center",
            fontsize=11, fontweight="bold", color=TEAL)
    _save(fig, "practice_u5_perimeter.png", practice=True)


def practice_u5_solve_y():
    fig, ax = plt.subplots(figsize=(7, 3.2))
    _off(ax)
    ax.set_title("Practice: solve for y — 9y − 12x = 36", fontsize=11, fontweight="bold", pad=10)
    steps = [
        ("Start", "9y − 12x = 36", BLUE),
        ("Add 12x", "9y = 36 + 12x", TEAL),
        ("÷ 9", "y = 4 + (4/3)x", GREEN),
    ]
    _equation_steps(ax, steps, y=0.45, box_h=0.4)
    _save(fig, "practice_u5_solve_y.png", practice=True)


LESSON_FUNCS = [
    activity_1_algebra_tiles_balance, activity_1_completing_tile_model,
    activity_2_properties_equality, activity_2_distributive_model,
    activity_3_distribute_negatives, activity_3_combine_like_terms,
    activity_4_one_solution, activity_4_no_solution_case,
    activity_5_multistep_flow, activity_5_variables_both_sides,
    activity_6_solve_for_y, activity_6_word_problem_setup,
]

PRACTICE_FUNCS = [
    practice_u5_tiles_2x, practice_u5_tiles_3x2, practice_u5_distribute_graphic,
    practice_u5_multistep, practice_u5_variables_both, practice_u5_hockey,
    practice_u5_perimeter, practice_u5_solve_y,
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
