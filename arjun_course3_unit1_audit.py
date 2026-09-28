"""Independently recompute Unit 1 MCQ answer keys (school packet + Grok clones)."""

from __future__ import annotations

import json
import math
import re
from fractions import Fraction
from pathlib import Path

import arjun_course3_answers as c3ans
from arjun_course3_concept_check_store import _unit_path, load_ai_bank
from arjun_course3_unit1_practice import UNIT1_QUESTION_BANK
from numeric_expression_eval import (
    _expand_unicode_exponents,
    _sanitize_math_text,
    comma_separated_int_tuple,
    compute_expected,
    compute_fraction_of_remainder,
    ensure_simplest_form_answer,
    evaluate_numeric,
    find_matching_option_index,
    find_ordering_option_index,
    option_numeric_value,
    parse_mixed_number_value,
    parse_rational_token,
)

_FRAC = re.compile(r"(-?\d+)\s*/\s*(-?\d+)")
_MIXED = re.compile(r"(-?\d+)\s+(\d+)\s*/\s*(-?\d+)")
_INT = re.compile(r"-?\d+(?:\.\d+)?")
_OVERLINE = "\u0305"


def _frac(num: int, den: int) -> Fraction:
    return Fraction(num, den)


def _to_fraction(text: str) -> Fraction | None:
    raw = str(text).strip()
    mixed = parse_mixed_number_value(raw)
    if mixed is not None:
        m = _MIXED.match(raw)
        if m:
            whole, num, den = int(m.group(1)), int(m.group(2)), int(m.group(3))
            sign = -1 if whole < 0 else 1
            return Fraction(sign * (abs(whole) * den + num), den)
    m = _FRAC.fullmatch(re.sub(r"\s+", "", raw))
    if m:
        den = int(m.group(2))
        if den == 0:
            return None
        return Fraction(int(m.group(1)), den)
    try:
        if re.fullmatch(r"-?\d+$", raw):
            return Fraction(int(raw), 1)
        if re.fullmatch(r"-?\d+\.\d+$", raw):
            return Fraction(raw)
    except ValueError:
        return None
    return None


def _all_fractions(text: str) -> list[Fraction]:
    out: list[Fraction] = []
    used: set[tuple[int, int, int]] = set()
    for m in _MIXED.finditer(text):
        span = (m.start(), m.end(), 1)
        used.add(span)
        whole, num, den = int(m.group(1)), int(m.group(2)), int(m.group(3))
        sign = -1 if whole < 0 else 1
        out.append(Fraction(sign * (abs(whole) * den + num), den))
    for m in _FRAC.finditer(text):
        if any(m.start() >= a and m.end() <= b for a, b, _ in used):
            continue
        den = int(m.group(2))
        if den:
            out.append(Fraction(int(m.group(1)), den))
    return out


def _nth_int(text: str, n: int = 0) -> int | None:
    nums = [int(x) for x in re.findall(r"-?\d+", text)]
    if n < len(nums):
        return nums[n]
    return None


_UNIT_SUFFIX_RE = re.compile(
    r"\s*(?:m²|cm²|in²|ft²|m2|cm2|in2|lb|pounds?|meters?|cm|in)\s*$",
    re.I,
)


def _option_number(opt: str) -> float | None:
    val = option_numeric_value(opt)
    if val is not None:
        return val
    cleaned = _UNIT_SUFFIX_RE.sub("", str(opt).strip())
    if cleaned != str(opt).strip():
        val = option_numeric_value(cleaned)
        if val is not None:
            return val
        frac = _to_fraction(cleaned)
        if frac is not None:
            return float(frac)
    lead = re.match(
        r"^\s*(-?\d+\s+\d+/\d+|-?\d+/\d+|-?\d+(?:\.\d+)?%?)",
        str(opt),
    )
    if lead:
        token = lead.group(1)
        if token.endswith("%"):
            parsed = parse_rational_token(token)
            return parsed * 100 if parsed is not None and parsed <= 1 else parsed
        frac = _to_fraction(token)
        if frac is not None:
            return float(frac)
        try:
            return float(token)
        except ValueError:
            return None
    return None


