"""Board-format 25-minute unit tests for NCERT Class 10 Mathematics."""

from __future__ import annotations

import random
import uuid
from typing import Any

import harshit_class10_board_seeds as h10bs
import harshit_class10_questions as h10q
import harshit_class10_topics as h10t

UNIT_TEST_DURATION_SEC = 25 * 60
UNIT_TEST_TOTAL_MARKS = 15
# Practice sessions use 100 + unit_id; unit tests use 200 + unit_id in Sheets / SQLite.
UNIT_TEST_SHEET_UNIT_OFFSET = 200

AR_OPTIONS = [
    "Both Assertion (A) and Reason (R) are true and R is the correct explanation of A",
    "Both A and R are true but R is NOT the correct explanation of A",
    "A is true but R is false",
    "A is false but R is true",
]

# Fallback when board seed bucket is empty (legacy templates)
_FALLBACK_AR: dict[int, list[dict]] = {}
_FALLBACK_WRITTEN: dict[int, dict[str, list[dict]]] = {}


def unit_test_available(unit_id: int) -> bool:
    return bool(h10t.topics_for_unit(unit_id)) and (
        h10bs.seeds_available(unit_id) or unit_id in _FALLBACK_WRITTEN
    )


def blueprint_summary() -> str:
    return (
        "Board-style unit test · 25 minutes · 15 marks\n"
        "Section A: 4 MCQs (1 mark) + 1 Assertion–Reason (1 mark)\n"
        "Section B: 1 Very Short Answer (2 marks)\n"
        "Section C: 1 Short Answer (3 marks)\n"
        "Section D: 1 Long Answer (5 marks)\n"
        "Questions seeded from CBSE 30/1, 30/2, 30/3 & official SQP papers."
    )


def seed_source_line(unit_id: int) -> str:
    sources = h10bs.seed_sources(unit_id)
    if not sources:
        return "Question bank templates"
    return "Board papers: " + ", ".join(sources[:4]) + ("…" if len(sources) > 4 else "")


def _pick_mcq(unit_id: int, used_ids: set[str], used_keys: set[str], level: str) -> dict | None:
    seed = h10bs.pick_mcq_seed(unit_id, exclude_ids=used_ids)
    if seed:
        used_ids.add(str(seed["id"]))
        return seed

    topics = h10t.topics_for_unit(unit_id)
    topic_ids = sorted(topics)
    random.shuffle(topic_ids)
    for tid in topic_ids:
        for _ in range(20):
            q = h10q.pick_question(unit_id, tid, level, exclude_ids=used_ids, exclude_text=used_keys)
            if not q:
                q = h10t.generate_question(
                    unit_id, tid, level, exclude_ids=used_ids, exclude_text=used_keys, templates_only=True
                )
            if not q:
                continue
            key = h10q.question_dedup_key(str(q.get("question", "")), q.get("options"))
            if str(q.get("id", "")) in used_ids or key in used_keys:
                continue
            used_ids.add(str(q["id"]))
            used_keys.add(key)
            return q
    return None


def _wrap_mcq(raw: dict, q_num: int) -> dict:
    return {
        **raw,
        "q_num": q_num,
        "section": "A",
        "section_label": "Section A — MCQ",
        "type": "mcq",
        "marks": 1,
        "source": raw.get("source_paper", raw.get("source", "board_seed")),
    }


def _wrap_ar(raw: dict, q_num: int) -> dict:
    return {
        "id": raw.get("id", f"ut_ar_{uuid.uuid4().hex[:8]}"),
        "q_num": q_num,
        "section": "A",
        "section_label": "Section A — Assertion–Reason",
        "type": "assertion_reason",
        "marks": 1,
        "question": "Assertion (A) and Reason (R) — choose the correct option.",
        "assertion": raw["assertion"],
        "reason": raw["reason"],
        "options": list(AR_OPTIONS),
        "answer": int(raw["answer"]),
        "explanation": raw.get("explanation", ""),
        "source": raw.get("source_paper", "board_seed"),
    }


def _wrap_written(raw: dict, q_num: int, section: str, default_marks: int) -> dict:
    marks = int(raw.get("marks", default_marks))
    if section == "B":
        label = "Section B — Very Short Answer"
    elif section == "C":
        label = "Section C — Short Answer"
    else:
        label = "Section D — Long Answer"
    wrapped = {
        "id": raw.get("id", f"ut_w_{uuid.uuid4().hex[:8]}"),
        "q_num": q_num,
        "section": section,
        "section_label": label,
        "type": "written",
        "marks": marks,
        "question": raw["question"],
        "model_answer": raw["model_answer"],
        "rubric": list(raw.get("rubric", [])),
        "source": raw.get("source_paper", "board_seed"),
    }
    if raw.get("marking_scheme"):
        wrapped["marking_scheme"] = raw["marking_scheme"]
    return wrapped


