"""NCERT Class 9 PreReq topics, difficulty levels, and question generators."""

from __future__ import annotations

import math
import random
import uuid
from fractions import Fraction

LEVEL_ORDER = ["A", "B", "C", "D", "E"]

# prereq_id -> topic_id -> metadata
TOPICS: dict[int, dict[int, dict]] = {
    1: {
        1: {
            "name": "Number Line & Integers",
            "short": "Number Line",
            "emoji": "📏",
            "levels": {
                "A": "Plot integers −10 to 10",
                "B": "Compare distances from zero",
                "C": "Add/subtract on the number line",
                "D": "Mixed integer operations",
                "E": "Nested signs & expressions",
            },
        },
        2: {
            "name": "Rational Number Operations",
            "short": "Rational Ops",
            "emoji": "➗",
            "levels": {
                "A": "Same-sign add/subtract",
                "B": "Different denominators",
                "C": "Multiply & divide fractions",
                "D": "Mixed rational expressions",
                "E": "Word-style rational problems",
            },
        },
        3: {
            "name": "Exponents & Roots",
            "short": "Exponents",
            "emoji": "²",
            "levels": {
                "A": "Positive integer exponents",
                "B": "Negative exponents",
                "C": "Fractional exponents intro",
                "D": "Square roots & perfect squares",
                "E": "Combine exponent laws",
            },
        },
        4: {
            "name": "Rationalizing Denominators",
            "short": "Rationalize",
            "emoji": "√",
            "levels": {
                "A": "Monomial denominators",
                "B": "Binomial with √",
                "C": "Conjugate pairs",
                "D": "Mixed surd forms",
                "E": "Apply to simplify expressions",
            },
        },
        5: {
            "name": "Irrational Numbers",
            "short": "Irrational",
            "emoji": "π",
            "levels": {
                "A": "Identify rational vs irrational",
                "B": "Locate roots on number line",
                "C": "Estimate √ values",
                "D": "Operations with irrationals",
                "E": "Decimal expansion patterns",
            },
        },
    },
    2: {
        1: {
            "name": "Polynomial Addition & Subtraction",
            "short": "Poly +/-",
            "emoji": "➕",
            "levels": {
                "A": "Like terms only",
                "B": "Introduce unlike terms",
                "C": "Subtract with parentheses",
                "D": "Multi-variable polynomials",
                "E": "Evaluate after simplify",
            },
        },
        2: {
            "name": "Polynomial Multiplication",
            "short": "Poly ×",
            "emoji": "✖️",
            "levels": {
                "A": "Monomial × polynomial",
                "B": "Binomial × binomial",
                "C": "Special products",
                "D": "Three-term products",
                "E": "Application problems",
            },
        },
        3: {
            "name": "Factorization",
            "short": "Factor",
            "emoji": "🧩",
            "levels": {
                "A": "Common factor",
                "B": "Grouping",
                "C": "Identities a²±2ab+b²",
                "D": "Difference of squares",
                "E": "Trinomial factorization",
            },
        },
        4: {
            "name": "Substitution in Linear Equations",
            "short": "Substitute",
            "emoji": "🔢",
            "levels": {
                "A": "Find y given x",
                "B": "Find x given y",
                "C": "Two-step substitution",
                "D": "Negative coefficients",
                "E": "Fraction coefficients",
            },
        },
        5: {
            "name": "Solution Tables & Ordered Pairs",
            "short": "Tables",
            "emoji": "📋",
            "levels": {
                "A": "Complete (x, ?) when y is given",
                "B": "Complete (?, y) when x is given",
                "C": "Build a small solution table",
                "D": "Standard form ax + by + c = 0",
                "E": "Infinitely many solutions concept",
            },
        },
        6: {
            "name": "Graphing & Point Verification",
            "short": "Graph",
            "emoji": "📈",
            "levels": {
                "A": "Which point satisfies the equation?",
                "B": "Is a point on the line? (yes/no style)",
                "C": "Read y from graph at given x",
                "D": "Match equation to graph description",
                "E": "Intercept-style reasoning",
            },
        },
        7: {
            "name": "Linear Word Problems & Applications",
            "short": "Word Prob",
            "emoji": "📝",
            "levels": {
                "A": "Form ax + by = c from context",
                "B": "Find one unknown from a story",
                "C": "Two-variable cost / quantity setups",
                "D": "Convert to standard form",
                "E": "Multi-step application problems",
            },
        },
    },
    3: {
        1: {
            "name": "Plotting & Reading Points",
            "short": "Plot Points",
            "emoji": "📍",
            "levels": {
                "A": "Quadrant identification",
                "B": "Plot from coordinates",
                "C": "Read coordinates from graph",
                "D": "Midpoint intuition",
                "E": "Distance from axes",
            },
        },
        2: {
            "name": "Equations of Lines",
            "short": "Line Equations",
            "emoji": "📊",
            "levels": {
                "A": "y = mx when c = 0",
                "B": "y = mx + c",
                "C": "Horizontal & vertical lines",
                "D": "Find slope from two points",
                "E": "Interpret slope in context",
            },
        },
    },
    4: {
        1: {
            "name": "Lines & Angles",
            "short": "Angles",
            "emoji": "📐",
            "levels": {
                "A": "Complementary & supplementary",
                "B": "Vertically opposite angles",
                "C": "Parallel line transversal",
                "D": "Angle chase multi-step",
                "E": "Proof-style reasoning",
            },
        },
        2: {
            "name": "Triangles",
            "short": "Triangles",
            "emoji": "🔺",
            "levels": {
                "A": "Angle sum property",
                "B": "Exterior angle theorem",
                "C": "Congruence (SSS/SAS)",
                "D": "Isosceles & equilateral",
                "E": "Inequalities in triangles",
            },
        },
        3: {
            "name": "Quadrilaterals",
            "short": "Quads",
            "emoji": "⬜",
            "levels": {
                "A": "Parallelogram properties",
                "B": "Rectangle & rhombus",
                "C": "Trapezium & kite",
                "D": "Mid-point theorem",
                "E": "Combine properties",
            },
        },
        4: {
            "name": "Circles",
            "short": "Circles",
            "emoji": "⭕",
            "levels": {
                "A": "Radius, diameter, chord",
                "B": "Angle subtended at centre",
                "C": "Cyclic quadrilateral",
                "D": "Arc & sector basics",
                "E": "Multi-step circle problems",
            },
        },
    },
    5: {
        1: {
            "name": "Heron's Formula",
            "short": "Heron",
            "emoji": "📐",
            "levels": {
                "A": "Semi-perimeter first",
                "B": "Integer side lengths",
                "C": "Include units",
                "D": "Compare triangle areas",
                "E": "Composite figures",
            },
        },
        2: {
            "name": "Surface Area",
            "short": "Surface Area",
            "emoji": "📦",
            "levels": {
                "A": "Cube & cuboid",
                "B": "Cylinder lateral area",
                "C": "Total surface cylinder",
                "D": "Cone & sphere intro",
                "E": "Combined solids",
            },
        },
        3: {
            "name": "Volume",
            "short": "Volume",
            "emoji": "🧊",
            "levels": {
                "A": "Cube & cuboid volume",
                "B": "Cylinder volume",
                "C": "Cone & hemisphere",
                "D": "Sphere volume",
                "E": "Capacity word problems",
            },
        },
    },
    6: {
        1: {
            "name": "Mean, Median & Mode",
            "short": "Central Tendency",
            "emoji": "📊",
            "levels": {
                "A": "Mean of small data sets",
                "B": "Median (odd count)",
                "C": "Median (even count)",
                "D": "Mode & bimodal data",
                "E": "Choose best measure",
            },
        },
        2: {
            "name": "Graphical Representation",
            "short": "Graphs",
            "emoji": "📈",
            "levels": {
                "A": "Bar graph reading",
                "B": "Histogram intervals",
                "C": "Frequency polygon",
                "D": "Compare distributions",
                "E": "Interpret trends",
            },
        },
        3: {
            "name": "Probability",
            "short": "Probability",
            "emoji": "🎲",
            "levels": {
                "A": "Equally likely outcomes",
                "B": "Complementary events",
                "C": "Two dice/coins",
                "D": "Simple word problems",
                "E": "Compare experimental vs theoretical",
            },
        },
    },
}


