"""Class 10 unit topics, difficulty levels, and question generators."""

from __future__ import annotations

import math
import random
import uuid
from fractions import Fraction

LEVEL_ORDER = ["A", "B", "C", "D", "E"]

DIFFICULTY_LABELS = {
    1: "Foundation (Level A)",
    2: "Build (Level B)",
    3: "Standard (Level C)",
    4: "Stretch (Level D)",
    5: "Challenge (Level E)",
}

DIFFICULTY_TO_LEVEL = {i: LEVEL_ORDER[i - 1] for i in range(1, 6)}

# unit_id -> topic_id -> metadata
TOPICS: dict[int, dict[int, dict]] = {
    1: {
        1: {
            "name": "Prime Factorisation & FTA",
            "short": "FTA",
            "emoji": "🔢",
            "levels": {
                "A": "Identify primes and composite numbers",
                "B": "Prime factorise small integers",
                "C": "Write numbers as powers of primes",
                "D": "Apply uniqueness of prime factorisation",
                "E": "Reason about digits of powers (e.g. 4^n)",
            },
        },
        2: {
            "name": "HCF and LCM",
            "short": "HCF/LCM",
            "emoji": "🔗",
            "levels": {
                "A": "HCF or LCM of two small numbers",
                "B": "Use prime factorisation for HCF/LCM",
                "C": "Verify HCF × LCM = product (two numbers)",
                "D": "HCF/LCM of three integers",
                "E": "LCM word problems (meet again)",
            },
        },
        3: {
            "name": "Irrational Numbers",
            "short": "Irrational",
            "emoji": "∞",
            "levels": {
                "A": "Classify rational vs irrational",
                "B": "Theorem 1.2: prime divides square",
                "C": "Proof by contradiction — first step",
                "D": "√p is irrational (p prime)",
                "E": "Prove expressions like 5 − √3 irrational",
            },
        },
        4: {
            "name": "Rationals & Irrationals Together",
            "short": "Combine",
            "emoji": "➕",
            "levels": {
                "A": "Sum/product of rational and irrational",
                "B": "Identify composite expressions",
                "C": "Show 3√2 is irrational",
                "D": "Combined irrational proofs",
                "E": "Multi-step reasoning from NCERT Ex 1.2",
            },
        },
    },
    2: {
        1: {
            "name": "Types & Degree of Polynomials",
            "short": "Degree",
            "emoji": "📐",
            "levels": {
                "A": "Identify degree of a polynomial",
                "B": "Classify linear, quadratic, cubic",
                "C": "Leading coefficient and terms",
                "D": "General form ax² + bx + c (a ≠ 0)",
                "E": "Recognise expressions that are not polynomials",
            },
        },
        2: {
            "name": "Geometrical Meaning of Zeroes",
            "short": "Zeroes",
            "emoji": "📈",
            "levels": {
                "A": "Zero of a linear polynomial",
                "B": "How many zeroes can a quadratic have?",
                "C": "x-intercepts and zeroes of p(x)",
                "D": "Graph touches or crosses the x-axis",
                "E": "Repeated zero / single x-intercept",
            },
        },
        3: {
            "name": "Zeroes & Coefficients",
            "short": "Coeff",
            "emoji": "🔗",
            "levels": {
                "A": "Sum of zeroes (quadratic)",
                "B": "Product of zeroes (quadratic)",
                "C": "Form quadratic from sum and product",
                "D": "Relations for ax² + bx + c",
                "E": "Find unknown coefficient from a given zero",
            },
        },
        4: {
            "name": "Division Algorithm",
            "short": "Divide",
            "emoji": "➗",
            "levels": {
                "A": "Remainder when dividing by (x − a)",
                "B": "Check whether (x − a) is a factor",
                "C": "Remainder theorem for quadratics",
                "D": "Find a zero using the factor theorem",
                "E": "Find missing coefficient using a factor",
            },
        },
    },
    3: {
        1: {
            "name": "Graphical Method & Consistency",
            "short": "Graph",
            "emoji": "📊",
            "levels": {
                "A": "Intersecting vs parallel lines",
                "B": "Unique, none, or infinitely many solutions",
                "C": "Consistent and inconsistent pairs",
                "D": "Coincident lines",
                "E": "Compare ratios a₁/a₂, b₁/b₂, c₁/c₂",
            },
        },
        2: {
            "name": "Substitution Method",
            "short": "Subst",
            "emoji": "🔄",
            "levels": {
                "A": "Solve simple pair (small integers)",
                "B": "Express one variable and substitute",
                "C": "Find x after substitution",
                "D": "Find y after substitution",
                "E": "Substitution with fractions/coefficients",
            },
        },
        3: {
            "name": "Elimination Method",
            "short": "Elim",
            "emoji": "➖",
            "levels": {
                "A": "Add/subtract equations to eliminate",
                "B": "Make coefficients equal then eliminate",
                "C": "Solve for x",
                "D": "Solve for y",
                "E": "Elimination with scaled equations",
            },
        },
        4: {
            "name": "Cross-Multiplication & Applications",
            "short": "Cross",
            "emoji": "✖️",
            "levels": {
                "A": "Cross-multiplication formula",
                "B": "Apply cross-multiplication",
                "C": "Age / number word problems",
                "D": "Fraction and digit problems",
                "E": "Multi-step application problems",
            },
        },
    },
    4: {
        1: {
            "name": "Standard Form & Roots",
            "short": "Standard",
            "emoji": "🎯",
            "levels": {
                "A": "Identify a, b, c in ax² + bx + c = 0",
                "B": "Verify whether a value is a root",
                "C": "Write quadratic from given roots",
                "D": "Number of roots of a quadratic",
                "E": "Form equation from sum/product of roots",
            },
        },
        2: {
            "name": "Factorisation Method",
            "short": "Factor",
            "emoji": "🧩",
            "levels": {
                "A": "Split middle term (monic)",
                "B": "Factorise and write roots",
                "C": "Solve by factorisation",
                "D": "Factorise with common factor first",
                "E": "Rearrange to standard form then factor",
            },
        },
        3: {
            "name": "Quadratic Formula",
            "short": "Formula",
            "emoji": "√",
            "levels": {
                "A": "State the quadratic formula",
                "B": "Compute discriminant before solving",
                "C": "Find roots using formula (integer roots)",
                "D": "Find roots (rational / surd form)",
                "E": "Choose appropriate method",
            },
        },
        4: {
            "name": "Discriminant & Nature of Roots",
            "short": "Disc",
            "emoji": "Δ",
            "levels": {
                "A": "Compute Δ = b² − 4ac",
                "B": "Nature of roots from Δ",
                "C": "Find k for equal roots",
                "D": "Find k for distinct real roots",
                "E": "Find k for no real roots",
            },
        },
    },
    5: {
        1: {
            "name": "Patterns & Definition of AP",
            "short": "AP Def",
            "emoji": "📈",
            "levels": {
                "A": "Recognise a constant difference pattern",
                "B": "Find common difference d",
                "C": "Decide if a list is an AP",
                "D": "Write the next term(s)",
                "E": "Finite vs infinite AP; general form a, a+d, …",
            },
        },
        2: {
            "name": "nth Term of an AP",
            "short": "nth",
            "emoji": "🔢",
            "levels": {
                "A": "State aₙ = a + (n − 1)d",
                "B": "Find a specific term (e.g. 10th)",
                "C": "Find n when a term value is given",
                "D": "Find a and d from two given terms",
                "E": "Term from the end / two-digit divisible problems",
            },
        },
        3: {
            "name": "Sum of First n Terms",
            "short": "Sum",
            "emoji": "➕",
            "levels": {
                "A": "State Sₙ = n/2 [2a + (n−1)d]",
                "B": "Sum of first n terms (integer AP)",
                "C": "Use Sₙ = n/2 (a + l) when last term known",
                "D": "Find n when sum is given",
                "E": "Pick the right sum formula",
            },
        },
        4: {
            "name": "Applications & Word Problems",
            "short": "Apps",
            "emoji": "🌱",
            "levels": {
                "A": "Salary / savings increment stories",
                "B": "Rows of plants, seats, or rungs",
                "C": "Simple interest forming an AP",
                "D": "Find number of terms from context",
                "E": "Multi-step board-style mixed problems",
            },
        },
    },
    6: {
        1: {
            "name": "Similar Figures & Scale Factor",
            "short": "Similar",
            "emoji": "🔺",
            "levels": {
                "A": "Congruent vs similar figures",
                "B": "Scale factor between similar figures",
                "C": "Corresponding sides in the same ratio",
                "D": "Find missing side using scale factor",
                "E": "Conditions for similar polygons",
            },
        },
        2: {
            "name": "Basic Proportionality Theorem (BPT)",
            "short": "BPT",
            "emoji": "📏",
            "levels": {
                "A": "State BPT (Thales Theorem 6.1)",
                "B": "Find a divided segment (AD/DB = AE/EC)",
                "C": "Use BPT when DE ∥ BC",
                "D": "Converse: line parallel to third side?",
                "E": "BPT in trapezium / combined ratios",
            },
        },
        3: {
            "name": "Similarity Criteria (AAA, SSS, SAS)",
            "short": "Criteria",
            "emoji": "△",
            "levels": {
                "A": "AAA / AA similarity",
                "B": "SSS similarity — sides proportional",
                "C": "SAS similarity — included angle",
                "D": "Pick the correct criterion",
                "E": "Find unknown side using similarity",
            },
        },
        4: {
            "name": "Pythagoras & Applications",
            "short": "Apps",
            "emoji": "📐",
            "levels": {
                "A": "Pythagoras theorem in right triangles",
                "B": "Proof idea via similar triangles",
                "C": "Indirect measurement (shadow / height)",
                "D": "Area ratio of similar triangles",
                "E": "Multi-step board-style geometry",
            },
        },
    },
    7: {
        1: {
            "name": "Distance Formula",
            "short": "Distance",
            "emoji": "📏",
            "levels": {
                "A": "State distance formula between two points",
                "B": "Distance on x-axis or y-axis",
                "C": "Distance between two general points",
                "D": "Distance with Pythagoras setup",
                "E": "Perimeter using distance formula",
            },
        },
        2: {
            "name": "Section Formula",
            "short": "Section",
            "emoji": "✂️",
            "levels": {
                "A": "Internal division in ratio m : n",
                "B": "Coordinates of dividing point",
                "C": "Mid-point as special case",
                "D": "Find ratio from given coordinates",
                "E": "Section formula word problems",
            },
        },
        3: {
            "name": "Collinearity & Verification",
            "short": "Collinear",
            "emoji": "📍",
            "levels": {
                "A": "Three points collinear — idea",
                "B": "Check collinearity using distances",
                "C": "Area of triangle from coordinates",
                "D": "Find unknown coordinate for collinearity",
                "E": "Verify quadrilateral type from vertices",
            },
        },
        4: {
            "name": "Coordinate Applications",
            "short": "Apps",
            "emoji": "🗺️",
            "levels": {
                "A": "Town on a grid — east/north distance",
                "B": "Find vertex of a triangle",
                "C": "Centroid / special point (mid-point chain)",
                "D": "Combined distance and section",
                "E": "Multi-step board-style coordinate problems",
            },
        },
    },
    8: {
        1: {
            "name": "Trigonometric Ratios",
            "short": "Ratios",
            "emoji": "📐",
            "levels": {
                "A": "sin, cos, tan in a right triangle",
                "B": "cosec, sec, cot definitions",
                "C": "Express ratios from sides",
                "D": "Find side using a ratio",
                "E": "Reciprocal and quotient relations",
            },
        },
        2: {
            "name": "Ratios of Specific Angles",
            "short": "Angles",
            "emoji": "🎯",
            "levels": {
                "A": "Values at 0°, 30°, 45°, 60°, 90°",
                "B": "Table of standard angles",
                "C": "Evaluate simple expressions",
                "D": "Complementary angle relations",
                "E": "Pick correct value from options",
            },
        },
        3: {
            "name": "Trigonometric Identities",
            "short": "Identities",
            "emoji": "🆔",
            "levels": {
                "A": "sin²θ + cos²θ = 1",
                "B": "1 + tan²θ = sec²θ",
                "C": "1 + cot²θ = cosec²θ",
                "D": "Simplify using identities",
                "E": "Prove simple identity steps",
            },
        },
        4: {
            "name": "Mixed Trigonometry",
            "short": "Mixed",
            "emoji": "🔀",
            "levels": {
                "A": "Express tan in sin and cos",
                "B": "Evaluate (sin 30° + cos 60°) type",
                "C": "Simplify (1 − sin²θ) expressions",
                "D": "Identity + specific angle combined",
                "E": "Board-style multi-step simplification",
            },
        },
    },
    9: {
        1: {
            "name": "Angle of Elevation & Depression",
            "short": "Angles",
            "emoji": "👁️",
            "levels": {
                "A": "Line of sight and horizontal",
                "B": "Elevation vs depression",
                "C": "Identify angle in a diagram",
                "D": "Two angles in same figure",
                "E": "Convert between elevation and depression",
            },
        },
        2: {
            "name": "Heights Using Trigonometry",
            "short": "Heights",
            "emoji": "🏗️",
            "levels": {
                "A": "Height = distance × tan θ",
                "B": "Tower / minar height problems",
                "C": "Height with observer eye-level",
                "D": "Two-stage height (balloon / cliff)",
                "E": "Multi-step height problems",
            },
        },
        3: {
            "name": "Distances Using Trigonometry",
            "short": "Distance",
            "emoji": "🌉",
            "levels": {
                "A": "Width of river / gap",
                "B": "Distance from tan and height",
                "C": "Boat / ladder distance",
                "D": "Find distance with two angles",
                "E": "Combined height and distance",
            },
        },
        4: {
            "name": "Applications & Word Problems",
            "short": "Apps",
            "emoji": "🏔️",
            "levels": {
                "A": "Single right triangle setup",
                "B": "Shadow length problems",
                "C": "Building across a river",
                "D": "Aeroplane / lighthouse problems",
                "E": "Board-style mixed applications",
            },
        },
    },
    10: {
        1: {
            "name": "Tangent to a Circle",
            "short": "Tangent",
            "emoji": "⭕",
            "levels": {
                "A": "Tangent touches circle at one point",
                "B": "Radius ⊥ tangent (Theorem 10.1)",
                "C": "Tangent vs secant vs non-intersecting",
                "D": "Find length using ⊥ radius",
                "E": "Pythagoras in tangent-radius triangle",
            },
        },
        2: {
            "name": "Tangents from an External Point",
            "short": "External",
            "emoji": "📍",
            "levels": {
                "A": "No tangent from inside; one on circle",
                "B": "Two tangents from outside (Case 3)",
                "C": "Equal tangent lengths (Theorem 10.2)",
                "D": "Angle between tangents",
                "E": "External point — count tangents",
            },
        },
        3: {
            "name": "Length of Tangent",
            "short": "Length",
            "emoji": "📏",
            "levels": {
                "A": "Length = √(OP² − r²)",
                "B": "Find tangent length from P",
                "C": "Find radius or OP",
                "D": "Concentric circles — chord as tangent",
                "E": "Multi-step tangent length",
            },
        },
        4: {
            "name": "Circle Applications & Proofs",
            "short": "Apps",
            "emoji": "🔧",
            "levels": {
                "A": "Identify tangent in a diagram",
                "B": "Prove equal tangents (idea)",
                "C": "Chord bisected at point of contact",
                "D": "∠PTQ and ∠OPQ relation",
                "E": "Board-style combined circle proofs",
            },
        },
    },
    11: {
        1: {
            "name": "Sector Area",
            "short": "Sector",
            "emoji": "🥧",
            "levels": {
                "A": "Sector area formula (θ/360)πr²",
                "B": "Find sector area given r and θ",
                "C": "Find angle from sector area",
                "D": "Semicircle and quadrant areas",
                "E": "Multi-step sector problems",
            },
        },
        2: {
            "name": "Arc Length",
            "short": "Arc",
            "emoji": "〰️",
            "levels": {
                "A": "Arc length formula (θ/360)2πr",
                "B": "Find arc length given r and θ",
                "C": "Find radius or angle from arc",
                "D": "Perimeter of sector",
                "E": "Combined arc length problems",
            },
        },
        3: {
            "name": "Segment Area",
            "short": "Segment",
            "emoji": "🌙",
            "levels": {
                "A": "Segment = sector − triangle",
                "B": "Minor segment area (60°, 90°)",
                "C": "Major vs minor segment",
                "D": "Segment with chord given",
                "E": "Board-style segment area",
            },
        },
        4: {
            "name": "Combined Circle Figures",
            "short": "Combine",
            "emoji": "🔵",
            "levels": {
                "A": "Square + quarter circles",
                "B": "Shaded region between circles",
                "C": "Wheel / brooch design areas",
                "D": "Area of ring (annulus)",
                "E": "Mixed mensuration applications",
            },
        },
    },
    12: {
        1: {
            "name": "Cylinder, Cone & Sphere Formulas",
            "short": "Formulas",
            "emoji": "📐",
            "levels": {
                "A": "Identify SA/volume formula",
                "B": "Cylinder CSA and volume",
                "C": "Cone and hemisphere SA/volume",
                "D": "Sphere surface area and volume",
                "E": "Compare dimensions from SA/volume",
            },
        },
        2: {
            "name": "Combination Surface Area",
            "short": "Combo SA",
            "emoji": "📦",
            "levels": {
                "A": "Which faces to include/exclude",
                "B": "Cylinder + hemisphere (toy)",
                "C": "Cone on cylinder — visible SA",
                "D": "Hollow cylinder SA",
                "E": "Board-style combination SA",
            },
        },
        3: {
            "name": "Combination Volume",
            "short": "Combo Vol",
            "emoji": "🧊",
            "levels": {
                "A": "Add volumes of solids",
                "B": "Volume of toy (cone + hemisphere)",
                "C": "Hollow solid volume",
                "D": "Water displaced / capacity",
                "E": "Multi-solid volume problems",
            },
        },
        4: {
            "name": "Frustum & Board Applications",
            "short": "Frustum",
            "emoji": "🪣",
            "levels": {
                "A": "Frustum — what is it?",
                "B": "Bucket / glass (frustum) volume idea",
                "C": "Conversion: melt and recast",
                "D": "Ratio of volumes of similar solids",
                "E": "Board-style SA/volume applications",
            },
        },
    },
    13: {
        1: {
            "name": "Mean of Grouped Data",
            "short": "Mean",
            "emoji": "📊",
            "levels": {
                "A": "Class mark xi for an interval",
                "B": "Direct method: Σfixi / Σfi",
                "C": "Assumed mean method",
                "D": "Step-deviation method",
                "E": "Find missing frequency from mean",
            },
        },
        2: {
            "name": "Median",
            "short": "Median",
            "emoji": "📈",
            "levels": {
                "A": "Median class from cumulative frequency",
                "B": "Median formula components",
                "C": "Compute median from grouped data",
                "D": "Compare mean and median",
                "E": "Missing frequency using median",
            },
        },
        3: {
            "name": "Mode",
            "short": "Mode",
            "emoji": "🔝",
            "levels": {
                "A": "Modal class identification",
                "B": "Mode formula: l + ((f1−f0)/(2f1−f0−f2))h",
                "C": "Compute mode from grouped data",
                "D": "Empirical relation 3 median − 2 mean",
                "E": "Board-style mode problems",
            },
        },
        4: {
            "name": "Ogive & Cumulative Frequency",
            "short": "Ogive",
            "emoji": "📉",
            "levels": {
                "A": "Less-than vs more-than ogive",
                "B": "Build cumulative frequency table",
                "C": "Read median from ogive intersection",
                "D": "Interpret ogive graph",
                "E": "Mixed statistics from tables/graphs",
            },
        },
    },
    14: {
        1: {
            "name": "Classical Probability",
            "short": "Classical",
            "emoji": "🎯",
            "levels": {
                "A": "P(E) = favourable / total outcomes",
                "B": "Probability of simple events",
                "C": "Impossible and certain events",
                "D": "Equally likely outcomes",
                "E": "Multi-outcome classical probability",
            },
        },
        2: {
            "name": "Complementary Events",
            "short": "Complement",
            "emoji": "↔️",
            "levels": {
                "A": "P(E') = 1 − P(E)",
                "B": "Not E from given P(E)",
                "C": "At least one vs none",
                "D": "Complement in word problems",
                "E": "Combined complement reasoning",
            },
        },
        3: {
            "name": "Cards & Dice",
            "short": "Cards/Dice",
            "emoji": "🃏",
            "levels": {
                "A": "Single die — one outcome",
                "B": "Two dice — sum probabilities",
                "C": "Drawing one card from deck",
                "D": "Face cards / red cards / ace",
                "E": "Board-style card and dice problems",
            },
        },
        4: {
            "name": "Mixed Probability",
            "short": "Mixed",
            "emoji": "🎲",
            "levels": {
                "A": "Bag of coloured balls",
                "B": "Two draws without replacement",
                "C": "Geometric probability (region)",
                "D": "Word problems — coins and bags",
                "E": "Board-style mixed probability",
            },
        },
    },
}


