"""School concept-check templates for Arjun Course 3 practice.

Based on the Math 3 concept-check format: computation, multi-step word problems,
pattern modeling, error analysis, and interpret-in-context questions.
"""

from __future__ import annotations

import math
import random
import time
from fractions import Fraction

# Share of each daily practice session reserved for concept-check-style items.
CONCEPT_CHECK_DAILY_RATIO = 0.5
CONCEPT_CHECK_FOCUS_RATIO = 0.55

# ── LLM style guidance (injected into Grok system prompt) ──

CONCEPT_CHECK_STYLE_RULES = """
CONCEPT CHECK STYLE (match Arjun's school assessments):
- Mix question types like the school's concept checks:
  (1) Evaluate an expression (fractions, exponents, order of operations).
  (2) Multi-step word problems with mixed numbers — state the story clearly.
  (3) Pattern/sequence: describe the rule OR find the next term OR write an expression in n.
  (4) Error analysis: "Who solved incorrectly and why?" or "Describe the student's error."
  (5) Interpret in context: explain what slope or y-intercept means in dollars, feet, etc.
  (6) Geometry applications: volume → edge length, perimeter → area (square/cube).
  (7) Compare/order: absolute values, fractions/decimals/percents, rational vs irrational.
- Answers must be in simplest form; explanations should show the key steps (Step 1, Step 2…).
- Use kid-friendly real-world contexts (food, sports, school, measurements).
- Fraction word problems: include unlike denominators when level is C or higher.
- For proportional vs linear: club fee + per-meal cost is NOT proportional; plain per-meal is.
"""

# Archetype hints per category for LLM slot planning
CATEGORY_ARCHETYPES: dict[str, list[str]] = {
    "patterns": [
        "Describe the pattern rule, then find the next term",
        "Table of figure number vs count → expression 3n + 1 → apply to figure 45",
        "Arithmetic sequence with fractional step (e.g. add 2/3 each time)",
    ],
    "fractions": [
        "Evaluate mixed-number subtraction: 15⅔ − 11⅝",
        "Multi-step word problem: total minus two uneaten portions",
        "Fraction of a remainder: 1/8 chocolate, 4/9 of vanilla hidden",
        "Mixed-number division word problem (how many fit?)",
    ],
    "powers_roots": [
        "Cube volume → edge length; then fraction of height",
        "Perimeter of square → area (don't confuse with side length)",
        "Error analysis: student used area formula instead of perimeter",
        "Solve √x² = √121",
    ],
    "rational_numbers": [
        "Convert fraction to percent",
        "Order fraction, decimal, and percent greatest to least",
        "Repeating decimal as fraction in simplest form",
    ],
    "irrational_numbers": [
        "Which value is irrational (MCQ)",
        "Estimate √n to nearest tenth using perfect squares",
        "Classify √64, ∛64, ∛25",
    ],
    "exponents": [
        "Simplify with product/quotient/power rules; positive exponents only",
        "Zero exponent: large number to the 0 power",
        "Justify: tripling 3^99 gives 3^100",
        "Order of operations with exponents and parentheses",
    ],
    "scientific_notation": [
        "Estimate large number in scientific notation",
        "Add two numbers in scientific notation (align powers of 10)",
    ],
    "sci_notation_ops": [
        "Divide numbers in scientific notation; proper coefficient 1≤|a|<10",
        "Multiply then rewrite in standard scientific notation",
    ],
    "expressions": [
        "Dot pattern: fill table, write expression, evaluate for n = 45",
        "Perimeter pattern 4, 6, 8 → expression 2n + 2",
    ],
    "solving_equations": [
        "Multi-step: distribute both sides, variables both sides, fractional answer",
        "Square park: sides equal → write and solve for perimeter",
    ],
    "slope": [
        "Slope from two points on a described graph",
        "Find k given slope and two points",
    ],
    "slope_intercept": [
        "Interpret slope as dollars per meal",
        "Interpret y-intercept as starting fee or membership cost",
    ],
    "proportional": [
        "Compare club (y = 10x + 250) vs non-club table — which is proportional?",
        "Explain why y-intercept ≠ 0 means not proportional",
    ],
    "systems": [
        "Two lines: unique solution vs parallel vs coincident",
        "Word problem setup for two equations",
    ],
    "angles": [
        "Supplementary angles with algebra",
        "Vertical angles + linear pair",
    ],
    "pythagorean": [
        "Find missing leg or hypotenuse in word context",
        "Converse: is triangle a right triangle?",
    ],
    "volume": [
        "Cube/cylinder volume → missing dimension",
        "Compare volumes after scaling",
    ],
    "function_basics": [
        "Is this relation a function? (vertical line test in words)",
        "Evaluate f(x) for given x",
    ],
    "linear_functions": [
        "Rate of change from table",
        "Write y = mx + b from context",
    ],
    "scatter_association": [
        "Describe association: positive, negative, none",
        "Outlier effect on trend",
    ],
    "two_way_tables": [
        "Two-way table: what fraction prefer X given Y?",
        "Joint vs marginal frequency",
    ],
    "transformations": [
        "Reflect a point across x-axis or y-axis",
        "Translation: add constant to coordinates",
    ],
    "similarity": [
        "Scale factor between similar figures",
        "Find missing side using proportions",
    ],
    "surface_area": [
        "Cube or rectangular prism surface area",
        "Net → total area",
    ],
    "bivariate_data": [
        "Trend from a small table of x and y",
        "Predict y from linear pattern in table",
    ],
    "comparing_functions": [
        "Which function grows faster for x > 0",
        "Compare rates from two equations",
    ],
    "constructing": [
        "Write equation from starting value + rate",
        "Build function from word problem",
    ],
    "linear_nonlinear": [
        "Identify nonlinear table (non-constant rate)",
        "Which graph description is nonlinear",
    ],
    "systems": [
        "Parallel vs intersecting lines",
        "No solution vs infinitely many",
    ],
}


# All practice categories that have school concept-check coverage (Units 1–5).
UNIT_CONCEPT_CHECK_CATEGORIES: dict[int, list[str]] = {
    1: [
        "patterns", "fractions", "powers_roots", "rational_numbers", "irrational_numbers",
        "exponents", "scientific_notation", "sci_notation_ops",
    ],
    2: [
        "expressions", "solving_equations", "slope", "slope_intercept",
        "proportional", "systems",
    ],
    3: [
        "angles", "transformations", "similarity", "pythagorean", "surface_area", "volume",
    ],
    4: [
        "function_basics", "comparing_functions", "constructing",
        "linear_functions", "linear_nonlinear",
    ],
    5: [
        "scatter_association", "bivariate_data", "mad", "two_way_tables",
    ],
}