def topics_for_prereq(prereq_id: int) -> dict[int, dict]:
    return TOPICS.get(prereq_id, {})


def default_week_config(prereq_id: int) -> dict:
    """Starter plan — Level A on every strategy/topic (PreReq 2 uses 7 Arjun-style strategies)."""
    topics = topics_for_prereq(prereq_id)
    meta = {1: "Number Systems", 2: "Algebra", 3: "Coordinate", 4: "Geometry", 5: "Mensuration", 6: "Data"}
    label = meta.get(prereq_id, f"PreReq {prereq_id}")
    if prereq_id == 2:
        return {
            "week_label": "Algebra — Week 1 (Foundation)",
            "topics": [{"id": tid, "levels": ["A"]} for tid in sorted(topics)],
            "warmup_count": 0,
            "use_llm": True,
            "use_chapter_llm": True,
            "grok_fresh_only": False,
            "prereq_id": prereq_id,
        }
    return {
        "week_label": f"{label} — Week 1",
        "topics": [{"id": tid, "levels": ["A", "B"]} for tid in sorted(topics)],
        "warmup_count": 0,
        "use_llm": True,
        "use_chapter_llm": True,
        "grok_fresh_only": False,
        "prereq_id": prereq_id,
    }


def format_topic_level_label(prereq_id: int, topic_id: int, level: str) -> str:
    info = TOPICS.get(prereq_id, {}).get(topic_id, {})
    return f"{info.get('short', topic_id)} · Level {level}"


def format_week_plan_summary(prereq_id: int, config: dict) -> str:
    lines = []
    if config.get("week_label"):
        lines.append(f"Week: {config['week_label']}")
    for item in config.get("topics", []):
        tid = int(item["id"])
        info = TOPICS.get(prereq_id, {}).get(tid, {})
        lvls = ", ".join(item.get("levels", []))
        lines.append(f"  • {info.get('name', tid)} [{lvls}]")
    wc = config.get("warmup_count", 0)
    if wc:
        lines.append(f"  • Warm-ups: {wc} quick checks")
    if config.get("use_chapter_llm") or config.get("use_llm"):
        lines.append("  • xAI (Grok) live generation: on")
    else:
        lines.append("  • xAI (Grok) live generation: off")
    return "\n".join(lines) if lines else "No topics selected."


def _mcq(
    prereq_id: int,
    topic_id: int,
    level: str,
    question: str,
    options: list[str],
    answer: int,
    explanation: str = "",
    *,
    diagram: dict | None = None,
) -> dict:
    item = {
        "id": f"p{prereq_id}_t{topic_id}_{level}_{uuid.uuid4().hex[:8]}",
        "question": question,
        "options": options,
        "answer": answer,
        "topic": topic_id,
        "level": level,
        "prereq_id": prereq_id,
        "category": f"p{prereq_id}_t{topic_id}_{level}",
        "category_label": format_topic_level_label(prereq_id, topic_id, level),
        "explanation": explanation,
        "source": "template",
    }
    if diagram:
        item["diagram"] = diagram
    return item


def _pad_distinct_distractors(correct: str, seen: set[str], needed: int) -> list[str]:
    """Fill missing wrong options with values distinct from `correct` and `seen`."""
    padded: list[str] = []
    try:
        val = int(correct)
        for delta in range(1, 50):
            for offset in (delta, -delta):
                candidate = str(val + offset)
                if candidate not in seen:
                    seen.add(candidate)
                    padded.append(candidate)
                    if len(padded) >= needed:
                        return padded
    except ValueError:
        pass
    try:
        if "/" in correct:
            base = Fraction(correct)
            for delta in range(1, 20):
                for offset in (Fraction(delta), Fraction(-delta)):
                    candidate = str(base + offset)
                    if candidate not in seen:
                        seen.add(candidate)
                        padded.append(candidate)
                        if len(padded) >= needed:
                            return padded
    except (ValueError, ZeroDivisionError):
        pass
    suffix = 1
    while len(padded) < needed:
        candidate = f"{correct} (alt {suffix})"
        suffix += 1
        if candidate not in seen:
            seen.add(candidate)
            padded.append(candidate)
    return padded


def _shuffle_options(correct: str, wrong: list[str]) -> tuple[list[str], int]:
    correct = str(correct)
    seen = {correct}
    unique_wrong: list[str] = []
    for item in wrong:
        candidate = str(item)
        if candidate in seen:
            continue
        seen.add(candidate)
        unique_wrong.append(candidate)
    if len(unique_wrong) < 3:
        unique_wrong.extend(_pad_distinct_distractors(correct, seen, 3 - len(unique_wrong)))
    opts = [correct, *unique_wrong[:3]]
    random.shuffle(opts)
    return opts, opts.index(correct)


# ── Unit 1 generators ──


