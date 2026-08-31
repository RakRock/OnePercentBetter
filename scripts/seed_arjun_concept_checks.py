#!/usr/bin/env python3
"""Seed AI-generated concept-check questions for Arjun Course 3 (Units 1–5)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import arjun_course3_concept_check as c3cc
import arjun_course3_concept_check_store as c3store
import arjun_course3_concept_check_llm as c3ccllm
import arjun_course3_practice as c3p
import xai_client  # noqa: F401 — truststore SSL for macOS


def _load_api_key() -> str:
    key = os.environ.get("XAI_API_KEY", "").strip()
    if key:
        return key
    secrets = ROOT / ".streamlit" / "secrets.toml"
    if secrets.is_file():
        try:
            import tomllib

            data = tomllib.loads(secrets.read_text(encoding="utf-8"))
            key = str(data.get("XAI_API_KEY", "")).strip()
        except Exception:
            pass
    return key


def seed_unit(
    unit_id: int,
    api_key: str,
    *,
    per_category: int = 4,
    levels: list[str] | None = None,
    verbose: bool = False,
    fill_missing: bool = True,
) -> int:
    cfg = c3p._unit_practice(unit_id)
    cats = cfg["categories"]
    lvls = levels or ["B", "C", "D"]
    existing = c3store.count_by_category(unit_id)
    batch: list[dict] = []
    for cat_id in c3cc.categories_for_unit(unit_id):
        if cat_id not in cats:
            continue
        have = existing.get(cat_id, 0) if fill_missing else 0
        need = max(0, per_category - have)
        if need == 0:
            print(f"  = {cat_id} already has {have}")
            continue
        wanted = [lvls[(have + i) % len(lvls)] for i in range(need)]
        print(f"  … {cat_id} generating {need} ({', '.join(wanted)})")
        generated = c3ccllm.generate_concept_check_batch_llm(
            api_key,
            unit_id,
            cat_id,
            wanted,
            categories=cats,
            revision_tips=cfg["revision_tips"],
            persist=False,
            verbose=verbose,
        )
        batch.extend(generated)
        print(f"  + {cat_id} {len(generated)}/{need} from batch")
        for lvl in wanted[len(generated) :]:
            q = c3ccllm.generate_concept_check_llm(
                api_key,
                unit_id,
                cat_id,
                lvl,
                categories=cats,
                revision_tips=cfg["revision_tips"],
                persist=False,
                verbose=verbose,
            )
            if q:
                batch.append(q)
                print(f"  + {cat_id} [{lvl}] fallback")
            else:
                print(f"  ! failed {cat_id} [{lvl}]")
    added = c3store.add_questions(unit_id, batch)
    print(f"Unit {unit_id}: saved {added}/{len(batch)} to {c3store._unit_path(unit_id)}")
    return added


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed Grok concept-check questions for Course 3")
    parser.add_argument("--units", default="1,2,3,4,5", help="Comma-separated unit ids")
    parser.add_argument("--per-category", type=int, default=4, help="Questions per category")
    parser.add_argument("--levels", default="B,C,D", help="Levels to rotate")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print failure reasons")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Generate per-category even if the AI bank already has enough",
    )
    args = parser.parse_args()

    api_key = _load_api_key()
    if not api_key:
        print("XAI_API_KEY not set — export it or add to .streamlit/secrets.toml")
        return 1

    unit_ids = [int(x.strip()) for x in args.units.split(",") if x.strip()]
    levels = [x.strip().upper() for x in args.levels.split(",") if x.strip()]
    total = 0
    for uid in unit_ids:
        if uid not in range(1, 6):
            print(f"Skip invalid unit {uid}")
            continue
        total += seed_unit(
            uid,
            api_key,
            per_category=args.per_category,
            levels=levels,
            verbose=args.verbose,
            fill_missing=not args.force,
        )
    print(f"Done. Added {total} AI concept-check questions total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
