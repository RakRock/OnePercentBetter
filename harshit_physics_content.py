"""Harshit Physics — Unit 1 content loader (NCERT Ch 9, Light)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UNIT1_DIR = ROOT / "HarshitPhysics" / "unit1"

UNIT_ID = 1
UNIT_TITLE = "Light – Reflection and Refraction"
STUDENT_NAME = "Harshit Sai"
SESSION_KIND_CONCEPTS = "harshit_physics_unit1_concepts"
SESSION_KIND_MCQ = "harshit_physics_unit1_mcq"
SESSION_UNIT_OFFSET = 300


def _load_json(name: str) -> dict:
    path = UNIT1_DIR / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def logic_schema() -> dict:
    return _load_json("logic_schema.json")


def error_state_machines() -> dict:
    return _load_json("error_state_machines.json")


def component_specs() -> dict:
    return _load_json("component_specs.json")


def mcq_bank() -> dict:
    return _load_json("mcq_bank.json")


def meta() -> dict:
    return logic_schema().get("meta", {})


def glossary() -> list[dict]:
    return logic_schema().get("glossary", [])


def list_days(*, stage: int | None = None) -> list[dict]:
    days = logic_schema().get("days", [])
    if stage is not None:
        days = [d for d in days if d.get("stage") == stage]
    return days


def get_day(day_id: int) -> dict | None:
    return next((d for d in list_days() if d["day"] == day_id), None)


def concepts_for_day(day_id: int) -> list[dict]:
    day = get_day(day_id)
    return list(day.get("concepts") or []) if day else []


def get_concept(concept_id: str) -> dict | None:
    for day in list_days():
        for c in day.get("concepts") or []:
            if c.get("id") == concept_id:
                return c
    return None


def concept_count_for_day(day_id: int) -> int:
    return len(concepts_for_day(day_id))


def total_concept_cards(*, active_only: bool = False) -> int:
    total = 0
    for day in list_days(stage=1):
        if active_only and not day.get("active"):
            continue
        total += len(day.get("concepts") or [])
    return total


def list_mcq_sessions() -> list[dict]:
    return mcq_bank().get("sessions", [])


def get_mcq_session(day_id: int) -> dict | None:
    return next((s for s in list_mcq_sessions() if s["day"] == day_id), None)


def misconception_machine(category: str) -> dict | None:
    return error_state_machines().get("machines", {}).get(category)


def css_variables_block() -> str:
    specs = component_specs()
    vars_dict = specs.get("css_variables", {})
    lines = [f"  {k}: {v};" for k, v in vars_dict.items()]
    return ":root {\n" + "\n".join(lines) + "\n}"


def stage1_complete(viewed_ids: set[str]) -> bool:
    """True when all non-stub concept cards have been viewed."""
    for day in list_days(stage=1):
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


def practice_unlocked(viewed_ids: set[str]) -> bool:
    """Stage 1 complete, or testing bypass via HARSHIT_PHYSICS_UNLOCK_PRACTICE."""
    return stage1_complete(viewed_ids) or _testing_practice_unlock_enabled()


def stage2_unlocked(viewed_ids: set[str]) -> bool:
    return practice_unlocked(viewed_ids)
