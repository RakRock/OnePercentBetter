"""Build Harshit PreReq practice sessions from weekly topic/level configuration."""

from __future__ import annotations

import os
import random

import database as db
import harshit_chapter_questions as hcq
import harshit_math_diagrams as hmd
import harshit_prereq_topics as hpt

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


def _generate_one(
    prereq_id: int,
    topic_id: int,
    level: str,
    used_ids: set[str],
    used_text: set[str],
) -> dict | None:
    def _fresh(q: dict | None) -> dict | None:
        if not q:
            return None
        text = str(q.get("question", "")).strip()
        if q.get("id") in used_ids or text in used_text:
            return None
        return q

    q = _fresh(
        hcq.pick_question(
            prereq_id,
            topic_id,
            level,
            exclude_ids=used_ids,
            exclude_text=used_text,
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
            exclude_text=used_text,
            templates_only=True,
        )
    )


def _fill_from_bank_and_templates(
    prereq_id: int,
    config: dict,
    count: int,
    *,
    used_ids: set[str] | None = None,
    used_text: set[str] | None = None,
) -> list[dict]:
    slots = _active_slots(prereq_id, config)
    if not slots or count <= 0:
        return []

    used_ids = used_ids or set()
    used_text = used_text or set()
    selected: list[dict] = []
    cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(cycle)

    for tid, lvl in cycle:
        if len(selected) >= count:
            break
        for _ in range(16):
            q = _generate_one(prereq_id, tid, lvl, used_ids, used_text)
            if q:
                text = str(q.get("question", "")).strip()
                selected.append(q)
                used_ids.add(q["id"])
                used_text.add(text)
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
                exclude_text=used_text,
                templates_only=True,
            )
            if q:
                text = str(q.get("question", "")).strip()
                if q["id"] not in used_ids and text not in used_text:
                    selected.append(q)
                    used_ids.add(q["id"])
                    used_text.add(text)

    random.shuffle(selected)
    return selected[:count]


def _build_warmups(
    prereq_id: int,
    config: dict,
    *,
    xai_api_key: str | None = None,
) -> list[dict]:
    count = max(0, min(MAX_WARMUP, int(config.get("warmup_count", 0))))
    if count == 0:
        return []
    slots = _active_slots(prereq_id, config)
    if not slots:
        return []

    warm: list[dict] = []
    used: set[str] = set()
    used_text: set[str] = set()
    easy = [(tid, "A") for tid, lvl in slots if lvl == "A"] or slots[:1]
    prefer_llm = bool(config.get("use_chapter_llm", True))

    if prefer_llm and xai_api_key:
        tid, lvl = random.choice(easy)
        try:
            import harshit_prereq_llm as hllm

            batch = hllm.generate_for_slot(xai_api_key, prereq_id, tid, lvl, count=count)
            added: list[dict] = []
            for q in batch:
                text = str(q.get("question", "")).strip()
                if q.get("id") in used or text in used_text:
                    continue
                q = dict(q)
                q["category_label"] = f"Warm-up · {q['category_label']}"
                q["is_warmup"] = True
                warm.append(q)
                added.append(q)
                used.add(q["id"])
                used_text.add(text)
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
        q = _generate_one(prereq_id, tid, lvl, used, used_text)
        if q:
            q = dict(q)
            q["category_label"] = f"Warm-up · {q['category_label']}"
            q["is_warmup"] = True
            warm.append(q)
            used.add(q["id"])
            used_text.add(str(q.get("question", "")).strip())
    return warm