def _pick_written(unit_id: int, bucket: str, section: str, default_marks: int, used_ids: set[str]) -> dict | None:
    raw = h10bs.pick_written_seed(unit_id, bucket, exclude_ids=used_ids)
    if raw:
        used_ids.add(str(raw["id"]))
        return raw
    fallback = _FALLBACK_WRITTEN.get(unit_id, {}).get(bucket, [])
    pool = [q for q in fallback if q.get("id") not in used_ids]
    if pool:
        choice = random.choice(pool)
        used_ids.add(str(choice["id"]))
        return choice
    return None


def build_unit_test(unit_id: int) -> tuple[list[dict], str | None]:
    """Build a fresh 15-mark board-format paper scoped to one NCERT unit."""
    if not unit_test_available(unit_id):
        return [], f"Unit test not ready for unit {unit_id} yet."

    used_ids: set[str] = set()
    used_keys: set[str] = set()
    questions: list[dict] = []
    q_num = 0

    levels = ["B", "C", "C", "D"]
    for lvl in levels:
        q_num += 1
        mcq = _pick_mcq(unit_id, used_ids, used_keys, lvl)
        if not mcq:
            return [], "Could not generate enough MCQs for this unit test."
        questions.append(_wrap_mcq(mcq, q_num))

    q_num += 1
    ar_raw = h10bs.pick_ar_seed(unit_id, exclude_ids=used_ids)
    if not ar_raw:
        return [], "No assertion–reason seeds for this unit."
    used_ids.add(str(ar_raw["id"]))
    questions.append(_wrap_ar(ar_raw, q_num))

    q_num += 1
    vsa = _pick_written(unit_id, "vsa", "B", 2, used_ids)
    if not vsa:
        return [], "No Section B seeds for this unit."
    questions.append(_wrap_written(vsa, q_num, "B", 2))

    q_num += 1
    sa = _pick_written(unit_id, "sa", "C", 3, used_ids)
    if not sa:
        return [], "No Section C seeds for this unit."
    questions.append(_wrap_written(sa, q_num, "C", 3))

    q_num += 1
    la = _pick_written(unit_id, "la", "D", 5, used_ids)
    if not la:
        return [], "No Section D seeds for this unit."
    questions.append(_wrap_written(la, q_num, "D", 5))

    return questions, None


def remaining_seconds(start_time: float, *, now: float | None = None) -> int:
    import time

    elapsed = int((now if now is not None else time.time()) - start_time)
    return max(0, UNIT_TEST_DURATION_SEC - elapsed)


def grade_mcq_pick(question: dict, picked_index: int) -> float:
    import harshit_math_answers as hma

    if hma.is_pick_correct(question, picked_index):
        return float(question.get("marks", 1))
    return 0.0


def grade_written_self_rating(marks: int, rating: str) -> float:
    if rating == "full":
        return float(marks)
    if rating == "partial":
        return float(marks) / 2.0
    return 0.0


def written_earned(question: dict, resp: dict) -> float:
    import harshit_class10_unit_test_grader as h10g

    marks = float(question.get("marks", 0))
    grade = resp.get("ai_grade") or {}
    if "earned" in grade:
        try:
            return h10g.clamp_half_mark(float(grade.get("earned", 0)), marks)
        except (TypeError, ValueError):
            return 0.0
    rating = str(resp.get("self_rating") or "")
    if rating:
        return grade_written_self_rating(int(marks), rating)
    return 0.0


def build_unit_test_report(questions: list[dict], responses: list[dict]) -> dict[str, Any]:
    earned = 0.0
    max_marks = 0.0
    breakdown: list[dict] = []

    for q, resp in zip(questions, responses):
        marks = float(q.get("marks", 0))
        max_marks += marks
        qtype = q.get("type", "mcq")
        if qtype in ("mcq", "assertion_reason"):
            picked = resp.get("picked_index")
            got = grade_mcq_pick(q, int(picked)) if picked is not None else 0.0
        else:
            got = written_earned(q, resp)
        earned += got
        breakdown.append(
            {
                "q_num": q.get("q_num"),
                "section": q.get("section"),
                "type": qtype,
                "marks": marks,
                "earned": got,
                "source": q.get("source", ""),
            }
        )

    pct = round(100 * earned / max_marks) if max_marks else 0
    return {
        "earned": earned,
        "max_marks": max_marks,
        "score_pct": pct,
        "breakdown": breakdown,
    }


