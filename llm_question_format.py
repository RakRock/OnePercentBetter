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
    "options like 8/15 (not 'eight fifteenths'), × and ÷ symbols, short clear wording."
)
