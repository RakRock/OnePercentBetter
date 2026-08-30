#!/usr/bin/env python3
"""Seed 3 unique exam-template variants per exam type into question banks."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import harshit_class10_exam_generators as h10eg
import harshit_class10_exam_types as h10et
import harshit_class10_questions as h10q


def _unique_variants(exam_type_id: str, count: int = 3) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for _ in range(count * 30):
        q = h10eg.generate(exam_type_id)
        if not q:
            continue
        key = h10q.question_dedup_key(str(q.get("question", "")), q.get("options"))
        if key in seen:
            continue
        seen.add(key)
        out.append(q)
        if len(out) >= count:
            break
    return out


def main() -> int:
    total_added = 0
    for et in h10et.EXAM_TYPES:
        variants = _unique_variants(et.id, count=3)
        if not variants:
            print(f"WARN: no variants for {et.id}")
            continue
        added = h10q.add_questions(et.unit_id, et.topic_id, et.level, variants)
        total_added += added
        print(f"{et.id}: seeded {added}/{len(variants)}")
    print(f"Done. Added {total_added} questions total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
