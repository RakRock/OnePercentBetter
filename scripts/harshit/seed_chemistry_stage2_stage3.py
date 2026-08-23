#!/usr/bin/env python3
"""Seed Harshit Chemistry units 1–4 Stage 2/3 ncert_source.json and exercise_bank.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.harshit.chemistry_stage2_stage3_data import UNIT_DATA  # noqa: E402


def _write_ncert(unit_id: int, pack: dict) -> Path:
    out = ROOT / "HarshitChemistry" / f"unit{unit_id}" / "ncert_source.json"
    payload = {
        "meta": pack["meta"],
        "activities": pack["activities"],
        "exercise_mcqs": pack["exercise_mcqs"],
        "intext_samples": pack["intext_samples"],
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def _write_exercise_bank(unit_id: int, pack: dict) -> Path:
    out = ROOT / "HarshitChemistry" / f"unit{unit_id}" / "exercise_bank.json"
    meta = dict(pack["exercise_meta"])
    meta["unit_id"] = unit_id
    payload = {
        "meta": meta,
        "questions": pack["exercises"],
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> None:
    summary: list[str] = []
    for unit_id in sorted(UNIT_DATA):
        pack = UNIT_DATA[unit_id]
        ncert_path = _write_ncert(unit_id, pack)
        ex_path = _write_exercise_bank(unit_id, pack)
        n_acts = len(pack["activities"])
        n_mcqs = len(pack["exercise_mcqs"])
        n_intext = len(pack["intext_samples"])
        n_written = len(pack["exercises"])
        summary.append(
            f"Unit {unit_id}: {ncert_path.name} "
            f"({n_acts} activities, {n_mcqs} exercise MCQs, {n_intext} intext) + "
            f"{ex_path.name} ({n_written} written Qs, {pack['exercise_meta']['range']})"
        )
        print(f"Wrote {ncert_path}")
        print(f"Wrote {ex_path}")

    print("\n--- Summary ---")
    for line in summary:
        print(line)


if __name__ == "__main__":
    main()
