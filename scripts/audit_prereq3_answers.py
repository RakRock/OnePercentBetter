#!/usr/bin/env python3
"""Audit PreReq 3 question banks — verify marked answers where computable."""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_DIR = ROOT / "HarshitMath" / "question_banks" / "prereq_03"

ROMAN_QUAD = {"I": 1, "II": 2, "III": 3, "IV": 4}
WORD_QUAD = {
    "first": 1, "second": 2, "third": 3, "fourth": 4,
    "quadrant i": 1, "quadrant ii": 2, "quadrant iii": 3, "quadrant iv": 4,
}


def _parse_coord(text: str) -> tuple[int, int] | None:
    m = re.search(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", text)
    return (int(m.group(1)), int(m.group(2))) if m else None


def _quad_num(x: int, y: int) -> int:
    if x > 0 and y > 0:
        return 1
    if x < 0 and y > 0:
        return 2
    if x < 0 and y < 0:
        return 3
    return 4


def _quad_label(n: int, style: str = "roman") -> str:
    if style == "word":
        return {1: "First", 2: "Second", 3: "Third", 4: "Fourth"}[n]
    return {1: "I", 2: "II", 3: "III", 4: "IV"}[n]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s).strip().lower())


def _norm_eq(eq: str) -> str:
    s = _norm(eq).replace("−", "-")
    s = re.sub(r"y\s*=\s*1x", "y = x", s)
    s = re.sub(r"\+\s*-", "- ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def _eq_match(expected: str, options: list[str]) -> int | None:
    exp = _norm_eq(expected)
    alts = {exp}
    m = re.match(r"y = (-?\d+)x \+ (-?\d+)", exp)
    if m:
        a, b = m.group(1), int(m.group(2))
        alts.add(_norm_eq(f"y = {a}x + {b}"))
        if b < 0:
            alts.add(_norm_eq(f"y = {a}x - {abs(b)}"))
        if b == 0:
            alts.add(_norm_eq(f"y = {a}x"))
            alts.add(_norm_eq(f"y = {a}x + 0"))
    m2 = re.match(r"y = (-?\d+)x$", exp)
    if m2:
        alts.add(_norm_eq(f"y = {m2.group(1)}x + 0"))
    for i, o in enumerate(options):
        if _norm_eq(o) in alts:
            return i
    return None


def _parse_line_from_text(text: str) -> tuple[float, float] | None:
    m = re.search(r"y\s*=\s*(-?\d+|1/2|\d+/\d+)x(?:\s*\+\s*(-?\d+))?", text, re.I)
    if not m:
        m = re.search(r"y\s*=\s*x(?:\s*\+\s*(-?\d+))?", text, re.I)
        if m:
            return 1.0, float(m.group(1) or 0)
        return None
    slope_raw = m.group(1)
    slope = float(Fraction(slope_raw)) if "/" in slope_raw else float(slope_raw)
    intercept = float(m.group(2) or 0)
    return slope, intercept


def _point_on_line_option(opts: list[str], slope: float, intercept: float = 0) -> int | None:
    for i, o in enumerate(opts):
        pt = _parse_coord(o)
        if pt and abs(pt[1] - (slope * pt[0] + intercept)) < 1e-6:
            return i
    return None


def _opt_match(expected: str, options: list[str]) -> int | None:
    exp = _norm(expected)
    for i, o in enumerate(options):
        if _norm(o) == exp:
            return i
    return None


def _marked(q: dict) -> str:
    opts = q.get("options", [])
    ans = int(q.get("answer", 0))
    return str(opts[ans]) if 0 <= ans < len(opts) else "?"


def _try_verify(q: dict) -> tuple[str, str | None]:
    """Return (status, expected_answer_text). status: ok|wrong|skip|bad"""
    text = str(q.get("question", ""))
    lower = text.lower()
    opts = [str(o) for o in q.get("options", [])]
    ans_idx = int(q.get("answer", 0))
    marked = _marked(q)

    # Trivial / invalid: coordinates in question match an option exactly
    if re.search(r"which point lies at|what point is at", lower):
        pt = _parse_coord(text)
        if pt and any(_norm(o) == _norm(f"({pt[0]}, {pt[1]})") for o in opts):
            return "bad", None

    # Quadrant from point (x, y)
    pt = _parse_coord(text)
    if pt and re.search(r"which quadrant|lies in which quadrant|belongs to which quadrant|lie in quadrant\?", lower):
        if pt[0] != 0 and pt[1] != 0:
            qn = _quad_num(*pt)
            for style in ("roman", "word"):
                expected = _quad_label(qn, style)
                idx = _opt_match(expected, opts)
                if idx is not None:
                    return ("ok" if idx == ans_idx else "wrong"), expected
            for i, o in enumerate(opts):
                ol = _norm(o)
                if str(qn) in ol or _quad_label(qn, "roman").lower() in ol or _quad_label(qn, "word").lower() in ol:
                    return ("ok" if i == ans_idx else "wrong"), o

    # Distance from nearer axis (Quadrant I)
    m = re.search(r"point\s*\(\s*(\d+)\s*,\s*(\d+)\s*\).*distance from the nearer axis", lower)
    if m:
        x, y = int(m.group(1)), int(m.group(2))
        expected = str(min(x, y))
        idx = _opt_match(expected, opts)
        if idx is not None:
            return ("ok" if idx == ans_idx else "wrong"), expected
    if "positive x-coordinate and positive y-coordinate" in lower:
        return _check_expected(_quad_label(1, _opt_style(opts)), opts, ans_idx)
    if "negative x-coordinate and positive y-coordinate" in lower:
        return _check_expected(_quad_label(2, _opt_style(opts)), opts, ans_idx)
    if "negative x-coordinate and negative y-coordinate" in lower:
        return _check_expected(_quad_label(3, _opt_style(opts)), opts, ans_idx)
    if "positive x-coordinate and negative y-coordinate" in lower:
        return _check_expected(_quad_label(4, _opt_style(opts)), opts, ans_idx)

    # Midpoint
    m = re.search(
        r"midpoint of\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*and\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)",
        text,
        re.I,
    )
    if m:
        x1, y1, x2, y2 = map(int, m.groups())
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        expected = f"({mx:g}, {my:g})"
        idx = _opt_match(expected, opts)
        if idx is not None:
            return ("ok" if idx == ans_idx else "wrong"), expected

    # x-coordinate from y-axis distance
    m = re.search(r"perpendicular distance from the y-axis.*is\s*(\d+)\s*units.*x-coordinate", lower)
    if m:
        expected = m.group(1)
        idx = _opt_match(expected, opts)
        if idx is not None:
            return ("ok" if idx == ans_idx else "wrong"), expected

    # y = mx + c
    m = re.search(r"slope\s*(-?\d+)\s*and y-intercept\s*(-?\d+)", lower)
    if m:
        slope, intercept = int(m.group(1)), int(m.group(2))
        expected = f"y = {slope}x + {intercept}"
        idx = _eq_match(expected, opts)
        if idx is not None:
            return ("ok" if idx == ans_idx else "wrong"), expected

    # origin slope m -> y = mx
    m = re.search(r"(?:through the origin|passes through the origin).*slope\s*(-?\d+)", lower)
    if not m:
        m = re.search(r"origin with slope\s*(-?\d+)", lower)
    if m:
        slope = m.group(1)
        expected = f"y = {slope}x"
        idx = _eq_match(expected, opts)
        if idx is not None:
            return ("ok" if idx == ans_idx else "wrong"), expected

    # Which point lies on line y = mx (+ c)?
    if "lies on the line" in lower or "lies on which line" in lower or "which point satisfies" in lower:
        parsed = _parse_line_from_text(text)
        if parsed:
            m_val, c_val = parsed
            idx = _point_on_line_option(opts, m_val, c_val)
            if idx is not None:
                return ("ok" if idx == ans_idx else "wrong"), opts[idx]

    # vertical x = k
    m = re.search(r"vertical line through x\s*=\s*(-?\d+)", lower)
    if m:
        expected = f"x = {m.group(1)}"
        idx = _opt_match(expected, opts)
        if idx is not None:
            return ("ok" if idx == ans_idx else "wrong"), expected

    # horizontal y = k
    m = re.search(r"horizontal line through y\s*=\s*(-?\d+)", lower)
    if m:
        expected = f"y = {m.group(1)}"
        idx = _opt_match(expected, opts)
        if idx is not None:
            return ("ok" if idx == ans_idx else "wrong"), expected

    # slope through two points
    m = re.search(
        r"through\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*and\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)",
        text,
        re.I,
    )
    if m and "slope" in lower:
        x1, y1, x2, y2 = map(int, m.groups())
        if x2 != x1:
            slope = Fraction(y2 - y1, x2 - x1)
            expected = str(slope) if slope.denominator != 1 else str(slope.numerator)
            for i, o in enumerate(opts):
                try:
                    if Fraction(str(o).strip()) == slope:
                        return ("ok" if i == ans_idx else "wrong"), expected
                except (ValueError, ZeroDivisionError):
                    if _norm(o) == _norm(expected):
                        return ("ok" if i == ans_idx else "wrong"), expected

    # y = mx find y when x = n
    m = re.search(r"y\s*=\s*(-?\d+)x(?:\s*\+\s*(-?\d+))?\b.*x\s*=\s*(-?\d+)", lower)
    if m and "find y" in lower or (m and "what is the y" in lower):
        slope = int(m.group(1))
        intercept = int(m.group(2) or 0)
        x = int(m.group(3))
        expected = str(slope * x + intercept)
        idx = _opt_match(expected, opts)
        if idx is not None:
            return ("ok" if idx == ans_idx else "wrong"), expected

    # simpler: For y = 4x with c = 0, find y when x = 2
    m = re.search(r"y\s*=\s*(\d+)x.*x\s*=\s*(\d+)", lower)
    if m and ("find y" in lower or "y value" in lower or "y-coordinate" in lower):
        expected = str(int(m.group(1)) * int(m.group(2)))
        idx = _opt_match(expected, opts)
        if idx is not None:
            return ("ok" if idx == ans_idx else "wrong"), expected

    # diameter = 2r
    m = re.search(r"radius\s*(\d+)", lower)
    if m and "diameter" in lower:
        expected = str(2 * int(m.group(1)))
        idx = _opt_match(expected, opts)
        if idx is not None:
            return ("ok" if idx == ans_idx else "wrong"), expected

    return "skip", None


def _opt_style(opts: list[str]) -> str:
    for o in opts:
        if _norm(o) in WORD_QUAD:
            return "word"
    return "roman"


def _check_expected(expected: str, opts: list[str], ans_idx: int) -> tuple[str, str | None]:
    idx = _opt_match(expected, opts)
    if idx is None:
        return "skip", None
    return ("ok" if idx == ans_idx else "wrong"), expected


def load_questions() -> list[dict]:
    out: list[dict] = []
    for path in sorted(BANK_DIR.glob("topic_*.json")):
        topic = int(path.stem.split("_")[1])
        data = json.loads(path.read_text())
        for level, bucket in data.get("questions", {}).items():
            if not isinstance(bucket, list):
                continue
            for q in bucket:
                out.append({**q, "topic": q.get("topic", topic), "level": q.get("level", level), "_file": path.name})
    return out


def main() -> int:
    questions = load_questions()
    counts = {"ok": 0, "wrong": 0, "skip": 0, "bad": 0}
    wrong: list[dict] = []
    bad: list[dict] = []

    for q in questions:
        status, expected = _try_verify(q)
        counts[status] += 1
        if status == "wrong":
            wrong.append({**q, "expected": expected, "marked": _marked(q)})
        if status == "bad":
            bad.append(q)

    print(f"Total questions: {len(questions)}")
    print(f"Verified OK: {counts['ok']} | Wrong: {counts['wrong']} | Bad/trivial: {counts['bad']} | Skipped (manual): {counts['skip']}")
    if bad:
        print("\n=== BAD / TRIVIAL ===")
        for q in bad[:20]:
            print(f"  [{q['_file']} {q.get('id')}] {q['question'][:90]}")
    if wrong:
        print("\n=== WRONG ANSWERS ===")
        for q in wrong[:40]:
            print(f"  [{q['_file']} {q.get('id')}]")
            print(f"    Q: {q['question'][:100]}")
            print(f"    Marked: {q['marked']} | Expected: {q['expected']}")
    return 1 if wrong or bad else 0


if __name__ == "__main__":
    sys.exit(main())
