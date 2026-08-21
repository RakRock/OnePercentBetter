"""Linear equation solving strategies, levels, and question generators."""

from __future__ import annotations

import random
import re
from fractions import Fraction
from math import gcd
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


def _parse_x_value(text: str) -> float | None:
    """Parse a numeric x answer (integer or simple fraction)."""
    s = _normalize_math_text(str(text).strip())
    if re.fullmatch(r"-?\d+/\d+", s):
        num, den = s.split("/", 1)
        den_i = int(den)
        if den_i == 0:
            return None
        return int(num) / den_i
    if re.fullmatch(r"-?\d+", s):
        return float(int(s))
    return None


def _prepare_expr_for_eval(expr: str) -> str:
    s = _normalize_math_text(expr).replace(" ", "")
    s = re.sub(r"(\d)\(", r"\1*(", s)
    s = re.sub(r"\)(\d)", r")*\1", s)
    s = re.sub(r"(\d)/(\d)([xy])", r"((\1)/(\2)*\3)", s)
    s = re.sub(r"(-?\d+)([xy])", r"\1*\2", s)
    return s


def _eval_expr_at_x(expr: str, x_val: float) -> float:
    s = _prepare_expr_for_eval(expr)
    s = re.sub(r"\bx\b", f"({x_val})", s, flags=re.I)
    if not re.fullmatch(r"[-+*/().0-9]+", s):
        raise ValueError(f"Unsupported expression: {expr}")
    return float(eval(s, {"__builtins__": {}}, {}))


def equation_holds_for_x(equation: str, x_value: str) -> bool:
    """True when substituting x_value satisfies the equation."""
    x_val = _parse_x_value(x_value)
    if x_val is None:
        return False
    eq = _normalize_math_text(equation)
    if "=" not in eq:
        return False
    lhs, rhs = eq.split("=", 1)
    try:
        left = _eval_expr_at_x(lhs, x_val)
        right = _eval_expr_at_x(rhs, x_val)
    except (ValueError, SyntaxError, ZeroDivisionError, TypeError):
        return False
    return abs(left - right) < 1e-6


def options_look_like_x_values(options: list[str]) -> bool:
    return sum(_parse_x_value(o) is not None for o in options) >= 3


def question_asks_for_x_value(sid: int, lvl: str, instruction: str, followup: str) -> bool:
    """True when the MCQ expects a numeric value of x (not a step description)."""
    if sid == 2 and lvl in ("A", "B"):
        return False
    if sid in (5, 6, 7):
        return False
    if sid == 4 and lvl in ("B", "E"):
        return False
    text = f"{instruction} {followup}".lower()
    if "what is x" in text or "solve for x" in text or "solve mentally" in text:
        return True
    if sid in (1, 2, 3, 4) and lvl in ("A", "B", "C", "D", "E"):
        return sid != 2 or lvl in ("C", "D", "E")
    return False


def resolve_x_answer_index(
    equation: str,
    options: list[str],
    *,
    sid: int,
    lvl: str,
    instruction: str,
    followup: str,
) -> int | None:
    """Return the option index whose value satisfies the equation, if verifiable."""
    if not equation or not options_look_like_x_values(options):
        return None
    if not question_asks_for_x_value(sid, lvl, instruction, followup):
        return None
    matches = [i for i, opt in enumerate(options) if equation_holds_for_x(equation, opt)]
    if len(matches) == 1:
        return matches[0]
    return None


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
    correct = str(correct).strip()
    opts = [correct]
    for w in wrong:
        w = str(w).strip()
        if w and w not in opts:
            opts.append(w)
    n = 1
    while len(opts) < 4:
        try:
            base = int(Fraction(correct))
            for delta in (n, -n, n + 1, -n - 1):
                alt = fmt_num(base + delta)
                if alt not in opts:
                    opts.append(alt)
                    break
            else:
                n += 1
                continue
        except (ValueError, TypeError):
            alt = f"Option {len(opts) + 1}"
            if alt not in opts:
                opts.append(alt)
        n += 1
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
    correct = str(correct).strip()
    pool = [str(c).strip() for c in candidates if str(c).strip() and str(c).strip() != correct]
    random.shuffle(pool)
    seen = {correct}
    out: list[str] = []
    for item in pool:
        if item not in seen:
            seen.add(item)
            out.append(item)
        if len(out) >= n:
            break
    return out