def _gen_p1_t1(level: str) -> dict:
    if level == "A":
        a, b = random.randint(-9, 9), random.randint(-9, 9)
        while a == b:
            b = random.randint(-9, 9)
        farther = a if abs(a) > abs(b) else b
        opts, ans = _shuffle_options(str(farther), [str(a), str(b), str(-farther)])
        return _mcq(1, 1, level, f"Which is farther from zero: {a} or {b}?", opts, ans, f"|{farther}| is larger.")
    if level == "B":
        a, b = random.randint(-12, 12), random.randint(-12, 12)
        opts, ans = _shuffle_options(str(a + b), [str(a - b), str(a * b), str(b - a)])
        return _mcq(1, 1, level, f"Compute: ({a}) + ({b})", opts, ans, "Add integers carefully, including signs.")
    if level in ("C", "D"):
        a, b = random.randint(-9, 9), random.randint(1, 8)
        val = a - b
        opts, ans = _shuffle_options(str(val), [str(a + b), str(-val), str(b - a)])
        return _mcq(1, 1, level, f"Compute: {a} − {b}", opts, ans)
    a, b, c = random.randint(-5, 5), random.randint(-5, 5), random.randint(1, 4)
    pattern = random.choice(["nested_sub", "group_add", "mixed_signs"])
    if pattern == "group_add":
        val = (a + b) - c
        opts, ans = _shuffle_options(str(val), [str(a + b + c), str(a - b + c), str(c - a - b)])
        return _mcq(1, 1, level, f"Compute: ({a} + {b}) − {c}", opts, ans)
    if pattern == "mixed_signs":
        val = a - b - c
        opts, ans = _shuffle_options(str(val), [str(a + b + c), str(b + c - a), str(a - b + c)])
        return _mcq(1, 1, level, f"Compute: {a} − {b} − {c}", opts, ans)
    val = a - (b + c)
    opts, ans = _shuffle_options(str(val), [str(a + b + c), str(b + c - a), str(a - b + c)])
    return _mcq(1, 1, level, f"Compute: {a} − ({b} + {c})", opts, ans)


def _gen_p1_t2(level: str) -> dict:
    if level in ("A", "B"):
        a, b = random.randint(1, 5), random.randint(1, 5)
        c, d = random.randint(2, 6), random.randint(2, 6)
        num = a * d + b * c if random.choice([True, False]) else a * d - b * c
        den = b * d
        g = Fraction(num, den)
        opts, ans = _shuffle_options(str(g), [str(g + 1), str(Fraction(1, 2)), str(g - 1)])
        return _mcq(1, 2, level, f"Compute: {a}/{b} + {c}/{d}", opts, ans)
    a, b, c = random.randint(1, 4), random.randint(2, 5), random.randint(1, 4)
    val = Fraction(a, b) * Fraction(c, b)
    opts, ans = _shuffle_options(str(val), [str(Fraction(a + c, b)), str(Fraction(a, b + c)), str(val + 1)])
    return _mcq(1, 2, level, f"Multiply: {a}/{b} × {c}/{b}", opts, ans)


def _gen_p1_t3(level: str) -> dict:
    if level in ("A", "B"):
        base, exp = random.randint(2, 5), random.randint(2, 4)
        val = base ** exp
        opts, ans = _shuffle_options(str(val), [str(base * exp), str(base + exp), str(val + base)])
        return _mcq(1, 3, level, f"Evaluate: {base}^{exp}", opts, ans)
    n = random.randint(2, 5)
    val = Fraction(1, n ** 2)
    opts, ans = _shuffle_options(str(val), [str(Fraction(1, n)), str(Fraction(2, n)), str(n)])
    return _mcq(1, 3, level, f"Evaluate: {n}^-2", opts, ans)


def _conjugate_product_mcq(prereq_id: int, topic_id: int, level: str, a: int, b: int) -> dict:
    """(√a + √b)(√a − √b) = a − b — kid-friendly wording and numeric options."""
    result = a - b
    correct = str(result)
    wrong = [str(a + b), f"√{a} + √{b}", f"√{a} − √{b}"]
    opts, ans = _shuffle_options(correct, wrong)
    question = f"Simplify: (√{a} + √{b})(√{a} − √{b}) = ?"
    if result == 0:
        explanation = (
            f"Use (x + y)(x − y) = x² − y². Here both parts use √{a}, so you get {a} − {b} = 0."
        )
    else:
        explanation = (
            f"Use (x + y)(x − y) = x² − y². With x = √{a} and y = √{b}, you get {a} − {b} = {result}."
        )
    return _mcq(prereq_id, topic_id, level, question, opts, ans, explanation)


def _gen_p1_t4(level: str) -> dict:
    if level in ("A", "B"):
        n = random.choice([2, 3, 5, 6, 7, 10, 11, 13])
        opts, ans = _shuffle_options(f"√{n}/{n}", [f"1/√{n}", f"{n}/√{n}", f"√{n}"])
        return _mcq(
            1, 4, level,
            f"Rationalize: 1/√{n} = ?",
            opts, ans,
            f"Multiply top and bottom by √{n} to get √{n}/{n}.",
        )
    a, b = random.randint(1, 4), random.choice([2, 3, 5])
    return _conjugate_product_mcq(1, 4, level, a, b)


def _construction_mcq(prereq_id: int, topic_id: int, level: str, spec: dict) -> dict:
    """Number-line / unit-square construction with diagram."""
    import harshit_math_diagrams as hmd

    kind = spec["type"]
    if kind == "unit_square":
        opts, ans = _shuffle_options("√2", ["1", "2", "√3"])
        expl = "By Pythagoras: OB = √(1² + 1²) = √2. Transfer OB to the number line with a compass."
        diagram = {"type": "unit_square", "target": 2}
        question = hmd.kid_friendly_prompt({"diagram": diagram}, diagram) or "What is diagonal OB?"
    elif kind == "sqrt_number_line":
        base, perp = int(spec["base"]), int(spec["perp"])
        target = base * base + perp * perp
        correct = f"√{target}"
        opts, ans = _shuffle_options(correct, [str(base + perp), f"√{base * base}", f"√{perp * perp}"])
        expl = f"By Pythagoras: OB = √({base}² + {perp}²) = √{target}."
        diagram = {"type": "sqrt_number_line", "base": base, "perp": perp, "target": target}
        question = hmd.kid_friendly_prompt({"diagram": diagram}, diagram) or "What is hypotenuse OB?"
    else:  # sqrt_extend
        perp = int(spec.get("perp", 1))
        target = int(spec.get("target", 3))
        correct = f"√{target}"
        opts, ans = _shuffle_options(correct, ["√2", "2", "√4"])
        expl = f"By Pythagoras: OB = √((√2)² + {perp}²) = √{target}."
        diagram = {"type": "sqrt_extend", "base_label": spec.get("base_label", "√2"), "perp": perp, "target": target}
        question = hmd.kid_friendly_prompt({"diagram": diagram}, diagram) or "What is hypotenuse OB?"
    return _mcq(prereq_id, topic_id, level, question, opts, ans, expl, diagram=diagram)