def archetype_hint(category: str, level: str) -> str:
    """Return a concept-check archetype hint for LLM user message."""
    hints = CATEGORY_ARCHETYPES.get(category, [])
    if not hints:
        return "Use a school concept-check style: computation or short word problem with clear steps."
    idx = (ord(level[0]) - ord("A")) % len(hints) if level else 0
    return hints[idx]


def concept_check_prompt_block() -> str:
    return CONCEPT_CHECK_STYLE_RULES.strip()


# ── MCQ helpers ──

def _mixed(frac: Fraction) -> str:
    if frac.denominator == 1:
        return str(frac.numerator)
    whole = int(frac.numerator // frac.denominator)
    rem = abs(frac.numerator % frac.denominator)
    sign = "-" if frac < 0 else ""
    if whole == 0:
        return f"{sign}{rem}/{frac.denominator}" if sign else f"{rem}/{frac.denominator}"
    if rem == 0:
        return str(whole) if not sign else f"-{abs(whole)}"
    return f"{sign}{abs(whole)} {rem}/{frac.denominator}"


def _mcq(
    qid: str,
    category: str,
    question: str,
    correct: str,
    wrong: list[str],
    explanation: str,
    *,
    level: str = "C",
) -> dict:
    opts = [correct] + wrong[:3]
    random.shuffle(opts)
    return {
        "id": qid,
        "category": category,
        "question": question,
        "options": opts,
        "answer": opts.index(correct),
        "explanation": explanation,
        "level": level,
        "source": "concept_check",
    }


# ── Unit 1 generators ──


def _gen_fractions() -> list[dict]:
    out: list[dict] = []
    a, b = Fraction(5, 1) + Fraction(1, 4), Fraction(2, 3)
    ans = a - b
    out.append(
        _mcq(
            "cc_u1_frac_eval",
            "fractions",
            f"Evaluate { _mixed(a) } − { _mixed(b) }. Give your answer in simplest form.",
            _mixed(ans),
            [_mixed(ans + Fraction(1, 4)), _mixed(Fraction(4, 1)), _mixed(ans - Fraction(1, 6))],
            f"Step 1: common denominator 12. Step 2: { _mixed(a) } − { _mixed(b) } = { _mixed(ans) }.",
            level="C",
        )
    )
    total = Fraction(14, 1) + Fraction(3, 4)
    eaten1, eaten2 = Fraction(4, 1) + Fraction(1, 5), Fraction(3, 1) + Fraction(1, 8)
    consumed = eaten1 + eaten2
    left = total - consumed
    out.append(
        _mcq(
            "cc_u1_frac_word",
            "fractions",
            (
                f"You have { _mixed(total) } lbs of snacks. "
                f"You ate { _mixed(eaten1) } lbs on Tuesday and { _mixed(eaten2) } lbs on Wednesday. "
                "How many lbs remain?"
            ),
            f"{ _mixed(left) } lbs",
            [f"{ _mixed(left + Fraction(1, 2)) } lbs", f"{ _mixed(consumed) } lbs", f"{ _mixed(total - eaten1) } lbs"],
            (
                f"Step 1: total eaten = { _mixed(eaten1) } + { _mixed(eaten2) } = { _mixed(consumed) }. "
                f"Step 2: { _mixed(total) } − { _mixed(consumed) } = { _mixed(left) } lbs."
            ),
            level="D",
        )
    )
    # fraction of remainder
    hidden = Fraction(3, 4) * Fraction(4, 9)
    out.append(
        _mcq(
            "cc_u1_frac_of_frac",
            "fractions",
            (
                "Of all cakes, 1/8 are chocolate and the rest are vanilla. "
                "Of the vanilla cakes, 4/9 are hidden. What fraction of ALL cakes are vanilla and hidden?"
            ),
            _mixed(hidden),
            [_mixed(Fraction(4, 9)), _mixed(Fraction(1, 2)), _mixed(Fraction(5, 18))],
            "Step 1: vanilla = 1 − 1/8 = 7/8. Step 2: 7/8 × 4/9 = 7/18.",
            level="D",
        )
    )
    return out


def _gen_patterns() -> list[dict]:
    out: list[dict] = []
    seq = [Fraction(6, 1) + Fraction(1, 3), Fraction(7, 1), Fraction(7, 1) + Fraction(2, 3)]
    next_term = seq[-1] + Fraction(2, 3)
    out.append(
        _mcq(
            "cc_u1_pat_rule",
            "patterns",
            f"A sequence starts {', '.join(_mixed(t) for t in seq)}, … Each term adds the same amount. What is the next term?",
            _mixed(next_term),
            [_mixed(Fraction(8, 1)), _mixed(Fraction(9, 1) + Fraction(1, 3)), _mixed(seq[-1] + Fraction(1, 3))],
            "The step is +2/3 each time. Add 2/3 to the last term shown.",
            level="C",
        )
    )
    out.append(
        _mcq(
            "cc_u1_pat_expr",
            "patterns",
            (
                "A dot pattern has 4 dots in figure 1, 7 in figure 2, and 10 in figure 3 "
                "(each new figure adds 3 dots). Which expression gives the dots in figure n?"
            ),
            "3n + 1",
            ["3n − 1", "4n − 3", "n + 3"],
            "Figure 1 → 3(1)+1 = 4; figure 2 → 7; figure 3 → 10. Rule: add 3 each time → 3n + 1.",
            level="D",
        )
    )
    out.append(
        _mcq(
            "cc_u1_pat_apply",
            "patterns",
            "Using the rule 3n + 1 for the dot pattern above, how many dots are in figure 45?",
            "136",
            ["135", "137", "145"],
            "Step 1: 3(45) + 1 = 135 + 1 = 136 dots.",
            level="E",
        )
    )
    return out


def _gen_powers_roots() -> list[dict]:
    out: list[dict] = []
    vol = 343
    edge = round(vol ** (1 / 3))
    out.append(
        _mcq(
            "cc_u1_pow_cube",
            "powers_roots",
            f"A cube has volume {vol} cubic ft. What is the length of one edge?",
            f"{edge} ft",
            [f"{edge - 1} ft", f"{edge + 2} ft", f"{vol // 10} ft"],
            f"Step 1: edge = ∛{vol} = {edge} because {edge}³ = {vol}.",
            level="C",
        )
    )
    perim = 24
    side = perim // 4
    area = side * side
    out.append(
        _mcq(
            "cc_u1_pow_perim_area",
            "powers_roots",
            f"A square penalty box is surrounded by {perim} ft of glass (perimeter). What is the area of its floor?",
            f"{area} sq ft",
            [f"{side} sq ft", f"{perim} sq ft", f"{area + 12} sq ft"],
            f"Step 1: side = {perim} ÷ 4 = {side} ft. Step 2: area = {side}² = {area} sq ft.",
            level="D",
        )
    )
    out.append(
        _mcq(
            "cc_u1_pow_error",
            "powers_roots",
            (
                "Kevin has 36 ft of fencing for a square garden. He says each side is 6 ft because √36 = 6. "
                "What is Kevin's error?"
            ),
            "He used area instead of perimeter; each side should be 36 ÷ 4 = 9 ft",
            [
                "36 ÷ 4 = 9 is wrong; sides are 6 ft",
                "Square roots cannot be used for fencing",
                "He should multiply 36 by 4",
            ],
            "Perimeter 36 ft on a square → side = 36/4 = 9 ft. √36 is area thinking, not perimeter.",
            level="D",
        )
    )
    return out


def _gen_rational() -> list[dict]:
    return [
        _mcq(
            "cc_u1_rat_pct",
            "rational_numbers",
            "Convert 1/8 to a percent.",
            "12.5%",
            ["8%", "1.8%", "0.125%"],
            "Step 1: 1 ÷ 8 = 0.125. Step 2: 0.125 × 100 = 12.5%.",
            level="B",
        ),
        _mcq(
            "cc_u1_rat_order",
            "rational_numbers",
            "Order from GREATEST to LEAST: 0.201111… (repeating 1), 20.1%, 1/5",
            "0.201111…, 20.1%, 1/5",
            ["1/5, 20.1%, 0.201111…", "20.1%, 1/5, 0.201111…", "All are equal"],
            "1/5 = 0.2 = 20%; 20.1% = 0.201; 0.201111… is slightly greater than 0.201.",
            level="C",
        ),
    ]


def _gen_irrational() -> list[dict]:
    return [
        _mcq(
            "cc_u1_irr_which",
            "irrational_numbers",
            "Which number is irrational?",
            "∛25",
            ["√64", "−17/8", "1.3̄45 (repeating)"],
            "∛25 is not a perfect cube. √64 = 8, −17/8 and repeating decimals are rational.",
            level="C",
        ),
        _mcq(
            "cc_u1_irr_est",
            "irrational_numbers",
            "Between which two consecutive integers does √140 lie?",
            "11 and 12",
            ["10 and 11", "12 and 13", "14 and 15"],
            "11² = 121 and 12² = 144; 140 is between 121 and 144 → between 11 and 12.",
            level="D",
        ),
    ]


def _gen_exponents() -> list[dict]:
    return [
        _mcq(
            "cc_u1_exp_zero",
            "exponents",
            "Simplify: 1,456,789,874,500⁰",
            "1",
            ["0", "1,456,789,874,500", "Cannot simplify"],
            "Any non-zero number to the 0 power equals 1.",
            level="B",
        ),
        _mcq(
            "cc_u1_exp_pemdas",
            "exponents",
            "Simplify: 5 − 5(5 + 5)²",
            "−495",
            ["495", "−245", "0"],
            "Step 1: (5+5)=10, 10²=100. Step 2: 5−5(100)=5−500=−495.",
            level="C",
        ),
        _mcq(
            "cc_u1_exp_justify",
            "exponents",
            "If you triple 3⁹⁹, what is the result?",
            "3¹⁰⁰",
            ["3²⁹⁷", "9⁹⁹", "3⁹⁹ + 3"],
            "Tripling means multiply by 3 = 3¹, so 3⁹⁹ × 3¹ = 3¹⁰⁰.",
            level="D",
        ),
    ]


def _gen_scientific() -> list[dict]:
    return [
        _mcq(
            "cc_u1_sci_est",
            "scientific_notation",
            "Estimate 8,345,000,676,709 in scientific notation (nearest hundredth in coefficient).",
            "8.35 × 10¹²",
            ["8.34 × 10¹²", "8.35 × 10⁹", "83.5 × 10¹¹"],
            "Round to 8.35; move decimal 12 places → 8.35 × 10¹².",
            level="C",
        ),
        _mcq(
            "cc_u1_sci_add",
            "scientific_notation",
            "Simplify (6.5 × 10¹⁵) + (2 × 10¹³) and write in scientific notation.",
            "6.52 × 10¹⁵",
            ["8.5 × 10¹⁵", "6.5 × 10¹⁵", "6.52 × 10¹³"],
            "2 × 10¹³ = 0.02 × 10¹⁵; add coefficients 6.5 + 0.02 = 6.52.",
            level="D",
        ),
    ]


def _gen_sci_ops() -> list[dict]:
    return [
        _mcq(
            "cc_u1_sciops_div",
            "sci_notation_ops",
            "Simplify (3 × 10³²) ÷ (4 × 10⁸). Write in proper scientific notation.",
            "7.5 × 10²³",
            ["0.75 × 10²⁴", "7.5 × 10²⁴", "3/4 × 10²⁴"],
            "3/4 = 0.75 → 7.5 × 10²³; exponents: 32 − 8 = 24, adjust coefficient.",
            level="D",
        ),
    ]


# ── Unit 2 generators ──


def _gen_solving_equations() -> list[dict]:
    return [
        _mcq(
            "cc_u2_eq_multi",
            "solving_equations",
            "Solve for x: −18x − 15 = 6(x − 4) + 12",
            "x = −1/8",
            ["x = 1/8", "x = −3/24", "x = −1/4"],
            "Step 1: distribute 6 on the right. Step 2: combine like terms → −24x=3. Step 3: x=−1/8.",
            level="D",
        ),
        _mcq(
            "cc_u2_eq_square",
            "solving_equations",
            (
                "Each side of a square park is (1/3 of the perimeter − 8) units long. "
                "Set up and solve: if x is the perimeter, one side is x/3 − 8. "
                "A square has 4 equal sides, so 4(x/3 − 8) = x. What is the perimeter?"
            ),
            "96 units",
            ["84 units", "72 units", "48 units"],
            "4(x/3−8)=x → 4x/3−32=x → x/3=32 → x=96.",
            level="E",
        ),
    ]


def _gen_slope() -> list[dict]:
    return [
        _mcq(
            "cc_u2_slope_k",
            "slope",
            "Points (4, −6) and (18, k) lie on a line with slope 3. Find k.",
            "36",
            ["42", "30", "24"],
            "(k − (−6))/(18 − 4) = 3 → k + 6 = 42 → k = 36.",
            level="D",
        ),
        _mcq(
            "cc_u2_slope_graph",
            "slope",
            "A line crosses (0, 7) and (9, 3). What is the slope?",
            "−4/9",
            ["4/9", "−9/4", "2/3"],
            "Slope = (3 − 7)/(9 − 0) = −4/9.",
            level="C",
        ),
    ]


def _gen_slope_intercept() -> list[dict]:
    return [
        _mcq(
            "cc_u2_interpret_m",
            "slope_intercept",
            "Club members pay y = 10x + 250 for x meals. What does 10 represent?",
            "$10 per meal",
            ["$250 joining fee", "$10 flat total", "10 meals free"],
            "In y = mx + b, m = 10 is the rate: cost per meal.",
            level="C",
        ),
        _mcq(
            "cc_u2_interpret_b",
            "slope_intercept",
            "For y = 10x + 250, what does 250 represent in context?",
            "$250 membership fee before any meals",
            ["Cost of 250 meals", "$250 per meal", "Total after 10 meals"],
            "b = 250 is the starting value when x = 0 meals.",
            level="C",
        ),
    ]


def _gen_proportional() -> list[dict]:
    return [
        _mcq(
            "cc_u2_prop_compare",
            "proportional",
            (
                "Club: y = 10x + 250. Non-club costs are $0, $25, $50, $75 for 0, 1, 2, 3 meals. "
                "Which scenario is directly proportional?"
            ),
            "Non-club meals (through origin, constant $25/meal)",
            ["Club meals", "Both", "Neither"],
            "Proportional lines pass through (0,0) with constant ratio y/x. Non-club: 25/1 = 50/2.",
            level="D",
        ),
    ]


def _gen_expressions() -> list[dict]:
    return [
        _mcq(
            "cc_u2_expr_dots",
            "expressions",
            "Perimeters of figures are 4, 6, 8, … (add 2 each time). Expression for figure n?",
            "2n + 2",
            ["2n", "4n", "n + 4"],
            "When n=1, perimeter 4 → 2(1)+2=4; pattern adds 2 → 2n+2.",
            level="C",
        ),
    ]


def _gen_systems() -> list[dict]:
    return [
        _mcq(
            "cc_u2_sys_type",
            "systems",
            "Lines y = 2x + 1 and y = 2x − 3 are:",
            "Parallel with no solution",
            ["Intersecting with one solution", "The same line", "Perpendicular"],
            "Same slope 2, different intercepts → parallel, never meet.",
            level="C",
        ),
    ]


# ── Unit 3–5 lightweight generators ──


def _gen_pythagorean() -> list[dict]:
    a, b = 6, 8
    c = 10
    return [
        _mcq(
            "cc_u3_pyth",
            "pythagorean",
            f"A right triangle has legs {a} ft and {b} ft. How long is the hypotenuse?",
            f"{c} ft",
            [f"{c - 2} ft", f"{a + b} ft", f"{c + 2} ft"],
            f"c² = a² + b² = {a*a}+{b*b} = {c*c} → c = {c}.",
            level="C",
        ),
    ]


def _gen_volume() -> list[dict]:
    return [
        _mcq(
            "cc_u3_vol_cube",
            "volume",
            "A cube has volume 216 in³. Sand fills 1/3 of the height. How deep is the sand?",
            "2 inches",
            ["6 inches", "3 inches", "72 inches"],
            "Edge = ∛216 = 6 in; sand depth = 6 × 1/3 = 2 in.",
            level="D",
        ),
    ]


def _gen_angles() -> list[dict]:
    return [
        _mcq(
            "cc_u3_ang_supp",
            "angles",
            "Two angles are supplementary. One is (3x + 10)° and the other is (2x + 20)°. Find x.",
            "30",
            ["25", "35", "40"],
            "3x+10+2x+20=180 → 5x=150 → x=30.",
            level="C",
        ),
    ]


def _gen_linear_functions() -> list[dict]:
    return [
        _mcq(
            "cc_u4_lin_rate",
            "linear_functions",
            "A taxi charges $3 plus $2 per mile. Which equation models cost y for x miles?",
            "y = 2x + 3",
            ["y = 3x + 2", "y = 2x", "y = 5x"],
            "$2 per mile is slope; $3 flat fee is y-intercept.",
            level="B",
        ),
    ]


def _gen_scatter() -> list[dict]:
    return [
        _mcq(
            "cc_u5_scatter",
            "scatter_association",
            "As hours studying increase, test scores increase. This scatter plot shows:",
            "Positive association",
            ["Negative association", "No association", "Nonlinear only"],
            "Both variables increase together → positive association.",
            level="B",
        ),
    ]


def _gen_two_way() -> list[dict]:
    return [
        _mcq(
            "cc_u5_twoway",
            "two_way_tables",
            "Of 50 students, 30 prefer pizza. Of 40 adults, 15 prefer pizza. "
            "Which group has the greater fraction preferring pizza?",
            "Students (30/50 = 3/5 vs 15/40 = 3/8)",
            ["Adults (15/40)", "Both equal", "Cannot determine"],
            "Students: 30/50 = 3/5 = 0.6. Adults: 15/40 = 3/8 = 0.375.",
            level="C",
        ),
    ]


def _gen_transformations() -> list[dict]:
    return [
        _mcq(
            "cc_u3_transform",
            "transformations",
            "A point at (4, 2) is reflected across the x-axis. Where does it land?",
            "(4, −2)",
            ["(−4, 2)", "(4, 2)", "(−4, −2)"],
            "Reflection over the x-axis changes the sign of y: (4, 2) → (4, −2).",
            level="B",
        ),
    ]


def _gen_similarity() -> list[dict]:
    return [
        _mcq(
            "cc_u3_similar",
            "similarity",
            "Two similar triangles have a scale factor of 3 (small → large). "
            "A side on the smaller triangle is 5 cm. What is the matching side on the larger triangle?",
            "15 cm",
            ["8 cm", "12 cm", "5 cm"],
            "Multiply corresponding sides by the scale factor: 5 × 3 = 15 cm.",
            level="C",
        ),
    ]


def _gen_surface_area() -> list[dict]:
    return [
        _mcq(
            "cc_u3_sa_cube",
            "surface_area",
            "A cube has edge length 4 cm. What is its total surface area?",
            "96 cm²",
            ["64 cm²", "16 cm²", "48 cm²"],
            "One face = 4² = 16; six faces → 6 × 16 = 96 cm².",
            level="C",
        ),
    ]


def _gen_function_basics() -> list[dict]:
    return [
        _mcq(
            "cc_u4_func_basic",
            "function_basics",
            "A relation maps 1→3, 2→3, 3→5. Can this be a function?",
            "Yes — each input has exactly one output",
            ["No — 3 appears twice as an output", "No — inputs repeat", "Only if the outputs increase"],
            "A function allows repeated outputs; inputs must not repeat with different outputs.",
            level="B",
        ),
    ]


def _gen_comparing_functions() -> list[dict]:
    return [
        _mcq(
            "cc_u4_compare",
            "comparing_functions",
            "Function A: y = 2x. Function B: y = 5x. For x > 0, which grows faster?",
            "Function B (larger rate of change)",
            ["Function A", "They grow at the same rate", "Neither grows"],
            "Both are linear through the origin; slope 5 > 2 so B increases faster.",
            level="C",
        ),
    ]


def _gen_constructing() -> list[dict]:
    return [
        _mcq(
            "cc_u4_construct",
            "constructing",
            "A plant starts at 3 cm and grows 2 cm per week. Which equation models height h after w weeks?",
            "h = 2w + 3",
            ["h = 3w + 2", "h = 2w", "h = 3w"],
            "Starting value 3 is the intercept; 2 cm/week is the slope → h = 2w + 3.",
            level="C",
        ),
    ]


def _gen_linear_nonlinear() -> list[dict]:
    return [
        _mcq(
            "cc_u4_nonlin",
            "linear_nonlinear",
            "Which table could represent a nonlinear function?",
            "x: 1,2,3 → y: 1,4,9 (perfect squares)",
            ["x: 1,2,3 → y: 2,4,6", "x: 1,2,3 → y: 5,5,5", "x: 1,2,3 → y: 3,5,7"],
            "Equal steps in x but y increases by 3, then 5 — not a constant rate → nonlinear.",
            level="C",
        ),
    ]


def _gen_bivariate() -> list[dict]:
    return [
        _mcq(
            "cc_u5_bivar",
            "bivariate_data",
            "Hours studied (2,4,6) match scores (60,70,80). What is the trend?",
            "Positive — more hours, higher scores",
            ["Negative", "No trend", "Nonlinear only"],
            "Both variables increase together → positive association.",
            level="B",
        ),
    ]


def _gen_mad() -> list[dict]:
    return [
        _mcq(
            "cc_u5_mad",
            "mad",
            "Data set: 4, 6, 8, 10. Mean = 7. What is the mean absolute deviation (MAD)?",
            "2",
            ["3", "1.5", "4"],
            "Deviations: |4−7|,|6−7|,|8−7|,|10−7| = 3,1,1,3 → average (3+1+1+3)/4 = 2.",
            level="D",
        ),
    ]


# ── Dynamic generators (fresh variants for daily practice) ──


def _dyn_id(unit_id: int, category: str) -> str:
    stamp = int(time.time() * 1000) % 1_000_000
    return f"cc_dyn_u{unit_id}_{category}_{stamp}_{random.randint(100, 999)}"


def _dyn_fractions(level: str) -> dict:
    whole = random.randint(2, 8)
    num, den = random.randint(1, 3), random.randint(4, 8)
    a = Fraction(whole, 1) + Fraction(num, den)
    sub = Fraction(random.randint(1, 2), random.choice([3, 4, 5, 6]))
    ans = a - sub
    return _mcq(
        _dyn_id(1, "fractions"),
        "fractions",
        f"Evaluate {_mixed(a)} − {_mixed(sub)}. Simplest form.",
        _mixed(ans),
        [_mixed(ans + Fraction(1, 6)), _mixed(a), _mixed(ans - Fraction(1, 4))],
        f"Step 1: common denominator. Step 2: {_mixed(a)} − {_mixed(sub)} = {_mixed(ans)}.",
        level=level,
    )


def _dyn_patterns(level: str) -> dict:
    start = random.randint(2, 6)
    step = random.choice([Fraction(2, 3), Fraction(1, 2), Fraction(3, 4), Fraction(1, 1)])
    terms = [start + step * i for i in range(4)]
    nxt = terms[-1] + step
    seq = ", ".join(_mixed(t) for t in terms)
    return _mcq(
        _dyn_id(1, "patterns"),
        "patterns",
        f"Sequence: {seq}, … Add the same amount each time. Next term?",
        _mixed(nxt),
        [_mixed(nxt + step), _mixed(terms[-1]), _mixed(nxt + Fraction(1, 1))],
        f"Each step adds {_mixed(step)} → next = {_mixed(nxt)}.",
        level=level,
    )


def _dyn_exponents(level: str) -> dict:
    inner = random.randint(2, 9)
    outer = random.randint(2, 5)
    val = random.randint(1, 4) - random.randint(3, 6)
    result = val - outer * (inner ** 2)
    return _mcq(
        _dyn_id(1, "exponents"),
        "exponents",
        f"Simplify: {val} − {outer}({inner})²",
        str(result),
        [str(result + outer), str(-result), str(val - inner)],
        f"Step 1: {inner}² = {inner**2}. Step 2: {val} − {outer}({inner**2}) = {result}.",
        level=level,
    )


def _dyn_solving_equations(level: str) -> dict:
    x = Fraction(random.choice([-3, -2, -1, 1, 2, 3]), random.choice([1, 2, 4, 8]))
    a, b = random.randint(2, 6), random.randint(2, 5)
    c = a * x + b
    return _mcq(
        _dyn_id(2, "solving_equations"),
        "solving_equations",
        f"Solve for x: {a}x + {b} = {c}",
        f"x = {_mixed(x)}",
        [f"x = {_mixed(x + 1)}", f"x = {_mixed(-x)}", f"x = {_mixed(x - 1)}"],
        f"Step 1: {a}x = {c} − {b}. Step 2: x = {_mixed(x)}.",
        level=level,
    )


def _dyn_slope(level: str) -> dict:
    x1, y1 = random.randint(0, 3), random.randint(2, 8)
    x2 = x1 + random.randint(4, 8)
    m = random.choice([Fraction(-2, 3), Fraction(1, 2), Fraction(3, 4), Fraction(2, 1)])
    y2 = y1 + m * (x2 - x1)
    return _mcq(
        _dyn_id(2, "slope"),
        "slope",
        f"Line through ({x1}, {y1}) and ({x2}, {int(y2) if y2.denominator == 1 else y2}). Slope?",
        _mixed(m),
        [_mixed(m + 1), _mixed(-m), _mixed(m * 2)],
        f"Slope = ({y2} − {y1}) / ({x2} − {x1}) = {_mixed(m)}.",
        level=level,
    )


def _dyn_pythagorean(level: str) -> dict:
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10)]
    a, b, c = random.choice(triples)
    return _mcq(
        _dyn_id(3, "pythagorean"),
        "pythagorean",
        f"A right triangle has legs {a} m and {b} m. Find the hypotenuse.",
        f"{c} m",
        [f"{a + b} m", f"{c + 1} m", f"{c - 1} m"],
        f"c² = {a}² + {b}² = {a*a + b*b} → c = {c}.",
        level=level,
    )


