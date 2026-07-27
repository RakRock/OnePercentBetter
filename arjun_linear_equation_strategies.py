"""Linear equation solving strategies, levels, and question generators."""

from __future__ import annotations

import random
import re
from fractions import Fraction
from typing import Callable

LEVEL_ORDER = ["A", "B", "C", "D", "E"]

STRATEGIES: dict[int, dict] = {
    1: {
        "name": "Inspection & Cover-Up Method",
        "short": "Inspection",
        "levels": {
            "A": "Positive Addition/Subtraction",
            "B": "Positive Multiplication/Division",
            "C": "Negative Numbers",
            "D": "Fraction Multipliers",
            "E": "Fraction Division/Negatives",
        },
    },
    2: {
        "name": "Inverse Operations (1-Step & 2-Step Equations)",
        "short": "Inverse Operations",
        "levels": {
            "A": "Positive Addition/Subtraction",
            "B": "Positive Multiplication/Division",
            "C": "Negative Numbers",
            "D": "Fraction Multipliers",
            "E": "Fraction Division & Negative Coefficients",
        },
    },
    3: {
        "name": "Grouping & Combining Like Terms Across Equality",
        "short": "Grouping & Like Terms",
        "levels": {
            "A": "Positive Integers",
            "B": "Negative Integers & Subtraction",
            "C": "Mixed Sign Operations",
            "D": "Fractional Coefficients",
            "E": "Negative Fraction Division",
        },
    },
    4: {
        "name": "Expansion via Distributive Property",
        "short": "Distributive Property",
        "levels": {
            "A": "Positive Distribution",
            "B": "Negative Distribution — Subtraction Trap",
            "C": "Double Distribution",
            "D": "Fractional Multiplier Distribution",
            "E": "Fractional Multipliers with Non-Multiple Constants",
        },
    },
    5: {
        "name": "Clearing Fractions & Decimals (LCD Method)",
        "short": "LCD Method",
        "levels": {
            "A": "Single Unit Fraction",
            "B": "Multiple Fractions, Same Denominator",
            "C": "Different Denominators — Positive",
            "D": "Different Denominators — Negative Signs",
            "E": "Fractional Parentheses / Decimals",
        },
    },
    6: {
        "name": "Literal Transposition (Solving for y)",
        "short": "Solve for y",
        "levels": {
            "A": "Positive Basic Standard Form",
            "B": "Positive Multiplier on y",
            "C": "Negative y Coefficient",
            "D": "Non-Zero Constant Rearrangement",
            "E": "Starting with Fractions",
        },
    },
    7: {
        "name": "Systems of Linear Equations",
        "short": "Systems",
        "levels": {
            "A": "Direct Addition — Elimination",
            "B": "Single Multiplication Step — Positive",
            "C": "Negative Multipliers & Subtraction",
            "D": "Substitution with Fractions",
            "E": "Systems with Fractional Coefficients",
        },
    },
}


def fmt_num(n: int | Fraction) -> str:
    if isinstance(n, Fraction):
        if n.denominator == 1:
            return str(n.numerator)
        return f"{n.numerator}/{n.denominator}"
    return str(n)


def fmt_eq(lhs: str, rhs: str) -> str:
    return f"{lhs} = {rhs}"


def fmt_frac(num: int, den: int) -> str:
    """Plain-text fraction for generators (e.g. 3/4)."""
    return f"{num}/{den}"


def _normalize_math_text(text: str) -> str:
    return text.replace("−", "-").replace("–", "-")


def text_to_latex(text: str) -> str:
    """Convert plain math strings to LaTeX with stacked \\frac{}{} fractions."""
    s = _normalize_math_text(text)
    s = re.sub(r"([xy])/(\d+)", r"\\frac{\1}{\2}", s)

    def _frac(m: re.Match) -> str:
        sign = m.group(1) or ""
        num, den = m.group(2), m.group(3)
        tail = m.group(4) or ""
        return f"{sign}\\frac{{{num}}}{{{den}}}{tail}"

    s = re.sub(r"(-)?(\d+)/(\d+)([xy])?", _frac, s)
    return s


