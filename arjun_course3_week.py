"""Default weekly practice plans for Arjun Course 3 Math (textbook track)."""

from __future__ import annotations

import arjun_course3_content as c3
import arjun_course3_levels as c3lvl
import arjun_course3_practice as c3p

DEFAULT_QUESTION_COUNT = c3p.DEFAULT_SESSION_COUNT

WEEKLY_GUIDANCE: dict[int, str] = {
    1: (
        "**Suggested pace (2 weeks):** Week 1 — Patterns, Fractions, Powers & Roots, Rational Numbers. "
        "Week 2 — Irrational Numbers, Exponents, Scientific Notation, Sci Notation Ops. "
        "Do one activity's notes, then the matching topic quiz."
    ),
    2: (
        "**Suggested pace:** Mon Expressions → Tue Solving Equations → Wed Slope → "
        "Thu Slope-Intercept → Fri Proportional + Systems review. End with full unit practice."
    ),
    3: (
        "**Suggested pace:** Angles → Transformations → Similarity → Pythagorean → "
        "Surface Area → Volume (one topic per day), then mixed unit practice."
    ),
    4: (
        "**Suggested pace:** Function basics → Comparing → Constructing → Linear functions → "
        "Linear vs nonlinear. Pair each activity with its topic quiz."
    ),
    5: (
        "**Suggested pace:** Scatter & association → Bivariate data → MAD → Two-way tables. "
        "Finish with a full 15-question unit review."
    ),
}


def default_week_config(unit_id: int) -> dict:
    categories_meta = c3p.get_categories(unit_id)
    unit = c3.get_unit(unit_id)
    title = unit["title"] if unit else f"Unit {unit_id}"
    topics = [
        {"id": cat_id, "levels": list(c3lvl.DEFAULT_LEVELS)}
        for cat_id in categories_meta
    ]
    return {
        "week_label": f"{title} — Week 1",
        "topics": topics,
        "categories": list(categories_meta.keys()),
        "question_count": DEFAULT_QUESTION_COUNT,
        "use_llm": False,
        "unit_id": unit_id,
    }


def weekly_guidance(unit_id: int) -> str:
    return WEEKLY_GUIDANCE.get(
        unit_id,
        "Select topics and difficulty levels for this week, then start daily practice.",
    )


def format_week_plan_summary(unit_id: int, config: dict) -> str:
    categories_meta = c3p.get_categories(unit_id)
    valid = set(categories_meta.keys())
    normalized = c3lvl.normalize_week_config(config, valid, unit_id=unit_id)
    lines: list[str] = []
    if normalized.get("week_label"):
        lines.append(f"Week: {normalized['week_label']}")
    for item in normalized.get("topics") or []:
        cat_id = str(item.get("id", ""))
        info = categories_meta.get(cat_id, {})
        lvls = ", ".join(item.get("levels") or [])
        lines.append(f"  • {info.get('emoji', '')} {info.get('name', cat_id)} [{lvls}]")
    lines.append(f"  • Questions per session: {DEFAULT_QUESTION_COUNT}")
    if normalized.get("use_llm"):
        lines.append("  • xAI (Grok): on — fresh questions each session")
    else:
        lines.append("  • xAI (Grok): off — built-in question bank")
    return "\n".join(lines) if lines else "No topics selected."