def topics_for_unit(unit_id: int) -> dict[int, dict]:
    return TOPICS.get(unit_id, {})


def default_week_config(unit_id: int) -> dict:
    import harshit_class10_units as h10u

    topics = topics_for_unit(unit_id)
    unit = h10u.get_unit(unit_id)
    title = unit["title"] if unit else f"Unit {unit_id}"
    return {
        "week_label": f"{title} — Week 1",
        "topics": [{"id": tid, "levels": ["B", "C"]} for tid in sorted(topics)],
        "practice_difficulty": 3,
        "use_chapter_llm": True,
        "grok_fresh_only": False,
        "unit_id": unit_id,
    }


def format_week_plan_summary(unit_id: int, config: dict) -> str:
    lines = []
    if config.get("week_label"):
        lines.append(f"Week: {config['week_label']}")
    for item in config.get("topics", []):
        tid = int(item["id"])
        info = TOPICS.get(unit_id, {}).get(tid, {})
        lvls = ", ".join(item.get("levels", []))
        lines.append(f"  • {info.get('name', tid)} [{lvls}]")
    if config.get("use_chapter_llm"):
        mode = "all fresh from Grok" if config.get("grok_fresh_only") else "Grok + bank fallback"
        lines.append(f"  • xAI (Grok): on ({mode})")
    else:
        lines.append("  • xAI (Grok): off — templates & bank only")
    return "\n".join(lines) if lines else "No topics selected."


def format_topic_level_label(unit_id: int, topic_id: int, level: str) -> str:
    info = TOPICS.get(unit_id, {}).get(topic_id, {})
    return f"{info.get('short', topic_id)} · Level {level}"


def _chapter_ref(unit_id: int) -> str:
    return {
        1: "NCERT Ch 1 Real Numbers",
        2: "NCERT Ch 2 Polynomials",
        3: "NCERT Ch 3 Pair of Linear Equations",
        4: "NCERT Ch 4 Quadratic Equations",
        5: "NCERT Ch 5 Arithmetic Progressions",
        6: "NCERT Ch 6 Triangles",
        7: "NCERT Ch 7 Coordinate Geometry",
        8: "NCERT Ch 8 Introduction to Trigonometry",
        9: "NCERT Ch 9 Applications of Trigonometry",
        10: "NCERT Ch 10 Circles",
        11: "NCERT Ch 11 Areas Related to Circles",
        12: "NCERT Ch 12 Surface Areas and Volumes",
        13: "NCERT Ch 13 Statistics",
        14: "NCERT Ch 14 Probability",
    }.get(unit_id, f"NCERT Unit {unit_id}")


def _mcq(
    unit_id: int,
    topic_id: int,
    level: str,
    question: str,
    options: list[str],
    answer: int,
    explanation: str = "",
) -> dict:
    return {
        "id": f"u{unit_id}_t{topic_id}_{level}_{uuid.uuid4().hex[:8]}",
        "question": question,
        "options": options,
        "answer": answer,
        "topic": topic_id,
        "level": level,
        "unit_id": unit_id,
        "category": f"u{unit_id}_t{topic_id}_{level}",
        "category_label": format_topic_level_label(unit_id, topic_id, level),
        "explanation": explanation,
        "source": "template",
        "chapter_ref": _chapter_ref(unit_id),
    }


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
    while len(unique_wrong) < 3:
        filler = f"{correct} (alt)"
        if filler not in seen:
            seen.add(filler)
            unique_wrong.append(filler)
        else:
            unique_wrong.append(f"{int(correct) + len(unique_wrong) + 1}" if correct.isdigit() else "None of these")
    opts = [correct, *unique_wrong[:3]]
    random.shuffle(opts)
    return opts, opts.index(correct)


