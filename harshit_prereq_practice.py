"""Build Harshit PreReq practice sessions from weekly topic/level configuration."""

from __future__ import annotations

import os
import random

import database as db
import harshit_chapter_questions as hcq
import harshit_math_diagrams as hmd
import harshit_prereq_topics as hpt
from practice_quality.assembler import qa_and_assemble
from practice_quality.report import build_learning_report

STRENGTH_THRESHOLD_PCT = 80
DEFAULT_QUESTION_COUNT = 15
MAX_WARMUP = 5


def _active_slots(prereq_id: int, config: dict) -> list[tuple[int, str]]:
    slots: list[tuple[int, str]] = []
    topics = hpt.topics_for_prereq(prereq_id)
    for item in config.get("topics", []):
        tid = int(item["id"])
        for lvl in item.get("levels", []):
            if tid in topics and lvl in topics[tid]["levels"]:
                slots.append((tid, lvl))
    return slots


def _slot_plan(prereq_id: int, config: dict, count: int) -> list[tuple[int, str]]:
    slots = _active_slots(prereq_id, config)
    if not slots:
        return []
    cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(cycle)
    return cycle[:count]


def _slot_dict(prereq_id: int, topic_id: int, level: str) -> dict:
    return {
        "prereq_id": prereq_id,
        "topic": topic_id,
        "level": level,
        "category": f"p{prereq_id}_t{topic_id}_{level}",
        "category_label": hpt.format_topic_level_label(prereq_id, topic_id, level),
        "question_type": "mcq",
    }


def _question_key(q: dict) -> str:
    return hcq.question_dedup_key(str(q.get("question", "")))


def _is_fresh(q: dict | None, used_ids: set[str], used_keys: set[str]) -> bool:
    if not q:
        return False
    if q.get("id") in used_ids:
        return False
    return _question_key(q) not in used_keys


def _generate_for_slot(slot: dict, used_ids: set[str], seen_fps: set[str]) -> dict | None:
    prereq_id = int(slot["prereq_id"])
    topic_id = int(slot["topic"])
    level = str(slot["level"])
    used_keys = seen_fps  # assembler tracks fingerprints; bank uses text keys too
    q = _generate_one(prereq_id, topic_id, level, used_ids, used_keys)
    if q:
        q = dict(q)
        q.setdefault("category", slot["category"])
        q.setdefault("category_label", slot["category_label"])
    return q


def _track_question(q: dict, used_ids: set[str], used_keys: set[str]) -> None:
    used_ids.add(str(q["id"]))
    used_keys.add(_question_key(q))


def _generate_one(
    prereq_id: int,
    topic_id: int,
    level: str,
    used_ids: set[str],
    used_keys: set[str],
) -> dict | None:
    def _fresh(q: dict | None) -> dict | None:
        return q if _is_fresh(q, used_ids, used_keys) else None

    q = _fresh(
        hcq.pick_question(
            prereq_id,
            topic_id,
            level,
            exclude_ids=used_ids,
            exclude_text=used_keys,
            quality_only=True,
        )
    )
    if q:
        return q

    return _fresh(
        hpt.generate_question(
            prereq_id,
            topic_id,
            level,
            exclude_ids=used_ids,
            exclude_text=used_keys,
            templates_only=True,
        )
    )


def _fill_from_bank_and_templates(
    prereq_id: int,
    config: dict,
    count: int,
    *,
    used_ids: set[str] | None = None,
    used_keys: set[str] | None = None,
) -> list[dict]:
    slots = _active_slots(prereq_id, config)
    if not slots or count <= 0:
        return []

    used_ids = used_ids or set()
    used_keys = used_keys or set()
    selected: list[dict] = []
    cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(cycle)

    for tid, lvl in cycle:
        if len(selected) >= count:
            break
        for _ in range(16):
            q = _generate_one(prereq_id, tid, lvl, used_ids, used_keys)
            if q:
                selected.append(q)
                _track_question(q, used_ids, used_keys)
                break

    if len(selected) < count:
        for tid, lvl in cycle:
            if len(selected) >= count:
                break
            q = hpt.generate_question(
                prereq_id,
                tid,
                lvl,
                exclude_ids=used_ids,
                exclude_text=used_keys,
                templates_only=True,
            )
            if _is_fresh(q, used_ids, used_keys):
                selected.append(q)
                _track_question(q, used_ids, used_keys)

    random.shuffle(selected)
    return selected[:count]