def _match_value(expected: float | Fraction, options: list[str]) -> int | None:
    """Match an option whose numeric value equals expected, not a number buried in a sentence."""
    value = float(expected)
    idx = find_matching_option_index(value, options)
    if idx is not None:
        opt = str(options[idx]).strip()
        if re.match(r"^(yes|no|who|he|she|liam|nora|sam|maya|ben)\b", opt, re.I):
            return None
        return idx
    for i, opt in enumerate(options):
        if re.match(r"^(yes|no|who|he|she)\b", str(opt).strip(), re.I):
            continue
        parsed = _option_number(opt)
        if parsed is not None and abs(parsed - value) <= 1e-4 * max(1.0, abs(value)):
            return i
    return None


def _match_trailing_number(expected: float | Fraction, options: list[str]) -> int | None:
    value = float(expected)
    hits = []
    for i, opt in enumerate(options):
        if ";" not in str(opt) and "next" not in str(opt).lower():
            continue
        nums = re.findall(r"-?\d+(?:\.\d+)?", str(opt))
        if nums and abs(float(nums[-1]) - value) <= 1e-6 * max(1.0, abs(value)):
            hits.append(i)
    return hits[0] if len(hits) == 1 else None


def _repeating_decimal_fraction(stem: str) -> Fraction | None:
    text = str(stem)
    if re.search(r"which is greater|compare|increasing|decreasing", text, re.I):
        return None
    if not re.search(r"convert|fraction|simplest form", text, re.I):
        return None
    ellipsis = re.search(r"0\.(\d+)\s*(?:…|\.\.\.)", text)
    if ellipsis:
        digits = ellipsis.group(1)
        if digits:
            return Fraction(int(digits), 10 ** len(digits) - 1)
    # Combining overline after digits: 0.1̅6̅ or 0.̅6
    m = re.search(r"0\.((?:\d" + _OVERLINE + r"?)+)", text)
    if not m:
        return None
    chunk = m.group(1)
    repeating = ""
    i = 0
    while i < len(chunk):
        if chunk[i].isdigit():
            if i + 1 < len(chunk) and chunk[i + 1] == _OVERLINE:
                repeating += chunk[i]
                i += 2
                continue
            # non-repeating leading decimal digit (0.1̅6 would be unusual here)
            i += 1
            continue
        i += 1
    if repeating:
        return Fraction(int(repeating), 10 ** len(repeating) - 1)
    return None


def _is_perfect_square(n: float) -> bool:
    if n < 0 or abs(n - round(n)) > 1e-9:
        return False
    r = round(math.sqrt(n))
    return r * r == int(round(n))


def _is_perfect_cube(n: float) -> bool:
    if abs(n - round(n)) > 1e-9:
        return False
    r = round(n ** (1 / 3) if n >= 0 else -((-n) ** (1 / 3)))
    return r * r * r == int(round(n))


def _term_is_rational(token: str) -> bool | None:
    t = token.strip().replace(" ", "")
    if t.lower() in {"π", "pi"}:
        return False
    if re.fullmatch(r"-?\d+(?:\.\d+)?", t):
        return True
    if _FRAC.fullmatch(t):
        return True
    cube = re.fullmatch(r"∛(-?\d+(?:\.\d+)?)", t)
    if cube:
        return _is_perfect_cube(float(cube.group(1)))
    sq = re.fullmatch(r"√(-?\d+(?:\.\d+)?)", t)
    if sq:
        val = float(sq.group(1))
        if val < 0:
            return None
        return _is_perfect_square(val)
    return None


def _rationals_in_set(stem: str) -> list[str] | None:
    m = re.search(r"\{([^}]+)\}", stem)
    if not m:
        return None
    tokens = [p.strip() for p in m.group(1).split(",") if p.strip()]
    if len(tokens) < 2:
        return None
    keep: list[str] = []
    for tok in tokens:
        flag = _term_is_rational(tok)
        if flag is None:
            return None
        if flag:
            keep.append(tok.strip())
    return keep


def _best_option_for_rationals(keep: list[str], options: list[str], tokens: list[str]) -> int | None:
    keep_n = {re.sub(r"\s+", "", k) for k in keep}
    scores: list[tuple[int, int]] = []
    for i, opt in enumerate(options):
        compact = re.sub(r"\s+", "", str(opt))
        if re.search(r"all of them", opt, re.I):
            hit = len(keep_n) if len(keep_n) == len(tokens) else -1
            scores.append((hit, i))
            continue
        hit = sum(1 for k in keep_n if k in compact)
        extra = sum(1 for t in tokens if re.sub(r"\s+", "", t) in compact and re.sub(r"\s+", "", t) not in keep_n)
        scores.append((hit - extra, i))
    scores.sort(reverse=True)
    if not scores:
        return None
    best, idx = scores[0]
    if best <= 0:
        return None
    if len(scores) > 1 and scores[1][0] == best:
        return None
    return idx