def _dyn_scatter(level: str) -> dict:
    rate = random.choice([2, 3, 5, 10])
    x = random.randint(2, 5)
    return _mcq(
        _dyn_id(5, "scatter_association"),
        "scatter_association",
        f"A scatter plot shows hours practiced vs baskets made. "
        f"At {x} hours, about {rate * x} baskets. What is the association?",
        "Positive — more practice, more baskets",
        ["Negative", "No association", "Cannot tell"],
        f"Baskets increase with hours → positive association.",
        level=level,
    )


def _dyn_two_way(level: str) -> dict:
    a_num, a_den = random.randint(10, 30), random.randint(40, 60)
    b_num = random.randint(5, 20)
    b_den = random.randint(30, 50)
    a_frac = Fraction(a_num, a_den)
    b_frac = Fraction(b_num, b_den)
    winner = "Group A" if a_frac > b_frac else "Group B"
    return _mcq(
        _dyn_id(5, "two_way_tables"),
        "two_way_tables",
        f"Group A: {a_num}/{a_den} prefer tea. Group B: {b_num}/{b_den} prefer tea. Who has the greater fraction?",
        winner,
        ["Group A" if winner == "Group B" else "Group B", "Equal", "Cannot determine"],
        f"Compare {a_frac} vs {b_frac}.",
        level=level,
    )


