"""Safe numeric expression evaluation for verifying LLM math MCQ answer keys."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from fractions import Fraction

_FRAC_RE = re.compile(r"^-?\d+/-?\d+$")
_INT_RE = re.compile(r"^-?\d+$")

_EXTRACT_PATTERNS: list[re.Pattern[str]] = [
    re.compile(
        r"^(?:Compute|Evaluate|Simplify|Add|Multiply|Subtract|Divide):\s*(.+?)(?:\s*=\s*\?)?\.?\s*$",
        re.I,
    ),
    re.compile(r"^(?:Compute|Evaluate)\s+(.+?)(?:\.|$)", re.I),
    re.compile(r"^What is\s+(.+?)\??\s*$", re.I),
    re.compile(r"^What is the value of\s+(.+?)\??\s*$", re.I),
]

_UNVERIFIABLE_HINTS = (
    "which ",
    "how many",
    "where ",
    "ordered pair",
    "equation ",
    "polynomial",
    "binomial",
    "p(x)",
    "on the number line",
    "between ",
    "infinitely",
    "classify",
    "factor",
    "expand",
    "write ",
    "complete the",
    "represents",
    "satisfies",
    "cost of",
    "diagram",
    "scientific notation",
    "× 10^",
    "\\times 10",
    "10^",
    "true or false",
    "do not solve",
    "setup",
    "table shows",
    "graph",
    "scatter",
    "percent of",
    "probability",
    "mean absolute",
    "slope",
    "intercept",
    "y =",
    "x =",
)

_SUPER_DIGITS = {
    "⁰": "0",
    "¹": "1",
    "²": "2",
    "³": "3",
    "⁴": "4",
    "⁵": "5",
    "⁶": "6",
    "⁷": "7",
    "⁸": "8",
    "⁹": "9",
}


def _expand_unicode_exponents(text: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "⁻":
            j = i + 1
            digits = []
            while j < len(text) and text[j] in _SUPER_DIGITS:
                digits.append(_SUPER_DIGITS[text[j]])
                j += 1
            if digits:
                out.append("^(-" + "".join(digits) + ")")
                i = j
                continue
        if ch in _SUPER_DIGITS:
            digits = []
            while i < len(text) and text[i] in _SUPER_DIGITS:
                digits.append(_SUPER_DIGITS[text[i]])
                i += 1
            out.append("^" + "".join(digits))
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _sanitize_math_text(text: str) -> str:
    s = str(text or "")
    s = s.replace("\\times", "×").replace("\\div", "÷")
    s = s.replace("−", "-").replace("–", "-")
    s = _expand_unicode_exponents(s)
    return s


def _normalize_expr(text: str) -> str:
    s = _sanitize_math_text(text)
    s = s.replace("×", "*").replace("÷", "/")
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"(\d)\(", r"\1*(", s)
    s = re.sub(r"\)\(", r")*(", s)
    return s


def _parse_number_token(tok: str) -> float | None:
    tok = tok.strip()
    if not tok:
        return None
    if _INT_RE.fullmatch(tok):
        return float(int(tok))
    if _FRAC_RE.fullmatch(tok):
        num, den = tok.split("/", 1)
        try:
            return float(Fraction(int(num), int(den)))
        except ZeroDivisionError:
            return None
    if "." in tok:
        try:
            return float(tok)
        except ValueError:
            return None
    return None


@dataclass
class _Tok:
    kind: str
    value: str = ""


def _tokenize(expr: str) -> list[_Tok]:
    s = _normalize_expr(expr)
    tokens: list[_Tok] = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in "+*/^()":
            tokens.append(_Tok(ch))
            i += 1
            continue
        if ch == "-":
            prev = tokens[-1].kind if tokens else ""
            if not tokens or prev in ("+", "-", "*", "/", "^", "("):
                tokens.append(_Tok("u-"))
            else:
                tokens.append(_Tok("-"))
            i += 1
            continue
        if ch.isdigit() or ch == ".":
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == "."):
                j += 1
            if j < len(s) and s[j] == "/":
                k = j + 1
                while k < len(s) and (s[k].isdigit() or s[k] == "-"):
                    k += 1
                if k > j + 1:
                    tokens.append(_Tok("num", s[i:k]))
                    i = k
                    continue
            tokens.append(_Tok("num", s[i:j]))
            i = j
            continue
        raise ValueError(f"unexpected character {ch!r} at {i}")
    return tokens


class _Parser:
    def __init__(self, tokens: list[_Tok]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> _Tok | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _eat(self, kind: str | None = None) -> _Tok:
        tok = self._peek()
        if tok is None:
            raise ValueError("unexpected end of expression")
        if kind and tok.kind != kind:
            raise ValueError(f"expected {kind}, got {tok.kind}")
        self.pos += 1
        return tok

    def parse(self) -> float:
        val = self._expr()
        if self.pos != len(self.tokens):
            raise ValueError("trailing tokens")
        return val

    def _expr(self) -> float:
        val = self._term()
        while True:
            tok = self._peek()
            if tok is None or tok.kind not in ("+", "-"):
                break
            self._eat()
            rhs = self._term()
            val = val + rhs if tok.kind == "+" else val - rhs
        return val

    def _term(self) -> float:
        val = self._power()
        while True:
            tok = self._peek()
            if tok is None or tok.kind not in ("*", "/"):
                break
            self._eat()
            rhs = self._power()
            val = val * rhs if tok.kind == "*" else val / rhs
        return val

    def _power(self) -> float:
        val = self._unary()
        tok = self._peek()
        if tok and tok.kind == "^":
            self._eat("^")
            exp = self._power()
            val = val**exp
        return val

    def _unary(self) -> float:
        tok = self._peek()
        if tok and tok.kind == "u-":
            self._eat("u-")
            return -self._unary()
        return self._atom()

    def _atom(self) -> float:
        tok = self._peek()
        if tok is None:
            raise ValueError("expected value")
        if tok.kind == "num":
            self._eat("num")
            val = _parse_number_token(tok.value)
            if val is None:
                raise ValueError(f"cannot parse number {tok.value!r}")
            return val
        if tok.kind == "(":
            self._eat("(")
            val = self._expr()
            self._eat(")")
            tok = self._peek()
            if tok and tok.kind == "^":
                self._eat("^")
                exp = self._power()
                val = val**exp
            return val
        raise ValueError(f"unexpected token {tok.kind}")


def evaluate_numeric(expr: str) -> float | None:
    """Evaluate a plain numeric expression; None when parsing fails."""
    try:
        tokens = _tokenize(expr)
        if not tokens:
            return None
        return _Parser(tokens).parse()
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def extract_expression(question: str) -> str | None:
    q = _sanitize_math_text(question).strip()
    ql = q.lower()
    if any(h in ql for h in _UNVERIFIABLE_HINTS):
        return None
    for pat in _EXTRACT_PATTERNS:
        m = pat.match(q)
        if m:
            expr = m.group(1).strip().rstrip(".")
            expr = re.sub(r"\s*=\s*\?$", "", expr).strip()
            if expr and not re.search(r"[a-zA-Z]", expr):
                return expr
    return None


def compute_expected(question: str) -> float | None:
    expr = extract_expression(question)
    if not expr:
        return None
    return evaluate_numeric(expr)


def _format_fraction(value: float) -> str | None:
    if not math.isfinite(value):
        return None
    try:
        frac = Fraction(value).limit_denominator(10000)
        if abs(float(frac) - value) <= 1e-9:
            if frac.denominator == 1:
                return str(frac.numerator)
            return f"{frac.numerator}/{frac.denominator}"
    except (OverflowError, ValueError):
        pass
    return None


def option_numeric_value(text: str) -> float | None:
    s = _normalize_expr(str(text))
    if not s:
        return None
    val = _parse_number_token(s)
    if val is not None:
        return val
    if any(ch in s for ch in "+-*/^()"):
        return evaluate_numeric(s)
    return None


def options_equivalent(a: str, b: str) -> bool:
    a_norm = _normalize_expr(a)
    b_norm = _normalize_expr(b)
    if a_norm == b_norm:
        return True
    va, vb = option_numeric_value(a), option_numeric_value(b)
    if va is not None and vb is not None:
        return abs(va - vb) <= 1e-9
    return False


def find_matching_option_index(expected: float, options: list[str]) -> int | None:
    frac = _format_fraction(expected)
    candidates = [str(int(round(expected)))] if abs(expected - round(expected)) < 1e-9 else []
    if frac:
        candidates.append(frac)
    candidates.append(str(expected))

    for i, opt in enumerate(options):
        for cand in candidates:
            if options_equivalent(str(opt), cand):
                return i
        ov = option_numeric_value(str(opt))
        if ov is not None and abs(ov - expected) <= 1e-9:
            return i
    return None


def ensure_numeric_answer_key(question: str, options: list[str], answer: int) -> int:
    """Return the option index matching the evaluated expression; auto-fix wrong keys."""
    if not isinstance(answer, int) or answer not in range(len(options)):
        raise ValueError("answer must be a valid option index")
    expected = compute_expected(question)
    if expected is None:
        return answer
    idx = find_matching_option_index(expected, options)
    if idx is None:
        raise ValueError(
            f"Computed value {expected!r} is not among options for question: {question[:100]}"
        )
    return idx


def simplest_fraction_form(text: str) -> str | None:
    """Return a/b in lowest terms when text is a plain fraction; else None."""
    s = _normalize_expr(str(text))
    if not _FRAC_RE.fullmatch(s):
        return None
    num, den = s.split("/", 1)
    try:
        frac = Fraction(int(num), int(den))
    except (ValueError, ZeroDivisionError):
        return None
    return f"{frac.numerator}/{frac.denominator}"


def validate_distinct_options(options: list[str]) -> None:
    """Reject MCQs where two options represent the same value (e.g. 45/99 and 5/11)."""
    for i in range(len(options)):
        for j in range(i + 1, len(options)):
            if options_equivalent(options[i], options[j]):
                raise ValueError(
                    f"Options {i + 1} and {j + 1} are equivalent "
                    f"({options[i]!r} vs {options[j]!r}) — use only one form"
                )


def ensure_simplest_form_answer(question: str, options: list[str], answer: int) -> int:
    """When the stem asks for simplest form, point the key at the reduced fraction."""
    if "simplest form" not in str(question).lower():
        return answer
    correct = str(options[answer])
    reduced = simplest_fraction_form(correct)
    if reduced is None:
        return answer
    if _normalize_expr(correct) == reduced:
        return answer
    for i, opt in enumerate(options):
        if _normalize_expr(str(opt)) == reduced:
            return i
    raise ValueError(
        f"Answer {correct!r} is not in simplest form ({reduced}); "
        "include the reduced fraction as an option"
    )