def question_to_latex(question: str) -> str:
    """Full question line as LaTeX with stacked fractions."""
    return text_to_latex(_normalize_math_text(question))


def has_fraction_markup(text: str) -> bool:
    s = _normalize_math_text(text)
    return bool(re.search(r"\d+/\d+", s) or re.search(r"[xy]/\d+", s))


_EQUATION_RE = re.compile(
    r"("
    r"(?:"
    r"-?\d+/\d+\s*[xy]|"
    r"-?\d+/\d+[xy]|"
    r"[xy]/\d+|"
    r"-?\d+[xy]\s*[+\-]\s*y|"
    r"-?\d+[xy]\s*[+\-]\s*[\d./+-]+|"
    r"[xy]\s*[+\-]\s*y|"
    r"[xy]\s*[+\-]\s*[\d./+-]+|"
    r"-?\d+[xy]|"
    r"[xy]"
    r")"
    r"\s*=\s*"
    r"-?[\d./xy\s+\-]+"
    r")",
    re.I,
)


def split_question(question: str) -> tuple[str, str, str]:
    """Split a prompt into plain-text instruction, equation, and optional follow-up."""
    q = _normalize_math_text(question).strip()
    m = _EQUATION_RE.search(q)
    if not m:
        return q, "", ""

    eq = m.group(1).strip().rstrip(".")
    instruction = q[: m.start()].strip()
    after = q[m.end() :].strip()

    followup = ""
    if after.startswith("."):
        after = after[1:].strip()
    if after == "?":
        if instruction and not instruction.endswith("?"):
            instruction = f"{instruction}?"
    elif after.startswith("?"):
        if instruction and not instruction.endswith("?"):
            instruction = f"{instruction}?"
        after = after[1:].strip()
        if after:
            followup = after
    elif after:
        followup = after

    return instruction, eq, followup


def default_instruction_for_slot(sid: int, lvl: str) -> str:
    """Clear prompt line shown above the equation box."""
    if sid == 1:
        return "Solve mentally."
    if sid == 2 and lvl in ("A", "B"):
        return "What is the first step to solve this equation?"
    if sid == 2:
        return "Solve for x."
    if sid == 3 or sid == 4:
        return "Solve for x."
    if sid == 5:
        return "What is the best first step to clear fractions?"
    if sid == 6:
        return "What is the first step to solve for y?"
    if sid == 7:
        return "What is the best next step?"
    return "Solve this equation."


def default_followup_for_slot(sid: int, lvl: str) -> str:
    if sid == 1:
        return "What is x?"
    if sid == 2 and lvl in ("C", "D", "E"):
        return "What is x?"
    if sid in (3, 4):
        return "What is x?"
    return ""


def compose_question(instruction: str, equation: str, followup: str = "") -> str:
    """Plain-text question string for emails and legacy display."""
    inst = instruction.strip().rstrip(".")
    if followup:
        return f"{inst}. {equation.strip()}. {followup.strip()}"
    if inst.endswith("?"):
        return f"{inst.rstrip('?')}. {equation.strip()}?"
    return f"{inst}. {equation.strip()}."


def _is_vague_instruction(instruction: str) -> bool:
    text = instruction.strip().lower().rstrip("?").rstrip(":")
    return text in {
        "first step to solve",
        "first step",
        "solve",
        "solve mentally",
        "best first step",
        "best first step to clear fractions in",
        "first step to solve for y in",
    }


def attach_question_parts(q: dict) -> dict:
    """Ensure question dict has instruction / equation / followup for UI rendering."""
    if q.get("equation"):
        out = dict(q)
        out.setdefault("instruction", default_instruction_for_slot(int(q["strategy"]), str(q["level"])))
        out.setdefault("followup", "")
        out["question"] = compose_question(out["instruction"], out["equation"], out.get("followup", ""))
        return out
    instruction, eq, followup = split_question(q.get("question", ""))
    if eq:
        sid, lvl = int(q["strategy"]), str(q["level"])
        if not instruction or _is_vague_instruction(instruction):
            instruction = default_instruction_for_slot(sid, lvl)
        if not followup:
            followup = default_followup_for_slot(sid, lvl)
        out = dict(q)
        out["instruction"] = instruction
        out["equation"] = eq
        out["followup"] = followup
        out["question"] = compose_question(instruction, eq, followup)
        out["question_tex"] = text_to_latex(eq)
        return out
    return q


