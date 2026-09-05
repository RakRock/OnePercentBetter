#!/usr/bin/env python3
"""Seed AI-generated Spanish practice questions via Grok (optional bulk run)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import xai_client  # noqa: F401 — truststore SSL on macOS

from arjun_spanish import config as escfg
from arjun_spanish import llm as esllm
from arjun_spanish import session as ess


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed Grok Spanish MCQs for Arjun")
    parser.add_argument("--count", type=int, default=12, help="Questions per batch")
    parser.add_argument("--topics", default="", help="Comma-separated topic ids (default: school topics)")
    args = parser.parse_args()

    api_key = _load_api_key()
    if not api_key:
        print("XAI_API_KEY not set")
        return 1

    cfg = escfg.default_config()
    if args.topics.strip():
        cfg["topics"] = [t.strip() for t in args.topics.split(",") if t.strip()]

    slots = ess._slot_plan({**cfg, "question_count": args.count}, args.count)
    print(f"Generating {len(slots)} questions…")
    batch = esllm.generate_session_questions_raw(api_key, slots)
    print(f"Saved {len(batch)} questions to ArjunSpanish/ai_questions.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
