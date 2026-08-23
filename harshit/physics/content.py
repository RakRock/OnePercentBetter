"""Harshit Physics — multi-unit content loader (NCERT Class 10)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

UNITS: dict[int, dict] = {
    1: {
        "dir": "unit1",
        "title": "Light – Reflection and Refraction",
        "ncert": "Class 10 Science, Chapter 9",
        "pdf": "jesc109.pdf",
        "session_kind_concepts": "harshit_physics_unit1_concepts",
        "session_kind_mcq": "harshit_physics_unit1_mcq",
        "chapter_ref": "NCERT Class 10 Ch 9 — Light",
    },
    2: {
        "dir": "unit2",
        "title": "The Human Eye and the Colourful World",
        "ncert": "Class 10 Science, Chapter 10",
        "pdf": "jesc110.pdf",
        "session_kind_concepts": "harshit_physics_unit2_concepts",
        "session_kind_mcq": "harshit_physics_unit2_mcq",
        "chapter_ref": "NCERT Class 10 Ch 10 — Human Eye",
    },
    3: {
        "dir": "unit3",
        "title": "Electricity",
        "ncert": "Class 10 Science, Chapter 11",
        "pdf": "jesc111.pdf",
        "session_kind_concepts": "harshit_physics_unit3_concepts",
        "session_kind_mcq": "harshit_physics_unit3_mcq",
        "chapter_ref": "NCERT Class 10 Ch 11 — Electricity",
    },
    4: {
        "dir": "unit4",
        "title": "Magnetic Effects of Electric Current",
        "ncert": "Class 10 Science, Chapter 12",
        "pdf": "jesc112.pdf",
        "session_kind_concepts": "harshit_physics_unit4_concepts",
        "session_kind_mcq": "harshit_physics_unit4_mcq",
        "chapter_ref": "NCERT Class 10 Ch 12 — Magnetism",
    },
}

STUDENT_NAME = "Harshit Sai"
SESSION_UNIT_OFFSET = 300

# Backward-compatible defaults (Unit 1)
UNIT_ID = 1
UNIT_TITLE = UNITS[1]["title"]
UNIT1_DIR = ROOT / "HarshitPhysics" / "unit1"
SESSION_KIND_CONCEPTS = UNITS[1]["session_kind_concepts"]
SESSION_KIND_MCQ = UNITS[1]["session_kind_mcq"]


def unit_dir(unit_id: int) -> Path:
    if unit_id not in UNITS:
        raise ValueError(f"Unknown physics unit_id: {unit_id}")
    return ROOT / "HarshitPhysics" / UNITS[unit_id]["dir"]


def active_unit_id() -> int:
    try:
        import streamlit as st

        return int(st.session_state.get("hp_unit_id", UNIT_ID))
    except Exception:
        return UNIT_ID


def unit_meta(unit_id: int | None = None) -> dict:
    uid = unit_id if unit_id is not None else active_unit_id()
    return dict(UNITS[uid])


def session_kinds(unit_id: int) -> tuple[str, str]:
    u = UNITS[unit_id]
    return u["session_kind_concepts"], u["session_kind_mcq"]


def _load_json(unit_id: int, name: str) -> dict:
    path = unit_dir(unit_id) / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def logic_schema(unit_id: int | None = None) -> dict:
    return _load_json(unit_id or active_unit_id(), "logic_schema.json")


def error_state_machines(unit_id: int | None = None) -> dict:
    return _load_json(unit_id or active_unit_id(), "error_state_machines.json")


def component_specs(unit_id: int | None = None) -> dict:
    return _load_json(unit_id or active_unit_id(), "component_specs.json")


def mcq_bank(unit_id: int | None = None) -> dict:
    return _load_json(unit_id or active_unit_id(), "mcq_bank.json")


def exercise_bank(unit_id: int | None = None) -> dict:
    path = unit_dir(unit_id or active_unit_id()) / "exercise_bank.json"
    if not path.is_file():
        return {"questions": [], "meta": {}}
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"questions": [], "meta": {}}


def list_exercise_questions(unit_id: int | None = None) -> list[dict]:
    return list(exercise_bank(unit_id).get("questions") or [])


def get_exercise_question(question_id: str, unit_id: int | None = None) -> dict | None:
    return next(
        (q for q in list_exercise_questions(unit_id) if q.get("id") == question_id),
        None,
    )


def get_exercise_question_by_num(num: int, unit_id: int | None = None) -> dict | None:
    return next(
        (q for q in list_exercise_questions(unit_id) if int(q.get("num", 0)) == num),
        None,
    )


def stage3_available(unit_id: int | None = None) -> bool:
    bank = exercise_bank(unit_id)
    if not bank.get("meta", {}).get("active"):
        return False
    return bool(list_exercise_questions(unit_id))


def stage3_unlocked(viewed_ids: set[str], unit_id: int | None = None) -> bool:
    return practice_unlocked(viewed_ids, unit_id=unit_id)


def ncert_source(unit_id: int | None = None) -> dict:
    path = unit_dir(unit_id or active_unit_id()) / "ncert_source.json"
    if not path.is_file():
        return {"activities": [], "exercise_mcqs": []}
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"activities": [], "exercise_mcqs": []}


def list_ncert_activities(unit_id: int | None = None) -> list[dict]:
    return list(ncert_source(unit_id).get("activities") or [])


def ncert_activities_for_stage2_day(stage2_day: int, unit_id: int | None = None) -> list[dict]:
    return [
        a
        for a in list_ncert_activities(unit_id)
        if int(a.get("stage2_day", 0)) == stage2_day
    ]


def stage2_available(unit_id: int | None = None) -> bool:
    bank = mcq_bank(unit_id)
    if not bank.get("meta", {}).get("active"):
        return False
    return any((s.get("questions") or []) for s in bank.get("sessions") or [])


def questions_for_mcq_day(day_id: int, unit_id: int | None = None) -> list[dict]:
    session = get_mcq_session(day_id, unit_id)
    if not session:
        return []
    return list(session.get("questions") or [])


def meta(unit_id: int | None = None) -> dict:
    return logic_schema(unit_id).get("meta", {})


def glossary(unit_id: int | None = None) -> list[dict]:
    return logic_schema(unit_id).get("glossary", [])


def list_days(*, stage: int | None = None, unit_id: int | None = None) -> list[dict]:
    days = logic_schema(unit_id).get("days", [])
    if stage is not None:
        days = [d for d in days if d.get("stage") == stage]
    return days


def get_day(day_id: int, unit_id: int | None = None) -> dict | None:
    return next((d for d in list_days(unit_id=unit_id) if d["day"] == day_id), None)


def concepts_for_day(day_id: int, unit_id: int | None = None) -> list[dict]:
    day = get_day(day_id, unit_id=unit_id)
    return list(day.get("concepts") or []) if day else []


def get_concept(concept_id: str, unit_id: int | None = None) -> dict | None:
    for day in list_days(unit_id=unit_id):
        for c in day.get("concepts") or []:
            if c.get("id") == concept_id:
                return c
    return None


def concept_count_for_day(day_id: int, unit_id: int | None = None) -> int:
    return len(concepts_for_day(day_id, unit_id=unit_id))


def total_concept_cards(*, active_only: bool = False, unit_id: int | None = None) -> int:
    total = 0
    for day in list_days(stage=1, unit_id=unit_id):
        if active_only and not day.get("active"):
            continue
        total += len(day.get("concepts") or [])
    return total


def list_mcq_sessions(unit_id: int | None = None) -> list[dict]:
    return mcq_bank(unit_id).get("sessions", [])


def get_mcq_session(day_id: int, unit_id: int | None = None) -> dict | None:
    return next((s for s in list_mcq_sessions(unit_id) if s["day"] == day_id), None)


def misconception_machine(category: str, unit_id: int | None = None) -> dict | None:
    return error_state_machines(unit_id).get("machines", {}).get(category)


def css_variables_block(unit_id: int | None = None) -> str:
    specs = component_specs(unit_id)
    vars_dict = specs.get("css_variables", {})
    lines = [f"  {k}: {v};" for k, v in vars_dict.items()]
    return ":root {\n" + "\n".join(lines) + "\n}"


def stage1_complete(viewed_ids: set[str], unit_id: int | None = None) -> bool:
    """True when all non-stub concept cards have been viewed."""
    for day in list_days(stage=1, unit_id=unit_id):
        for c in day.get("concepts") or []:
            if c.get("stub"):
                continue
            if not day.get("active"):
                continue
            if c["id"] not in viewed_ids:
                return False
    return True


def _testing_practice_unlock_enabled() -> bool:
    import os

    if os.environ.get("HARSHIT_PHYSICS_UNLOCK_PRACTICE", "").strip().lower() in ("1", "true", "yes"):
        return True
    try:
        import streamlit as st

        return bool(st.secrets.get("HARSHIT_PHYSICS_UNLOCK_PRACTICE"))
    except Exception:
        return False


def practice_unlocked(viewed_ids: set[str], unit_id: int | None = None) -> bool:
    """Stage 1 complete, or testing bypass via HARSHIT_PHYSICS_UNLOCK_PRACTICE."""
    return stage1_complete(viewed_ids, unit_id=unit_id) or _testing_practice_unlock_enabled()


def stage2_unlocked(viewed_ids: set[str], unit_id: int | None = None) -> bool:
    return practice_unlocked(viewed_ids, unit_id=unit_id)
