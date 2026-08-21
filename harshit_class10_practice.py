"""Build Class 10 unit practice sessions from weekly configuration."""

from __future__ import annotations

import os
import random

import harshit_class10_questions as h10q
import harshit_class10_topics as h10t

DEFAULT_QUESTION_COUNT = 15


def _active_slots(unit_id: int, config: dict) -> list[tuple[int, str]]:
    slots: list[tuple[int, str]] = []
    topics = h10t.topics_for_unit(unit_id)
    for item in config.get("topics", []):
        tid = int(item["id"])
        for lvl in item.get("levels", []):
            if tid in topics and lvl in topics[tid]["levels"]:
                slots.append((tid, lvl))
    return slots


def _slot_plan(unit_id: int, config: dict, count: int) -> list[tuple[int, str]]:
    slots = _active_slots(unit_id, config)
    if not slots:
        return []
    cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(cycle)
    return cycle[:count]


def _generate_one(
    unit_id: int,
    topic_id: int,
    level: str,
    used_ids: set[str],
    used_keys: set[str],
) -> dict | None:
    q = h10q.pick_question(
        unit_id,
        topic_id,
        level,
        exclude_ids=used_ids,
        exclude_text=used_keys,
    )
    if q:
        return q
    return h10t.generate_question(
        unit_id,
        topic_id,
        level,
        exclude_ids=used_ids,
        exclude_text=used_keys,
        templates_only=False,
    )


def _fill_from_bank(
    unit_id: int,
    config: dict,
    count: int,
    *,
    used_ids: set[str] | None = None,
    used_keys: set[str] | None = None,
) -> list[dict]:
    used_ids = used_ids or set()
    used_keys = used_keys or set()
    selected: list[dict] = []
    cycle = _slot_plan(unit_id, config, count)
    if not cycle:
        return []

    for tid, lvl in cycle:
        if len(selected) >= count:
            break
        for attempt in range(40):
            q = _generate_one(unit_id, tid, lvl, used_ids, used_keys)
            if not q and attempt >= 24:
                q = h10t.generate_question(unit_id, tid, lvl, templates_only=True)
            if not q:
                continue
            key = h10q.question_dedup_key(str(q.get("question", "")), q.get("options"))
            if str(q.get("id", "")) in used_ids or key in used_keys:
                continue
            selected.append(q)
            used_ids.add(str(q["id"]))
            used_keys.add(key)
            break

    slots = _active_slots(unit_id, config)
    while len(selected) < count and slots:
        added_any = False
        for tid, lvl in slots:
            if len(selected) >= count:
                break
            for _ in range(30):
                q = h10t.generate_question(
                    unit_id, tid, lvl, exclude_ids=used_ids, exclude_text=used_keys, templates_only=True
                )
                if not q:
                    continue
                key = h10q.question_dedup_key(str(q.get("question", "")), q.get("options"))
                if str(q.get("id", "")) in used_ids or key in used_keys:
                    continue
                selected.append(q)
                used_ids.add(str(q["id"]))
                used_keys.add(key)
                added_any = True
                break
        if not added_any:
            break

    random.shuffle(selected)
    return selected[:count]


def apply_practice_difficulty(config: dict) -> dict:
    """Expand practice_difficulty (1–5) into topic level selections when topics empty."""
    unit_id = int(config.get("unit_id", 1))
    topics = config.get("topics") or []
    if topics:
        return config
    diff = int(config.get("practice_difficulty", 3))
    level = h10t.DIFFICULTY_TO_LEVEL.get(diff, "C")
    all_topics = h10t.topics_for_unit(unit_id)
    return {
        **config,
        "topics": [{"id": tid, "levels": [level]} for tid in sorted(all_topics)],
    }


def build_session_set(
    unit_id: int,
    config: dict,
    count: int = DEFAULT_QUESTION_COUNT,
    *,
    xai_api_key: str | None = None,
) -> tuple[list[dict], str]:
    config = apply_practice_difficulty({**config, "unit_id": unit_id})
    if not _active_slots(unit_id, config):
        return [], "Select topics and levels in Week Setup."

    prefer_llm = bool(config.get("use_chapter_llm", True))
    fresh_only = bool(config.get("grok_fresh_only", False))
    api_key = xai_api_key or os.environ.get("XAI_API_KEY", "").strip() or None
    grok_error = ""
    used_ids: set[str] = set()
    used_keys: set[str] = set()
    questions: list[dict] = []

    if prefer_llm and api_key:
        import harshit_class10_llm as h10llm

        try:
            batch = h10llm.generate_session_questions_raw(api_key, unit_id, config, count)
            for q in batch:
                key = h10q.question_dedup_key(str(q.get("question", "")), q.get("options"))
                if str(q.get("id", "")) in used_ids or key in used_keys:
                    continue
                questions.append(q)
                used_ids.add(str(q["id"]))
                used_keys.add(key)
        except ValueError as exc:
            grok_error = str(exc)

    if not fresh_only and len(questions) < count:
        extra = _fill_from_bank(
            unit_id,
            config,
            count - len(questions),
            used_ids=used_ids,
            used_keys=used_keys,
        )
        questions.extend(extra)

    if prefer_llm and api_key and fresh_only and len(questions) < count:
        return questions[:count], grok_error or f"Only {len(questions)} of {count} from Grok."

    random.shuffle(questions)
    return questions[:count], grok_error if prefer_llm and api_key and not questions else ""


def build_session_report(questions: list[dict], answers: list[dict], *, student_name: str = "Student") -> dict:
    total = len(questions)
    correct = sum(1 for a in answers if a.get("correct"))
    by_cat: dict[str, dict] = {}
    for q, a in zip(questions, answers):
        label = q.get("category_label", q.get("category", ""))
        bucket = by_cat.setdefault(label, {"name": label, "correct": 0, "total": 0})
        bucket["total"] += 1
        if a.get("correct"):
            bucket["correct"] += 1

    strengths = []
    needs = []
    for item in by_cat.values():
        pct = round(100 * item["correct"] / item["total"]) if item["total"] else 0
        row = {**item, "pct": pct, "emoji": "✅" if pct >= 80 else "📚"}
        if pct >= 80:
            strengths.append(row)
        elif pct < 60:
            needs.append(row)

    return {
        "student": student_name,
        "total": total,
        "correct_count": correct,
        "score_pct": round(100 * correct / total) if total else 0,
        "strengths": strengths,
        "needs_revision": needs,
    }


def session_meta_from_config(unit_id: int, config: dict) -> dict:
    return {
        "unit_id": unit_id,
        "week_label": config.get("week_label", ""),
        "topics": config.get("topics", []),
        "use_chapter_llm": config.get("use_chapter_llm", True),
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
