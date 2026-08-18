"""NCERT Class 9 PreReq topics, difficulty levels, and question generators."""

from __future__ import annotations

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
            "name": "Linear Equations (Two Variables)",
            "short": "Linear 2-var",
            "emoji": "📈",
            "levels": {
                "A": "Find y given x",
                "B": "Find x given y",
                "C": "Table completion",
                "D": "Graph from equation",
                "E": "Word problems",
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
    if config.get("use_llm"):
        lines.append("  • AI generation: on")
    return "\n".join(lines) if lines else "No topics selected."


def _mcq(
    prereq_id: int,
    topic_id: int,
    level: str,
    question: str,
    options: list[str],
    answer: int,
    explanation: str = "",
) -> dict:
    return {
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


def _shuffle_options(correct: str, wrong: list[str]) -> tuple[list[str], int]:
    opts = [correct] + wrong[:3]
    random.shuffle(opts)
    return opts, opts.index(correct)


# ── Unit 1 generators ──


def _gen_p1_t1(level: str) -> dict:
    if level in ("A", "B"):
        a, b = random.randint(-9, 9), random.randint(-9, 9)
        while a == b:
            b = random.randint(-9, 9)
        farther = a if abs(a) > abs(b) else b
        opts, ans = _shuffle_options(str(farther), [str(a), str(b), str(-farther)])
        return _mcq(1, 1, level, f"Which is farther from zero: {a} or {b}?", opts, ans, f"|{farther}| is larger.")
    x, y = random.randint(1, 8), random.randint(1, 8)
    opts, ans = _shuffle_options(str(x - y), [str(x + y), str(-x - y), str(y - x)])
    return _mcq(1, 1, level, f"Compute: {x} − ({y})", opts, ans)


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
    return _mcq(1, 3, level, f"Evaluate: {n}^{{-2}}", opts, ans)


def _gen_p1_t4(level: str) -> dict:
    n = random.choice([2, 3, 5])
    opts, ans = _shuffle_options(f"√{n}/n", [f"1/√{n}", f"{n}/√{n}", f"√{n}"])
    return _mcq(1, 4, level, f"Rationalize: 1/√{n} = ?", opts, ans, "Multiply numerator and denominator by √{n}.")


def _gen_p1_t5(level: str) -> dict:
    choices = [("√4", "Rational"), ("√2", "Irrational"), ("22/7", "Rational"), ("0.1010010001…", "Irrational")]
    q, correct = random.choice(choices)
    wrong = [c for _, c in choices if c != correct]
    opts, ans = _shuffle_options(correct, wrong)
    return _mcq(1, 5, level, f"Classify: {q}", opts, ans)


# ── Unit 2 generators ──


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
    m, c = random.randint(1, 5), random.randint(-3, 3)
    x = random.randint(1, 4)
    y = m * x + c
    opts, ans = _shuffle_options(str(y), [str(m * x), str(x + c), str(y + 1)])
    return _mcq(2, 4, level, f"If y = {m}x + {c}, find y when x = {x}.", opts, ans)


# ── Unit 3 generators ──


def _gen_p3_t1(level: str) -> dict:
    pts = [(3, 4), (-2, 5), (-4, -1), (2, -3)]
    x, y = random.choice(pts)
    quad = "I" if x > 0 and y > 0 else "II" if x < 0 and y > 0 else "III" if x < 0 and y < 0 else "IV"
    opts, ans = _shuffle_options(quad, ["I", "II", "III", "IV"])
    return _mcq(3, 1, level, f"Point ({x}, {y}) lies in Quadrant?", opts, ans)


def _gen_p3_t2(level: str) -> dict:
    m, c = random.randint(1, 4), random.randint(-2, 3)
    opts, ans = _shuffle_options(f"y = {m}x + {c}", [f"y = {c}x + {m}", f"x = {m}y + {c}", f"y = {m}x − {c}"])
    return _mcq(3, 2, level, f"Which equation has slope {m} and y-intercept {c}?", opts, ans)


# ── Unit 4 generators ──


def _gen_p4_t1(level: str) -> dict:
    angle = random.randint(20, 70)
    sup = 180 - angle
    opts, ans = _shuffle_options(f"{sup}°", [f"{angle}°", f"{90-angle}°", f"{angle+90}°"])
    return _mcq(4, 1, level, f"An angle measures {angle}°. Its supplement is?", opts, ans)


def _gen_p4_t2(level: str) -> dict:
    opts, ans = _shuffle_options("180°", ["90°", "360°", "270°"])
    return _mcq(4, 2, level, "Sum of angles in a triangle is?", opts, ans)


def _gen_p4_t3(level: str) -> dict:
    opts, ans = _shuffle_options("Opposite sides parallel", ["All sides equal", "Diagonals perpendicular", "One pair parallel"])
    return _mcq(4, 3, level, "A parallelogram always has:", opts, ans)


def _gen_p4_t4(level: str) -> dict:
    opts, ans = _shuffle_options("Equal chords subtend equal angles at centre", ["Chord = radius", "Tangent ⊥ radius", "Angle in semicircle = 90°"])
    return _mcq(4, 4, level, "Which is true for a circle?", opts, ans)


# ── Unit 5 generators ──


def _gen_p5_t1(level: str) -> dict:
    a, b, c = 3, 4, 5
    s = (a + b + c) / 2
    import math
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    opts, ans = _shuffle_options("6", ["12", "7.5", "10"])
    return _mcq(5, 1, level, f"Area of triangle with sides 3, 4, 5 (Heron)?", opts, ans)


def _gen_p5_t2(level: str) -> dict:
    l, w, h = random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)
    sa = 2 * (l * w + w * h + h * l)
    opts, ans = _shuffle_options(f"{sa}", [f"{l*w*h}", f"{l+w+h}", f"{sa+2}"])
    return _mcq(5, 2, level, f"Total surface area of cuboid {l}×{w}×{h}?", opts, ans)


def _gen_p5_t3(level: str) -> dict:
    l, w, h = random.randint(2, 4), random.randint(2, 4), random.randint(2, 4)
    vol = l * w * h
    opts, ans = _shuffle_options(f"{vol}", [f"{l+w+h}", f"{2*(l*w)}", f"{vol+1}"])
    return _mcq(5, 3, level, f"Volume of cuboid {l}×{w}×{h}?", opts, ans)


# ── Unit 6 generators ──


def _gen_p6_t1(level: str) -> dict:
    data = [random.randint(1, 9) for _ in range(5)]
    mean = sum(data) / len(data)
    correct = str(mean) if mean == int(mean) else f"{mean:.1f}"
    opts, ans = _shuffle_options(correct, [str(int(mean) + 1), str(max(data)), str(min(data))])
    return _mcq(6, 1, level, f"Mean of {data}?", opts, ans)


def _gen_p6_t2(level: str) -> dict:
    opts, ans = _shuffle_options("Histogram", ["Pie chart only", "Line graph", "Scatter plot"])
    return _mcq(6, 2, level, "Best graph for grouped continuous data?", opts, ans)


def _gen_p6_t3(level: str) -> dict:
    opts, ans = _shuffle_options("1/2", ["1/4", "1/6", "2/3"])
    return _mcq(6, 3, level, "Fair coin: P(heads)?", opts, ans)


GENERATORS: dict[tuple[int, int], callable] = {
    (1, 1): _gen_p1_t1, (1, 2): _gen_p1_t2, (1, 3): _gen_p1_t3, (1, 4): _gen_p1_t4, (1, 5): _gen_p1_t5,
    (2, 1): _gen_p2_t1, (2, 2): _gen_p2_t2, (2, 3): _gen_p2_t3, (2, 4): _gen_p2_t4,
    (3, 1): _gen_p3_t1, (3, 2): _gen_p3_t2,
    (4, 1): _gen_p4_t1, (4, 2): _gen_p4_t2, (4, 3): _gen_p4_t3, (4, 4): _gen_p4_t4,
    (5, 1): _gen_p5_t1, (5, 2): _gen_p5_t2, (5, 3): _gen_p5_t3,
    (6, 1): _gen_p6_t1, (6, 2): _gen_p6_t2, (6, 3): _gen_p6_t3,
}


def generate_question(prereq_id: int, topic_id: int, level: str) -> dict | None:
    fn = GENERATORS.get((prereq_id, topic_id))
    if not fn:
        return None
    if level not in TOPICS.get(prereq_id, {}).get(topic_id, {}).get("levels", {}):
        return None
    try:
        return fn(level)
    except Exception:
        return None
