#!/usr/bin/env python3
"""Build Harshit Physics Unit 4 question bank (200 MCQs from concept cards)."""

from __future__ import annotations

import json
import random
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import harshit_physics_content as hpc  # noqa: E402
import harshit_physics_topics as hpt  # noqa: E402

from scripts.build_physics_unit2_question_bank import (  # noqa: E402
    GENERATORS,
    _questions_for_day as _questions_for_day_base,
)

UNIT_ID = 4
TARGET_TOTAL = 200
BANK_PATH = ROOT / "HarshitPhysics" / "unit4" / "question_bank.json"
CHAPTER_REF = "NCERT Class 10 Ch 12 — Magnetic Effects of Electric Current"
PREFIX = f"u{UNIT_ID}"


def _questions_for_day(day_id: int, count: int) -> list[dict]:
    concepts = hpc.concepts_for_day(day_id, unit_id=UNIT_ID)
    if not concepts:
        return []
    out: list[dict] = []
    seq = 1
    levels_cycle = ["A", "B", "C"]
    ci = 0
    gi = 0
    while len(out) < count:
        concept = concepts[ci % len(concepts)]
        level = levels_cycle[len(out) % 3]
        gens = GENERATORS[level]
        gen = gens[gi % len(gens)]
        q = gen(concept, day_id, concepts, level, seq)
        q["id"] = q["id"].replace("u2_", f"{PREFIX}_")
        q["category"] = q["category"].replace("u2_", f"{PREFIX}_")
        q["category_label"] = hpt.format_topic_level_label(UNIT_ID, day_id, level)
        q["chapter_ref"] = CHAPTER_REF
        out.append(q)
        seq += 1
        ci += 1
        gi += 1
    return out


def build_bank(*, seed: int = 42) -> dict:
    random.seed(seed)
    days = [d for d in hpc.list_days(stage=1, unit_id=UNIT_ID) if d.get("active")]
    n_days = len(days) or 1
    base = TARGET_TOTAL // n_days
    extra = TARGET_TOTAL % n_days

    all_q: list[dict] = []
    by_day: dict[str, list[dict]] = {}
    for i, day in enumerate(sorted(days, key=lambda d: d["day"])):
        did = int(day["day"])
        count = base + (1 if i < extra else 0)
        day_qs = _questions_for_day(did, count)
        by_day[str(did)] = day_qs
        all_q.extend(day_qs)

    seen: set[str] = set()
    unique: list[dict] = []
    for q in all_q:
        key = q["question"].strip().lower()
        if key in seen:
            q["id"] = f"{PREFIX}_{uuid.uuid4().hex[:8]}"
            key = q["question"].strip().lower() + q["id"]
        seen.add(key)
        unique.append(q)

    return {
        "meta": {
            "unit_id": UNIT_ID,
            "chapter_ref": CHAPTER_REF,
            "total_questions": len(unique),
            "seed": seed,
        },
        "questions_by_day": by_day,
        "questions": unique,
    }


def main() -> None:
    bank = build_bank()
    BANK_PATH.parent.mkdir(parents=True, exist_ok=True)
    BANK_PATH.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {BANK_PATH} — {bank['meta']['total_questions']} questions")


if __name__ == "__main__":
    main()
