#!/usr/bin/env python3
"""Build Harshit Physics Unit 4 logic_schema.json (160 concept cards, Days 1–16)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.harshit.physics_unit4_content import DAY_BUILDERS, DAY_TITLES  # noqa: E402

OUT = ROOT / "HarshitPhysics" / "unit4" / "logic_schema.json"


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
            "unit_id": 4,
            "unit_title": "Magnetic Effects of Electric Current",
            "ncert": "Class 10 Science, Chapter 12",
            "stage1_days": 16,
            "stage2_days": 4,
            "concept_cards_total": 160,
            "mcq_total": 40,
            "release_active": 4,
            "session_kind_concepts": "harshit_physics_unit4_concepts",
            "session_kind_mcq": "harshit_physics_unit4_mcq",
        },
        "glossary": [
            {"term": "magnetic field", "definition": "Region around a magnet where magnetic force on a pole can be detected."},
            {"term": "magnetic field lines", "definition": "Curves showing direction and strength of magnetic field; emerge from N, enter S."},
            {"term": "right-hand thumb rule", "definition": "Thumb along current; curled fingers give field direction around straight conductor."},
            {"term": "solenoid", "definition": "Cylinder-shaped coil of many closely wound turns of insulated copper wire."},
            {"term": "electromagnet", "definition": "Magnet formed by magnetising soft iron core inside current-carrying solenoid."},
            {"term": "Fleming's left-hand rule", "definition": "First finger B, second I, thumb F — mutually perpendicular."},
            {"term": "live wire", "definition": "Red-insulated mains wire at high potential (~220 V w.r.t. neutral)."},
            {"term": "neutral wire", "definition": "Black-insulated return wire at ~0 V reference."},
            {"term": "earth wire", "definition": "Green-insulated wire connected to ground for appliance safety."},
            {"term": "short circuit", "definition": "Direct contact of live and neutral causing abrupt high current."},
            {"term": "overloading", "definition": "Drawing current beyond safe limit due to too many appliances or voltage surge."},
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
