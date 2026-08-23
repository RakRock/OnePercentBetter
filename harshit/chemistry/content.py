"""Harshit Chemistry — multi-unit content loader (NCERT Class 10)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

UNITS: dict[int, dict] = {
    1: {
        "dir": "unit1",
        "title": "Chemical Reactions and Equations",
        "ncert": "Class 10 Science, Chapter 1 (Chemistry)",
        "session_kind_concepts": "harshit_chemistry_unit1_concepts",
        "session_kind_mcq": "harshit_chemistry_unit1_mcq",
        "chapter_ref": "NCERT Class 10 Ch 1 — Chemical Reactions and Equations",
        "pdf": "jesc101.pdf",
    },
    2: {
        "dir": "unit2",
        "title": "Acids, Bases and Salts",
        "ncert": "Class 10 Science, Chapter 2 (Chemistry)",
        "session_kind_concepts": "harshit_chemistry_unit2_concepts",
        "session_kind_mcq": "harshit_chemistry_unit2_mcq",
        "chapter_ref": "NCERT Class 10 Ch 2 — Acids, Bases and Salts",
        "pdf": "jesc102.pdf",
    },
    3: {
        "dir": "unit3",
        "title": "Metals and Non-metals",
        "ncert": "Class 10 Science, Chapter 3 (Chemistry)",
        "session_kind_concepts": "harshit_chemistry_unit3_concepts",
        "session_kind_mcq": "harshit_chemistry_unit3_mcq",
        "chapter_ref": "NCERT Class 10 Ch 3 — Metals and Non-metals",
        "pdf": "jesc103.pdf",
    },
    4: {
        "dir": "unit4",
        "title": "Carbon and its Compounds",
        "ncert": "Class 10 Science, Chapter 4 (Chemistry)",
        "session_kind_concepts": "harshit_chemistry_unit4_concepts",
        "session_kind_mcq": "harshit_chemistry_unit4_mcq",
        "chapter_ref": "NCERT Class 10 Ch 4 — Carbon and its Compounds",
        "pdf": "jesc104.pdf",
    },
}

STUDENT_NAME = "Harshit Sai"
SESSION_UNIT_OFFSET = 400

# Backward-compatible defaults (Unit 1)
UNIT_ID = 1
UNIT_TITLE = UNITS[1]["title"]
UNIT1_DIR = ROOT / "HarshitChemistry" / "unit1"
SESSION_KIND_CONCEPTS = UNITS[1]["session_kind_concepts"]
SESSION_KIND_MCQ = UNITS[1]["session_kind_mcq"]


def unit_dir(unit_id: int) -> Path:
    if unit_id not in UNITS:
        raise ValueError(f"Unknown chemistry unit_id: {unit_id}")
    return ROOT / "HarshitChemistry" / UNITS[unit_id]["dir"]


def active_unit_id() -> int:
    try:
        import streamlit as st

        return int(st.session_state.get("hc_unit_id", UNIT_ID))
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

    if os.environ.get("HARSHIT_CHEMISTRY_UNLOCK_PRACTICE", "").strip().lower() in ("1", "true", "yes"):
        return True
    try:
        import streamlit as st

        return bool(st.secrets.get("HARSHIT_CHEMISTRY_UNLOCK_PRACTICE"))
    except Exception:
        return False


def practice_unlocked(viewed_ids: set[str], unit_id: int | None = None) -> bool:
    """Stage 1 complete, or testing bypass via HARSHIT_CHEMISTRY_UNLOCK_PRACTICE."""
    return stage1_complete(viewed_ids, unit_id=unit_id) or _testing_practice_unlock_enabled()


def stage2_unlocked(viewed_ids: set[str], unit_id: int | None = None) -> bool:
    return practice_unlocked(viewed_ids, unit_id=unit_id)
