"""Mental math muscle-memory drills for weekly plan warm-ups."""

from __future__ import annotations

import random
from math import gcd, lcm

MENTAL_MATH_PER_SESSION = 5
MENTAL_MATH_COUNT_MAX = 15

DRILL_GROUPS: dict[str, list[str]] = {
    "Powers & Roots": ["squares", "cubes", "square_roots", "powers_of_ten"],
    "Core Arithmetic": [
        "mult_facts",
        "integer_ops",
        "order_of_ops",
        "distributive_trick",
    ],
    "Fractions & Percents": ["frac_decimal", "frac_ops", "percent_snap", "gcf_lcm"],
    "Algebra Patterns": ["special_products", "unit_rates", "slope_snap"],
    "Geometry": ["pythagorean_triples", "angle_pairs"],
}

DRILLS: dict[str, dict] = {
    "squares": {
        "name": "Perfect Squares (n²)",
        "emoji": "⬜",
        "short": "Squares",
        "levels": {
            "A": "2–10 (must-know)",
            "B": "11–15 (stretch)",
            "C": "16–20 (challenge)",
        },
    },
    "cubes": {
        "name": "Perfect Cubes (n³)",
        "emoji": "🧊",
        "short": "Cubes",
        "levels": {
            "A": "2–6 (must-know)",
            "B": "7–10 (stretch)",
        },
    },
    "square_roots": {
        "name": "Square Roots (√)",
        "emoji": "√",
        "short": "Square Roots",
        "levels": {
            "A": "Perfect squares ≤ 100",
            "B": "Perfect squares 121–225",
        },
    },
    "mult_facts": {
        "name": "Multiplication Facts",
        "emoji": "✖️",
        "short": "Times Tables",
        "levels": {
            "A": "6–9 × single digit",
            "B": "10–12 × single digit",
            "C": "Double-digit × single digit",
        },
    },
    "frac_decimal": {
        "name": "Fraction ↔ Decimal Snap",
        "emoji": "🍕",
        "short": "Frac/Decimal",
        "levels": {
            "A": "Halves & quarters",
            "B": "Thirds & fifths",
            "C": "Sixths & eighths",
        },
    },
    "percent_snap": {
        "name": "Percent Benchmarks",
        "emoji": "💯",
        "short": "Percents",
        "levels": {
            "A": "10% and 50%",
            "B": "25% and 75%",
            "C": "20% and 15%",
        },
    },
    "integer_ops": {
        "name": "Integer Quick Rules",
        "emoji": "➕➖",
        "short": "Integers",
        "levels": {
            "A": "Add/subtract positives & negatives",
            "B": "Multiply & divide signed numbers",
        },
    },
    "powers_of_ten": {
        "name": "Powers of 10",
        "emoji": "🔟",
        "short": "Powers of 10",
        "levels": {
            "A": "10² through 10⁴",
            "B": "10⁵ and 10⁶",
        },
    },
    "distributive_trick": {
        "name": "Distributive Shortcuts",
        "emoji": "🔀",
        "short": "Distributive",
        "levels": {
            "A": "× 9, 11, or numbers near 10/100",
            "B": "× 98, 102, 995-style tricks",
        },
    },
    "pythagorean_triples": {
        "name": "Pythagorean Triples",
        "emoji": "📐",
        "short": "Pythagorean",
        "levels": {
            "A": "Classic 3-4-5 family",
            "B": "5-12-13 and 8-15-17",
            "C": "Find a missing leg",
        },
    },
    "angle_pairs": {
        "name": "Complementary & Supplementary Angles",
        "emoji": "📏",
        "short": "Angle Pairs",
        "levels": {
            "A": "Complementary (sum to 90°)",
            "B": "Supplementary (sum to 180°)",
            "C": "Mixed angle-finding",
        },
    },
    "slope_snap": {
        "name": "Slope from Rise/Run",
        "emoji": "📈",
        "short": "Slope",
        "levels": {
            "A": "Positive rise/run",
            "B": "From two coordinate points",
            "C": "Negative slopes",
        },
    },
    "unit_rates": {
        "name": "Unit Rates",
        "emoji": "🏷️",
        "short": "Unit Rates",
        "levels": {
            "A": "Price per item, simple rates",
            "B": "Speed and word-problem rates",
        },
    },
    "order_of_ops": {
        "name": "Order of Operations",
        "emoji": "🔢",
        "short": "Order of Ops",
        "levels": {
            "A": "Multiply before add/subtract",
            "B": "Parentheses first",
            "C": "With exponents",
        },
    },
    "frac_ops": {
        "name": "Fraction Operations",
        "emoji": "➗",
        "short": "Fraction Ops",
        "levels": {
            "A": "Add/subtract same denominator",
            "B": "Multiply & divide simple fractions",
            "C": "Unlike denominators (small LCD)",
        },
    },
    "gcf_lcm": {
        "name": "GCF, LCM & LCD",
        "emoji": "🔗",
        "short": "GCF/LCM",
        "levels": {
            "A": "Greatest common factor",
            "B": "Least common multiple",
            "C": "LCD for adding fractions",
        },
    },
    "special_products": {
        "name": "Special Products",
        "emoji": "✨",
        "short": "Special Products",
        "levels": {
            "A": "(a + b)² mental expand",
            "B": "(a − b)² mental expand",
            "C": "Difference of squares a² − b²",
        },
    },
}