def _arithmetic_nth_term(stem: str) -> Fraction | None:
    q = str(stem).lower()
    m = re.search(
        r"(?:starts at|begins at|start the sequence at)\s+"
        r"(-?\d+\s+\d+/\d+|-?\d+/\d+|-?\d+(?:\.\d+)?)\s+and (?:adds|add|increases by)\s+"
        r"(-?\d+\s+\d+/\d+|-?\d+/\d+|-?\d+(?:\.\d+)?)",
        q,
    )
    n_m = re.search(r"(\d+)(?:st|nd|rd|th) term", q)
    if not m or not n_m:
        return None
    a = _to_fraction(m.group(1))
    d = _to_fraction(m.group(2))
    n = int(n_m.group(1))
    if a is None or d is None or n < 1:
        return None
    return a + d * (n - 1)


def _listed_sequence_next(stem: str, count: int = 1) -> list[float] | None:
    m = re.search(r"pattern[:\s]+(-?\d+(?:\s*,\s*-?\d+){2,})\s*(?:…|\.\.\.)?", stem, re.I)
    if not m:
        m = re.search(r":\s*(-?\d+(?:\s*,\s*-?\d+){2,})\s*(?:…|\.\.\.)", stem)
    if not m:
        return None
    nums = [float(x) for x in re.findall(r"-?\d+", m.group(1))]
    if len(nums) < 3:
        return None
    diffs = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    if all(abs(d - diffs[0]) < 1e-9 for d in diffs):
        out = []
        cur = nums[-1]
        for _ in range(count):
            cur += diffs[0]
            out.append(cur)
        return out
    if all(nums[i] != 0 and abs(nums[i + 1] / nums[i] - nums[1] / nums[0]) < 1e-9 for i in range(len(nums) - 1)):
        ratio = nums[1] / nums[0]
        out = []
        cur = nums[-1]
        for _ in range(count):
            cur *= ratio
            out.append(cur)
        return out
    return None


def _how_many_pieces(stem: str) -> Fraction | None:
    q = str(stem).lower()
    if not re.search(r"how many (?:full )?(?:pieces|servings|layers)", q):
        return None
    if re.search(r"can be made using|layers can", q):
        return None
    fracs = _all_fractions(stem)
    if len(fracs) < 2:
        return None
    total, piece = fracs[0], fracs[1]
    if piece == 0:
        return None
    return total / piece


def _fraction_operation(stem: str) -> Fraction | None:
    q = _sanitize_math_text(stem)
    m = re.search(r"what is\s+(.+?)\s*\??\s*$", q, re.I)
    expr = m.group(1) if m else None
    if not expr:
        m = re.search(r"(add|subtract|multiply|divide).{0,40}?\b(\d+\s+\d+/\d+|\d+/\d+)\s*[+\-×x÷/]\s*(\d+\s+\d+/\d+|\d+/\d+)", q, re.I)
        if not m:
            m2 = re.search(r"(\d+\s+\d+/\d+|\d+/\d+)\s*([+\-×x÷/])\s*(\d+\s+\d+/\d+|\d+/\d+)", q)
            if not m2:
                return None
            left, op, right = m2.group(1), m2.group(2), m2.group(3)
        else:
            return None
    else:
        m2 = re.search(r"(\d+\s+\d+/\d+|\d+/\d+)\s*([+\-×x÷/])\s*(\d+\s+\d+/\d+|\d+/\d+)", expr)
        if not m2:
            val = evaluate_numeric(expr)
            return Fraction(val).limit_denominator(1000) if val is not None else None
        left, op, right = m2.group(1), m2.group(2), m2.group(3)
    a, b = _to_fraction(left), _to_fraction(right)
    if a is None or b is None:
        return None
    if op in {"+", "add"}:
        return a + b
    if op in {"-", "subtract"}:
        return a - b
    if op in {"×", "x", "*"}:
        return a * b
    if op in {"÷", "/"} and b != 0:
        return a / b
    return None


