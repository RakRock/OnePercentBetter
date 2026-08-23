#!/usr/bin/env python3
"""Build Harshit Physics Unit 4 Stage 2 mcq_bank (40 MCQs, days 17–20)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import harshit.physics.questions as hpq  # noqa: E402

UNIT_ID = 4
CHAPTER_REF = "NCERT Class 10 Ch 12 — Magnetism"
OUT = ROOT / "HarshitPhysics" / "unit4" / "mcq_bank.json"
NCERT = ROOT / "HarshitPhysics" / "unit4" / "ncert_source.json"
QUESTIONS_PER_DAY = 10

SESSIONS = [
    (17, "Magnetic Fields and Field Lines", [1, 2], [1, 2, 3, 4]),
    (18, "Field due to Current in a Conductor", [], [4, 5, 6, 7]),
    (19, "Coils, Solenoids and Force on Conductor", [], [5, 6, 7, 8, 9]),
    (20, "Domestic Circuits and Safety", [], [10, 11, 12, 13, 14, 15, 16]),
]


def _load_ncert() -> dict:
    return json.loads(NCERT.read_text(encoding="utf-8"))


def _exercise_by_num(ncert: dict, num: int) -> dict | None:
    for ex in ncert.get("exercise_mcqs", []):
        if int(ex["num"]) == num:
            return ex
    return None


def _intext_questions(ncert: dict) -> list[dict]:
    return list(ncert.get("intext_samples") or [])


def _normalize_ncert(raw: dict, *, day_id: int, seq: int, prefix: str = "ncert") -> dict:
    return {
        "id": f"u4_d{day_id}_{prefix}_{seq:02d}",
        "question": raw["question"],
        "options": [str(o) for o in raw["options"]],
        "answer": int(raw["answer"]),
        "explanation": str(raw.get("explanation", "")),
        "misconception": raw.get("misconception", ""),
        "concept_id": (raw.get("concept_ids") or [""])[0] if raw.get("concept_ids") else "",
        "source": raw.get("source", "NCERT Ch 12"),
        "chapter_ref": CHAPTER_REF,
        "ncert_ref": raw.get("source") or raw.get("ref", ""),
    }


def _from_bank(day_id: int, level: str, seq: int, used_text: set[str]) -> dict | None:
    for raw in hpq.pool_for(day_id, level, UNIT_ID):
        key = hpq.question_dedup_key(str(raw.get("question", "")), raw.get("options"))
        if key in used_text:
            continue
        try:
            q = hpq.normalize_question(raw, UNIT_ID)
        except ValueError:
            continue
        used_text.add(key)
        out = dict(q)
        out["id"] = f"u4_s2_d{day_id}_bank_{seq:02d}"
        out["misconception"] = out.get("misconception") or _guess_misconception(out)
        out["source"] = "concept_bank"
        return out
    return None


def _fill_bank_questions(
    session_day: int,
    bank_days: list[int],
    need: int,
    used_text: set[str],
    start_seq: int,
) -> list[dict]:
    out: list[dict] = []
    seq = start_seq
    for src_day in bank_days:
        for lvl in ("B", "C", "A"):
            if len(out) >= need:
                return out
            q = _from_bank(src_day, lvl, seq, used_text)
            if q:
                out.append(q)
                seq += 1
    for src_day in range(1, 17):
        if len(out) >= need:
            break
        for lvl in ("B", "C", "A"):
            if len(out) >= need:
                break
            q = _from_bank(src_day, lvl, seq, used_text)
            if q:
                out.append(q)
                seq += 1
    return out


def _guess_misconception(q: dict) -> str:
    text = (q.get("question", "") + " " + q.get("explanation", "")).lower()
    if "fleming" in text or "left hand" in text or "right hand" in text:
        return "right_left_hand_rule_swap"
    if "field line" in text or "magnetic field" in text:
        return "field_lines_cross_or_open"
    if "domestic" in text or "parallel" in text and "appliance" in text:
        return "domestic_series_wiring_error"
    if "solenoid" in text or "coil" in text:
        return "solenoid_uniform_field_confusion"
    if "electron" in text or "conventional current" in text:
        return "electron_current_direction"
    if "short circuit" in text or "overload" in text or "fuse" in text:
        return "short_circuit_overload_confusion"
    if "earth" in text:
        return "earth_wire_purpose_error"
    if "straight wire" in text or "concentric" in text:
        return "straight_wire_field_pattern_error"
    return "right_left_hand_rule_swap"


def _build_session(
    day_id: int,
    title: str,
    exercise_nums: list[int],
    bank_days: list[int],
    ncert: dict,
    intext_pool: list[dict],
    used_bank: set[str],
) -> dict:
    questions: list[dict] = []
    seq = 1

    for num in exercise_nums:
        ex = _exercise_by_num(ncert, num)
        if ex:
            questions.append(_normalize_ncert(ex, day_id=day_id, seq=seq))
            seq += 1

    while intext_pool and len(questions) < QUESTIONS_PER_DAY:
        raw = intext_pool.pop(0)
        questions.append(_normalize_ncert(raw, day_id=day_id, seq=seq, prefix="intext"))
        seq += 1

    if len(questions) < QUESTIONS_PER_DAY:
        extra = _fill_bank_questions(
            day_id,
            bank_days,
            QUESTIONS_PER_DAY - len(questions),
            used_bank,
            seq,
        )
        questions.extend(extra)

    activity_ids = [
        a["id"]
        for a in ncert.get("activities", [])
        if int(a.get("stage2_day", 0)) == day_id
    ]
    return {
        "day": day_id,
        "title": title,
        "active": True,
        "activity_refs": activity_ids,
        "questions": questions[:QUESTIONS_PER_DAY],
    }


def main() -> None:
    ncert = _load_ncert()
    intext_pool = _intext_questions(ncert)
    used_bank: set[str] = set()
    sessions = []
    for day_id, title, ex_nums, bank_days in SESSIONS:
        sessions.append(
            _build_session(day_id, title, ex_nums, bank_days, ncert, intext_pool, used_bank)
        )

    total = sum(len(s["questions"]) for s in sessions)
    payload = {
        "meta": {
            "unit_id": UNIT_ID,
            "stage": 2,
            "active": True,
            "release": 5,
            "total_mcqs": total,
            "pdf": "jesc112.pdf",
            "note": "Stage 2: NCERT Exercises Q1–2 + Q3 T/F intext + concept bank. Activities 12.1–12.7 linked per day.",
        },
        "sessions": sessions,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} — {total} MCQs across {len(sessions)} sessions")


if __name__ == "__main__":
    main()
