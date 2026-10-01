"""Default weekly practice plans for Arjun Course 3 Math (textbook track)."""

from __future__ import annotations

import arjun_course3_content as c3
import arjun_course3_levels as c3lvl
import arjun_course3_practice as c3p

DEFAULT_QUESTION_COUNT = c3p.DEFAULT_SESSION_COUNT

WEEKLY_GUIDANCE: dict[int, str] = {
    1: (
        "**School worksheets load by default** (13 of every 15 questions). "
        "Stems match the teacher packet: rewrite/simplify, nested “of … of …”, convert, estimate, order, "
        "and “Was ___ correct?”. Scientific notation is off until class gets there. "
        "Packet III, Exponent Properties IV, and 1st-quarter BootCamp review "
        "are in the mix. Use **Reset to school packet (through 9/30)** if the week plan was customized."
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
    school = school_packet_week_config(unit_id)
    if school:
        return school
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


def school_packet_week_config(unit_id: int) -> dict | None:
    """Preset matching the teacher worksheets Arjun brought in (Course 3 through 9/30)."""
    if unit_id != 1:
        return None
    from arjun_course3_unit1_school_packet import SCHOOL_PACKET_LABEL, SCHOOL_PACKET_TOPICS

    return {
        "week_label": SCHOOL_PACKET_LABEL,
        "topics": [dict(t) for t in SCHOOL_PACKET_TOPICS],
        "categories": [t["id"] for t in SCHOOL_PACKET_TOPICS],
        "question_count": DEFAULT_QUESTION_COUNT,
        "school_packet_count": c3p.DEFAULT_SCHOOL_PACKET_COUNT,
        "use_llm": False,
        "unit_id": unit_id,
    }


def should_refresh_unit1_school_plan(config: dict | None) -> bool:
    """True when Unit 1 should load/replace the saved week plan with the school packet."""
    school = school_packet_week_config(1)
    if not school:
        return False
    if not config:
        return True
    topics = config.get("topics") or []
    if not topics:
        return True
    label = str(config.get("week_label") or "")
    if label == school["week_label"]:
        school_ids = {str(t.get("id")) for t in school["topics"]}
        saved_ids = {str(t.get("id")) for t in topics if isinstance(t, dict)}
        return saved_ids != school_ids
    if "school packet" in label.lower():
        return True
    topic_ids = {str(t.get("id")) for t in topics if isinstance(t, dict)}
    if "scientific_notation" in topic_ids or "sci_notation_ops" in topic_ids:
        return True
    if "week 1" in label.lower() and "school packet" not in label.lower():
        return True
    return False


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
    session_n = int(normalized.get("question_count") or DEFAULT_QUESTION_COUNT)
    lines.append(f"  • Questions per session: {session_n}")
    school_n = c3p.resolved_school_packet_count(normalized, count=session_n, unit_id=unit_id)
    if school_n:
        lines.append(f"  • School packet: {school_n} of {session_n} questions")
    if normalized.get("use_llm"):
        lines.append("  • xAI (Grok): on — fresh questions each session")
    else:
        lines.append("  • xAI (Grok): off — built-in question bank")
    return "\n".join(lines) if lines else "No topics selected."
