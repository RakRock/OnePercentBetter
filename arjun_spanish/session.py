"""Build Spanish practice sessions (bank + Grok + AI store)."""

from __future__ import annotations

import os
import random

import database as db
from arjun_spanish import bank as esbank
from arjun_spanish import config as escfg
from arjun_spanish import content as es
from arjun_spanish import store as esstore
from practice_quality.assembler import qa_and_assemble
from practice_quality.report import build_learning_report


def _active_topics(config: dict) -> list[str]:
    allowed = {t["id"] for t in es.TOPICS}
    topics = [t for t in config.get("topics", []) if t in allowed]
    return topics or es.school_topic_ids()


def _slot_plan(config: dict, count: int) -> list[dict]:
    topics = _active_topics(config)
    if not topics:
        return []
    directions = ("es_en", "en_es")
    cycle: list[dict] = []
    for i in range(count):
        topic_id = topics[i % len(topics)]
        direction = directions[i % len(directions)]
        topic = es.topic_by_id(topic_id)
        cycle.append(
            {
                "topic_id": topic_id,
                "direction": direction,
                "category": topic_id,
                "category_label": f"{topic.get('emoji', '')} {topic['title']}".strip(),
            }
        )
    random.shuffle(cycle)
    return cycle


def _generate_for_slot(slot: dict, used_ids: set[str], seen_fps: set[str]) -> dict | None:
    topic_id = slot["topic_id"]
    direction = slot["direction"]
    q = esstore.pick_ai_question(topic_id, used_ids=used_ids, seen_fps=seen_fps)
    if q:
        q = dict(q)
        q.setdefault("source", "ai_bank")
        return q
    return esbank.pick_bank_question(
        topic_id,
        direction,
        used_ids=used_ids,
        seen_fps=seen_fps,
    )


def build_session_set(
    config: dict | None = None,
    *,
    count: int | None = None,
    user_id: int | None = None,
    xai_api_key: str | None = None,
) -> tuple[list[dict], str]:
    cfg = escfg.ensure_config() if config is None else {**escfg.ensure_config(), **config}
    question_count = int(count or cfg.get("question_count") or es.DEFAULT_SESSION_COUNT)
    prefer_llm = bool(cfg.get("use_llm", False))
    fresh_only = bool(cfg.get("grok_fresh_only", False))
    api_key = xai_api_key or os.environ.get("XAI_API_KEY", "").strip() or None
    grok_error = ""

    slots = _slot_plan(cfg, question_count)
    if not slots:
        return [], "Select at least one topic in Practice Setup."

    used_ids: set[str] = set()
    seen_fps: set[str] = set()
    if user_id:
        used_ids.update(
            db.get_recent_ec3_question_ids(
                user_id,
                es.SESSION_UNIT_OFFSET,
                es.RECENT_SESSIONS_TO_AVOID,
            )
        )

    initial: list[dict | None] = [None] * len(slots)
    if prefer_llm and api_key:
        from arjun_spanish import llm as esllm

        try:
            batch = esllm.generate_session_questions_raw(api_key, slots)
            for i, q in enumerate(batch[: len(slots)]):
                initial[i] = q
        except ValueError as exc:
            grok_error = str(exc)

    if fresh_only and prefer_llm and api_key:
        filled = [q for q in initial if q]
        if len(filled) < question_count:
            return filled[:question_count], grok_error or f"Only {len(filled)} of {question_count} from Grok."
        random.shuffle(filled)
        return filled[:question_count], grok_error

    try:
        questions = qa_and_assemble(
            slots,
            _generate_for_slot,
            initial=initial,
            exclude_ids=used_ids,
            exclude_keys=seen_fps,
            program="spanish",
        )
    except ValueError as exc:
        grok_error = grok_error or str(exc)
        questions = []
        for i, slot in enumerate(slots):
            q = initial[i] if i < len(initial) and initial[i] else _generate_for_slot(slot, used_ids, seen_fps)
            if q:
                questions.append(q)

    random.shuffle(questions)
    out = questions[:question_count]
    if prefer_llm and api_key and not out and grok_error:
        return [], grok_error
    if prefer_llm and api_key and len(out) < question_count and grok_error:
        return out, grok_error
    return out, grok_error if prefer_llm and api_key and grok_error else ""


def build_session_report(
    questions: list[dict],
    answers: list[dict],
    *,
    student_name: str = "Arjun",
) -> dict:
    return build_learning_report(questions, answers, student_name=student_name, program="generic")


def session_meta_from_config(config: dict) -> dict:
    return {
        "week_label": config.get("week_label", ""),
        "topics": config.get("topics", []),
        "use_llm": config.get("use_llm", False),
        "question_count": config.get("question_count", es.DEFAULT_SESSION_COUNT),
    }


def format_report_details(report: dict) -> str:
    lines = [f"Score: {report['correct_count']}/{report['total']} ({report['score_pct']}%)\n"]
    if report.get("strengths"):
        lines.append("Doing well:")
        for s in report["strengths"]:
            lines.append(f"  • {s['name']} — {s['correct']}/{s['total']}")
    if report.get("needs_revision"):
        lines.append("Review:")
        for s in report["needs_revision"]:
            lines.append(f"  • {s['name']} — {s['correct']}/{s['total']}")
    return "\n".join(lines)
