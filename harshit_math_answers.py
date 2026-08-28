"""Compare Harshit Math MCQ answers for equivalent forms (√n powers, rational exponents)."""

from __future__ import annotations

import math
import re

from fractions import Fraction

import harshit_math_render as hmr

_EXP_FRAC_RE = re.compile(r"^\(([^)]+)\)$")
_RADICAL_POWER_RE = re.compile(r"^\(√(\d+)\)\^(-?\d+)$")
_RATIONAL_POWER_RE = re.compile(r"^(\d+)\^\((-?\d+)/(\d+)\)$")
_INT_POWER_RE = re.compile(r"^(\d+)\^(-?\d+)$")
_ONE_ZERO_RE = re.compile(r"One zero of p\(x\)\s*=\s*(.+?)\s+is\s*:?\s*$", re.IGNORECASE)


def _parse_exp_token(token: str) -> float | None:
    token = token.strip()
    if re.fullmatch(r"-?\d+", token):
        return float(token)
    m = _EXP_FRAC_RE.match(token)
    if m and re.fullmatch(r"-?\d+/-?\d+", m.group(1)):
        num, den = m.group(1).split("/", 1)
        return float(num) / float(den)
    return None


def numeric_value(text: str) -> float | None:
    """Best-effort numeric value for simple power / radical expressions."""
    s = hmr.sanitize_grok_math_text(text).replace(" ", "").replace("×", "*")
    if not s:
        return None

    m = _RADICAL_POWER_RE.match(s)
    if m:
        base, exp = int(m.group(1)), float(m.group(2))
        return base ** (exp / 2.0)

    m = _RATIONAL_POWER_RE.match(s)
    if m:
        base = int(m.group(1))
        exp = float(m.group(2)) / float(m.group(3))
        return base ** exp

    m = _INT_POWER_RE.match(s)
    if m:
        return int(m.group(1)) ** int(m.group(2))

    if re.fullmatch(r"-?\d+", s):
        return float(s)
    if re.fullmatch(r"-?\d+/-?\d+", s):
        num, den = s.split("/", 1)
        try:
            return float(Fraction(int(num), int(den)))
        except ZeroDivisionError:
            return None
    return None


def parse_monic_quadratic(poly: str) -> tuple[int, int] | None:
    """Parse x² + bx + c (integer coefficients) into (b, c)."""
    s = re.sub(r"\s+", "", str(poly or "").strip())
    if not s.startswith("x²"):
        return None
    s = s[2:]
    b, c = 0, 0
    if not s:
        return b, c
    if s[0] in "+-":
        m = re.match(r"([+-]\d+)x", s)
        if m:
            b = int(m.group(1))
            s = s[m.end():]
        else:
            m = re.match(r"([+-])x", s)
            if m:
                b = 1 if m.group(1) == "+" else -1
                s = s[2:]
    elif s.startswith("x"):
        b = 1
        s = s[1:]
    if s:
        m = re.match(r"([+-]\d+)", s)
        if m:
            c = int(m.group(1))
    return b, c


def integer_roots_of_monic_quadratic(b: int, c: int) -> list[int]:
    """Integer roots of x² + bx + c = 0, if any."""
    disc = b * b - 4 * c
    if disc < 0:
        return []
    root = math.isqrt(disc)
    if root * root != disc:
        return []
    if (b + root) % 2 != 0:
        return []
    return sorted({(-b + root) // 2, (-b - root) // 2})


def alternate_polynomial_zero_accepted(question: str, picked: str) -> bool:
    """Accept any valid zero when the prompt asks for one zero (not the other)."""
    q = str(question or "").strip()
    lower = q.lower()
    if "other zero" in lower:
        return False
    if re.search(r"one zero of p\(x\)\s*=.+ is\s+-?\d", q, re.IGNORECASE):
        return False
    m = _ONE_ZERO_RE.search(q)
    if not m:
        return False
    parsed = parse_monic_quadratic(m.group(1))
    if not parsed:
        return False
    b, c = parsed
    roots = integer_roots_of_monic_quadratic(b, c)
    if not roots:
        return False
    pv = numeric_value(picked)
    if pv is None:
        return False
    return any(abs(pv - float(r)) <= 1e-9 for r in roots)


def answers_equivalent(a: str, b: str) -> bool:
    """True when two option strings represent the same value or identical text."""
    a_norm = hmr.sanitize_grok_math_text(a).strip().lower()
    b_norm = hmr.sanitize_grok_math_text(b).strip().lower()
    if a_norm == b_norm:
        return True
    va, vb = numeric_value(a), numeric_value(b)
    if va is not None and vb is not None:
        return abs(va - vb) <= 1e-9
    return False


def is_pick_correct(question: dict, picked_index: int) -> bool:
    """Grade by keyed index, but accept equivalent math forms."""
    if picked_index == question["answer"]:
        return True
    opts = question.get("options") or []
    if picked_index < 0 or picked_index >= len(opts):
        return False
    picked = str(opts[picked_index])
    correct = str(opts[question["answer"]])
    if answers_equivalent(picked, correct):
        return True
    valid = question.get("valid_answers")
    if isinstance(valid, list):
        for alt in valid:
            if answers_equivalent(picked, str(alt)):
                return True
    return alternate_polynomial_zero_accepted(str(question.get("question", "")), picked)
