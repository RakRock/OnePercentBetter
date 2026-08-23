"""Build Harshit Chemistry Unit 1 practice sessions (15 MCQs from question bank)."""

from __future__ import annotations

import os
import random

import database as db
from . import content as hpc
from . import questions as hpq
from . import topics as hpt
from practice_quality.assembler import qa_and_assemble
from practice_quality.report import build_learning_report

DEFAULT_QUESTION_COUNT = 15


def _active_slots(unit_id: int, config: dict) -> list[tuple[int, str]]:
    slots: list[tuple[int, str]] = []
    topics = hpt.topics_for_unit(unit_id)
    for item in config.get("topics", []):
        did = int(item["id"])
        for lvl in item.get("levels", []):
            if did in topics and lvl in topics[did]["levels"]:
                slots.append((did, lvl))
    return slots


def _slot_plan(unit_id: int, config: dict, count: int) -> list[tuple[int, str]]:
    slots = _active_slots(unit_id, config)
    if not slots:
        return []
    cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(cycle)
    return cycle[:count]


def _slot_dict(unit_id: int, day_id: int, level: str) -> dict:
    return {
        "unit_id": unit_id,
        "day_id": day_id,
        "topic": day_id,
        "level": level,
        "category": f"u1_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(unit_id, day_id, level),
        "question_type": "mcq",
    }


def _generate_for_slot(slot: dict, used_ids: set[str], seen_fps: set[str]) -> dict | None:
    unit_id = int(slot.get("unit_id", hpc.UNIT_ID))
    day_id = int(slot["day_id"])
    level = str(slot["level"])
    q = hpq.pick_question(
        unit_id,
        day_id,
        level,
        exclude_ids=used_ids,
        exclude_text=seen_fps,
    )
    if q:
        q = dict(q)
        q.setdefault("category", slot["category"])
        q.setdefault("category_label", slot["category_label"])
    return q


def apply_practice_difficulty(config: dict) -> dict:
    unit_id = int(config.get("unit_id", hpc.UNIT_ID))
    topics = config.get("topics") or []
    if topics:
        return config
    diff = int(config.get("practice_difficulty", 3))
    level_map = {1: "A", 2: "A", 3: "B", 4: "C", 5: "C"}
    level = level_map.get(diff, "B")
    all_topics = hpt.topics_for_unit(unit_id)
    return {
        **config,
        "topics": [{"id": did, "levels": [level]} for did in sorted(all_topics)],
    }


def build_session_set(
    unit_id: int,
    config: dict,
    count: int = DEFAULT_QUESTION_COUNT,
    *,
    user_id: int | None = None,
    xai_api_key: str | None = None,
) -> tuple[list[dict], str]:
    config = apply_practice_difficulty({**config, "unit_id": unit_id})
    if not _active_slots(unit_id, config):
        return [], "Select topics in Practice Setup."

    prefer_llm = bool(config.get("use_chapter_llm", False))
    fresh_only = bool(config.get("grok_fresh_only", False))
    api_key = xai_api_key or os.environ.get("XAI_API_KEY", "").strip() or None
    grok_error = ""

    used_ids: set[str] = set()
    seen_fps: set[str] = set()
    if user_id:
        ec3_unit = hpc.SESSION_UNIT_OFFSET + unit_id
        used_ids.update(db.get_recent_ec3_question_ids(user_id, ec3_unit, sessions=6))

    plan = _slot_plan(unit_id, config, count)
    slot_dicts = [_slot_dict(unit_id, did, lvl) for did, lvl in plan]
    initial: list[dict | None] = [None] * len(slot_dicts)

    if prefer_llm and api_key:
        from . import llm as hpll

        try:
            batch = hpll.generate_session_questions_raw(api_key, unit_id, config, count)
            for i, q in enumerate(batch[: len(slot_dicts)]):
                initial[i] = q
        except ValueError as exc:
            grok_error = str(exc)

    if fresh_only and prefer_llm and api_key:
        filled = [q for q in initial if q]
        if len(filled) < count:
            return filled[:count], grok_error or f"Only {len(filled)} of {count} from Grok."
        random.shuffle(filled)
        return filled[:count], grok_error

    try:
        questions = qa_and_assemble(
            slot_dicts,
            _generate_for_slot,
            initial=initial,
            exclude_ids=used_ids,
            exclude_keys=seen_fps,
            program="harshit",
        )
    except ValueError as exc:
        grok_error = grok_error or str(exc)
        questions = []
        for i, slot in enumerate(slot_dicts):
            q = initial[i] if i < len(initial) and initial[i] else _generate_for_slot(slot, used_ids, seen_fps)
            if q:
                questions.append(q)

    random.shuffle(questions)
    out = questions[:count]
    if prefer_llm and api_key and not out and grok_error:
        return [], grok_error
    if prefer_llm and api_key and len(out) < count and grok_error:
        return out, grok_error
    return out, grok_error if prefer_llm and api_key and grok_error else ""


def build_session_report(
    questions: list[dict],
    answers: list[dict],
    *,
    student_name: str = "Student",
) -> dict:
    return build_learning_report(questions, answers, student_name=student_name, program="harshit")


def session_meta_from_config(unit_id: int, config: dict) -> dict:
    return {
        "unit_id": unit_id,
        "week_label": config.get("week_label", ""),
        "topics": config.get("topics", []),
        "use_chapter_llm": config.get("use_chapter_llm", False),
    }


def format_report_details(report: dict) -> str:
    lines = [f"Score: {report['correct_count']}/{report['total']} ({report['score_pct']}%)\n"]
    if report.get("strengths"):
        lines.append("Doing well:")
        for s in report["strengths"]:
            lines.append(f"  • {s['name']} — {s['correct']}/{s['total']}")
    if report.get("needs_revision"):
        lines.append("Needs revision:")
        for s in report["needs_revision"]:
            lines.append(f"  • {s['name']} — {s['correct']}/{s['total']}")
    return "\n".join(lines)