def _dyn_mad(level: str) -> dict:
    data = sorted([random.randint(2, 12) for _ in range(4)])
    mean = sum(data) / len(data)
    mad = sum(abs(x - mean) for x in data) / len(data)
    mad_str = str(int(mad)) if mad == int(mad) else f"{mad:.1f}"
    return _mcq(
        _dyn_id(5, "mad"),
        "mad",
        f"Data: {', '.join(map(str, data))}. Mean = {mean:.1f}. What is the MAD?",
        mad_str,
        [str(int(mad) + 1), str(max(0, int(mad) - 1)), str(int(mean))],
        f"Average of |each value − mean| = {mad_str}.",
        level=level,
    )


def _dyn_powers_roots(level: str) -> dict:
    n = random.choice([64, 81, 121, 144, 169])
    root = int(math.isqrt(n))
    return _mcq(
        _dyn_id(1, "powers_roots"),
        "powers_roots",
        f"Solve for x: √x² = √{n}",
        str(root),
        [str(root + 1), str(root - 1), str(n // 10)],
        f"x² = {n} → x = {root} (principal root).",
        level=level,
    )


def _dyn_rational(level: str) -> dict:
    num, den = random.choice([(1, 4), (1, 5), (3, 8), (2, 5)])
    pct = Fraction(num, den) * 100
    pct_str = f"{float(pct):g}%"
    return _mcq(
        _dyn_id(1, "rational_numbers"),
        "rational_numbers",
        f"Convert {num}/{den} to a percent.",
        pct_str,
        [f"{pct_str.replace('.', '')}", f"{num}%", f"{den}%"],
        f"{num} ÷ {den} = {float(Fraction(num, den))} → ×100 = {pct_str}.",
        level=level,
    )


def _dyn_irrational(level: str) -> dict:
    n = random.choice([50, 72, 90, 110, 140])
    lo = int(math.isqrt(n))
    return _mcq(
        _dyn_id(1, "irrational_numbers"),
        "irrational_numbers",
        f"Between which two consecutive integers does √{n} lie?",
        f"{lo} and {lo + 1}",
        [f"{lo - 1} and {lo}", f"{lo + 1} and {lo + 2}", f"{lo} and {lo + 2}"],
        f"{lo}² = {lo*lo} and {(lo+1)}² = {(lo+1)**2}; {n} is between.",
        level=level,
    )


def _dyn_scientific(level: str) -> dict:
    exp = random.randint(4, 9)
    coef = round(random.uniform(1.2, 9.5), 2)
    return _mcq(
        _dyn_id(1, "scientific_notation"),
        "scientific_notation",
        f"Write {coef} × 10^{exp} in words: the coefficient is?",
        str(coef),
        [str(coef + 0.5), str(coef / 10), str(exp)],
        f"Scientific notation a × 10^n has coefficient a = {coef}.",
        level=level,
    )


def _dyn_sci_ops(level: str) -> dict:
    a_coef, a_exp = random.uniform(2, 8), random.randint(10, 20)
    b_coef, b_exp = random.uniform(1, 5), a_exp - random.randint(1, 3)
    result_coef = round(a_coef * b_coef, 2)
    result_exp = a_exp + b_exp
    while result_coef >= 10:
        result_coef /= 10
        result_exp += 1
    ans = f"{result_coef:g} × 10^{result_exp}"
    return _mcq(
        _dyn_id(1, "sci_notation_ops"),
        "sci_notation_ops",
        f"Simplify ({a_coef:g} × 10^{a_exp}) × ({b_coef:g} × 10^{b_exp}). Scientific notation?",
        ans,
        [f"{a_coef * b_coef:g} × 10^{result_exp}", f"{result_coef:g} × 10^{a_exp}", f"{result_coef:g} × 10^{b_exp}"],
        f"Multiply coefficients; add exponents → {ans}.",
        level=level,
    )


def _dyn_expressions(level: str) -> dict:
    start, step = random.randint(2, 6), random.randint(2, 4)
    n = random.randint(10, 50)
    ans = step * n + (start - step)
    return _mcq(
        _dyn_id(2, "expressions"),
        "expressions",
        f"Perimeter pattern: {start}, {start+step}, {start+2*step}, … Rule {step}n + {start-step}. Figure {n} perimeter?",
        str(ans),
        [str(ans + step), str(ans - step), str(step * n)],
        f"{step}({n}) + {start-step} = {ans}.",
        level=level,
    )


def _dyn_slope_intercept(level: str) -> dict:
    m, b = random.randint(2, 12), random.randint(50, 300)
    return _mcq(
        _dyn_id(2, "slope_intercept"),
        "slope_intercept",
        f"A gym charges y = {m}x + {b} for x months. What does {b} represent?",
        f"${b} sign-up fee before monthly charges",
        [f"${m} per month", f"Total after 1 month", f"${b} per month"],
        f"When x = 0, y = {b} → starting fee.",
        level=level,
    )


def _dyn_proportional(level: str) -> dict:
    rate = random.randint(3, 15)
    return _mcq(
        _dyn_id(2, "proportional"),
        "proportional",
        f"Cost y = {rate}x with no starting fee. Is this proportional?",
        f"Yes — through (0,0) with constant ratio {rate}",
        ["No — has a y-intercept", "No — rate changes", "Cannot tell"],
        f"y/x = {rate} always; line passes through origin.",
        level=level,
    )


def _dyn_systems(level: str) -> dict:
    m = random.randint(2, 5)
    return _mcq(
        _dyn_id(2, "systems"),
        "systems",
        f"y = {m}x + 1 and y = {m}x − 4 represent lines that are:",
        "Parallel with no solution",
        ["Intersecting once", "The same line", "Perpendicular"],
        f"Same slope {m}, different intercepts → parallel.",
        level=level,
    )


def _dyn_angles(level: str) -> dict:
    x = random.randint(20, 40)
    return _mcq(
        _dyn_id(3, "angles"),
        "angles",
        f"Vertical angles: one angle is ({2*x + 10})°. The vertical angle equals?",
        f"{2*x + 10}°",
        [f"{180 - (2*x + 10)}°", f"{90 - x}°", f"{x}°"],
        "Vertical angles are congruent.",
        level=level,
    )


def _dyn_transformations(level: str) -> dict:
    x, y = random.randint(2, 8), random.randint(2, 8)
    return _mcq(
        _dyn_id(3, "transformations"),
        "transformations",
        f"Point ({x}, {y}) reflected over the y-axis lands at:",
        f"({-x}, {y})",
        [f"({x}, {-y})", f"({y}, {x})", f"({-x}, {-y})"],
        "Reflection over y-axis negates x.",
        level=level,
    )


def _dyn_similarity(level: str) -> dict:
    k = random.choice([2, 3, 4])
    side = random.randint(3, 12)
    return _mcq(
        _dyn_id(3, "similarity"),
        "similarity",
        f"Similar figures scale factor {k}. Small side {side} cm → large side?",
        f"{k * side} cm",
        [f"{side + k} cm", f"{side // k} cm", f"{side} cm"],
        f"Multiply by scale factor: {side} × {k} = {k*side}.",
        level=level,
    )


def _dyn_surface_area(level: str) -> dict:
    e = random.randint(3, 9)
    sa = 6 * e * e
    return _mcq(
        _dyn_id(3, "surface_area"),
        "surface_area",
        f"Cube edge {e} cm. Total surface area?",
        f"{sa} cm²",
        [f"{e*e} cm²", f"{sa + 6} cm²", f"{4*e*e} cm²"],
        f"6 faces × {e}² = {sa} cm².",
        level=level,
    )


def _dyn_volume(level: str) -> dict:
    e = random.randint(3, 8)
    vol = e ** 3
    return _mcq(
        _dyn_id(3, "volume"),
        "volume",
        f"Cube volume {vol} cm³. Edge length?",
        f"{e} cm",
        [f"{e+1} cm", f"{vol // e} cm", f"{e-1} cm"],
        f"∛{vol} = {e} cm.",
        level=level,
    )


def _dyn_function_basics(level: str) -> dict:
    x = random.randint(2, 7)
    ans = 3 * x - 1
    return _mcq(
        _dyn_id(4, "function_basics"),
        "function_basics",
        f"If f(x) = 3x − 1, what is f({x})?",
        str(ans),
        [str(ans + 2), str(3 * x + 1), str(x - 1)],
        f"f({x}) = 3({x}) − 1 = {ans}.",
        level=level,
    )


def _dyn_comparing_functions(level: str) -> dict:
    r1, r2 = random.randint(2, 5), random.randint(6, 12)
    return _mcq(
        _dyn_id(4, "comparing_functions"),
        "comparing_functions",
        f"y = {r1}x vs y = {r2}x for x > 0. Which increases faster?",
        f"y = {r2}x",
        [f"y = {r1}x", "Both same", "Neither"],
        f"Larger slope {r2} → faster increase.",
        level=level,
    )


def _dyn_constructing(level: str) -> dict:
    start, rate = random.randint(2, 8), random.randint(2, 6)
    return _mcq(
        _dyn_id(4, "constructing"),
        "constructing",
        f"Starts at {start} cm and grows {rate} cm/week. Height h after w weeks?",
        f"h = {rate}w + {start}",
        [f"h = {start}w + {rate}", f"h = {rate}w", f"h = {start} + w"],
        f"Rate {rate} is slope; start {start} is intercept.",
        level=level,
    )


def _dyn_linear_functions(level: str) -> dict:
    x1, y1, x2, y2 = 0, random.randint(2, 8), 4, random.randint(10, 20)
    m = Fraction(y2 - y1, x2 - x1)
    return _mcq(
        _dyn_id(4, "linear_functions"),
        "linear_functions",
        f"Line through ({x1},{y1}) and ({x2},{y2}). Rate of change?",
        _mixed(m),
        [_mixed(m + 1), _mixed(-m), str(y2)],
        f"({y2}−{y1})/({x2}−{x1}) = {_mixed(m)}.",
        level=level,
    )


def _dyn_linear_nonlinear(level: str) -> dict:
    return _mcq(
        _dyn_id(4, "linear_nonlinear"),
        "linear_nonlinear",
        "Which table shows a nonlinear relationship?",
        "x: 1,2,3 → y: 1,4,9",
        ["x: 1,2,3 → y: 3,5,7", "x: 1,2,3 → y: 2,4,6", "x: 1,2,3 → y: 5,5,5"],
        "Equal Δx but y changes 3,5… not constant → nonlinear.",
        level=level,
    )


def _dyn_bivariate(level: str) -> dict:
    return _mcq(
        _dyn_id(5, "bivariate_data"),
        "bivariate_data",
        "Hours (1,2,3) and pages read (20,40,60). Describe the trend.",
        "Positive linear — pages increase 20 per hour",
        ["Negative", "No trend", "Nonlinear only"],
        "Both variables increase together at a constant rate.",
        level=level,
    )


_DYNAMIC_BY_CATEGORY: dict[str, callable] = {
    "patterns": _dyn_patterns,
    "fractions": _dyn_fractions,
    "powers_roots": _dyn_powers_roots,
    "rational_numbers": _dyn_rational,
    "irrational_numbers": _dyn_irrational,
    "exponents": _dyn_exponents,
    "scientific_notation": _dyn_scientific,
    "sci_notation_ops": _dyn_sci_ops,
    "expressions": _dyn_expressions,
    "solving_equations": _dyn_solving_equations,
    "slope": _dyn_slope,
    "slope_intercept": _dyn_slope_intercept,
    "proportional": _dyn_proportional,
    "systems": _dyn_systems,
    "angles": _dyn_angles,
    "transformations": _dyn_transformations,
    "similarity": _dyn_similarity,
    "pythagorean": _dyn_pythagorean,
    "surface_area": _dyn_surface_area,
    "volume": _dyn_volume,
    "function_basics": _dyn_function_basics,
    "comparing_functions": _dyn_comparing_functions,
    "constructing": _dyn_constructing,
    "linear_functions": _dyn_linear_functions,
    "linear_nonlinear": _dyn_linear_nonlinear,
    "scatter_association": _dyn_scatter,
    "bivariate_data": _dyn_bivariate,
    "mad": _dyn_mad,
    "two_way_tables": _dyn_two_way,
}


def categories_for_unit(unit_id: int) -> list[str]:
    return list(UNIT_CONCEPT_CHECK_CATEGORIES.get(unit_id, []))


def daily_concept_check_quota(session_count: int) -> int:
    """How many concept-check items to target in a daily unit session."""
    if session_count <= 0:
        return 0
    target = round(session_count * CONCEPT_CHECK_DAILY_RATIO)
    return max(2, min(session_count - 1, target))


def focus_concept_check_quota(session_count: int) -> int:
    target = round(session_count * CONCEPT_CHECK_FOCUS_RATIO)
    return max(1, min(session_count, target))


def is_concept_check(question: dict) -> bool:
    return question.get("source") == "concept_check"


def generate_concept_check_question(
    unit_id: int,
    category: str,
    level: str,
) -> dict | None:
    """Build a fresh concept-check MCQ when static bank items are exhausted."""
    gen = _DYNAMIC_BY_CATEGORY.get(category)
    if not gen:
        return None
    q = gen(level)
    q["unit_id"] = unit_id
    return q


def pick_or_generate_concept_check(
    unit_id: int,
    category: str,
    level: str,
    bank: list[dict],
    used_ids: set[str],
    avoid_ids: set[str],
    allowed_levels: set[str],
    *,
    xai_api_key: str | None = None,
    persist_ai: bool = True,
) -> dict | None:
    """Pick static/AI concept-check from bank, generate parametrically, or call Grok."""
    import arjun_course3_levels as c3lvl

    def _level_ok(lvl: str) -> bool:
        return not allowed_levels or lvl in allowed_levels

    def _try_pick(allow_recent: bool) -> dict | None:
        candidates = [
            q
            for q in bank
            if is_concept_check(q)
            and q.get("category") == category
            and q.get("id") not in used_ids
            and (allow_recent or q.get("id") not in avoid_ids)
        ]
        tagged = [(q, str(q.get("level") or c3lvl.infer_level(0, 1))) for q in candidates]
        for target in (level, *c3lvl.LEVEL_ORDER):
            if not _level_ok(target):
                continue
            pool = [q for q, lvl in tagged if lvl == target]
            random.shuffle(pool)
            if pool:
                q = dict(pool[0])
                used_ids.add(q["id"])
                return q
        return None

    for allow_recent in (False, True):
        picked = _try_pick(allow_recent)
        if picked:
            return picked

    if _level_ok(level) or not allowed_levels:
        generated = generate_concept_check_question(unit_id, category, level)
        if generated and generated["id"] not in used_ids:
            used_ids.add(generated["id"])
            return generated

    if xai_api_key:
        try:
            from arjun_course3_concept_check_llm import generate_concept_check_llm

            ai_q = generate_concept_check_llm(
                xai_api_key,
                unit_id,
                category,
                level,
                persist=persist_ai,
            )
            if ai_q and ai_q["id"] not in used_ids:
                used_ids.add(ai_q["id"])
                return ai_q
        except Exception:
            pass
    return None


def build_concept_check_bank(unit_id: int) -> list[dict]:
    """Return built-in concept-check MCQs for a unit."""
    gens = _UNIT_GENERATORS.get(unit_id, [])
    out: list[dict] = []
    for gen in gens:
        out.extend(gen())
    return out


def load_full_concept_check_bank(unit_id: int) -> list[dict]:
    """Built-in + AI-persisted concept-check questions."""
    from arjun_course3_concept_check_store import load_ai_bank

    seen: set[str] = set()
    merged: list[dict] = []
    for q in build_concept_check_bank(unit_id) + load_ai_bank(unit_id):
        qid = str(q.get("id", ""))
        if qid and qid in seen:
            continue
        merged.append(q)
        if qid:
            seen.add(qid)
    return merged


def extend_bank(base_bank: list[dict], unit_id: int) -> list[dict]:
    """Append concept-check questions (built-in + AI JSON) to a unit bank."""
    existing = {q.get("id") for q in base_bank}
    extra = [q for q in load_full_concept_check_bank(unit_id) if q.get("id") not in existing]
    return list(base_bank) + extra


_UNIT_GENERATORS: dict[int, list] = {
    1: [
        _gen_fractions,
        _gen_patterns,
        _gen_powers_roots,
        _gen_rational,
        _gen_irrational,
        _gen_exponents,
        _gen_scientific,
        _gen_sci_ops,
    ],
    2: [
        _gen_expressions,
        _gen_solving_equations,
        _gen_slope,
        _gen_slope_intercept,
        _gen_proportional,
        _gen_systems,
    ],
    3: [_gen_angles, _gen_pythagorean, _gen_volume, _gen_transformations, _gen_similarity, _gen_surface_area],
    4: [
        _gen_linear_functions,
        _gen_function_basics,
        _gen_comparing_functions,
        _gen_constructing,
        _gen_linear_nonlinear,
    ],
    5: [_gen_scatter, _gen_two_way, _gen_bivariate, _gen_mad],
}
