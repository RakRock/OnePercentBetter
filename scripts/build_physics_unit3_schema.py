#!/usr/bin/env python3
"""Build Harshit Physics Unit 3 logic_schema.json (160 concept cards, Days 1–16)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.physics_unit3_content import DAY_BUILDERS, DAY_TITLES  # noqa: E402

OUT = ROOT / "HarshitPhysics" / "unit3" / "logic_schema.json"


def build_schema() -> dict:
    days = []
    for day_num in sorted(DAY_BUILDERS):
        days.append(
            {
                "day": day_num,
                "stage": 1,
                "title": DAY_TITLES[day_num],
                "active": True,
                "release": (day_num - 1) // 4 + 1,
                "concepts": DAY_BUILDERS[day_num](),
            }
        )

    return {
        "meta": {
            "student": "Harshit Sai",
            "unit_id": 3,
            "unit_title": "Electricity",
            "ncert": "Class 10 Science, Chapter 11",
            "stage1_days": 16,
            "stage2_days": 4,
            "concept_cards_total": 160,
            "mcq_total": 40,
            "release_active": 4,
            "session_kind_concepts": "harshit_physics_unit3_concepts",
            "session_kind_mcq": "harshit_physics_unit3_mcq",
        },
        "glossary": [
            {"term": "electric current", "definition": "Rate of flow of electric charge; I = Q/t; unit ampere (A)."},
            {"term": "coulomb", "definition": "SI unit of charge (C)."},
            {"term": "ampere", "definition": "SI unit of current; 1 A = 1 C/s."},
            {"term": "potential difference", "definition": "Work done per unit charge; V = W/Q; unit volt (V)."},
            {"term": "volt", "definition": "SI unit of potential difference; 1 V = 1 J/C."},
            {"term": "Ohm's law", "definition": "V = IR for metallic conductor at constant temperature."},
            {"term": "resistance", "definition": "Opposition to current; R = V/I; unit ohm (Ω)."},
            {"term": "ohm", "definition": "SI unit of resistance."},
            {"term": "resistivity", "definition": "Material property ρ; R = ρl/A; unit Ω m."},
            {"term": "rheostat", "definition": "Variable resistor used to control current."},
            {"term": "series", "definition": "Components end to end; same current; R adds."},
            {"term": "parallel", "definition": "Components across same two points; same V; reciprocals add."},
            {"term": "heating effect", "definition": "Heat produced when current flows through resistor."},
            {"term": "Joule's law", "definition": "H = I²Rt."},
            {"term": "electric power", "definition": "P = VI = I²R = V²/R; unit watt (W)."},
            {"term": "watt", "definition": "SI unit of power; 1 W = 1 V·A."},
            {"term": "kilowatt-hour", "definition": "Commercial energy unit; 1 kWh = 3.6×10⁶ J."},
            {"term": "ammeter", "definition": "Measures current; connected in series."},
            {"term": "voltmeter", "definition": "Measures potential difference; connected in parallel."},
            {"term": "fuse", "definition": "Safety device that melts to break circuit on overcurrent."},
        ],
        "days": days,
    }


def main() -> None:
    schema = build_schema()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    active_cards = sum(len(d["concepts"]) for d in schema["days"] if d.get("active"))
    print(f"Wrote {OUT} — {active_cards} active concept cards (Days 1–16)")


if __name__ == "__main__":
    main()