def _gen_p1_t5(level: str) -> dict:
    if level in ("A", "B"):
        kind = random.choice(["sqrt_int", "sqrt_prime", "decimal", "frac"])
        if kind == "sqrt_int":
            q, correct = f"√{random.choice([4, 9, 16, 25])}", "Rational"
        elif kind == "sqrt_prime":
            q, correct = f"√{random.choice([2, 3, 5, 7])}", "Irrational"
        elif kind == "decimal":
            q, correct = f"0.{'0' * random.randint(1, 3)}1… (non-repeating)", "Irrational"
        else:
            q, correct = f"{random.randint(1, 9)}/3", "Rational"
        wrong = [x for x in ("Rational", "Irrational") if x != correct]
        opts, ans = _shuffle_options(correct, wrong + ["Neither"])
        return _mcq(1, 5, level, f"Classify: {q}", opts, ans)
    if level in ("C", "D"):
        spec = random.choice([
            {"type": "unit_square"},
            {"type": "sqrt_number_line", "base": 2, "perp": 1},
            {"type": "sqrt_number_line", "base": 3, "perp": 1},
            {"type": "sqrt_extend", "base_label": "√2", "perp": 1, "target": 3},
        ])
        return _construction_mcq(1, 5, level, spec)
    n = random.randint(2, 12)
    opts, ans = _shuffle_options("Between 3 and 4", ["Between 2 and 3", "Between 4 and 5", "Exactly 4"])
    return _mcq(1, 5, level, f"√{n} lies on the number line…", opts, ans, "√9=3 and √16=4 bracket most values.")


# ── Unit 2 generators ──


def _lin_term(coeff: int, var: str) -> str:
    if coeff == 1:
        return var
    if coeff == -1:
        return f"-{var}"
    return f"{coeff}{var}"


def _lin_eq(a: int, b: int, c: int) -> str:
    parts: list[str] = []
    if a != 0:
        parts.append(_lin_term(a, "x"))
    if b != 0:
        if parts:
            parts.append(f"+ {_lin_term(b, 'y')}" if b > 0 else f"- {_lin_term(-b, 'y')}")
        else:
            parts.append(_lin_term(b, "y"))
    return f"{' '.join(parts)} = {c}"


def _gen_p2_t1(level: str) -> dict:
    a, b = random.randint(1, 5), random.randint(1, 5)
    c, d = random.randint(1, 4), random.randint(1, 4)
    expr = f"({a}x + {b}) + ({c}x + {d})"
    coeff, const = a + c, b + d
    correct = f"{coeff}x + {const}" if const else f"{coeff}x"
    opts, ans = _shuffle_options(correct, [f"{a+c+1}x + {const}", f"{coeff}x + {const+1}", f"{a}x + {b+c}"])
    return _mcq(2, 1, level, f"Simplify: {expr}", opts, ans)


def _gen_p2_t2(level: str) -> dict:
    a, b = random.randint(1, 4), random.randint(1, 4)
    correct = f"{a}x² + {a*b}x" if b else f"{a}x²"
    opts, ans = _shuffle_options(correct, [f"{a}x + {b}", f"{a}x² + {b}", f"{2*a}x²"])
    return _mcq(2, 2, level, f"Expand: {a}x(x + {b})", opts, ans)


def _gen_p2_t3(level: str) -> dict:
    a = random.randint(2, 6)
    b = random.randint(1, 5)
    correct = f"{a}({b}x + 1)"
    opts, ans = _shuffle_options(correct, [f"({a+b})x + 1", f"{a}x + {b}", f"{a*b}x"])
    return _mcq(2, 3, level, f"Factor: {a*b}x + {a}", opts, ans)


def _gen_p2_t4(level: str) -> dict:
    a, b = random.randint(1, 4), random.randint(1, 4)
    c = random.randint(6, 18)
    if level in ("A", "C"):
        x = random.randint(0, 4)
        y = (c - a * x) // b if (c - a * x) % b == 0 else (c - a * x) / b
        correct = str(int(y)) if y == int(y) else str(Fraction(y).limit_denominator())
        opts, ans = _shuffle_options(correct, [str(x + b), str(a * x), str(c - a)])
        return _mcq(2, 4, level, f"For {_lin_eq(a, b, c)}, find y when x = {x}.", opts, ans)
    if level in ("B", "D"):
        y = random.randint(0, 4)
        x_val = (c - b * y) // a if (c - b * y) % a == 0 else (c - b * y) / a
        correct = str(int(x_val)) if x_val == int(x_val) else str(Fraction(x_val).limit_denominator())
        opts, ans = _shuffle_options(correct, [str(y + a), str(b * y), str(c - b)])
        return _mcq(2, 4, level, f"For {_lin_eq(a, b, c)}, find x when y = {y}.", opts, ans)
    a, b, c = 2, 3, 12
    x = random.randint(1, 3)
    y = Fraction(c - a * x, b)
    correct = str(y)
    opts, ans = _shuffle_options(correct, [str(y + 1), str(Fraction(c, b)), str(x)])
    return _mcq(2, 4, level, f"For {_lin_eq(a, b, c)}, find y when x = {x}.", opts, ans)


