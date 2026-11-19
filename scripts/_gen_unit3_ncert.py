"""Build and check the Unit 3 NCERT practice set. One-shot generator."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

OUT = Path("HarshitMath/class10/ncert/unit_03.json")

AR = [
    "Both Assertion and Reason are true, and Reason explains Assertion.",
    "Both Assertion and Reason are true, and Reason does not explain Assertion.",
    "Assertion is true and Reason is false.",
    "Assertion is false and Reason is true.",
]


def solve(eq1: tuple, eq2: tuple) -> tuple[Fraction, Fraction]:
    a, b, c = map(Fraction, eq1)
    d, e, f = map(Fraction, eq2)
    det = a * e - b * d
    if det == 0:
        raise ValueError(f"not a unique system: {eq1} {eq2}")
    x = (c * e - b * f) / det
    y = (a * f - c * d) / det
    return x, y


def kind(eq1: tuple, eq2: tuple) -> str:
    a, b, c = map(Fraction, eq1)
    d, e, f = map(Fraction, eq2)
    det = a * e - b * d
    if det != 0:
        return "unique"
    if a * f - c * d == 0 and b * f - c * e == 0:
        return "infinite"
    return "none"


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def mcq(qid: str, question: str, options: list[str], answer: int, explanation: str) -> dict:
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(qid)
    if not 0 <= answer < 4:
        raise ValueError(qid)
    return {
        "id": qid,
        "marks": 1,
        "type": "mcq",
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
    }


def written(qid: str, marks: int, question: str, steps: list[str], accept: str) -> dict:
    if marks not in (2, 3, 5) or len(steps) < 2:
        raise ValueError(qid)
    if any("=" in step for step in steps):
        raise ValueError(f"equals in {qid}")
    last = steps[-1].rstrip(".")
    if last != accept or len(last) > 90:
        raise ValueError(f"accept mismatch {qid}: {last!r}")
    model = " ".join(step if step.endswith(".") else step + "." for step in steps)
    return {
        "id": qid,
        "marks": marks,
        "type": "written",
        "question": question,
        "model_answer": model,
        "explanation": accept + ".",
        "accept": accept,
    }


def pair(qid: str, marks: int, eq1, eq2, label: str) -> dict:
    x, y = solve(eq1, eq2)
    # Confirm the values satisfy both equations.
    for a, b, c in (eq1, eq2):
        if Fraction(a) * x + Fraction(b) * y != Fraction(c):
            raise ValueError(qid)
    accept = f"{fmt(x)} and {fmt(y)}"
    return written(
        qid,
        marks,
        f"Solve {label}.",
        [
            f"Eliminate one variable from the pair. x is {fmt(x)} and y is {fmt(y)}",
            accept,
        ],
        accept,
    )


questions: list[dict] = []

questions += [
    mcq(
        "ncert_u3_lines_ab",
        "The lines x = a and y = b, with a and b different, are",
        ["intersecting at (a, b)", "intersecting at (b, a)", "parallel", "coincident"],
        0,
        "A vertical line and a horizontal line meet once, at (a, b).",
    ),
    mcq(
        "ncert_u3_two_axis_lines",
        "The pair 2x + 1 = 0 and 3y - 5 = 0 has",
        ["a unique solution", "two solutions", "no solution", "infinitely many solutions"],
        0,
        "Each equation fixes one variable, so the pair meets at one point.",
    ),
    mcq(
        "ncert_u3_which_inconsistent",
        "Which pair is inconsistent?",
        [
            "3x - y = 9 and x + y = 3",
            "4x + 3y = 24 and -2x + 3y = 6",
            "5x - y = 10 and 10x - 2y = 20",
            "-2x + y = 3 and -4x + 2y = 10",
        ],
        3,
        "In the last pair the x and y ratios match, but the constants do not.",
    ),
    mcq(
        "ncert_u3_equal_coeff_ratios",
        "If a1/a2 = b1/b2 for a pair of linear equations, the pair has",
        [
            "a unique solution",
            "no solution",
            "infinitely many solutions",
            "no solution or infinitely many solutions",
        ],
        3,
        "Equal x and y ratios mean the lines are parallel or the same line.",
    ),
    mcq(
        "ncert_u3_ab_parallel",
        "ax + 2y = 9 and 3x + by = 18 are parallel, with a and b integers, when",
        ["a = b", "3a = 2b", "2a = 3b", "ab = 6"],
        3,
        "The x and y ratios match when ab is 6, and that common ratio is not 1/2 for an integer a.",
    ),
    mcq(
        "ncert_u3_k_minus5",
        "The value of k for which 3x - ky = 7 and 6x + 10y = 3 is inconsistent is",
        ["-10", "-5", "5", "7"],
        1,
        "The x ratio is 1/2, so -k/10 is 1/2 and k is -5. The constants do not match.",
    ),
    mcq(
        "ncert_u3_k_four_fifths",
        "The value of k for which 5x + 2y - 7 = 0 and 2x + ky + 1 = 0 has no solution is",
        ["4/5", "-4/5", "5/4", "2"],
        0,
        "5/2 equals 2/k when k is 4/5, and that ratio is not the constant ratio.",
    ),
    mcq(
        "ncert_u3_parallel_second",
        "A line parallel to 3x - 2y = 5 is",
        ["9x + 8y = 7", "-12x - 8y = 7", "-12x + 8y = 7", "12x + 8y = 7"],
        2,
        "-12x + 8y = 7 has the same slope 3/2 and a different intercept.",
    ),
    mcq(
        "ncert_u3_k_minus6",
        "The value of k for which 3x - 7y = 1 and kx + 14y = 6 is inconsistent is",
        ["-6", "-3", "6", "2"],
        0,
        "The y ratio is -1/2, so 3/k is -1/2 and k is -6.",
    ),
    mcq(
        "ncert_u3_solution_a_b",
        "The solution of x + y = a + b and ax - by = a^2 - b^2 is",
        ["x = b, y = a", "x = -a, y = b", "x = a, y = b", "x = a, y = -b"],
        2,
        "x is a and y is b satisfy both equations.",
    ),
    mcq(
        "ncert_u3_32_33",
        "The solution of 32x + 33y = 34 and 33x + 32y = 31 is",
        ["-1 and 2", "-1 and 4", "1 and -2", "-1 and -4"],
        0,
        "Adding gives x + y is 1, and subtracting gives x - y is -3.",
    ),
    mcq(
        "ncert_u3_two_digit_ratio",
        "The ratio of a two-digit number to the sum of its digits is 7 : 1. How many such numbers are there?",
        ["1", "4", "9", "infinitely many"],
        1,
        "The tens digit is twice the units digit, which gives 21, 42, 63 and 84.",
    ),
    mcq(
        "ncert_u3_ar_parallel",
        "Assertion: x + 2y - 4 = 0 and 2x + 4y - 12 = 0 are parallel. Reason: If a1/a2 = b1/b2 and this is not equal to c1/c2, the lines are parallel and the pair has no solution.",
        AR,
        0,
        "Both coefficient ratios are 1/2 and the constant ratio is 1/3, so the reason explains the assertion.",
    ),
    mcq(
        "ncert_u3_ar_not_parallel",
        "Assertion: 2x + y = 6 and 2x - y + 2 = 0 are parallel. Reason: When k = 1, 5x + ky = 4 and 15x + 3y = 12 have infinitely many solutions.",
        AR,
        3,
        "The y coefficients are 1 and -1, so the lines meet. The reason is a true statement about a different pair.",
    ),
    mcq(
        "ncert_u3_ar_intersect",
        "Assertion: 3x + 2y = 12 and 5x - 4y = 10 intersect. Reason: The graphs intersect when a1/a2 is not equal to b1/b2.",
        AR,
        0,
        "3/5 is not equal to 2/(-4), so the reason explains the assertion.",
    ),
    mcq(
        "ncert_u3_ar_k3_false",
        "Assertion: kx - y = 2 and 6x - 2y = 3 have a unique solution when k = 3. Reason: ax + by + c = 0 and dx + ey + f = 0 have a unique solution when a/d is not equal to b/e.",
        AR,
        3,
        "k = 3 makes the coefficient ratios equal and the constants unequal, so there is no solution. The reason is true.",
    ),
    mcq(
        "ncert_u3_ar_infinite",
        "Assertion: 9x + 3y + 12 = 0 and 18x + 6y + 24 = 0 have infinitely many solutions. Reason: The pair has infinitely many solutions when a1/a2 = b1/b2 = c1/c2.",
        AR,
        0,
        "Every ratio is 1/2, so the reason explains the assertion.",
    ),
    mcq(
        "ncert_u3_zero_solutions",
        "The number of solutions of x + 2y + 5 = 0 and -3x - 6y + 1 = 0 is",
        ["0", "1", "2", "infinitely many"],
        0,
        "The coefficient ratios are both -1/3, but the constants are not in that ratio.",
    ),
    mcq(
        "ncert_u3_class_intersect",
        "The lines 5x - 4y + 8 = 0 and 7x + 6y - 9 = 0",
        ["intersect at one point", "are parallel", "are coincident", "cannot be compared"],
        0,
        "5/7 is not equal to -4/6, so there is one intersection.",
    ),
    mcq(
        "ncert_u3_class_parallel",
        "The lines 6x - 3y + 10 = 0 and 2x - y + 9 = 0",
        ["intersect at one point", "are parallel", "are coincident", "cannot be compared"],
        1,
        "Both coefficient ratios are 3, and 10/9 is not 3.",
    ),
    mcq(
        "ncert_u3_class_coincident",
        "The lines 9x + 3y + 12 = 0 and 18x + 6y + 24 = 0",
        ["intersect at one point", "are parallel", "are coincident", "cannot be compared"],
        2,
        "The second equation is twice the first.",
    ),
    mcq(
        "ncert_u3_x_minus_y",
        "If 2x + y = 13 and 4x - y = 17, then x - y is",
        ["2", "3", "5", "8"],
        0,
        "Adding gives x is 5 and y is 3, so x - y is 2.",
    ),
    mcq(
        "ncert_u3_a3_b1",
        "If x = a and y = b solve x - y = 2 and x + y = 4, then a and b are",
        ["3 and 1", "2 and 4", "4 and 2", "1 and 3"],
        0,
        "Adding gives 2a is 6, so a is 3 and b is 1.",
    ),
    mcq(
        "ncert_u3_lambda_1",
        "5x + λy = 4 and 15x + 3y = 12 have infinitely many solutions when λ is",
        ["1", "3", "4", "5"],
        0,
        "All three ratios equal 1/3 when λ is 1.",
    ),
    mcq(
        "ncert_u3_k_is_2",
        "3x + y = 3 and 6x + ky = 8 have no solution when k is",
        ["1", "2", "3", "4"],
        1,
        "The x ratio is 1/2, so k is 2, and 3/8 is not 1/2.",
    ),
    mcq(
        "ncert_u3_chairs_algebra",
        "3 chairs and 4 tables cost Rs 900. 5 chairs and 3 tables cost Rs 2100. If a chair costs Rs x and a table costs Rs y, the equations are",
        [
            "3x + 4y = 900 and 5x + 3y = 2100",
            "3x + y = 900 and 5x + 3y = 2100",
            "4x + 3y = 900 and 3x + 5y = 2100",
            "3x + 4y = 2100 and 5x + 3y = 900",
        ],
        0,
        "The chair count multiplies x and the table count multiplies y.",
    ),
    mcq(
        "ncert_u3_fare_120",
        "A taxi has a fixed charge of Rs 20 and then Rs 10 per km. The fare for 10 km is",
        ["Rs 100", "Rs 120", "Rs 200", "Rs 220"],
        1,
        "20 plus 10 times 10 is 120.",
    ),
    mcq(
        "ncert_u3_paths_parallel",
        "The paths 7x - 5y = 3 and 21x - 15y = 5",
        ["cross once", "do not cross", "are the same path", "cross twice"],
        1,
        "Both coefficient ratios are 1/3, and 3/5 is not 1/3.",
    ),
    mcq(
        "ncert_u3_k_infinite_7",
        "2x + 3y = 7 and (k - 1)x + (k + 2)y = 3k have infinitely many solutions when k is",
        ["5", "6", "7", "8"],
        2,
        "The three ratios are equal only when k is 7.",
    ),
    mcq(
        "ncert_u3_p_parallel",
        "-x + py = 1 and px - y = 1 represent parallel lines when p is",
        ["-1", "0", "1", "2"],
        2,
        "p is 1 makes the coefficient ratios equal to -1, which is not the constant ratio. p is -1 makes the lines the same.",
    ),
    mcq(
        "ncert_u3_parallel_to_5_8",
        "Which line is parallel to 5x + 8y = 20?",
        ["10x + 16y = 40", "10x + 16y = 1", "x + y = 1", "5x - 8y = 20"],
        1,
        "10x + 16y = 40 is the same line. 10x + 16y = 1 has the same slope and a different intercept.",
    ),
]

# Unique pairs. Each is checked by substitution.
PAIRS = [
    ("ncert_u3_xy_4_1", 2, (2, 1, 9), (1, -2, 2), "2x + y = 9 and x - 2y = 2"),
    ("ncert_u3_xy_3_4", 2, (1, -1, -1), (2, 1, 10), "x - y = -1 and 2x + y = 10"),
    ("ncert_u3_xy_2_2", 2, (1, 2, 6), (3, -2, 2), "x + 2y = 6 and 3x - 2y = 2"),
    ("ncert_u3_xy_2_3", 2, (1, -1, -1), (3, 2, 12), "x - y + 1 = 0 and 3x + 2y - 12 = 0"),
    ("ncert_u3_xy_3_4b", 2, (4, -1, 8), (2, -3, -6), "4x - y - 8 = 0 and 2x - 3y + 6 = 0"),
    ("ncert_u3_xy_0_0", 2, (2, -1, 0), (1, 1, 0), "2x - y = 0 and x + y = 0"),
    ("ncert_u3_xy_5_3", 2, (1, 1, 8), (2, -3, 1), "x + y = 8 and 2x - 3y = 1"),
    ("ncert_u3_xy_28_12", 2, (1, 1, 8), (2, -3, 4), "x + y = 8 and 2x - 3y = 4"),
    ("ncert_u3_xy_2_m1", 2, (3, -4, 10), (1, 1, 1), "3x - 4y = 10 and x + y = 1"),
    ("ncert_u3_xy_4_18", 2, (3, -1, -6), (2, -4, -20), "y = 3x + 6 and 2y - 4x = 20"),
    ("ncert_u3_xy_2_3b", 2, (2, 3, 13), (4, 5, 23), "0.2x + 0.3y = 1.3 and 0.4x + 0.5y = 2.3"),
    ("ncert_u3_xy_m3_7", 2, (8, 5, 11), (1, 1, 4), "8x + 5y = 11 and x + y = 4"),
    ("ncert_u3_xy_4_1b", 2, (1, -1, 3), (3, -2, 10), "x - y = 3 and 3x - 2y = 10"),
    ("ncert_u3_xy_2_1", 3, (62, 43, 167), (43, 62, 148), "62x + 43y = 167 and 43x + 62y = 148"),
    ("ncert_u3_xy_1_2", 3, (117, 231, 579), (231, 117, 465), "117x + 231y = 579 and 231x + 117y = 465"),
    ("ncert_u3_xy_3_m1", 3, (23, -29, 98), (29, -23, 110), "23x - 29y = 98 and 29x - 23y = 110"),
    ("ncert_u3_xy_19_6", 3, (1, 1, 5), (2, -3, 4), "x + y = 5 and 2x - 3y = 4"),
    ("ncert_u3_xy_2_1c", 2, (3, 4, 10), (1, -1, 1), "3x + 4y = 10 and x - y = 1"),
    ("ncert_u3_xy_9_m5", 3, (3, -5, 4), (9, -2, 7), "3x - 5y = 4 and 9x - 2y = 7"),
    ("ncert_u3_xy_2_m3", 2, (1, 4, -6), (1, -1, 3), "x/2 + 2y/3 = -1 and x - y/3 = 3"),
    ("ncert_u3_xy_2_3c", 2, (4, 3, 17), (7, -2, 8), "0.4x + 0.3y = 1.7 and 0.7x - 0.2y = 0.8"),
    ("ncert_u3_xy_18_m1", 2, (1, -2, 20), (1, 1, 17), "x - 2y = 20 and x + y = 17"),
    ("ncert_u3_xy_3_m5", 2, (3, 1, 4), (5, 2, 5), "3x + y = 4 and 5x + 2y = 5"),
    ("ncert_u3_xy_1_1", 3, (7, -2, 5), (8, 7, 15), "7x - 2y = 5 and 8x + 7y = 15"),
    ("ncert_u3_xy_1_m4", 2, (1, -2, 3), (3, -3, 5), "x - 2y = 3 and 3x - 3y = 5"),
]

# Fix the 2y-4x equation: y = 3x+6 means  -3x + y = 6, and 2y - 4x = 20 means -4x + 2y = 20.
# I encoded (3, -1, -6) which is 3x - y = -6, i.e. y = 3x+6. Good.
# Second (2, -4, -20) is 2x - 4y = -20, NOT 2y-4x=20.
# 2y - 4x = 20 is -4x + 2y = 20. Coefficients (-4, 2, 20).
PAIRS[9] = ("ncert_u3_xy_4_18", 2, (-3, 1, 6), (-4, 2, 20), "y = 3x + 6 and 2y - 4x = 20")

# 3x-4y=10 and x+y=1 was a rewrite of 3x-4y=10 and 2x+2y=2. Good.
# x/2 + 2y/3 = -1 multiplied by 6 is 3x+4y=-6. I used (1, 4, -6) which is x+4y=-6. WRONG.
PAIRS[19] = ("ncert_u3_xy_2_m3", 2, (3, 4, -6), (3, -1, 9), "x/2 + 2y/3 = -1 and x - y/3 = 3")
# Second x - y/3 = 3 multiplied by 3 is 3x - y = 9. Good.

# 0.2x+0.3y=1.3 -> 2x+3y=13, 0.4x+0.5y=2.3 -> 4x+5y=23. I used that. Good.
# 0.1x-0.2y=2 -> x-2y=20. I used that. Good.
# 0.4x+0.3y=1.7 -> 4x+3y=17. I used that. Good.

for qid, marks, eq1, eq2, label in PAIRS:
    questions.append(pair(qid, marks, eq1, eq2, label))

# Classifications and single-parameter answers.
questions += [
    written(
        "ncert_u3_no_10_30",
        2,
        "How many solutions do 3x + 2y = 10 and 12x + 8y = 30 have?",
        [
            "The second equation has x and y coefficients four times the first, but 40 is not 30",
            "The pair has no solution",
        ],
        "The pair has no solution",
    ),
    written(
        "ncert_u3_infinite_same",
        2,
        "How many solutions do 3x - y = 3 and 9x - 3y = 9 have?",
        [
            "The second equation is three times the first",
            "The pair has infinitely many solutions",
        ],
        "The pair has infinitely many solutions",
    ),
    written(
        "ncert_u3_inconsistent_3_5",
        2,
        "Are 3x - 5y = 11 and 6x - 10y = 7 consistent?",
        [
            "Both coefficient ratios are 1/2, but 11/7 is not 1/2",
            "No, the pair is inconsistent",
        ],
        "No, the pair is inconsistent",
    ),
    written(
        "ncert_u3_coincident_6_3",
        2,
        "Are 6x - 3y = 12 and 2x - y = 4 coincident?",
        [
            "The first equation is three times the second",
            "Yes, the lines are coincident",
        ],
        "Yes, the lines are coincident",
    ),
    written(
        "ncert_u3_k_not_unique_6",
        2,
        "For which k do kx + 2y = 5 and 3x + y = 1 not have a unique solution?",
        [
            "The coefficient ratios are equal when k/3 is 2",
            "k is 6",
        ],
        "k is 6",
    ),
    written(
        "ncert_u3_k_none_12",
        2,
        "Find k so that 4x + 5y = 17 and kx + 15y = 33 has no solution.",
        [
            "The y ratio is 1/3, so 4/k is 1/3, and the constant ratio is not 1/3",
            "k is 12",
        ],
        "k is 12",
    ),
    written(
        "ncert_u3_k_none_2",
        2,
        "Find k so that 2x + ky = 8 and x + y = 6 has no solution.",
        [
            "The x ratio is 2, so k is 2, and 8/6 is not 2",
            "k is 2",
        ],
        "k is 2",
    ),
    written(
        "ncert_u3_k_none_pm4",
        3,
        "Find the values of k for which kx + 2y = 5 and 8x + ky = 20 has no solution.",
        [
            "The coefficient ratios match when k squared is 16",
            "For both 4 and -4, the constant ratio is different",
            "k is 4 or -4",
        ],
        "k is 4 or -4",
    ),
    written(
        "ncert_u3_k_none_pair_2",
        2,
        "Find k so that 3x + y = 4 and (2k - 1)x + (k - 1)y = 2k + 1 has no solution.",
        [
            "3/(2k - 1) equals 1/(k - 1) when k is 2, and the constants are not in that ratio",
            "k is 2",
        ],
        "k is 2",
    ),
    written(
        "ncert_u3_k_infinite_m10",
        2,
        "Find k so that 3x - y - 5 = 0 and 6x - 2y + k = 0 has infinitely many solutions.",
        [
            "The x and y ratios are already equal to 1/2, so the constant ratio -5/k must be 1/2",
            "k is -10",
        ],
        "k is -10",
    ),
    written(
        "ncert_u3_k_infinite_10",
        2,
        "Find k so that 4x + 7y = 10 and (k + 2)x + 21y = 3k has infinitely many solutions.",
        [
            "7/21 is 1/3, so 4/(k + 2) and 10/(3k) are both 1/3",
            "k is 10",
        ],
        "k is 10",
    ),
    written(
        "ncert_u3_k_infinite_4",
        2,
        "Find k so that x + 2y + 7 = 0 and 2x + ky + 14 = 0 has infinitely many solutions.",
        [
            "1/2, 2/k and 7/14 are equal when k is 4",
            "k is 4",
        ],
        "k is 4",
    ),
    written(
        "ncert_u3_k_infinite_5",
        2,
        "Find k so that 2x + (k - 2)y = k and 6x + (2k - 1)y = 2k + 5 has infinitely many solutions.",
        [
            "The x ratio is 1/3, so k - 2 over 2k - 1 is 1/3 and k over 2k + 5 is 1/3",
            "k is 5",
        ],
        "k is 5",
    ),
    written(
        "ncert_u3_k_infinite_4b",
        3,
        "Find k so that 2x + 3y = 2 and (k + 2)x + (2k + 1)y = 2(k - 1) has infinitely many solutions.",
        [
            "2/(k + 2), 3/(2k + 1) and 1/(k - 1) are equal when k is 4",
            "k is 4",
        ],
        "k is 4",
    ),
    written(
        "ncert_u3_k_infinite_2c",
        3,
        "Find k so that x + (k + 1)y = 5 and (k + 1)x + 9y = 8k - 1 has infinitely many solutions.",
        [
            "(k + 1) squared is 9, and only k is 2 also matches the constant ratio 1/3",
            "k is 2",
        ],
        "k is 2",
    ),
    written(
        "ncert_u3_pq_17_11",
        3,
        "Find p and q so that (2p - 1)x + 3y = 5 and 3x + (q - 1)y = 2 has infinitely many solutions.",
        [
            "Every ratio must equal 5/2",
            "p is 17/4 and q is 11/5",
        ],
        "p is 17/4 and q is 11/5",
    ),
    written(
        "ncert_u3_pq_5_1",
        2,
        "Find p and q so that 2x + 3y = 7 and (p + q)x + (2p - q)y = 21 has infinitely many solutions.",
        [
            "The constant ratio is 1/3, so p + q is 6 and 2p - q is 9",
            "p is 5 and q is 1",
        ],
        "p is 5 and q is 1",
    ),
    written(
        "ncert_u3_k_parallel_m6",
        2,
        "Find k so that kx + 3y = 3 and 12x + ky = 6 are parallel.",
        [
            "k/12 equals 3/k when k is 6 or -6. k is 6 makes the lines the same",
            "k is -6",
        ],
        "k is -6",
    ),
    written(
        "ncert_u3_k_three_cases",
        3,
        "For x + 2y = 3 and 5x + ky + 7 = 0, find k for intersecting lines, for parallel lines, and say whether the lines can be coincident.",
        [
            "The lines meet whenever 1/5 is not equal to 2/k, that is whenever k is not 10",
            "They are parallel when k is 10, because the constant ratio is not 1/5",
            "They are never coincident, and they are parallel when k is 10",
        ],
        "They are never coincident, and they are parallel when k is 10",
    ),
]

# Word and geometry results, each checked below.
questions += [
    written(
        "ncert_u3_boys_girls",
        2,
        "10 students took part in a quiz. The number of girls is 4 more than the number of boys. How many boys and how many girls took part?",
        [
            "Let the numbers be b and g. Then b + g is 10 and g is b + 4",
            "2b + 4 is 10",
            "3 boys and 7 girls",
        ],
        "3 boys and 7 girls",
    ),
    written(
        "ncert_u3_pencil_pen",
        3,
        "5 pencils and 7 pens cost Rs 50. 7 pencils and 5 pens cost Rs 46. Find the cost of one pencil and one pen.",
        [
            "5p + 7n is 50 and 7p + 5n is 46",
            "Clearing one variable gives 24p is 72",
            "A pencil costs Rs 3 and a pen costs Rs 5",
        ],
        "A pencil costs Rs 3 and a pen costs Rs 5",
    ),
    written(
        "ncert_u3_chair_table_small",
        3,
        "4 chairs and 3 tables cost Rs 210. 5 chairs and 2 tables cost Rs 175. Find the cost of one chair and one table.",
        [
            "4c + 3t is 210 and 5c + 2t is 175",
            "Clearing t gives 7c is 105",
            "A chair costs Rs 15 and a table costs Rs 50",
        ],
        "A chair costs Rs 15 and a table costs Rs 50",
    ),
    written(
        "ncert_u3_pen_box",
        3,
        "4 pens and 4 pencil boxes cost Rs 100. Three times the cost of a pen is Rs 15 more than the cost of a pencil box. Find each cost.",
        [
            "The first statement gives one pen plus one box is Rs 25",
            "Three times the pen is the box plus 15",
            "A pen costs Rs 10 and a pencil box costs Rs 15",
        ],
        "A pen costs Rs 10 and a pencil box costs Rs 15",
    ),
    written(
        "ncert_u3_salim_age",
        3,
        "Two years ago Salim was thrice as old as his daughter. Six years later he will be 4 years older than twice her age. How old are they now?",
        [
            "Let their present ages be s and d. Then s - 2 is 3(d - 2), and s + 6 is 2(d + 6) + 4",
            "Subtracting the two equations gives the daughter's age",
            "Salim is 38 years old and his daughter is 14",
        ],
        "Salim is 38 years old and his daughter is 14",
    ),
    written(
        "ncert_u3_ratio_numbers",
        3,
        "Two numbers are in the ratio 5 : 6. If 8 is subtracted from each, the ratio becomes 4 : 5. Find the numbers.",
        [
            "Let the numbers be 5k and 6k. Then 5(5k - 8) is 4(6k - 8)",
            "k is 8",
            "The numbers are 40 and 48",
        ],
        "The numbers are 40 and 48",
    ),
    written(
        "ncert_u3_fraction_5_12",
        3,
        "A fraction becomes 1/3 when 1 is subtracted from the numerator. It becomes 1/4 when 8 is added to the denominator. Find the fraction.",
        [
            "Let the fraction be n/d. Then n - 1 over d is 1/3, and n over d + 8 is 1/4",
            "The two equations give n is 5 and d is 12",
            "The fraction is 5/12",
        ],
        "The fraction is 5/12",
    ),
    written(
        "ncert_u3_digits_48",
        3,
        "The sum of the digits of a two-digit number is 12. Seven times the number equals four times the number formed by reversing the digits. Find the number.",
        [
            "Let the tens digit be t and the units digit be u. Then t + u is 12 and 7(10t + u) is 4(10u + t)",
            "The second equation simplifies to u is 2t",
            "The number is 48",
        ],
        "The number is 48",
    ),
    written(
        "ncert_u3_digits_63",
        3,
        "The sum of a two-digit number and the number formed by reversing its digits is 99. The tens digit is 3 more than the units digit. Find the number.",
        [
            "The sum of a number and its reverse is 11 times the sum of the digits, so the digits add to 9",
            "The tens digit is the units digit plus 3",
            "The number is 63",
        ],
        "The number is 63",
    ),
    written(
        "ncert_u3_amit_baljeet",
        3,
        "Five years ago Amit was thrice as old as Baljeet. Ten years from now Amit will be twice as old as Baljeet. Find their present ages.",
        [
            "Let the present ages be a and b. Then a - 5 is 3(b - 5), and a + 10 is 2(b + 10)",
            "Subtracting gives Baljeet's present age",
            "Amit is 50 and Baljeet is 20",
        ],
        "Amit is 50 and Baljeet is 20",
    ),
    written(
        "ncert_u3_notes_6_8",
        3,
        "Sheena withdraws Rs 1000 in Rs 100 and Rs 50 notes only, and receives 14 notes. How many notes of each kind does she receive?",
        [
            "Let the counts be h and f. Then h + f is 14 and 100h + 50f is 1000",
            "Dividing the money equation by 50 gives 2h + f is 20",
            "6 notes of Rs 100 and 8 notes of Rs 50",
        ],
        "6 notes of Rs 100 and 8 notes of Rs 50",
    ),
    written(
        "ncert_u3_rectangle_40_30",
        5,
        "The area of a rectangle falls by 80 square units if the length is reduced by 5 and the breadth is increased by 2. The area rises by 50 square units if the length is increased by 10 and the breadth is reduced by 5. Find the length and the breadth.",
        [
            "The two changes give 2L - 5B is -70 and -5L + 10B is 100",
            "The second equation says L is 2B - 20. Substituting gives B is 30",
            "The length is 40 and the breadth is 30",
        ],
        "The length is 40 and the breadth is 30",
    ),
    written(
        "ncert_u3_chairs_5650",
        3,
        "Two chairs and three tables cost Rs 5650. Three chairs and two tables cost Rs 7100. Find the cost of one chair and one table.",
        [
            "2c + 3t is 5650 and 3c + 2t is 7100",
            "Clearing t gives 5c is 10000",
            "A chair costs Rs 2000 and a table costs Rs 550",
        ],
        "A chair costs Rs 2000 and a table costs Rs 550",
    ),
    written(
        "ncert_u3_sum_diff",
        2,
        "The sum of two numbers is 105 and their difference is 45. Find the numbers.",
        [
            "Adding the two statements gives twice the larger number",
            "The numbers are 75 and 30",
        ],
        "The numbers are 75 and 30",
    ),
    written(
        "ncert_u3_ajay_marriage",
        3,
        "At marriage Ajay was 5 years older than his wife. Sixteen years later their ages are in the ratio 9 : 8. Find their ages at the time of marriage.",
        [
            "Let the present ages be 9k and 8k. The difference is still 5, so k is 5",
            "Subtract 16 from each present age",
            "Ajay was 29 and his wife was 24",
        ],
        "Ajay was 29 and his wife was 24",
    ),
    written(
        "ncert_u3_father_45",
        3,
        "A father's age is 3 times the sum of the ages of his two children. After 5 years his age will be twice the sum of their ages. Find the father's present age.",
        [
            "Let the children's ages add to s. Then the father is 3s, and 3s + 5 is 2(s + 10)",
            "s is 15",
            "The father is 45 years old",
        ],
        "The father is 45 years old",
    ),
    written(
        "ncert_u3_halls_100_80",
        3,
        "Sending 10 students from hall A to hall B makes the halls equal. Sending 20 students from B to A makes A double B. How many students are in the halls now?",
        [
            "A - 10 is B + 10, and A + 20 is 2(B - 20)",
            "The first equation says A is B + 20. Substituting gives B is 80",
            "Hall A has 100 students and hall B has 80",
        ],
        "Hall A has 100 students and hall B has 80",
    ),
    written(
        "ncert_u3_almonds",
        5,
        "2 kg of almonds and 3 kg of raisins cost Rs 1400. 3 kg of almonds and 5 kg of raisins cost Rs 2150. Find the cost of 1 kg of each, and the cost of 1.5 kg of almonds with 2.5 kg of raisins.",
        [
            "2a + 3r is 1400 and 3a + 5r is 2150. Clearing a gives r is 100 and a is 550",
            "Almonds cost Rs 550 per kg and raisins cost Rs 100 per kg. The mix of 1.5 kg and 2.5 kg costs Rs 1075",
            "550, 100 and 1075",
        ],
        "550, 100 and 1075",
    ),
    written(
        "ncert_u3_coaching_fees",
        5,
        "Batch I has 20 poor children and 5 rich children and collects Rs 9000. Batch II has 5 poor children and 25 rich children and collects Rs 26000. Find the monthly fee for a poor child and for a rich child, the difference, and the collection from a batch of 10 poor and 20 rich children.",
        [
            "20p + 5r is 9000 and 5p + 25r is 26000. Dividing gives 4p + r is 1800 and p + 5r is 5200",
            "A poor child pays Rs 200 and a rich child pays Rs 1000, so the difference is Rs 800. The new batch collects Rs 22000",
            "200, 1000, 800 and 22000",
        ],
        "200, 1000, 800 and 22000",
    ),
    written(
        "ncert_u3_taxi_5_10",
        3,
        "A taxi fare is a fixed charge plus a charge per km. A 10 km ride costs Rs 105 and a 15 km ride costs Rs 155. Find the fixed charge and the charge per km.",
        [
            "Let the fixed charge be f and the rate be r. Then f + 10r is 105 and f + 15r is 155",
            "Subtracting gives 5r is 50",
            "The fixed charge is Rs 5 and the charge per km is Rs 10",
        ],
        "The fixed charge is Rs 5 and the charge per km is Rs 10",
    ),
    written(
        "ncert_u3_popcorn",
        2,
        "Two packets of popcorn and one mango drink cost Rs 330. One packet of popcorn and two mango drinks cost Rs 300. Find the cost of one packet of popcorn.",
        [
            "2p + m is 330 and p + 2m is 300",
            "Clearing m gives 3p is 360",
            "One packet of popcorn costs Rs 120",
        ],
        "One packet of popcorn costs Rs 120",
    ),
    written(
        "ncert_u3_simran_ticket",
        3,
        "Simran spends Rs 600 on a ticket and food. The food costs one-third of the ticket. Find the cost of the ticket and the cost of the food.",
        [
            "Let the ticket cost t. Then the food is t/3 and t + t/3 is 600",
            "4t/3 is 600",
            "The ticket costs Rs 450 and the food costs Rs 150",
        ],
        "The ticket costs Rs 450 and the food costs Rs 150",
    ),
    written(
        "ncert_u3_passcode_94",
        3,
        "A two-digit locker code satisfies two clues. Subtracting twice the ones digit from the tens digit leaves 1. Three more than the tens digit is thrice the ones digit. Find the code.",
        [
            "Let the digits be t and u. Then t - 2u is 1 and t + 3 is 3u",
            "Substituting t is 3u - 3 gives u is 4",
            "The code is 94",
        ],
        "The code is 94",
    ),
    written(
        "ncert_u3_cars_100_80",
        5,
        "Places A and B are 180 km apart. Two cars start at the same time, one from each place. Travelling in the same direction they meet after 9 hours. Travelling towards each other they meet after 1 hour. Find their speeds.",
        [
            "If the speeds are x and y, with x greater than y, then x - y is 20 and x + y is 180",
            "Adding gives twice the faster speed",
            "The speeds are 100 km/h and 80 km/h",
        ],
        "The speeds are 100 km/h and 80 km/h",
    ),
    written(
        "ncert_u3_nidhi",
        5,
        "Nidhi receives Rs 1200 interest in one year from Rs x at 6% per annum and Rs y at 5% per annum. If instead x earned 3% and y earned 8%, the interest would be Rs 1260. Find x and y.",
        [
            "6x + 5y is 120000 and 3x + 8y is 126000, in rupees after clearing the percentages",
            "Doubling the second equation and subtracting the first gives y",
            "x is 10000 and y is 12000",
        ],
        "x is 10000 and y is 12000",
    ),
    written(
        "ncert_u3_marbles",
        5,
        "Ananya's red, blue and yellow marbles are in the ratio 4 : 5 : 3. She gives Neha all the red marbles and some blue ones, 20 marbles in all. The blue and yellow marbles left with Ananya are in the ratio 7 : 9. How many red marbles did she give?",
        [
            "Let the original counts be 4k, 5k and 3k. She gives away 4k red marbles and 20 - 4k blue marbles",
            "Blue left over yellow left is (9k - 20) over 3k, and that ratio is 7/9",
            "She gave 12 red marbles",
        ],
        "She gave 12 red marbles",
    ),
    written(
        "ncert_u3_lines_pq",
        5,
        "The lines are 5x + 3y = 2p, 35x + 21y = pq and 100x + 4qy = 240. Find q so that the first two lines coincide for a nonzero p, and say whether that second line is parallel to the third.",
        [
            "The first two lines have coefficient ratio 1/7, so 2/q is 1/7",
            "With q at that value, the second and third lines have slopes that are not equal",
            "q is 14, and the second line is not parallel to the third",
        ],
        "q is 14, and the second line is not parallel to the third",
    ),
    written(
        "ncert_u3_m_minus5",
        3,
        "Solve 2x - 3y = 13 and 7x - 2y = 20. Hence find m if y = mx + 7.",
        [
            "Clearing y gives x is 2 and y is -3",
            "-3 is 2m + 7",
            "x is 2, y is -3 and m is -5",
        ],
        "x is 2, y is -3 and m is -5",
    ),
    written(
        "ncert_u3_m_minus1",
        3,
        "Solve 5x + 4y = 10 and 3x - 2y + 16 = 0. Hence find m if y = mx + 3.",
        [
            "The second equation is 3x - 2y is -16. Clearing y gives x is -2 and y is 5",
            "5 is -2m + 3",
            "x is -2, y is 5 and m is -1",
        ],
        "x is -2, y is 5 and m is -1",
    ),
    written(
        "ncert_u3_p_zero",
        3,
        "Solve x + 2y = 6 and 2x + y = 6. Hence find p if y = px + 2.",
        [
            "Clearing one variable gives x is 2 and y is 2",
            "2 is 2p + 2",
            "x is 2, y is 2 and p is 0",
        ],
        "x is 2, y is 2 and p is 0",
    ),
    written(
        "ncert_u3_vertices_x_axis",
        3,
        "The lines x - y = -1 and 2x + y = 10 meet the x-axis and each other. Find the vertices of the triangle.",
        [
            "The lines meet at (3, 4). On the x-axis, y is 0, so the intercepts are (-1, 0) and (5, 0)",
            "The vertices are (-1, 0), (5, 0) and (3, 4)",
        ],
        "The vertices are (-1, 0), (5, 0) and (3, 4)",
    ),
    written(
        "ncert_u3_vertices_y_axis",
        3,
        "The lines x + 2y = 6 and 3x - 2y = 2 meet the y-axis and each other. Find the vertices of the triangle.",
        [
            "The lines meet at (2, 2). On the y-axis, x is 0, so the intercepts are (0, 3) and (0, -1)",
            "The vertices are (2, 2), (0, 3) and (0, -1)",
        ],
        "The vertices are (2, 2), (0, 3) and (0, -1)",
    ),
    written(
        "ncert_u3_vertices_y_axis_2",
        3,
        "The lines x - y + 1 = 0 and 3x + 2y - 12 = 0 meet the y-axis and each other. Find the vertices of the triangle.",
        [
            "The lines meet at (2, 3). Their y-intercepts are (0, 1) and (0, 6)",
            "The vertices are (0, 1), (0, 6) and (2, 3)",
        ],
        "The vertices are (0, 1), (0, 6) and (2, 3)",
    ),
    written(
        "ncert_u3_consistent_yes",
        2,
        "Is 4x + y = 8 and 4x - 2y = 16 consistent? Does x = 3 and y = -3 satisfy both equations?",
        [
            "The x coefficients match and the y coefficients do not, so there is one solution and the pair is consistent",
            "3 + (-3) is not a check of the first equation: 4 times 3 plus -3 is 9, not 8",
            "Yes, the pair is consistent, but x is 3 and y is -3 do not satisfy it",
        ],
        "Yes, the pair is consistent, but x is 3 and y is -3 do not satisfy it",
    ),
    written(
        "ncert_u3_paths_14",
        2,
        "Do the paths 7x - 5y = 3 and 14x - 10y = 5 cross?",
        [
            "Both coefficient ratios are 1/2, and 3/5 is not 1/2",
            "No, the paths do not cross",
        ],
        "No, the paths do not cross",
    ),
    written(
        "ncert_u3_k_greater_none",
        3,
        "For k greater than 1, how many solutions do (k - 1)x + y = k + 1 and (k^2 - 1)x + (k + 1)y = 1 - k^2 have?",
        [
            "The second x coefficient is (k - 1)(k + 1), so the x ratio is 1/(k + 1)",
            "The y ratio is also 1/(k + 1), but the constant ratio is not, when k is greater than 1",
            "The pair has no solution",
        ],
        "The pair has no solution",
    ),
]


def audit() -> None:
    # Re-solve every generated pair and the parameter conditions.
    seen = [item[0] for item in PAIRS]
    if len(seen) != len(set(seen)):
        raise SystemExit("duplicate pair id")
    by_id = {q["id"]: q for q in questions}
    if len(by_id) != len(questions):
        raise SystemExit("duplicate question id")

    checks = {
        "ncert_u3_which_inconsistent": kind((-2, 1, 3), (-4, 2, 10)) == "none",
        "ncert_u3_k_minus5": kind((3, 5, 7), (6, 10, 3)) == "none",
        "ncert_u3_k_four_fifths": kind((5, 2, 7), (2, Fraction(4, 5), -1)) == "none",
        "ncert_u3_k_minus6": kind((3, -7, 1), (-6, 14, 6)) == "none",
        "ncert_u3_32_33": solve((32, 33, 34), (33, 32, 31)) == (Fraction(-1), Fraction(2)),
        "ncert_u3_zero_solutions": kind((1, 2, -5), (-3, -6, -1)) == "none",
        "ncert_u3_class_intersect": kind((5, -4, -8), (7, 6, 9)) == "unique",
        "ncert_u3_class_parallel": kind((6, -3, -10), (2, -1, -9)) == "none",
        "ncert_u3_class_coincident": kind((9, 3, -12), (18, 6, -24)) == "infinite",
        "ncert_u3_x_minus_y": solve((2, 1, 13), (4, -1, 17)) == (Fraction(5), Fraction(3)),
        "ncert_u3_a3_b1": solve((1, -1, 2), (1, 1, 4)) == (Fraction(3), Fraction(1)),
        "ncert_u3_lambda_1": kind((5, 1, 4), (15, 3, 12)) == "infinite",
        "ncert_u3_k_is_2": kind((3, 1, 3), (6, 2, 8)) == "none",
        "ncert_u3_k_infinite_7": kind((2, 3, 7), (6, 9, 21)) == "infinite",
        "ncert_u3_p_parallel": kind((-1, 1, 1), (1, -1, 1)) == "none",
        "ncert_u3_no_10_30": kind((3, 2, 10), (12, 8, 30)) == "none",
        "ncert_u3_infinite_same": kind((3, -1, 3), (9, -3, 9)) == "infinite",
        "ncert_u3_inconsistent_3_5": kind((3, -5, 11), (6, -10, 7)) == "none",
        "ncert_u3_coincident_6_3": kind((6, -3, 12), (2, -1, 4)) == "infinite",
        "ncert_u3_k_not_unique_6": kind((6, 2, 5), (3, 1, 1)) == "none",
        "ncert_u3_k_none_12": kind((4, 5, 17), (12, 15, 33)) == "none",
        "ncert_u3_k_none_2": kind((2, 2, 8), (1, 1, 6)) == "none",
        "ncert_u3_k_none_pm4": kind((4, 2, 5), (8, 4, 20)) == "none" and kind((-4, 2, 5), (8, -4, 20)) == "none",
        "ncert_u3_k_none_pair_2": kind((3, 1, 4), (3, 1, 5)) == "none",
        "ncert_u3_k_infinite_m10": kind((3, -1, 5), (6, -2, 10)) == "infinite",
        "ncert_u3_k_infinite_10": kind((4, 7, 10), (12, 21, 30)) == "infinite",
        "ncert_u3_k_infinite_4": kind((1, 2, -7), (2, 4, -14)) == "infinite",
        "ncert_u3_k_infinite_5": kind((2, 3, 5), (6, 9, 15)) == "infinite",
        "ncert_u3_k_infinite_4b": kind((2, 3, 2), (6, 9, 6)) == "infinite",
        "ncert_u3_k_infinite_2c": kind((1, 3, 5), (3, 9, 15)) == "infinite",
        "ncert_u3_pq_17_11": kind((Fraction(17, 2) - 1, 3, 5), (3, Fraction(11, 5) - 1, 2)) == "infinite",
        "ncert_u3_pq_5_1": kind((2, 3, 7), (6, 9, 21)) == "infinite",
        "ncert_u3_k_parallel_m6": kind((-6, 3, 3), (12, -6, 6)) == "none" and kind((6, 3, 3), (12, 6, 6)) == "infinite",
        "ncert_u3_boys_girls": solve((1, 1, 10), (-1, 1, 4)) == (Fraction(3), Fraction(7)),
        "ncert_u3_pencil_pen": solve((5, 7, 50), (7, 5, 46)) == (Fraction(3), Fraction(5)),
        "ncert_u3_chair_table_small": solve((4, 3, 210), (5, 2, 175)) == (Fraction(15), Fraction(50)),
        "ncert_u3_pen_box": solve((1, 1, 25), (3, -1, 15)) == (Fraction(10), Fraction(15)),
        "ncert_u3_salim_age": solve((1, -3, -4), (1, -2, 10)) == (Fraction(38), Fraction(14)),
        "ncert_u3_fraction_5_12": solve((3, -1, 3), (4, -1, 8)) == (Fraction(5), Fraction(12)),
        "ncert_u3_amit_baljeet": solve((1, -3, -10), (1, -2, 10)) == (Fraction(50), Fraction(20)),
        "ncert_u3_notes_6_8": solve((1, 1, 14), (2, 1, 20)) == (Fraction(6), Fraction(8)),
        "ncert_u3_rectangle_40_30": solve((2, -5, -70), (-1, 2, 20)) == (Fraction(40), Fraction(30)),
        "ncert_u3_chairs_5650": solve((2, 3, 5650), (3, 2, 7100)) == (Fraction(2000), Fraction(550)),
        "ncert_u3_sum_diff": solve((1, 1, 105), (1, -1, 45)) == (Fraction(75), Fraction(30)),
        "ncert_u3_halls_100_80": solve((1, -1, 20), (1, -2, -60)) == (Fraction(100), Fraction(80)),
        "ncert_u3_almonds": solve((2, 3, 1400), (3, 5, 2150)) == (Fraction(550), Fraction(100)),
        "ncert_u3_coaching_fees": solve((4, 1, 1800), (1, 5, 5200)) == (Fraction(200), Fraction(1000)),
        "ncert_u3_taxi_5_10": solve((1, 10, 105), (1, 15, 155)) == (Fraction(5), Fraction(10)),
        "ncert_u3_popcorn": solve((2, 1, 330), (1, 2, 300)) == (Fraction(120), Fraction(90)),
        "ncert_u3_simran_ticket": solve((1, 1, 600), (1, -3, 0)) == (Fraction(450), Fraction(150)),
        "ncert_u3_cars_100_80": solve((1, -1, 20), (1, 1, 180)) == (Fraction(100), Fraction(80)),
        "ncert_u3_nidhi": solve((6, 5, 120000), (3, 8, 126000)) == (Fraction(10000), Fraction(12000)),
        "ncert_u3_m_minus5": solve((2, -3, 13), (7, -2, 20)) == (Fraction(2), Fraction(-3)),
        "ncert_u3_m_minus1": solve((5, 4, 10), (3, -2, -16)) == (Fraction(-2), Fraction(5)),
        "ncert_u3_p_zero": solve((1, 2, 6), (2, 1, 6)) == (Fraction(2), Fraction(2)),
        "ncert_u3_paths_14": kind((7, -5, 3), (14, -10, 5)) == "none",
        "ncert_u3_paths_parallel": kind((7, -5, 3), (21, -15, 5)) == "none",
    }
    # k = -5 was encoded as 3x + 5y = 7 because -k y with k=-5 is +5y. Original is 3x - ky = 7.
    # I checked kind((3, 5, 7), (6, -10, 3)). Original second is 6x + 10y = 3, and -k = 5 so the
    # y coefficient in the first equation is -(-5) = +5. Yes 3x + 5y = 7. Good.
    # Vertices and the k = 10 case.
    if solve((1, -1, -1), (2, 1, 10)) != (Fraction(3), Fraction(4)):
        raise SystemExit("vertices x-axis")
    if solve((1, 2, 6), (3, -2, 2)) != (Fraction(2), Fraction(2)):
        raise SystemExit("vertices y-axis")
    if solve((1, -1, -1), (3, 2, 12)) != (Fraction(2), Fraction(3)):
        raise SystemExit("vertices y-axis 2")
    if kind((1, 2, 3), (5, 10, -7)) != "none":
        raise SystemExit("k 10 parallel")
    if kind((1, 2, 3), (5, 4, -7)) != "unique":
        raise SystemExit("k not 10")
    if solve((4, 1, 8), (4, -2, 16)) != (Fraction(8, 3), Fraction(-8, 3)):
        raise SystemExit("consistent pair")
    raw = json.loads(OUT.read_text(encoding="utf-8")) if OUT.is_file() else None
    if raw:
        saved = {q["id"]: q for q in raw["questions"]}
        for qid, _marks, eq1, eq2, _label in PAIRS:
            x, y = solve(eq1, eq2)
            expect = f"{fmt(x)} and {fmt(y)}"
            if saved[qid]["accept"] != expect:
                raise SystemExit(f"json drift {qid}")
    failed = [key for key, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(f"audit failed: {failed}")
    missing = [key for key in checks if key not in by_id]
    if missing:
        raise SystemExit(f"missing ids: {missing}")

    # Spot-check a few word results that are not 2-by-2 in the table.
    if 5 * 8 != 40 or 6 * 8 != 48:
        raise SystemExit("ratio numbers")
    number = 48
    if sum(int(d) for d in "48") != 12 or 7 * number != 4 * 84:
        raise SystemExit("digits 48")
    if 63 + 36 != 99 or 6 != 3 + 3:
        raise SystemExit("digits 63")
    if Fraction(9) / 3 != 3 or (9 * 5 - 16) - (8 * 5 - 16) != 5:
        raise SystemExit("ajay")
    if 3 * 15 != 45 or 45 + 5 != 2 * (15 + 10):
        raise SystemExit("father")
    red, blue, yellow = 12, 15, 9
    if Fraction(blue - 8, yellow) != Fraction(7, 9) or red + 8 != 20:
        raise SystemExit("marbles")
    if 9 - 2 * 4 != 1 or 9 + 3 != 3 * 4:
        raise SystemExit("passcode")
    # q = 14: first two lines coincide for p != 0, and second is not parallel to third.
    if kind((5, 3, 2), (35, 21, 14)) != "infinite":
        raise SystemExit("lines coincide")
    if kind((35, 21, 14), (100, 56, 240)) == "none" and (35 * 56 - 21 * 100) == 0:
        raise SystemExit("unexpected parallel")
    if 35 * 56 - 21 * 100 == 0:
        raise SystemExit("slopes matched")
    # 1.5*550 + 2.5*100
    if Fraction(3, 2) * 550 + Fraction(5, 2) * 100 != 1075:
        raise SystemExit("almond mix")
    if 10 * 200 + 20 * 1000 != 22000 or 1000 - 200 != 800:
        raise SystemExit("coaching extra")
    # k > 1 sample
    if kind((2, 1, 4), (8, 4, -8)) != "none":
        raise SystemExit("k>1")
    # y = mx + 7 with x=2, y=-3
    if -3 != -5 * 2 + 7 or 5 != -1 * -2 + 3 or 2 != 0 * 2 + 2:
        raise SystemExit("parameter m")
    # ab = 6 parallel samples
    for a, b in ((1, 6), (2, 3), (3, 2), (6, 1), (-2, -3)):
        if kind((a, 2, 9), (3, b, 18)) != "none":
            raise SystemExit(f"ab parallel {a},{b}")
    # two-digit count
    found = [10 * a + b for b in range(0, 10) for a in range(1, 10) if a == 2 * b and (10 * a + b) * 1 == 7 * (a + b)]
    if found != [21, 42, 63, 84]:
        raise SystemExit(found)
    # solution x=a, y=b
    if solve((1, 1, 5 + 2), (5, -2, 25 - 4)) != (Fraction(5), Fraction(2)):
        raise SystemExit("symbolic a b")
    # slopes
    def slope(aa, bb):
        return Fraction(-aa, bb)

    if slope(-12, 8) != slope(3, -2):
        raise SystemExit("parallel slope")
    if slope(10, 16) != slope(5, 8):
        raise SystemExit("5 8 slope")
    if kind((10, 16, 1), (5, 8, 20)) != "none":
        raise SystemExit("parallel 10 16")
    if kind((10, 16, 40), (5, 8, 20)) != "infinite":
        raise SystemExit("same line")
    return len(checks), len(questions)


def main() -> None:
    checked, total = audit()
    print("audited", checked, "conditions;", "questions", total)
    marks: dict[int, int] = {}
    for question in questions:
        marks[question["marks"]] = marks.get(question["marks"], 0) + 1
    payload = {
        "meta": {
            "unit_id": 3,
            "chapter": "Pair of Linear Equations in Two Variables",
            "source": "NCERT Chapter 3 exercises and All in One practice items that can be solved without a figure",
        },
        "questions": questions,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT, marks)


if __name__ == "__main__":
    main()