def _build_warmups(
    prereq_id: int,
    config: dict,
    *,
    xai_api_key: str | None = None,
    used_ids: set[str] | None = None,
    used_keys: set[str] | None = None,
) -> list[dict]:
    count = max(0, min(MAX_WARMUP, int(config.get("warmup_count", 0))))
    if count == 0:
        return []
    slots = _active_slots(prereq_id, config)
    if not slots:
        return []

    warm: list[dict] = []
    used = set(used_ids or ())
    used_keys = set(used_keys or ())
    easy = [(tid, "A") for tid, lvl in slots if lvl == "A"] or slots[:1]
    prefer_llm = bool(config.get("use_chapter_llm", True))

    if prefer_llm and xai_api_key:
        tid, lvl = random.choice(easy)
        try:
            import harshit_prereq_llm as hllm

            batch = hllm.generate_for_slot(xai_api_key, prereq_id, tid, lvl, count=count)
            added: list[dict] = []
            for q in batch:
                if not _is_fresh(q, used, used_keys):
                    continue
                q = dict(q)
                q["category_label"] = f"Warm-up · {q['category_label']}"
                q["is_warmup"] = True
                warm.append(q)
                added.append(q)
                _track_question(q, used, used_keys)
                if len(warm) >= count:
                    break
            if added:
                ch = hcq.chapter_for_topic(prereq_id, tid)
                hcq.add_questions(prereq_id, tid, lvl, added, chapter_num=ch)
            if len(warm) >= count:
                return warm
        except ValueError:
            pass
        return warm

    cycle = easy * (count + 1)
    random.shuffle(cycle)
    for tid, lvl in cycle:
        if len(warm) >= count:
            break
        q = _generate_one(prereq_id, tid, lvl, used, used_keys)
        if q:
            q = dict(q)
            q["category_label"] = f"Warm-up · {q['category_label']}"
            q["is_warmup"] = True
            warm.append(q)
            _track_question(q, used, used_keys)
    return warm


def _template_session(config: dict, count: int) -> list[dict]:
    prereq_id = int(config.get("prereq_id", 0))
    used_ids = set(config.get("_exclude_ids") or [])
    used_keys = set(config.get("_exclude_keys") or config.get("_exclude_text") or ())
    return _fill_from_bank_and_templates(
        prereq_id, config, count, used_ids=used_ids, used_keys=used_keys
    )


def build_session_set(
    prereq_id: int,
    config: dict,
    count: int = DEFAULT_QUESTION_COUNT,
    *,
    xai_api_key: str | None = None,
    user_id: int | None = None,
) -> tuple[list[dict], str]:
    config = {**config, "prereq_id": prereq_id}
    if not _active_slots(prereq_id, config):
        warmups = _build_warmups(prereq_id, config, xai_api_key=xai_api_key)
        warmups = [_enrich_question(q) for q in warmups]
        return warmups, ""

    prefer_llm = bool(config.get("use_chapter_llm", True))
    api_key = xai_api_key or os.environ.get("XAI_API_KEY", "").strip() or None

    used_ids: set[str] = set()
    seen_fps: set[str] = set()
    grok_error = ""
    if user_id:
        recent_ids, recent_text = db.get_recent_harshit_practice_exclusions(user_id, prereq_id)
        used_ids.update(recent_ids)
        for t in recent_text:
            seen_fps.add(hcq.question_dedup_key(t))

    plan = _slot_plan(prereq_id, config, count)
    slot_dicts = [_slot_dict(prereq_id, tid, lvl) for tid, lvl in plan]
    initial: list[dict | None] = [None] * len(slot_dicts)

    if prefer_llm and api_key:
        import harshit_prereq_llm as hllm

        try:
            batch = hllm.generate_session_questions_raw(
                api_key,
                prereq_id,
                config,
                count,
            )
            for i, q in enumerate(batch[: len(slot_dicts)]):
                initial[i] = q
        except ValueError as exc:
            grok_error = str(exc)

    try:
        main = qa_and_assemble(
            slot_dicts,
            _generate_for_slot,
            initial=initial,
            exclude_ids=used_ids,
            exclude_keys=seen_fps,
            program="harshit",
        )
    except ValueError as exc:
        grok_error = grok_error or str(exc)
        main = _fill_from_bank_and_templates(
            prereq_id, config, count, used_ids=used_ids, used_keys=seen_fps
        )[:count]

    main = [_enrich_question(q) for q in main[:count]]
    warmups = _build_warmups(
        prereq_id,
        config,
        xai_api_key=api_key if prefer_llm else None,
        used_ids=used_ids,
        used_keys=seen_fps,
    )
    warmups = [_enrich_question(q) for q in warmups]
    questions = warmups + main if warmups else main
    if prefer_llm and api_key and not main and grok_error:
        return questions, grok_error
    return questions, grok_error if prefer_llm and api_key and len(main) < count else ""


def _enrich_question(q: dict) -> dict:
    try:
        return hmd.enrich_question(q)
    except Exception:
        return q


def build_session_report(
    questions: list[dict],
    answers: list[dict],
    *,
    student_name: str = "Student",
) -> dict:
    return build_learning_report(questions, answers, student_name=student_name, program="harshit")


def session_meta_from_config(prereq_id: int, config: dict) -> dict:
    return {
        "prereq_id": prereq_id,
        "week_label": config.get("week_label", ""),
        "topics": config.get("topics", []),
        "warmup_count": config.get("warmup_count", 0),
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
