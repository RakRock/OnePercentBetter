"""Compare Harshit Math MCQ answers for equivalent forms (√n powers, rational exponents)."""

from __future__ import annotations

import re

from fractions import Fraction

import harshit_math_render as hmr

_EXP_FRAC_RE = re.compile(r"^\(([^)]+)\)$")
_RADICAL_POWER_RE = re.compile(r"^\(√(\d+)\)\^(-?\d+)$")
_RATIONAL_POWER_RE = re.compile(r"^(\d+)\^\((-?\d+)/(\d+)\)$")
_INT_POWER_RE = re.compile(r"^(\d+)\^(-?\d+)$")


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
    return answers_equivalent(picked, correct)
