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
    unit_id: int, topic_id: int, level: str, target: int, *, max_attempts: int
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


def seed_unit(unit_id: int, per_level: int = 12) -> dict:
    topics = h10t.topics_for_unit(unit_id)
    summary: dict[str, dict] = {}
    for topic_id in sorted(topics):
        for level in h10t.LEVEL_ORDER:
            existing = len(h10q.load_bank(unit_id, topic_id).get("questions", {}).get(level, []))
            batch, attempts = _collect_unique_templates(
                unit_id, topic_id, level, per_level, max_attempts=per_level * 80
            )
            added = h10q.add_questions(unit_id, topic_id, level, batch)
            summary[f"u{unit_id}_t{topic_id}_{level}"] = {
                "existing": existing,
                "generated": len(batch),
                "added": added,
                "attempts": attempts,
            }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Harshit Class 10 question banks")
    parser.add_argument("--unit", type=int, default=1)
    parser.add_argument("--per-level", type=int, default=12, help="Target unique questions per topic/level")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Clear existing bank files for this unit before seeding",
    )
    args = parser.parse_args()

    before = h10q.bank_stats(args.unit)["total"]
    if args.refresh:
        removed = h10q.clear_unit_bank(args.unit)
        print(f"Unit {args.unit}: cleared {removed} bank file(s) ({before} questions removed)")

    summary = seed_unit(args.unit, args.per_level)
    after = h10q.bank_stats(args.unit)["total"]
    added_total = sum(row["added"] for row in summary.values())

    print(f"Unit {args.unit}: added {added_total} questions (bank total: {before} → {after})")
    for key, row in sorted(summary.items()):
        if row["added"] or row["generated"] < args.per_level:
            print(
                f"  {key}: +{row['added']} "
                f"(had {row['existing']}, generated {row['generated']}/{args.per_level} unique templates)"
            )

    if added_total == 0 and not args.refresh:
        print(
            "\nNo new questions added — the bank already contains every unique template "
            f"the generators could produce at --per-level {args.per_level}."
        )
        print("Use --refresh to wipe and rebuild, or increase generator variety in harshit_class10_topics.py.")


if __name__ == "__main__":
    main()
