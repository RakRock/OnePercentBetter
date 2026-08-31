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
  (8) Systems: solve without graphing, write a system for a given point, or SET UP a quantity+value word problem (do not solve).
  (9) Angle pairs: alternate interior/exterior, corresponding, same-side interior, vertical; algebra with 90° or 180°.
  (10) Triangle/quadrilateral angles: interior sum, exterior-angle theorem, "can these angles form a polygon?"
  (11) Transformations: identify 90°/180°/dilation from a point pair; compositions (order matters); rigid vs non-rigid.
  (12) Similarity: corresponding angles, scale factor, missing side, area scales by k², perimeter by k.
  (13) Pythagorean: converse, missing side (including radicals), coordinate distance, 3-D space diagonal.
  (14) Volume/SA: triangular-prism lateral vs total SA vs volume; cone/cylinder/pyramid; leave π exact; composite solids.
  (15) Functions: domain from points, mapping/table "is it a function?", discrete vs continuous, write y=mx+b from a table, interpret rate and start, qualitative distance-time graphs.
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
        "Solve a 2×2 system by elimination or substitution (integer solution)",
        "Write a system whose only solution is a given point",
        "Quantity + value word problem: SET UP the system, do not solve",
        "Describe or identify a system with no solution (parallel lines)",
    ],
    "angles": [
        "Identify alternate interior, corresponding, alternate exterior, or same-side interior",
        "Which angle pairs are congruent vs supplementary (select-all style)",
        "Algebra: corresponding/alternate equal, or same-side interiors sum to 180°",
        "Triangle angle-sum word problem; exterior-angle theorem; quadrilateral sum 360°",
    ],
    "pythagorean": [
        "Converse: is 8-15-17 (or similar) a right triangle?",
        "Missing side with radicals: √2 and √18 → other leg 4",
        "Coordinate distance between two points",
        "3-D space diagonal of a rectangular prism; tree/statue shadow word problem",
    ],
    "volume": [
        "Triangular-prism volume V = Bh",
        "Cone or cylinder volume in terms of π; find missing h or r",
        "Pyramid V = (1/3)Bh; composite cylinder+cone or cylinder−hemisphere",
    ],
    "function_basics": [
        "Domain from plotted points (−5,1), (−1,5), (0,−2), (2,−1), (4,6)",
        "Mapping/table: (1,4), (2,4), (5,4), (5,8) is NOT a function",
        "Evaluate y = −6x + 2 at x = 5",
        "Discrete vs continuous: tickets vs time-to-eat 10 hot dogs",
    ],
    "linear_functions": [
        "Table 0,1,2 min → 12,16,20 pineapples → y = 4x + 12",
        "Bathtub 220, 209, 198 L → y = −11x + 220; after 5 min; empty when y=0",
        "Interpret slope as pineapples per minute and intercept as starting amount",
    ],
    "scatter_association": [
        "More TV hours, lower scores → negative; more homework, higher scores → positive",
        "Describe direction, form (linear), and strength from a word description",
        "One outlier far from the cluster: removing it makes the trend stronger",
    ],
    "two_way_tables": [
        "Defense 35 pizza + 9 burger: what percent prefer burger? 9/44",
        "330 of 500 males always wear a seat belt → 66%",
        "Compare row percents to decide if two groups are associated",
        "Of 50 students 30 prefer pizza vs 15 of 40 adults — who has the greater fraction?",
    ],
    "transformations": [
        "Identify 90° CCW, 180° about origin, or dilation from a point pair",
        "Composition: translate, then rotate/reflect/dilate — track (x, y)",
        "Order matters; double reflection over both axes = 180° rotation",
        "Which is NOT rigid? Dilations",
    ],
    "similarity": [
        "Corresponding angles in similar triangles (180° − given)",
        "Scale factor from side ratios; missing side via proportion",
        "Area scales by k²; perimeter scales by k; inverse scale for the smaller figure",
    ],
    "surface_area": [
        "Triangular-prism lateral area (perimeter of base × length)",
        "Total SA = lateral + 2 triangular bases",
        "Cube or rectangular prism surface area",
    ],
    "bivariate_data": [
        "Hours 1,2,3 and pages 20,40,60 — predict pages at 5 hours",
        "Use trend line y = 8x + 12 to predict y when x = 6",
        "Warn against extrapolation far outside the data",
    ],
    "comparing_functions": [
        "Shop A: C = 5h + 20 vs Shop B: C = 6h + 15 — who has the greater hourly rate?",
        "After 10 hours, which shop costs less? Compute both totals",
        "Distance-time graph: running home must be steeper than walking there",
    ],
    "constructing": [
        "Giants tickets: y = 200x + 20 (fees + per ticket)",
        "Movies: 4 per year → y = 4x; discrete points not a solid line",
        "Table x: −4, 10, 28 and y: 8, 15, 24 → y = (1/2)x + 10",
    ],
    "linear_nonlinear": [
        "Squares table 1,4,9 is nonlinear; 2,4,6 is linear",
        "Uneven x-gaps but constant Δy/Δx = 1/2 is still linear",
        "Error analysis: student called a curve linear because it 'goes up'",
    ],
    "mad": [
        "Data 4, 6, 8, 10; mean 7; MAD = 2",
        "Compare two teams' MAD — smaller MAD is more consistent",
        "Compute MAD from a 5-value set; show |each − mean| then average",
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
    seen = {correct}
    unique_wrong: list[str] = []
    for item in list(wrong) + [
        "Cannot tell from the given information",
        "None of these",
        "Not enough information",
    ]:
        if item in seen:
            continue
        seen.add(item)
        unique_wrong.append(item)
        if len(unique_wrong) == 3:
            break
    opts = [correct] + unique_wrong[:3]
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
        _mcq(
            "cc_u2_sys_solve",
            "systems",
            "Solve using any method except graphing: 2x + 5y = 16 and 4y = 3x − 24.",
            "(8, 0)",
            ["(0, 8)", "(8, 4)", "(2, 0)"],
            "Rewrite as −3x + 4y = −24. Eliminate x: 3(2x+5y) + 2(−3x+4y) = 48 − 48 → 23y = 0 → y = 0, x = 8.",
            level="D",
        ),
        _mcq(
            "cc_u2_sys_write_point",
            "systems",
            "Which system has (2, −4) as its only solution?",
            "x + y = −2 and x − y = 6",
            [
                "x + y = 2 and x − y = −4",
                "x + y = −2 and x − y = −6",
                "2x + y = 0 and x + y = 2",
            ],
            "Plug in (2, −4): 2 + (−4) = −2 and 2 − (−4) = 6. Two independent lines meet at one point.",
            level="C",
        ),
        _mcq(
            "cc_u2_sys_setup_pies",
            "systems",
            (
                "Apple pies cost $5 and pumpkin pies cost $4. You bought 13 pies and spent $58. "
                "Which system could be used to solve this? Do NOT solve."
            ),
            "x + y = 13 and 5x + 4y = 58",
            [
                "x + y = 58 and 5x + 4y = 13",
                "5x + 4y = 13 and x + y = 58",
                "x + y = 13 and 5x + 4y = 13",
            ],
            "Let x = apple pies, y = pumpkin pies. Count: x+y=13. Cost: 5x+4y=58.",
            level="C",
        ),
        _mcq(
            "cc_u2_sys_solve2",
            "systems",
            "Solve: 4x − 5y = 23 and 6x + 9y = −15.",
            "(2, −3)",
            ["(−2, 3)", "(3, −2)", "(2, 3)"],
            "Eliminate x: −3(4x−5y)+2(6x+9y) = −69 − 30 → 33y = −99 → y = −3, then x = 2.",
            level="D",
        ),
        _mcq(
            "cc_u2_sys_setup_hours",
            "systems",
            (
                "Dwight raises $50 per hour and Clark raises $75 per hour. Together they worked 84 hours "
                "and raised $4,900. Which system could find their hours? Do NOT solve."
            ),
            "x + y = 84 and 50x + 75y = 4900",
            [
                "x + y = 4900 and 50x + 75y = 84",
                "50x + 75y = 84 and x + y = 4900",
                "x + y = 84 and 50x + 75y = 84",
            ],
            "x = Dwight hours, y = Clark hours. Total hours x+y=84. Total money 50x+75y=4900.",
            level="C",
        ),
        _mcq(
            "cc_u2_sys_write_1419",
            "systems",
            "Which system has (14, 9) as its only solution?",
            "x + y = 23 and x − y = 5",
            [
                "x + y = 14 and x − y = 9",
                "x + y = 23 and x − y = 23",
                "x + y = 5 and x − y = 23",
            ],
            "14+9=23 and 14−9=5. Two different lines through (14, 9) give a unique solution.",
            level="C",
        ),
    ]


