#!/usr/bin/env python3
"""Audit Harshit Math question banks for wrong keys, duplicate options, and structural issues."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# harshit_math_render imports streamlit; stub it for CLI use.
if "streamlit" not in sys.modules:
    import types

    _st = types.ModuleType("streamlit")
    _st.markdown = lambda *a, **k: None
    _st.latex = lambda *a, **k: None
    sys.modules["streamlit"] = _st

import harshit_chapter_questions as hcq
import harshit_math_answers as hma
import harshit_math_render as hmr

BANK_DIR = hcq.BANK_DIR

# ---------------------------------------------------------------------------
# Safe numeric expression evaluator (+, -, ×, /, ^, √, fractions, parens)
# ---------------------------------------------------------------------------

_FRAC_RE = re.compile(r"^-?\d+/-?\d+$")
_INT_RE = re.compile(r"^-?\d+$")
_SQRT_RE = re.compile(r"^√(\d+)$")
_RADICAL_POWER_RE = re.compile(r"^\(√(\d+)\)\^(-?\d+)$")
_RATIONAL_POWER_RE = re.compile(r"^(\d+)\^\((-?\d+)/(\d+)\)$")
_INT_POWER_RE = re.compile(r"^(\d+)\^(-?\d+)$")
_COEFF_SQRT_RE = re.compile(r"^(-?\d+)√(\d+)$")
_SQRT_FRAC_RE = re.compile(r"^√(\d+)/(\d+)$")
_INV_SQRT_RE = re.compile(r"^1/√(\d+)$")
_NUM_INV_SQRT_RE = re.compile(r"^(\d+)/√(\d+)$")


def _normalize_expr(text: str) -> str:
    s = hmr.sanitize_grok_math_text(text)
    s = s.replace("−", "-").replace("–", "-")
    s = s.replace("×", "*").replace("÷", "/")
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"(\d)\(", r"\1*(", s)
    return s


def extended_numeric_value(text: str) -> float | None:
    """Parse option/answer strings including radicals and rationalized forms."""
    s = _normalize_expr(str(text))
    if not s:
        return None

    base = hma.numeric_value(s)
    if base is not None:
        return base

    m = _COEFF_SQRT_RE.match(s)
    if m:
        return int(m.group(1)) * math.sqrt(int(m.group(2)))

    m = _SQRT_FRAC_RE.match(s)
    if m:
        return math.sqrt(int(m.group(1))) / int(m.group(2))

    m = _INV_SQRT_RE.match(s)
    if m:
        return 1.0 / math.sqrt(int(m.group(1)))

    m = _NUM_INV_SQRT_RE.match(s)
    if m:
        return int(m.group(1)) / math.sqrt(int(m.group(2)))

    m = _SQRT_RE.match(s)
    if m:
        return math.sqrt(int(m.group(1)))

    if _INT_RE.fullmatch(s):
        return float(int(s))
    if _FRAC_RE.fullmatch(s):
        num, den = s.split("/", 1)
        try:
            return float(Fraction(int(num), int(den)))
        except ZeroDivisionError:
            return None

    # Parenthesized or compound numeric expressions, e.g. (5 - √10)/3
    if any(ch in s for ch in "+-*/^()√"):
        val = evaluate_numeric(s)
        if val is not None:
            return val

    return None


def _parse_number_token(tok: str) -> float | None:
    """Parse a single atomic token (no operators)."""
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
    m = _SQRT_RE.match(tok)
    if m:
        return math.sqrt(int(m.group(1)))
    m = _COEFF_SQRT_RE.match(tok)
    if m:
        return int(m.group(1)) * math.sqrt(int(m.group(2)))
    return hma.numeric_value(tok)


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
            # unary minus vs binary minus
            prev = tokens[-1].kind if tokens else ""
            if not tokens or prev in ("+", "-", "*", "/", "^", "("):
                tokens.append(_Tok("u-"))
            else:
                tokens.append(_Tok("-"))
            i += 1
            continue
        if ch == "√":
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            tokens.append(_Tok("num", s[i:j]))
            i = j
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


def _format_fraction(value: float) -> str | None:
    """Best-effort exact fraction string for small rationals."""
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


# ---------------------------------------------------------------------------
# Question pattern extraction
# ---------------------------------------------------------------------------

_EXTRACT_PATTERNS: list[re.Pattern[str]] = [
    re.compile(
        r"^(?:Compute|Evaluate|Simplify|Add|Multiply|Subtract|Divide|Rationalize):\s*(.+?)(?:\s*=\s*\?)?\.?\s*$",
        re.I,
    ),
    re.compile(r"^(?:Compute|Evaluate)\s+(.+?)(?:\.|$)", re.I),
    re.compile(r"^What is\s+(.+?)\??\s*$", re.I),
    re.compile(r"^What is the value of\s+(.+?)\??\s*$", re.I),
    re.compile(r"^Multiply\s+(.+?)\.?\s*$", re.I),
]

# Multi-part / non-numeric patterns we intentionally skip
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
    "lie between",
    "farthest",
    "farther",
    "distance",
    "centre of",
    "classify",
    "factor",
    "expand",
    "write ",
    "complete the",
    "represents",
    "satisfies",
    "cost of",
    "diagram",
    "locate the result among",
    "relative to 0",
    "starting at",
    "starting from",
    "move ",
    "moving ",
    "reach which",
    "end?",
    "land?",
    "exists in the gaps",
    "per the excerpt",
    "using integer positions",
    "using positions",
    "using conjugate",
    "check a number",
    "to place the result",
    "and identify",
    "and locate",
    "subtract like terms",
    "constant terms",
    "add the polynomials",
    "add exponents",
    "using exponent rules",
    "multiply the binomials",
    "evaluate p(",
)


def extract_expression(question: str) -> str | None:
    q = hmr.sanitize_grok_math_text(question).strip()
    ql = q.lower()
    if any(h in ql for h in _UNVERIFIABLE_HINTS):
        return None
    for pat in _EXTRACT_PATTERNS:
        m = pat.match(q)
        if m:
            expr = m.group(1).strip().rstrip(".")
            expr = re.sub(r"\s*=\s*\?$", "", expr).strip()
            if expr and not re.search(r"[a-zA-Z]", expr.replace("sqrt", "")):
                return expr
    return None


def compute_expected(question: str) -> float | None:
    expr = extract_expression(question)
    if not expr:
        return None
    return evaluate_numeric(expr)


def _options_equivalent(a: str, b: str) -> bool:
    if hma.answers_equivalent(a, b):
        return True
    va, vb = extended_numeric_value(a), extended_numeric_value(b)
    if va is not None and vb is not None:
        return abs(va - vb) <= 1e-9
    return False


def find_matching_option_index(expected: float, options: list[str]) -> int | None:
    for i, opt in enumerate(options):
        if _options_equivalent(str(opt), _value_repr(expected)):
            return i
        ov = extended_numeric_value(str(opt))
        if ov is not None and abs(ov - expected) <= 1e-9:
            return i
    return None


def _value_repr(value: float) -> str:
    frac = _format_fraction(value)
    return frac if frac is not None else str(value)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


@dataclass
class Issue:
    kind: str
    file: str
    qid: str
    level: str
    question: str
    detail: str
    fixable: bool = False
    fix_action: str = ""


@dataclass
class AuditResult:
    total: int = 0
    verified_ok: int = 0
    issues: list[Issue] = field(default_factory=list)
    fixes: list[dict[str, Any]] = field(default_factory=list)
    unverifiable: list[Issue] = field(default_factory=list)


def _check_structure(q: dict, path: str, level: str) -> list[Issue]:
    issues: list[Issue] = []
    qid = str(q.get("id", "?"))
    question = str(q.get("question", ""))
    opts = q.get("options")
    ans = q.get("answer")

    if not isinstance(opts, list) or len(opts) != 4:
        issues.append(
            Issue(
                "bad_structure",
                path,
                qid,
                level,
                question,
                f"expected 4 options, got {len(opts) if isinstance(opts, list) else type(opts).__name__}",
            )
        )
        return issues

    if not isinstance(ans, int) or ans not in range(4):
        issues.append(
            Issue(
                "bad_structure",
                path,
                qid,
                level,
                question,
                f"answer index out of range: {ans!r}",
            )
        )

    return issues


def _check_duplicate_options(q: dict, path: str, level: str) -> list[Issue]:
    issues: list[Issue] = []
    qid = str(q.get("id", "?"))
    question = str(q.get("question", ""))
    opts = [str(o) for o in q.get("options", [])]
    ans = q.get("answer")

    for i in range(len(opts)):
        for j in range(i + 1, len(opts)):
            if _options_equivalent(opts[i], opts[j]):
                both_correct = False
                expected = compute_expected(question)
                if expected is not None:
                    vi = extended_numeric_value(opts[i])
                    if vi is not None and abs(vi - expected) <= 1e-9:
                        both_correct = True
                issues.append(
                    Issue(
                        "duplicate_equiv_options",
                        path,
                        qid,
                        level,
                        question,
                        f"options[{i}]={opts[i]!r} ≈ options[{j}]={opts[j]!r}"
                        + (" (both match computed answer)" if both_correct else ""),
                        fixable=True,
                        fix_action="replace_duplicate_distractor",
                    )
                )
    return issues


def _check_wrong_key(q: dict, path: str, level: str) -> tuple[list[Issue], bool]:
    """Return (issues, was_verifiable)."""
    issues: list[Issue] = []
    qid = str(q.get("id", "?"))
    question = str(q.get("question", ""))
    opts = [str(o) for o in q.get("options", [])]
    ans = q.get("answer")

    if not isinstance(ans, int) or ans not in range(len(opts)):
        return issues, False

    expected = compute_expected(question)
    if expected is None:
        return issues, False

    keyed = opts[ans]
    keyed_val = extended_numeric_value(keyed)
    if keyed_val is not None and abs(keyed_val - expected) <= 1e-9:
        return issues, True

    match_idx = find_matching_option_index(expected, opts)
    if match_idx is not None and match_idx != ans:
        issues.append(
            Issue(
                "wrong_key",
                path,
                qid,
                level,
                question,
                f"keyed [{ans}]={keyed!r} (≈{keyed_val}), computed {_value_repr(expected)} "
                f"matches options[{match_idx}]={opts[match_idx]!r}",
                fixable=True,
                fix_action=f"rekey_to_{match_idx}",
            )
        )
        return issues, True

    if keyed_val is None or abs(keyed_val - expected) > 1e-9:
        issues.append(
            Issue(
                "wrong_key",
                path,
                qid,
                level,
                question,
                f"keyed [{ans}]={keyed!r} ≠ computed {_value_repr(expected)}; no matching option",
                fixable=True,
                fix_action="replace_keyed_option",
            )
        )
        return issues, True

    return issues, True


def audit_question(q: dict, path: str, level: str) -> tuple[list[Issue], bool, bool]:
    """Returns (issues, verifiable, ok)."""
    all_issues: list[Issue] = []
    all_issues.extend(_check_structure(q, path, level))
    if any(i.kind == "bad_structure" for i in all_issues):
        return all_issues, False, False

    all_issues.extend(_check_duplicate_options(q, path, level))
    wrong_issues, verifiable = _check_wrong_key(q, path, level)
    all_issues.extend(wrong_issues)

    ok = verifiable and not any(
        i.kind in ("wrong_key", "duplicate_equiv_options", "bad_structure") for i in all_issues
    )
    return all_issues, verifiable, ok


def load_all_banks() -> list[tuple[Path, dict]]:
    banks: list[tuple[Path, dict]] = []
    for path in sorted(BANK_DIR.rglob("topic_*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"WARN: cannot read {path}: {exc}", file=sys.stderr)
            continue
        banks.append((path, data))
    return banks


def _next_wrong_distractor(expected: float, existing: set[str]) -> str | None:
    """Generate a numeric distractor not equivalent to existing options."""
    candidates: list[str] = []
    for delta_num in (1, 2, 3, -1, -2, -3, 4, -4):
        v = expected + delta_num
        for rep in (_value_repr(v), str(int(v)) if v == int(v) else None):
            if not rep or rep in existing:
                continue
            if _options_equivalent(rep, _value_repr(expected) or ""):
                continue
            if any(_options_equivalent(rep, ex) for ex in existing):
                continue
            if "." in rep and "/" not in rep and "√" not in rep:
                continue
            candidates.append(rep)
    return candidates[0] if candidates else None


def _fallback_distractor(existing: set[str]) -> str:
    for fb in ("1/2", "1/3", "2/3", "3/4", "5/6", "7/8", "√2", "2√2", "3/4", "5/4"):
        if not any(_options_equivalent(fb, ex) for ex in existing):
            return fb
    return "1/7"


def _best_answer_repr(expected: float, question: str) -> str:
    """Pick a readable answer form (fraction or coeff√radicand when exact)."""
    best: tuple[int, int] | None = None
    for n in range(1, 25):
        for m in range(2, 200):
            if abs(n * math.sqrt(m) - expected) <= 1e-9:
                if best is None:
                    best = (n, m)
                elif n > 1 and best[0] == 1:
                    best = (n, m)
                elif n == best[0] and m < best[1]:
                    best = (n, m)
    if best:
        n, m = best
        return f"{n}√{m}" if n > 1 else f"√{m}"
    frac = _format_fraction(expected)
    if frac is not None:
        return frac
    if expected == int(expected):
        return str(int(expected))
    return None  # avoid ugly decimal replacements


_CONFIDENT_WRONG_KEY_PREFIXES = (
    "compute:",
    "evaluate:",
    "simplify:",
    "add:",
    "multiply:",
    "subtract:",
    "divide:",
    "what is ",
)


def _confident_wrong_key(question: str, issue: Issue) -> bool:
    if issue.fix_action.startswith("rekey_to_"):
        return True
    ql = question.strip().lower()
    if not any(ql.startswith(p) for p in _CONFIDENT_WRONG_KEY_PREFIXES):
        return False
    if "rationalize" in ql:
        return False
    return issue.fix_action == "replace_keyed_option"


def apply_fix(q: dict, issue: Issue) -> dict | None:
    """Apply a single fix; return change record or None."""
    opts = [str(o) for o in q.get("options", [])]
    ans = q.get("answer")
    question = str(q.get("question", ""))
    expected = compute_expected(question)

    if issue.kind == "wrong_key" and issue.fixable and issue.fix_action.startswith("rekey_to_"):
        new_idx = int(issue.fix_action.rsplit("_", 1)[-1])
        old = ans
        q["answer"] = new_idx
        return {"field": "answer", "old": old, "new": new_idx}

    if (
        issue.kind == "wrong_key"
        and issue.fixable
        and issue.fix_action == "replace_keyed_option"
        and expected is not None
        and isinstance(ans, int)
        and 0 <= ans < len(opts)
    ):
        new_opt = _best_answer_repr(expected, question)
        if not new_opt:
            return None
        old_opt = opts[ans]
        opts[ans] = new_opt
        q["options"] = opts
        return {"field": f"options[{ans}]", "old": old_opt, "new": new_opt}

    if issue.kind == "duplicate_equiv_options":
        m = re.search(r"options\[(\d+)\].*options\[(\d+)\]", issue.detail)
        if not m:
            return None
        i, j = int(m.group(1)), int(m.group(2))
        if isinstance(ans, int) and ans in (i, j):
            replace_idx = j if ans == i else i
        else:
            replace_idx = max(i, j)
        existing = {str(o) for k, o in enumerate(opts) if k != replace_idx}
        ref_val = expected
        if ref_val is None:
            ref_val = extended_numeric_value(opts[i]) or extended_numeric_value(opts[j])
        if ref_val is None:
            ref_val = float(i + j + 1)
        new_opt = _next_wrong_distractor(ref_val, existing)
        if not new_opt:
            new_opt = _fallback_distractor(existing)
        old_opt = opts[replace_idx]
        if _options_equivalent(old_opt, new_opt):
            return None
        opts[replace_idx] = new_opt
        q["options"] = opts
        return {"field": f"options[{replace_idx}]", "old": old_opt, "new": new_opt}

    return None


def run_audit(*, fix: bool = False) -> AuditResult:
    result = AuditResult()
    banks = load_all_banks()

    for path, data in banks:
        rel = path.relative_to(ROOT).as_posix()
        questions = data.get("questions", {})
        if not isinstance(questions, dict):
            continue
        file_changed = False

        for level, bucket in questions.items():
            if not isinstance(bucket, list):
                continue
            for q in bucket:
                if not isinstance(q, dict):
                    continue
                result.total += 1
                issues, verifiable, ok = audit_question(q, rel, str(level))

                if not verifiable and not issues:
                    result.unverifiable.append(
                        Issue(
                            "unverifiable",
                            rel,
                            str(q.get("id", "?")),
                            str(level),
                            str(q.get("question", "")),
                            "no numeric evaluator matched",
                        )
                    )
                elif ok:
                    result.verified_ok += 1

                fixable_issues = [i for i in issues if i.fixable]
                seen_fix_keys: set[str] = set()

                for issue in issues:
                    if issue.kind == "unverifiable":
                        result.unverifiable.append(issue)
                    else:
                        result.issues.append(issue)

                if fix:
                    # Prefer rekey before replacing options; one fix per issue kind per question.
                    for issue in sorted(
                        fixable_issues,
                        key=lambda i: (0 if i.fix_action.startswith("rekey") else 1, i.kind),
                    ):
                        if issue.kind == "wrong_key" and not _confident_wrong_key(
                            str(q.get("question", "")), issue
                        ):
                            continue
                        fix_key = f"{issue.kind}:{issue.fix_action}:{issue.detail[:40]}"
                        if fix_key in seen_fix_keys:
                            continue
                        change = apply_fix(q, issue)
                        if change:
                            seen_fix_keys.add(fix_key)
                            file_changed = True
                            result.fixes.append(
                                {
                                    "file": rel,
                                    "id": q.get("id"),
                                    "level": level,
                                    "issue": issue.kind,
                                    "detail": issue.detail,
                                    **change,
                                }
                            )

        if fix and file_changed:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return result


def _print_report(result: AuditResult, *, fix: bool, total_fixes: int = 0) -> None:
    print("=" * 72)
    print("HARSHIT MATH QUESTION BANK AUDIT")
    print("=" * 72)
    print(f"Total questions:        {result.total}")
    print(f"Verified OK:              {result.verified_ok}")
    print(f"Unverifiable:             {len(result.unverifiable)}")
    print(f"Issues found:             {len(result.issues)}")
    if fix:
        print(f"Fixes applied:            {total_fixes}")
    print()

    by_kind: dict[str, list[Issue]] = {}
    for issue in result.issues:
        by_kind.setdefault(issue.kind, []).append(issue)

    for kind in ("bad_structure", "wrong_key", "duplicate_equiv_options"):
        items = by_kind.get(kind, [])
        if not items:
            continue
        print(f"--- {kind.upper()} ({len(items)}) ---")
        for it in items:
            print(f"  [{it.file}] {it.qid} ({it.level})")
            print(f"    Q: {it.question[:100]}{'…' if len(it.question) > 100 else ''}")
            print(f"    {it.detail}")
            if it.fixable:
                print(f"    fixable: {it.fix_action or 'yes'}")
        print()

    needs_manual = [
        i
        for i in result.issues
        if not i.fixable or (i.kind == "wrong_key" and "no matching option" in i.detail)
    ]
    print(f"Needs manual review:      {len(needs_manual) + len(result.unverifiable)}")
    print(f"  structural/unfixable:   {len(needs_manual)}")
    print(f"  unverifiable:           {len(result.unverifiable)}")

    if result.fixes:
        print()
        print(f"--- FIXES APPLIED ({len(result.fixes)}) ---")
        for fx in result.fixes:
            print(
                f"  [{fx['file']}] {fx['id']} ({fx['level']}): "
                f"{fx['issue']} — {fx.get('field')} {fx.get('old')!r} → {fx.get('new')!r}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Harshit Math question banks")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply confident fixes (wrong_key re-key, duplicate distractor replacement)",
    )
    args = parser.parse_args()

    total_fixes = 0
    if args.fix:
        while True:
            pass_result = run_audit(fix=True)
            n = len(pass_result.fixes)
            total_fixes += n
            if n == 0:
                break
        result = run_audit(fix=False)
        result.fixes_count = total_fixes  # type: ignore[attr-defined]
    else:
        result = run_audit(fix=False)

    _print_report(result, fix=args.fix, total_fixes=total_fixes if args.fix else 0)


if __name__ == "__main__":
    main()
