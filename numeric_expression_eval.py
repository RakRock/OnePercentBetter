"""Safe numeric expression evaluation for verifying LLM math MCQ answer keys."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from fractions import Fraction

_FRAC_RE = re.compile(r"^-?\d+/-?\d+$")
_INT_RE = re.compile(r"^-?\d+$")

_BAD_EXPLANATION_RE = re.compile(
    r"pick plausible|adjust:\s*actually|wait,\s*recalculate|"
    r"not in (?:the )?list|closest match|options adjusted|revised calc|"
    r"correct path yields|fix:\s*proper|closest match adjusted|"
    r"but options|yields \d+\? no|calc error|choose matching|needs adjustment",
    re.I,
)
_LINEAR_EXPR_RE = re.compile(r"(-?\d+)\s*n\s*([+-])\s*(\d+)", re.I)
_LINEAR_OPTION_RE = re.compile(r"^(-?\d*)n([+-])(\d+)$", re.I)
_LEADING_NUM_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?(?:/\d+)?)")
_VERBAL_CONTEXT_RE = re.compile(
    r"\b(?:more|less|per|every|each|start(?:ing)?|association|positive|negative|"
    r"cannot|both|walked|age|year|years|meter|meters|minute|minutes|fat|grams)\b",
    re.I,
)
_MIXED_NUM_RE = re.compile(r"^\s*(-?\d+)\s+(\d+)\s*/\s*(\d+)")
_THOUSANDS_SEP_RE = re.compile(r"^-?\d{1,3}(?:,\d{3})+(?:\.\d+)?$")
_EXPL_RESULT_RE = re.compile(r"=\s*(-?\d+(?:\.\d+)?)\s*(?:\?|\.|,|;|\s|$)")
_SCI_TERM_RE = re.compile(
    r"(-?\d+(?:\.\d+)?)\s*(?:×|x|\*|\\times)?\s*10\s*\^?\s*(-?\d+)",
    re.I,
)

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


def parse_mixed_number_value(text: str) -> float | None:
    """Parse whole-number + fraction forms like 8 1/3 or -6 1/2."""
    raw = str(text).strip()
    m = _MIXED_NUM_RE.match(raw)
    if not m:
        return None
    whole = int(m.group(1))
    num = int(m.group(2))
    den = int(m.group(3))
    if den == 0:
        return None
    frac_part = num / den
    if whole < 0:
        return float(whole) - frac_part
    return float(whole) + frac_part


def _strip_thousands_separators(text: str) -> str:
    """Remove grouping commas from plain integers like 1,456,789,874,500."""
    s = str(text).strip()
    if _THOUSANDS_SEP_RE.fullmatch(s):
        return s.replace(",", "")
    return s


def _contains_unicode_exponent(text: str) -> bool:
    return "⁻" in text or any(ch in _SUPER_DIGITS for ch in text)


def _parse_power_term(text: str) -> tuple[float, float] | None:
    """Return (base, exponent) when text is a single power like 3¹⁰⁰ or 3^100."""
    s = _normalize_expr(str(text).strip())
    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)\^(-?\d+(?:\.\d+)?)", s)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def power_options_equivalent(a: str, b: str) -> bool | None:
    """Compare single power expressions by base and exponent; None if not both powers."""
    pa = _parse_power_term(a)
    pb = _parse_power_term(b)
    if pa is None or pb is None:
        return None
    return pa == pb


def _parse_linear_n_expression(text: str) -> tuple[int, int] | None:
    """Parse an + b style options like 3n + 1 or n + 3 into (coefficient, constant)."""
    s = _normalize_expr(str(text).strip())
    if s.lower().count("n") != 1:
        return None
    m = _LINEAR_OPTION_RE.match(s)
    if not m:
        return None
    coeff_raw = m.group(1)
    if coeff_raw in ("", "+"):
        coeff = 1
    elif coeff_raw == "-":
        coeff = -1
    else:
        coeff = int(coeff_raw)
    const = int(m.group(3))
    offset = const if m.group(2) == "+" else -const
    return coeff, offset


def linear_n_options_equivalent(a: str, b: str) -> bool | None:
    """Compare linear expressions in n by coefficient and constant."""
    pa = _parse_linear_n_expression(a)
    pb = _parse_linear_n_expression(b)
    if pa is None or pb is None:
        return None
    return pa == pb


def _is_equation_system_option(text: str) -> bool:
    """True for paired equations like ``3p + 2d = 11 and 2p + 4d = 12``."""
    s = str(text).lower()
    if " and " not in s or "=" not in s:
        return False
    return bool(re.search(r"\d+\s*[pdxy]", s))


def _normalize_system_option(text: str) -> tuple[str, ...] | None:
    if not _is_equation_system_option(text):
        return None
    parts = [re.sub(r"\s+", "", p.strip().lower()) for p in str(text).split(" and ")]
    if len(parts) < 2 or not all("=" in p for p in parts):
        return None
    return tuple(sorted(parts))


def system_options_equivalent(a: str, b: str) -> bool | None:
    """Compare equation-system MCQ options by normalized equation set."""
    sa = _normalize_system_option(a)
    sb = _normalize_system_option(b)
    if sa is None or sb is None:
        return None
    return sa == sb


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
    if expr:
        val = evaluate_numeric(expr)
        if val is not None:
            return val
    return compute_fraction_of_remainder(question) or compute_linear_expression(question) or compute_scientific_notation_sum(question)


def _parse_scientific_notation_terms(text: str) -> list[tuple[float, int]]:
    s = _sanitize_math_text(text)
    return [
        (float(m.group(1)), int(m.group(2)))
        for m in _SCI_TERM_RE.finditer(s)
    ]


def parse_scientific_notation_value(text: str) -> float | None:
    terms = _parse_scientific_notation_terms(text)
    if len(terms) != 1:
        return None
    coef, exp = terms[0]
    return coef * (10 ** exp)


def is_proper_scientific_coefficient(coef: float) -> bool:
    """True when coefficient satisfies 1 ≤ |a| < 10 (standard scientific notation)."""
    return 1.0 <= abs(coef) < 10.0


def _single_scientific_notation_term(text: str) -> tuple[float, int] | None:
    terms = _parse_scientific_notation_terms(text)
    if len(terms) != 1:
        return None
    return terms[0]


def scientific_notation_options_equivalent(a: str, b: str) -> bool | None:
    """Compare sci-notation MCQ options; None when either side is not a single term.

    Same numeric value is not enough: 12×10⁹ and 1.2×10¹⁰ differ because only the
    latter uses a proper coefficient (1 ≤ |a| < 10).
    """
    ta = _single_scientific_notation_term(a)
    tb = _single_scientific_notation_term(b)
    if ta is None or tb is None:
        return None
    ca, ea = ta
    cb, eb = tb
    va = ca * (10 ** ea)
    vb = cb * (10 ** eb)
    if abs(va - vb) > 1e-9:
        return False
    proper_a = is_proper_scientific_coefficient(ca)
    proper_b = is_proper_scientific_coefficient(cb)
    if proper_a and proper_b:
        return True
    if proper_a != proper_b:
        return False
    return True


def compute_scientific_notation_sum(question: str) -> float | None:
    """Add two scientific-notation values, e.g. 4.5×10^6 + 3.2×10^5."""
    lower = str(question).lower()
    if not re.search(r"\badd\b", lower):
        return None
    terms = _parse_scientific_notation_terms(question)
    if len(terms) < 2:
        return None
    return sum(coef * (10 ** exp) for coef, exp in terms[:2])


_RATIONAL_TOKEN_RE = re.compile(r"\d+/\d+|\d+\.\d+|\d+%")


def parse_rational_token(token: str) -> float | None:
    raw = str(token).strip()
    if raw.endswith("%"):
        try:
            return float(raw[:-1]) / 100.0
        except ValueError:
            return None
    if "/" in raw:
        num, den = raw.split("/", 1)
        try:
            return float(Fraction(int(num), int(den)))
        except (ValueError, ZeroDivisionError):
            return None
    try:
        return float(raw)
    except ValueError:
        return None


def _extract_rational_tokens(question: str) -> list[str]:
    seen: list[str] = []
    for token in _RATIONAL_TOKEN_RE.findall(str(question)):
        if token not in seen:
            seen.append(token)
    return seen


def _ordering_values_from_option(option: str) -> tuple[float, ...] | None:
    tokens = _RATIONAL_TOKEN_RE.findall(str(option))
    if len(tokens) < 3:
        return None
    values: list[float] = []
    for token in tokens[:3]:
        val = parse_rational_token(token)
        if val is None:
            return None
        values.append(val)
    return tuple(values)


def find_ordering_option_index(question: str, options: list[str]) -> int | None:
    """Match greatest-to-least / least-to-greatest ordering MCQs."""
    lower = str(question).lower()
    if not re.search(r"greatest to least|least to greatest", lower):
        return None
    tokens = _extract_rational_tokens(question)
    if len(tokens) < 3:
        return None
    pairs = [(token, parse_rational_token(token)) for token in tokens[:3]]
    if any(val is None for _, val in pairs):
        return None
    descending = "greatest to least" in lower
    pairs.sort(key=lambda item: item[1], reverse=descending)
    expected = tuple(val for _, val in pairs)
    for i, opt in enumerate(options):
        ordered = _ordering_values_from_option(opt)
        if ordered == expected:
            return i
    return None


def compute_linear_expression(question: str) -> float | None:
    """Evaluate an + b style rules at a given figure number, e.g. 3n+1 at figure 45."""
    text = str(question)
    m = _LINEAR_EXPR_RE.search(text)
    if not m:
        return None
    a = int(m.group(1))
    sign = m.group(2)
    b = int(m.group(3))
    n_match = re.search(r"figure\s*(\d+)", text, re.I)
    if not n_match:
        n_match = re.search(r"\bn\s*=\s*(\d+)", text, re.I)
    if not n_match:
        return None
    n = int(n_match.group(1))
    offset = b if sign == "+" else -b
    return float(a * n + offset)


def compute_fraction_of_remainder(question: str) -> float | None:
    """Fraction-of-remainder word problems: eat 1/8, then 4/9 of what's left."""
    q = str(question).lower()
    if not re.search(r"\b(remaining|rest|left)\b", q):
        return None

    rem_match = re.search(r"(\d+)\s*/\s*(\d+)\s+of\s+(?:the\s+)?(?:remaining|rest)", q)
    if not rem_match:
        return None

    eaten: Fraction | None = None
    eat_match = re.search(
        r"(?:eating|eat|ate|removed|take out|taken out|taking)\s+(\d+)\s*/\s*(\d+)",
        q,
    )
    if eat_match:
        eaten = Fraction(int(eat_match.group(1)), int(eat_match.group(2)))
    else:
        choc_match = re.search(
            r"(\d+)\s*/\s*(\d+)\s+of\s+(?:them\s+are|the\s+(?:bar|candies|chocolate))",
            q,
        )
        if choc_match:
            eaten = Fraction(int(choc_match.group(1)), int(choc_match.group(2)))
        else:
            first_frac = re.search(r"(\d+)\s*/\s*(\d+)", q)
            if first_frac:
                eaten = Fraction(int(first_frac.group(1)), int(first_frac.group(2)))

    if eaten is None or eaten >= 1:
        return None

    portion = Fraction(int(rem_match.group(1)), int(rem_match.group(2)))
    result = (Fraction(1, 1) - eaten) * portion
    return float(result)


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
    raw = _strip_thousands_separators(str(text).strip())
    sci = parse_scientific_notation_value(raw)
    if sci is not None:
        return sci
    mixed = parse_mixed_number_value(raw)
    if mixed is not None:
        return mixed
    if _parse_linear_n_expression(raw) is not None:
        return None
    if _is_equation_system_option(raw):
        return None
    if _contains_unicode_exponent(raw) or "^" in _sanitize_math_text(raw):
        term = _parse_power_term(raw)
        if term is not None:
            base, exp = term
            if abs(exp) <= 400 and abs(base) <= 100:
                try:
                    return base ** exp
                except OverflowError:
                    return None
            return None
        s = _normalize_expr(raw)
        if any(ch in s for ch in "+-*/"):
            return evaluate_numeric(s)
        return None
    lead = _LEADING_NUM_RE.match(raw)
    if lead:
        val = _parse_number_token(lead.group(1))
        if val is not None:
            return val
    s = _normalize_expr(raw)
    if not s:
        return None
    val = _parse_number_token(s)
    if val is not None:
        return val
    if any(ch in s for ch in "+-*/^()"):
        return evaluate_numeric(s)
    return None