# ── Unit 3–4 school-style generators ──


def _gen_pythagorean() -> list[dict]:
    return [
        _mcq(
            "cc_u3_pyth",
            "pythagorean",
            "A right triangle has legs 6 ft and 8 ft. How long is the hypotenuse?",
            "10 ft",
            ["8 ft", "14 ft", "12 ft"],
            "c² = 6² + 8² = 36 + 64 = 100 → c = 10.",
            level="C",
        ),
        _mcq(
            "cc_u3_pyth_converse",
            "pythagorean",
            "Determine if a triangle with sides 8, 15, and 17 is a right triangle.",
            "Yes — 8² + 15² = 17²",
            [
                "No — 8 + 15 ≠ 17",
                "Yes — 8 + 15 = 17",
                "No — 8² + 17² ≠ 15²",
            ],
            "8² + 15² = 64 + 225 = 289 = 17², so the converse of the Pythagorean theorem says it is right.",
            level="C",
        ),
        _mcq(
            "cc_u3_pyth_radicals",
            "pythagorean",
            "A right triangle has one leg √2 cm and hypotenuse √18 cm. What is the other leg?",
            "4 cm",
            ["√16 cm only if left unsimplified", "√20 cm", "3 cm"],
            "(√2)² + x² = (√18)² → 2 + x² = 18 → x² = 16 → x = 4 cm.",
            level="D",
        ),
        _mcq(
            "cc_u3_pyth_distance",
            "pythagorean",
            "Find the distance between (−4, 2) and (0, 5).",
            "5 units",
            ["7 units", "3 units", "√7 units"],
            "Horizontal change 4, vertical change 3: 4² + 3² = 25 → distance 5.",
            level="C",
        ),
        _mcq(
            "cc_u3_pyth_3d",
            "pythagorean",
            (
                "A box is 12 in by 9 in by 8 in. What is the space diagonal from one bottom corner "
                "to the opposite top corner?"
            ),
            "17 in",
            ["15 in", "21 in", "√145 in"],
            "d² = 12² + 9² + 8² = 144 + 81 + 64 = 289 → d = 17 in.",
            level="E",
        ),
        _mcq(
            "cc_u3_pyth_map",
            "pythagorean",
            (
                "On a map, Space Mountain is at (5, −1) and Rise of the Resistance is at (−4, 11). "
                "If 1 unit takes 3 minutes to walk, how long is the walk?"
            ),
            "45 minutes",
            ["15 minutes", "30 minutes", "36 minutes"],
            "Δx = 9, Δy = 12 → distance 15 units. 15 × 3 = 45 minutes.",
            level="D",
        ),
        _mcq(
            "cc_u3_pyth_shadow",
            "pythagorean",
            (
                "A tree casts a 15 ft shadow. The distance from the top of the tree to the tip of "
                "the shadow is 17 ft. How tall is the tree?"
            ),
            "8 ft",
            ["2 ft", "32 ft", "√481 ft"],
            "15² + h² = 17² → 225 + h² = 289 → h² = 64 → h = 8 ft.",
            level="C",
        ),
        _mcq(
            "cc_u3_pyth_statue",
            "pythagorean",
            (
                "A statue is 10 ft tall. The distance from the top of the statue to the tip of its "
                "shadow is √164 ft. How long is the shadow?"
            ),
            "8 ft",
            ["√64 ft left unsimplified only", "12 ft", "6 ft"],
            "10² + s² = 164 → 100 + s² = 164 → s² = 64 → s = 8 ft.",
            level="D",
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
        _mcq(
            "cc_u3_vol_prism",
            "volume",
            (
                "A right triangular prism has a 6 cm by 8 cm right-triangle base (hypotenuse 10 cm) "
                "and length 4 cm. What is its volume?"
            ),
            "96 cm³",
            ["96 cm²", "144 cm³", "192 cm³"],
            "Base area = (6×8)/2 = 24. Volume = Bh = 24 × 4 = 96 cm³.",
            level="C",
        ),
        _mcq(
            "cc_u3_vol_cone",
            "volume",
            "Find the volume of a cone with radius 9 and height 2. Leave the answer in terms of π.",
            "54π",
            ["162π", "54", "81π"],
            "V = (1/3)πr²h = (1/3)π(81)(2) = 54π.",
            level="C",
        ),
        _mcq(
            "cc_u3_vol_cyl_h",
            "volume",
            "A cylinder has volume 200π cubic units and radius 5. What is its height?",
            "8 units",
            ["5 units", "40 units", "8π units"],
            "πr²h = 200π → 25h = 200 → h = 8.",
            level="C",
        ),
        _mcq(
            "cc_u3_vol_pyramid",
            "volume",
            "A rectangular pyramid has base 13 yd by 7 yd and height 12 yd. What is its volume?",
            "364 yd³",
            ["1092 yd³", "273 yd³", "91 yd³"],
            "V = (1/3)Bh = (1/3)(13×7)(12) = (1/3)(91)(12) = 364 yd³.",
            level="D",
        ),
        _mcq(
            "cc_u3_vol_composite",
            "volume",
            (
                "A cylinder of radius 3 m and height 50 m sits on a cone with the same radius and "
                "height 4 m. What is the total volume, in terms of π?"
            ),
            "462π m³",
            ["450π m³", "462 m³", "150π m³"],
            "Cylinder: π(9)(50)=450π. Cone: (1/3)π(9)(4)=12π. Total 462π m³.",
            level="E",
        ),
        _mcq(
            "cc_u3_vol_cyl_r",
            "volume",
            "A cylinder has volume 144π and height 4. What is the radius?",
            "6 units",
            ["4 units", "12 units", "36 units"],
            "πr²(4) = 144π → 4r² = 144 → r² = 36 → r = 6.",
            level="C",
        ),
        _mcq(
            "cc_u3_vol_hemisphere",
            "volume",
            (
                "A hemisphere of radius 3 is scooped out of a cylinder of radius 4 and height 10. "
                "What remaining volume, in terms of π?"
            ),
            "142π",
            ["160π", "142", "118π"],
            "Cylinder 16π×10=160π. Hemisphere (2/3)π(27)=18π. Remaining 142π.",
            level="E",
        ),
        _mcq(
            "cc_u3_vol_cone_h",
            "volume",
            "A cone has volume 108π and radius 9. What is its height?",
            "4 units",
            ["12 units", "3 units", "36 units"],
            "(1/3)π(81)h = 108π → 27h = 108 → h = 4.",
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
        _mcq(
            "cc_u3_ang_supp2",
            "angles",
            "∠A and ∠B are supplementary. m∠A = 3x° and m∠B = (5x + 44)°. Find x.",
            "17",
            ["19", "15", "22"],
            "3x + 5x + 44 = 180 → 8x = 136 → x = 17.",
            level="C",
        ),
        _mcq(
            "cc_u3_ang_comp",
            "angles",
            "∠A and ∠B are complementary. m∠A = (2x + 14)° and m∠B = (5x + 6)°. Find x.",
            "10",
            ["8", "12", "20"],
            "2x+14+5x+6=90 → 7x+20=90 → 7x=70 → x=10.",
            level="C",
        ),
        _mcq(
            "cc_u3_ang_same_side",
            "angles",
            (
                "Parallel lines cut by a transversal form same-side interior angles (11x)° and "
                "(5x + 36)°. What is x?"
            ),
            "9",
            ["6", "12", "16"],
            "Same-side interiors are supplementary: 11x + 5x + 36 = 180 → 16x = 144 → x = 9.",
            level="D",
        ),
        _mcq(
            "cc_u3_ang_corresponding",
            "angles",
            (
                "Parallel lines: corresponding angles measure (3x + 10)° and (4x − 20)°. Find x."
            ),
            "30",
            ["10", "20", "15"],
            "Corresponding angles are congruent: 3x+10=4x−20 → 30=x.",
            level="C",
        ),
        _mcq(
            "cc_u3_ang_alt_int",
            "angles",
            (
                "Parallel lines: alternate interior angles measure (12x + 8)° and (3x + 26)°. Find x."
            ),
            "2",
            ["4", "6", "18"],
            "Alternate interiors are congruent: 12x+8=3x+26 → 9x=18 → x=2.",
            level="C",
        ),
        _mcq(
            "cc_u3_ang_vertical",
            "angles",
            "If m∠2 = 60° and ∠2 and ∠3 are vertical angles, what is m∠3? Why?",
            "60° — vertical angles are congruent",
            [
                "120° — they form a linear pair",
                "30° — they are complementary",
                "180° — they are supplementary",
            ],
            "Vertical angles are equal, so m∠3 = 60°.",
            level="B",
        ),
        _mcq(
            "cc_u3_ang_alt_ext",
            "angles",
            "If m∠2 = 60° and ∠2 and ∠7 are alternate exterior angles on parallel lines, m∠7 is:",
            "60° — alternate exterior angles are congruent",
            [
                "120° — they are supplementary",
                "30° — they are complementary",
                "Cannot tell without a diagram scale",
            ],
            "Alternate exterior angles formed by parallel lines are congruent.",
            level="B",
        ),
        _mcq(
            "cc_u3_ang_congruent_pairs",
            "angles",
            "When parallel lines are cut by a transversal, which pairs are congruent?",
            "Alternate interior, alternate exterior, corresponding, and vertical",
            [
                "Only vertical angles",
                "Only corresponding angles",
                "Same-side interior and linear pairs (those are supplementary, not congruent)",
            ],
            "Alt. int., alt. ext., corresponding, and vertical angles are congruent. Same-side interiors sum to 180°.",
            level="C",
        ),
        _mcq(
            "cc_u3_ang_tri_alg",
            "angles",
            "The angles of a triangle are x°, (2x + 15)°, and (4x − 10)°. Find x.",
            "25",
            ["20", "30", "35"],
            "x+2x+15+4x−10=180 → 7x+5=180 → 7x=175 → x=25.",
            level="C",
        ),
        _mcq(
            "cc_u3_ang_tri_word",
            "angles",
            (
                "In △ABC, ∠B is twice ∠A, and ∠C is 24° more than ∠A. What is m∠A?"
            ),
            "39°",
            ["36°", "48°", "52°"],
            "x + 2x + (x+24) = 180 → 4x+24=180 → 4x=156 → x=39°.",
            level="D",
        ),
        _mcq(
            "cc_u3_ang_tri_word2",
            "angles",
            (
                "In △XYZ, ∠Y is 3 times ∠X, and ∠Z is 20° less than ∠X. What are the three angles?"
            ),
            "40°, 120°, and 20°",
            ["40°, 80°, and 60°", "36°, 108°, and 16°", "45°, 135°, and 25°"],
            "x+3x+(x−20)=180 → 5x=200 → x=40. Then Y=120°, Z=20°.",
            level="D",
        ),
        _mcq(
            "cc_u3_ang_exterior",
            "angles",
            (
                "A triangle has remote interior angles 51° and (4x + 22)°. The exterior angle is "
                "(11x + 10)°. Find x."
            ),
            "9",
            ["5", "7", "11"],
            "Exterior-angle theorem: 51+4x+22 = 11x+10 → 73+4x=11x+10 → 63=7x → x=9.",
            level="D",
        ),
        _mcq(
            "cc_u3_ang_quad_sum",
            "angles",
            (
                "Bobana says she has a quadrilateral with angles 34°, 98°, 105°, and 122°. "
                "Bobryce says that cannot be true. Who is right?"
            ),
            "Bobryce — the angles add to 359°, not 360°",
            [
                "Bobana — any four angles make a quadrilateral",
                "Bobryce — quadrilaterals must add to 180°",
                "Neither — you cannot tell without a drawing",
            ],
            "34+98+105+122=359 ≠ 360, so those measures cannot be a quadrilateral.",
            level="C",
        ),
        _mcq(
            "cc_u3_ang_quad_why",
            "angles",
            "Why is the sum of the interior angles of any quadrilateral 360°?",
            "A diagonal splits it into two triangles, and 180° + 180° = 360°",
            [
                "Four right angles are required",
                "Each exterior angle is 90°",
                "Quadrilaterals have four sides, so 4 × 90°",
            ],
            "One diagonal makes two triangles; each triangle sums to 180°.",
            level="B",
        ),
        _mcq(
            "cc_u3_ang_quad_ext",
            "angles",
            (
                "A quadrilateral has interior angles 137°, 25°, and 155°. The fourth interior angle "
                "has an adjacent exterior angle y. What is y?"
            ),
            "137°",
            ["43°", "223°", "360°"],
            "Fourth interior = 360 − 317 = 43°. Exterior y is supplementary: 180 − 43 = 137°.",
            level="E",
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
        _mcq(
            "cc_u4_lin_table",
            "linear_functions",
            (
                "Minutes after 1 pm: 0, 1, 2. Pineapples eaten: 12, 16, 20. "
                "Which linear function relates pineapples y to minutes x?"
            ),
            "y = 4x + 12",
            ["y = 12x + 4", "y = 4x", "y = x + 12"],
            "Rate (16−12)/(1−0)=4. Start at 12 when x=0 → y=4x+12.",
            level="C",
        ),
        _mcq(
            "cc_u4_lin_interpret_m",
            "linear_functions",
            "For y = 4x + 12 pineapples after x minutes, what does the 4 mean?",
            "4 pineapples eaten per minute",
            ["12 pineapples per minute", "4 pineapples already eaten", "Total after 4 minutes"],
            "Slope is the rate of change: pineapples per minute.",
            level="B",
        ),
        _mcq(
            "cc_u4_lin_interpret_b",
            "linear_functions",
            "For y = 4x + 12 pineapples after x minutes, what does the 12 mean?",
            "12 pineapples already eaten at 1 pm",
            ["12 pineapples per minute", "You eat 12 more each minute", "The domain"],
            "Initial value (y-intercept) is the starting amount when x=0.",
            level="B",
        ),
        _mcq(
            "cc_u4_lin_bathtub",
            "linear_functions",
            (
                "A tub has 220 L at 0 min, 209 L at 1 min, and 198 L at 2 min. "
                "Which function gives liters y after x minutes?"
            ),
            "y = −11x + 220",
            ["y = 11x + 220", "y = −11x", "y = 220x − 11"],
            "Rate (209−220)/1 = −11 L/min. Start 220 → y=−11x+220.",
            level="C",
        ),
        _mcq(
            "cc_u4_lin_bathtub_eval",
            "linear_functions",
            "Using y = −11x + 220, how many liters remain after 5 minutes?",
            "165 L",
            ["175 L", "55 L", "209 L"],
            "y = −11(5)+220 = −55+220 = 165 L.",
            level="C",
        ),
        _mcq(
            "cc_u4_lin_bathtub_zero",
            "linear_functions",
            "Using y = −11x + 220, after how many minutes is the tub empty?",
            "20 minutes",
            ["11 minutes", "220 minutes", "15 minutes"],
            "0 = −11x + 220 → 11x = 220 → x = 20 minutes.",
            level="D",
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
        _mcq(
            "cc_u5_sc_tv",
            "scatter_association",
            "Students who watch more TV hours tend to have lower test scores. What association is this?",
            "Negative association",
            ["Positive association", "No association", "Cannot tell"],
            "TV hours up, scores down → negative association.",
            level="B",
        ),
        _mcq(
            "cc_u5_sc_hot_choc",
            "scatter_association",
            (
                "A scatter plot of daily temperature vs cups of hot chocolate sold goes down "
                "from left to right, with points close to a straight line. Describe it."
            ),
            "Strong negative linear association",
            [
                "Weak positive association",
                "No association",
                "Strong positive linear association",
            ],
            "As temperature rises, sales fall, and points hug a line → strong negative linear.",
            level="C",
        ),
        _mcq(
            "cc_u5_sc_outlier",
            "scatter_association",
            (
                "Eleven points show a clear positive trend (more practice, more goals). "
                "One outlier is many hours with almost no goals. If you remove the outlier, "
                "what happens to the trend?"
            ),
            "The positive association becomes stronger",
            [
                "The association becomes negative",
                "The trend disappears",
                "The association becomes weaker",
            ],
            "The outlier pulls against the pattern. Removing it makes the positive trend clearer.",
            level="D",
        ),
        _mcq(
            "cc_u5_sc_none",
            "scatter_association",
            (
                "A plot of shoe size vs favorite ice-cream flavor score looks like a random cloud "
                "with no up or down pattern. What association is shown?"
            ),
            "No association",
            ["Positive linear", "Negative linear", "Strong nonlinear only"],
            "No direction: knowing shoe size does not help predict the score.",
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
        _mcq(
            "cc_u5_tw_burger",
            "two_way_tables",
            (
                "Offense: 23 pizza, 21 burger. Defense: 35 pizza, 9 burger. "
                "What percent of defensive players prefer burger?"
            ),
            "About 20.5% (9/44)",
            ["9%", "35%", "About 50%"],
            "Defense total = 35+9=44. Burger share = 9/44 ≈ 20.5%.",
            level="C",
        ),
        _mcq(
            "cc_u5_tw_seatbelt",
            "two_way_tables",
            "330 of 500 males always wear a seat belt. What percent is that?",
            "66%",
            ["33%", "50%", "330%"],
            "330/500 = 0.66 = 66%.",
            level="B",
        ),
        _mcq(
            "cc_u5_tw_assoc",
            "two_way_tables",
            (
                "Males: 66% always wear a seat belt. Females: 325 of 500 always wear one. "
                "Is there a meaningful association with gender?"
            ),
            "No — 325/500 = 65%, almost the same as 66%",
            [
                "Yes — the percents are completely different",
                "Yes — males are twice as likely",
                "Cannot compare percents from two-way tables",
            ],
            "Row percents 66% vs 65% are nearly equal, so little association.",
            level="D",
        ),
        _mcq(
            "cc_u5_tw_row",
            "two_way_tables",
            (
                "A table shows 12 sixth graders and 18 seventh graders like soccer; "
                "8 sixth graders and 6 seventh graders like basketball. "
                "What fraction of sixth graders like soccer?"
            ),
            "12/20 = 3/5",
            ["12/18", "12/44", "18/24"],
            "Sixth-grade total = 12+8=20. Soccer = 12/20 = 3/5.",
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
        _mcq(
            "cc_u3_tr_180",
            "transformations",
            "Point A is at (4, 10) and A′ is at (−4, −10). If this was NOT a translation, what happened?",
            "180° rotation about the origin",
            [
                "Reflection over the x-axis only",
                "90° counterclockwise about the origin",
                "Dilation by −1 from (4, 10)",
            ],
            "(x, y) → (−x, −y) is a 180° rotation about the origin.",
            level="C",
        ),
        _mcq(
            "cc_u3_tr_90ccw",
            "transformations",
            "Identify the transformation (not a translation): (9, −12) → (12, 9).",
            "90° counterclockwise about the origin",
            [
                "90° clockwise about the origin",
                "180° about the origin",
                "Reflection over y = x",
            ],
            "90° CCW rule is (x, y) → (−y, x): −(−12)=12 and x=9.",
            level="C",
        ),
        _mcq(
            "cc_u3_tr_compose1",
            "transformations",
            (
                "B is at (−5, 9). Translate 4 right and 12 down, rotate 90° CCW about the origin, "
                "then reflect across y = x. Where is B‴?"
            ),
            "(−1, 3)",
            ["(3, −1)", "(−1, −3)", "(1, −3)"],
            "Translate → (−1, −3). 90° CCW (−y, x) → (3, −1). Reflect y=x (y, x) → (−1, 3).",
            level="E",
        ),
        _mcq(
            "cc_u3_tr_compose2",
            "transformations",
            (
                "A is at (3, 1). Translate 8 right and 5 down, reflect over the x-axis, "
                "then rotate 270° CCW about the origin. Where is A‴?"
            ),
            "(4, −11)",
            ["(11, 4)", "(−4, 11)", "(4, 11)"],
            "Translate → (11, −4). Reflect x-axis → (11, 4). 270° CCW (y, −x) → (4, −11).",
            level="E",
        ),
        _mcq(
            "cc_u3_tr_order",
            "transformations",
            (
                "If you do the same three transformations as above but in reverse order, "
                "does A end in the same place?"
            ),
            "No — order of transformations matters",
            [
                "Yes — compositions always commute",
                "Yes — each step is a rigid motion",
                "Only if you include a dilation",
            ],
            "Translations, reflections, and rotations do not all commute; reverse order lands elsewhere.",
            level="C",
        ),
        _mcq(
            "cc_u3_tr_combine",
            "transformations",
            (
                "Write one rule for: translate 12 left and 1 up, then apply (x, y) → (x + 9, y − 12)."
            ),
            "(x, y) → (x − 3, y − 11)",
            [
                "(x, y) → (x − 21, y + 13)",
                "(x, y) → (x + 3, y − 11)",
                "(x, y) → (x − 3, y + 11)",
            ],
            "First (x−12, y+1), then add (9, −12) → (x−3, y−11).",
            level="D",
        ),
        _mcq(
            "cc_u3_tr_rigid",
            "transformations",
            "Which of these is NOT a rigid transformation?",
            "Dilations",
            ["Translations", "Reflections", "Rotations"],
            "Rigid motions preserve distance. Dilations change size.",
            level="B",
        ),
        _mcq(
            "cc_u3_tr_double_ref",
            "transformations",
            (
                "A point is reflected across the x-axis and then across the y-axis. "
                "Besides a translation, what single transformation matches that?"
            ),
            "180° rotation about the origin",
            [
                "90° counterclockwise about the origin",
                "Reflection over y = x",
                "Dilation by −1 from the point",
            ],
            "Reflect x then y: (x, y) → (x, −y) → (−x, −y), which is 180° about the origin.",
            level="D",
        ),
        _mcq(
            "cc_u3_tr_dilate",
            "transformations",
            "Identify the transformation (not a translation): (12, 16) → (27, 36).",
            "Dilation by 9/4 about the origin",
            [
                "Dilation by 4/9 about the origin",
                "90° counterclockwise about the origin",
                "Translation 15 right and 20 up only",
            ],
            "27/12 = 36/16 = 9/4, so both coordinates scale by 9/4 from the origin.",
            level="D",
        ),
    ]


def _gen_similarity() -> list[dict]:
    return [
        _mcq(
            "cc_u3_similar",
            "similarity",
            (
                "Two similar triangles have a scale factor of 3 (small → large). "
                "A side on the smaller triangle is 5 cm. What is the matching side on the larger triangle?"
            ),
            "15 cm",
            ["8 cm", "12 cm", "5 cm"],
            "Multiply corresponding sides by the scale factor: 5 × 3 = 15 cm.",
            level="C",
        ),
        _mcq(
            "cc_u3_sim_angles",
            "similarity",
            "△CHL ∼ △ZOE. m∠C = 50° and m∠O = 100°. What is m∠L?",
            "30°",
            ["50°", "100°", "80°"],
            "Corresponding angles: ∠H ↔ ∠O = 100°. Then m∠L = 180 − 50 − 100 = 30°.",
            level="C",
        ),
        _mcq(
            "cc_u3_sim_sides",
            "similarity",
            (
                "△ABC has sides 10, 24, 26. △XYZ has corresponding sides 15, 36, 39. "
                "Are they similar, and what is the scale factor of ABC to XYZ?"
            ),
            "Yes — scale factor 3/2",
            [
                "Yes — scale factor 2/3",
                "No — the sides are not proportional",
                "Yes — scale factor 5",
            ],
            "15/10 = 36/24 = 39/26 = 3/2, so △ABC ∼ △XYZ with k = 3/2.",
            level="C",
        ),
        _mcq(
            "cc_u3_sim_area",
            "similarity",
            "△ABC ∼ △XYZ with scale factor 5 (ABC → XYZ). If area of ABC is 8 m², area of XYZ is:",
            "200 m²",
            ["40 m²", "13 m²", "25 m²"],
            "Areas scale by k²: 5² × 8 = 25 × 8 = 200 m².",
            level="D",
        ),
        _mcq(
            "cc_u3_sim_perim",
            "similarity",
            "△ABC ∼ △XYZ with scale factor 5 (ABC → XYZ). If perimeter of ABC is 4 m, perimeter of XYZ is:",
            "20 m",
            ["9 m", "100 m", "4/5 m"],
            "Perimeters scale by k: 4 × 5 = 20 m.",
            level="C",
        ),
        _mcq(
            "cc_u3_sim_inverse",
            "similarity",
            (
                "Figure A ∼ figure B. Scale factor of A to B is 7/2. "
                "A side of B is 42. What is the matching side of A?"
            ),
            "12",
            ["147", "21", "6"],
            "A is smaller: multiply by 2/7. 42 × (2/7) = 12.",
            level="D",
        ),
        _mcq(
            "cc_u3_sim_missing",
            "similarity",
            (
                "△ABC ∼ △DEF. AC = 63 m and DF = 14 m. Hypotenuse BC = 90 m and EF = x. "
                "What is x?"
            ),
            "20 m",
            ["405 m", "76 m", "14 m"],
            "k of ABC to DEF is 14/63 = 2/9. Then x = 90 × (2/9) = 20 m.",
            level="D",
        ),
        _mcq(
            "cc_u3_sim_alg",
            "similarity",
            (
                "△ABC ∼ △DEF. Heights (3x + 15) and x, hypotenuses 65 and 13. Find x."
            ),
            "7.5",
            ["5", "13", "15"],
            "65/13 = (3x+15)/x → 5 = (3x+15)/x → 5x = 3x+15 → 2x = 15 → x = 7.5.",
            level="E",
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
        _mcq(
            "cc_u3_sa_prism_lat",
            "surface_area",
            (
                "A right triangular prism has a 6-8-10 cm triangular base and length 4 cm. "
                "What is the lateral area?"
            ),
            "96 cm²",
            ["144 cm²", "48 cm²", "96 cm³"],
            "Lateral area = perimeter of base × length = (6+8+10)×4 = 96 cm².",
            level="C",
        ),
        _mcq(
            "cc_u3_sa_prism_total",
            "surface_area",
            (
                "Same 6-8-10 prism of length 4 cm. What is the total surface area?"
            ),
            "144 cm²",
            ["96 cm²", "192 cm²", "48 cm²"],
            "Lateral 96 plus two triangular bases: 2×(6×8)/2 = 48. Total 144 cm².",
            level="D",
        ),
        _mcq(
            "cc_u3_sa_prism2",
            "surface_area",
            (
                "An isosceles triangular prism has base sides 10, 10, and 12, triangle height 8, "
                "and length 20. What is the lateral area?"
            ),
            "640",
            ["96", "736", "320"],
            "Perimeter 10+10+12=32. Lateral = 32×20 = 640.",
            level="C",
        ),
        _mcq(
            "cc_u3_sa_prism2_total",
            "surface_area",
            "For that same prism (sides 10-10-12, height 8, length 20), what is the total surface area?",
            "736",
            ["640", "96", "800"],
            "Two bases: 2×(1/2)×12×8 = 96. Total SA = 640 + 96 = 736.",
            level="D",
        ),
        _mcq(
            "cc_u3_sa_345",
            "surface_area",
            "A 3-4-5 triangular prism has length 9 cm. What is the total surface area?",
            "120 cm²",
            ["108 cm²", "54 cm²", "135 cm²"],
            "Lateral (3+4+5)×9=108. Two bases 2×(1/2)×3×4=12. Total 120 cm².",
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
        _mcq(
            "cc_u4_fn_domain",
            "function_basics",
            (
                "A graph shows the points (−5, 1), (−1, 5), (0, −2), (2, −1), and (4, 6). "
                "What is the domain?"
            ),
            "{−5, −1, 0, 2, 4}",
            [
                "{1, 5, −2, −1, 6}",
                "All real numbers",
                "{−5, −1, 0, 2, 4, 1, 5}",
            ],
            "Domain is the set of x-values of the plotted points.",
            level="B",
        ),
        _mcq(
            "cc_u4_fn_graph",
            "function_basics",
            "Is that five-point graph a function? Why?",
            "Yes — each x-value has exactly one y-value",
            [
                "No — some y-values repeat",
                "No — the points are not on a line",
                "Only if you connect the dots",
            ],
            "No input repeats with a different output, so it is a function.",
            level="B",
        ),
        _mcq(
            "cc_u4_fn_mapping",
            "function_basics",
            "A table lists pairs (1, 4), (2, 4), (5, 4), and (5, 8). Is this a function?",
            "No — input 5 has two different outputs",
            [
                "Yes — outputs can repeat",
                "Yes — 4 appears more than once",
                "Only if you draw a mapping",
            ],
            "Input 5 maps to both 4 and 8, so it is not a function.",
            level="B",
        ),
        _mcq(
            "cc_u4_fn_table_yes",
            "function_basics",
            "A table lists pairs (1, 4), (2, 4), (5, 4), and (6, 8). Is this a function?",
            "Yes — no input repeats",
            [
                "No — output 4 repeats",
                "No — the y-values are not increasing",
                "Only if it is linear",
            ],
            "Each x appears once. Repeated outputs are allowed.",
            level="B",
        ),
        _mcq(
            "cc_u4_fn_continuous",
            "function_basics",
            (
                "Is the time it takes you to eat 10 hot dogs discrete or continuous? Why?"
            ),
            "Continuous — time can be any value, including fractions of a second",
            [
                "Discrete — you eat a whole number of hot dogs",
                "Discrete — you cannot finish in 5.1 seconds",
                "Neither — time is only measured in minutes",
            ],
            "Time can take any real value in an interval, so the measurement is continuous.",
            level="C",
        ),
        _mcq(
            "cc_u4_fn_discrete",
            "function_basics",
            (
                "Tickets cost $200 each plus $20 in fees: y = 200x + 20. "
                "What does the domain represent, and is it discrete or continuous?"
            ),
            "Number of tickets — discrete (you cannot buy half a ticket)",
            [
                "Total cost — continuous",
                "Number of tickets — continuous because money is continuous",
                "The $20 fee — discrete",
            ],
            "x is a count of tickets, so only whole numbers make sense → discrete.",
            level="C",
        ),
        _mcq(
            "cc_u4_fn_eval",
            "function_basics",
            "Use y = −6x + 2. What is y when x = 5?",
            "−28",
            ["28", "−32", "32"],
            "−6(5) + 2 = −30 + 2 = −28.",
            level="B",
        ),
        _mcq(
            "cc_u4_fn_range",
            "function_basics",
            (
                "Points (−5, 1), (−1, 5), (0, −2), (2, −1), and (4, 6) form a function. "
                "What is the range?"
            ),
            "{−2, −1, 1, 5, 6}",
            [
                "{−5, −1, 0, 2, 4}",
                "{1, 5, −2, −1, 6, −5}",
                "All real numbers",
            ],
            "Range is the set of y-values: −2, −1, 1, 5, and 6.",
            level="C",
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
        _mcq(
            "cc_u4_compare_qual",
            "comparing_functions",
            (
                "A distance-from-home graph shows a steep line away, a flat segment, then a "
                "shallower line back. The story is: walk to a friend, hang out, run home. "
                "Does the graph match? Why?"
            ),
            "No — running home should be steeper than walking there",
            [
                "Yes — the flat part is hanging out",
                "Yes — any return path works",
                "No — hanging out should slope upward",
            ],
            "The return segment is less steep than the outbound walk, but running is faster, so it should be steeper.",
            level="D",
        ),
        _mcq(
            "cc_u4_compare_total",
            "comparing_functions",
            (
                "Shop A charges C = 5h + 20. Shop B charges C = 6h + 15. "
                "After 10 hours, which shop is cheaper, and by how much?"
            ),
            "Shop A is cheaper by $5 (70 vs 75)",
            [
                "Shop B is cheaper by $5",
                "They cost the same",
                "Shop A is cheaper by $20",
            ],
            "A: 5(10)+20=70. B: 6(10)+15=75. Shop A costs $5 less.",
            level="C",
        ),
        _mcq(
            "cc_u4_compare_error",
            "comparing_functions",
            (
                "Maya says y = 8x + 3 grows faster than y = 3x + 80 because 80 is bigger. "
                "What is Maya's error?"
            ),
            "She compared intercepts; the rate (slope) 8 is larger than 3",
            [
                "She is right — 80 means it grows faster",
                "Both grow at the same rate",
                "You cannot compare two linear functions",
            ],
            "Growth speed is the slope. 8 > 3, so y=8x+3 increases faster. 80 is only the start.",
            level="D",
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
        _mcq(
            "cc_u4_con_tickets",
            "constructing",
            (
                "A Giants game costs $20 in online fees plus $200 per ticket. "
                "Which function relates total cost y to tickets x?"
            ),
            "y = 200x + 20",
            ["y = 20x + 200", "y = 220x", "y = 200x"],
            "Rate $200 per ticket; $20 fee is the starting value.",
            level="B",
        ),
        _mcq(
            "cc_u4_con_movies",
            "constructing",
            "A studio releases 4 movies per year. Which function gives total movies y after x years?",
            "y = 4x",
            ["y = x + 4", "y = 4x + 4", "y = x/4"],
            "Starts at 0 movies and adds 4 each year → y = 4x.",
            level="B",
        ),
        _mcq(
            "cc_u4_con_linear_table",
            "constructing",
            (
                "A table has x: −4, 10, 28 and y: 8, 15, 24. It has a constant rate of change. "
                "Write the linear function."
            ),
            "y = (1/2)x + 10",
            ["y = 2x + 10", "y = (1/2)x + 8", "y = x + 12"],
            "m = (15−8)/(10−(−4)) = 7/14 = 1/2. Using (10, 15): 15 = (1/2)(10)+b → b=10.",
            level="D",
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
        _mcq(
            "cc_u4_lin_croc",
            "linear_nonlinear",
            (
                "x: −4, 10, 28 and y: 8, 15, 24. Δx is 14 then 18; Δy is 7 then 9. "
                "Is this a linear function?"
            ),
            "Yes — Δy/Δx = 1/2 both times (constant rate of change)",
            [
                "No — the x-steps are not equal",
                "No — the y-steps are not equal",
                "Only if you plot it and it looks straight",
            ],
            "7/14 = 9/18 = 1/2, so the rate is constant even though the x-gaps differ.",
            level="D",
        ),
        _mcq(
            "cc_u4_lin_discrete_graph",
            "linear_nonlinear",
            (
                "A studio makes 4 movies per year for 5 years. Which graph is correct?"
            ),
            "Discrete points at (1, 4), (2, 8), …, (5, 20) — you cannot make half a movie",
            [
                "A solid line through those points",
                "A curve starting at the origin",
                "Only a bar for year 5",
            ],
            "Movie counts are discrete, so plot points with gaps, not a continuous line.",
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
        _mcq(
            "cc_u5_bv_pages",
            "bivariate_data",
            (
                "Hours 1, 2, 3 match pages read 20, 40, 60. "
                "If the pattern continues, how many pages after 5 hours?"
            ),
            "100",
            ["80", "60", "120"],
            "Pages increase 20 per hour. After 5 hours: 20×5=100.",
            level="C",
        ),
        _mcq(
            "cc_u5_bv_predict",
            "bivariate_data",
            "A trend line is y = 8x + 12. Predict y when x = 6.",
            "60",
            ["48", "20", "72"],
            "y = 8(6)+12 = 48+12 = 60.",
            level="C",
        ),
        _mcq(
            "cc_u5_bv_extra",
            "bivariate_data",
            (
                "A trend line from TV hours 0–12 is used to predict the score at 40 hours of TV. "
                "Why is that prediction risky?"
            ),
            "It is extrapolation — 40 hours is far outside the data",
            [
                "Trend lines can never be used to predict",
                "40 is less than 12 so it is interpolation",
                "You must use MAD instead",
            ],
            "Predicting far beyond the data range is extrapolation and can be unreliable.",
            level="D",
        ),
        _mcq(
            "cc_u5_bv_slope",
            "bivariate_data",
            (
                "A trend line for practice hours x and points scored y is y = 3x + 5. "
                "What does the 3 mean?"
            ),
            "About 3 more points for each extra hour of practice",
            ["Starting points when x = 0 is 3", "Exactly 3 hours of practice", "The MAD is 3"],
            "Slope 3 is the rate: points per hour of practice.",
            level="C",
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
        _mcq(
            "cc_u5_mad_compute",
            "mad",
            "Data: 2, 4, 6, 8, 10. Mean = 6. What is the MAD?",
            "2.4",
            ["2", "6", "4"],
            "Deviations 4,2,0,2,4. Average = 12/5 = 2.4.",
            level="D",
        ),
        _mcq(
            "cc_u5_mad_compare",
            "mad",
            (
                "Team A scores have MAD 2. Team B scores have MAD 6. "
                "Which team is more consistent, and why?"
            ),
            "Team A — smaller MAD means scores stay closer to the mean",
            [
                "Team B — larger MAD means more consistent",
                "They are equally consistent",
                "You need the mean, not the MAD",
            ],
            "MAD is average distance from the mean. Smaller MAD → less spread → more consistent.",
            level="C",
        ),
        _mcq(
            "cc_u5_mad_steps",
            "mad",
            "Data: 10, 10, 10, 22. Mean = 13. What is the MAD?",
            "4.5",
            ["3", "13", "12"],
            "Deviations: 3, 3, 3, 9. Average = 18/4 = 4.5.",
            level="D",
        ),
        _mcq(
            "cc_u5_mad_meaning",
            "mad",
            "A class has mean score 80 and MAD 3. What does that tell you?",
            "Typical scores are about 3 points from 80",
            [
                "Everyone scored exactly 80",
                "The highest score is 83",
                "The mean is 3",
            ],
            "MAD is the average distance from the mean, so scores typically sit near 80 ± 3.",
            level="C",
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
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25)]
    a, b, c = random.choice(triples)
    style = random.choice(["hyp", "converse", "distance"])
    if style == "converse":
        return _mcq(
            _dyn_id(3, "pythagorean"),
            "pythagorean",
            f"Is a triangle with sides {a}, {b}, and {c} a right triangle?",
            f"Yes — {a}² + {b}² = {c}²",
            [
                f"No — {a} + {b} ≠ {c}",
                f"Yes — {a} + {b} = {c}",
                f"No — {a}² + {c}² ≠ {b}²",
            ],
            f"{a}² + {b}² = {a*a + b*b} = {c}².",
            level=level,
        )
    if style == "distance":
        x1, y1 = random.randint(-6, 2), random.randint(-2, 4)
        return _mcq(
            _dyn_id(3, "pythagorean"),
            "pythagorean",
            f"Distance between ({x1}, {y1}) and ({x1 + a}, {y1 + b})?",
            f"{c} units",
            [f"{a + b} units", f"{c + 2} units", f"{abs(a - b)} units"],
            f"Δx={a}, Δy={b} → {a}²+{b}²={c}² → distance {c}.",
            level=level,
        )
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
    style = random.choice(["parallel", "solve", "write", "setup"])
    if style == "parallel":
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
    if style == "write":
        px, py = random.randint(2, 12), random.randint(-8, 8)
        if py == 0:
            py = 3
        return _mcq(
            _dyn_id(2, "systems"),
            "systems",
            f"Which system has ({px}, {py}) as its only solution?",
            f"x + y = {px + py} and x − y = {px - py}",
            [
                f"x + y = {px} and x − y = {py}",
                f"x + y = {px + py} and x − y = {px + py}",
                f"x + y = {py} and x − y = {px}",
            ],
            f"Check: {px}+{py}={px+py} and {px}−({py})={px-py}. Two independent lines meet once.",
            level=level,
        )
    if style == "setup":
        apple, pumpkin, n = 5, 4, random.choice([10, 12, 13, 15])
        a = random.randint(3, n - 3)
        total = apple * a + pumpkin * (n - a)
        return _mcq(
            _dyn_id(2, "systems"),
            "systems",
            (
                f"Apple pies cost ${apple} and pumpkin pies cost ${pumpkin}. "
                f"You bought {n} pies and spent ${total}. Which system could you use? Do NOT solve."
            ),
            f"x + y = {n} and {apple}x + {pumpkin}y = {total}",
            [
                f"x + y = {total} and {apple}x + {pumpkin}y = {n}",
                f"{apple}x + {pumpkin}y = {n} and x + y = {total}",
                f"x + y = {n} and {apple}x + {pumpkin}y = {n}",
            ],
            f"Count: x+y={n}. Cost: {apple}x+{pumpkin}y={total}.",
            level=level,
        )
    x, y = random.randint(1, 6), random.choice([-4, -3, -2, 1, 2, 3])
    a1, b1 = 2, 5
    c1 = a1 * x + b1 * y
    a2, b2 = 3, -1
    c2 = a2 * x + b2 * y
    correct = f"({x}, {y})"
    distractors = [f"({y}, {x})", f"({x}, {-y})", f"({-x}, {y})", f"({x + 1}, {y})"]
    distractors = [d for d in distractors if d != correct][:3]
    return _mcq(
        _dyn_id(2, "systems"),
        "systems",
        f"Solve: {a1}x + {b1}y = {c1} and {a2}x + {b2}y = {c2}.",
        correct,
        distractors,
        f"Elimination or substitution gives x={x}, y={y}.",
        level=level,
    )


def _dyn_angles(level: str) -> dict:
    style = random.choice(["supp", "comp", "tri", "exterior"])
    if style == "supp":
        x = random.randint(8, 20)
        a, b = 3, 5
        extra = 180 - (a + b) * x
        if extra <= 0:
            extra = 20
            x = (180 - extra) // (a + b)
        return _mcq(
            _dyn_id(3, "angles"),
            "angles",
            f"Supplementary angles ({a}x)° and ({b}x + {extra})°. Find x.",
            str(x),
            [str(x + 2), str(x - 2 if x > 2 else x + 3), str(extra)],
            f"{a}x + {b}x + {extra} = 180 → {(a+b)}x = {180-extra} → x = {x}.",
            level=level,
        )
    if style == "comp":
        x = random.randint(6, 14)
        extra = 90 - 7 * x
        if extra <= 0:
            x = 10
            extra = 20
        return _mcq(
            _dyn_id(3, "angles"),
            "angles",
            f"Complementary angles (2x + {extra})° and (5x)°. Find x.",
            str(x),
            [str(x + 2), str(x - 2 if x > 2 else x + 4), "90"],
            f"2x + {extra} + 5x = 90 → 7x = {90-extra} → x = {x}.",
            level=level,
        )
    if style == "tri":
        x = random.choice([15, 18, 20, 24, 25, 30])
        return _mcq(
            _dyn_id(3, "angles"),
            "angles",
            f"Triangle angles x°, (2x)°, and ({180 - 3*x})°. Find x.",
            str(x),
            [str(x + 5), str(x - 5 if x > 5 else x + 8), str(180 - 3 * x)],
            f"x+2x+{180-3*x}=180 → 3x={3*x} → x={x}.",
            level=level,
        )
    remote, x = random.choice([40, 50, 55, 60]), random.randint(4, 12)
    other = 3 * x + 5
    exterior = remote + other
    return _mcq(
        _dyn_id(3, "angles"),
        "angles",
        (
            f"Remote interiors {remote}° and (3x + 5)°. Exterior angle {exterior}°. "
            f"If 3x + 5 = {other}, what is x?"
        ),
        str(x),
        [str(x + 2), str(x - 1 if x > 1 else x + 3), str(other)],
        f"Exterior-angle theorem: {remote} + 3x + 5 = {exterior} → 3x = {other-5} → x = {x}.",
        level=level,
    )


def _dyn_transformations(level: str) -> dict:
    x, y = random.randint(2, 8), random.randint(2, 8)
    style = random.choice(["reflect_y", "rot180", "rot90", "dilate"])
    if style == "reflect_y":
        return _mcq(
            _dyn_id(3, "transformations"),
            "transformations",
            f"Point ({x}, {y}) reflected over the y-axis lands at:",
            f"({-x}, {y})",
            [f"({x}, {-y})", f"({y}, {x})", f"({-x}, {-y})"],
            "Reflection over y-axis negates x.",
            level=level,
        )
    if style == "rot180":
        return _mcq(
            _dyn_id(3, "transformations"),
            "transformations",
            f"({x}, {y}) → ({-x}, {-y}) is which transformation about the origin?",
            "180° rotation",
            ["90° counterclockwise", "Reflection over x-axis", "Dilation by −1 from the point"],
            "(x, y) → (−x, −y) is 180° about the origin.",
            level=level,
        )
    if style == "rot90":
        return _mcq(
            _dyn_id(3, "transformations"),
            "transformations",
            f"({x}, {y}) → ({-y}, {x}) is which rotation about the origin?",
            "90° counterclockwise",
            ["90° clockwise", "180°", "270° counterclockwise"],
            "90° CCW rule: (x, y) → (−y, x).",
            level=level,
        )
    k = random.choice([2, 3, 4])
    return _mcq(
        _dyn_id(3, "transformations"),
        "transformations",
        f"({x}, {y}) → ({k*x}, {k*y}) is:",
        f"Dilation by {k} about the origin",
        [
            f"Translation {k} units",
            f"Dilation by {k} from ({x}, {y})",
            "90° counterclockwise",
        ],
        f"Both coordinates multiply by {k} → dilation about the origin.",
        level=level,
    )


def _dyn_similarity(level: str) -> dict:
    style = random.choice(["side", "area", "perim"])
    k = random.choice([2, 3, 4, 5])
    side = random.randint(3, 12)
    if style == "area":
        area = random.choice([6, 8, 10, 12])
        return _mcq(
            _dyn_id(3, "similarity"),
            "similarity",
            f"Similar figures, scale factor {k} (small → large). Small area {area}. Large area?",
            str(k * k * area),
            [str(k * area), str(area + k * k), str(k * k)],
            f"Areas scale by k²: {k}² × {area} = {k*k*area}.",
            level=level,
        )
    if style == "perim":
        perim = random.choice([8, 10, 12, 16])
        return _mcq(
            _dyn_id(3, "similarity"),
            "similarity",
            f"Similar figures, scale factor {k}. Small perimeter {perim}. Large perimeter?",
            str(k * perim),
            [str(k * k * perim), str(perim + k), str(perim)],
            f"Perimeters scale by k: {perim} × {k} = {k*perim}.",
            level=level,
        )
    return _mcq(
        _dyn_id(3, "similarity"),
        "similarity",
        f"Similar figures scale factor {k}. Small side {side} cm → large side?",
        f"{k * side} cm",
        [f"{side + k} cm", f"{max(1, side // k)} cm", f"{side} cm"],
        f"Multiply by scale factor: {side} × {k} = {k*side}.",
        level=level,
    )


def _dyn_surface_area(level: str) -> dict:
    if random.random() < 0.5:
        a, b, c = random.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10)])
        length = random.choice([4, 6, 8, 9])
        lat = (a + b + c) * length
        bases = a * b
        total = lat + bases
        return _mcq(
            _dyn_id(3, "surface_area"),
            "surface_area",
            f"A {a}-{b}-{c} right triangular prism has length {length}. Total surface area?",
            f"{total}",
            [f"{lat}", f"{bases}", f"{lat + bases // 2}"],
            f"Lateral ({a}+{b}+{c})×{length}={lat}. Two bases {a}×{b}={bases}. Total {total}.",
            level=level,
        )
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
    style = random.choice(["cube", "cone", "cyl", "prism"])
    if style == "cone":
        r, h = random.choice([3, 6, 9]), random.choice([2, 3, 4, 6])
        coeff = (r * r * h) // 3
        return _mcq(
            _dyn_id(3, "volume"),
            "volume",
            f"Cone radius {r}, height {h}. Volume in terms of π?",
            f"{coeff}π",
            [f"{r*r*h}π", f"{coeff}", f"{(r*r*h)//2}π"],
            f"V=(1/3)πr²h=(1/3)π({r*r})({h})={coeff}π.",
            level=level,
        )
    if style == "cyl":
        r, h = random.choice([3, 4, 5, 6]), random.choice([4, 5, 8, 10])
        return _mcq(
            _dyn_id(3, "volume"),
            "volume",
            f"Cylinder volume {r*r*h}π and radius {r}. Height?",
            str(h),
            [str(r), str(r * r), str(h + 2)],
            f"πr²h={r*r*h}π → {r*r}h={r*r*h} → h={h}.",
            level=level,
        )
    if style == "prism":
        a, b, length = 6, 8, random.choice([3, 4, 5])
        vol = (a * b // 2) * length
        return _mcq(
            _dyn_id(3, "volume"),
            "volume",
            f"Right triangular prism, legs {a} and {b}, length {length}. Volume?",
            f"{vol}",
            [f"{a*b*length}", f"{(a+b)*length}", f"{vol + a}"],
            f"B=({a}×{b})/2={a*b//2}. V=Bh={vol}.",
            level=level,
        )
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
    style = random.choice(["eval", "function", "discrete"])
    if style == "function":
        x = random.randint(2, 6)
        return _mcq(
            _dyn_id(4, "function_basics"),
            "function_basics",
            f"A table lists ({x}, 3), ({x + 1}, 3), and ({x}, 8). Is this a function?",
            f"No — input {x} has two outputs",
            [
                "Yes — outputs can repeat",
                "Yes — there are three pairs",
                "Only if you draw a mapping",
            ],
            f"Input {x} maps to both 3 and 8.",
            level=level,
        )
    if style == "discrete":
        fee, rate = random.choice([10, 20, 25]), random.choice([8, 12, 15])
        return _mcq(
            _dyn_id(4, "function_basics"),
            "function_basics",
            (
                f"Cost is ${fee} plus ${rate} per ticket. The domain (number of tickets) is:"
            ),
            "Discrete — you cannot buy a fraction of a ticket",
            [
                "Continuous — money can be any amount",
                "Discrete — because the fee is fixed",
                "Neither — domain is the total cost",
            ],
            "x is a count of tickets, so only whole numbers make sense.",
            level=level,
        )
    x = random.randint(2, 7)
    ans = 3 * x - 1
    return _mcq(
        _dyn_id(4, "function_basics"),
        "function_basics",
        f"If f(x) = 3x − 1, what is f({x})?",
        str(ans),
        [str(ans + 3), str(3 * x + 1), str(x - 1)],
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
    if random.random() < 0.5:
        fee, rate = random.choice([15, 20, 25]), random.choice([50, 80, 200])
        return _mcq(
            _dyn_id(4, "constructing"),
            "constructing",
            f"${fee} in fees plus ${rate} per ticket. Total cost y for x tickets?",
            f"y = {rate}x + {fee}",
            [f"y = {fee}x + {rate}", f"y = {rate + fee}x", f"y = {rate}x"],
            f"Rate ${rate}/ticket is slope; ${fee} fee is the intercept.",
            level=level,
        )
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
    start = random.choice([12, 20, 40, 100, 220])
    rate = random.choice([-11, -5, 3, 4, 6])
    style = random.choice(["write", "eval", "rate"])
    if style == "write":
        y1, y2 = start, start + rate
        return _mcq(
            _dyn_id(4, "linear_functions"),
            "linear_functions",
            f"At 0 min: {start}. At 1 min: {y1 + rate}. Linear function for y after x minutes?",
            f"y = {rate}x + {start}",
            [f"y = {start}x + {rate}", f"y = {rate}x", f"y = {abs(rate)}x + {start}"],
            f"Rate {y2}-{start}={rate}; start {start} → y={rate}x+{start}.",
            level=level,
        )
    if style == "eval":
        mins = random.choice([3, 4, 5, 6])
        ans = rate * mins + start
        return _mcq(
            _dyn_id(4, "linear_functions"),
            "linear_functions",
            f"Using y = {rate}x + {start}, what is y when x = {mins}?",
            str(ans),
            [str(ans + rate), str(start), str(ans - start if ans != start else ans + 11)],
            f"y = {rate}({mins}) + {start} = {ans}.",
            level=level,
        )
    return _mcq(
        _dyn_id(4, "linear_functions"),
        "linear_functions",
        f"In y = {rate}x + {start}, what does {rate} represent?",
        f"The amount y changes each time x increases by 1",
        [f"The starting value when x = 0", f"The value of y when x = {rate}", "The domain"],
        "Slope is the rate of change.",
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
