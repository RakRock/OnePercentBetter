#!/usr/bin/env python3
"""Seed Class 10 unit question banks from template generators."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import harshit_class10_questions as h10q
import harshit_class10_topics as h10t


def _collect_unique_templates(
    unit_id: int,
    topic_id: int,
    level: str,
    target: int,
    *,
    max_attempts: int,
) -> tuple[list[dict], int]:
    batch: list[dict] = []
    seen: set[str] = set()
    attempts = 0
    while len(batch) < target and attempts < max_attempts:
        attempts += 1
        q = h10t.generate_question(unit_id, topic_id, level, templates_only=True)
        if not q:
            continue
        key = h10q.question_dedup_key(str(q.get("question", "")), q.get("options"))
        if key in seen:
            continue
        seen.add(key)
        batch.append(q)
    return batch, attempts


def seed_unit(
    unit_id: int,
    per_level: int = 12,
    *,
    attempt_multiplier: int = 80,
) -> dict:
    topics = h10t.topics_for_unit(unit_id)
    summary: dict[str, dict] = {}
    for topic_id in sorted(topics):
        for level in h10t.LEVEL_ORDER:
            existing = len(h10q.load_bank(unit_id, topic_id).get("questions", {}).get(level, []))
            need = max(0, per_level - existing)
            if need == 0:
                summary[f"u{unit_id}_t{topic_id}_{level}"] = {
                    "existing": existing,
                    "generated": 0,
                    "added": 0,
                    "attempts": 0,
                }
                continue
            batch, attempts = _collect_unique_templates(
                unit_id,
                topic_id,
                level,
                need,
                max_attempts=max(need * attempt_multiplier, 400),
            )
            added = h10q.add_questions(unit_id, topic_id, level, batch)
            summary[f"u{unit_id}_t{topic_id}_{level}"] = {
                "existing": existing,
                "generated": len(batch),
                "added": added,
                "attempts": attempts,
            }
    return summary


def _seed_one_unit(
    unit_id: int,
    *,
    per_level: int,
    refresh: bool,
    attempt_multiplier: int,
    passes: int,
) -> int:
    before = h10q.bank_stats(unit_id)["total"]
    if refresh:
        removed = h10q.clear_unit_bank(unit_id)
        print(f"Unit {unit_id}: cleared {removed} bank file(s) ({before} questions removed)")
        before = 0

    added_total = 0
    for pass_num in range(1, passes + 1):
        summary = seed_unit(unit_id, per_level, attempt_multiplier=attempt_multiplier)
        pass_added = sum(row["added"] for row in summary.values())
        added_total += pass_added
        if pass_added == 0 and pass_num > 1:
            break

    after = h10q.bank_stats(unit_id)["total"]
    print(f"Unit {unit_id}: added {added_total} questions (bank total: {before} → {after})")
    return added_total


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Harshit Class 10 question banks")
    parser.add_argument("--unit", type=int, default=1)
    parser.add_argument("--from-unit", type=int, default=0, help="Batch start unit (inclusive)")
    parser.add_argument("--to-unit", type=int, default=0, help="Batch end unit (inclusive)")
    parser.add_argument("--per-level", type=int, default=12, help="Target unique questions per topic/level")
    parser.add_argument(
        "--passes",
        type=int,
        default=1,
        help="Number of seed passes (adds more unique templates when generators vary)",
    )
    parser.add_argument(
        "--attempt-multiplier",
        type=int,
        default=80,
        help="Max generator attempts = per_level × this multiplier",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Clear existing bank files for this unit before seeding",
    )
    args = parser.parse_args()

    if args.from_unit and args.to_unit:
        units = range(args.from_unit, args.to_unit + 1)
    else:
        units = [args.unit]

    grand_total = 0
    for unit_id in units:
        if not h10t.topics_for_unit(unit_id):
            print(f"Unit {unit_id}: skipped (no topics defined)")
            continue
        grand_total += _seed_one_unit(
            unit_id,
            per_level=args.per_level,
            refresh=args.refresh,
            attempt_multiplier=args.attempt_multiplier,
            passes=args.passes,
        )

    if len(units) > 1:
        print(f"\nBatch complete: {grand_total} questions added across units {units.start}–{units.stop - 1}.")
    elif grand_total == 0 and not args.refresh:
        print(
            "\nNo new questions added — banks may already meet --per-level "
            f"or generators need more variety in harshit_class10_topics.py."
        )


if __name__ == "__main__":
    main()
