#!/usr/bin/env python3
"""Repair Class 10 Unit 3 (Pair of Linear Equations) question banks."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT03_DIR = ROOT / "HarshitMath" / "class10" / "question_banks" / "unit_03"

_ALT_SUFFIX = re.compile(r"\s*\(alt\)\s*$", re.I)
_ALT_NUM_SUFFIX = re.compile(r"\s*\(alt\s*\d+\)\s*$", re.I)
_LINES_A = re.compile(
    r"^Lines (.+?) and (.+?)(?: \(different slopes\))? are:\s*$",
    re.I,
)
_X_SUM_DIFF = re.compile(
    r"^x \+ y = (\d+) and x [-−] y = (-?\d+)\. x equals\?\s*$",
)
_TRAIN = re.compile(r"^A train covers (\d+) km in (\d+) hours\. Speed = \? km/h\s*$", re.I)
_AGE_DIFF = re.compile(
    r"^Father is (\d+)× son's age; in (\d+) years he will be (\d+)× son's age\. Age difference now\?\s*$",
    re.I,
)
_AGE_SOLVE = re.compile(
    r"^Father is (\d+)× son's age; in (\d+) years he will be (\d+)× son's age\. "
    r"Step 2 — present ages are:\s*$",
    re.I,
)
_AGE_SETUP = re.compile(
    r"^Father is (\d+) times son's age\. In (\d+) years he will be (\d+) times son's age\. "
    r"Step 1 — form the equations \(x = son, y = father\):\s*$",
    re.I,
)
_AMBIG_B = (
    "a pair of linear equations can have:",
    "a pair of linear equations in two variables can have:",
    "which is a possible outcome for a pair of linear equations?",
    "solutions of a pair of linear equations:",
)


def _det_int(seed: str, lo: int, hi: int) -> int:
    h = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
    return lo + h % (hi - lo + 1)


def _strip_alt(text: str) -> str:
    s = _ALT_SUFFIX.sub("", str(text).strip())
    return _ALT_NUM_SUFFIX.sub("", s).strip()


def _norm_option(text: str) -> str:
    return _strip_alt(text).strip().lower()


def _wrong_distractor(correct: str, used: set[str], seed: str) -> str:
    """Numeric or 'N years' distractor distinct from correct and used set."""
    base = _strip_alt(correct)
    used_norm = {_norm_option(u) for u in used}
    m = re.match(r"^(-?\d+)\s*years?\s*$", base, re.I)
    if m:
        v = int(m.group(1))
        for delta in (3, 5, 7, 9, 11, 2, 4):
            cand = f"{v + delta} years"
            if _norm_option(cand) not in used_norm and _norm_option(cand) != _norm_option(correct):
                return cand
    m = re.match(r"^(-?\d+)$", base.strip())
    if m:
        v = int(m.group(1))
        for delta in (1, 2, 3, 4, 5):
            for cand in (str(v + delta), str(v - delta)):
                if _norm_option(cand) not in used_norm and _norm_option(cand) != _norm_option(correct):
                    return cand
    n = _det_int(seed, 2, 50)
    cand = str(n)
    if _norm_option(cand) not in used_norm:
        return cand
    return str(n + 17)


def _parse_lin_eq(eq: str) -> tuple[int, int, int]:
    eq = eq.strip().replace("−", "-")
    lhs, rhs = eq.split("=", 1)
    c = int(rhs.strip())
    a = b = 0
    lhs = lhs.strip()
    if not lhs:
        return a, b, c
    if lhs[0] not in "+-":
        lhs = "+" + lhs
    for term in re.findall(r"[+-][^+-]+", lhs):
        body = term[1:].strip().replace(" ", "")
        sign = -1 if term[0] == "-" else 1
        if "x" in body:
            coef = body.replace("x", "") or "1"
            a = sign * int(coef)
        elif "y" in body:
            coef = body.replace("y", "") or "1"
            b = sign * int(coef)
    return a, b, c


def _line_pair_label(a1: int, b1: int, c1: int, a2: int, b2: int, c2: int) -> str:
    det = a1 * b2 - a2 * b1
    if det != 0:
        return "Intersecting"
    if a1 * c2 == a2 * c1 and b1 * c2 == b2 * c1:
        return "Coincident"
    return "Parallel"


def _shuffle_opts(correct: str, wrong: list[str], seed: str) -> tuple[list[str], int]:
    correct = _strip_alt(correct)
    seen = {_norm_option(correct)}
    distractors: list[str] = []
    used: set[str] = {correct}
    for w in wrong:
        w = _strip_alt(str(w))
        key = _norm_option(w)
        if key in seen:
            continue
        distractors.append(w)
        seen.add(key)
        used.add(w)
        if len(distractors) >= 3:
            break
    while len(distractors) < 3:
        filler = _wrong_distractor(correct, used, f"{seed}-f{len(distractors)}")
        distractors.append(filler)
        seen.add(_norm_option(filler))
        used.add(filler)
    opts = [correct] + distractors[:3]
    shift = _det_int(seed, 0, 3)
    for _ in range(shift):
        opts = [opts[-1]] + opts[:-1]
    return opts, opts.index(correct)


def _fix_equivalent_options(q: dict) -> bool:
    raw = [str(o) for o in q.get("options", [])]
    if len(raw) != 4:
        return False
    ans = q.get("answer")
    if not isinstance(ans, int) or not (0 <= ans < 4):
        return False
    opts = [_strip_alt(o) for o in raw]
    correct_norm = _norm_option(opts[ans])
    changed = opts != raw
    seen_norm: set[str] = set()
    for i in range(4):
        n = _norm_option(opts[i])
        if i == ans:
            seen_norm.add(correct_norm)
            continue
        if n == correct_norm or n in seen_norm:
            used = {opts[j] for j in range(4) if j != i}
            opts[i] = _wrong_distractor(opts[ans], used, f"{q.get('id', '')}-{i}")
            changed = True
            n = _norm_option(opts[i])
        seen_norm.add(n)
    if changed:
        q["options"] = opts
    return changed


def _fix_cross_mult_stem(q: dict) -> bool:
    qu = str(q.get("question", ""))
    if "Cross-multiplication formula" not in qu or "a₂x" in qu:
        return False
    q["question"] = "Cross-multiplication formula for a₁x + b₁y = c₁ and a₂x + b₂y = c₂:"
    if not str(q.get("explanation", "")).strip():
        q["explanation"] = (
            "Cramer / cross-multiplication: x = (c₁b₂ − c₂b₁)/Δ, y = (a₁c₂ − a₂c₁)/Δ, Δ = a₁b₂ − a₂b₁."
        )
    return True


def _fix_lines_level_a(q: dict) -> bool:
    m = _LINES_A.match(str(q.get("question", "")).strip())
    if not m:
        return False
    a1, b1, c1 = _parse_lin_eq(m.group(1))
    a2, b2, c2 = _parse_lin_eq(m.group(2))
    correct = _line_pair_label(a1, b1, c1, a2, b2, c2)
    q["question"] = f"Lines {m.group(1).strip()} and {m.group(2).strip()} are:"
    wrong = [x for x in ["Intersecting", "Parallel", "Coincident", "Vertical only"] if x != correct]
    opts, ans = _shuffle_opts(correct, wrong, str(q.get("id", "")))
    q["options"] = opts
    q["answer"] = ans
    return True


def _fix_subst_x_level_a(q: dict) -> bool:
    m = _X_SUM_DIFF.match(str(q.get("question", "")).strip())
    if not m:
        return False
    s_sum, s_diff = int(m.group(1)), int(m.group(2))
    x = (s_sum + s_diff) // 2
    if (s_sum + s_diff) % 2 != 0:
        return False
    correct = str(x)
    opts, ans = _shuffle_opts(
        correct,
        [str(x + 1), str(max(0, x - 1)), str(s_sum)],
        str(q.get("id", "")) + "x",
    )
    q["options"] = opts
    q["answer"] = ans
    return True


def _valid_age_params(mult: int, future: int, years: int) -> tuple[int, int] | None:
    """Present ages (son, father) for y=mult*x and y+years=future*(x+years)."""
    if future >= mult or future < 1:
        return None
    # mult*x + years = future*x + future*years => x*(mult-future) = years*(future-1)
    num = years * (future - 1)
    den = mult - future
    if den == 0 or num % den != 0:
        return None
    son = num // den
    if son <= 0:
        return None
    father = mult * son
    return son, father


def _normalize_age_problem(q: dict, mult: int, years: int, future: int) -> tuple[int, int, int, int]:
    """Return mult, years, future, son using 3→2 template when invalid."""
    params = _valid_age_params(mult, future, years)
    if params:
        return mult, years, future, params[0]
    qid = str(q.get("id", ""))
    years = _det_int(qid + "y", 6, 18)
    return 3, years, 2, years


def _fix_age_diff(q: dict) -> bool:
    m = _AGE_DIFF.match(str(q.get("question", "")).strip())
    if not m:
        return False
    mult, years, future = int(m.group(1)), int(m.group(2)), int(m.group(3))
    mult, years, future, son = _normalize_age_problem(q, mult, years, future)
    diff = mult * son - son
    correct = f"{diff} years"
    q["question"] = (
        f"Father is {mult}× son's age; in {years} years he will be {future}× son's age. "
        f"Age difference now?"
    )
    opts, ans = _shuffle_opts(
        correct,
        [f"{years} years", f"{diff + years} years", f"{mult * son} years"],
        str(q.get("id", "")),
    )
    q["options"] = opts
    q["answer"] = ans
    q["explanation"] = (
        f"3x + {years} = {future}(x + {years}) ⇒ x = {son}; difference = {diff}."
        if mult == 3 and future == 2
        else f"y = {mult}x; y + {years} = {future}(x + {years}) ⇒ son = {son}, difference = {diff}."
    )
    return True


def _fix_age_solve(q: dict) -> bool:
    m = _AGE_SOLVE.match(str(q.get("question", "")).strip())
    if not m:
        return False
    mult, years, future = int(m.group(1)), int(m.group(2)), int(m.group(3))
    mult, years, future, son = _normalize_age_problem(q, mult, years, future)
    father = mult * son
    correct = f"Son = {son}, Father = {father}"
    q["question"] = (
        f"Father is {mult}× son's age; in {years} years he will be {future}× son's age. "
        f"Step 2 — present ages are:"
    )
    opts, ans = _shuffle_opts(
        correct,
        [
            f"Son = {son + years}, Father = {father + years}",
            f"Son = {father}, Father = {son}",
            f"Son = {son + 1}, Father = {father}",
        ],
        str(q.get("id", "")),
    )
    q["options"] = opts
    q["answer"] = ans
    q["explanation"] = (
        f"From y = {mult}x and y + {years} = {future}(x + {years}), x = {son}, y = {father}."
    )
    return True


def _fix_age_setup(q: dict) -> bool:
    m = _AGE_SETUP.match(str(q.get("question", "")).strip())
    if not m:
        return False
    mult, years, future = int(m.group(1)), int(m.group(2)), int(m.group(3))
    mult, years, future, _ = _normalize_age_problem(q, mult, years, future)
    correct = f"y = {mult}x; y + {years} = {future}(x + {years})"
    q["question"] = (
        f"Father is {mult} times son's age. In {years} years he will be "
        f"{future} times son's age. Step 1 — form the equations (x = son, y = father):"
    )
    opts, ans = _shuffle_opts(
        correct,
        [
            f"x = {mult}y; x + {years} = {future}(y + {years})",
            f"y = {mult}x; y = {future}x",
            f"x + y = {years}; y − x = {mult}",
        ],
        str(q.get("id", "")),
    )
    q["options"] = opts
    q["answer"] = ans
    return True


def _fix_train_speed(q: dict) -> bool:
    m = _TRAIN.match(str(q.get("question", "")).strip())
    if not m:
        return False
    d, t = int(m.group(1)), int(m.group(2))
    if t <= 0:
        return False
    speed = round(d / t)
    correct = str(speed)
    opts, ans = _shuffle_opts(
        correct,
        [str(speed + 10), str(max(1, speed - 5)), str(speed + 1)],
        str(q.get("id", "")),
    )
    q["options"] = [_strip_alt(o) for o in opts]
    q["answer"] = ans
    q["explanation"] = f"Speed = distance/time = {d}/{t} ≈ {speed} km/h (nearest whole number)."
    return True


def _fix_ambiguous_level_b(q: dict) -> bool:
    ql = str(q.get("question", "")).strip().lower()
    if not any(p in ql for p in _AMBIG_B):
        return False
    scenarios = [
        (
            "A pair of linear equations representing parallel distinct lines has:",
            "No solution",
            ["Exactly one solution", "Infinitely many solutions", "Exactly two solutions"],
        ),
        (
            "A pair of linear equations with intersecting lines has:",
            "Exactly one solution",
            ["No solution", "Infinitely many solutions", "Exactly two solutions"],
        ),
        (
            "A pair of linear equations representing coincident lines has:",
            "Infinitely many solutions",
            ["No solution", "Exactly one solution", "Exactly two solutions"],
        ),
    ]
    idx = _det_int(str(q.get("id", "")), 0, len(scenarios) - 1)
    qtext, correct, wrong = scenarios[idx]
    opts, ans = _shuffle_opts(correct, wrong, str(q.get("id", "")) + "b")
    q["question"] = qtext
    q["options"] = opts
    q["answer"] = ans
    return True


def _normalize_options(q: dict) -> None:
    opts = q.get("options")
    if isinstance(opts, list):
        q["options"] = [_strip_alt(o) for o in opts]


def repair_file(path: Path) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    stats = {k: 0 for k in ("lines_a", "subst_a", "age", "train", "ambig_b", "alt", "dedupe", "cross")}
    questions = data.get("questions", {})
    if not isinstance(questions, dict):
        return stats

    for bucket in questions.values():
        if not isinstance(bucket, list):
            continue
        for q in bucket:
            if not isinstance(q, dict):
                continue
            before = json.dumps(q.get("options", []))
            _normalize_options(q)
            if before != json.dumps(q.get("options", [])):
                stats["alt"] += 1
            if _fix_lines_level_a(q):
                stats["lines_a"] += 1
            if _fix_subst_x_level_a(q):
                stats["subst_a"] += 1
            if _fix_age_diff(q) or _fix_age_solve(q) or _fix_age_setup(q):
                stats["age"] += 1
            if _fix_train_speed(q):
                stats["train"] += 1
            if _fix_ambiguous_level_b(q):
                stats["ambig_b"] += 1
            if _fix_equivalent_options(q):
                stats["dedupe"] += 1
            if _fix_cross_mult_stem(q):
                stats["cross"] += 1

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return stats


def main() -> int:
    if not UNIT03_DIR.is_dir():
        print(f"Missing {UNIT03_DIR}", file=sys.stderr)
        return 1
    totals = {k: 0 for k in ("lines_a", "subst_a", "age", "train", "ambig_b", "alt", "dedupe", "cross")}
    for path in sorted(UNIT03_DIR.glob("topic_*.json")):
        stats = repair_file(path)
        for k in totals:
            totals[k] += stats[k]
        print(f"{path.name}: {stats}")
    print("Totals:", totals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
