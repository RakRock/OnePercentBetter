#!/usr/bin/env python3
"""Build Harshit Physics Unit 2 logic_schema.json (160 concept cards, Days 1–16)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.physics_unit2_content import DAY_BUILDERS, DAY_TITLES  # noqa: E402

OUT = ROOT / "HarshitPhysics" / "unit2" / "logic_schema.json"


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
            "unit_id": 2,
            "unit_title": "The Human Eye and the Colourful World",
            "ncert": "Class 10 Science, Chapter 10",
            "stage1_days": 16,
            "stage2_days": 4,
            "concept_cards_total": 160,
            "mcq_total": 40,
            "release_active": 4,
            "session_kind_concepts": "harshit_physics_unit2_concepts",
            "session_kind_mcq": "harshit_physics_unit2_mcq",
        },
        "glossary": [
            {"term": "accommodation", "definition": "Ability of eye lens to adjust focal length for near and far objects."},
            {"term": "near point", "definition": "Least distance of distinct vision; about 25 cm for normal young adult."},
            {"term": "far point", "definition": "Farthest distance for clear vision; infinity for normal eye."},
            {"term": "myopia", "definition": "Near-sightedness; distant objects blurred; image forms in front of retina."},
            {"term": "hypermetropia", "definition": "Far-sightedness; nearby objects blurred; image forms behind retina for close objects."},
            {"term": "presbyopia", "definition": "Age-related loss of accommodation; near point recedes."},
            {"term": "concave lens", "definition": "Diverging lens; corrects myopia."},
            {"term": "convex lens", "definition": "Converging lens; corrects hypermetropia."},
            {"term": "bifocal lens", "definition": "Upper concave for distance, lower convex for near vision."},
            {"term": "cataract", "definition": "Clouding of eye lens with age; surgery can restore vision."},
            {"term": "prism", "definition": "Transparent medium with two inclined refracting faces."},
            {"term": "angle of deviation", "definition": "Angle between emergent and incident ray directions in a prism."},
            {"term": "dispersion", "definition": "Splitting of white light into component colours."},
            {"term": "spectrum", "definition": "Band of colours from dispersed light; VIBGYOR order."},
            {"term": "rainbow", "definition": "Natural spectrum from sunlight dispersed by raindrops."},
            {"term": "atmospheric refraction", "definition": "Bending of light by Earth's atmosphere with changing density."},
            {"term": "twinkling", "definition": "Apparent flicker of stars due to atmospheric refraction."},
            {"term": "scattering", "definition": "Redirecting of light by particles; depends on wavelength and size."},
            {"term": "Tyndall effect", "definition": "Visible beam path when light scatters from colloidal particles."},
            {"term": "dioptre", "definition": "Unit of lens power; P = 1/f with f in metres."},
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
