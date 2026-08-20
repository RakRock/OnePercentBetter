#!/usr/bin/env python3
"""Build chapter-derived question banks from NCERT Class 9 PDFs.

Requires chapter PDFs in HarshitMath/class9_chapters/chapter_XX/ and XAI_API_KEY.

Examples:
    python3 scripts/build_harshit_chapter_questions.py --prereq 1
    python3 scripts/build_harshit_chapter_questions.py --prereq 1 --seed-templates
    python3 scripts/build_harshit_chapter_questions.py --all --per-level 4
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import harshit_chapter_pdf as hcp
import harshit_chapter_questions as hcq
import harshit_math_prereqs as hmp
import harshit_prereq_llm as hllm
import harshit_prereq_topics as hpt


def _aliases_for_chapter(prereq_id: int, chapter_num: int) -> list[str] | None:
    prereq = hmp.get_prereq(prereq_id)
    if not prereq:
        return None
    for ch in prereq.get("class9_chapters", []):
        if ch["number"] == chapter_num:
            return ch.get("folder_aliases")
    return None


def seed_prereq_bank(prereq_id: int, per_level: int) -> int:
    """Seed bank with NCERT-aligned math MCQs (fractions, integers, etc.) when LLM is unavailable."""
    topics = hpt.topics_for_prereq(prereq_id)
    total_added = 0
    for topic_id, info in sorted(topics.items()):
        ch = hcq.chapter_for_topic(prereq_id, topic_id)
        print(f"  topic {topic_id}: {info['name']} ← seed Ch {ch or '?'}")
        for level in info.get("levels", {}):
            qs: list[dict] = []
            used_keys: set[str] = set()
            attempts = 0
            while len(qs) < per_level and attempts < per_level * 16:
                attempts += 1
                q = hpt.generate_question(
                    prereq_id,
                    topic_id,
                    level,
                    exclude_text=used_keys,
                    templates_only=True,
                )
                if not q:
                    break
                key = hcq.question_dedup_key(str(q.get("question", "")))
                if key in used_keys:
                    continue
                used_keys.add(key)
                item = dict(q)
                item["source"] = "chapter_seed"
                item["chapter_num"] = ch
                qs.append(item)
            added = hcq.add_questions(prereq_id, topic_id, level, qs, chapter_num=ch)
            total_added += added
            print(f"    Level {level}: +{added} seeded question(s)")
    return total_added


def build_prereq(prereq_id: int, per_level: int, api_key: str, *, max_workers: int | None = None) -> int:
    topics = hpt.topics_for_prereq(prereq_id)
    tasks: list[tuple[int, str, int]] = []
    meta: dict[tuple[int, str], tuple[int, list[str]]] = {}

    for topic_id, info in sorted(topics.items()):
        ch = hcq.chapter_for_topic(prereq_id, topic_id)
        if ch is None:
            print(f"  skip topic {topic_id} — no chapter mapping")
            continue
        bundle = hcp.extract_chapter_text(ch, _aliases_for_chapter(prereq_id, ch))
        if not bundle["has_text"]:
            print(f"  skip topic {topic_id} ({info['name']}) — no PDF/text for Ch {ch}")
            continue
        print(f"  topic {topic_id}: {info['name']} ← Ch {ch} ({len(bundle['text'])} chars)")
        for level in info.get("levels", {}):
            tasks.append((topic_id, level, per_level))
            meta[(topic_id, level)] = (ch, bundle.get("sources", []))

    if not tasks:
        return 0

    workers = max_workers or hllm.DEFAULT_PARALLEL
    print(f"  generating {len(tasks)} slot(s) in parallel (workers={workers})…")
    results, errors = hllm.generate_for_slots_parallel(
        api_key, prereq_id, tasks, max_workers=workers
    )

    total_added = 0
    for (topic_id, level), qs in sorted(results.items()):
        ch, sources = meta.get((topic_id, level), (None, []))
        source = sources[0] if sources else ""
        added = hcq.add_questions(
            prereq_id,
            topic_id,
            level,
            qs,
            chapter_num=ch,
            source_pdf=source,
        )
        total_added += added
        print(f"    topic {topic_id} Level {level}: +{added} question(s)")

    failed = len(tasks) - len(results)
    if errors:
        for err in errors[:5]:
            print(f"  error: {err}")
        if len(errors) > 5:
            print(f"  … and {len(errors) - 5} more error(s)")
    if failed:
        print(f"  {failed} slot(s) failed — check API key / rate limits")

    return total_added


def _load_xai_key() -> str:
    key = os.environ.get("XAI_API_KEY", "").strip()
    if key:
        return key
    secrets_path = ROOT / ".streamlit" / "secrets.toml"
    if secrets_path.is_file():
        try:
            import tomllib

            data = tomllib.loads(secrets_path.read_text(encoding="utf-8"))
            return str(data.get("XAI_API_KEY", "")).strip()
        except Exception:
            pass
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Harshit chapter question banks from PDFs")
    parser.add_argument("--prereq", type=int, help="PreReq id 1-6")
    parser.add_argument("--all", action="store_true", help="Build all six PreReq units")
    parser.add_argument("--per-level", type=int, default=3, help="Questions per topic/level (LLM mode)")
    parser.add_argument(
        "--parallel",
        type=int,
        default=hllm.DEFAULT_PARALLEL,
        help=f"Concurrent Grok requests (default {hllm.DEFAULT_PARALLEL})",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Parse NCERT PDF fill-in-blank exercises directly (no XAI_API_KEY needed)",
    )
    parser.add_argument(
        "--seed-templates",
        action="store_true",
        help="Seed bank with NCERT-aligned math MCQs (integers, fractions, exponents)",
    )
    parser.add_argument(
        "--purge",
        action="store_true",
        help="Remove low-quality placeholder questions from existing banks",
    )
    args = parser.parse_args()

    if args.purge:
        removed = hcq.purge_low_quality_banks()
        print(f"Purged {removed} low-quality question(s) from {hcq.BANK_DIR}")
        return

    if args.offline:
        import harshit_chapter_extract as hce

        chapters = None
        if args.prereq and not args.all:
            chapters = sorted(
                {
                    hcq.chapter_for_topic(args.prereq, tid)
                    for tid in hpt.topics_for_prereq(args.prereq)
                    if hcq.chapter_for_topic(args.prereq, tid)
                }
            )
        total = hce.build_offline_banks(chapters)
        print(f"\nOffline extract done — {total} question(s) added to {hcq.BANK_DIR}")
        return

    if args.seed_templates:
        ids = list(range(1, 7)) if args.all else ([args.prereq] if args.prereq else [])
        if not ids:
            parser.error("Specify --prereq N or --all")
        grand = 0
        for pid in ids:
            prereq = hmp.get_prereq(pid)
            title = prereq["title"] if prereq else f"PreReq {pid}"
            print(f"\nPreReq {pid}: {title} (template seed)")
            grand += seed_prereq_bank(pid, args.per_level)
        print(f"\nDone — {grand} question(s) seeded to {hcq.BANK_DIR}")
        return

    api_key = _load_xai_key()
    if not api_key:
        print("No XAI_API_KEY — falling back to template seed.")
        args.seed_templates = True
        ids = list(range(1, 7)) if args.all else ([args.prereq] if args.prereq else [])
        if not ids:
            parser.error("Specify --prereq N or --all")
        grand = 0
        for pid in ids:
            prereq = hmp.get_prereq(pid)
            title = prereq["title"] if prereq else f"PreReq {pid}"
            print(f"\nPreReq {pid}: {title} (template seed)")
            grand += seed_prereq_bank(pid, args.per_level)
        print(f"\nDone — {grand} question(s) seeded to {hcq.BANK_DIR}")
        return

    ids = list(range(1, 7)) if args.all else ([args.prereq] if args.prereq else [])
    if not ids:
        parser.error("Specify --prereq N or --all")

    grand = 0
    for pid in ids:
        prereq = hmp.get_prereq(pid)
        title = prereq["title"] if prereq else f"PreReq {pid}"
        print(f"\nPreReq {pid}: {title}")
        added = build_prereq(pid, args.per_level, api_key, max_workers=args.parallel)
        if added == 0:
            print("  xAI returned nothing — seeding template bank as fallback…")
            added = seed_prereq_bank(pid, args.per_level)
        grand += added

    print(f"\nDone — {grand} question(s) added to {hcq.BANK_DIR}")


if __name__ == "__main__":
    main()