def _make_options(correct: int, spread: int | None = None) -> tuple[list[int], int]:
    if spread is None:
        spread = max(3, abs(correct) // 4) if correct else 5
    options = {correct}
    attempts = 0
    while len(options) < 4 and attempts < 50:
        offset = random.randint(1, max(1, spread))
        sign = random.choice([-1, 1])
        distractor = correct + sign * offset
        if distractor != correct and distractor not in options:
            options.add(distractor)
        attempts += 1
    while len(options) < 4:
        options.add(correct + len(options) * 2)
    opts = list(options)
    random.shuffle(opts)
    return opts, opts.index(correct)


def _mcq(
    question: str,
    correct: int,
    drill_id: str,
    level: str,
    explanation: str,
    *,
    spread: int | None = None,
) -> dict:
    options, answer = _make_options(correct, spread)
    return {
        "id": f"mm_{drill_id}_{level}_{random.randint(1000, 9999)}",
        "drill": drill_id,
        "level": level,
        "question": question,
        "options": [str(o) for o in options],
        "answer": answer,
        "explanation": explanation,
        "category": f"mm_{drill_id}_{level}",
        "category_label": format_drill_level_label(drill_id, level),
        "source": "mental_math",
    }


def _mcq_str(
    question: str,
    correct: str,
    drill_id: str,
    level: str,
    explanation: str,
    *,
    wrong: list[str] | None = None,
) -> dict:
    pool = list(dict.fromkeys([correct] + (wrong or [])))
    while len(pool) < 4:
        pool.append(f"{correct}?")
    opts = random.sample(pool, 4) if len(pool) > 4 else pool[:4]
    if correct not in opts:
        opts[0] = correct
        random.shuffle(opts)
    return {
        "id": f"mm_{drill_id}_{level}_{random.randint(1000, 9999)}",
        "drill": drill_id,
        "level": level,
        "question": question,
        "options": opts,
        "answer": opts.index(correct),
        "explanation": explanation,
        "category": f"mm_{drill_id}_{level}",
        "category_label": format_drill_level_label(drill_id, level),
        "source": "mental_math",
    }


def get_mental_math_count(config: dict) -> int:
    """How many mental-math questions to prepend (0 if no drills enabled)."""
    if not config.get("mental_math"):
        return 0
    raw = config.get("mental_math_count", MENTAL_MATH_PER_SESSION)
    try:
        n = int(raw)
    except (TypeError, ValueError):
        n = MENTAL_MATH_PER_SESSION
    return max(0, min(MENTAL_MATH_COUNT_MAX, n))


def format_drill_level_label(drill_id: str, level: str) -> str:
    info = DRILLS[drill_id]
    return f"⚡ {info['short']} — Level {level} ({info['levels'][level]})"


def format_mental_math_summary(config: dict) -> list[str]:
    lines: list[str] = []
    for item in config.get("mental_math", []):
        did = str(item.get("id", ""))
        if did not in DRILLS:
            continue
        for lvl in item.get("levels", []):
            if lvl in DRILLS[did]["levels"]:
                lines.append(format_drill_level_label(did, lvl))
    return lines


def _range_for_squares(level: str) -> tuple[int, int]:
    if level == "A":
        return 2, 10
    if level == "B":
        return 11, 15
    return 16, 20


def _range_for_cubes(level: str) -> tuple[int, int]:
    return (2, 6) if level == "A" else (7, 10)


def _gen_squares(level: str) -> dict:
    lo, hi = _range_for_squares(level)
    n = random.randint(lo, hi)
    correct = n * n
    return _mcq(
        f"What is {n}²?",
        correct,
        "squares",
        level,
        f"{n} × {n} = {correct}.",
    )


def _gen_cubes(level: str) -> dict:
    lo, hi = _range_for_cubes(level)
    n = random.randint(lo, hi)
    correct = n ** 3
    return _mcq(
        f"What is {n}³?",
        correct,
        "cubes",
        level,
        f"{n} × {n} × {n} = {correct}.",
        spread=max(10, correct // 4),
    )


def _gen_square_roots(level: str) -> dict:
    if level == "A":
        roots = list(range(2, 11))
    else:
        roots = list(range(11, 16))
    r = random.choice(roots)
    n = r * r
    return _mcq(
        f"What is the square root of {n}?",
        r,
        "square_roots",
        level,
        f"√{n} = {r} because {r}² = {n}.",
        spread=3,
    )


def _gen_mult_facts(level: str) -> dict:
    if level == "A":
        a, b = random.randint(6, 9), random.randint(2, 9)
    elif level == "B":
        a, b = random.randint(10, 12), random.randint(2, 9)
    else:
        a = random.randint(12, 25)
        b = random.randint(3, 9)
    correct = a * b
    return _mcq(
        f"What is {a} × {b}?",
        correct,
        "mult_facts",
        level,
        f"{a} × {b} = {correct}.",
        spread=max(8, correct // 5),
    )


_FRAC_DECIMAL = {
    "A": [(1, 2), (1, 4), (3, 4), (2, 4)],
    "B": [(1, 3), (2, 3), (1, 5), (2, 5), (3, 5), (4, 5)],
    "C": [(1, 6), (5, 6), (1, 8), (3, 8), (5, 8), (7, 8)],
}


def _gen_frac_decimal(level: str) -> dict:
    num, den = random.choice(_FRAC_DECIMAL[level])
    if random.choice([True, False]):
        dec = num / den
        if dec == int(dec):
            correct_str = str(int(dec))
        else:
            correct_str = f"{dec:.2f}".rstrip("0").rstrip(".")
        q = f"What is {num}/{den} as a decimal?"
        pool = ["0.25", "0.5", "0.75", "0.2", "0.4", "0.6", "0.8", "0.125", "0.375", "0.625", "0.875", "0.333", "0.667"]
        opts = list(dict.fromkeys([correct_str] + [p for p in pool if p != correct_str]))
        random.shuffle(opts)
        opts = opts[:4]
        if correct_str not in opts:
            opts[0] = correct_str
            random.shuffle(opts)
        return {
            "id": f"mm_frac_decimal_{level}_{random.randint(1000, 9999)}",
            "drill": "frac_decimal",
            "level": level,
            "question": q,
            "options": opts,
            "answer": opts.index(correct_str),
            "explanation": f"{num}/{den} = {correct_str}.",
            "category": f"mm_frac_decimal_{level}",
            "category_label": format_drill_level_label("frac_decimal", level),
            "source": "mental_math",
        }
    dec = num / den
    dec_str = str(int(dec)) if dec == int(dec) else f"{dec:.2f}".rstrip("0").rstrip(".")
    q = f"Which fraction equals {dec_str}?"
    wrong_fracs = []
    for n, d in _FRAC_DECIMAL["A"] + _FRAC_DECIMAL["B"] + _FRAC_DECIMAL["C"]:
        if (n, d) != (num, den):
            wrong_fracs.append(f"{n}/{d}")
    opts = [f"{num}/{den}"] + random.sample(wrong_fracs, min(3, len(wrong_fracs)))
    random.shuffle(opts)
    return {
        "id": f"mm_frac_decimal_{level}_{random.randint(1000, 9999)}",
        "drill": "frac_decimal",
        "level": level,
        "question": q,
        "options": opts,
        "answer": opts.index(f"{num}/{den}"),
        "explanation": f"{dec_str} = {num}/{den}.",
        "category": f"mm_frac_decimal_{level}",
        "category_label": format_drill_level_label("frac_decimal", level),
        "source": "mental_math",
    }


def _gen_percent_snap(level: str) -> dict:
    if level == "A":
        pcts = [10, 50]
    elif level == "B":
        pcts = [25, 75]
    else:
        pcts = [20, 15]
    pct = random.choice(pcts)
    base = random.choice([40, 60, 80, 100, 120, 160, 200, 240, 300, 400])
    correct = int(base * pct / 100)
    return _mcq(
        f"What is {pct}% of {base}?",
        correct,
        "percent_snap",
        level,
        f"{pct}% of {base} = {correct}.",
        spread=max(5, correct // 3),
    )


def _gen_integer_ops(level: str) -> dict:
    if level == "A":
        templates = [
            lambda: (random.randint(5, 20), random.randint(5, 15), "+"),
            lambda: (random.randint(10, 30), random.randint(5, 20), "-"),
            lambda: (-random.randint(5, 15), random.randint(1, 10), "+"),
            lambda: (random.randint(5, 20), -random.randint(5, 15), "+"),
        ]
        a, b, op = random.choice(templates)()
        correct = a + b if op == "+" else a - b
        q = f"What is {a} {'+' if op == '+' else '−'} {abs(b) if b < 0 and op == '+' else b}?"
        if b < 0 and op == "+":
            q = f"What is {a} + ({b})?"
        elif b < 0 and op == "-":
            q = f"What is {a} − ({abs(b)})?"
    else:
        if random.random() < 0.5:
            a = random.choice([-1, 1]) * random.randint(2, 12)
            b = random.choice([-1, 1]) * random.randint(2, 9)
            correct = a * b
            q = f"What is ({a}) × ({b})?"
        else:
            b = random.choice([-1, 1]) * random.randint(2, 9)
            correct = random.randint(3, 12)
            a = b * correct
            q = f"What is ({a}) ÷ ({b})?"
    return _mcq(
        q,
        correct,
        "integer_ops",
        level,
        f"Work the signs carefully → {correct}.",
        spread=max(5, abs(correct) // 3),
    )


def _gen_powers_of_ten(level: str) -> dict:
    exp = random.randint(2, 4) if level == "A" else random.randint(5, 6)
    correct = 10 ** exp
    return _mcq(
        f"What is 10 to the power of {exp}?",
        correct,
        "powers_of_ten",
        level,
        f"10^{exp} = {'1' + '0' * exp}.",
        spread=max(50, correct // 5),
    )


def _gen_distributive_trick(level: str) -> dict:
    if level == "A":
        a = random.randint(3, 9)
        near = random.choice([9, 11])
        base = 10 if near in (9, 11) else 100
        offset = base - near if near < base else near - base
        sign = -1 if near < base else 1
        num = near
        correct = a * num
        if sign == -1:
            q = f"Use a shortcut: {a} × {num}  (think: {a}×{base} − {a}×{offset})"
            expl = f"{a}×{base} − {a}×{offset} = {correct}."
        else:
            q = f"Use a shortcut: {a} × {num}  (think: {a}×{base} + {a}×{offset})"
            expl = f"{a}×{base} + {a}×{offset} = {correct}."
    else:
        a = random.randint(4, 9)
        base = random.choice([100, 1000])
        offset = random.randint(2, 5)
        num = base - offset
        correct = a * num
        q = f"Use a shortcut: {a} × {num}  (think: {a}×{base} − {a}×{offset})"
        expl = f"{a}×{base} − {a}×{offset} = {correct}."
    return _mcq(q, correct, "distributive_trick", level, expl, spread=max(5, correct // 5))


_PYTH_TRIPLES_A = [(3, 4, 5), (6, 8, 10), (9, 12, 15)]
_PYTH_TRIPLES_B = [(5, 12, 13), (8, 15, 17), (7, 24, 25)]


def _gen_pythagorean_triples(level: str) -> dict:
    if level == "A":
        a, b, c = random.choice(_PYTH_TRIPLES_A)
        q = f"A right triangle has legs {a} and {b}. What is the hypotenuse?"
        return _mcq(q, c, "pythagorean_triples", level, f"{a}² + {b}² = {c}² → hypotenuse = {c}.")
    if level == "B":
        a, b, c = random.choice(_PYTH_TRIPLES_B)
        q = f"A right triangle has legs {a} and {b}. What is the hypotenuse?"
        return _mcq(q, c, "pythagorean_triples", level, f"{a}² + {b}² = {c}² → hypotenuse = {c}.")
    a, b, c = random.choice(_PYTH_TRIPLES_A + _PYTH_TRIPLES_B)
    if random.choice([True, False]):
        q = f"A right triangle has hypotenuse {c} and one leg {a}. What is the other leg?"
        return _mcq(q, b, "pythagorean_triples", level, f"{c}² − {a}² = {b}² → other leg = {b}.")
    q = f"A right triangle has hypotenuse {c} and one leg {b}. What is the other leg?"
    return _mcq(q, a, "pythagorean_triples", level, f"{c}² − {b}² = {a}² → other leg = {a}.")


def _gen_angle_pairs(level: str) -> dict:
    if level == "A":
        known = random.randint(10, 80)
        correct = 90 - known
        q = f"Two angles are complementary. One angle is {known}°. What is the other?"
        expl = f"Complementary angles sum to 90° → 90 − {known} = {correct}°."
    elif level == "B":
        known = random.randint(20, 160)
        correct = 180 - known
        q = f"Two angles are supplementary. One angle is {known}°. What is the other?"
        expl = f"Supplementary angles sum to 180° → 180 − {known} = {correct}°."
    else:
        if random.random() < 0.5:
            known = random.randint(15, 75)
            correct = 90 - known
            q = f"One angle in a pair is {known}°. The pair adds to 90°. Find the missing angle."
            expl = f"90 − {known} = {correct}°."
        else:
            known = random.randint(30, 150)
            correct = 180 - known
            q = f"One angle in a pair is {known}°. The pair adds to 180°. Find the missing angle."
            expl = f"180 − {known} = {correct}°."
    return _mcq(q, correct, "angle_pairs", level, expl, spread=5)


def _gen_slope_snap(level: str) -> dict:
    if level == "A":
        rise, run = random.choice([(1, 2), (2, 3), (3, 4), (2, 5), (4, 1), (3, 2)])
        correct = f"{rise}/{run}" if run != 1 else str(rise)
        q = f"On a graph, a line goes up {rise} and right {run}. What is the slope?"
        wrong = [f"{run}/{rise}", f"{rise + 1}/{run}", f"{rise}/{run + 1}", str(rise + run)]
    elif level == "B":
        x2, y2 = random.randint(2, 8), random.randint(2, 8)
        x1, y1 = 0, 0
        g = gcd(y2, x2) if x2 else 1
        num, den = y2 // g, x2 // g
        correct = f"{num}/{den}" if den != 1 else str(num)
        q = f"What is the slope of the line through (0, 0) and ({x2}, {y2})?"
        wrong = [f"{den}/{num}", f"{num + 1}/{den}", f"{num}/{den + 1}", str(num + den)]
    else:
        rise, run = random.choice([(-2, 3), (-3, 4), (-1, 2), (-4, 5)])
        correct = f"{rise}/{run}"
        q = f"A line goes down {abs(rise)} and right {run}. What is the slope?"
        wrong = [f"{abs(rise)}/{run}", f"{run}/{rise}", f"{rise - 1}/{run}", str(rise + run)]
    return _mcq_str(
        q, correct, "slope_snap", level, f"Slope = rise ÷ run = {correct}.", wrong=wrong
    )


def _gen_unit_rates(level: str) -> dict:
    if level == "A":
        items = random.randint(2, 8)
        total = items * random.randint(2, 12)
        correct = total // items
        templates = [
            f"${total} for {items} items — what is the cost per item?",
            f"{total} miles in {items} hours — how many miles per hour?",
            f"{total} pages read in {items} days — pages per day?",
        ]
        q = random.choice(templates)
        expl = f"{total} ÷ {items} = {correct} per unit."
    else:
        hours = random.choice([2, 3, 4, 5])
        mph = random.randint(8, 15)
        miles = hours * mph
        q = f"A car travels {miles} miles in {hours} hours. What is its average speed in mph?"
        correct = mph
        expl = f"{miles} ÷ {hours} = {mph} mph."
    return _mcq(q, correct, "unit_rates", level, expl, spread=max(3, correct // 3))


def _gen_order_of_ops(level: str) -> dict:
    if level == "A":
        a, b, c = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
        correct = a + b * c
        q = f"What is {a} + {b} × {c}?"
        expl = f"Multiply first: {b} × {c} = {b * c}, then add {a} → {correct}."
    elif level == "B":
        a, b, c = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
        correct = (a + b) * c
        q = f"What is ({a} + {b}) × {c}?"
        expl = f"Parentheses first: {a} + {b} = {a + b}, then × {c} → {correct}."
    else:
        a, b, c = random.randint(2, 5), random.randint(2, 4), random.randint(2, 3)
        correct = a + b ** 2 * c
        q = f"What is {a} + {b}² × {c}?"
        expl = f"Exponent first ({b}² = {b ** 2}), then × {c}, then + {a} → {correct}."
    return _mcq(q, correct, "order_of_ops", level, expl, spread=max(4, correct // 4))


def _gen_frac_ops(level: str) -> dict:
    if level == "A":
        den = random.choice([4, 5, 6, 8, 10])
        n1, n2 = random.randint(1, den - 2), random.randint(1, den - 2)
        if random.choice([True, False]):
            num = n1 + n2
            op = "+"
        else:
            num = abs(n1 - n2)
            op = "−"
        if num == 0:
            num = n1 + n2
            op = "+"
        correct = f"{num}/{den}"
        q = f"What is {n1}/{den} {op} {n2}/{den}?"
        wrong = [f"{num + 1}/{den}", f"{max(1, num - 1)}/{den}", f"{num}/{den + 1}", f"{n1 + n2}/{den * 2}"]
    elif level == "B":
        if random.random() < 0.5:
            n1, d1 = random.randint(1, 5), random.randint(2, 6)
            n2, d2 = random.randint(1, 5), random.randint(2, 6)
            num, den = n1 * n2, d1 * d2
            g = gcd(num, den)
            num, den = num // g, den // g
            correct = f"{num}/{den}" if den != 1 else str(num)
            q = f"What is {n1}/{d1} × {n2}/{d2}?"
            wrong = [f"{n1 + n2}/{d1 + d2}", f"{n1}/{d1 * d2}", f"{n1 * n2}/{d1}", f"{num + 1}/{den}"]
        else:
            n1, d1 = random.randint(2, 8), random.randint(2, 6)
            n2 = random.randint(2, 5)
            correct = f"{n1}/{d1 * n2}"
            q = f"What is {n1}/{d1} ÷ {n2}?"
            wrong = [f"{n1}/{d1 + n2}", f"{n1 * n2}/{d1}", f"{n1 + n2}/{d1}", f"{n1}/{d1 * n2 + 1}"]
    else:
        pairs = [((1, 2), (1, 3), (5, 6)), ((1, 4), (1, 3), (7, 12)), ((2, 3), (1, 6), (5, 6))]
        (n1, d1), (n2, d2), (rn, rd) = random.choice(pairs)
        correct = f"{rn}/{rd}"
        q = f"What is {n1}/{d1} + {n2}/{d2}?"
        wrong = [f"{n1 + n2}/{d1 + d2}", f"{rn}/{rd + 1}", f"{rn + 1}/{rd}", f"{n1 + n2}/{max(d1, d2)}"]
    return _mcq_str(q, correct, "frac_ops", level, f"Answer: {correct}.", wrong=wrong)


def _gen_gcf_lcm(level: str) -> dict:
    pairs = [(12, 18), (8, 12), (15, 25), (16, 24), (9, 12), (18, 24), (10, 15), (4, 6)]
    a, b = random.choice(pairs)
    if level == "A":
        correct = gcd(a, b)
        q = f"What is the GCF (greatest common factor) of {a} and {b}?"
        expl = f"GCF of {a} and {b} is {correct}."
    elif level == "B":
        correct = lcm(a, b)
        q = f"What is the LCM (least common multiple) of {a} and {b}?"
        expl = f"LCM of {a} and {b} is {correct}."
    else:
        correct = lcm(a, b)
        q = f"What is the LCD (least common denominator) for fractions with denominators {a} and {b}?"
        expl = f"LCD = LCM({a}, {b}) = {correct}."
    return _mcq(q, correct, "gcf_lcm", level, expl, spread=max(3, correct // 2))


def _gen_special_products(level: str) -> dict:
    if level == "A":
        a, b = random.randint(2, 9), random.randint(1, 6)
        correct = (a + b) ** 2
        q = f"Use mental math: what is ({a} + {b})² ?"
        expl = f"({a} + {b})² = {a}² + 2·{a}·{b} + {b}² = {correct}."
    elif level == "B":
        b = random.randint(1, 4)
        a = random.randint(b + 2, 12)
        correct = (a - b) ** 2
        q = f"Use mental math: what is ({a} − {b})² ?"
        expl = f"({a} − {b})² = {correct}."
    else:
        a, b = random.randint(4, 12), random.randint(1, 4)
        correct = a ** 2 - b ** 2
        q = f"Use mental math: what is {a}² − {b}² ?"
        expl = f"{a}² − {b}² = ({a} + {b})({a} − {b}) = {correct}."
    return _mcq(q, correct, "special_products", level, expl, spread=max(5, correct // 5))


GENERATOR_MAP: dict[str, dict[str, callable]] = {
    "squares": {"A": _gen_squares, "B": _gen_squares, "C": _gen_squares},
    "cubes": {"A": _gen_cubes, "B": _gen_cubes},
    "square_roots": {"A": _gen_square_roots, "B": _gen_square_roots},
    "mult_facts": {"A": _gen_mult_facts, "B": _gen_mult_facts, "C": _gen_mult_facts},
    "frac_decimal": {"A": _gen_frac_decimal, "B": _gen_frac_decimal, "C": _gen_frac_decimal},
    "percent_snap": {"A": _gen_percent_snap, "B": _gen_percent_snap, "C": _gen_percent_snap},
    "integer_ops": {"A": _gen_integer_ops, "B": _gen_integer_ops},
    "powers_of_ten": {"A": _gen_powers_of_ten, "B": _gen_powers_of_ten},
    "distributive_trick": {"A": _gen_distributive_trick, "B": _gen_distributive_trick},
    "pythagorean_triples": {
        "A": _gen_pythagorean_triples,
        "B": _gen_pythagorean_triples,
        "C": _gen_pythagorean_triples,
    },
    "angle_pairs": {"A": _gen_angle_pairs, "B": _gen_angle_pairs, "C": _gen_angle_pairs},
    "slope_snap": {"A": _gen_slope_snap, "B": _gen_slope_snap, "C": _gen_slope_snap},
    "unit_rates": {"A": _gen_unit_rates, "B": _gen_unit_rates},
    "order_of_ops": {"A": _gen_order_of_ops, "B": _gen_order_of_ops, "C": _gen_order_of_ops},
    "frac_ops": {"A": _gen_frac_ops, "B": _gen_frac_ops, "C": _gen_frac_ops},
    "gcf_lcm": {"A": _gen_gcf_lcm, "B": _gen_gcf_lcm, "C": _gen_gcf_lcm},
    "special_products": {
        "A": _gen_special_products,
        "B": _gen_special_products,
        "C": _gen_special_products,
    },
}


def _active_drill_slots(config: dict) -> list[tuple[str, str]]:
    slots: list[tuple[str, str]] = []
    for item in config.get("mental_math", []):
        did = str(item.get("id", ""))
        for lvl in item.get("levels", []):
            if did in DRILLS and lvl in DRILLS[did]["levels"]:
                slots.append((did, lvl))
    return slots


def generate_drill_question(drill_id: str, level: str) -> dict | None:
    fn = GENERATOR_MAP.get(drill_id, {}).get(level)
    if not fn:
        return None
    return fn(level)


def build_mental_warmups(config: dict, count: int | None = None) -> list[dict]:
    """Generate mental-math warm-up questions from weekly drill selections."""
    slots = _active_drill_slots(config)
    if not slots:
        return []

    if count is None:
        count = get_mental_math_count(config)
    if count <= 0:
        return []

    selected: list[dict] = []
    used_ids: set[str] = set()
    slot_cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(slot_cycle)

    for did, lvl in slot_cycle:
        if len(selected) >= count:
            break
        for _ in range(12):
            q = generate_drill_question(did, lvl)
            if q and q["id"] not in used_ids:
                selected.append(q)
                used_ids.add(q["id"])
                break
    return selected
