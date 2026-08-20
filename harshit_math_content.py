"""Harshit Math — Phase 1 content loader (NCERT Class 9 Ch 1, Days 1–10)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHASE1_DIR = ROOT / "HarshitMath" / "phase1"

PHASE_ID = "phase1"
PHASE_TITLE = "Number Sense"
STUDENT_NAME = "Harshit Sai"
SESSION_UNIT_OFFSET = 200  # Google Sheets / ec3 session id offset


def _load_json(name: str) -> dict:
    path = PHASE1_DIR / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def logic_schema() -> dict:
    return _load_json("logic_schema.json")


def error_state_machines() -> dict:
    return _load_json("error_state_machines.json")


def component_specs() -> dict:
    return _load_json("component_specs.json")


def list_days() -> list[dict]:
    return logic_schema()["days"]


def get_day(day_id: int) -> dict | None:
    return next((d for d in list_days() if d["day"] == day_id), None)


def get_state_machine(problem_id: str) -> dict | None:
    machines = error_state_machines().get("machines", {})
    return machines.get(problem_id)


def problems_for_day(day_id: int) -> list[dict]:
    day = get_day(day_id)
    if not day:
        return []
    prob = day.get("ncert_problem")
    return [prob] if prob else []


def problem_count_for_day(day_id: int) -> int:
    return len(problems_for_day(day_id))


def css_variables_block() -> str:
    specs = component_specs()
    vars_dict = specs.get("css_variables", {})
    lines = [f"  {k}: {v};" for k, v in vars_dict.items()]
    return ":root {\n" + "\n".join(lines) + "\n}"