def _is_verbal_context_option(text: str) -> bool:
    """True for slope/rate/word-problem MCQ options that must not match by leading number alone."""
    return bool(_VERBAL_CONTEXT_RE.search(str(text)))


def options_equivalent(a: str, b: str) -> bool:
    a_order = _ordering_values_from_option(a)
    b_order = _ordering_values_from_option(b)
    if a_order is not None and b_order is not None:
        return a_order == b_order
    sci_equiv = scientific_notation_options_equivalent(a, b)
    if sci_equiv is not None:
        return sci_equiv
    pow_equiv = power_options_equivalent(a, b)
    if pow_equiv is not None:
        return pow_equiv
    lin_equiv = linear_n_options_equivalent(a, b)
    if lin_equiv is not None:
        return lin_equiv
    sys_equiv = system_options_equivalent(a, b)
    if sys_equiv is not None:
        return sys_equiv
    a_norm = _normalize_expr(a)
    b_norm = _normalize_expr(b)
    if a_norm == b_norm:
        return True
    if _is_verbal_context_option(a) or _is_verbal_context_option(b):
        return str(a).strip().casefold() == str(b).strip().casefold()
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


def _stem_requires_scientific_notation_answer(stem: str) -> bool:
    """True when the stem asks for a result written in scientific notation."""
    lower = str(stem).lower()
    if "scientific notation" not in lower:
        return False
    if re.search(r"(?:is|written in)\s+(?:correct\s+)?scientific notation\??", lower):
        return False
    return bool(re.search(r"(?:in|give|write|express|using)\s+scientific notation", lower))