def _remaining_fraction(stem: str) -> Fraction | None:
    q = str(stem).lower()
    if not re.search(r"remain|left after|were left", q):
        return None
    if re.search(r"of (?:the )?(?:remaining|rest)", q):
        return None
    fracs = _all_fractions(stem)
    if len(fracs) < 2:
        return None
    if len(fracs) == 2:
        whole = Fraction(1, 1)
        return whole - fracs[0] - fracs[1]
    # picked a, ate b, gave c
    if len(fracs) >= 3:
        return fracs[0] - fracs[1] - fracs[2]
    return None


def _as_percent(stem: str) -> float | None:
    q = str(stem).lower()
    if "as a percent" not in q and "as a %" not in q and "to a percent" not in q:
        if not (q.startswith("write ") and "percent" in q):
            return None
    # skip two-part "as a decimal and as a percent"
    if "decimal" in q and "percent" in q:
        return None
    fr = _all_fractions(stem)
    if len(fr) == 1:
        return float(fr[0] * 100)
    m = re.search(r"write\s+(-?\d+\.\d+)\s+as a percent", q)
    if m:
        return float(m.group(1)) * 100
    return None


def _estimate_root(stem: str) -> float | None:
    q = str(stem)
    if "nearest tenth" not in q.lower():
        return None
    m = re.search(r"√\s*\(?\s*(\d+(?:\.\d+)?)", q)
    if m:
        return round(math.sqrt(float(m.group(1))), 1)
    m = re.search(r"∛\s*\(?\s*(\d+(?:\.\d+)?)", q)
    if m:
        return round(float(m.group(1)) ** (1 / 3), 1)
    return None


def _square_area_from_perimeter(stem: str) -> float | None:
    q = str(stem).lower()
    if "square" not in q or "area" not in q:
        return None
    m = re.search(r"perimeter of\s+(\d+(?:\.\d+)?)", q)
    if not m:
        m = re.search(r"perimeter\s+(\d+(?:\.\d+)?)", q)
    if not m:
        return None
    side = float(m.group(1)) / 4.0
    return side * side


def _square_area_from_side(stem: str) -> float | None:
    q = str(stem).lower()
    if "square" not in q or "area" not in q:
        return None
    m = re.search(r"side length of\s+(\d+(?:\.\d+)?)", q)
    if not m:
        return None
    s = float(m.group(1))
    return s * s


def _solve_power_equation(stem: str) -> float | None:
    q = _expand_unicode_exponents(_sanitize_math_text(stem))
    m = re.search(r"([a-zA-Z])\s*\^\s*2\s*=\s*(\d+(?:\.\d+)?)", q)
    if m:
        return math.sqrt(float(m.group(2)))
    m = re.search(r"([a-zA-Z])\s*\^\s*3\s*=\s*(\d+(?:\.\d+)?)", q)
    if m:
        return float(m.group(2)) ** (1 / 3)
    m = re.search(r"x\s*²\s*=\s*(\d+)", stem)
    if m:
        return math.sqrt(float(m.group(1)))
    m = re.search(r"y\s*³\s*=\s*(\d+)", stem)
    if m:
        return float(m.group(1)) ** (1 / 3)
    return None


def _same_base_power(stem: str) -> tuple[str, int] | None:
    q = _expand_unicode_exponents(_sanitize_math_text(stem))
    if "(" in q or ")" in q:
        return None
    if len(re.findall(r"[·•×*]", q)) > 1:
        return None
    prod = re.search(r"([A-Za-z]|\d+)\s*\^\s*(-?\d+)\s*[·•*]\s*\1\s*\^\s*(-?\d+)", q)
    if prod:
        return prod.group(1), int(prod.group(2)) + int(prod.group(3))
    div = re.search(r"([A-Za-z]|\d+)\s*\^\s*(-?\d+)\s*(?:÷|/)\s*\1\s*\^\s*(-?\d+)", q)
    if div:
        return div.group(1), int(div.group(2)) - int(div.group(3))
    return None