def _mcq(question: str, correct: str, wrong: list[str], sid: int, level: str, explanation: str) -> dict:
    opts = [correct] + wrong[:3]
    random.shuffle(opts)
    item = {
        "id": f"leq_s{sid}_{level}_{random.randint(1000, 9999)}",
        "strategy": sid,
        "level": level,
        "question": question,
        "question_tex": question_to_latex(question),
        "options": opts,
        "options_tex": [text_to_latex(o) for o in opts],
        "answer": opts.index(correct),
        "explanation": explanation,
    }
    return attach_question_parts(item)


def _pick_wrong(correct: str, candidates: list[str], n: int = 3) -> list[str]:
    pool = [c for c in candidates if c != correct]
    random.shuffle(pool)
    return pool[:n]


# ── Strategy 1: Inspection ──

def _s1_a() -> dict:
    a = random.randint(2, 12)
    x = random.randint(2, 15)
    b = x + a
    correct = fmt_num(x)
    return _mcq(
        f"Solve mentally: x + {a} = {b}. What is x?",
        correct,
        _pick_wrong(correct, [fmt_num(x + 1), fmt_num(x - 1), fmt_num(b), fmt_num(a)]),
        1, "A",
        f"Think: what plus {a} equals {b}? → x = {x}.",
    )


def _s1_b() -> dict:
    if random.choice([True, False]):
        a = random.randint(2, 9)
        x = random.randint(2, 12)
        b = a * x
        eq = fmt_eq(f"{a}x", str(b))
        correct = fmt_num(x)
        expl = f"What times {a} equals {b}? → x = {x}."
    else:
        d = random.choice([2, 3, 4, 5])
        x = random.randint(2, 20)
        b = Fraction(x, d)
        eq = fmt_eq(f"x/{d}", fmt_num(b))
        correct = fmt_num(x)
        expl = f"x ÷ {d} = {fmt_num(b)} → x = {x}."
    return _mcq(f"Solve mentally: {eq}. What is x?", correct,
                _pick_wrong(correct, [fmt_num(int(correct) + 1), fmt_num(int(correct) - 1), "0"]), 1, "B", expl)


def _s1_c() -> dict:
    if random.choice([True, False]):
        a = random.randint(3, 10)
        x = random.randint(-8, 8)
        b = x - a
        eq = fmt_eq(f"x − {a}", str(b))
        correct = fmt_num(x)
        expl = f"Add {a} to both sides mentally: x = {b} + {a} = {x}."
    else:
        a = random.randint(2, 6)
        x = random.randint(-10, -2)
        b = a * x
        eq = fmt_eq(f"−{a}x", str(b))
        correct = fmt_num(x)
        expl = f"−{a}x = {b} → x = {b} ÷ (−{a}) = {x}."
    return _mcq(f"Solve mentally: {eq}. What is x?", correct,
                _pick_wrong(correct, [fmt_num(-int(correct) if correct.lstrip('-').isdigit() else 0), "0", "1"]), 1, "C", expl)


def _s1_d() -> dict:
    num, den = random.choice([(2, 3), (3, 4), (1, 2)])
    x = random.choice([6, 9, 12, 15])
    b = Fraction(num * x, den)
    eq = fmt_eq(f"{num}/{den}x", fmt_num(b))
    correct = fmt_num(x)
    return _mcq(
        f"Solve mentally: {eq}. What is x?",
        correct,
        _pick_wrong(correct, [fmt_num(x + 3), fmt_num(x - 3), fmt_num(Fraction(b) * den)]),
        1, "D",
        f"{num}/{den} of x is {fmt_num(b)} → x = {x}.",
    )


