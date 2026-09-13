#!/usr/bin/env python3
"""Repair Class 10 Unit 5 (Arithmetic Progressions) question banks."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT05_DIR = ROOT / "HarshitMath" / "class10" / "question_banks" / "unit_05"

_ALT_SUFFIX = re.compile(r"\s*\(alt\)\s*$", re.I)
_ALT_NUM_SUFFIX = re.compile(r"\s*\(alt\s*\d+\)\s*$", re.I)


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

    m = re.match(r"^(-?\d+)\s*years?\s*$", base, re.I)
    if m:
        v = int(m.group(1))
        for delta in (3, 5, 7, 2, 4, 9):
            cand = f"{v + delta} years"
            if _norm_option(cand) not in used_norm:
                return cand

    if "/" in base:
        parts = base.split("/", 1)
        if len(parts) == 2 and parts[0].lstrip("-").isdigit() and parts[1].isdigit():
            num, den = int(parts[0]), int(parts[1])
            for dn, dd in ((1, 0), (-1, 0), (2, 0), (0, 1)):
                cand = f"{num + dn}/{max(1, den + dd)}"
                if _norm_option(cand) not in used_norm:
                    return cand

    if base.lstrip("-").isdigit():
        v = int(base)
        for delta in (1, 2, 3, 4, 5, -1, -2, -3):
            cand = str(v + delta)
            if _norm_option(cand) not in used_norm and _norm_option(cand) != _norm_option(correct):
                return cand

    if base.endswith(" km"):
        v = int(base.split()[0])
        for delta in (2, 5, 10):
            cand = f"{v + delta} km"
            if _norm_option(cand) not in used_norm:
                return cand

    if base.startswith("₹") and base[1:].lstrip("-").isdigit():
        v = int(base[1:])
        for delta in (5, 10, 15):
            cand = f"₹{v + delta}"
            if _norm_option(cand) not in used_norm:
                return cand

    n = _det_int(seed, 2, 80)
    cand = str(n)
    if _norm_option(cand) not in used_norm:
        return cand
    return str(n + 13)


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
    seen: set[str] = set()

    for i in range(4):
        n = _norm_option(opts[i])
        if i == ans:
            seen.add(correct_norm)
            continue
        if n == correct_norm or n in seen:
            used = {opts[j] for j in range(4) if j != i}
            opts[i] = _wrong_distractor(opts[ans], used, f"{q.get('id', '')}-{i}")
            changed = True
            n = _norm_option(opts[i])
        seen.add(n)

    if changed:
        q["options"] = opts
    return changed


def repair_file(path: Path) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    stats = {"dedupe": 0, "questions": 0}
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
                stats["dedupe"] += 1

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return stats


def main() -> int:
    if not UNIT05_DIR.is_dir():
        print(f"Missing {UNIT05_DIR}", file=sys.stderr)
        return 1
    totals = {"dedupe": 0, "questions": 0}
    for path in sorted(UNIT05_DIR.glob("topic_*.json")):
        stats = repair_file(path)
        for k in totals:
            totals[k] += stats[k]
        print(f"{path.name}: dedupe={stats['dedupe']} questions={stats['questions']}")
    print("Totals:", totals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
