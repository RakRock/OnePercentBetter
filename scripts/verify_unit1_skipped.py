#!/usr/bin/env python3
"""Independently re-solve Unit 1 questions the local checker could not prove.

Hides the keyed answer, asks Grok to pick 0–3, then compares.
Resume-safe: writes a JSON report after every batch.

  .venv/bin/python scripts/verify_unit1_skipped.py
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import xai_client  # noqa: F401 — truststore SSL for macOS

from arjun_course3_concept_check_store import _unit_path, load_ai_bank
from arjun_course3_unit1_audit import collect_unverified_unit1_questions
from openai import APIConnectionError, APITimeoutError, OpenAIError
from xai_client import make_xai_client

XAI_MODEL = "grok-3-mini"
REPORT_PATH = ROOT / "ArjunCourse3" / "concept_checks" / "unit_1_skipped_verify.json"
BATCH_SIZE = 6
MAX_RETRIES = 4


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


def _load_report() -> dict:
    if not REPORT_PATH.is_file():
        return {"results": {}, "errors": {}}
    try:
        data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"results": {}, "errors": {}}
    data.setdefault("results", {})
    data.setdefault("errors", {})
    return data


def _save_report(report: dict) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _compact(q: dict) -> dict:
    opts = [str(o) for o in (q.get("options") or [])]
    return {
        "id": str(q.get("id")),
        "category": q.get("category"),
        "question": str(q.get("question", "")),
        "options": opts,
    }


def _parse_answers(raw: str, expected_ids: list[str]) -> dict[str, int]:
    match = re.search(r"\[[\s\S]*\]", raw)
    if not match:
        raise ValueError("No JSON array in Grok response")
    items = json.loads(match.group())
    if not isinstance(items, list):
        raise ValueError("Expected a JSON array")
    out: dict[str, int] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        qid = str(item.get("id", "")).strip()
        ans = item.get("answer")
        if qid and isinstance(ans, int) and ans in range(4):
            out[qid] = ans
    missing = [qid for qid in expected_ids if qid not in out]
    if missing:
        raise ValueError(f"Missing ids in Grok response: {missing}")
    return out


def _verify_batch(client, batch: list[dict]) -> dict[str, int]:
    payload = [_compact(q) for q in batch]
    ids = [str(q["id"]) for q in payload]
    user = (
        "Solve each Grade 8 multiple-choice question. "
        "Pick the correct option index (0, 1, 2, or 3). Work the math. "
        "Do not assume any answer is already marked.\n\n"
        f"{json.dumps(payload, ensure_ascii=False)}\n\n"
        'Return ONLY a JSON array like '
        '[{"id":"u1_pat1","answer":1}, ...] with one object per question, same ids.'
    )
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an independent Grade 8 math checker. "
                            "Compute each answer yourself. Return ONLY JSON."
                        ),
                    },
                    {"role": "user", "content": user},
                ],
                max_tokens=1200,
                temperature=0.0,
            )
            raw = (resp.choices[0].message.content or "").strip()
            return _parse_answers(raw, ids)
        except (APIConnectionError, APITimeoutError, OpenAIError) as exc:
            last_err = str(exc)
            wait = 70 if "429" in last_err or "rate" in last_err.lower() else 8 * (attempt + 1)
            print(f"    retry {attempt + 1}/{MAX_RETRIES} after {wait}s ({last_err[:120]})", flush=True)
            time.sleep(wait)
        except (ValueError, json.JSONDecodeError, KeyError, TypeError) as exc:
            last_err = str(exc)
            user += f"\n\nPrevious response invalid ({last_err}). Return ONLY the JSON array."
            time.sleep(3)
    raise RuntimeError(last_err or "Grok verification failed")


def apply_ai_mismatches(mismatches: list[dict]) -> int:
    """Rewrite keyed answers in the AI JSON bank when Grok disagrees."""
    path = _unit_path(1)
    if not path.is_file() or not mismatches:
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    by_id = {row["id"]: row["grok"] for row in mismatches}
    changed = 0
    for item in data:
        qid = str(item.get("id", ""))
        if qid in by_id and item.get("answer") != by_id[qid]:
            item["answer"] = by_id[qid]
            item["answer_verified"] = "grok"
            changed += 1
    if changed:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Grok-verify Unit 1 questions the local checker skipped")
    parser.add_argument("--apply", action="store_true", help="Write Grok answers into the AI JSON bank")
    args = parser.parse_args()

    api_key = _load_api_key()
    if not api_key:
        print("XAI_API_KEY missing")
        return 1

    questions = collect_unverified_unit1_questions()
    print(f"Unverified seed questions: {len(questions)}", flush=True)
    report = _load_report()
    done = report["results"]
    pending = [q for q in questions if str(q.get("id")) not in done]
    print(f"Already checked: {len(done)}  remaining: {len(pending)}", flush=True)

    client = make_xai_client(api_key)
    for i in range(0, len(pending), BATCH_SIZE):
        batch = pending[i : i + BATCH_SIZE]
        print(f"  batch {i // BATCH_SIZE + 1}  {len(batch)}  {batch[0].get('id')}…", flush=True)
        try:
            answers = _verify_batch(client, batch)
        except Exception as exc:
            print(f"  FAILED batch: {exc}", flush=True)
            report["errors"][str(batch[0].get("id"))] = str(exc)
            _save_report(report)
            time.sleep(70)
            continue
        for q in batch:
            qid = str(q.get("id"))
            grok = answers.get(qid)
            keyed = q.get("answer")
            done[qid] = {
                "keyed": keyed,
                "grok": grok,
                "agree": grok == keyed,
                "category": q.get("category"),
                "source": q.get("source") or "base",
                "stem": str(q.get("question", ""))[:160],
                "keyed_opt": (q.get("options") or [None] * 4)[keyed] if isinstance(keyed, int) and keyed in range(4) else None,
                "grok_opt": (q.get("options") or [None] * 4)[grok] if isinstance(grok, int) else None,
            }
        _save_report(report)
        time.sleep(2)

    results = list(done.values())
    agree = sum(1 for r in results if r.get("agree"))
    disagree = [r for r in results if not r.get("agree")]
    print(f"\nChecked {len(results)}")
    print(f"Agree with key: {agree}")
    print(f"Disagree: {len(disagree)}")
    for row in disagree:
        print(f"  {row.get('stem', '')[:90]}")
        print(f"    keyed={row.get('keyed_opt')!r}")
        print(f"    grok ={row.get('grok_opt')!r}")

    fixed = 0
    if args.apply:
        ai_ids = {str(q.get("id")) for q in load_ai_bank(1)}
        ai_mismatches = []
        for qid, row in done.items():
            if qid in ai_ids and not row.get("agree") and isinstance(row.get("grok"), int):
                ai_mismatches.append({"id": qid, "grok": row["grok"]})
        fixed = apply_ai_mismatches(ai_mismatches)
        print(f"Applied {fixed} Grok answer-key fixes to unit_1.json")
    else:
        print("No keys rewritten (pass --apply to write Grok answers into the AI bank).")
    report["summary"] = {
        "checked": len(results),
        "agree": agree,
        "disagree": len(disagree),
        "ai_fixed": fixed,
    }
    _save_report(report)
    return 0 if not report.get("errors") else 0


if __name__ == "__main__":
    raise SystemExit(main())
