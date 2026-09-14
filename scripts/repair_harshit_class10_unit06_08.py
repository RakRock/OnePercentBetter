#!/usr/bin/env python3
"""Repair Class 10 Units 6–8 question banks (distinct MCQ options)."""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from numeric_expression_eval import options_equivalent, validate_distinct_options

_ALT_SUFFIX = re.compile(r"\s*\(alt\)\s*$", re.I)
_ALT_NUM_SUFFIX = re.compile(r"\s*\(alt\s*\d+\)\s*$", re.I)
_RATIO_RE = re.compile(r"^\s*(-?\d+)\s*:\s*(-?\d+)\s*$")
_TRIG_POOL = ["0", "1", "1/2", "√3/2", "1/√2", "1/√3", "√3", "√2", "undefined", "2"]


def _det_int(seed: str, lo: int, hi: int) -> int:
    h = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
    return lo + h % (hi - lo + 1)


def _strip_alt(text: str) -> str:
    s = _ALT_SUFFIX.sub("", str(text).strip())
    return _ALT_NUM_SUFFIX.sub("", s).strip()


def _norm_option(text: str) -> str:
    return _strip_alt(text).strip().lower()


def _wrong_distractor(correct: str, used: set[str], seed: str) -> str:
    used_norm = {_norm_option(u) for u in used}
    base = _strip_alt(correct)

    m = _RATIO_RE.match(base)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        for da, db in ((1, 0), (0, 1), (2, 0), (-1, 0), (0, 2), (1, 1)):
            cand = f"{a + da}:{max(1, b + db)}"
            if _norm_option(cand) not in used_norm and not any(
                options_equivalent(cand, u) for u in used
            ):
                return cand

    if base in _TRIG_POOL or "√" in base or base in ("1/2",):
        for cand in _TRIG_POOL:
            if _norm_option(cand) in used_norm:
                continue
            if options_equivalent(cand, correct) or any(options_equivalent(cand, u) for u in used):
                continue
            return cand

    if re.search(r"²\s*[-−+]\s*\d+²", base) or re.search(r"\d+²\s*[-−]\s*\d+²", base):
        return f"({_det_int(seed, 2, 8)}² + {_det_int(seed, 3, 9)}²)"

    if re.fullmatch(r"√\(\d+² \+ \d+²\)", base.replace(" ", "")):
        n = _det_int(seed, 2, 9)
        return f"{n} units"

    if base.lstrip("-").isdigit():
        v = int(base)
        for delta in (1, 2, 3, 4, -1, -2, 5):
            cand = str(v + delta)
            if _norm_option(cand) not in used_norm and not options_equivalent(cand, correct):
                return cand

    if base.endswith(" units"):
        v = int(base.split()[0])
        for delta in (1, 2, 3, 5):
            cand = f"{v + delta} units"
            if _norm_option(cand) not in used_norm:
                return cand

    if " : " in base:
        parts = [p.strip() for p in base.split(":")]
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            a, b = int(parts[0]), int(parts[1])
            cand = f"{a + 1} : {b + 2}"
            if _norm_option(cand) not in used_norm:
                return cand

    n = _det_int(seed, 3, 99)
    cand = str(n)
    if _norm_option(cand) not in used_norm and not options_equivalent(cand, correct):
        return cand
    return str(n + 7)


def _fix_equivalent_options(q: dict) -> bool:
    raw = [str(o) for o in q.get("options", [])]
    if len(raw) != 4:
        return False
    ans = q.get("answer")
    if not isinstance(ans, int) or not (0 <= ans < 4):
        return False

    opts = [_strip_alt(o) for o in raw]
    changed = opts != raw
    correct = opts[ans]
    seen: set[str] = set()

    for i in range(4):
        if i == ans:
            seen.add(_norm_option(correct))
            continue
        dup = options_equivalent(opts[i], correct) or any(
            options_equivalent(opts[i], opts[j]) for j in range(4) if j != i
        )
        n = _norm_option(opts[i])
        if dup or n in seen:
            used = {opts[j] for j in range(4) if j != i}
            opts[i] = _wrong_distractor(correct, used, f"{q.get('id', '')}-{i}")
            changed = True
            n = _norm_option(opts[i])
        seen.add(n)

    if changed:
        q["options"] = opts
        try:
            validate_distinct_options(opts)
        except ValueError:
            return _fix_equivalent_options(q)
    return changed


def repair_file(path: Path) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    stats = {"fixed": 0, "questions": 0}
    questions = data.get("questions", {})
    if not isinstance(questions, dict):
        return stats

    for bucket in questions.values():
        if not isinstance(bucket, list):
            continue
        for q in bucket:
            if not isinstance(q, dict):
                continue
            stats["questions"] += 1
            if _fix_equivalent_options(q):
                stats["fixed"] += 1
                try:
                    validate_distinct_options([str(o) for o in q["options"]])
                except ValueError as exc:
                    print(f"  still broken {q.get('id')}: {exc}", file=sys.stderr)

    if stats["fixed"]:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return stats


def main() -> int:
    total_fixed = 0
    for unit in (6, 7, 8):
        unit_dir = ROOT / "HarshitMath" / "class10" / "question_banks" / f"unit_{unit:02d}"
        if not unit_dir.is_dir():
            print(f"Missing {unit_dir}", file=sys.stderr)
            continue
        print(f"Unit {unit}:")
        for path in sorted(unit_dir.glob("topic_*.json")):
            stats = repair_file(path)
            total_fixed += stats["fixed"]
            if stats["fixed"]:
                print(f"  {path.name}: fixed {stats['fixed']} / {stats['questions']}")
    print(f"Total questions repaired: {total_fixed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
