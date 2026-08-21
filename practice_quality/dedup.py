"""Duplicate and near-duplicate detection for practice questions."""

from __future__ import annotations

import re
from fractions import Fraction

# Instruction prefixes stripped before comparing math bodies.
_INSTRUCTION_PREFIXES = (
    "solve for x",
    "solve for y",
    "solve mentally",
    "what is the first step to solve this equation",
    "what is the first step to solve for y in",
    "what is the best first step to clear fractions",
    "what is the best next step",
    "multiply the monomial by the polynomial",
    "simplify",
    "evaluate",
    "compute",
    "find",
)

_VAR_RE = re.compile(r"\b[xy]\b", re.I)
_FRAC_RE = re.compile(r"(-?\d+)/(\d+)")


def _normalize_unicode(text: str) -> str:
    return (
        str(text or "")
        .replace("−", "-")
        .replace("–", "-")
        .replace("—", "-")
        .replace("×", "*")
        .replace("÷", "/")
        .replace("·", "*")
    )


def normalize_question_text(text: str) -> str:
    """Lowercase, collapse whitespace, strip trailing punctuation."""
    t = _normalize_unicode(text).strip().lower()
    t = re.sub(r"\s+", " ", t)
    for prefix in _INSTRUCTION_PREFIXES:
        if t.startswith(prefix + ":"):
            t = t[len(prefix) + 1 :].strip()
        elif t.startswith(prefix + "."):
            t = t[len(prefix) + 1 :].strip()
        elif t.startswith(prefix + " "):
            t = t[len(prefix) :].strip()
    return t.rstrip(".?!: ").strip()


def question_text(q: dict) -> str:
    if q.get("equation"):
        try:
            import arjun_linear_equation_strategies as leqs

            return leqs.compose_question(
                str(q.get("instruction", "")),
                str(q.get("equation", "")),
                str(q.get("followup", "")),
            )
        except Exception:
            pass
    return str(q.get("question", "")).strip()


def extract_equation(q: dict) -> str:
    if q.get("equation"):
        return str(q["equation"]).strip()
    try:
        import arjun_linear_equation_strategies as leqs

        _, eq, _ = leqs.split_question(question_text(q))
        if eq:
            return eq.strip()
    except Exception:
        pass
    text = question_text(q)
    if "=" in text:
        m = re.search(r"([^=]+=[^=?]+)", text)
        if m:
            return m.group(1).strip().rstrip(".")
    return ""


def _reduce_fractions(text: str) -> str:
    def _repl(m: re.Match) -> str:
        num, den = int(m.group(1)), int(m.group(2))
        if den == 0:
            return m.group(0)
        f = Fraction(num, den)
        return f"{f.numerator}/{f.denominator}"

    return _FRAC_RE.sub(_repl, text)


def normalize_equation(eq: str) -> str:
    s = _normalize_unicode(eq)
    s = re.sub(r"\s+", "", s)
    s = _reduce_fractions(s)
    s = _VAR_RE.sub("v", s)
    return s.lower()


def linear_equation_signature(eq: str) -> tuple[float, float] | None:
    """Canonical (a, b) for ax + b = 0 form of lhs - rhs, if linear in x."""
    if not eq or "=" not in eq:
        return None
    try:
        import arjun_linear_equation_strategies as leqs

        lhs, rhs = eq.split("=", 1)

        def delta(x: float) -> float:
            return leqs._eval_expr_at_x(lhs, x) - leqs._eval_expr_at_x(rhs, x)

        b = delta(0.0)
        a = delta(1.0) - b
        if abs(delta(2.0) - (a * 2.0 + b)) > 1e-4:
            return None
        if abs(delta(-1.0) - (a * -1.0 + b)) > 1e-4:
            return None
        return (round(a, 6), round(b, 6))
    except Exception:
        return None


def fingerprints_for_question(q: dict) -> set[str]:
    """Multiple keys so spacing, formatting, and equivalent equations match."""
    text = question_text(q)
    norm = normalize_question_text(text)
    fps: set[str] = {f"text:{norm}"}
    eq = extract_equation(q)
    if eq:
        eq_norm = normalize_equation(eq)
        fps.add(f"eq:{eq_norm}")
        sig = linear_equation_signature(_normalize_unicode(eq))
        if sig is not None:
            fps.add(f"sig:{sig[0]}:{sig[1]}")
    # Numbers-only skeleton (catches same structure, different variable labels).
    skeleton = re.sub(r"[a-z]", "v", norm)
    skeleton = re.sub(r"\s+", "", skeleton)
    fps.add(f"sk:{skeleton}")
    return fps


def is_duplicate_of_any(q: dict, seen: set[str]) -> bool:
    return bool(fingerprints_for_question(q) & seen)


def register_fingerprints(q: dict, seen: set[str]) -> None:
    seen.update(fingerprints_for_question(q))