def _four_options(correct: str, candidates: list[str]) -> tuple[list[str], int]:
    """Build four distinct MCQ options and return (options, answer_index)."""
    correct = str(correct).strip()
    opts = [correct, *_pick_wrong(correct, candidates, n=6)]
    n = 1
    while len(opts) < 4:
        try:
            base = int(Fraction(correct))
            for delta in (n, -n, n + 2, -n - 2, n + 3, -n - 3):
                alt = fmt_num(base + delta)
                if alt not in opts:
                    opts.append(alt)
                    break
            else:
                n += 1
                continue
        except (ValueError, TypeError):
            alt = f"Option {len(opts) + 1}"
            if alt not in opts:
                opts.append(alt)
        n += 1
    opts = opts[:4]
    random.shuffle(opts)
    return opts, opts.index(correct)


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
        b = -a * x
        eq = fmt_eq(f"−{a}x", str(b))
        correct = fmt_num(x)
        expl = f"−{a}x = {b} → x = {b} ÷ (−{a}) = {x}."
    return _mcq(f"Solve mentally: {eq}. What is x?", correct,
                _pick_wrong(correct, [fmt_num(-x), fmt_num(x + 1), fmt_num(x - 1), "0", "1"]), 1, "C", expl)


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
    a = random.randint(3, 7)
    b = random.randint(1, a - 1)
    x = random.randint(-12, -2)
    c = random.randint(2, 12)
    rhs = (a - b) * x - c
    rhs_side = f"{b}x"
    if rhs >= 0:
        rhs_side += f" + {rhs}"
    else:
        rhs_side += f" − {abs(rhs)}"
    eq = fmt_eq(f"{a}x − {c}", rhs_side)
    correct = fmt_num(x)
    opts, ans = _four_options(correct, [fmt_num(-x), fmt_num(x + 2), fmt_num(x - 2), "0", "1"])
    return attach_question_parts(
        {
            "id": f"leq_s3_B_{random.randint(1000, 9999)}",
            "strategy": 3,
            "level": "B",
            "instruction": "Solve for x.",
            "equation": eq,
            "followup": "What is x?",
            "question": compose_question("Solve for x.", eq, "What is x?"),
            "question_tex": text_to_latex(eq),
            "options": opts,
            "options_tex": [text_to_latex(o) for o in opts],
            "answer": ans,
            "explanation": f"Move x terms and constants → x = {x}.",
        }
    )


def _s3_c() -> dict:
    a = random.randint(2, 5)
    b = random.randint(a + 2, a + 6)
    x = random.randint(-12, -2)
    c = random.randint(2, 15)
    d = (a - b) * x - c
    eq = fmt_eq(f"−{a}x + {c}", f"−{b}x − {d}")
    correct = fmt_num(x)
    opts, ans = _four_options(correct, [fmt_num(-x), fmt_num(x + 2), fmt_num(x - 2), "0", "1"])
    return attach_question_parts(
        {
            "id": f"leq_s3_C_{random.randint(1000, 9999)}",
            "strategy": 3,
            "level": "C",
            "instruction": "Solve for x.",
            "equation": eq,
            "followup": "What is x?",
            "question": compose_question("Solve for x.", eq, "What is x?"),
            "question_tex": text_to_latex(eq),
            "options": opts,
            "options_tex": [text_to_latex(o) for o in opts],
            "answer": ans,
            "explanation": f"Add {b}x and subtract {c} → x = {x}.",
        }
    )