def build_unit_test_failed_questions(questions: list[dict], responses: list[dict]) -> list[dict]:
    """Questions that lost marks — for email and sheet sync."""
    import harshit_math_answers as hma

    failed: list[dict] = []
    for idx, (q, resp) in enumerate(zip(questions, responses)):
        qtype = q.get("type", "mcq")
        q_num = int(q.get("q_num", idx + 1))
        if qtype in ("mcq", "assertion_reason"):
            picked_i = resp.get("picked_index")
            opts = q.get("options") or []
            if picked_i is None:
                failed.append(
                    {
                        "number": q_num,
                        "topic": f"Section {q.get('section', 'A')}",
                        "question": str(q.get("question") or "Assertion–Reason"),
                        "picked": "Not attempted",
                        "correct": opts[q["answer"]] if opts and "answer" in q else "",
                        "explanation": str(q.get("explanation", "")),
                    }
                )
                continue
            if not hma.is_pick_correct(q, int(picked_i)):
                failed.append(
                    {
                        "number": q_num,
                        "topic": f"Section {q.get('section', 'A')}",
                        "question": str(q.get("question") or "Assertion–Reason"),
                        "picked": opts[int(picked_i)] if 0 <= int(picked_i) < len(opts) else "?",
                        "correct": opts[q["answer"]] if opts and "answer" in q else "?",
                        "explanation": str(q.get("explanation", "")),
                    }
                )
            continue

        marks = int(q.get("marks", 0))
        got = written_earned(q, resp)
        if got >= marks:
            continue
        grade = resp.get("ai_grade") or {}
        n_photos = len(resp.get("work_images") or [])
        photo_note = f" ({n_photos} paper photo(s) on file)" if n_photos else ""
        feedback = str(grade.get("feedback") or grade.get("corrections") or "").strip()
        if not feedback:
            feedback = "Review the CBSE marking-scheme steps for this question."
        picked = f"{got:g}/{marks} (examiner)"
        if resp.get("self_rating") and "earned" not in grade:
            labels = {"full": "Full marks", "partial": "Partial credit", "missed": "Missed"}
            picked = labels.get(str(resp.get("self_rating")), str(resp.get("self_rating")))
        failed.append(
            {
                "number": q_num,
                "topic": f"Section {q.get('section', '?')} written ({marks} marks){photo_note}",
                "question": str(q.get("question", "")),
                "picked": picked,
                "correct": str(q.get("model_answer", "")),
                "explanation": feedback,
            }
        )
    return failed


def enrich_report_for_sync(
    report: dict[str, Any],
    questions: list[dict],
    responses: list[dict],
    *,
    student_name: str = "Student",
) -> dict[str, Any]:
    """Add fields expected by practice email and Google Sheets."""
    failed = build_unit_test_failed_questions(questions, responses)
    earned = float(report.get("earned", 0))
    max_m = float(report.get("max_marks", 0))
    pct = int(report.get("score_pct", 0))
    first = student_name.split()[0] if student_name.strip() else "Student"

    by_section: dict[str, dict[str, Any]] = {}
    for item in report.get("breakdown", []):
        sec = str(item.get("section", "?"))
        bucket = by_section.setdefault(
            sec,
            {"name": f"Section {sec}", "correct": 0.0, "total": 0.0},
        )
        bucket["total"] += float(item.get("marks", 0))
        bucket["correct"] += float(item.get("earned", 0))

    strengths: list[dict] = []
    needs: list[dict] = []
    for item in by_section.values():
        sec_pct = round(100 * item["correct"] / item["total"]) if item["total"] else 0
        row = {
            "name": item["name"],
            "correct": item["correct"],
            "total": item["total"],
            "pct": sec_pct,
            "emoji": "✅" if sec_pct >= 80 else "📚",
        }
        if sec_pct >= 80:
            strengths.append(row)
        elif sec_pct < 60:
            needs.append(row)

    if pct >= 80:
        status = "Strong"
    elif pct >= 60:
        status = "Good"
    else:
        status = "Developing"

    return {
        **report,
        "session_type": "unit_test",
        "student": student_name,
        "correct_count": earned,
        "total": max_m,
        "failed_questions": failed,
        "summary_narrative": (
            f"{first} completed a 25-minute CBSE board-format unit test "
            f"and scored {earned:g}/{max_m:g} marks ({pct}%)."
        ),
        "overall_status": status,
        "strengths": strengths,
        "needs_revision": needs,
    }


def format_unit_test_report_details(report: dict[str, Any]) -> str:
    """Plain-text summary for activity log / SharePoint details field."""
    lines = [
        f"Unit test: {report.get('earned', 0):g}/{report.get('max_marks', 0):g} marks "
        f"({report.get('score_pct', 0)}%)",
        "",
        "Question breakdown:",
    ]
    for item in report.get("breakdown", []):
        lines.append(
            f"  Q{item.get('q_num')} Section {item.get('section')}: "
            f"{item.get('earned', 0):g}/{item.get('marks', 0):g}"
        )
    failed = report.get("failed_questions") or []
    if failed:
        lines.append("")
        lines.append(f"Questions to review ({len(failed)}):")
        for f in failed:
            lines.append(f"  Q{f.get('number')}: {f.get('topic', '')}")
    return "\n".join(lines)