def _gen_p2_t5(level: str) -> dict:
    a, b = random.randint(1, 4), random.randint(1, 4)
    c = random.randint(6, 16)
    if level in ("A", "C"):
        y = c // b if c % b == 0 else random.randint(1, 4)
        if a * 0 + b * y != c:
            y = (c - a * 0) // b
        correct = str(y)
        opts, ans = _shuffle_options(correct, [str(y + 1), str(b), str(c // a if a else c)])
        return _mcq(2, 5, level, f"For {_lin_eq(a, b, c)}, complete (0, ?).", opts, ans)
    if level in ("B", "D"):
        x = c // a if c % a == 0 else random.randint(1, 4)
        correct = str(x)
        opts, ans = _shuffle_options(correct, [str(x + 1), str(a), str(c // b if b else c)])
        return _mcq(2, 5, level, f"For {_lin_eq(a, b, c)}, complete (?, 0).", opts, ans)
    opts, ans = _shuffle_options("Infinitely many", ["Exactly one", "None", "Two only"])
    return _mcq(2, 5, level, f"How many solutions does {_lin_eq(a, b, c)} have?", opts, ans)


def _gen_p2_t6(level: str) -> dict:
    a, b = random.randint(1, 3), random.randint(1, 3)
    c = a * 2 + b * 2
    good = f"(2, 2)"
    bad = [
        f"({2 + 1}, {2})",
        f"({2}, {2 + 1})",
        f"({2 - 1}, {2 - 1})",
    ]
    opts, ans = _shuffle_options(good, bad)
    return _mcq(2, 6, level, f"Which point lies on {_lin_eq(a, b, c)}?", opts, ans)


def _gen_p2_t7(level: str) -> dict:
    x_cost, y_cost = random.randint(2, 5), random.randint(3, 7)
    total = random.randint(20, 40)
    if level in ("A", "D"):
        opts, ans = _shuffle_options(
            _lin_eq(x_cost, y_cost, total),
            [f"x + y = {total}", f"{x_cost}x = {y_cost}y", f"{_lin_eq(x_cost, -y_cost, total)}"],
        )
        return _mcq(
            2, 7, level,
            f"A shop sells items at ₹{x_cost} and ₹{y_cost}. Total spent is ₹{total}. "
            f"Which equation models x items at ₹{x_cost} and y items at ₹{y_cost}?",
            opts, ans,
        )
    a, b, c = x_cost, y_cost, total
    x = random.randint(1, 4)
    y = (c - a * x) // b if (c - a * x) % b == 0 else 1
    correct = str(y)
    opts, ans = _shuffle_options(correct, [str(y + 2), str(x), str(c)])
    return _mcq(
        2, 7, level,
        f"Using {_lin_eq(a, b, c)}, if x = {x}, what is y?",
        opts, ans,
    )


# ── Unit 3 generators ──


def _quadrant_label(x: int, y: int) -> str:
    if x > 0 and y > 0:
        return "I"
    if x < 0 and y > 0:
        return "II"
    if x < 0 and y < 0:
        return "III"
    return "IV"


def _gen_p3_t1(level: str) -> dict:
    if level in ("A", "B"):
        x, y = random.randint(-8, 8), random.randint(-8, 8)
        while x == 0 or y == 0:
            x, y = random.randint(-8, 8), random.randint(-8, 8)
        quad = _quadrant_label(x, y)
        opts, ans = _shuffle_options(quad, ["I", "II", "III", "IV"])
        return _mcq(
            3, 1, level,
            f"Point ({x}, {y}) lies in which quadrant?",
            opts, ans,
            f"({x}, {y}) is in Quadrant {quad}.",
        )
    if level == "C":
        x, y = random.randint(-6, 6), random.randint(-6, 6)
        while x == 0 or y == 0:
            x, y = random.randint(-6, 6), random.randint(-6, 6)
        correct = f"({x}, {y})"
        opts, ans = _shuffle_options(correct, [f"({y}, {x})", f"({-x}, {y})", f"({x}, {-y})"])
        return _mcq(3, 1, level, f"A point is {abs(x)} units from the y-axis and {abs(y)} units from the x-axis, on the same side of both axes as ({x}, {y}). What are its coordinates?", opts, ans)
    if level == "D":
        x1, y1 = random.randint(-5, 5), random.randint(-5, 5)
        x2, y2 = random.randint(-5, 5), random.randint(-5, 5)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        correct = f"({mx:g}, {my:g})"
        opts, ans = _shuffle_options(correct, [f"({x1 + x2}, {y1})", f"({x1}, {y2})", f"({x2 - x1}, {y2 - y1})"])
        return _mcq(3, 1, level, f"Midpoint of ({x1}, {y1}) and ({x2}, {y2})?", opts, ans, "Average the x- and y-coordinates.")
    x, y = random.randint(1, 9), random.randint(1, 9)
    dist = min(abs(x), abs(y))
    opts, ans = _shuffle_options(f"{dist}", [f"{x + y}", f"{max(abs(x), abs(y))}", f"{x * y}"])
    return _mcq(3, 1, level, f"Point ({x}, {y}) is in Quadrant I. Its distance from the nearer axis is?", opts, ans, "Use the smaller of |x| and |y|.")


def _gen_p3_t2(level: str) -> dict:
    if level == "A":
        m = random.randint(1, 5)
        opts, ans = _shuffle_options(f"y = {m}x", [f"y = {m}x + 1", f"x = {m}y", f"y = {m + 1}x"])
        return _mcq(3, 2, level, f"Which line passes through the origin with slope {m}?", opts, ans)
    if level == "B":
        m, c = random.randint(1, 4), random.randint(-3, 4)
        opts, ans = _shuffle_options(f"y = {m}x + {c}", [f"y = {c}x + {m}", f"x = {m}y + {c}", f"y = {m}x − {c}"])
        return _mcq(3, 2, level, f"Which equation has slope {m} and y-intercept {c}?", opts, ans)
    if level == "C":
        k = random.randint(-5, 5)
        if random.choice([True, False]):
            opts, ans = _shuffle_options(f"x = {k}", [f"y = {k}", f"y = x + {k}", f"x = y + {k}"])
            return _mcq(3, 2, level, f"Which equation represents a vertical line through x = {k}?", opts, ans)
        opts, ans = _shuffle_options(f"y = {k}", [f"x = {k}", f"y = x + {k}", f"x = y + {k}"])
        return _mcq(3, 2, level, f"Which equation represents a horizontal line through y = {k}?", opts, ans)
    if level == "D":
        x1, y1 = random.randint(-3, 3), random.randint(-3, 3)
        x2, y2 = x1 + random.randint(1, 4), y1 + random.randint(1, 4)
        slope = Fraction(y2 - y1, x2 - x1)
        correct = str(slope) if slope.denominator != 1 else str(slope.numerator)
        opts, ans = _shuffle_options(correct, [str(slope + 1), str(-slope), str(slope + 2)])
        return _mcq(3, 2, level, f"Slope of the line through ({x1}, {y1}) and ({x2}, {y2})?", opts, ans, "Slope = (y₂ − y₁)/(x₂ − x₁).")
    m = random.randint(1, 4)
    opts, ans = _shuffle_options("Distance increases by 3 km per hour", [f"Fixed cost of {m} km", "No change over time", "Distance decreases"])
    return _mcq(3, 2, level, f"A taxi charges a fixed fee plus {m}×(km). Which describes the slope in a distance-vs-time graph if speed is constant?", opts, ans, "Slope is rate of change.")


# ── Unit 4 generators ──


def _gen_p4_t1(level: str) -> dict:
    if level in ("A", "B"):
        angle = random.randint(15, 75)
        if random.choice([True, False]):
            sup = 180 - angle
            opts, ans = _shuffle_options(f"{sup}°", [f"{angle}°", f"{90 - angle}°", f"{angle + 90}°"])
            return _mcq(
                4, 1, level, f"An angle measures {angle}°. Its supplement is?", opts, ans,
                diagram={"type": "angle_arc", "degrees": angle},
            )
        comp = 90 - angle
        opts, ans = _shuffle_options(f"{comp}°", [f"{angle}°", f"{180 - angle}°", f"{angle + 90}°"])
        return _mcq(
            4, 1, level, f"An acute angle measures {angle}°. Its complement is?", opts, ans,
            diagram={"type": "angle_arc", "degrees": angle},
        )
    if level == "C":
        angle = random.randint(40, 70)
        alt = angle
        corr = 180 - angle
        opts, ans = _shuffle_options(f"{corr}°", [f"{alt}°", f"{90 - angle}°", f"{angle + 90}°"])
        return _mcq(
            4, 1, level,
            f"Two parallel lines are cut by a transversal. One interior angle is {angle}°. A co-interior angle on the same side is?",
            opts, ans, "Co-interior angles are supplementary.",
            diagram={"type": "parallel_transversal", "angle": angle},
        )
    a, b = random.randint(20, 50), random.randint(20, 50)
    vert = b
    opts, ans = _shuffle_options(f"{vert}°", [f"{180 - b}°", f"{90 - b}°", f"{a + b}°"])
    return _mcq(
        4, 1, level,
        f"Two lines intersect. One angle is {a}° and its adjacent angle is {b}°. A vertically opposite angle to {b}° is?",
        opts, ans, "Vertically opposite angles are equal.",
        diagram={"type": "intersecting_lines", "angle_a": a, "angle_b": b},
    )


def _gen_p4_t2(level: str) -> dict:
    if level == "A":
        a, b = random.randint(30, 70), random.randint(30, 70)
        while a + b >= 170:
            b = random.randint(20, 60)
        third = 180 - a - b
        opts, ans = _shuffle_options(f"{third}°", [f"{a + b}°", f"{180 - a}°", f"{90}°"])
        return _mcq(
            4, 2, level, f"In a triangle, two angles are {a}° and {b}°. The third angle is?", opts, ans,
            "Angles in a triangle sum to 180°.",
            diagram={"type": "triangle", "angle_a": a, "angle_b": b},
        )
    if level == "B":
        interior = random.randint(40, 100)
        exterior = 180 - interior
        opts, ans = _shuffle_options(f"{exterior}°", [f"{interior}°", f"{180 + interior}°", f"{90}°"])
        return _mcq(
            4, 2, level,
            f"An exterior angle of a triangle equals the sum of the two remote interior angles. If one remote interior angle is {interior}° and the other is 35°, the exterior angle is?",
            opts, ans,
            diagram={"type": "triangle", "angle_a": interior, "angle_b": 35, "exterior": True},
        )
    if level == "C":
        rule = random.choice(["SSS", "SAS", "ASA"])
        wrong = [r for r in ["SSS", "SAS", "ASA", "AAA"] if r != rule]
        opts, ans = _shuffle_options(rule, wrong[:3])
        return _mcq(4, 2, level, f"Which congruence rule is listed: {rule}?", opts, ans, diagram={"type": "triangle"})
    if level == "D":
        base = random.randint(4, 12)
        opts, ans = _shuffle_options(f"{180 - 2 * base}°", [f"{base}°", f"{2 * base}°", f"{90 - base}°"])
        return _mcq(
            4, 2, level, f"In an isosceles triangle, each base angle is {base}°. The vertex angle is?", opts, ans,
            diagram={"type": "triangle", "angle_a": base, "angle_b": base},
        )
    a, b, c = 5, 7, 10
    opts, ans = _shuffle_options("No", ["Yes", "Maybe", "Only if right-angled"])
    return _mcq(4, 2, level, f"Can a triangle have sides {a}, {b}, and {c}?", opts, ans, "Check triangle inequality: 5 + 7 > 10 fails.", diagram={"type": "triangle"})


def _gen_p4_t3(level: str) -> dict:
    if level == "A":
        prop = random.choice([
            ("A parallelogram always has:", "Opposite sides parallel", ["All sides equal", "Diagonals always equal", "All angles 90°"], {"type": "parallelogram"}),
            ("Opposite sides of a parallelogram are:", "Equal and parallel", ["Perpendicular", "Unequal", "Only parallel"], {"type": "parallelogram"}),
            ("Adjacent angles in a parallelogram are:", "Supplementary", ["Equal", "Complementary", "Right angles"], {"type": "parallelogram", "show_diagonals": True}),
        ])
        opts, ans = _shuffle_options(prop[1], list(prop[2]))
        return _mcq(4, 3, level, prop[0], opts, ans, diagram=prop[3])
    if level == "B":
        shape = random.choice(["rectangle", "rhombus"])
        if shape == "rectangle":
            opts, ans = _shuffle_options("All angles 90°", ["All sides equal", "Diagonals perpendicular", "One pair of parallel sides"])
            return _mcq(4, 3, level, "A rectangle always has:", opts, ans, diagram={"type": "rectangle", "show_diagonals": True})
        opts, ans = _shuffle_options("All sides equal", ["All angles 90°", "Diagonals equal", "Opposite sides not parallel"])
        return _mcq(4, 3, level, "A rhombus always has:", opts, ans, diagram={"type": "rhombus", "show_diagonals": True})
    if level == "C":
        opts, ans = _shuffle_options("Exactly one pair of parallel sides", ["Two pairs of parallel sides", "All sides equal", "All angles equal"])
        return _mcq(4, 3, level, "A trapezium has:", opts, ans, diagram={"type": "trapezium"})
    if level == "D":
        opts, ans = _shuffle_options("Joining midpoints of two sides", ["Drawing a diagonal", "Extending a side", "Bisecting an angle"])
        return _mcq(4, 3, level, "The mid-point theorem is about:", opts, ans, diagram={"type": "triangle", "midpoints": True})
    opts, ans = _shuffle_options("Diagonals bisect each other", ["All sides equal", "All angles 90°", "One axis of symmetry only"])
    return _mcq(
        4, 3, level, "Which property is true for every parallelogram?", opts, ans,
        diagram={"type": "parallelogram", "show_diagonals": True},
    )


def _gen_p4_t4(level: str) -> dict:
    if level == "A":
        r = random.randint(3, 12)
        d = 2 * r
        opts, ans = _shuffle_options(f"{d}", [f"{r}", f"{r + d}", f"{d + 2}"])
        return _mcq(
            4, 4, level, f"A circle has radius {r} cm. Its diameter is?", opts, ans,
            diagram={"type": "circle", "variant": "basic"},
        )
    if level == "B":
        angle = random.randrange(40, 122, 2)
        half = angle // 2
        opts, ans = _shuffle_options(f"{half}°", [f"{angle}°", f"{180 - angle}°", f"{half + angle}°"])
        return _mcq(
            4, 4, level,
            f"An angle of {angle}° is subtended at the centre by a chord. The angle subtended by the same chord at any point on the major arc is half of this. That angle is?",
            opts, ans, "Angle at circumference is half the angle at centre.",
            diagram={"type": "circle", "variant": "center_angle", "angle": angle, "hide_center_label": True},
        )
    if level == "C":
        opts, ans = _shuffle_options("Opposite angles sum to 180°", ["All angles equal", "Adjacent angles equal", "Diagonals equal"])
        return _mcq(4, 4, level, "In a cyclic quadrilateral:", opts, ans, diagram={"type": "circle", "variant": "cyclic"})
    if level == "D":
        r = random.randint(2, 7)
        length = round(2 * math.pi * r, 1)
        opts, ans = _shuffle_options(f"{length}", [f"{math.pi * r}", f"{r ** 2}", f"{length + 2}"])
        return _mcq(
            4, 4, level, f"Circumference of a circle with radius {r} (use π ≈ 3.14)?", opts, ans, "C = 2πr.",
            diagram={"type": "circle", "variant": "basic"},
        )
    r = random.randint(3, 8)
    opts, ans = _shuffle_options("Equal chords subtend equal angles at the centre", ["Chord equals radius", "Tangent is parallel to radius", "Diameter equals circumference"])
    return _mcq(
        4, 4, level, f"In a circle of radius {r}, which statement is always true?", opts, ans,
        diagram={"type": "circle", "variant": "chord"},
    )


# ── Unit 5 generators ──


def _heron_area(a: int, b: int, c: int) -> float:
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def _gen_p5_t1(level: str) -> dict:
    triples = [(3, 4, 5), (5, 5, 6), (6, 8, 10), (7, 8, 9), (5, 12, 13)]
    a, b, c = random.choice(triples)
    area = _heron_area(a, b, c)
    correct = str(int(area)) if area == int(area) else f"{area:.1f}"
    s = (a + b + c) / 2
    if level == "A":
        opts, ans = _shuffle_options(f"{s:g}", [f"{a + b}", f"{c}", f"{s + 1:g}"])
        return _mcq(5, 1, level, f"Triangle sides {a}, {b}, {c}. Semi-perimeter s = ?", opts, ans, "s = (a + b + c)/2.")
    opts, ans = _shuffle_options(correct, [str(int(area) + 2), str(int(area) + 5), f"{a * b / 2:g}"])
    unit = " sq units" if level == "C" else ""
    return _mcq(5, 1, level, f"Area of triangle with sides {a}, {b}, {c} (Heron's formula)?{unit}", opts, ans)


def _gen_p5_t2(level: str) -> dict:
    if level == "A":
        side = random.randint(2, 8)
        sa = 6 * side ** 2
        opts, ans = _shuffle_options(f"{sa}", [f"{side ** 3}", f"{4 * side ** 2}", f"{sa + 6}"])
        return _mcq(5, 2, level, f"Total surface area of a cube of edge {side}?", opts, ans, "TSA = 6a².")
    if level in ("B", "C"):
        r, h = random.randint(2, 6), random.randint(3, 10)
        if level == "B":
            la = 2 * math.pi * r * h
            val = round(la, 1)
            opts, ans = _shuffle_options(f"{val:g}", [f"{math.pi * r * h:g}", f"{2 * r * h}", f"{val + 5:g}"])
            return _mcq(5, 2, level, f"Lateral surface area of cylinder r={r}, h={h} (π ≈ 3.14)?", opts, ans)
        tsa = 2 * math.pi * r * (r + h)
        val = round(tsa, 1)
        opts, ans = _shuffle_options(f"{val:g}", [f"{2 * math.pi * r * h:g}", f"{math.pi * r ** 2:g}", f"{val + 10:g}"])
        return _mcq(5, 2, level, f"Total surface area of cylinder r={r}, h={h} (π ≈ 3.14)?", opts, ans)
    if level == "D":
        r = random.randint(2, 5)
        sa = round(4 * math.pi * r ** 2, 1)
        opts, ans = _shuffle_options(f"{sa:g}", [f"{2 * math.pi * r:g}", f"{math.pi * r ** 2:g}", f"{sa + 4:g}"])
        return _mcq(5, 2, level, f"Surface area of a sphere of radius {r} (π ≈ 3.14)?", opts, ans)
    l, w, h = random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)
    cube_sa = 6 * l ** 2
    cuboid_sa = 2 * (l * w + w * h + h * l)
    opts, ans = _shuffle_options(f"{cube_sa + cuboid_sa}", [f"{cube_sa}", f"{cuboid_sa}", f"{l * w * h}"])
    return _mcq(5, 2, level, f"Cube edge {l} and cuboid {l}×{w}×{h}: sum of their total surface areas?", opts, ans)


def _gen_p5_t3(level: str) -> dict:
    if level == "A":
        l, w, h = random.randint(2, 6), random.randint(2, 6), random.randint(2, 6)
        vol = l * w * h
        opts, ans = _shuffle_options(f"{vol}", [f"{l + w + h}", f"{2 * (l * w)}", f"{vol + 1}"])
        return _mcq(5, 3, level, f"Volume of cuboid {l}×{w}×{h}?", opts, ans)
    if level == "B":
        r, h = random.randint(2, 6), random.randint(3, 9)
        vol = round(math.pi * r ** 2 * h, 1)
        opts, ans = _shuffle_options(f"{vol:g}", [f"{math.pi * r * h:g}", f"{r ** 2 * h}", f"{vol + 5:g}"])
        return _mcq(5, 3, level, f"Volume of cylinder r={r}, h={h} (π ≈ 3.14)?", opts, ans)
    if level == "C":
        r, h = random.randint(2, 5), random.randint(4, 9)
        vol = round(math.pi * r ** 2 * h / 3, 1)
        opts, ans = _shuffle_options(f"{vol:g}", [f"{math.pi * r ** 2 * h:g}", f"{2 * vol:g}", f"{vol + 3:g}"])
        return _mcq(5, 3, level, f"Volume of cone r={r}, h={h} (π ≈ 3.14)?", opts, ans)
    if level == "D":
        r = random.randint(2, 6)
        vol = round(4 * math.pi * r ** 3 / 3, 1)
        opts, ans = _shuffle_options(f"{vol:g}", [f"{4 * math.pi * r ** 2:g}", f"{math.pi * r ** 3:g}", f"{vol + 6:g}"])
        return _mcq(5, 3, level, f"Volume of sphere r={r} (π ≈ 3.14)?", opts, ans)
    litres = random.randint(2, 8)
    cm3 = litres * 1000
    opts, ans = _shuffle_options(f"{cm3} cm³", [f"{litres} cm³", f"{litres * 100} cm³", f"{cm3 // 10} cm³"])
    return _mcq(5, 3, level, f"A tank holds {litres} L. How many cm³ is that?", opts, ans, "1 L = 1000 cm³.")


# ── Unit 6 generators ──


def _gen_p6_t1(level: str) -> dict:
    if level in ("A", "B", "C"):
        n = 5 if level == "A" else (6 if level == "B" else 6)
        data = sorted(random.randint(1, 12) for _ in range(n))
        if level == "A":
            mean = sum(data) / len(data)
            correct = str(mean) if mean == int(mean) else f"{mean:.1f}"
            opts, ans = _shuffle_options(correct, [str(int(mean) + 1), str(max(data)), str(min(data))])
            return _mcq(6, 1, level, f"Mean of {data}?", opts, ans)
        mid = (data[len(data) // 2 - 1] + data[len(data) // 2]) / 2 if len(data) % 2 == 0 else data[len(data) // 2]
        correct = str(mid) if mid == int(mid) else f"{mid:.1f}"
        opts, ans = _shuffle_options(correct, [str(data[0]), str(data[-1]), str(int(mid) + 2)])
        return _mcq(6, 1, level, f"Median of {data}?", opts, ans)
    if level == "D":
        val = random.randint(2, 9)
        data = [val] * 3 + [val + 2, val + 4, val - 1, val + 1]
        random.shuffle(data)
        opts, ans = _shuffle_options(str(val), [str(val + 1), str(val - 1), str(val + 2)])
        return _mcq(6, 1, level, f"Mode of {data}?", opts, ans)
    data = [10, 12, 14, 100]
    opts, ans = _shuffle_options("Median", ["Mean", "Mode", "Range"])
    return _mcq(6, 1, level, f"Data {data} has an outlier. Which measure of centre is least affected?", opts, ans)


def _gen_p6_t2(level: str) -> dict:
    if level == "A":
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = [random.randint(2, 9) for _ in cats]
        total = sum(vals)
        opts, ans = _shuffle_options(f"{total}", [f"{total + 3}", f"{max(vals)}", f"{total - 2}"])
        return _mcq(6, 2, level, f"Bar graph counts {list(zip(cats, vals))}. Total count?", opts, ans)
    if level == "B":
        kind = random.choice(["histogram", "bar", "frequency"])
        if kind == "histogram":
            opts, ans = _shuffle_options("Histogram", ["Pie chart only", "Line graph only", "Scatter plot"])
            return _mcq(6, 2, level, "Best graph for grouped continuous data?", opts, ans)
        if kind == "bar":
            opts, ans = _shuffle_options("Bar graph", ["Histogram", "Frequency polygon", "Scatter plot"])
            return _mcq(6, 2, level, "Best graph for comparing discrete categories?", opts, ans)
        opts, ans = _shuffle_options("Frequency table", ["Pie chart only", "Line graph only", "Venn diagram"])
        return _mcq(6, 2, level, "Before drawing a graph, data is often organized in a:", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("Frequency polygon", ["Bar graph only", "Pie chart", "Stem-and-leaf only"])
        return _mcq(6, 2, level, "A graph formed by joining midpoints of histogram bars is a:", opts, ans)
    opts, ans = _shuffle_options("The distribution with the higher peak", ["Always the one with larger range", "Always the leftmost graph", "They must be identical"])
    return _mcq(6, 2, level, "When comparing two histograms, which is easiest to compare visually?", opts, ans)


def _gen_p6_t3(level: str) -> dict:
    if level == "A":
        fav = random.randint(1, 5)
        total = random.randint(fav + 2, fav + 8)
        prob = Fraction(fav, total)
        opts, ans = _shuffle_options(str(prob), [str(Fraction(1, total)), str(Fraction(fav, total + 1)), str(Fraction(total - fav, total))])
        return _mcq(6, 3, level, f"A bag has {total} balls, {fav} red. P(red) = ?", opts, ans)
    if level == "B":
        p = random.randint(1, 4)
        q = 6 - p
        opts, ans = _shuffle_options(f"{q}/6", [f"{p}/6", "1", "0"])
        return _mcq(6, 3, level, f"Fair die: P(not rolling a {p}) = ?", opts, ans, "Use complementary probability.")
    if level == "C":
        opts, ans = _shuffle_options("1/36", ["1/6", "1/12", "2/6"])
        return _mcq(6, 3, level, "Two fair dice: P(double six) = ?", opts, ans)
    if level == "D":
        red, blue = random.randint(2, 5), random.randint(2, 5)
        total = red + blue
        opts, ans = _shuffle_options(f"{blue}/{total}", [f"{red}/{total}", f"1/{total}", f"{blue}/{red}"])
        return _mcq(6, 3, level, f"A box has {red} red and {blue} blue marbles. One is picked at random. P(blue) = ?", opts, ans)
    opts, ans = _shuffle_options("Experimental may differ from 1/2", ["Experimental must equal 1/2", "Theoretical is always 0", "They are unrelated"])
    return _mcq(6, 3, level, "After 20 coin tosses you get 9 heads. Compared to theoretical P(heads):", opts, ans)


GENERATORS: dict[tuple[int, int], callable] = {
    (1, 1): _gen_p1_t1, (1, 2): _gen_p1_t2, (1, 3): _gen_p1_t3, (1, 4): _gen_p1_t4, (1, 5): _gen_p1_t5,
    (2, 1): _gen_p2_t1, (2, 2): _gen_p2_t2, (2, 3): _gen_p2_t3, (2, 4): _gen_p2_t4,
    (2, 5): _gen_p2_t5, (2, 6): _gen_p2_t6, (2, 7): _gen_p2_t7,
    (3, 1): _gen_p3_t1, (3, 2): _gen_p3_t2,
    (4, 1): _gen_p4_t1, (4, 2): _gen_p4_t2, (4, 3): _gen_p4_t3, (4, 4): _gen_p4_t4,
    (5, 1): _gen_p5_t1, (5, 2): _gen_p5_t2, (5, 3): _gen_p5_t3,
    (6, 1): _gen_p6_t1, (6, 2): _gen_p6_t2, (6, 3): _gen_p6_t3,
}


def generate_question(
    prereq_id: int,
    topic_id: int,
    level: str,
    *,
    exclude_ids: set[str] | None = None,
    exclude_text: set[str] | None = None,
    templates_only: bool = False,
) -> dict | None:
    import harshit_chapter_questions as hcq

    if not templates_only:
        q = hcq.pick_question(
            prereq_id,
            topic_id,
            level,
            exclude_ids=exclude_ids,
            exclude_text=exclude_text,
        )
        if q:
            return q

    fn = GENERATORS.get((prereq_id, topic_id))
    if not fn:
        return None
    if level not in TOPICS.get(prereq_id, {}).get(topic_id, {}).get("levels", {}):
        return None
    exclude_ids = exclude_ids or set()
    exclude_text = exclude_text or set()
    for _ in range(16):
        try:
            q = fn(level)
        except Exception:
            return None
        if not q:
            continue
        text = str(q.get("question", "")).strip()
        if hcq.is_question_excluded(q, exclude_ids=exclude_ids, exclude_text=exclude_text):
            continue
        return q
    return None