def find_proper_scientific_notation_index(expected: float, options: list[str]) -> int | None:
    """Among sci-notation options matching ``expected``, prefer proper coefficient form."""
    fallback: int | None = None
    for i, opt in enumerate(options):
        terms = _parse_scientific_notation_terms(str(opt))
        if len(terms) != 1:
            continue
        coef, exp = terms[0]
        val = coef * (10 ** exp)
        if abs(val - expected) > 1e-6 * max(1.0, abs(expected)):
            continue
        if is_proper_scientific_coefficient(coef):
            return i
        if fallback is None:
            fallback = i
    return fallback


def validate_explanation_quality(explanation: str) -> None:
    """Reject Grok explanations that admit the answer key is wrong."""
    if _BAD_EXPLANATION_RE.search(str(explanation)):
        raise ValueError("Explanation contains self-correction or contradictory text")


def validate_explanation_matches_key(explanation: str, options: list[str], answer: int) -> None:
    """Reject when the explanation's final numeric result disagrees with the marked option."""
    validate_explanation_quality(explanation)
    matches = _EXPL_RESULT_RE.findall(str(explanation))
    if not matches:
        return
    try:
        conclusion = float(matches[-1])
    except ValueError:
        return
    idx = find_matching_option_index(conclusion, options)
    if idx is None:
        return
    if idx != answer:
        raise ValueError(
            f"Explanation concludes {matches[-1]} but answer key marks {options[answer]!r}"
        )


def ensure_numeric_answer_key(question: str, options: list[str], answer: int) -> int:
    """Return the option index matching the evaluated expression; auto-fix wrong keys."""
    if not isinstance(answer, int) or answer not in range(len(options)):
        raise ValueError("answer must be a valid option index")
    lower_q = str(question).lower()
    if re.search(r"which answer\(s\)|all of the above|more than one", lower_q):
        return answer
    if re.search(r"\bboth\b", str(options[answer]), re.I):
        return answer
    ordering_idx = find_ordering_option_index(question, options)
    if ordering_idx is not None:
        return ordering_idx
    expected = compute_expected(question)
    if expected is None:
        return answer
    idx = find_matching_option_index(expected, options)
    if idx is None:
        raise ValueError(
            f"Computed value {expected!r} is not among options for question: {question[:100]}"
        )
    if _stem_requires_scientific_notation_answer(lower_q):
        proper_idx = find_proper_scientific_notation_index(expected, options)
        if proper_idx is not None:
            return proper_idx
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
