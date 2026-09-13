#!/usr/bin/env python3
"""Repair Class 10 Unit 4 (Quadratic Equations) question banks."""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT04_DIR = ROOT / "HarshitMath" / "class10" / "question_banks" / "unit_04"

_ALT_SUFFIX = re.compile(r"\s*\(alt\)\s*$", re.I)
_EQUAL_ROOTS = re.compile(r"x²\s*\+\s*kx\s*\+\s*(\d+)", re.I)
_NO_REAL_FIXED = re.compile(
    r"^x²\s*\+\s*(\d*)x\s*\+\s*(\d+)\s*=\s*0 has no real roots because:\s*$",
    re.I,
)
_RECT = re.compile(
    r"A rectangle has length (\d+) m more than width\. Area = (\d+) m²\. Width = \?",
    re.I,
)
_ALT_NUM_SUFFIX = re.compile(r"\s*\(alt\s*\d+\)\s*$", re.I)

_NATURE_OPTIONS = [
    "Two distinct real roots",
    "Two equal real roots",
    "No real roots",
    "Always real roots",
]


def _normalize_factor_text(text: str) -> str:
    s = str(text)
    s = re.sub(r"\+\s*-", "- ", s)
    s = re.sub(r"-\s*-", "+ ", s)
    s = re.sub(r"\(x\s*-\s*-(\d+)\)", r"(x + \1)", s)
    s = re.sub(r"\(x\s*\+\s*-(\d+)\)", r"(x - \1)", s)
    s = re.sub(r"x\s*-\s*-(\d+)", r"x + \1", s)
    s = re.sub(r"x\s*\+\s*-(\d+)", r"x - \1", s)
    s = re.sub(r"\(x\s*-\s*0\)", "x", s)
    s = re.sub(r"\(x\s*\+\s*0\)", "x", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _strip_alt(text: str) -> str:
    s = _ALT_SUFFIX.sub("", str(text).strip())
    return _ALT_NUM_SUFFIX.sub("", s).strip()


def _norm_option(text: str) -> str:
    return _normalize_factor_text(_strip_alt(text)).lower()


def _nature_key(text: str) -> str | None:
    t = _norm_option(text)
    if "distinct" in t and "root" in t:
        return "nature:distinct"
    if "equal" in t and "root" in t:
        return "nature:equal"
    if "no real" in t:
        return "nature:none"
    if "always real" in t:
        return "nature:always"
    return None


def _parse_factor_quad(question: str) -> tuple[int, int, int] | None:
    m = re.search(r"Factorise completely:\s*(.+?)\s*=\s*0", str(question), re.I)
    if not m:
        return None
    s = m.group(1).replace(" ", "").replace("−", "-")
    m2 = re.match(r"(\d+)x²([+-])(\d+)x([+-])(\d+)$", s)
    if not m2:
        return None
    a = int(m2.group(1))
    b = int(m2.group(3)) if m2.group(2) == "+" else -int(m2.group(3))
    c = int(m2.group(5)) if m2.group(4) == "+" else -int(m2.group(5))
    return a, b, c


def _wrong_distractor(correct: str, used: set[str], seed: str) -> str:
    used_norm = {_norm_option(u) for u in used}
    correct_norm = _norm_option(correct)
    nkey = _nature_key(correct)
    if nkey:
        for opt in _NATURE_OPTIONS:
            if _nature_key(opt) != nkey and _norm_option(opt) not in used_norm:
                return opt
    m = re.match(r"^(-?\d+)$", _strip_alt(correct).strip())
    if m:
        v = int(m.group(1))
        for delta in (1, 2, 3, 4, 5, -1, -2):
            cand = str(v + delta)
            if _norm_option(cand) not in used_norm and cand != correct:
                return cand
    if "x²" in correct or "x2" in correct.lower():
        for delta in (1, 2, 3, 5, 7):
            cand = re.sub(r"=\s*0$", f" + {delta} = 0", correct)
            if _norm_option(cand) not in used_norm:
                return _normalize_factor_text(cand)
    n = _det_int(seed, 2, 50)
    cand = str(n)
    if _norm_option(cand) not in used_norm:
        return cand
    return str(n + 11)


def _det_int(seed: str, lo: int, hi: int) -> int:
    h = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
    return lo + h % (hi - lo + 1)


def _factor_root_term(r: int) -> str:
    if r == 0:
        return "x"
    if r > 0:
        return f"(x − {r})"
    return f"(x + {-r})"


def _complete_factored_quad(k: int, r1: int, r2: int) -> str:
    if r1 == r2:
        f = _factor_root_term(r1)
        if f == "x":
            return f"{k}x² = 0"
        return f"{k}{f}² = 0"
    f1, f2 = _factor_root_term(r1), _factor_root_term(r2)
    if k == 1:
        return f"{f1}{f2} = 0"
    return f"{k}{f1}{f2} = 0"


def _integer_roots(a: int, b: int, c: int) -> tuple[int, int] | None:
    """Return roots (r1, r2) for ax²+bx+c if both are integers."""
    if a == 0:
        return None
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    s = math.isqrt(disc)
    if s * s != disc:
        return None
    r1 = (-b + s) // (2 * a)
    r2 = (-b - s) // (2 * a)
    if a * r1 * r1 + b * r1 + c != 0 or a * r2 * r2 + b * r2 + c != 0:
        return None
    return r1, r2


def _fix_equal_roots(q: dict) -> bool:
    question = str(q.get("question", ""))
    if "equal roots" not in question.lower() or "k" not in question.lower():
        return False
    m = _EQUAL_ROOTS.search(question.replace("x2", "x²"))
    if not m:
        return False
    c = int(m.group(1))
    root = int(math.isqrt(c))
    if root * root != c:
        return False
    k_pos = 2 * root

    opts = [_strip_alt(o) for o in q.get("options", [])]
    pos = str(k_pos)
    if pos not in opts:
        wrong = [str(k_pos + 1), str(k_pos - 2), str(c)]
        opts = [pos] + [w for w in wrong if w != pos][:3]
        while len(opts) < 4:
            opts.append(str(k_pos + len(opts)))
        opts = opts[:4]

    q["question"] = f"For x² + kx + {c} = 0 to have equal roots, find k when k > 0."

    q["options"] = opts
    q["answer"] = opts.index(pos)
    q["explanation"] = (
        f"Equal roots ⇒ Δ = k² − 4({c}) = 0, so k² = {4 * c}. With k > 0, k = {k_pos}."
    )
    return True


def _fix_no_real_roots_fixed(q: dict) -> bool:
    m = _NO_REAL_FIXED.match(str(q.get("question", "")).strip())
    if not m:
        return False
    b, c = int(m.group(1) or 1), int(m.group(2))
    if b * b - 4 * c >= 0:
        qid = str(q.get("id", ""))
        b = _det_int(qid + "b", 1, 12)
        c = _det_int(qid + "c", 1, 30)
        while b * b - 4 * c >= 0:
            c += 1
        bx = f"{b}x" if b != 1 else "x"
        q["question"] = f"x² + {bx} + {c} = 0 has no real roots because:"
    correct = "Δ < 0"
    pool = ["Δ > 0", "Δ = 0", "Always real"]
    opts = [correct] + pool
    qid = str(q.get("id", ""))
    shift = _det_int(qid + "shuf", 0, 5)
    for _ in range(shift % 4):
        opts = [opts[-1]] + opts[:-1]
    q["options"] = opts
    q["answer"] = opts.index(correct)
    m2 = re.search(r"^x²\s*\+\s*(\d*)x\s*\+\s*(\d+)\s*=", q["question"])
    b2 = int(m2.group(1) or 1) if m2 else b
    c2 = int(m2.group(2)) if m2 else c
    d = b2 * b2 - 4 * c2
    q["explanation"] = f"Δ = {b2}² − 4({c2}) = {d} < 0."
    return True


def _fix_rectangle(q: dict) -> bool:
    if not _RECT.search(str(q.get("question", ""))):
        return False
    qid = str(q.get("id", "rect"))
    w = _det_int(qid + "w", 3, 10)
    d = _det_int(qid + "d", 2, 14)
    area = w * (w + d)
    q["question"] = f"A rectangle has length {d} m more than width. Area = {area} m². Width = ?"
    correct = f"{w} m"
    wrong = [f"{d} m", f"{w + 1} m", f"{area} m"]
    opts = [correct] + [x for x in wrong if x != correct][:3]
    while len(opts) < 4:
        opts.append(f"{w + len(opts)} m")
    shift = _det_int(qid + "r", 0, 3)
    for _ in range(shift):
        opts = [opts[-1]] + opts[:-1]
    q["options"] = opts
    q["answer"] = opts.index(correct)
    q["explanation"] = f"Let width = x; x(x+{d}) = {area} ⇒ x = {w}."
    return True


def _fix_complete_factorisation(q: dict) -> bool:
    parsed = _parse_factor_quad(str(q.get("question", "")))
    if not parsed:
        return False
    a, b, c = parsed
    roots = _integer_roots(a, b, c)
    if not roots:
        return False
    r1, r2 = roots
    correct = _normalize_factor_text(_complete_factored_quad(a, r1, r2))
    inner_b, inner_c = b // a, c // a
    alt_roots = _complete_factored_quad(a, r1 + 1, r2) if r1 != r2 else _complete_factored_quad(a, r1, r2 + 1)
    wrong = [
        _normalize_factor_text(f"{a}(x² + {inner_b}x + {inner_c})"),
        _normalize_factor_text(alt_roots),
        _normalize_factor_text(f"(x² + {b}x + {c})"),
    ]
    used = {correct}
    distractors: list[str] = []
    for w in wrong:
        if _norm_option(w) == _norm_option(correct) or _norm_option(w) in {_norm_option(x) for x in used}:
            continue
        distractors.append(w)
        used.add(w)
    while len(distractors) < 3:
        filler = _wrong_distractor(correct, used, f"{q.get('id', '')}-f{len(distractors)}")
        distractors.append(_normalize_factor_text(filler))
        used.add(filler)
    opts = [correct] + distractors[:3]
    qid = str(q.get("id", ""))
    shift = _det_int(qid + "f", 0, 3)
    for _ in range(shift):
        opts = [opts[-1]] + opts[:-1]
    q["options"] = opts
    q["answer"] = opts.index(correct)
    return True


def _fix_equivalent_options(q: dict) -> bool:
    raw = [str(o) for o in q.get("options", [])]
    if len(raw) != 4:
        return False
    ans = q.get("answer")
    if not isinstance(ans, int) or not (0 <= ans < 4):
        return False
    opts = [_strip_alt(o) for o in raw]
    changed = opts != raw
    correct_norm = _norm_option(opts[ans])
    correct_nature = _nature_key(opts[ans])
    seen: set[str] = set()
    for i in range(4):
        n = _norm_option(opts[i])
        nk = _nature_key(opts[i])
        equiv = nk if nk and correct_nature else n
        if i == ans:
            seen.add(equiv)
            continue
        if equiv == (correct_nature or correct_norm) or equiv in seen or n == correct_norm:
            used = {opts[j] for j in range(4) if j != i}
            opts[i] = _wrong_distractor(opts[ans], used, f"{q.get('id', '')}-{i}")
            changed = True
            n = _norm_option(opts[i])
            nk = _nature_key(opts[i])
            equiv = nk if nk else n
        seen.add(equiv)
    if changed:
        q["options"] = [_normalize_factor_text(o) for o in opts]
    return changed


def _normalize_question_fields(q: dict) -> None:
    q["question"] = _normalize_factor_text(str(q.get("question", "")))
    if q.get("explanation"):
        q["explanation"] = _normalize_factor_text(str(q.get("explanation", "")))
    opts = q.get("options")
    if isinstance(opts, list):
        q["options"] = [_normalize_factor_text(_strip_alt(o)) for o in opts]


def repair_file(path: Path) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    stats = {
        "equal_roots": 0,
        "no_real": 0,
        "rectangle": 0,
        "factor": 0,
        "dedupe": 0,
        "normalized": 0,
    }
    questions = data.get("questions", {})
    if not isinstance(questions, dict):
        return stats

    for bucket in questions.values():
        if not isinstance(bucket, list):
            continue
        for q in bucket:
            if not isinstance(q, dict):
                continue
            _normalize_question_fields(q)
            stats["normalized"] += 1
            if _fix_equal_roots(q):
                stats["equal_roots"] += 1
            if _fix_no_real_roots_fixed(q):
                stats["no_real"] += 1
            if _fix_rectangle(q):
                stats["rectangle"] += 1
            if _fix_complete_factorisation(q):
                stats["factor"] += 1
            if _fix_equivalent_options(q):
                stats["dedupe"] += 1
            if "equal roots" in str(q.get("question", "")).lower():
                _fix_equal_roots(q)
            _fix_equivalent_options(q)

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return stats


def main() -> int:
    if not UNIT04_DIR.is_dir():
        print(f"Missing {UNIT04_DIR}", file=sys.stderr)
        return 1
    totals = {k: 0 for k in ("equal_roots", "no_real", "rectangle", "factor", "dedupe", "normalized")}
    for path in sorted(UNIT04_DIR.glob("topic_*.json")):
        stats = repair_file(path)
        for k in totals:
            totals[k] += stats[k]
        print(
            f"{path.name}: equal_roots={stats['equal_roots']} no_real={stats['no_real']} "
            f"rectangle={stats['rectangle']} factor={stats['factor']} dedupe={stats['dedupe']}"
        )
    print("Totals:", totals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