def _prime_factors(n: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    d = 2
    x = n
    while d * d <= x:
        while x % d == 0:
            factors[d] = factors.get(d, 0) + 1
            x //= d
        d += 1 if d == 2 else 2
    if x > 1:
        factors[x] = factors.get(x, 0) + 1
    return factors


def _factor_string(n: int) -> str:
    fac = _prime_factors(n)
    parts = []
    for p in sorted(fac):
        exp = fac[p]
        parts.append(str(p) if exp == 1 else f"{p}^{exp}")
    return " × ".join(parts)


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def _random_composite(lo: int = 12, hi: int = 999) -> int:
    for _ in range(200):
        n = random.randint(lo, hi)
        if not _is_prime(n) and n > 1:
            return n
    return 12


def _random_pair() -> tuple[int, int]:
    return random.randint(6, 120), random.randint(6, 120)


# ── Unit 1 generators ──


def _gen_u1_t1(level: str) -> dict:
    if level == "A":
        if random.random() < 0.5:
            n = random.choice([p for p in range(11, 97) if _is_prime(p)])
            label, wrong = "Prime", ["Composite", "Even only", "Neither"]
            expl = f"{n} has no divisors other than 1 and itself."
        else:
            n = _random_composite(4, 99)
            label, wrong = "Composite", ["Prime", "Odd only", "Neither"]
            expl = f"{n} has more than two positive divisors."
        opts, ans = _shuffle_options(label, wrong)
        return _mcq(1, 1, level, f"Is {n} a prime number?", opts, ans, expl)
    if level == "B":
        n = _random_composite(12, 99)
        correct = _factor_string(n)
        wrong = [_factor_string(n + 1), _factor_string(n - 1 if n > 12 else n + 2), str(n)]
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(1, 1, level, f"Prime factorisation of {n}?", opts, ans)
    if level == "C":
        n = random.choice([140, 156, 180, 225, 360, 3825, 5005, 7429, 32760, 420, 504, 630])
        correct = _factor_string(n)
        alt = n // 2 if n % 2 == 0 else n + 11
        opts, ans = _shuffle_options(correct, [_factor_string(alt), _factor_string(n + 13), "2 × 3 × 5"])
        return _mcq(1, 1, level, f"Write {n} as a product of powers of primes.", opts, ans)
    if level == "D":
        n = _random_composite(24, 720)
        opts, ans = _shuffle_options("Exactly one (apart from order)", ["Infinitely many", "Two only", "None"])
        return _mcq(
            1, 1, level,
            f"By the Fundamental Theorem of Arithmetic, how many prime factorisations does {n} have?",
            opts, ans,
        )
    base = random.choice([4, 6, 8, 9, 12, 16])
    ends_zero = base % 10 == 0 or (base % 2 == 0 and base % 5 == 0)
    if base in (4, 6, 8, 9, 12, 16):
        ends_zero = False
    answer = "Yes" if ends_zero else "No"
    opts, ans = _shuffle_options(answer, ["No", "Yes", "Only when n is even"] if answer == "Yes" else ["Yes", "Only when n is even", "Only when n is a multiple of 5"])
    return _mcq(
        1, 1, level,
        f"Can {base}^n end with the digit 0 for any natural number n?",
        opts, ans,
        f"{base}^n needs prime factor 5 in its factorisation to end in 0.",
    )


def _gen_u1_t2(level: str) -> dict:
    if level == "A":
        a, b = _random_pair()
        if random.random() < 0.5:
            val = math.gcd(a, b)
            label = f"HCF({a}, {b}) = ?"
        else:
            val = a * b // math.gcd(a, b)
            label = f"LCM({a}, {b}) = ?"
        opts, ans = _shuffle_options(str(val), [str(a + b), str(a * b), str(val + 3)])
        return _mcq(1, 2, level, label, opts, ans)
    if level == "B":
        a, b = _random_pair()
        if random.random() < 0.5:
            val = math.gcd(a, b)
            label = f"HCF({a}, {b}) = ?"
        else:
            val = a * b // math.gcd(a, b)
            label = f"LCM({a}, {b}) = ?"
        opts, ans = _shuffle_options(str(val), [str(a + b), str(abs(a - b)), str(val + 5)])
        return _mcq(1, 2, level, label, opts, ans)
    if level == "C":
        a, b = _random_pair()
        hcf = math.gcd(a, b)
        lcm = a * b // hcf
        if random.random() < 0.5:
            correct, expl = str(a * b), "HCF(a,b) × LCM(a,b) = a × b for two positive integers."
            wrong = [str(hcf + lcm), str(hcf * lcm), str(lcm - hcf)]
            qtext = f"For {a} and {b}, HCF × LCM equals?"
        else:
            correct, expl = str(hcf), "HCF uses the smallest power of each common prime."
            wrong = [str(lcm), str(a + b), str(hcf + 2)]
            qtext = f"HCF({a}, {b}) using prime factorisation equals?"
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(1, 2, level, qtext, opts, ans, expl)
    if level == "D":
        a, b, c = sorted([random.randint(4, 60) for _ in range(3)])
        if random.random() < 0.5:
            val = math.gcd(math.gcd(a, b), c)
            qtext = f"HCF({a}, {b}, {c}) = ?"
        else:
            val = math.lcm(math.lcm(a, b), c)
            qtext = f"LCM({a}, {b}, {c}) = ?"
        opts, ans = _shuffle_options(str(val), [str(a + b + c), str(a * b), str(val + 4)])
        return _mcq(1, 2, level, qtext, opts, ans)
    t1, t2 = _random_pair()
    lcm = t1 * t2 // math.gcd(t1, t2)
    names = random.choice([("Sonia", "Ravi"), ("Asha", "Ben"), ("Mira", "Jay")])
    opts, ans = _shuffle_options(
        f"{lcm} minutes",
        [f"{t1 + t2} minutes", f"{math.gcd(t1, t2)} minutes", f"{lcm + t1} minutes"],
    )
    return _mcq(
        1, 2, level,
        f"{names[0]} takes {t1} min per round, {names[1]} takes {t2} min. "
        f"After how many minutes do they meet at the start?",
        opts, ans, "Use LCM of the two lap times.",
    )


def _gen_u1_t3(level: str) -> dict:
    if level == "A":
        irrationals = [f"√{p}" for p in [2, 3, 5, 6, 7, 10, 11, 13, 15]] + ["π", "0.101101110…"]
        rationals = [f"{random.randint(1, 9)}/{random.randint(2, 9)}" for _ in range(6)] + ["0.25", "-7", "0.333…"]
        correct = random.choice(irrationals)
        wrong = random.sample(rationals, 3)
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(1, 3, level, "Which number is irrational?", opts, ans)
    if level == "B":
        p = random.choice([2, 3, 5, 7, 11, 13, 17])
        a = random.randint(2, 40) * p
        opts, ans = _shuffle_options("p divides a", ["p divides a² only", "a divides p", "p is composite"])
        return _mcq(1, 3, level, f"If p = {p} (prime) and p divides {a}², then:", opts, ans, "Theorem 1.2: p | a² ⇒ p | a.")
    if level == "C":
        root = random.choice([2, 3, 5, 6, 7, 10, 11])
        sym = f"√{root}"
        opts, ans = _shuffle_options(
            f"Assume {sym} is rational",
            [f"Assume {sym} is irrational", "Square both sides first", "Set a = b"],
        )
        return _mcq(1, 3, level, f"Proof by contradiction that {sym} is irrational begins by:", opts, ans)
    if level == "D":
        p = random.choice([5, 7, 11, 13, 17, 19, 23])
        opts, ans = _shuffle_options(
            f"√{p} is irrational",
            [f"√{p} is rational", f"{p} is composite", f"√{p} = {p}/2"],
        )
        return _mcq(1, 3, level, f"Which statement about √{p} is true?", opts, ans, f"√{p} is irrational for prime {p}.")
    a, b = random.randint(2, 9), random.choice([2, 3, 5, 7])
    expr = f"{a} − √{b}" if random.random() < 0.5 else f"{a} + √{b}"
    opts, ans = _shuffle_options(
        f"{expr} is irrational",
        [f"{expr} is rational", f"√{b} is rational", "All such sums are rational"],
    )
    return _mcq(1, 3, level, f"Which is correct about {expr}?", opts, ans, "Assuming it rational leads to √ being rational — contradiction.")


def _gen_u1_t4(level: str) -> dict:
    if level == "A":
        prompts = [
            ("Non-zero rational + irrational is always:", "Irrational"),
            ("Non-zero rational × irrational is always:", "Irrational"),
            ("Rational ÷ (non-zero irrational) is always:", "Irrational"),
        ]
        qtext, correct = random.choice(prompts)
        opts, ans = _shuffle_options(correct, ["Rational", "Integer", "Natural"])
        return _mcq(1, 4, level, qtext, opts, ans)
    if level == "B":
        a, b, c = random.sample([3, 5, 7, 11, 13], 3)
        k = random.randint(2, 9)
        templates = [
            (f"{a} × {b} × {c} + {c}", f"Factor: {c}({a}×{b} + 1)."),
            (f"{a} × {b} × {c} + {a}", f"Factor: {a}({b}×{c} + 1)."),
            (f"{k} × {a} × {b} + {b}", f"Factor: {b}({k}×{a} + 1)."),
        ]
        expr, expl = random.choice(templates)
        opts, ans = _shuffle_options("Composite", ["Prime", "Irrational", "Perfect square"])
        return _mcq(1, 4, level, f"{expr} is:", opts, ans, expl)
    if level == "C":
        k = random.randint(2, 12)
        root = random.choice([2, 3, 5, 7])
        opts, ans = _shuffle_options("Irrational", ["Rational", "Integer", "Zero"])
        return _mcq(1, 4, level, f"{k}√{root} is:", opts, ans, f"If {k}√{root} were rational, √{root} would be rational.")
    if level == "D":
        a, b = random.randint(1, 5), random.choice([2, 3, 5, 7])
        expr = f"{a} + {random.randint(1, 4)}√{b}"
        opts, ans = _shuffle_options(
            f"{expr} is irrational",
            [f"{expr} is rational", f"√{b} is rational", f"{a}√{b} is rational"],
        )
        return _mcq(1, 4, level, f"Which follows from NCERT Ex 1.2 style proofs?", opts, ans)
    n = random.choice([2, 3, 5, 6, 7, 10, 15, 75, 4, 9])
    if n == 4:
        expr, kind = "(√2)²", "Rational"
    else:
        expr = f"√{n}"
        r = math.isqrt(n)
        kind = "Rational" if r * r == n else "Irrational"
    opts, ans = _shuffle_options(kind, [x for x in ["Rational", "Irrational", "Integer", "Prime"] if x != kind][:3])
    return _mcq(1, 4, level, f"{expr} is:", opts, ans)


# ── Unit 2 generators ──


def _random_quadratic() -> tuple[int, int, int, int, int]:
    """Return r1, r2, b, c for monic x² + bx + c with integer roots."""
    r1, r2 = random.randint(-6, 6), random.randint(-6, 6)
    b = -(r1 + r2)
    c = r1 * r2
    return r1, r2, b, c


def _poly_linear(a: int, b: int) -> str:
    if a == 1:
        ax = "x"
    elif a == -1:
        ax = "-x"
    else:
        ax = f"{a}x"
    if b == 0:
        return ax
    sign = "+" if b > 0 else "-"
    return f"{ax} {sign} {abs(b)}"


def _poly_quadratic(b: int, c: int, a: int = 1) -> str:
    if a == 1:
        head = "x²"
    else:
        head = f"{a}x²"
    mid = ""
    if b != 0:
        sign = "+" if b > 0 else "-"
        if abs(b) == 1:
            mid = f" {sign} x"
        else:
            mid = f" {sign} {abs(b)}x"
    tail = ""
    if c != 0:
        sign = "+" if c > 0 else "-"
        tail = f" {sign} {abs(c)}"
    return head + mid + tail


def _poly_cubic(a: int, b: int, c: int, d: int) -> str:
    head = "x³" if a == 1 else f"{a}x³"
    parts = [head]
    for coef, var in ((b, "x²"), (c, "x"), (d, "")):
        if coef == 0:
            continue
        sign = "+" if coef > 0 else "-"
        mag = abs(coef)
        if var:
            term = f"{mag}{var}" if mag != 1 else var
        else:
            term = str(mag)
        parts.append(f" {sign} {term}")
    return "".join(parts)


def _eval_poly(coeffs: list[int], x: int) -> int:
    total = 0
    power = len(coeffs) - 1
    for coef in coeffs:
        total += coef * (x ** power)
        power -= 1
    return total


def _gen_u2_t1(level: str) -> dict:
    if level == "A":
        templates = [
            (f"{random.randint(2, 9)}x³ + {random.randint(1, 5)}x − {random.randint(1, 9)}", 3),
            (f"x² + {random.randint(1, 8)}x + {random.randint(1, 9)}", 2),
            (f"{random.randint(2, 7)}x − {random.randint(1, 12)}", 1),
            (f"{random.randint(2, 5)}x⁴ + x² − 1", 4),
        ]
        expr, deg = random.choice(templates)
        opts, ans = _shuffle_options(str(deg), [str((deg + 1) % 5), str(max(0, deg - 1)), "0"])
        return _mcq(2, 1, level, f"What is the degree of p(x) = {expr}?", opts, ans)
    if level == "B":
        kind = random.choice(["Linear", "Quadratic", "Cubic"])
        samples = {
            "Linear": _poly_linear(random.randint(2, 5), random.randint(-8, 8)),
            "Quadratic": _poly_quadratic(*_random_quadratic()[2:4]),
            "Cubic": _poly_cubic(1, random.randint(-3, 3), random.randint(-4, 4), random.randint(-5, 5)),
        }
        expr = samples[kind]
        wrong = [k for k in samples if k != kind]
        opts, ans = _shuffle_options(kind, wrong)
        return _mcq(2, 1, level, f"p(x) = {expr} is a:", opts, ans)
    if level == "C":
        a = random.randint(2, 6)
        b, c = random.randint(-7, 7), random.randint(-9, 9)
        expr = _poly_quadratic(b, c, a)
        opts, ans = _shuffle_options(str(a), [str(b), str(c), str(a + b)])
        return _mcq(2, 1, level, f"Leading coefficient of p(x) = {expr}?", opts, ans)
    if level == "D":
        variants = [
            ("General form of a quadratic polynomial in x:", "ax² + bx + c, a ≠ 0", ["ax + b", "ax³ + bx² + cx + d", "a/x + b"]),
            ("General form of a cubic polynomial in x:", "ax³ + bx² + cx + d, a ≠ 0", ["ax² + bx + c", "ax + b", "a/x³ + b"]),
            ("Degree of a non-zero constant polynomial p(x) = 7:", "0", ["1", "7", "Undefined"]),
        ]
        qtext, correct, wrong = random.choice(variants)
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(2, 1, level, qtext, opts, ans)
    non_poly = random.choice([
        "1/x + 2", "√x + 3", "5/x² − 1", "2x⁻¹ + 4",
        "x + 1/x", "3√x − 2", "1/(x+1) + 5", "x⁰·⁵ + 1",
    ])
    opts, ans = _shuffle_options(non_poly, [_poly_quadratic(3, 2), _poly_linear(4, 1), "x² + 1"])
    return _mcq(2, 1, level, "Which expression is NOT a polynomial in x?", opts, ans)


def _gen_u2_t2(level: str) -> dict:
    if level == "A":
        a, b = random.randint(2, 9), random.randint(-12, 12)
        while a == 0:
            a = random.randint(2, 9)
        zero = Fraction(-b, a)
        correct = str(int(zero)) if zero.denominator == 1 else f"{zero.numerator}/{zero.denominator}"
        opts, ans = _shuffle_options(correct, [str(int(zero) + 1), str(int(zero) - 1), "0"])
        return _mcq(2, 2, level, f"Zero of p(x) = {_poly_linear(a, b)} is:", opts, ans, "Set p(x) = 0 and solve for x.")
    if level == "B":
        kind = random.choice(["quadratic", "linear", "cubic"])
        if kind == "linear":
            qtext, correct, wrong = (
                "A linear polynomial can have how many zeroes?",
                "Exactly 1",
                ["At most 2", "0 only", "Infinitely many"],
            )
        elif kind == "cubic":
            qtext, correct, wrong = (
                "A cubic polynomial can have at most how many zeroes?",
                "3",
                ["2", "1", "Infinitely many"],
            )
        else:
            qtext, correct, wrong = (
                "A quadratic polynomial can have how many zeroes?",
                "At most 2",
                ["Exactly 1", "At most 1", "Infinitely many"],
            )
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(2, 2, level, qtext, opts, ans)
    if level == "C":
        r1, r2, b, c = _random_quadratic()
        poly = _poly_quadratic(b, c)
        if random.random() < 0.5:
            correct, qtext = str(r1), f"One zero of p(x) = {poly} is:"
        else:
            correct, qtext = str(r2), f"Another zero of p(x) = {poly} is:"
        opts, ans = _shuffle_options(correct, [str(r1 + r2), str(r1 * r2), str(r1 + r2 + 1)])
        return _mcq(2, 2, level, qtext, opts, ans, f"Zeroes are {r1} and {r2}.")
    if level == "D":
        count = random.choice([0, 1, 2])
        desc = random.choice([
            {
                0: "The parabola lies entirely above the x-axis.",
                1: "The graph touches the x-axis at exactly one point.",
                2: "The graph cuts the x-axis at two distinct points.",
            }[count],
            {
                0: "The graph never meets the x-axis.",
                1: "The graph is tangent to the x-axis at one point.",
                2: "The parabola crosses the x-axis twice.",
            }[count],
        ])
        opts, ans = _shuffle_options(str(count), [str((count + 1) % 3), "3", "Infinitely many"])
        return _mcq(2, 2, level, f"{desc} Number of zeroes:", opts, ans)
    r = random.randint(2, 9)
    poly = _poly_quadratic(-2 * r, r * r)
    variants = [
        (f"1 (repeated zero x = {r})", [f"2 distinct zeroes", "0 zeroes", f"3 zeroes"]),
        (f"One repeated zero", ["Two distinct zeroes", "No zeroes", "Three zeroes"]),
    ]
    correct, wrong = random.choice(variants)
    opts, ans = _shuffle_options(correct, wrong)
    return _mcq(
        2, 2, level,
        f"p(x) = {poly} = (x − {r})². How many distinct zeroes?",
        opts, ans,
        f"The graph touches the x-axis at x = {r} only.",
    )


def _gen_u2_t3(level: str) -> dict:
    r1, r2, b, c = _random_quadratic()
    poly = _poly_quadratic(b, c)
    if level == "A":
        correct = str(-b)
        opts, ans = _shuffle_options(correct, [str(c), str(r1 * r2), str(r1 + r2 + 1)])
        return _mcq(2, 3, level, f"Sum of zeroes of p(x) = {poly}?", opts, ans, "For x² + bx + c, sum = −b.")
    if level == "B":
        correct = str(c)
        opts, ans = _shuffle_options(correct, [str(-b), str(r1 + r2), str(c + 1)])
        return _mcq(2, 3, level, f"Product of zeroes of p(x) = {poly}?", opts, ans, "For x² + bx + c, product = c.")
    if level == "C":
        s, p = -b, c
        correct = _poly_quadratic(-s, p)
        wrong = [_poly_quadratic(s, p), _poly_quadratic(-s, -p), _poly_quadratic(s, -p)]
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(
            2, 3, level,
            f"Quadratic with sum of zeroes {s} and product {p}:",
            opts, ans,
            "Use x² − (sum)x + (product).",
        )
    if level == "D":
        a = random.randint(2, 5)
        b, c = random.randint(-9, 9), random.randint(-12, 12)
        poly = _poly_quadratic(b, c, a)
        if random.random() < 0.5:
            val = Fraction(-b, a)
            label = "Sum of zeroes"
        else:
            val = Fraction(c, a)
            label = "Product of zeroes"
        correct = str(int(val)) if val.denominator == 1 else f"{val.numerator}/{val.denominator}"
        opts, ans = _shuffle_options(correct, [str(int(val) + 1), str(a), str(b)])
        return _mcq(2, 3, level, f"{label} of p(x) = {poly}?", opts, ans)
    r1, r2, b, c = _random_quadratic()
    poly = _poly_quadratic(b, c)
    correct = str(b)
    opts, ans = _shuffle_options(correct, [str(c), str(-b), str(b + 2)])
    return _mcq(
        2, 3, level,
        f"If {r1} and {r2} are zeroes of p(x) = {poly}, then the coefficient of x (k) equals:",
        opts, ans,
        "For x² + kx + c, sum of zeroes = −k.",
    )


def _gen_u2_t4(level: str) -> dict:
    if level == "A":
        a = random.randint(1, 4)
        x_val = random.randint(2, 6)
        b = random.randint(-8, 8)
        c = random.randint(-6, 6)
        poly = _poly_quadratic(b, c, a)
        correct = str(_eval_poly([a, b, c], x_val))
        opts, ans = _shuffle_options(correct, [str(int(correct) + 1), str(int(correct) - 1), "0"])
        return _mcq(
            2, 4, level,
            f"Remainder when p(x) = {poly} is divided by (x − {x_val}):",
            opts, ans,
            "Remainder equals p(x_val).",
        )
    if level == "B":
        r1, r2, b, c = _random_quadratic()
        poly = _poly_quadratic(b, c)
        check = r1
        is_factor = random.random() < 0.5
        if is_factor:
            answer = "Yes"
        else:
            check = r1 + random.randint(1, 3)
            answer = "No"
        opts, ans = _shuffle_options(answer, ["No", "Yes", "Only if x = 0"] if answer == "Yes" else ["Yes", "Only if x = 0", "Cannot tell"])
        return _mcq(2, 4, level, f"Is (x − {check}) a factor of p(x) = {poly}?", opts, ans, "Use factor theorem: (x − a) is a factor iff p(a) = 0.")
    if level == "C":
        r1, r2, b, c = _random_quadratic()
        poly = _poly_quadratic(b, c)
        x_val = random.choice([r1, r2])
        rem = 0
        opts, ans = _shuffle_options(str(rem), [str(r1 + r2), str(c), "1"])
        return _mcq(
            2, 4, level,
            f"Remainder when p(x) = {poly} is divided by (x − {x_val}):",
            opts, ans,
            f"p({x_val}) = 0 because x = {x_val} is a zero.",
        )
    if level == "D":
        r1, r2, b, c = _random_quadratic()
        poly = _poly_quadratic(b, c)
        if random.random() < 0.5:
            correct, qtext = str(r2), f"One zero of p(x) = {poly} is {r1}. The other zero is:"
            wrong = [str(r1), str(b), str(c)]
        else:
            correct, qtext = str(r1), f"One zero of p(x) = {poly} is {r2}. The other zero is:"
            wrong = [str(r2), str(b), str(c)]
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(2, 4, level, qtext, opts, ans, f"Zeroes are {r1} and {r2}.")
    r = random.randint(2, 9)
    k = -2 * r
    missing = r * r
    variants = [
        (f"If (x − {r})² divides x² + kx + t, then t equals:", str(missing)),
        (f"If x = {r} is a repeated zero of x² + kx + t, then t equals:", str(missing)),
    ]
    qtext, correct = random.choice(variants)
    opts, ans = _shuffle_options(correct, [str(k), str(-k), str(missing + r)])
    return _mcq(2, 4, level, qtext, opts, ans, f"Repeated zero x = {r} gives t = r².")


# ── Shared helpers for Units 3–4 ──


def _lin_eq(a: int, b: int, c: int) -> str:
    terms: list[str] = []
    if a != 0:
        if a == 1:
            terms.append("x")
        elif a == -1:
            terms.append("-x")
        else:
            terms.append(f"{a}x")
    if b != 0:
        sign = "+" if b > 0 else "-"
        mag = abs(b)
        yterm = "y" if mag == 1 else f"{mag}y"
        if terms:
            terms.append(f" {sign} {yterm}")
        else:
            terms.append(f"-{yterm}" if b < 0 else yterm)
    expr = "".join(terms) if terms else "0"
    return f"{expr} = {c}"


def _random_lin_sys() -> tuple[int, int, tuple[int, int, int], tuple[int, int, int]]:
    x, y = random.randint(-6, 9), random.randint(-6, 9)
    a1, b1 = random.randint(1, 6), random.randint(1, 6)
    c1 = a1 * x + b1 * y
    for _ in range(60):
        a2 = random.randint(1, 6)
        b2 = random.randint(-6, 6)
        if a1 * b2 != a2 * b1:
            c2 = a2 * x + b2 * y
            return x, y, (a1, b1, c1), (a2, b2, c2)
    a2, b2, c2 = a1 + 1, b1 + 1, (a1 + 1) * x + (b1 + 1) * y
    return x, y, (a1, b1, c1), (a2, b2, c2)


def _parallel_sys() -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    a, b = random.randint(2, 5), random.randint(1, 5)
    k = random.randint(2, 4)
    c1 = random.randint(5, 20)
    return (a, b, c1), (k * a, k * b, c1 + random.randint(1, 5))


def _coincident_sys() -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    a, b = random.randint(2, 5), random.randint(1, 5)
    c = random.randint(6, 24)
    k = random.randint(2, 4)
    return (a, b, c), (k * a, k * b, k * c)


def _quad_std(a: int, b: int, c: int) -> str:
    head = f"{a}x²" if a != 1 else "x²"
    mid = ""
    if b != 0:
        sign = "+" if b > 0 else "-"
        mag = abs(b)
        mid = f" {sign} {mag}x" if mag != 1 else f" {sign} x"
    tail = ""
    if c != 0:
        sign = "+" if c > 0 else "-"
        tail = f" {sign} {abs(c)}"
    return f"{head}{mid}{tail} = 0"


def _random_quad_roots() -> tuple[int, int, int, int]:
    r1, r2 = random.randint(-8, 8), random.randint(-8, 8)
    b = -(r1 + r2)
    c = r1 * r2
    return r1, r2, b, c


def _nature_from_disc(d: int) -> str:
    if d > 0:
        return "Two distinct real roots"
    if d == 0:
        return "Two equal real roots"
    return "No real roots"


# ── Unit 3 generators ──


def _gen_u3_t1(level: str) -> dict:
    if level == "A":
        eq1 = _lin_eq(random.randint(1, 4), random.randint(1, 4), random.randint(3, 15))
        eq2 = _lin_eq(random.randint(1, 4), random.randint(-4, 4), random.randint(3, 15))
        opts, ans = _shuffle_options("Intersecting", ["Parallel", "Coincident", "Vertical only"])
        return _mcq(3, 1, level, f"Lines {eq1} and {eq2} (different slopes) are:", opts, ans)
    if level == "B":
        variants = [
            ("Exactly one solution", ["No solution", "Infinitely many", "Exactly two"]),
            ("No solution", ["Exactly one solution", "Infinitely many", "Exactly two"]),
            ("Infinitely many solutions", ["No solution", "Exactly one solution", "Exactly two"]),
            ("Unique solution (consistent)", ["Inconsistent pair", "No variable", "Three solutions"]),
        ]
        correct, wrong = random.choice(variants)
        opts, ans = _shuffle_options(correct, wrong)
        qtext = random.choice([
            "A pair of linear equations in two variables can have:",
            "Which is a possible outcome for a pair of linear equations?",
            "Solutions of a pair of linear equations:",
        ])
        return _mcq(3, 1, level, qtext, opts, ans)
    if level == "C":
        (a1, b1, c1), (a2, b2, c2) = _parallel_sys()
        opts, ans = _shuffle_options("Inconsistent (no solution)", ["Consistent with unique solution", "Consistent with infinitely many", "Dependent only"])
        return _mcq(
            3, 1, level,
            f"Pair: {_lin_eq(a1, b1, c1)} and {_lin_eq(a2, b2, c2)} is:",
            opts, ans, "Parallel distinct lines → inconsistent.",
        )
    if level == "D":
        (a1, b1, c1), (a2, b2, c2) = _coincident_sys()
        opts, ans = _shuffle_options("Infinitely many solutions", ["No solution", "Unique solution", "Two solutions"])
        return _mcq(
            3, 1, level,
            f"Coincident pair: {_lin_eq(a1, b1, c1)} and {_lin_eq(a2, b2, c2)} has:",
            opts, ans,
        )
    x, y, (a1, b1, c1), (a2, b2, c2) = _random_lin_sys()
    det = a1 * b2 - a2 * b1
    opts, ans = _shuffle_options("Unique solution", ["No solution", "Infinitely many", "Cannot determine"])
    return _mcq(
        3, 1, level,
        f"If a₁/a₂ ≠ b₁/b₂ for {_lin_eq(a1, b1, c1)} and {_lin_eq(a2, b2, c2)}, the pair has:",
        opts, ans,
        f"Solution is x = {x}, y = {y} (det = {det}).",
    )


def _gen_u3_t2(level: str) -> dict:
    x, y, (a1, b1, c1), (a2, b2, c2) = _random_lin_sys()
    eq1, eq2 = _lin_eq(a1, b1, c1), _lin_eq(a2, b2, c2)
    if level == "A":
        sx, sy = random.randint(1, 9), random.randint(1, 9)
        if random.random() < 0.5:
            correct, q = str(sx + sy), f"x + y = {sx + sy} and x − y = {sx - sy}. x equals?"
        else:
            correct, q = str(sx), f"x + y = {sx + sy} and x − y = {sx - sy}. x equals?"
        opts, ans = _shuffle_options(correct, [str(int(correct) + 1), str(int(correct) - 1), str(int(correct) + 2)])
        return _mcq(3, 2, level, q, opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(f"x = ({c1} − {b1}y)/{a1}", [f"y = ({c1} − {a1}x)/{b1}", f"x = {c1} − {b1}y", f"x = {c1}/{a1}"])
        return _mcq(3, 2, level, f"From {eq1}, express x in terms of y:", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options(str(x), [str(y), str(x + y), str(x - y)])
        return _mcq(3, 2, level, f"Using substitution on {eq1} and {eq2}, x equals:", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options(str(y), [str(x), str(x + y), str(x - y)])
        return _mcq(3, 2, level, f"Using substitution on {eq1} and {eq2}, y equals:", opts, ans)
    a1, b1, c1 = random.randint(2, 5), random.randint(2, 5), random.randint(10, 30)
    x_val = random.randint(2, 6)
    y_val = (c1 - a1 * x_val) // b1 if (c1 - a1 * x_val) % b1 == 0 else None
    if y_val is None:
        y_val = random.randint(1, 5)
        c1 = a1 * x_val + b1 * y_val
    opts, ans = _shuffle_options(str(y_val), [str(x_val), str(y_val + 1), str(x_val + y_val)])
    return _mcq(3, 2, level, f"Solve by substitution: {_lin_eq(a1, b1, c1)} and x = {x_val}. Then y = ?", opts, ans)


def _gen_u3_t3(level: str) -> dict:
    x, y, (a1, b1, c1), (a2, b2, c2) = _random_lin_sys()
    eq1, eq2 = _lin_eq(a1, b1, c1), _lin_eq(a2, b2, c2)
    if level == "A":
        steps = [
            ("Add or subtract equations to eliminate one variable", ["Substitute x = 0", "Divide both equations", "Graph the lines only"]),
            ("Multiply equations to equalise coefficients, then add/subtract", ["Set y = 0 only", "Add constants term-wise only", "Swap x and y"]),
            ("Eliminate either x or y using suitable multipliers", ["Always divide by a", "Ignore second equation", "Use quadratic formula"]),
        ]
        correct, wrong = random.choice(steps)
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(3, 3, level, "First step in elimination method:", opts, ans)
    if level == "B":
        hints = [
            ("Multiply one or both equations to equalise a coefficient", ["Set x = 0", "Add constants only", "Swap x and y"]),
            ("Make coefficients of x or y equal in magnitude", ["Eliminate constants first", "Use cross-multiplication only", "Graph both lines"]),
            ("Scale an equation so one variable cancels on adding", ["Divide both by c", "Substitute y = x", "Ignore coefficients"]),
        ]
        correct, wrong = random.choice(hints)
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(3, 3, level, "To eliminate a variable when coefficients differ:", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options(str(x), [str(y), str(x + 1), str(y + 1)])
        return _mcq(3, 3, level, f"Elimination on {eq1} and {eq2} gives x = ?", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options(str(y), [str(x), str(x + 1), str(y + 1)])
        return _mcq(3, 3, level, f"Elimination on {eq1} and {eq2} gives y = ?", opts, ans)
    # scaled elimination
    m = random.randint(2, 3)
    a1, b1, c1 = 2, 3, random.randint(8, 20)
    a2, b2, c2 = 4, 6, 2 * c1  # dependent-ish; use different
    x, y, (a1, b1, c1), (a2, b2, c2) = _random_lin_sys()
    opts, ans = _shuffle_options(f"x = {x}, y = {y}", [f"x = {y}, y = {x}", f"x = {x + 1}, y = {y}", f"x = {x}, y = {y + 1}"])
    return _mcq(3, 3, level, f"Solve by elimination: {eq1} and {eq2}.", opts, ans)


def _gen_u3_t4(level: str) -> dict:
    x, y, (a1, b1, c1), (a2, b2, c2) = _random_lin_sys()
    det = a1 * b2 - a2 * b1
    x_cross = (c1 * b2 - c2 * b1) // det if det else x
    y_cross = (a1 * c2 - a2 * c1) // det if det else y
    if level == "A":
        opts, ans = _shuffle_options(
            "x = (c₁b₂ − c₂b₁)/(a₁b₂ − a₂b₁), y = (a₁c₂ − a₂c₁)/(a₁b₂ − a₂b₁)",
            ["x = c₁/a₁, y = c₂/a₂", "x = (a₁c₂ − a₂c₁)/(b₁c₂ − b₂c₁)", "x = y = c₁ + c₂"],
        )
        return _mcq(3, 4, level, "Cross-multiplication formula for a₁x + b₁y = c₁:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(f"x = {x_cross}, y = {y_cross}", [f"x = {y_cross}, y = {x_cross}", f"x = {x_cross + 1}, y = {y_cross}", f"x = {x}, y = {y + 1}"])
        return _mcq(
            3, 4, level,
            f"Cross-multiplication on {_lin_eq(a1, b1, c1)} and {_lin_eq(a2, b2, c2)}:",
            opts, ans,
        )
    if level == "C":
        opts, ans = _shuffle_options("24 years", ["12 years", "36 years", "18 years"])
        return _mcq(
            3, 4, level,
            "Father is 3× son's age; in 12 years he will be 2× son's age. Age difference now?",
            opts, ans, "Set son = x, father = 3x; solve 3x + 12 = 2(x + 12) → x = 12, difference = 24.",
        )
    if level == "D":
        tens, ones = random.randint(2, 7), random.randint(1, 9)
        num = 10 * tens + ones
        rev = 10 * ones + tens
        diff = abs(num - rev)
        opts, ans = _shuffle_options(str(diff), [str(diff + 9), str(diff - 1), str(tens + ones)])
        return _mcq(
            3, 4, level,
            f"A two-digit number has tens digit {tens} and units {ones}. "
            f"Difference between the number and its reverse?",
            opts, ans,
        )
    price_a, price_b = random.randint(20, 50), random.randint(10, 30)
    total_items = random.randint(4, 10)
    total_cost = price_a * random.randint(1, total_items - 1) + price_b * (total_items - random.randint(1, total_items - 1))
    opts, ans = _shuffle_options("Form two linear equations in two unknowns", ["Single quadratic", "One variable only", "No variables needed"])
    return _mcq(
        3, 4, level,
        "A shop sells two types of pens at different prices. "
        "Given counts and total cost, the NCERT approach is to:",
        opts, ans,
    )


# ── Unit 4 generators ──


def _gen_u4_t1(level: str) -> dict:
    r1, r2, b, c = _random_quad_roots()
    a = random.choice([1, 2, 3]) if level in ("D", "E") else 1
    eq = _quad_std(a, a * b, a * c) if a != 1 else _quad_std(1, b, c)
    if level == "A":
        if random.random() < 0.5:
            correct, q = str(a), f"In {eq}, a equals?"
            wrong = [str(b), str(c), str(a + 1)]
        elif random.random() < 0.5:
            correct, q = str(a * b if a != 1 else b), f"In {eq}, b equals?"
            wrong = [str(a), str(c), str(b + 1)]
        else:
            correct, q = str(a * c if a != 1 else c), f"In {eq}, c equals?"
            wrong = [str(a), str(b), str(c + 1)]
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(4, 1, level, q, opts, ans)
    if level == "B":
        root = random.choice([r1, r2])
        opts, ans = _shuffle_options("Yes", ["No", "Only if x > 0", "Cannot tell"])
        return _mcq(4, 1, level, f"Is x = {root} a root of {eq}?", opts, ans, f"Substitute: ({root}) satisfies the equation.")
    if level == "C":
        correct = _quad_std(1, -(r1 + r2), r1 * r2)
        wrong = [_quad_std(1, r1 + r2, r1 * r2), _quad_std(1, -(r1 + r2), -(r1 * r2)), _quad_std(1, r1, r2)]
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(4, 1, level, f"Quadratic with roots {r1} and {r2}:", opts, ans, "Use (x − α)(x − β) = 0.")
    if level == "D":
        opts, ans = _shuffle_options("At most 2", ["Exactly 1", "Infinitely many", "At most 3"])
        return _mcq(4, 1, level, "A quadratic equation can have real roots:", opts, ans)
    s, p = -(r1 + r2), r1 * r2
    correct = _quad_std(1, -s, p)
    opts, ans = _shuffle_options(correct, [_quad_std(1, s, p), _quad_std(1, -s, -p), _quad_std(1, s, -p)])
    return _mcq(4, 1, level, f"Sum of roots = {s}, product = {p}. The quadratic is:", opts, ans)


def _gen_u4_t2(level: str) -> dict:
    r1, r2, b, c = _random_quad_roots()
    eq = _quad_std(1, b, c)
    if level == "A":
        opts, ans = _shuffle_options(f"{c} = {r1} × {r2}", [f"{b} = {r1} + {r2}", f"{b} = {r1} × {r2}", f"{c} = {r1} + {r2}"])
        return _mcq(4, 2, level, f"Split middle term for {eq}: constant term relation?", opts, ans)
    if level == "B":
        correct = f"(x − {r1})(x − {r2}) = 0" if r1 != r2 else f"(x − {r1})² = 0"
        wrong = [f"(x + {r1})(x + {r2}) = 0", f"(x − {r1})(x + {r2}) = 0", f"(x + {r1})² = 0"]
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(4, 2, level, f"Factorised form of {eq}:", opts, ans)
    if level == "C":
        roots = f"x = {r1}, {r2}" if r1 != r2 else f"x = {r1} (repeated)"
        opts, ans = _shuffle_options(roots, [f"x = {-r1}, {-r2}", f"x = {r1 + r2}", f"x = {r1 * r2}"])
        return _mcq(4, 2, level, f"Solutions of {eq} by factorisation:", opts, ans)
    if level == "D":
        k = random.randint(2, 4)
        b, c = k * (-(r1 + r2)), k * (r1 * r2)
        eq = f"{k}x² + {b}x + {c} = 0"
        opts, ans = _shuffle_options(f"{k}(x² + {b // k}x + {c // k})", [f"{k}(x² − {b // k}x + {c // k})", f"(x² + {b}x + {c})", f"{k}x(x + {b // k})"])
        return _mcq(4, 2, level, f"Factorise completely: {eq}", opts, ans)
    # rearrange
    b, c = _random_quad_roots()[2:4]
    shifted = random.randint(1, 5)
    eq = f"x² + {b}x = {c + shifted}"
    correct = _quad_std(1, b, -(c + shifted))
    opts, ans = _shuffle_options(correct, [_quad_std(1, -b, c), _quad_std(1, b, c), _quad_std(1, b, c + shifted)])
    return _mcq(4, 2, level, f"Standard form of {eq}:", opts, ans)


def _gen_u4_t3(level: str) -> dict:
    r1, r2, b, c = _random_quad_roots()
    a = 1
    d = b * b - 4 * a * c
    if level == "A":
        opts, ans = _shuffle_options(
            "x = (−b ± √(b² − 4ac)) / 2a",
            ["x = (−b ± √(b² + 4ac)) / 2a", "x = b ± √c", "x = −c/b"],
        )
        return _mcq(4, 3, level, "Quadratic formula for ax² + bx + c = 0:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(str(d), [str(b), str(c), str(d + 4)])
        return _mcq(4, 3, level, f"Discriminant of {_quad_std(a, b, c)}:", opts, ans)
    if level == "C":
        roots = f"{r1} and {r2}" if r1 != r2 else f"{r1} (twice)"
        opts, ans = _shuffle_options(roots, [f"{-r1} and {-r2}", f"{r1 + r2}", f"{r1 * r2}"])
        return _mcq(4, 3, level, f"Roots of {_quad_std(a, b, c)} by formula:", opts, ans)
    if level == "D":
        a = random.choice([2, 3])
        b, c = a * random.randint(-6, 6), a * random.randint(-9, 9)
        d = b * b - 4 * a * c
        if d < 0:
            nature = "No real roots"
        elif d == 0:
            nature = "Equal roots"
        else:
            nature = "Two distinct real roots"
        opts, ans = _shuffle_options(nature, [x for x in ["No real roots", "Equal roots", "Two distinct real roots"] if x != nature])
        return _mcq(4, 3, level, f"Nature of roots of {_quad_std(a, b, c)} (use Δ first):", opts, ans)
    opts, ans = _shuffle_options("Factorisation if easy; else quadratic formula", ["Always graph", "Always cross-multiply", "Only completing the square"])
    return _mcq(4, 3, level, "Best NCERT method when factorisation is not obvious:", opts, ans)


def _gen_u4_t4(level: str) -> dict:
    a = random.choice([1, 2, 3])
    b = random.randint(-10, 10)
    c = random.randint(-12, 12)
    d = b * b - 4 * a * c
    if level == "A":
        opts, ans = _shuffle_options(str(d), [str(b), str(4 * a * c), str(d + 1)])
        return _mcq(4, 4, level, f"Δ for {_quad_std(a, b, c)}:", opts, ans)
    if level == "B":
        correct = _nature_from_disc(d)
        wrong = [x for x in ["Two distinct real roots", "Two equal real roots", "No real roots"] if x != correct]
        opts, ans = _shuffle_options(correct, wrong)
        return _mcq(4, 4, level, f"If Δ = {d} for a quadratic, nature of roots:", opts, ans)
    if level == "C":
        # equal roots: D=0 => k^2 - 4*1*c = 0 for x^2 + kx + c
        r = random.randint(2, 7)
        k = -2 * r
        opts, ans = _shuffle_options(str(k), [str(-k), str(r), str(r * r)])
        return _mcq(4, 4, level, f"For x² + kx + {r * r} = 0 to have equal roots, k = ?", opts, ans, "Δ = k² − 4r² = 0.")
    if level == "D":
        k = random.randint(-8, 8)
        c = random.randint(1, 6)
        d_k = k * k - 4 * c
        answer = "Any k with k² > 4c" if d_k > 0 else f"k = ±{int(math.isqrt(4 * c))}" if 4 * c >= 0 else "Depends on k"
        if 4 * c > 0 and math.isqrt(4 * c) ** 2 == 4 * c:
            correct = f"|k| > {math.isqrt(4 * c)}"
        else:
            correct = "Two distinct real roots when Δ > 0"
        opts, ans = _shuffle_options(correct, ["No real roots always", "Equal roots always", "k = 0 only"])
        return _mcq(4, 4, level, f"x² + kx + {c} = 0 has distinct real roots when:", opts, ans)
    k = random.randint(1, 8)
    c = k * k + random.randint(1, 5)
    opts, ans = _shuffle_options(f"|k| < {int(math.isqrt(4 * c))}" if 4 * c > 0 else "Δ < 0", ["Δ > 0", "Δ = 0", "Always real"])
    return _mcq(4, 4, level, f"x² + {k}x + {c} = 0 has no real roots because:", opts, ans, "Check Δ = k² − 4c < 0.")


# ── Unit 5 generators ──


def _ap_nth(a: int, d: int, n: int) -> int:
    return a + (n - 1) * d


def _ap_sum(a: int, d: int, n: int) -> int:
    return n * (2 * a + (n - 1) * d) // 2


def _random_ap() -> tuple[int, int]:
    a = random.randint(-8, 15)
    d = random.choice([x for x in range(-6, 7) if x != 0])
    return a, d


def _ap_terms_str(a: int, d: int, count: int = 4) -> str:
    terms = [_ap_nth(a, d, i) for i in range(1, count + 1)]
    return ", ".join(str(t) for t in terms) + ", …"


def _gen_u5_t1(level: str) -> dict:
    a, d = _random_ap()
    seq = _ap_terms_str(a, d)
    if level == "A":
        opts, ans = _shuffle_options(
            "Each term differs by a fixed number from the previous one",
            ["Each term is double the previous", "Terms are perfect squares", "Terms multiply by a fixed ratio"],
        )
        return _mcq(5, 1, level, f"The list {seq} follows which pattern?", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(str(d), [str(d + 1), str(-d), str(a)])
        return _mcq(5, 1, level, f"In the AP {seq} the common difference d is:", opts, ans)
    if level == "C":
        if random.random() < 0.5:
            opts, ans = _shuffle_options("Yes", ["No", "Only if n is even", "Cannot tell"])
            return _mcq(5, 1, level, f"Is {seq} an arithmetic progression?", opts, ans, f"Successive differences equal {d}.")
        b, c = random.randint(2, 5), random.randint(2, 5)
        not_ap = f"{b}, {b * c}, {b + c}, {b * c + c}, …"
        opts, ans = _shuffle_options("No", ["Yes", "Only for even terms", "Yes if c = 0"])
        return _mcq(5, 1, level, f"Is {not_ap} an arithmetic progression?", opts, ans, "Differences are not constant.")
    if level == "D":
        next_t = _ap_nth(a, d, 5)
        opts, ans = _shuffle_options(str(next_t), [str(next_t + d), str(a + d), str(next_t - d)])
        return _mcq(5, 1, level, f"Next term after {seq.rstrip(', …')} is:", opts, ans)
    opts, ans = _shuffle_options(
        "a, a + d, a + 2d, a + 3d, …",
        ["a, ad, ad², ad³, …", "a, a², a³, a⁴, …", "a, a − d, a − 2d, …"],
    )
    return _mcq(5, 1, level, "General form of an AP with first term a and common difference d:", opts, ans)


def _gen_u5_t2(level: str) -> dict:
    a, d = _random_ap()
    n = random.randint(5, 15)
    if level == "A":
        opts, ans = _shuffle_options(
            "aₙ = a + (n − 1)d",
            ["aₙ = a + nd", "aₙ = a × dⁿ", "aₙ = n(a + d)"],
        )
        return _mcq(5, 2, level, "nth term of an AP:", opts, ans)
    if level == "B":
        term = _ap_nth(a, d, n)
        opts, ans = _shuffle_options(str(term), [str(term + d), str(a + n * d), str(term - d)])
        return _mcq(
            5, 2, level,
            f"10th term of AP with a = {a}, d = {d}:" if n == 10 else f"{n}th term of AP with a = {a}, d = {d}:",
            opts, ans,
            f"a_{n} = {a} + ({n}−1)×{d} = {term}.",
        )
    if level == "C":
        n_target = random.randint(8, 20)
        term_val = _ap_nth(a, d, n_target)
        opts, ans = _shuffle_options(str(n_target), [str(n_target + 1), str(n_target - 1), str(n_target + 2)])
        return _mcq(
            5, 2, level,
            f"Which term of the AP {_ap_terms_str(a, d)} equals {term_val}?",
            opts, ans,
            f"Solve {term_val} = {a} + (n−1)({d}).",
        )
    if level == "D":
        a3, a7 = _ap_nth(a, d, 3), _ap_nth(a, d, 7)
        opts, ans = _shuffle_options(f"a = {a}, d = {d}", [f"a = {a + d}, d = {d + 1}", f"a = {a - 1}, d = {d}", f"a = {a}, d = 0"])
        return _mcq(
            5, 2, level,
            f"AP whose 3rd term is {a3} and 7th term is {a7}:",
            opts, ans,
            "Two equations: a + 2d and a + 6d.",
        )
    # term from end style
    a_pos, d_neg = 10, -3
    n_total = 25
    l = _ap_nth(a_pos, d_neg, n_total)
    term_from_end = _ap_nth(a_pos, d_neg, n_total - 10)  # 11th from last = 15th
    opts, ans = _shuffle_options(str(term_from_end), [str(l), str(_ap_nth(a_pos, d_neg, 11)), str(term_from_end + 3)])
    return _mcq(
        5, 2, level,
        f"AP 10, 7, 4, …, {l} has 25 terms. The 11th term from the last is:",
        opts, ans,
        "11th from last = 15th from start = 10 + 14(−3) = −32.",
    )


def _gen_u5_t3(level: str) -> dict:
    a, d = _random_ap()
    n = random.randint(5, 12)
    if level == "A":
        opts, ans = _shuffle_options(
            "Sₙ = n/2 [2a + (n − 1)d]",
            ["Sₙ = n(a + d)", "Sₙ = a + (n − 1)d", "Sₙ = n²d"],
        )
        return _mcq(5, 3, level, "Sum of first n terms of an AP:", opts, ans)
    if level == "B":
        total = _ap_sum(a, d, n)
        opts, ans = _shuffle_options(str(total), [str(total + n), str(_ap_nth(a, d, n)), str(total - d)])
        return _mcq(
            5, 3, level,
            f"Sum of first {n} terms of AP with a = {a}, d = {d}:",
            opts, ans,
            f"S_{n} = {n}/2[2×{a} + ({n}−1)×{d}] = {total}.",
        )
    if level == "C":
        l = _ap_nth(a, d, n)
        total = _ap_sum(a, d, n)
        alt_wrong = n * (a + l) // 2 + d
        opts, ans = _shuffle_options(str(total), [str(alt_wrong), str(l), str(a + l)])
        return _mcq(
            5, 3, level,
            f"AP: a = {a}, d = {d}, n = {n}. Sum using Sₙ = n/2(a + l):",
            opts, ans,
            f"l = {l}, S = {n}/2({a}+{l}) = {total}.",
        )
    if level == "D":
        n_solve = random.randint(6, 10)
        s_val = _ap_sum(a, d, n_solve)
        opts, ans = _shuffle_options(str(n_solve), [str(n_solve + 1), str(n_solve - 1), str(n_solve + 2)])
        return _mcq(
            5, 3, level,
            f"Sum of an AP is {s_val} with a = {a}, d = {d}. Number of terms n = ?",
            opts, ans,
        )
    opts, ans = _shuffle_options(
        "Sₙ = n/2(a + l) when last term l is known",
        ["Always use Sₙ = n²d", "Use aₙ formula instead", "Add terms one by one only"],
    )
    return _mcq(5, 3, level, "Best formula when first term a and last term l are known:", opts, ans)


def _gen_u5_t4(level: str) -> dict:
    if level == "A":
        start, inc, yr = 8000, 500, 5
        salary = start + (yr - 1) * inc
        opts, ans = _shuffle_options(f"₹{salary}", [f"₹{salary + inc}", f"₹{start + yr * inc}", f"₹{start}"])
        return _mcq(
            5, 4, level,
            f"Monthly salary starts at ₹{start} with ₹{inc} annual increment. Salary in year {yr}?",
            opts, ans,
            f"AP with a = {start}, d = {inc}; year {yr} term = {salary}.",
        )
    if level == "B":
        first, diff, last = 23, -2, 5
        n = (last - first) // diff + 1
        opts, ans = _shuffle_options(str(n), [str(n + 1), str(n - 1), str(abs(n))])
        return _mcq(
            5, 4, level,
            f"Rose plants per row: {first}, {first + diff}, …, {last}. How many rows?",
            opts, ans,
            f"Solve {last} = {first} + (n−1)({diff}).",
        )
    if level == "C":
        p, rate, yrs = 1000, 8, 30
        interest = p * rate * yrs // 100
        opts, ans = _shuffle_options(f"₹{interest}", [f"₹{p * rate // 100}", f"₹{interest + 80}", f"₹{p + interest}"])
        return _mcq(
            5, 4, level,
            f"₹{p} at {rate}% simple interest per year — interest at end of year {yrs}?",
            opts, ans,
            f"Interests 80, 160, … form AP; a_{yrs} = {interest}.",
        )
    if level == "D":
        a, d, target = 12, 3, 99
        n = (target - a) // d + 1
        opts, ans = _shuffle_options(str(n), [str(n - 1), str(n + 1), "33"])
        return _mcq(
            5, 4, level,
            "How many two-digit numbers are divisible by 3?",
            opts, ans,
            f"AP 12, 15, …, 99 gives n = {n}.",
        )
    a, d = 6, 4
    s10 = _ap_sum(a, d, 10)
    opts, ans = _shuffle_options(str(s10), [str(_ap_nth(a, d, 10)), str(s10 + 10), str(s10 - 4)])
    return _mcq(
        5, 4, level,
        f"Find the sum of first 10 terms of AP {a}, {a + d}, {a + 2 * d}, …",
        opts, ans,
        f"S_10 = 10/2[2×{a} + 9×{d}] = {s10}.",
    )


# ── Unit 6 generators ──


def _bpt_ec(ad: int, db: int, ae: int) -> int:
    """EC when AD/DB = AE/EC with integer result."""
    return ae * db // ad


def _gen_u6_t1(level: str) -> dict:
    if level == "A":
        opts, ans = _shuffle_options(
            "All congruent figures are similar, but similar figures need not be congruent",
            ["All similar figures are congruent", "Congruent and similar mean the same", "No relation between them"],
        )
        return _mcq(6, 1, level, "Which statement about congruence and similarity is correct?", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(
            "The ratio of corresponding side lengths (scale factor)",
            ["The sum of corresponding angles", "The difference of perimeters", "Always 1"],
        )
        return _mcq(6, 1, level, "Scale factor between two similar figures is:", opts, ans)
    if level == "C":
        small, large = random.randint(3, 8), random.randint(10, 18)
        ratio = f"{small}:{large}"
        opts, ans = _shuffle_options(ratio, [f"{large}:{small}", f"{small + 1}:{large}", f"{small}:{large + 2}"])
        return _mcq(
            6, 1, level,
            f"Side AB = {small} cm in ΔABC and A′B′ = {large} cm in similar ΔA′B′C′. Scale factor (small → large):",
            opts, ans,
            f"Corresponding sides are in ratio {small}:{large}.",
        )
    if level == "D":
        k_num, k_den = random.randint(2, 4), random.randint(2, 3)
        base = random.randint(4, 9)
        missing = base * k_num // k_den
        opts, ans = _shuffle_options(f"{missing} cm", [f"{base} cm", f"{missing + 2} cm", f"{base * k_den // k_num} cm"])
        return _mcq(
            6, 1, level,
            f"Two similar triangles have sides in ratio {k_num}:{k_den}. If the smaller side is {base} cm, the corresponding larger side is:",
            opts, ans,
        )
    opts, ans = _shuffle_options(
        "Equal corresponding angles AND proportional corresponding sides",
        ["Equal sides only", "Equal angles only", "Same perimeter"],
    )
    return _mcq(6, 1, level, "Two polygons with the same number of sides are similar if:", opts, ans)


def _gen_u6_t2(level: str) -> dict:
    if level == "A":
        opts, ans = _shuffle_options(
            "A line parallel to one side divides the other two sides in the same ratio",
            ["Parallel lines have equal length", "All triangles are equilateral", "Angles sum to 180° only"],
        )
        return _mcq(6, 2, level, "Basic Proportionality Theorem (Theorem 6.1) states:", opts, ans)
    ad, db = random.randint(2, 5), random.randint(3, 8)
    ae = random.randint(3, 9)
    ec = _bpt_ec(ad, db, ae)
    if level == "B":
        opts, ans = _shuffle_options(f"{ec} cm", [f"{ae} cm", f"{ec + ad} cm", f"{db} cm"])
        return _mcq(
            6, 2, level,
            f"In ΔABC, DE ∥ BC. AD = {ad} cm, DB = {db} cm, AE = {ae} cm. EC = ?",
            opts, ans,
            f"AD/DB = AE/EC ⇒ EC = {ae}×{db}/{ad} = {ec}.",
        )
    if level == "C":
        ab = ad + db
        ac = ae + ec
        opts, ans = _shuffle_options(f"AE/AC = {ae}/{ac}", [f"AD/AB = {db}/{ab}", f"AE/EC = {db}/{ad}", f"AD/AE = {ec}/{ae}"])
        return _mcq(
            6, 2, level,
            f"DE ∥ BC with AD = {ad}, DB = {db}, AE = {ae}, EC = {ec}. Which ratio is correct?",
            opts, ans,
            "Also AD/AB = AE/AC when DE ∥ BC.",
        )
    if level == "D":
        pe, eq, pf, fr = 3, 4, 6, 8  # 3/4 = 6/8 → parallel
        opts, ans = _shuffle_options("Yes, EF ∥ QR", ["No", "Only if PQ = PR", "Cannot tell"])
        return _mcq(
            6, 2, level,
            f"In ΔPQR, PE = {pe} cm, EQ = {eq} cm, PF = {pf} cm, FR = {fr} cm. Is EF ∥ QR?",
            opts, ans,
            f"PE/EQ = {pe}/{eq} = PF/FR = {pf}/{fr} — converse of BPT applies.",
        )
    opts, ans = _shuffle_options(
        "AE/ED = BF/FC when EF ∥ AB in a trapezium",
        ["AE = BF always", "EF = AB", "No ratio relation"],
    )
    return _mcq(
        6, 2, level,
        "In trapezium ABCD (AB ∥ DC), EF ∥ AB with E on AD and F on BC. Then:",
        opts, ans,
    )


def _gen_u6_t3(level: str) -> dict:
    r1, r2 = random.randint(2, 4), random.randint(2, 4)
    side_small = random.randint(4, 9)
    side_large = side_small * r2 // r1
    if level == "A":
        opts, ans = _shuffle_options(
            "If corresponding angles are equal, triangles are similar (AAA)",
            ["If one side matches, triangles are congruent", "All triangles are similar", "Equal perimeters imply similarity"],
        )
        return _mcq(6, 3, level, "AAA similarity criterion (Theorem 6.3):", opts, ans)
    if level == "B":
        a, b, c = 3, 4, 5
        ka = random.randint(2, 4)
        opts, ans = _shuffle_options(
            f"{ka * a}, {ka * b}, {ka * c}",
            [f"{a + ka}, {b + ka}, {c + ka}", f"{a}, {b}, {c + 1}", f"{ka}, {ka + 1}, {ka + 2}"],
        )
        return _mcq(
            6, 3, level,
            f"Δ with sides {a}, {b}, {c} is similar to Δ with sides:",
            opts, ans,
            "SSS similarity: all three pairs of sides in the same ratio.",
        )
    if level == "C":
        opts, ans = _shuffle_options(
            "One equal angle and the sides including it are proportional (SAS)",
            ["Two sides equal length only", "All angles 60°", "Same perimeter"],
        )
        return _mcq(6, 3, level, "SAS similarity criterion (Theorem 6.5) requires:", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options("AAA (two angles equal)", ["SSS only", "Perimeter match", "Same area"])
        return _mcq(
            6, 3, level,
            "In two triangles, ∠A = ∠D and ∠B = ∠E. Best criterion to prove similarity:",
            opts, ans,
            "Two angles equal ⇒ third pair equal ⇒ AAA.",
        )
    opts, ans = _shuffle_options(f"{side_large} cm", [f"{side_small} cm", f"{side_large + r1} cm", f"{side_small * r1 // r2} cm"])
    return _mcq(
        6, 3, level,
        f"ΔABC ~ ΔDEF with AB/DE = {r1}/{r2}. If AB = {side_small} cm, then DE = ?",
        opts, ans,
        f"DE = AB × {r2}/{r1} = {side_large}.",
    )


def _gen_u6_t4(level: str) -> dict:
    if level == "A":
        a, b = 3, 4
        c = 5
        opts, ans = _shuffle_options(f"{c} cm", [f"{a + b} cm", f"{a * b} cm", f"{c + 1} cm"])
        return _mcq(
            6, 4, level,
            f"Right triangle with legs {a} cm and {b} cm. Hypotenuse = ?",
            opts, ans,
            f"{a}² + {b}² = {c}².",
        )
    if level == "B":
        opts, ans = _shuffle_options(
            "Drop altitude on hypotenuse — creates similar right triangles",
            ["Use factorisation of a² + b²", "Measure with a tape only", "Assume c = a + b"],
        )
        return _mcq(
            6, 4, level,
            "NCERT uses similarity of triangles to prove Pythagoras theorem by:",
            opts, ans,
        )
    if level == "C":
        h_obj, sh_obj = 150, 90  # cm
        sh_pole = 60
        h_pole = h_obj * sh_pole // sh_obj
        opts, ans = _shuffle_options(f"{h_pole} cm", [f"{sh_pole} cm", f"{h_obj} cm", f"{h_pole + 30} cm"])
        return _mcq(
            6, 4, level,
            f"A {h_obj // 100} m tree casts a {sh_obj // 100} m shadow. A pole casts {sh_pole // 100} m shadow. Pole height?",
            opts, ans,
            "Similar triangles: height/shadow is constant.",
        )
    if level == "D":
        k = random.randint(2, 4)
        area_ratio = k * k
        opts, ans = _shuffle_options(f"{area_ratio}:1", [f"{k}:1", f"{2 * k}:1", f"{k + 1}:1"])
        return _mcq(
            6, 4, level,
            f"Two similar triangles have corresponding sides in ratio 1:{k}. Ratio of their areas is:",
            opts, ans,
            "Area ratio = (scale factor)².",
        )
    # multi-step: ladder against wall
    base, hyp = 6, 10
    height = 8
    opts, ans = _shuffle_options(f"{height} m", [f"{base} m", f"{hyp} m", f"{height + 2} m"])
    return _mcq(
        6, 4, level,
        f"A ladder {hyp} m long rests against a wall with foot {base} m from the wall. Height reached on wall?",
        opts, ans,
        f"Pythagoras: h² = {hyp}² − {base}² = {height}².",
    )


# ── Unit 7 helpers & generators ──


def _coord_dist(x1: int, y1: int, x2: int, y2: int) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def _section_point(x1: int, y1: int, x2: int, y2: int, m: int, n: int) -> tuple[float, float]:
    return (m * x2 + n * x1) / (m + n), (m * y2 + n * y1) / (m + n)


def _gen_u7_t1(level: str) -> dict:
    if level == "A":
        opts, ans = _shuffle_options(
            "√[(x₂ − x₁)² + (y₂ − y₁)²]",
            ["|x₂ − x₁| + |y₂ − y₁|", "(x₂ − x₁)(y₂ − y₁)", "x₂² + y₂²"],
        )
        return _mcq(7, 1, level, "Distance between (x₁, y₁) and (x₂, y₂):", opts, ans)
    if level == "B":
        a, b = random.randint(2, 9), random.randint(5, 15)
        dist = abs(b - a)
        opts, ans = _shuffle_options(f"{dist} units", [f"{a + b} units", f"{dist + 2} units", f"{abs(a - b) + 1} units"])
        return _mcq(
            7, 1, level,
            f"Distance between ({a}, 0) and ({b}, 0) on the x-axis:",
            opts, ans,
            f"|{b} − {a}| = {dist}.",
        )
    x1, y1 = random.randint(1, 5), random.randint(1, 5)
    x2, y2 = x1 + random.randint(3, 6), y1 + random.randint(4, 8)
    d = int(_coord_dist(x1, y1, x2, y2))
    if level == "C":
        opts, ans = _shuffle_options(f"{d} units", [f"{d + 3} units", f"{x2 - x1 + y2 - y1} units", f"{d - 2} units"])
        return _mcq(
            7, 1, level,
            f"Distance between ({x1}, {y1}) and ({x2}, {y2}):",
            opts, ans,
            f"√[({x2}−{x1})² + ({y2}−{y1})²] = {d}.",
        )
    if level == "D":
        dx, dy = x2 - x1, y2 - y1
        opts, ans = _shuffle_options(f"√({dx}² + {dy}²)", [f"{dx + dy}", f"{dx}² − {dy}²", f"({dx + dy})/2"])
        return _mcq(
            7, 1, level,
            f"Which expression gives distance from ({x1}, {y1}) to ({x2}, {y2})?",
            opts, ans,
        )
    # perimeter of triangle with nice distances
    pts = [(0, 0), (3, 0), (0, 4)]
    perim = 3 + 4 + 5
    opts, ans = _shuffle_options(f"{perim} units", ["12 units", "7 units", "10 units"])
    return _mcq(
        7, 1, level,
        "Perimeter of triangle with vertices (0, 0), (3, 0), (0, 4):",
        opts, ans,
        "Sides 3, 4, 5 — right triangle.",
    )


def _gen_u7_t2(level: str) -> dict:
    if level == "A":
        opts, ans = _shuffle_options(
            "((mx₂ + nx₁)/(m + n), (my₂ + ny₁)/(m + n))",
            ["((x₁ + x₂)/2, (y₁ + y₂)/2) only", "(mx₁ − nx₂, my₁ − ny₂)", "(x₂ − x₁, y₂ − y₁)"],
        )
        return _mcq(7, 2, level, "Internal section formula (ratio m : n):", opts, ans)
    x1, y1 = random.randint(0, 4), random.randint(0, 4)
    x2, y2 = x1 + random.randint(4, 8), y1 + random.randint(4, 8)
    m, n = random.randint(1, 3), random.randint(1, 3)
    px, py = _section_point(x1, y1, x2, y2, m, n)
    if level == "B":
        opts, ans = _shuffle_options(
            f"({px:g}, {py:g})",
            [f"({x1}, {y1})", f"({x2}, {y2})", f"({(x1+x2)/2:g}, {(y1+y2)/2:g})"],
        )
        return _mcq(
            7, 2, level,
            f"Point dividing ({x1}, {y1}) and ({x2}, {y2}) internally in ratio {m}:{n}:",
            opts, ans,
        )
    if level == "C":
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        opts, ans = _shuffle_options(f"({mx:g}, {my:g})", [f"({px:g}, {py:g})", f"({x1}, {y2})", f"({x2}, {y1})"])
        return _mcq(
            7, 2, level,
            f"Mid-point of ({x1}, {y1}) and ({x2}, {y2}):",
            opts, ans,
            "Mid-point is ratio 1:1.",
        )
    if level == "D":
        opts, ans = _shuffle_options(f"{m} : {n}", [f"{n} : {m}", f"{m + n} : 1", "1 : 1"])
        return _mcq(
            7, 2, level,
            f"P divides AB with A({x1}, {y1}), B({x2}, {y2}), P({px:g}, {py:g}). Ratio AP : PB ≈ ?",
            opts, ans,
        )
    east, north = random.randint(10, 50), random.randint(5, 30)
    opts, ans = _shuffle_options(f"({east}, {north})", [f"({north}, {east})", f"({east + north}, 0)", "(0, 0)"])
    return _mcq(
        7, 2, level,
        f"Town B is {east} km east and {north} km north of A (origin). Coordinates of B:",
        opts, ans,
    )


def _gen_u7_t3(level: str) -> dict:
    if level == "A":
        opts, ans = _shuffle_options(
            "Area of triangle = 0 (or points on one line)",
            ["Perimeter is zero", "All x-coordinates equal 1", "Distances are all different"],
        )
        return _mcq(7, 3, level, "Three points A, B, C are collinear when:", opts, ans)
    k = random.randint(2, 5)
    if level == "B":
        opts, ans = _shuffle_options("Yes", ["No", "Only if y equal", "Cannot tell"])
        return _mcq(
            7, 3, level,
            f"Are (1, 2), (1 + {k}, 2 + 2{k}), (1 + 2{k}, 2 + 4{k}) collinear?",
            opts, ans,
            "Constant slope 2.",
        )
    if level == "C":
        base, height = random.randint(3, 8), random.randint(3, 8)
        area = base * height // 2
        opts, ans = _shuffle_options(f"{area} sq units", [f"{base + height} sq units", f"{base * height} sq units", "0 sq units"])
        return _mcq(
            7, 3, level,
            f"Area of triangle with vertices (0, 0), ({base}, 0), (0, {height}):",
            opts, ans,
            f"Area = ½ × {base} × {height} = {area}.",
        )
    if level == "D":
        k2 = random.randint(3, 8)
        opts, ans = _shuffle_options(f"k = {2 * k2}", [f"k = {k2}", f"k = {k2 + 2}", f"k = {2 * k2 + 1}"])
        return _mcq(
            7, 3, level,
            f"If (1, 2), (3, k), (5, {2 * k2}) are collinear, then k = ?",
            opts, ans,
            "Equal slope gives k = 2 × middle term pattern.",
        )
    side = random.randint(3, 6)
    opts, ans = _shuffle_options("Square", ["Rectangle (non-square)", "Rhombus only", "Circle"])
    return _mcq(
        7, 3, level,
        f"A(0,0), B({side},0), C({side},{side}), D(0,{side}) form which quadrilateral?",
        opts, ans,
    )


def _gen_u7_t4(level: str) -> dict:
    east, north = random.randint(20, 50), random.randint(10, 25)
    dist = int(math.sqrt(east * east + north * north))
    if level == "A":
        opts, ans = _shuffle_options(f"{dist} km", [f"{east + north} km", f"{east} km", f"{north} km"])
        return _mcq(
            7, 4, level,
            f"Town B is {east} km east and {north} km north of A. Distance AB ≈ ?",
            opts, ans,
            f"√({east}² + {north}²) = {dist}.",
        )
    side = random.randint(3, 8)
    if level == "B":
        opts, ans = _shuffle_options(f"(0, {side})", [f"({side}, 0)", f"({side}, {side})", "(0, 0)"])
        return _mcq(
            7, 4, level,
            f"Isosceles right triangle with A(0,0), B({side},0), C above x-axis with AB = BC. C could be:",
            opts, ans,
        )
    x2 = random.randint(4, 10)
    if level == "C":
        opts, ans = _shuffle_options(f"({x2 // 2}, {x2 // 2})", [f"({x2}, {x2})", "(0, 0)", f"({x2 // 2}, 0)"])
        return _mcq(
            7, 4, level,
            f"Mid-point of diagonal from (0,0) to ({x2}, {x2}):",
            opts, ans,
        )
    x1, y1 = random.randint(0, 3), random.randint(0, 3)
    x2, y2 = x1 + random.randint(3, 6), y1 + random.randint(4, 7)
    d = int(_coord_dist(x1, y1, x2, y2))
    if level == "D":
        opts, ans = _shuffle_options(f"{d} units", [f"{d + 2} units", f"{x2 - x1} units", f"{y2 - y1} units"])
        return _mcq(
            7, 4, level,
            f"Distance from ({x1}, {y1}) to ({x2}, {y2}) is {d}.",
            opts, ans,
        )
    a, b = random.randint(4, 8), random.randint(4, 8)
    perim = a + b + int(math.sqrt(a * a + b * b))
    opts, ans = _shuffle_options(f"{perim} units", [f"{a + b} units", f"{2 * (a + b)} units", f"{a * b} units"])
    return _mcq(
        7, 4, level,
        f"Vertices (0,0), ({a},0), (0,{b}). Perimeter of triangle:",
        opts, ans,
    )


# ── Unit 8 helpers & generators ──

_STD_TRIG: dict[int, tuple[str, str, str]] = {
    0: ("0", "1", "0"),
    30: ("1/2", "√3/2", "1/√3"),
    45: ("1/√2", "1/√2", "1"),
    60: ("√3/2", "1/2", "√3"),
    90: ("1", "0", "undefined"),
}


def _gen_u8_t1(level: str) -> dict:
    scale = random.randint(1, 4)
    opp, adj, hyp = 3 * scale, 4 * scale, 5 * scale
    if level == "A":
        opts, ans = _shuffle_options(
            "sin θ = opposite/hypotenuse",
            ["sin θ = adjacent/hypotenuse", "sin θ = opposite/adjacent", "sin θ = hypotenuse/opposite"],
        )
        return _mcq(8, 1, level, "In right ΔABC (∠B = 90°), with respect to ∠A:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(
            "cosec θ = 1/sin θ",
            ["cosec θ = sin θ", "cosec θ = cos θ/sin θ", "cosec θ = tan θ"],
        )
        return _mcq(8, 1, level, "Correct reciprocal relation:", opts, ans)
    if level == "C":
        sin_val = f"{opp}/{hyp}"
        opts, ans = _shuffle_options(sin_val, [f"{adj}/{hyp}", f"{opp}/{adj}", f"{adj}/{opp}"])
        return _mcq(
            8, 1, level,
            f"Right triangle: opposite = {opp}, hypotenuse = {hyp}. sin θ = ?",
            opts, ans,
        )
    if level == "D":
        opts, ans = _shuffle_options(f"{adj}", [f"{opp}", f"{hyp}", f"{opp + adj}"])
        return _mcq(
            8, 1, level,
            f"cos θ = {adj}/{hyp} in a right triangle. Adjacent side if hypotenuse = {hyp}:",
            opts, ans,
        )
    opts, ans = _shuffle_options("tan θ = sin θ/cos θ", ["tan θ = cos θ/sin θ", "tan θ = sin θ + cos θ", "tan θ = 1/cos θ"])
    return _mcq(8, 1, level, "Quotient relation among ratios:", opts, ans)


def _gen_u8_t2(level: str) -> dict:
    angle = random.choice([0, 30, 45, 60, 90])
    sin_v, cos_v, tan_v = _STD_TRIG[angle]
    ratio_type = random.choice(["sin", "cos", "tan"])
    correct = {"sin": sin_v, "cos": cos_v, "tan": tan_v}[ratio_type]
    if level == "A":
        opts, ans = _shuffle_options(_STD_TRIG[30][0], [_STD_TRIG[45][0], _STD_TRIG[60][0], "1"])
        return _mcq(8, 2, level, "sin 30° = ?", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(_STD_TRIG[45][2], [_STD_TRIG[30][2], _STD_TRIG[60][2], "0"])
        return _mcq(8, 2, level, "tan 45° = ?", opts, ans)
    if level == "C":
        others = [v for k, v in zip(["sin", "cos", "tan"], _STD_TRIG[angle]) if k != ratio_type]
        opts, ans = _shuffle_options(correct, others + ["1"])
        return _mcq(8, 2, level, f"{ratio_type} {angle}° = ?", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options("sin(90° − θ) = cos θ", ["sin(90° − θ) = sin θ", "cos(90° − θ) = tan θ", "tan(90° − θ) = sec θ"])
        return _mcq(8, 2, level, "Complementary angle relation:", opts, ans)
    ang = random.choice([30, 60])
    opts, ans = _shuffle_options(_STD_TRIG[ang][2], [_STD_TRIG[30][2], _STD_TRIG[45][2], "1/2"])
    return _mcq(8, 2, level, f"tan {ang}° = ?", opts, ans)


def _gen_u8_t3(level: str) -> dict:
    if level == "A":
        opts, ans = _shuffle_options("sin²θ + cos²θ = 1", ["sin θ + cos θ = 1", "sin²θ − cos²θ = 1", "tan²θ + 1 = 0"])
        return _mcq(8, 3, level, "Fundamental trigonometric identity:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options("1 + tan²θ = sec²θ", ["1 + sin²θ = sec²θ", "tan²θ + cos²θ = 1", "sec²θ = tan²θ − 1"])
        return _mcq(8, 3, level, "Identity involving sec and tan:", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("1 + cot²θ = cosec²θ", ["cot²θ = cosec²θ + 1", "cosec²θ = 1 − cot²θ", "cot θ = tan θ"])
        return _mcq(8, 3, level, "Identity involving cosec and cot:", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options("cos²θ", ["sin²θ", "1", "tan²θ"])
        return _mcq(8, 3, level, "1 − sin²θ simplifies to:", opts, ans)
    n = random.randint(2, 9)
    opts, ans = _shuffle_options(f"{n}² − {n}² sin²θ = {n}² cos²θ", [f"{n} sin²θ = {n}", "0 = 1", f"sin²θ = {n}"])
    return _mcq(
        8, 3, level,
        f"Which simplification uses sin²θ + cos²θ = 1?",
        opts, ans,
    )


def _gen_u8_t4(level: str) -> dict:
    a, b = random.choice([(30, 60), (45, 45), (60, 30), (0, 90)])
    if level == "A":
        opts, ans = _shuffle_options("sin θ/cos θ", ["cos θ/sin θ", "1/cos θ", "sin θ × cos θ"])
        return _mcq(8, 4, level, "tan θ in terms of sin and cos:", opts, ans)
    if level == "B":
        pairs = {
            (30, 60): ("1", "1/2 + 1/2 = 1."),
            (45, 45): ("√2", "2/√2 = √2."),
            (60, 30): ("(√3+1)/2", "√3/2 + 1/2."),
            (0, 90): ("1", "0 + 1 = 1."),
        }
        ans_val, expl = pairs[(a, b)]
        opts, ans = _shuffle_options(ans_val, ["0", "√3", "1/2"])
        return _mcq(8, 4, level, f"sin {a}° + cos {b}° = ?", opts, ans, expl)
    if level == "C":
        opts, ans = _shuffle_options("1", ["sin²θ", "0", "sec²θ"])
        return _mcq(8, 4, level, "(1 − sin²θ)(1 + tan²θ) simplifies to:", opts, ans)
    if level == "D":
        val = round(1 / math.sqrt(2) + 1 / math.sqrt(2), 4)
        opts, ans = _shuffle_options(str(val), ["1", "√3", "0.5"])
        return _mcq(8, 4, level, "sin 45° + cos 45° = ?", opts, ans)
    x = random.choice([30, 45, 60])
    opts, ans = _shuffle_options(_STD_TRIG[x][0], [_STD_TRIG[x][1], _STD_TRIG[x][2], "1"])
    return _mcq(8, 4, level, f"Value of sin {x}°:", opts, ans)


# ── Unit 9 generators ──


def _gen_u9_t1(level: str) -> dict:
    angle = random.choice([30, 45, 60])
    if level == "A":
        opts, ans = _shuffle_options(
            "Line from observer's eye to object",
            ["Horizontal ground line", "Vertical height only", "Hypotenuse of any triangle"],
        )
        return _mcq(9, 1, level, "Line of sight is:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(
            "Elevation: above horizontal; Depression: below horizontal",
            ["Both mean the same", "Elevation is below horizontal", "Depression is above horizontal"],
        )
        return _mcq(9, 1, level, "Angle of elevation vs depression:", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("Angle of elevation", ["Angle of depression", "Right angle", "Straight angle"])
        return _mcq(
            9, 1, level,
            f"Student looking up at top of minar ({angle}° to horizontal) — this is:",
            opts, ans,
        )
    if level == "D":
        opts, ans = _shuffle_options(f"{angle}° elevation and {angle}° depression", ["Both 90°", "No angles", "Only depression"])
        return _mcq(
            9, 1, level,
            f"Observer on cliff sees boat at {angle}° depression; boat sees cliff at {angle}° elevation. This shows:",
            opts, ans,
            "Alternate interior angles with parallel horizontals.",
        )
    ang = random.choice([20, 40, 50])
    opts, ans = _shuffle_options("Equal to angle of elevation from object", ["Always 90°", "Twice elevation", "Zero"])
    return _mcq(
        9, 1, level,
        f"Angle of elevation of top = {ang}°. Angle of depression from top to observer equals:",
        opts, ans,
    )


def _gen_u9_t2(level: str) -> dict:
    dist = random.choice([10, 20, 30, 50, 100])
    angle = random.choice([30, 45, 60])
    if angle == 45:
        height = dist
    elif angle == 30:
        height = round(dist / math.sqrt(3))
    else:
        height = round(dist * math.sqrt(3))
    if level == "A":
        opts, ans = _shuffle_options(f"{height} m", [f"{dist} m", f"{height // 2} m", f"{height * 2} m"])
        return _mcq(
            9, 2, level,
            f"From {dist} m away, angle of elevation {angle}°. Tower height ≈ ?",
            opts, ans,
            f"Use tan {angle}°.",
        )
    if level == "B":
        opts, ans = _shuffle_options(f"{height} m", [f"{dist} m", f"{height + 10} m", f"{height - 5} m"])
        return _mcq(
            9, 2, level,
            f"Minar: observer {dist} m from foot, elevation {angle}°. Height ≈ ?",
            opts, ans,
        )
    if level == "C":
        eye = round(random.uniform(1.2, 1.8), 1)
        tower = round(eye + dist * math.tan(math.radians(angle)))
        opts, ans = _shuffle_options(f"{tower} m", [f"{tower - 5} m", f"{eye} m", f"{dist} m"])
        return _mcq(
            9, 2, level,
            f"Observer {eye} m tall, {dist} m from minar, elevation {angle}°. Minar height ≈ ?",
            opts, ans,
        )
    if level == "D":
        h = random.choice([40, 60, 80])
        opts, ans = _shuffle_options(f"{h} m", [f"{h // 2} m", f"{h * 2} m", f"{dist} m"])
        return _mcq(
            9, 2, level,
            f"Balloon at {h} m. Horizontal distance {h} m gives elevation:",
            opts, ans,
            "tan θ = 1 ⇒ 45°.",
        )
    pole, shadow = random.randint(4, 8), random.randint(4, 8)
    tower_shadow = random.randint(20, 50)
    tower_h = pole * tower_shadow // shadow
    opts, ans = _shuffle_options(f"{tower_h} m", [f"{pole} m", f"{tower_shadow} m", f"{tower_h + 10} m"])
    return _mcq(
        9, 2, level,
        f"{pole} m pole casts {shadow} m shadow. Tower casts {tower_shadow} m shadow. Tower height?",
        opts, ans,
    )


def _gen_u9_t3(level: str) -> dict:
    angle = random.choice([30, 45, 60])
    height = random.choice([10, 20, 50])
    if angle == 45:
        dist = height
    elif angle == 30:
        dist = round(height * math.sqrt(3))
    else:
        dist = round(height / math.sqrt(3))
    if level == "A":
        opts, ans = _shuffle_options(f"{dist} m", [f"{height} m", f"{dist // 2} m", f"{dist * 2} m"])
        return _mcq(
            9, 3, level,
            f"Width of river if height {height} m, angle {angle}° across:",
            opts, ans,
        )
    if level == "B":
        opts, ans = _shuffle_options(f"{dist} m", [f"{height} m", f"{dist + 5} m", f"{dist - 3} m"])
        return _mcq(
            9, 3, level,
            f"Ladder reaches {height} m on wall, elevation {angle}°. Foot from wall ≈ ?",
            opts, ans,
        )
    if level == "C":
        d1, d2 = random.randint(4, 12), random.randint(2, 8)
        opts, ans = _shuffle_options(f"{abs(d1 - d2)} m apart", [f"{d1 + d2} m", f"{d1} m", f"{d2} m"])
        return _mcq(
            9, 3, level,
            f"Boat moves from {d1} m to {d2} m from cliff. Distance moved ≈ ?",
            opts, ans,
        )
    if level == "D":
        opts, ans = _shuffle_options(f"{height} m", [f"{dist} m", f"{height * 2} m", f"{height // 2} m"])
        return _mcq(
            9, 3, level,
            f"From {height} m building, depression of car is {angle}°. Car distance ≈ ?",
            opts, ans,
        )
    base = random.randint(50, 150)
    opts, ans = _shuffle_options(f"{base} m", [f"{base // 2} m", f"{base * 2} m", f"{height} m"])
    return _mcq(
        9, 3, level,
        f"Two observers {base} m apart see pole at {angle}° and 45°. Setup uses:",
        opts, ans,
    )


def _gen_u9_t4(level: str) -> dict:
    pole, shadow = random.randint(3, 9), random.randint(3, 9)
    if level == "A":
        opts, ans = _shuffle_options("Draw right triangle with known angle", ["Use AP formula", "Only measure with tape", "Ignore horizontal"])
        return _mcq(9, 4, level, "First step in a heights-and-distances problem:", opts, ans)
    if level == "B":
        small_pole = pole // 2 + 1
        ans_val = max(1, small_pole * shadow // pole)
        opts, ans = _shuffle_options(f"{ans_val} m", [f"{pole} m", f"{shadow} m", f"{ans_val + 2} m"])
        return _mcq(
            9, 4, level,
            f"{pole} m pole casts {shadow} m shadow. A {small_pole} m pole casts shadow ≈ ?",
            opts, ans,
            "Same ratio height/shadow.",
        )
    h = random.choice([15, 20, 30])
    dist = round(h / math.tan(math.radians(30)))
    if level == "C":
        opts, ans = _shuffle_options(f"{dist} m", [f"{h} m", f"{dist // 2} m", f"{dist * 2} m"])
        return _mcq(
            9, 4, level,
            f"From window {h} m high, depression 30° to boat. Distance ≈ ?",
            opts, ans,
        )
    if level == "D":
        alt = random.choice([500, 1000, 1500])
        opts, ans = _shuffle_options(f"{alt} m", [f"{alt // 2} m", f"{alt * 2} m", f"{h} m"])
        return _mcq(
            9, 4, level,
            f"Aeroplane at {alt} m; depression 45° gives horizontal distance ≈ ?",
            opts, ans,
        )
    lh = random.choice([50, 75, 100])
    opts, ans = _shuffle_options(f"{round(lh / math.sqrt(3))} m", [f"{lh} m", f"{lh * 2} m", f"{lh // 2} m"])
    return _mcq(
        9, 4, level,
        f"Lighthouse {lh} m high; elevation 30° from boat. Distance ≈ ?",
        opts, ans,
    )


# ── Unit 10 generators ──

_TANGENT_PAIRS = [(3, 5, 4), (5, 13, 12), (6, 10, 8), (7, 25, 24), (8, 17, 15), (9, 15, 12)]


def _tangent_len(op: int, r: int) -> int:
    return int(math.sqrt(op * op - r * r))


def _gen_u10_t1(level: str) -> dict:
    r, op, pq = random.choice(_TANGENT_PAIRS)
    if level == "A":
        opts, ans = _shuffle_options(
            "Intersects the circle at exactly one point",
            ["Does not meet the circle", "Meets at two points", "Passes through centre always"],
        )
        return _mcq(10, 1, level, "A tangent to a circle:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(
            "Radius is perpendicular to tangent at point of contact",
            ["Radius is parallel to tangent", "Tangent equals diameter", "Angle is 45° always"],
        )
        return _mcq(10, 1, level, "Theorem 10.1:", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("Secant", ["Tangent", "Non-intersecting line", "Diameter"])
        return _mcq(
            10, 1, level,
            "Line cutting a circle at two points is called a:",
            opts, ans,
        )
    if level == "D":
        opts, ans = _shuffle_options(f"{pq} cm", [f"{op} cm", f"{r} cm", f"{pq + r} cm"])
        return _mcq(
            10, 1, level,
            f"Tangent from Q with OQ = {op} cm, radius = {r} cm. Length PQ = ?",
            opts, ans,
            f"PQ = √({op}² − {r}²) = {pq}.",
        )
    opts, ans = _shuffle_options(f"{pq} cm", [f"{op} cm", f"{r + pq} cm", f"{r} cm"])
    return _mcq(
        10, 1, level,
        f"Radius {r} cm, point {op} cm from centre. Tangent length = ?",
        opts, ans,
    )


def _gen_u10_t2(level: str) -> dict:
    angle = random.choice([30, 45, 60, 90])
    if level == "A":
        opts, ans = _shuffle_options("No tangent from a point inside the circle", ["Two tangents from inside", "One tangent from inside", "Infinite tangents from inside"])
        return _mcq(10, 2, level, "From a point inside a circle:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options("Exactly two tangents", ["One tangent", "No tangent", "Infinite tangents"])
        return _mcq(10, 2, level, "From an external point to a circle:", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("PQ = PR", ["PQ = 2PR", "PQ ⊥ PR", "PQ parallel PR"])
        return _mcq(
            10, 2, level,
            "Tangents PQ and PR from external point P (Theorem 10.2):",
            opts, ans,
        )
    if level == "D":
        half = angle // 2
        opts, ans = _shuffle_options(f"{half}°", ["90°", f"{angle}°", f"{angle + 30}°"])
        return _mcq(
            10, 2, level,
            f"Two tangents from P make {angle}° at P. Angle between OP and either tangent is:",
            opts, ans,
            "OP bisects ∠QPR.",
        )
    opts, ans = _shuffle_options("2", ["0", "1", "5"])
    return _mcq(10, 2, level, "Maximum tangents from an external point:", opts, ans)


def _gen_u10_t3(level: str) -> dict:
    r, op, pq = random.choice(_TANGENT_PAIRS)
    if level == "A":
        opts, ans = _shuffle_options("√(OP² − r²)", ["OP + r", "OP − r", "r² + OP²"])
        return _mcq(10, 3, level, "Length of tangent from point P at distance OP from centre:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(f"{pq} cm", [f"{op} cm", f"{r} cm", f"{pq + 2} cm"])
        return _mcq(
            10, 3, level,
            f"Radius {r} cm, OP = {op} cm. Tangent length = ?",
            opts, ans,
        )
    if level == "C":
        opts, ans = _shuffle_options(f"{r} cm", [f"{op} cm", f"{pq} cm", f"{r + op} cm"])
        return _mcq(
            10, 3, level,
            f"Tangent length {pq} cm from point {op} cm from centre. Radius = ?",
            opts, ans,
            f"r = √({op}² − {pq}²) = {r}.",
        )
    if level == "D":
        opts, ans = _shuffle_options("AP = BP", ["AB = AP", "OP = AP", "AP = 2BP"])
        return _mcq(
            10, 3, level,
            "Chord of larger circle touches smaller concentric circle at P. Then:",
            opts, ans,
        )
    r2, op2, tl2 = random.choice(_TANGENT_PAIRS)
    opts, ans = _shuffle_options(f"{tl2} cm", [f"{op2} cm", f"{r2} cm", f"{tl2 + 3} cm"])
    return _mcq(
        10, 3, level,
        f"From point {op2} cm from centre, radius {r2} cm. Tangent length = ?",
        opts, ans,
    )


def _gen_u10_t4(level: str) -> dict:
    r, op, pq = random.choice(_TANGENT_PAIRS)
    if level == "A":
        opts, ans = _shuffle_options("Line touching circle at one point only", ["Line through centre", "Any chord", "Diameter only"])
        return _mcq(10, 4, level, "Identify the tangent in a diagram:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options("RHS congruence of ΔOQP and ΔORP", ["SSA always", "ASA with radius", "No proof needed"])
        return _mcq(
            10, 4, level,
            "Equal tangents from P are proved using:",
            opts, ans,
        )
    if level == "C":
        opts, ans = _shuffle_options("Bisected at P", ["Doubled at P", "Unchanged", "Perpendicular only"])
        return _mcq(
            10, 4, level,
            "Chord of larger circle touching smaller concentric circle is:",
            opts, ans,
        )
    if level == "D":
        opts, ans = _shuffle_options("∠PTQ = 2 ∠OPQ", ["∠PTQ = ∠OPQ", "∠PTQ = 90° − ∠OPQ", "No relation"])
        return _mcq(
            10, 4, level,
            "Two tangents TP, TQ from external T. Then:",
            opts, ans,
        )
    opts, ans = _shuffle_options(f"{pq} cm", [f"{op} cm", f"{r} cm", f"{pq + r} cm"])
    return _mcq(
        10, 4, level,
        f"Combined: radius {r} cm, OQ = {op} cm. Tangent PQ length = ?",
        opts, ans,
    )


# ── Unit 11 generators ──

def _sector_area(r: int, angle: int) -> float:
    return round(angle / 360 * math.pi * r * r, 2)


def _arc_length(r: int, angle: int) -> float:
    return round(angle / 360 * 2 * math.pi * r, 2)


def _gen_u11_t1(level: str) -> dict:
    r = random.choice([7, 14, 21, 28, 35])
    angle = random.choice([30, 45, 60, 90, 120, 180])
    area = _sector_area(r, angle)
    if level == "A":
        opts, ans = _shuffle_options("(θ/360) × πr²", ["θ × πr²", "2πr × θ", "πr² only"])
        return _mcq(11, 1, level, "Area of a sector of angle θ and radius r:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(f"{area} cm²", [f"{area * 2} cm²", f"{r * r} cm²", f"{area / 2} cm²"])
        return _mcq(11, 1, level, f"Sector: r = {r} cm, θ = {angle}°. Area ≈ ?", opts, ans, f"(θ/360)πr².")
    if level == "C":
        opts, ans = _shuffle_options(f"{angle}°", ["90°", "180°", f"{angle + 30}°"])
        return _mcq(11, 1, level, f"Sector area ≈ {area} cm², r = {r} cm. Angle θ ≈ ?", opts, ans)
    if level == "D":
        semi = round(math.pi * r * r / 2, 2)
        opts, ans = _shuffle_options(f"{semi} cm²", [f"{r * r} cm²", f"{area} cm²", f"{semi * 2} cm²"])
        return _mcq(11, 1, level, f"Area of semicircle, radius {r} cm ≈ ?", opts, ans)
    quad = round(math.pi * r * r / 4, 2)
    opts, ans = _shuffle_options(f"{quad} cm²", [f"{area} cm²", f"{r} cm²", f"{quad * 2} cm²"])
    return _mcq(11, 1, level, f"Area of quadrant, radius {r} cm ≈ ?", opts, ans)


def _gen_u11_t2(level: str) -> dict:
    r = random.choice([7, 14, 21, 28])
    angle = random.choice([60, 90, 120, 180])
    arc = _arc_length(r, angle)
    if level == "A":
        opts, ans = _shuffle_options("(θ/360) × 2πr", ["(θ/360) × πr²", "2πr", "πr"])
        return _mcq(11, 2, level, "Length of an arc subtending angle θ at centre:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(f"{arc} cm", [f"{arc * 2} cm", f"{2 * math.pi * r:.1f} cm", f"{r} cm"])
        return _mcq(11, 2, level, f"Arc length: r = {r} cm, θ = {angle}° ≈ ?", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options(f"{r} cm", [f"{r * 2} cm", f"{arc} cm", f"{r // 2} cm"])
        return _mcq(11, 2, level, f"Arc length {arc} cm for θ = {angle}°. Radius ≈ ?", opts, ans)
    perim = round(arc + 2 * r, 2)
    if level == "D":
        opts, ans = _shuffle_options(f"{perim} cm", [f"{arc} cm", f"{2 * r} cm", f"{perim + r} cm"])
        return _mcq(11, 2, level, f"Perimeter of sector (r = {r} cm, θ = {angle}°) ≈ ?", opts, ans)
    opts, ans = _shuffle_options(f"{arc + _arc_length(r, 180 - angle):.1f} cm", [f"{arc} cm", f"{2 * arc} cm", f"{r} cm"])
    return _mcq(11, 2, level, f"Two arcs on same circle: {angle}° and {180 - angle}° (r = {r}). Total arc ≈ ?", opts, ans)


def _gen_u11_t3(level: str) -> dict:
    r = random.choice([7, 14, 21])
    angle = random.choice([60, 90, 120])
    sector = _sector_area(r, angle)
    tri = round(r * r * math.sin(math.radians(angle)) / 2, 2)
    segment = round(sector - tri, 2)
    if level == "A":
        opts, ans = _shuffle_options("Sector area − area of triangle", ["πr² − sector", "Arc length × r", "2 × sector"])
        return _mcq(11, 3, level, "Area of a segment equals:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(f"{segment} cm²", [f"{sector} cm²", f"{tri} cm²", f"{segment * 2} cm²"])
        return _mcq(11, 3, level, f"Minor segment: r = {r} cm, θ = {angle}°. Area ≈ ?", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("Major segment", ["Minor segment", "Semicircle", "Quadrant"])
        return _mcq(11, 3, level, f"Segment larger than semicircle (θ = {angle}°) is:", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options(f"{segment} cm²", [f"{sector} cm²", f"{tri} cm²", f"{r} cm²"])
        return _mcq(11, 3, level, f"Chord subtends {angle}° at centre, r = {r} cm. Minor segment ≈ ?", opts, ans)
    opts, ans = _shuffle_options(f"{round(math.pi * r * r - segment, 2)} cm²", [f"{segment} cm²", f"{sector} cm²", f"{tri} cm²"])
    return _mcq(11, 3, level, f"Circle r = {r} cm; minor segment ≈ {segment} cm². Major segment ≈ ?", opts, ans)


def _gen_u11_t4(level: str) -> dict:
    r = random.choice([7, 14, 21])
    side = 2 * r
    sq = side * side
    quad_area = round(math.pi * r * r / 4, 2)
    if level == "A":
        shaded = round(sq - 4 * quad_area, 2)
        opts, ans = _shuffle_options(f"{shaded} cm²", [f"{sq} cm²", f"{quad_area} cm²", f"{4 * quad_area} cm²"])
        return _mcq(11, 4, level, f"Square side {side} cm with four quadrants (r = {r}) cut from corners. Shaded (centre) ≈ ?", opts, ans)
    if level == "B":
        outer, inner = random.choice([(14, 7), (21, 14), (28, 21)])
        ring = round(math.pi * (outer * outer - inner * inner), 2)
        opts, ans = _shuffle_options(f"{ring} cm²", [f"{math.pi * outer * outer:.0f} cm²", f"{inner} cm²", f"{ring / 2} cm²"])
        return _mcq(11, 4, level, f"Ring: outer r = {outer} cm, inner r = {inner} cm. Area ≈ ?", opts, ans)
    if level == "C":
        brooch = round(6 * quad_area, 2)
        opts, ans = _shuffle_options(f"{brooch} cm²", [f"{quad_area} cm²", f"{sq} cm²", f"{brooch * 2} cm²"])
        return _mcq(11, 4, level, f"Brooch: 6 equal quadrants, each r = {r} cm. Total area ≈ ?", opts, ans)
    if level == "D":
        ring = round(math.pi * (r * 2) ** 2 - math.pi * r * r, 2)
        opts, ans = _shuffle_options(f"{ring} cm²", [f"{math.pi * r * r:.0f} cm²", f"{r} cm²", f"{ring * 2} cm²"])
        return _mcq(11, 4, level, f"Annulus: outer R = {2 * r} cm, inner r = {r} cm. Area ≈ ?", opts, ans)
    combined = round(_sector_area(r, 60) + _sector_area(r, 120), 2)
    opts, ans = _shuffle_options(f"{combined} cm²", [f"{_sector_area(r, 60)} cm²", f"{r} cm²", f"{combined * 2} cm²"])
    return _mcq(11, 4, level, f"Two sectors same r = {r}: 60° + 120°. Combined area ≈ ?", opts, ans)


# ── Unit 12 generators ──

def _gen_u12_t1(level: str) -> dict:
    r, h = random.choice([(3, 7), (7, 10), (14, 5), (5, 12)])
    if level == "A":
        opts, ans = _shuffle_options("2πrh", ["πr²h", "πrl", "4πr²"])
        return _mcq(12, 1, level, "Curved surface area of a right circular cylinder:", opts, ans)
    if level == "B":
        csa = round(2 * math.pi * r * h, 2)
        opts, ans = _shuffle_options(f"{csa} cm²", [f"{math.pi * r * r * h:.0f} cm²", f"{2 * r * h} cm²", f"{csa * 2} cm²"])
        return _mcq(12, 1, level, f"Cylinder: r = {r} cm, h = {h} cm. CSA ≈ ?", opts, ans)
    if level == "C":
        vol_cone = round(math.pi * r * r * h / 3, 2)
        opts, ans = _shuffle_options(f"{vol_cone} cm³", [f"{math.pi * r * r * h:.0f} cm³", f"{2 * vol_cone} cm³", f"{r * h} cm³"])
        return _mcq(12, 1, level, f"Cone: r = {r} cm, h = {h} cm. Volume ≈ ?", opts, ans)
    if level == "D":
        sa_sphere = round(4 * math.pi * r * r, 2)
        opts, ans = _shuffle_options(f"{sa_sphere} cm²", [f"{2 * math.pi * r * r:.0f} cm²", f"{(4/3) * math.pi * r ** 3:.0f} cm³", f"{sa_sphere * 2} cm²"])
        return _mcq(12, 1, level, f"Sphere radius {r} cm. Surface area ≈ ?", opts, ans)
    vol_sph = round(4 * math.pi * r ** 3 / 3, 2)
    opts, ans = _shuffle_options(f"{vol_sph} cm³", [f"{4 * math.pi * r * r:.0f} cm²", f"{vol_sph * 3} cm³", f"{r ** 3} cm³"])
    return _mcq(12, 1, level, f"Sphere r = {r} cm. Volume ≈ ?", opts, ans)


def _gen_u12_t2(level: str) -> dict:
    r, h = random.choice([(3, 6), (7, 14), (5, 10)])
    if level == "A":
        opts, ans = _shuffle_options("Exclude the common circular face", ["Add all faces twice", "Only curved areas", "Ignore hemisphere"])
        return _mcq(12, 2, level, "Cylinder surmounted by hemisphere — for total SA:", opts, ans)
    if level == "B":
        csa_cyl = 2 * math.pi * r * h
        sa_hemi = 2 * math.pi * r * r
        base = math.pi * r * r
        total = round(csa_cyl + sa_hemi + base, 2)
        opts, ans = _shuffle_options(f"{total} cm²", [f"{csa_cyl:.0f} cm²", f"{sa_hemi:.0f} cm²", f"{total * 2} cm²"])
        return _mcq(12, 2, level, f"Toy: cylinder r = {r}, h = {h} + hemisphere on top. Total SA ≈ ?", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("CSA of cone + CSA of cylinder − base overlap", ["Sum all TSA", "Volume only", "2πr(h + l)"])
        return _mcq(12, 2, level, "Cone on cylinder — visible surface area uses:", opts, ans)
    if level == "D":
        outer_r, inner_r, h2 = r + 2, r, h
        hollow_csa = round(2 * math.pi * (outer_r + inner_r) * h2, 2)
        opts, ans = _shuffle_options(f"{hollow_csa} cm²", [f"{2 * math.pi * outer_r * h2:.0f} cm²", f"{h2} cm²", f"{hollow_csa / 2} cm²"])
        return _mcq(12, 2, level, f"Hollow cylinder: outer r = {outer_r}, inner r = {inner_r}, h = {h2}. CSA ≈ ?", opts, ans)
    total = round(2 * math.pi * r * h + 2 * math.pi * r * r, 2)
    opts, ans = _shuffle_options(f"{total} cm²", [f"{2 * math.pi * r * h:.0f} cm²", f"{math.pi * r * r:.0f} cm²", f"{total / 2} cm²"])
    return _mcq(12, 2, level, f"Closed cylinder r = {r}, h = {h}. Total SA ≈ ?", opts, ans)


def _gen_u12_t3(level: str) -> dict:
    r, h = random.choice([(3, 7), (7, 14), (5, 9)])
    if level == "A":
        opts, ans = _shuffle_options("Add individual volumes", ["Multiply SA and h", "Average of volumes", "Subtract smaller solid"])
        return _mcq(12, 3, level, "Volume of a solid made of two joined solids:", opts, ans)
    if level == "B":
        vol = round(math.pi * r * r * h / 3 + 2 * math.pi * r ** 3 / 3, 2)
        opts, ans = _shuffle_options(f"{vol} cm³", [f"{math.pi * r * r * h / 3:.0f} cm³", f"{4 * math.pi * r ** 3 / 3:.0f} cm³", f"{vol * 2} cm³"])
        return _mcq(12, 3, level, f"Toy: cone h = {h}, r = {r} + hemisphere. Volume ≈ ?", opts, ans)
    if level == "C":
        outer, inner, ht = r + 3, r, h
        hollow = round(math.pi * (outer ** 2 - inner ** 2) * ht, 2)
        opts, ans = _shuffle_options(f"{hollow} cm³", [f"{math.pi * outer ** 2 * ht:.0f} cm³", f"{inner} cm³", f"{hollow * 2} cm³"])
        return _mcq(12, 3, level, f"Hollow cylinder: outer r = {outer}, inner r = {inner}, h = {ht}. Volume ≈ ?", opts, ans)
    if level == "D":
        vol_cyl = math.pi * r * r * h
        opts, ans = _shuffle_options(f"{vol_cyl:.0f} cm³", [f"{vol_cyl / 1000:.2f} L", f"{r} cm³", f"{vol_cyl * 2:.0f} cm³"])
        return _mcq(12, 3, level, f"Cylindrical tank r = {r} cm, h = {h} cm holds water ≈ ? cm³", opts, ans)
    v1 = round(4 * math.pi * r ** 3 / 3, 2)
    v2 = round(math.pi * r * r * h, 2)
    opts, ans = _shuffle_options(f"{v1 + v2:.0f} cm³", [f"{v1} cm³", f"{v2} cm³", f"{r} cm³"])
    return _mcq(12, 3, level, f"Sphere r = {r} + cylinder same r, h = {h}. Combined volume ≈ ?", opts, ans)


def _gen_u12_t4(level: str) -> dict:
    r1, r2, h = random.choice([(7, 3, 10), (14, 7, 12), (10, 5, 8)])
    if level == "A":
        opts, ans = _shuffle_options("Portion of a cone between two parallel cuts", ["Full cone", "Cylinder only", "Hemisphere cut"])
        return _mcq(12, 4, level, "A frustum of a cone is:", opts, ans)
    if level == "B":
        vol = round(math.pi * h * (r1 * r1 + r1 * r2 + r2 * r2) / 3, 2)
        opts, ans = _shuffle_options(f"{vol} cm³", [f"{math.pi * r1 * r1 * h / 3:.0f} cm³", f"{h} cm³", f"{vol * 2} cm³"])
        return _mcq(12, 4, level, f"Frustum: radii {r1} & {r2} cm, height {h} cm. Volume ≈ ?", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("Volume stays same (conservation)", ["Volume doubles", "SA unchanged", "Shape irrelevant"])
        return _mcq(12, 4, level, "Metallic sphere melted and recast into cylinder. Which is true?", opts, ans)
    if level == "D":
        k = random.choice([2, 3])
        opts, ans = _shuffle_options(f"{k ** 3}", [f"{k}", f"{k ** 2}", f"{2 * k}"])
        return _mcq(12, 4, level, f"Two similar solids; linear scale factor {k}. Volume ratio = ?", opts, ans)
    bucket = round(math.pi * h * (r1 * r1 + r1 * r2 + r2 * r2) / 3, 2)
    opts, ans = _shuffle_options(f"{bucket} cm³", [f"{math.pi * r1 ** 2 * h:.0f} cm³", f"{r1 - r2} cm³", f"{bucket / 2} cm³"])
    return _mcq(12, 4, level, f"Bucket (frustum): top r = {r1}, bottom r = {r2}, depth {h} cm. Capacity ≈ ?", opts, ans)


# ── Unit 13 generators ──

def _gen_u13_t1(level: str) -> dict:
    lo, hi = random.choice([(10, 20), (20, 30), (30, 40)])
    mid = (lo + hi) // 2
    if level == "A":
        opts, ans = _shuffle_options(f"{mid}", [f"{lo}", f"{hi}", f"{lo + hi}"])
        return _mcq(13, 1, level, f"Class mark for interval {lo}–{hi}:", opts, ans, "(lower + upper)/2")
    freqs = [random.randint(2, 8) for _ in range(4)]
    classes = [(10, 20), (20, 30), (30, 40), (40, 50)]
    fx = sum(f * ((a + b) // 2) for f, (a, b) in zip(freqs, classes))
    sf = sum(freqs)
    mean = round(fx / sf, 1)
    if level == "B":
        opts, ans = _shuffle_options(f"{mean}", [f"{mean + 5}", f"{sf}", f"{fx}"])
        return _mcq(13, 1, level, f"Grouped data: Σfixi = {fx}, Σfi = {sf}. Mean ≈ ?", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("Assumed mean a and deviations di", ["Only midpoints", "No frequencies", "Median class"])
        return _mcq(13, 1, level, "Assumed mean method uses:", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options("ui = (xi − a)/h step widths", ["xi only", "cf only", "Mode formula"])
        return _mcq(13, 1, level, "Step-deviation method uses:", opts, ans)
    missing_f = random.randint(3, 7)
    opts, ans = _shuffle_options(f"{missing_f}", [f"{missing_f + 2}", f"{sf}", f"1"])
    return _mcq(13, 1, level, f"Mean = {mean}; total frequency {sf + missing_f - sum(freqs[:1])}. Find missing f in first class ≈ ?", opts, ans)


def _gen_u13_t2(level: str) -> dict:
    n = random.choice([40, 50, 60, 80])
    half = n // 2
    if level == "A":
        opts, ans = _shuffle_options("Class where cf crosses n/2", ["Highest frequency class", "First class", "Last class"])
        return _mcq(13, 2, level, "Median class is the:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options("l + ((n/2 − cf)/f) × h", ["Σfixi/Σfi", "l + ((f1−f0)/(2f1−f0−f2))h", "cf only"])
        return _mcq(13, 2, level, "Median of grouped data formula:", opts, ans)
    l, f, cf, h = 20, 12, 18, 10
    median = round(l + ((half - cf) / f) * h, 1)
    if level == "C":
        opts, ans = _shuffle_options(f"{median}", [f"{l}", f"{l + h}", f"{half}"])
        return _mcq(13, 2, level, f"n = {n}, median class lower l = {l}, f = {f}, cf = {cf}, h = {h}. Median ≈ ?", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options("Mean affected by extremes; median more robust", ["Always equal", "Median always larger", "Mean always larger"])
        return _mcq(13, 2, level, "Compare mean and median for skewed data:", opts, ans)
    opts, ans = _shuffle_options(f"{f}", [f"{cf}", f"{l}", f"{h}"])
    return _mcq(13, 2, level, f"Median = {median}, known l, cf, h. Frequency f of median class ≈ ?", opts, ans)


def _gen_u13_t3(level: str) -> dict:
    if level == "A":
        opts, ans = _shuffle_options("Class with maximum frequency", ["Lowest class", "Median class", "Last class"])
        return _mcq(13, 3, level, "Modal class is the:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options("l + ((f1−f0)/(2f1−f0−f2)) × h", ["Σfixi/Σfi", "n/2 formula", "cf graph"])
        return _mcq(13, 3, level, "Mode formula for grouped data:", opts, ans)
    l, f1, f0, f2, h = 30, 15, 10, 8, 10
    mode = round(l + ((f1 - f0) / (2 * f1 - f0 - f2)) * h, 1)
    if level == "C":
        opts, ans = _shuffle_options(f"{mode}", [f"{l}", f"{l + h}", f"{f1}"])
        return _mcq(13, 3, level, f"Modal class l = {l}, f1 = {f1}, f0 = {f0}, f2 = {f2}, h = {h}. Mode ≈ ?", opts, ans)
    if level == "D":
        mean_val, median_val = 35.0, 33.0
        emp = round(3 * median_val - 2 * mean_val, 1)
        opts, ans = _shuffle_options(f"{emp}", [f"{mean_val}", f"{median_val}", f"{mean_val + median_val}"])
        return _mcq(13, 3, level, f"Mean = {mean_val}, median = {median_val}. Mode (empirical) ≈ ?", opts, ans)
    opts, ans = _shuffle_options(f"{mode}", [f"{l + h}", f"{f0}", f"{2 * f1}"])
    return _mcq(13, 3, level, f"Grouped data: modal class starts at {l}. Mode ≈ ?", opts, ans)


def _gen_u13_t4(level: str) -> dict:
    if level == "A":
        opts, ans = _shuffle_options("Less-than type: cf on y-axis", ["More-than only", "Frequency on x-axis only", "No cf"])
        return _mcq(13, 4, level, "Less-than ogive plots:", opts, ans)
    if level == "B":
        freqs = [5, 8, 12, 6]
        cf = []
        s = 0
        for f in freqs:
            s += f
            cf.append(s)
        opts, ans = _shuffle_options(str(cf[-1]), [str(freqs[-1]), str(sum(freqs) + 1), "0"])
        return _mcq(13, 4, level, f"Frequencies {freqs}. Total (last cf) = ?", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("x-coordinate of intersection of ogives", ["Maximum frequency", "Class width", "First cf"])
        return _mcq(13, 4, level, "Median from ogives is read at:", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options("Steep rise → many observations in that interval", ["Always decreasing", "Mean equals mode", "Zero frequency"])
        return _mcq(13, 4, level, "On a less-than ogive, a steep rise indicates:", opts, ans)
    n = 50
    opts, ans = _shuffle_options(f"{n // 2}", [f"{n}", f"{n // 4}", "0"])
    return _mcq(13, 4, level, f"Total n = {n}. Median position on ogive is at cf = ?", opts, ans)


# ── Unit 14 generators ──

def _gen_u14_t1(level: str) -> dict:
    fav, total = random.choice([(1, 6), (2, 6), (3, 52), (4, 52), (1, 2)])
    p = Fraction(fav, total)
    if level == "A":
        opts, ans = _shuffle_options("Favourable outcomes / Total outcomes", ["Total / Favourable", "1 − P(E)", "Always 1/2"])
        return _mcq(14, 1, level, "Classical probability P(E) =", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(str(p), [str(Fraction(total - fav, total)), "0", "1"])
        return _mcq(14, 1, level, f"Fair die/cards: {fav} favourable out of {total}. P(E) = ?", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("0", ["1", "1/2", "Undefined"])
        return _mcq(14, 1, level, "Probability of impossible event:", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options("Equally likely", ["Always 0", "Always 1", "Complementary"])
        return _mcq(14, 1, level, "Classical probability assumes outcomes are:", opts, ans)
    p2 = Fraction(fav + 1, total)
    opts, ans = _shuffle_options(str(p2), [str(p), "1", "0"])
    return _mcq(14, 1, level, f"Bag: {fav + 1} red out of {total} identical balls. P(red) = ?", opts, ans)


def _gen_u14_t2(level: str) -> dict:
    p = random.choice([Fraction(1, 6), Fraction(1, 4), Fraction(2, 5), Fraction(3, 8)])
    comp = Fraction(1) - p
    if level == "A":
        opts, ans = _shuffle_options("1 − P(E)", ["P(E) − 1", "1 + P(E)", "P(E)/2"])
        return _mcq(14, 2, level, "P(not E) equals:", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options(str(comp), [str(p), "0", "1"])
        return _mcq(14, 2, level, f"P(E) = {p}. P(not E) = ?", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options(str(Fraction(5, 6)), [str(Fraction(1, 6)), "0", "1"])
        return _mcq(14, 2, level, "Die: P(at least one six) in one throw uses complement with P(no six) = 5/6?", opts, ans)
    if level == "D":
        rain_p = Fraction(3, 10)
        opts, ans = _shuffle_options(str(Fraction(1) - rain_p), [str(rain_p), "0", "1"])
        return _mcq(14, 2, level, f"P(rain) = {rain_p}. P(no rain) = ?", opts, ans)
    opts, ans = _shuffle_options(str(comp), [str(p), str(p * 2), "1"])
    return _mcq(14, 2, level, f"P(win) = {p}. P(lose) = ?", opts, ans)


def _gen_u14_t3(level: str) -> dict:
    if level == "A":
        opts, ans = _shuffle_options("1/6", ["1/3", "1/2", "1/36"])
        return _mcq(14, 3, level, "One fair die: P(getting 4) = ?", opts, ans)
    if level == "B":
        opts, ans = _shuffle_options("1/36", ["1/6", "1/12", "2/36"])
        return _mcq(14, 3, level, "Two dice: P(sum = 2) = ?", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("1/52", ["1/13", "1/4", "4/52"])
        return _mcq(14, 3, level, "One card from standard deck: P(specific card) = ?", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options("3/13", ["1/13", "12/52", "4/52"])
        return _mcq(14, 3, level, "P(drawing a king from deck) = ?", opts, ans)
    opts, ans = _shuffle_options("1/2", ["1/4", "26/52", "13/52"])
    return _mcq(14, 3, level, "P(red card from well-shuffled deck) = ?", opts, ans)


def _gen_u14_t4(level: str) -> dict:
    red, blue = random.choice([(3, 5), (4, 6), (5, 3)])
    total = red + blue
    if level == "A":
        opts, ans = _shuffle_options(f"{red}/{total}", [f"{blue}/{total}", "1/2", "0"])
        return _mcq(14, 4, level, f"Bag: {red} red, {blue} blue balls. P(red) = ?", opts, ans)
    if level == "B":
        p = Fraction(red, total) * Fraction(red - 1, total - 1)
        opts, ans = _shuffle_options(str(p), [str(Fraction(red, total)), "1", "0"])
        return _mcq(14, 4, level, f"Two draws without replacement from bag ({red}R, {blue}B). P(both red) = ?", opts, ans)
    if level == "C":
        opts, ans = _shuffle_options("Favourable area / Total area", ["Perimeter ratio", "Always 1/2", "Volume ratio"])
        return _mcq(14, 4, level, "Geometric probability on a region uses:", opts, ans)
    if level == "D":
        opts, ans = _shuffle_options("1/2", ["1/4", "1", "0"])
        return _mcq(14, 4, level, "Two fair coins tossed. P(exactly one head) = ?", opts, ans)
    opts, ans = _shuffle_options(f"{blue}/{total}", [f"{red}/{total}", "1", "0"])
    return _mcq(14, 4, level, f"Bag {red} red, {blue} blue. P(blue) = ?", opts, ans)


GENERATORS: dict[tuple[int, int], callable] = {
    (1, 1): _gen_u1_t1,
    (1, 2): _gen_u1_t2,
    (1, 3): _gen_u1_t3,
    (1, 4): _gen_u1_t4,
    (2, 1): _gen_u2_t1,
    (2, 2): _gen_u2_t2,
    (2, 3): _gen_u2_t3,
    (2, 4): _gen_u2_t4,
    (3, 1): _gen_u3_t1,
    (3, 2): _gen_u3_t2,
    (3, 3): _gen_u3_t3,
    (3, 4): _gen_u3_t4,
    (4, 1): _gen_u4_t1,
    (4, 2): _gen_u4_t2,
    (4, 3): _gen_u4_t3,
    (4, 4): _gen_u4_t4,
    (5, 1): _gen_u5_t1,
    (5, 2): _gen_u5_t2,
    (5, 3): _gen_u5_t3,
    (5, 4): _gen_u5_t4,
    (6, 1): _gen_u6_t1,
    (6, 2): _gen_u6_t2,
    (6, 3): _gen_u6_t3,
    (6, 4): _gen_u6_t4,
    (7, 1): _gen_u7_t1,
    (7, 2): _gen_u7_t2,
    (7, 3): _gen_u7_t3,
    (7, 4): _gen_u7_t4,
    (8, 1): _gen_u8_t1,
    (8, 2): _gen_u8_t2,
    (8, 3): _gen_u8_t3,
    (8, 4): _gen_u8_t4,
    (9, 1): _gen_u9_t1,
    (9, 2): _gen_u9_t2,
    (9, 3): _gen_u9_t3,
    (9, 4): _gen_u9_t4,
    (10, 1): _gen_u10_t1,
    (10, 2): _gen_u10_t2,
    (10, 3): _gen_u10_t3,
    (10, 4): _gen_u10_t4,
    (11, 1): _gen_u11_t1,
    (11, 2): _gen_u11_t2,
    (11, 3): _gen_u11_t3,
    (11, 4): _gen_u11_t4,
    (12, 1): _gen_u12_t1,
    (12, 2): _gen_u12_t2,
    (12, 3): _gen_u12_t3,
    (12, 4): _gen_u12_t4,
    (13, 1): _gen_u13_t1,
    (13, 2): _gen_u13_t2,
    (13, 3): _gen_u13_t3,
    (13, 4): _gen_u13_t4,
    (14, 1): _gen_u14_t1,
    (14, 2): _gen_u14_t2,
    (14, 3): _gen_u14_t3,
    (14, 4): _gen_u14_t4,
}


def generate_question(
    unit_id: int,
    topic_id: int,
    level: str,
    *,
    exclude_ids: set[str] | None = None,
    exclude_text: set[str] | None = None,
    templates_only: bool = False,
) -> dict | None:
    import harshit_class10_questions as h10q

    if not templates_only:
        q = h10q.pick_question(
            unit_id, topic_id, level, exclude_ids=exclude_ids, exclude_text=exclude_text
        )
        if q:
            return q

    fn = GENERATORS.get((unit_id, topic_id))
    if not fn:
        return None
    if level not in TOPICS.get(unit_id, {}).get(topic_id, {}).get("levels", {}):
        return None
    exclude_ids = exclude_ids or set()
    exclude_text = exclude_text or set()
    for _ in range(24):
        try:
            q = fn(level)
        except Exception:
            return None
        if not q:
            continue
        if h10q.question_dedup_key(str(q.get("question", "")), q.get("options")) in exclude_text:
            continue
        if str(q.get("id") or "") in exclude_ids:
            continue
        return q
    return None