def _match_power_option(base: str, exp: int, options: list[str]) -> int | None:
    want = {f"{base}^{exp}", f"{base}^{{{exp}}}", f"{base}{''.join(chr(0x2070 + int(d) if d != '1' else 0x00B9) for d in str(exp))}"}
    # unicode superscript mapping is messy; compare parsed power terms
    from numeric_expression_eval import _parse_power_term

    for i, opt in enumerate(options):
        term = _parse_power_term(str(opt).split()[0])
        if term is None:
            compact = _expand_unicode_exponents(_sanitize_math_text(opt))
            term = _parse_power_term(compact)
        if term is not None:
            b, e = term
            try:
                if abs(b - float(base)) < 1e-9 and int(e) == exp:
                    return i
            except ValueError:
                if str(int(b)) == base and int(e) == exp:
                    return i
            if base.isalpha() and int(e) == exp and str(opt).replace(" ", "").lower().startswith(base.lower()):
                return i
        compact = _expand_unicode_exponents(_sanitize_math_text(opt)).replace(" ", "")
        if f"{base}^{exp}" in compact:
            return i
    return None


def _was_root_between_correct(stem: str) -> bool | None:
    q = str(stem)
    if "was " not in q.lower() or "correct" not in q.lower():
        return None
    m = re.search(r"√\s*(\d+)\s+is between\s+(\d+)\s+and\s+(\d+)", q)
    if not m:
        m = re.search(r"√\s*(\d+).{0,40}between\s+(\d+)\s+and\s+(\d+)", q)
    if not m:
        return None
    n, lo, hi = float(m.group(1)), float(m.group(2)), float(m.group(3))
    val = math.sqrt(n)
    return lo < val < hi


def _yes_no_index(claim_true: bool, options: list[str]) -> int | None:
    yes = [i for i, o in enumerate(options) if re.match(r"^\s*yes\b", str(o), re.I)]
    no = [i for i, o in enumerate(options) if re.match(r"^\s*no\b", str(o), re.I)]
    pool = yes if claim_true else no
    if len(pool) == 1:
        return pool[0]
    if len(pool) > 1:
        # prefer the mathematically specific option (mentions the bound numbers)
        return pool[-1] if claim_true else pool[0]
    return None


def independent_answer_index(question: dict) -> tuple[int | None, str]:
    """Return (option index, how it was verified) or (None, skip reason)."""
    stem = str(question.get("question", ""))
    options = [str(o) for o in (question.get("options") or [])]
    if len(options) != 4:
        return None, "not-4-options"

    lower = stem.lower()
    order = find_ordering_option_index(stem, options)
    if order is not None:
        return order, "ordering"

    if (
        not re.search(r"which answer\(s\)|all of the above|more than one|scientific notation", lower)
        and "× 10" not in stem
        and "x 10" not in lower
    ):
        expected = compute_expected(stem)
        if expected is not None:
            idx = _match_value(expected, options)
            if idx is not None:
                return idx, "compute_expected"

    nth = _arithmetic_nth_term(stem)
    if nth is not None:
        idx = _match_value(nth, options)
        if idx is not None:
            return idx, "arithmetic-nth"

    want_terms = 2 if re.search(r"next two", lower) else 1
    seq = _listed_sequence_next(stem, want_terms)
    if seq is not None:
        if want_terms == 2:
            expected_pair = tuple(int(round(x)) for x in seq)
            for i, opt in enumerate(options):
                if comma_separated_int_tuple(opt) == expected_pair:
                    return i, "sequence-next"
        else:
            idx = _match_value(seq[0], options) or _match_trailing_number(seq[0], options)
            if idx is not None:
                return idx, "sequence-next"

    pieces = _how_many_pieces(stem)
    if pieces is not None:
        val: float | Fraction = math.floor(float(pieces)) if "full" in lower else pieces
        idx = _match_value(val, options)
        if idx is not None:
            return idx, "pieces"

    nested = compute_fraction_of_remainder(stem)
    if nested is not None:
        idx = _match_value(nested, options)
        if idx is not None:
            return idx, "nested-remaining"

    rem = _remaining_fraction(stem)
    if rem is not None:
        idx = _match_value(rem, options)
        if idx is not None:
            return idx, "remaining"

    op = _fraction_operation(stem)
    if op is not None:
        idx = _match_value(op, options)
        if idx is not None:
            return idx, "fraction-op"

    pct = _as_percent(stem)
    if pct is not None:
        idx = _match_value(pct, options)
        if idx is not None:
            return idx, "percent"

    repeating = _repeating_decimal_fraction(stem)
    if repeating is not None:
        idx = _match_value(repeating, options)
        if idx is not None:
            try:
                idx = ensure_simplest_form_answer(stem, options, idx)
            except ValueError:
                pass
            return idx, "repeating"

    est = _estimate_root(stem)
    if est is not None:
        idx = _match_value(est, options)
        if idx is not None:
            return idx, "estimate-root"

    if not any(re.match(r"^(yes|no|who|he|she)\b", str(o), re.I) for o in options):
        area_p = _square_area_from_perimeter(stem)
        if area_p is not None:
            idx = _match_value(area_p, options)
            if idx is not None:
                return idx, "square-perimeter-area"
        area_s = _square_area_from_side(stem)
        if area_s is not None:
            idx = _match_value(area_s, options)
            if idx is not None:
                return idx, "square-side-area"

    if not any(" or " in str(o).lower() for o in options):
        pow_eq = _solve_power_equation(stem)
        if pow_eq is not None:
            idx = _match_value(pow_eq, options)
            if idx is not None:
                return idx, "power-eq"

    same = _same_base_power(stem)
    if same is not None:
        idx = _match_power_option(same[0], same[1], options)
        if idx is not None:
            return idx, "same-base-power"

    keep = _rationals_in_set(stem)
    if keep is not None and "name the rational" in stem.lower():
        m = re.search(r"\{([^}]+)\}", stem)
        tokens = [p.strip() for p in m.group(1).split(",")] if m else keep
        idx = _best_option_for_rationals(keep, options, tokens)
        if idx is not None:
            return idx, "rationals-in-set"

    claim = _was_root_between_correct(stem)
    if claim is not None:
        idx = _yes_no_index(claim, options)
        if idx is not None:
            return idx, "was-root-between"

    return None, "skipped"