def _template_session(config: dict, count: int) -> list[dict]:
    prereq_id = int(config.get("prereq_id", 0))
    used_ids = set(config.get("_exclude_ids") or [])
    used_text = set(config.get("_exclude_text") or [])
    return _fill_from_bank_and_templates(
        prereq_id, config, count, used_ids=used_ids, used_text=used_text
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
    slots = _active_slots(prereq_id, config)
    if not slots:
        warmups = _build_warmups(prereq_id, config, xai_api_key=xai_api_key)
        warmups = [_enrich_question(q) for q in warmups]
        return warmups, ""

    prefer_llm = bool(config.get("use_chapter_llm", True))
    api_key = xai_api_key or os.environ.get("XAI_API_KEY", "").strip() or None

    selected: list[dict] = []
    used_ids: set[str] = set()
    used_text: set[str] = set()
    grok_error = ""
    if user_id:
        recent_ids, recent_text = db.get_recent_harshit_practice_exclusions(user_id, prereq_id)
        used_ids.update(recent_ids)
        used_text.update(recent_text)

    if prefer_llm and api_key:
        import harshit_prereq_llm as hllm

        fresh_only = bool(config.get("grok_fresh_only", False))
        fallback = None if fresh_only else _template_session
        for attempt, exclusions in enumerate(
            ((set(used_ids), set(used_text)), (set(), set())) if fresh_only else ((set(used_ids), set(used_text)),)
        ):
            try:
                llm_qs = hllm.generate_session_questions(
                    api_key,
                    prereq_id,
                    config,
                    count,
                    fallback=fallback,
                    exclude_ids=exclusions[0],
                    exclude_text=exclusions[1],
                    max_rounds=1,
                )
                for q in llm_qs:
                    text = str(q.get("question", "")).strip()
                    if q.get("id") not in used_ids and text not in used_text:
                        selected.append(q)
                        used_ids.add(q["id"])
                        used_text.add(text)
                if len(selected) >= count or not fresh_only:
                    break
            except ValueError as exc:
                grok_error = str(exc)
                if fresh_only and attempt == 0 and exclusions[0]:
                    continue
                break

        if not fresh_only and len(selected) < count:
            extra = _fill_from_bank_and_templates(
                prereq_id,
                config,
                count - len(selected),
                used_ids=used_ids,
                used_text=used_text,
            )
            selected.extend(extra)
    else:
        selected = _fill_from_bank_and_templates(
            prereq_id,
            config,
            count,
            used_ids=used_ids,
            used_text=used_text,
        )

    random.shuffle(selected)
    main = [_enrich_question(q) for q in selected[:count]]
    warmups = _build_warmups(prereq_id, config, xai_api_key=api_key if prefer_llm else None)
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


def build_session_report(questions: list[dict], answers: list[dict]) -> dict:
    by_key: dict[str, dict] = {}
    for q, ans in zip(questions, answers):
        key = q.get("category") or "unknown"
        bucket = by_key.setdefault(
            key,
            {"correct": 0, "total": 0, "label": q.get("category_label", key)},
        )
        bucket["total"] += 1
        if ans.get("correct"):
            bucket["correct"] += 1

    strengths: list[dict] = []
    needs_revision: list[dict] = []
    for key, stats in by_key.items():
        pct = int(100 * stats["correct"] / stats["total"]) if stats["total"] else 0
        emoji = "⚡" if "Warm-up" in stats["label"] else "📘"
        entry = {
            "category": key,
            "name": stats["label"],
            "emoji": emoji,
            "correct": stats["correct"],
            "total": stats["total"],
            "pct": pct,
            "tip": f"Review {stats['label']} in your NCERT notes.",
        }
        if pct >= STRENGTH_THRESHOLD_PCT:
            strengths.append(entry)
        else:
            needs_revision.append(entry)

    strengths.sort(key=lambda x: (-x["pct"], x["name"]))
    needs_revision.sort(key=lambda x: (x["pct"], x["name"]))
    correct_count = sum(1 for a in answers if a.get("correct"))
    total = len(answers)
    score_pct = int(100 * correct_count / total) if total else 0

    return {
        "correct_count": correct_count,
        "total": total,
        "score_pct": score_pct,
        "strengths": strengths,
        "needs_revision": needs_revision,
        "tip": needs_revision[0]["tip"] if needs_revision else "",
    }


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
