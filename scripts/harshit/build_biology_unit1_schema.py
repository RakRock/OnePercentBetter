#!/usr/bin/env python3
"""Build HarshitBiology/unit1/logic_schema.json (160 concept cards, Days 1–16)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.harshit.biology_unit1_content import DAY_BUILDERS, DAY_TITLES  # noqa: E402

OUT = ROOT / "HarshitBiology" / "unit1" / "logic_schema.json"


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
            "unit_id": 1,
            "unit_title": "Life Processes",
            "ncert": "Class 10 Science, Chapter 5 (Biology)",
            "stage1_days": 16,
            "stage2_days": 4,
            "concept_cards_total": 160,
            "mcq_total": 40,
            "release_active": 4,
            "session_kind_concepts": "harshit_biology_unit1_concepts",
            "session_kind_mcq": "harshit_biology_unit1_mcq",
        },
        "glossary": [
            {"term": "life processes", "definition": "Basic functions like nutrition, respiration, transport, and excretion that maintain life."},
            {"term": "nutrition", "definition": "Process of obtaining and using food for growth, repair, and energy."},
            {"term": "photosynthesis", "definition": "Synthesis of food in green plants using CO₂, water, and sunlight."},
            {"term": "autotrophic nutrition", "definition": "Organism makes its own food from inorganic substances."},
            {"term": "heterotrophic nutrition", "definition": "Organism depends on ready-made organic food from other organisms."},
            {"term": "respiration", "definition": "Release of energy from food inside cells, often using oxygen."},
            {"term": "aerobic respiration", "definition": "Respiration using oxygen; complete breakdown of glucose in mitochondria."},
            {"term": "anaerobic respiration", "definition": "Respiration without oxygen; partial breakdown with less ATP."},
            {"term": "xylem", "definition": "Vascular tissue transporting water and minerals upward in plants."},
            {"term": "phloem", "definition": "Vascular tissue transporting food (sucrose) in plants."},
            {"term": "excretion", "definition": "Removal of harmful metabolic wastes from the body."},
            {"term": "nephron", "definition": "Structural and functional unit of the kidney that filters blood and forms urine."},
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