def _s1_e() -> dict:
    x = Fraction(6, 1)
    lhs = Fraction(-3, 4) * x
    eq = fmt_eq(f"−3/4 x", fmt_num(lhs))
    correct = fmt_num(x)
    return _mcq(
        f"Inspection gets harder here. Solve: {eq}. What is x?",
        correct,
        _pick_wrong(correct, ["4", "−4", "3/2", "−3/2"]),
        1, "E",
        "Use inverse operations: multiply both sides by −4/3 → x = 6.",
    )


# ── Strategy 2: Inverse Operations ──

def _s2_a() -> dict:
    a = random.randint(3, 15)
    x = random.randint(5, 25)
    b = x + a
    correct = f"Subtract {a}"
    return _mcq(
        f"First step to solve x + {a} = {b}?",
        correct,
        _pick_wrong(correct, [f"Add {a}", f"Divide by {a}", f"Multiply by {a}"]),
        2, "A",
        f"Undo +{a} by subtracting {a} → x = {x}.",
    )


def _s2_b() -> dict:
    a = random.randint(2, 8)
    x = random.randint(3, 12)
    b = a * x
    correct = f"Divide both sides by {a}"
    return _mcq(
        f"First step to solve {a}x = {b}?",
        correct,
        _pick_wrong(correct, [f"Multiply by {a}", f"Add {a}", f"Subtract {a}"]),
        2, "B",
        f"Divide by {a} → x = {x}.",
    )


def _s2_c() -> dict:
    a = random.randint(2, 5)
    x = random.randint(3, 10)
    b = -a * x - 8
    # -3x - 8 = 13 style: after add 8, -3x = 21, x = -7... use positive x
    c = random.randint(4, 12)
    rhs = -a * x + c
    eq = fmt_eq(f"−{a}x + {c}", str(rhs))
    correct = fmt_num(x)
    return _mcq(
        f"Solve: {eq}. What is x?",
        correct,
        _pick_wrong(correct, [fmt_num(-x), fmt_num(x + 2), fmt_num(x - 2)]),
        2, "C",
        f"Subtract {c}, then divide by −{a} → x = {x}.",
    )


