"""Shared formatting rules and validation for kid-friendly LLM math questions."""

from __future__ import annotations

import re

# Spelled-out fractions like "two thirds", "eight fifteenths"
_WORD_FRACTION_RE = re.compile(
    r"\b("
    r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
    r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred"
    r")\s+("
    r"half|halves|third|thirds|fourth|fourths|quarter|quarters|"
    r"fifth|fifths|sixth|sixths|seventh|sevenths|eighth|eighths|"
    r"ninth|ninths|tenth|tenths|eleventh|elevenths|twelfth|twelfths"
    r")\b",
    re.I,
)

KID_NUMERIC_FORMAT_RULES = """
NUMERICAL FORMAT (required — an 11-year-old must read numbers at a glance):
- Write ALL fractions as numerals with a slash: 2/3, 4/5, 8/15 — NEVER spell them ("two thirds", "eight fifteenths").
- Write operations with symbols: use × for multiply, ÷ for divide, + − and = where helpful.
- Good fraction question: "Multiply: 2/3 × 4/5 = ?" or "What is 2/3 × 4/5?"
- Good fraction options: "8/15", "2/15", "6/10", "1/3" — all numeric, same style.
- Decimals as digits: 0.75, 1.5 — not "three quarters" unless the lesson is explicitly about words.
- Percents as digits: 25%, 40% — not "twenty-five percent".
- Keep questions short and direct; one clear task per question.
- BAD: "Multiply the fractions two thirds and four fifths." / "eight fifteenths"
- GOOD: "Multiply: 2/3 × 4/5 = ?" with options ["8/15", "2/15", "6/8", "4/15"]
"""


def validate_numerical_format(question: str, options: list[str]) -> None:
    """Raise ValueError if question or options use spelled-out fractions."""
    texts = [question, *options]
    for text in texts:
        if _WORD_FRACTION_RE.search(text):
            raise ValueError(
                "Use numeric fractions (e.g. 2/3, 8/15), not words like 'two thirds' or 'eight fifteenths'"
            )


NUMERIC_RETRY_HINT = (
    "Use NUMERIC notation only: fractions as 2/3 (not 'two thirds'), "
    "roots as √3 or (√3)^2 (not \\\\sqrt{{3}} or LaTeX), "
    "options like 8/15 (not 'eight fifteenths'), × and ÷ symbols, short clear wording."
)

_META_QUESTION_PHRASES = (
    "which best describes",
    "chapter example",
    "history note",
    "theorem with proof",
    "unrelated formula",
    "worked example from",
    "from exercise",
)

_META_OPTION_PHRASES = (
    "theorem with proof",
    "history note only",
    "unrelated formula",
    "worked example from the ncert chapter",
    "i can solve this using the chapter method",
    "review in textbook",
)

# PDF extraction often drops blank words — reject these broken stems.
_BROKEN_STATEMENT_PATTERNS = (
    r"\bin of the\b",
    r"\bis a of the\b",
    r"\bis a when\b",
    r"\band of the circle\b",
    r"\bis of the form\b",
    r"\bin parts\s*$",
    r"\bthe circle and\s*$",
    r"\(exterior\s*/\s*interior\)",
    r"\(interior\s*/\s*exterior\)",
    r";\s*$",
    r"^\s*inside the circle,\s*which",
    r"^\s*the circle and\s*$",
    r"\bbetween an arc and of the\b",
)

_FILL_BLANK_TAIL_RE = re.compile(r"\(([^/)]+)/\s*([^)]+)\)\s*\.?\s*$")


def _statement_from_true_false_question(question: str) -> str:
    q = str(question).strip()
    prefix = "true or false?"
    if q.lower().startswith(prefix):
        return q[len(prefix) :].strip()
    return q


def is_quality_true_false_statement(statement: str) -> bool:
    """True/false stem must be a complete sentence — not a fill-in-blank fragment."""
    s = re.sub(r"\s+", " ", str(statement).strip().lower())
    if len(s) < 15 or len(s) > 120:
        return False
    if _FILL_BLANK_TAIL_RE.search(s):
        return False
    for pat in _BROKEN_STATEMENT_PATTERNS:
        if re.search(pat, s):
            return False
    if s.count(" ") < 4:
        return False
    return True


def is_quality_practice_question(question: str, options: list[str]) -> bool:
    """Reject meta/categorization prompts, true/false, and placeholder MCQs."""
    q = str(question).strip()
    q_lower = q.lower()
    opts = [str(o).strip().lower() for o in options]
    if len(q) < 12 or len(q) > 220:
        return False
    # Practice must be solvable math MCQs — not true/false drills.
    if q_lower.startswith("true or false?") or q_lower.startswith("true or false:"):
        return False
    tf_opts = {"true", "false", "cannot say", "only sometimes", "none of these"}
    if tf_opts.issuperset(set(opts)):
        return False
    if any(p in q_lower for p in _META_QUESTION_PHRASES):
        return False
    if "solution :" in q_lower or "solution:" in q_lower:
        return False
    if q_lower.startswith("(from exercise"):
        return False
    meta_opts = sum(1 for o in opts if any(p in o for p in _META_OPTION_PHRASES))
    if meta_opts >= 2:
        return False
    if any(o == "i can solve this using the chapter method" for o in opts):
        return False
    if "quadrant" in q_lower and not re.search(r"\(\s*-?\d+\s*,\s*-?\d+\s*\)", q):
        if "point p" in q_lower or "marked on the coordinate" in q_lower:
            return False
    return True


def validate_practice_question(question: str, options: list[str]) -> None:
    """Raise ValueError if an LLM question is not a solvable student-facing MCQ."""
    validate_numerical_format(question, options)
    q_lower = str(question).strip().lower()
    if q_lower.startswith("true or false"):
        raise ValueError("Do not generate true/false questions — use 4 concrete answer choices.")
    opts_lower = {str(o).strip().lower() for o in options}
    if {"true", "false"}.issubset(opts_lower):
        raise ValueError("Options must be math answers, not True/False.")
    if not is_quality_practice_question(question, options):
        raise ValueError(
            "Question must be a solvable math problem with real answer choices — "
            "not a meta question about examples, exercises, or content types."
        )
    if len(options) != 4 or len({str(o).strip().lower() for o in options}) < 4:
        raise ValueError("Need 4 distinct, non-empty options.")