def iter_unit1_seed_questions() -> list[dict]:
    """Base 105 + AI bank (school-seeded and older concept-check JSON)."""
    from arjun_course3_concept_check_store import load_ai_bank
    from arjun_course3_unit1_practice import UNIT1_QUESTION_BANK

    out: list[dict] = []
    seen: set[str] = set()
    for q in list(UNIT1_QUESTION_BANK) + load_ai_bank(1):
        qid = str(q.get("id", ""))
        if qid and qid in seen:
            continue
        out.append(q)
        if qid:
            seen.add(qid)
    return out


def collect_unverified_unit1_questions() -> list[dict]:
    """Questions the local math checker cannot uniquely prove."""
    return [q for q in iter_unit1_seed_questions() if independent_answer_index(q)[0] is None]


def audit_questions(questions: list[dict]) -> dict:
    ok: list[dict] = []
    mismatch: list[dict] = []
    skipped: list[dict] = []
    unfixable: list[dict] = []
    for q in questions:
        keyed = q.get("answer")
        idx, how = independent_answer_index(q)
        row = {
            "id": q.get("id"),
            "category": q.get("category"),
            "source": q.get("source"),
            "how": how,
            "keyed": keyed,
            "computed": idx,
            "stem": str(q.get("question", ""))[:160],
            "keyed_opt": (q.get("options") or [None] * 4)[keyed] if isinstance(keyed, int) and keyed in range(4) else None,
            "computed_opt": (q.get("options") or [None] * 4)[idx] if isinstance(idx, int) else None,
        }
        if idx is None:
            skipped.append(row)
        elif idx == keyed:
            ok.append(row)
        else:
            row["question"] = q
            mismatch.append(row)
    return {"ok": ok, "mismatch": mismatch, "skipped": skipped, "unfixable": unfixable}


def apply_ai_bank_fixes(unit_id: int = 1) -> dict:
    """Fix wrong keys in the AI JSON bank; drop items whose true answer is not an option."""
    path = _unit_path(unit_id)
    original = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []
    kept: list[dict] = []
    fixed = 0
    dropped = 0
    verified = 0
    skipped = 0
    for item in original:
        q = dict(item)
        idx, how = independent_answer_index(q)
        if idx is None:
            skipped += 1
            kept.append(q)
            continue
        verified += 1
        if idx == q.get("answer"):
            kept.append(q)
            continue
        opts = q.get("options") or []
        if idx not in range(len(opts)):
            dropped += 1
            continue
        q["answer"] = idx
        q["answer_verified"] = how
        kept.append(c3ans.finalize_question(q))
        fixed += 1
    path.write_text(json.dumps(kept, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "path": str(path),
        "before": len(original),
        "after": len(kept),
        "fixed": fixed,
        "dropped": dropped,
        "verified": verified,
        "skipped": skipped,
    }