def _s2_d() -> dict:
    x = random.randint(6, 15)
    b = Fraction(3 * x, 5)
    correct = fmt_num(x)
    return _mcq(
        f"Solve: 3/5 x = {fmt_num(b)}. What is x?",
        correct,
        _pick_wrong(correct, [fmt_num(x + 2), fmt_num(x - 2), fmt_num(Fraction(b) * 5 // 3)]),
        2, "D",
        f"Multiply both sides by 5/3 → x = {x}.",
    )


def _s2_e() -> dict:
    x = Fraction(14, 5)
    lhs = Fraction(-4, 7) * x
    correct = fmt_num(x)
    return _mcq(
        f"Solve: −4/7 x = −8/5. What is x?",
        correct,
        _pick_wrong(correct, ["−14/5", "8/5", "−8/5", "2"]),
        2, "E",
        "Multiply both sides by −7/4 → x = 14/5.",
    )


# ── Strategy 3: Grouping & Like Terms ──

def _s3_a() -> dict:
    a, b = sorted(random.sample([2, 3, 4, 5], 2), reverse=True)
    x = random.randint(2, 8)
    rhs = (a - b) * x + random.randint(2, 6)
    const = rhs - (a - b) * x
    eq = fmt_eq(f"{a}x + {const}", f"{b}x + {rhs}")
    correct = fmt_num(x)
    return _mcq(f"Solve: {eq}. What is x?", correct,
                _pick_wrong(correct, [fmt_num(x + 1), fmt_num(x - 1), "0"]), 3, "A",
                f"Subtract {b}x and constants → x = {x}.")


def _s3_b() -> dict:
    x = -5
    eq = "3x − 8 = 7x + 12"
    correct = fmt_num(x)
    return _mcq(f"Solve: {eq}. What is x?", correct,
                _pick_wrong(correct, ["5", "−4", "4"]), 3, "B",
                "Subtract 7x: −4x − 8 = 12 → −4x = 20 → x = −5.")


def _s3_c() -> dict:
    x = -5
    eq = "−4x + 10 = −9x − 15"
    correct = fmt_num(x)
    return _mcq(f"Solve: {eq}. What is x?", correct,
                _pick_wrong(correct, ["5", "−4", "4"]), 3, "C",
                "Add 9x: 5x + 10 = −15 → 5x = −25 → x = −5.")


def _s3_d() -> dict:
    x = 24
    eq = "1/2 x + 4 = 3/4 x − 2"
    correct = fmt_num(x)
    return _mcq(f"Solve: {eq}. What is x?", correct,
                _pick_wrong(correct, ["12", "−24", "6"]), 3, "D",
                "Subtract 1/2 x and add 2 → 1/4 x = 6 → x = 24.")


def _s3_e() -> dict:
    x = -4
    eq = "−2/3 x − 1 = 1/6 x + 3"
    correct = fmt_num(x)
    return _mcq(f"Solve: {eq}. What is x?", correct,
                _pick_wrong(correct, ["4", "−2", "2"]), 3, "E",
                "Combine x terms → −5/6 x = 4 → x = −4.")


# ── Strategy 4: Distributive Property ──

def _s4_a() -> dict:
    a = random.randint(2, 5)
    b = random.randint(2, 6)
    c = random.randint(3, 8)
    x = random.randint(2, 6)
    rhs = a * (b * x + c)
    eq = fmt_eq(f"{a}({b}x + {c})", str(rhs))
    correct = fmt_num(x)
    return _mcq(f"Solve: {eq}. What is x?", correct,
                _pick_wrong(correct, [fmt_num(x + 1), fmt_num(x - 1), "0"]), 4, "A",
                f"Distribute → {a*b}x + {a*c} = {rhs} → x = {x}.")


def _s4_b() -> dict:
    x = 2
    correct = "8 − 6x + 15 = 11"
    return _mcq(
        "After distributing, which equation matches 8 − 3(2x − 5) = 11?",
        correct,
        _pick_wrong(correct, ["8 − 6x − 15 = 11", "8 + 6x − 15 = 11", "8 − 6x + 5 = 11"]),
        4, "B",
        "−3(2x − 5) = −6x + 15.",
    )


def _s4_c() -> dict:
    x = -2
    eq = "2(x − 3) − 4(2x + 1) = 10"
    correct = fmt_num(x)
    return _mcq(f"Solve: {eq}. What is x?", correct,
                _pick_wrong(correct, ["2", "−1", "1"]), 4, "C",
                "Expand → 2x − 6 − 8x − 4 = 10 → −6x = 20 → x = −2.")


def _s4_d() -> dict:
    x = 4
    eq = "1/3(6x − 9) = 10"
    correct = fmt_num(x)
    return _mcq(f"Solve: {eq}. What is x?", correct,
                _pick_wrong(correct, ["2", "6", "−4"]), 4, "D",
                "Distribute → 2x − 3 = 10 → x = 4.")


def _s4_e() -> dict:
    correct = "−6/5 x + 8/5"
    return _mcq(
        "Expand the left side: −2/5(3x − 4) = ?",
        correct,
        _pick_wrong(correct, ["−6/5 x − 8/5", "6/5 x + 8/5", "−6/5 x + 4"]),
        4, "E",
        "Distribute −2/5 through (3x − 4).",
    )


# ── Strategy 5: LCD Method ──

def _s5_a() -> dict:
    d = random.choice([3, 4, 5, 6])
    x = random.randint(2, 20)
    c = random.randint(2, 8)
    b = Fraction(x, d) + c
    eq = fmt_eq(f"x/{d} + {c}", fmt_num(b))
    correct = f"Multiply every term by {d}"
    return _mcq(f"Best first step to clear fractions in {eq}?", correct,
                _pick_wrong(correct, [f"Add {d}", f"Divide by {d}", "Combine x terms"]), 5, "A",
                f"Multiplying by {d} clears the denominator.")


def _s5_b() -> dict:
    correct = "Multiply every term by 5"
    return _mcq(
        "Best first step for 2/5 x + 1/5 = 4/5?",
        correct,
        _pick_wrong(correct, ["Multiply by 2", "Add 1/5", "Divide by 5"]),
        5, "B",
        "LCD is 5 — one multiplication clears all denominators.",
    )


def _s5_c() -> dict:
    correct = "Multiply every term by 6"
    return _mcq(
        "LCD to clear fractions in 1/2 x + 2/3 = 5/6?",
        correct,
        _pick_wrong(correct, ["Multiply by 2", "Multiply by 3", "Multiply by 12"]),
        5, "C",
        "LCD(2, 3, 6) = 6.",
    )


def _s5_d() -> dict:
    correct = "Multiply every term by 8"
    return _mcq(
        "Best first step for −3/4 x − 1/2 = 5/8?",
        correct,
        _pick_wrong(correct, ["Multiply by 4", "Multiply by 2", "Add 1/2"]),
        5, "D",
        "LCD(4, 2, 8) = 8; watch negative signs on every term.",
    )


def _s5_e() -> dict:
    correct = "Convert 0.2 to 1/5, then find LCD of all denominators"
    return _mcq(
        "Best plan for −2/3(x − 1/2) = 3/4 x + 0.2?",
        correct,
        _pick_wrong(correct, ["Multiply by 2 only", "Distribute first, skip LCD", "Add 0.2 to both sides"]),
        5, "E",
        "Convert decimals, distribute if needed, then multiply by LCD.",
    )


# ── Strategy 6: Solve for y ──

def _s6_a() -> dict:
    a = random.randint(2, 6)
    b = random.randint(4, 15)
    correct = f"Subtract {a}x from both sides"
    return _mcq(f"First step to solve for y in {a}x + y = {b}?", correct,
                _pick_wrong(correct, [f"Add {a}x", f"Divide by {a}", f"Subtract {b}"]), 6, "A",
                f"y = {b} − {a}x.")


def _s6_b() -> dict:
    correct = "y = −3/2 x + 4"
    return _mcq(
        "3x + 2y = 8 solved for y gives —",
        correct,
        _pick_wrong(correct, ["y = 3/2 x + 4", "y = −3x + 8", "y = 3x + 4"]),
        6, "B",
        "2y = −3x + 8 → divide by 2.",
    )


def _s6_c() -> dict:
    correct = "y = 4/3 x − 4"
    return _mcq(
        "4x − 3y = 12 solved for y gives —",
        correct,
        _pick_wrong(correct, ["y = −4/3 x + 4", "y = 4/3 x + 4", "y = 4x − 4"]),
        6, "C",
        "−3y = −4x + 12 → divide by −3 (signs flip).",
    )


def _s6_d() -> dict:
    correct = "Add 10 to both sides, then subtract 4, then divide by 2"
    return _mcq(
        "Best order for −5x + 4 = 2y − 10 when solving for y?",
        correct,
        _pick_wrong(correct, ["Divide by 2 first", "Add 5x last", "Subtract 10 from left only"]),
        6, "D",
        "Move constants before dividing by the y-coefficient.",
    )


def _s6_e() -> dict:
    correct = "Multiply by 12 to clear denominators, then isolate y"
    return _mcq(
        "Best approach for −2/3 x + 1/4 y − 1/2 = 0?",
        correct,
        _pick_wrong(correct, ["Divide by 1/4 first", "Add 2/3 x only", "Ignore fractions"]),
        6, "E",
        "LCD = 12 clears all fractional coefficients.",
    )


# ── Strategy 7: Systems ──

def _s7_a() -> dict:
    correct = "(7, 3)"
    return _mcq(
        "Solve by adding equations: x + y = 10 and x − y = 4.",
        correct,
        _pick_wrong(correct, ["(3, 7)", "(6, 4)", "(5, 5)"]),
        7, "A",
        "Add → 2x = 14 → x = 7, y = 3.",
    )


def _s7_b() -> dict:
    correct = "Multiply the second equation by 3"
    return _mcq(
        "To eliminate y in {2x + 3y = 12, x − y = 1}, best first step?",
        correct,
        _pick_wrong(correct, ["Multiply first by 2", "Add the equations", "Subtract equations"]),
        7, "B",
        "x − y = 1 → 3x − 3y = 3, then add to first equation.",
    )


def _s7_c() -> dict:
    correct = "Multiply eq. 1 by 2 and eq. 2 by −3"
    return _mcq(
        "To eliminate x in {3x + 4y = 10, 2x + 5y = 9}, one valid step is —",
        correct,
        _pick_wrong(correct, ["Add equations directly", "Multiply eq. 1 by −2 only", "Divide eq. 2 by 2"]),
        7, "C",
        "Oppositely scaled x-coefficients allow elimination.",
    )


def _s7_d() -> dict:
    correct = "Substitute y = 2/3 x − 4 into the other equation"
    return _mcq(
        "System includes y = 2/3 x − 4. Best next move?",
        correct,
        _pick_wrong(correct, ["Add both equations", "Multiply by 3 only", "Graph and guess"]),
        7, "D",
        "Substitution replaces y with an expression in x.",
    )


def _s7_e() -> dict:
    correct = "Multiply each equation by its LCD to clear fractions, then eliminate"
    return _mcq(
        "System: −1/2 x + 1/3 y = −2 and 2/5 x − 3/4 y = 1. Best start?",
        correct,
        _pick_wrong(correct, ["Add equations immediately", "Solve for x first", "Skip clearing fractions"]),
        7, "E",
        "Clear fractions in both equations before elimination.",
    )


GENERATOR_MAP: dict[tuple[int, str], Callable[[], dict]] = {
    (1, "A"): _s1_a, (1, "B"): _s1_b, (1, "C"): _s1_c, (1, "D"): _s1_d, (1, "E"): _s1_e,
    (2, "A"): _s2_a, (2, "B"): _s2_b, (2, "C"): _s2_c, (2, "D"): _s2_d, (2, "E"): _s2_e,
    (3, "A"): _s3_a, (3, "B"): _s3_b, (3, "C"): _s3_c, (3, "D"): _s3_d, (3, "E"): _s3_e,
    (4, "A"): _s4_a, (4, "B"): _s4_b, (4, "C"): _s4_c, (4, "D"): _s4_d, (4, "E"): _s4_e,
    (5, "A"): _s5_a, (5, "B"): _s5_b, (5, "C"): _s5_c, (5, "D"): _s5_d, (5, "E"): _s5_e,
    (6, "A"): _s6_a, (6, "B"): _s6_b, (6, "C"): _s6_c, (6, "D"): _s6_d, (6, "E"): _s6_e,
    (7, "A"): _s7_a, (7, "B"): _s7_b, (7, "C"): _s7_c, (7, "D"): _s7_d, (7, "E"): _s7_e,
}


def generate_question(strategy_id: int, level: str) -> dict | None:
    fn = GENERATOR_MAP.get((strategy_id, level))
    if not fn:
        return None
    return fn()


def format_strategy_level_label(strategy_id: int, level: str) -> str:
    s = STRATEGIES[strategy_id]
    return f"Strategy {strategy_id}: {s['short']} — Level {level} ({s['levels'][level]})"


def format_week_plan_summary(config: dict) -> str:
    lines = []
    label = config.get("week_label", "").strip()
    if label:
        lines.append(f"Week: {label}")
    if config.get("use_llm"):
        lines.append("Question source: AI (xAI Grok)")
    else:
        lines.append("Question source: Built-in generators")
    for item in config.get("strategies", []):
        sid = item["id"]
        for lvl in item.get("levels", []):
            lines.append(format_strategy_level_label(sid, lvl))
    return "\n".join(lines) if lines else "No strategies configured."
