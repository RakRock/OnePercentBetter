"""Default weekly practice plans for Arjun Edgenuity Course 3 Math."""

from __future__ import annotations

import arjun_course3_levels as c3lvl
import arjun_edgenuity_course3_content as ec3
import arjun_edgenuity_course3_practice as ec3p

DEFAULT_QUESTION_COUNT = 15

WEEKLY_GUIDANCE: dict[int, str] = {
    1: (
        "**Suggested pace:** One activity per day (Coordinate Plane → Functions → Graph Behavior → "
        "Linear Equations → Tables → Word Problems), then daily mixed practice."
    ),
    2: (
        "**Suggested pace:** Slope & Rate → Y-Intercept → Direct Variation → Special Lines → "
        "Writing Equations → Linear Modeling."
    ),
    3: (
        "**Suggested pace:** Point-slope → Slope-intercept → Standard form → Parallel & perpendicular → "
        "Writing from context → Modeling."
    ),
    4: (
        "**Suggested pace:** Scatter plots → Line of best fit → Association → Two-way tables → "
        "Categorical data → Predictions."
    ),
    5: (
        "**Suggested pace:** One-step → Two-step → Variables both sides → Special cases → "
        "Word problems → Review."
    ),
    6: (
        "**Suggested pace:** Graphing systems → Substitution → Elimination → Special systems → "
        "Word problems → Mixed review."
    ),
}


def default_week_config(unit_id: int) -> dict:
    categories_meta = ec3p.get_categories(unit_id)
    unit = ec3.get_unit(unit_id)
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
    categories_meta = ec3p.get_categories(unit_id)
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
        lines.append("  • xAI (Grok): off — built-in question bank with graphs")
    return "\n".join(lines) if lines else "No topics selected."