def _s3_d() -> dict:
    a_num, a_den = random.choice([(1, 2), (1, 3), (2, 3), (3, 4)])
    c_num, c_den = random.choice([(1, 4), (1, 2), (3, 4), (2, 5)])
    while Fraction(c_num, c_den) == Fraction(a_num, a_den):
        c_num, c_den = random.choice([(1, 4), (1, 2), (3, 4), (2, 5)])
    b = random.randint(1, 8)
    x = random.randint(4, 36)
    d = int(Fraction(a_num, a_den) * x + b - Fraction(c_num, c_den) * x)
    eq = f"{a_num}/{a_den} x + {b} = {c_num}/{c_den} x + {d}"
    correct = fmt_num(x)
    wrong = _pick_wrong(correct, [fmt_num(x + 2), fmt_num(-x), fmt_num(max(1, x // 2))])
    opts = [correct] + wrong
    random.shuffle(opts)
    return attach_question_parts(
        {
            "id": f"leq_s3_D_{random.randint(1000, 9999)}",
            "strategy": 3,
            "level": "D",
            "instruction": "Solve for x.",
            "equation": eq,
            "followup": "What is x?",
            "question": compose_question("Solve for x.", eq, "What is x?"),
            "question_tex": text_to_latex(eq),
            "options": opts,
            "options_tex": [text_to_latex(o) for o in opts],
            "answer": opts.index(correct),
            "explanation": "Move x terms to one side and constants to the other, then divide by the x-coefficient.",
        }
    )


def _s3_e() -> dict:
    a_num, a_den = random.choice([(2, 3), (1, 2), (3, 4)])
    b_num, b_den = random.choice([(1, 6), (1, 4), (1, 3)])
    x = random.randint(-10, -2)
    c = random.randint(1, 6)
    d_val = int(Fraction(-a_num, a_den) * x - c - Fraction(b_num, b_den) * x)
    rhs_side = f"{b_num}/{b_den} x"
    if d_val >= 0:
        rhs_side += f" + {d_val}"
    else:
        rhs_side += f" − {abs(d_val)}"
    eq = f"−{a_num}/{a_den} x − {c} = {rhs_side}"
    correct = fmt_num(x)
    opts, ans = _four_options(correct, [fmt_num(-x), fmt_num(x + 2), fmt_num(x - 2), "0", "1"])
    return attach_question_parts(
        {
            "id": f"leq_s3_E_{random.randint(1000, 9999)}",
            "strategy": 3,
            "level": "E",
            "instruction": "Solve for x.",
            "equation": eq,
            "followup": "What is x?",
            "question": compose_question("Solve for x.", eq, "What is x?"),
            "question_tex": text_to_latex(eq),
            "options": opts,
            "options_tex": [text_to_latex(o) for o in opts],
            "answer": ans,
            "explanation": "Combine x terms, then divide by the x-coefficient.",
        }
    )


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
    left = random.randint(4, 12)
    outer = random.randint(2, 5)
    inner_a = random.randint(2, 4)
    inner_b = random.randint(1, 7)
    rhs = random.randint(5, 24)
    distributed_rhs = outer * inner_b
    distributed_x = outer * inner_a
    correct = f"{left} − {distributed_x}x + {distributed_rhs} = {rhs}"
    eq = f"{left} − {outer}({inner_a}x − {inner_b}) = {rhs}"
    prompt = f"After distributing, which equation matches {eq}?"
    return _mcq(
        prompt,
        correct,
        _pick_wrong(
            correct,
            [
                f"{left} − {distributed_x}x − {distributed_rhs} = {rhs}",
                f"{left} + {distributed_x}x − {distributed_rhs} = {rhs}",
                f"{left} − {distributed_x}x + {inner_b} = {rhs}",
            ],
        ),
        4,
        "B",
        f"−{outer}({inner_a}x − {inner_b}) = −{distributed_x}x + {distributed_rhs}.",
    )


def _s4_c() -> dict:
    x = random.randint(-8, -1)
    a = random.randint(2, 4)
    shift = random.randint(2, 5)
    d = random.randint(2, 5)
    rhs = a * (x - shift) - d * (2 * x + 1)
    eq = f"{a}(x − {shift}) − {d}(2x + 1) = {rhs}"
    correct = fmt_num(x)
    return _mcq(
        f"Solve: {eq}. What is x?",
        correct,
        _pick_wrong(correct, [fmt_num(-x), fmt_num(x + 1), fmt_num(x - 1), "0"]),
        4,
        "C",
        "Expand both groups, combine like terms, then isolate x.",
    )


def _s4_d() -> dict:
    num, den = random.choice([(1, 3), (1, 2), (2, 5)])
    x = random.randint(2, 12)
    inner_a = random.randint(2, 6)
    inner_b = random.randint(1, 9)
    rhs = int(Fraction(num, den) * (inner_a * x - inner_b))
    eq = f"{num}/{den}({inner_a}x − {inner_b}) = {rhs}"
    correct = fmt_num(x)
    return _mcq(
        f"Solve: {eq}. What is x?",
        correct,
        _pick_wrong(correct, [fmt_num(x + 2), fmt_num(x - 2), fmt_num(-x), "0"]),
        4,
        "D",
        "Distribute the fraction, then isolate x.",
    )


def _s4_e() -> dict:
    num, den = random.choice([(2, 5), (3, 4), (1, 3)])
    a = random.randint(2, 5)
    b = random.randint(2, 8)
    correct = f"−{num * a}/{den} x + {num * b}/{den}"
    eq = f"−{num}/{den}({a}x − {b}) = ?"
    return _mcq(
        eq,
        correct,
        _pick_wrong(
            correct,
            [
                f"{num * a}/{den} x + {num * b}/{den}",
                f"−{num * a}/{den} x − {num * b}/{den}",
                f"{num * a}/{den} x − {num * b}/{den}",
            ],
        ),
        4,
        "E",
        f"Distribute −{num}/{den} through ({a}x − {b}).",
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
    d = random.choice([4, 5, 6, 8, 10])
    num = random.randint(1, d - 1)
    const = random.randint(1, d - 1)
    rhs = random.randint(1, d - 1)
    eq = f"{num}/{d} x + {const}/{d} = {rhs}/{d}"
    correct = f"Multiply every term by {d}"
    return _mcq(
        f"Best first step for {eq}?",
        correct,
        _pick_wrong(correct, [f"Multiply by {num}", f"Add {const}/{d}", f"Divide by {d}"]),
        5,
        "B",
        f"LCD is {d} — one multiplication clears all denominators.",
    )


def _s5_c() -> dict:
    denoms = random.choice([(2, 3, 6), (2, 3, 4), (3, 4, 12)])
    lcd = denoms[0] * denoms[1] // gcd(denoms[0], denoms[1])
    lcd = lcd * denoms[2] // gcd(lcd, denoms[2])
    eq = f"1/{denoms[0]} x + 2/{denoms[1]} = 5/{denoms[2]}"
    correct = f"Multiply every term by {lcd}"
    return _mcq(
        f"LCD to clear fractions in {eq}?",
        correct,
        _pick_wrong(correct, [f"Multiply by {denoms[0]}", f"Multiply by {denoms[1]}", f"Multiply by {lcd * 2}"]),
        5,
        "C",
        f"LCD({', '.join(map(str, denoms))}) = {lcd}.",
    )


def _s5_d() -> dict:
    den = random.choice([4, 8, 6])
    num = random.randint(2, den - 1)
    const = random.randint(1, den // 2)
    rhs = random.randint(1, den - 1)
    eq = f"−{num}/{den} x − {const}/{den} = {rhs}/{den}"
    correct = f"Multiply every term by {den}"
    return _mcq(
        f"Best first step for {eq}?",
        correct,
        _pick_wrong(correct, [f"Multiply by {num}", f"Multiply by 2", f"Add {const}/{den}"]),
        5,
        "D",
        f"LCD = {den}; watch negative signs on every term.",
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
    x_coef = random.randint(2, 5)
    y_coef = random.randint(2, 4)
    rhs = random.randint(6, 20)
    correct = f"y = −{x_coef}/{y_coef} x + {int(Fraction(rhs, y_coef))}"
    return _mcq(
        f"{x_coef}x + {y_coef}y = {rhs} solved for y gives —",
        correct,
        _pick_wrong(
            correct,
            [f"y = {x_coef}/{y_coef} x + {int(Fraction(rhs, y_coef))}", f"y = −{x_coef}x + {rhs}", f"y = {x_coef}x + {rhs}"],
        ),
        6,
        "B",
        f"{y_coef}y = −{x_coef}x + {rhs} → divide by {y_coef}.",
    )


def _s6_c() -> dict:
    x_coef = random.randint(2, 6)
    y_coef = random.randint(2, 5)
    rhs = random.randint(6, 24)
    correct = f"y = {x_coef}/{y_coef} x − {int(Fraction(rhs, y_coef))}"
    return _mcq(
        f"{x_coef}x − {y_coef}y = {rhs} solved for y gives —",
        correct,
        _pick_wrong(
            correct,
            [f"y = −{x_coef}/{y_coef} x + {int(Fraction(rhs, y_coef))}", f"y = {x_coef}/{y_coef} x + {rhs}", f"y = {x_coef}x − {rhs}"],
        ),
        6,
        "C",
        f"−{y_coef}y = −{x_coef}x + {rhs} → divide by −{y_coef} (signs flip).",
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
    x = random.randint(3, 12)
    y = random.randint(2, 10)
    s = x + y
    d = x - y
    correct = f"({x}, {y})"
    return _mcq(
        f"Solve by adding equations: x + y = {s} and x − y = {d}.",
        correct,
        _pick_wrong(correct, [f"({y}, {x})", f"({x + 1}, {y})", f"({x}, {y + 1})"]),
        7,
        "A",
        f"Add → 2x = {s + d} → x = {x}, y = {y}.",
    )


def _s7_b() -> dict:
    a = random.randint(2, 4)
    b = random.randint(2, 5)
    correct = f"Multiply the second equation by {b}"
    return _mcq(
        f"To eliminate y in {{{a}x + {b}y = {a * 3 + b * 2}, x − y = 1}}, best first step?",
        correct,
        _pick_wrong(correct, [f"Multiply first by {a}", "Add the equations", "Subtract equations"]),
        7,
        "B",
        f"x − y = 1 → {b}x − {b}y = {b}, then add to the first equation.",
    )


def _s7_c() -> dict:
    mult1 = random.randint(2, 3)
    mult2 = random.randint(2, 4)
    correct = f"Multiply eq. 1 by {mult1} and eq. 2 by −{mult2}"
    return _mcq(
        f"To eliminate x in {{3x + 4y = 10, 2x + 5y = 9}}, one valid step is —",
        correct,
        _pick_wrong(correct, ["Add equations directly", f"Multiply eq. 1 by −{mult1} only", "Divide eq. 2 by 2"]),
        7,
        "C",
        "Oppositely scaled x-coefficients allow elimination.",
    )


def _s7_d() -> dict:
    num = random.choice([2, 3, 4])
    den = random.choice([3, 4, 5])
    intercept = random.randint(2, 8)
    correct = f"Substitute y = {num}/{den} x − {intercept} into the other equation"
    return _mcq(
        f"System includes y = {num}/{den} x − {intercept}. Best next move?",
        correct,
        _pick_wrong(correct, ["Add both equations", f"Multiply by {den} only", "Graph and guess"]),
        7,
        "D",
        "Substitution replaces y with an expression in x.",
    )


def _s7_e() -> dict:
    correct = "Multiply each equation by its LCD to clear fractions, then eliminate"
    eq1 = random.choice(["−1/2 x + 1/3 y = −2", "1/4 x + 1/2 y = 3", "2/3 x − 1/5 y = 1"])
    eq2 = random.choice(["2/5 x − 3/4 y = 1", "1/3 x + 1/6 y = 2", "3/4 x − 1/2 y = −1"])
    return _mcq(
        f"System: {eq1} and {eq2}. Best start?",
        correct,
        _pick_wrong(correct, ["Add equations immediately", "Solve for x first", "Skip clearing fractions"]),
        7,
        "E",
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
    mm_lines = []
    try:
        from arjun_mental_math_drills import format_mental_math_summary, get_mental_math_count

        mm_lines = format_mental_math_summary(config)
        warmup_count = get_mental_math_count(config)
    except ImportError:
        warmup_count = 0
    if mm_lines and warmup_count:
        lines.append(f"Mental math warm-ups: {warmup_count} per session · {len(mm_lines)} drill level(s)")
        lines.extend(mm_lines)
    for item in config.get("strategies", []):
        sid = item["id"]
        for lvl in item.get("levels", []):
            lines.append(format_strategy_level_label(sid, lvl))
    return "\n".join(lines) if lines else "No strategies configured."
