"""Build Class 10 unit practice sessions from weekly configuration."""

from __future__ import annotations

import os
import random
import re

import harshit_class10_practice_pyq as h10pyq
import harshit_class10_questions as h10q
import harshit_class10_topics as h10t
import harshit_math_answers as hma

DEFAULT_QUESTION_COUNT = h10pyq.SESSION_SIZE


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

    # Daily practice is a 10-question PYQ paper: 5×1, unit-specific 2/3, and 1×5.
    if (
        count == DEFAULT_QUESTION_COUNT
        and config.get("include_board_pyq", True)
    ):
        questions = h10pyq.build_mark_pattern_session(unit_id, used_ids=used_ids)
        if len(questions) < count and not (fresh_only and prefer_llm and api_key):
            extra = _fill_from_bank(
                unit_id,
                config,
                count - len(questions),
                used_ids=used_ids,
                used_keys=used_keys,
            )
            for q in extra:
                q.setdefault("marks", 1)
            questions.extend(extra)
        questions = _number_session_questions(questions[:count])
        return questions, ""

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

    questions = h10pyq.inject_pyq_into_session(
        unit_id,
        questions[:count],
        config,
        used_ids=used_ids,
        session_count=count,
    )

    random.shuffle(questions)
    questions = _number_session_questions(questions[:count])
    return questions, grok_error if prefer_llm and api_key and not questions else ""


def _number_session_questions(questions: list[dict]) -> list[dict]:
    for i, q in enumerate(questions, start=1):
        q["q_num"] = i
    return questions


_GENERIC_STEP = re.compile(
    r"^(correct method|accurate final result|correct complete solution.*)$",
    re.IGNORECASE,
)


def _compact(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _norm_answer(text: str) -> str:
    value = str(text or "").lower().replace("×", "*").replace("−", "-").replace("–", "-")
    value = value.replace("√", "sqrt")
    return re.sub(r"[^a-z0-9/+*=.-]", "", value)


def _chain_steps(text: str) -> list[str]:
    """Turn a = b = c into successive board lines that end at the result."""
    parts = [part.strip(" .;") for part in re.split(r"\s*=\s*", text) if part.strip(" .;")]
    if len(parts) < 3:
        return []
    steps = [f"{parts[0]} = {parts[1]}"]
    for part in parts[2:]:
        steps.append(f"= {part}")
    return steps


def board_working_steps(question: dict) -> list[str]:
    """Board-style steps that arrive at the result."""
    model = _compact(question.get("model_answer") or "")
    explanation = _compact(question.get("explanation") or "")
    rubric = [
        _compact(step)
        for step in (question.get("rubric") or [])
        if _compact(step) and not _GENERIC_STEP.match(_compact(step))
    ]
    chunks = [part.strip(" ;") for part in re.split(r"(?<=[.;])\s+", model) if part.strip(" ;")] if model else []
    chain = _chain_steps(model) if model else []
    if len(chunks) >= 2:
        return chunks
    if rubric and chain:
        return [*rubric, *chain]
    if chain:
        return chain
    if rubric and model:
        return [*rubric, model]
    if chunks:
        return chunks
    if explanation:
        parts = [part.strip() for part in re.split(r"(?<=[.;])\s+", explanation) if part.strip()]
        return parts or [explanation]
    if rubric:
        return rubric
    return ["Work in steps, then state the final result."]


def expected_fill_in(question: dict) -> str:
    """Short result the student should type after working on paper."""
    model = _compact(question.get("model_answer") or "")
    if not model:
        return _compact(question.get("explanation") or "")
    hcf = re.search(r"HCF\s*=\s*([0-9]+)", model, re.IGNORECASE)
    lcm = re.search(r"LCM\s*=\s*([0-9]+)", model, re.IGNORECASE)
    if hcf and lcm:
        return f"HCF = {hcf.group(1)}, LCM = {lcm.group(1)}"
    equals = re.findall(r"=\s*([^=.;]{1,48})", model)
    if equals:
        last = equals[-1].strip(" .)")
        if last:
            return last
    sentences = [part.strip() for part in re.split(r"(?<=[.])\s+", model) if part.strip()]
    if sentences and len(sentences[-1]) <= 90:
        return sentences[-1].rstrip(".")
    return model[:160]


def _number_in_text(number: str, typed: str) -> bool:
    number = re.sub(r"\s+", "", number)
    if hma.answers_equivalent(typed, number):
        return True
    if re.fullmatch(r"-?\d+", number):
        return re.search(rf"(?<!\d){re.escape(number)}(?!\d)", typed.replace(",", "")) is not None
    return _norm_answer(number) in _norm_answer(typed)


def fill_in_is_correct(question: dict, typed: str) -> bool:
    typed_text = _compact(typed)
    if not typed_text:
        return False
    expected = expected_fill_in(question)
    if expected and hma.answers_equivalent(typed_text, expected):
        return True
    numbers = re.findall(r"-?\d+\s*/\s*\d+|-?\d+(?:\.\d+)?", expected)
    if len(numbers) >= 2:
        return all(_number_in_text(number, typed_text) for number in numbers)
    if len(numbers) == 1 and hma.answers_equivalent(typed_text, numbers[0].replace(" ", "")):
        return True
    expected_norm = _norm_answer(expected)
    typed_norm = _norm_answer(typed_text)
    if len(typed_norm) >= 8 and expected_norm and (typed_norm in expected_norm or expected_norm in typed_norm):
        return True
    return False


def build_session_report(questions: list[dict], answers: list[dict], *, student_name: str = "Student") -> dict:
    """Score every final answer. Written marks are full or zero from the typed result."""
    by_cat: dict[str, dict] = {}
    written_review: list[dict] = []
    worked_solutions: list[dict] = []
    scored_correct = 0
    marks_earned = 0.0
    marks_max = 0.0
    for idx, q in enumerate(questions):
        ans = answers[idx] if idx < len(answers) else {}
        marks = float(q.get("marks") or 1)
        marks_max += marks
        is_written = q.get("type") == "written"
        picked = _compact(ans.get("picked") or "")
        if is_written:
            expected = expected_fill_in(q)
            is_correct = fill_in_is_correct(q, picked) if picked else False
            your_answer = picked or "Not answered"
        else:
            expected = _compact(ans.get("correct_val") or "")
            is_correct = bool(ans.get("correct"))
            your_answer = picked or "Not answered"
        earned = marks if is_correct else 0.0
        marks_earned += earned
        if is_correct:
            scored_correct += 1
        label = q.get("category_label", q.get("category", ""))
        bucket = by_cat.setdefault(label, {"name": label, "correct": 0, "total": 0})
        bucket["total"] += 1
        if is_correct:
            bucket["correct"] += 1
        steps = board_working_steps(q)
        worked_solutions.append(
            {
                "number": int(q.get("q_num") or idx + 1),
                "topic": label,
                "marks": marks,
                "question": _compact(q.get("question") or q.get("assertion") or ""),
                "your_answer": your_answer,
                "correct_answer": expected,
                "correct": is_correct,
                "steps": steps,
            }
        )
        if is_written:
            written_review.append(
                {
                    "number": int(q.get("q_num") or idx + 1),
                    "topic": label,
                    "marks": marks,
                    "earned": earned,
                    "question": _compact(q.get("question") or ""),
                    "model_answer": _compact(q.get("model_answer") or ""),
                    "explanation": _compact(q.get("explanation") or ""),
                    "your_answer": your_answer,
                    "correct_answer": expected,
                    "steps": steps,
                    "attempted": bool(picked),
                }
            )

    strengths = []
    needs = []
    for item in by_cat.values():
        if not item["total"]:
            continue
        pct = round(100 * item["correct"] / item["total"])
        row = {**item, "pct": pct, "emoji": "✅" if pct >= 80 else "📚"}
        if pct >= 80:
            strengths.append(row)
        else:
            needs.append(row)

    total = len(questions)
    score_pct = round(100 * marks_earned / marks_max) if marks_max else 0
    first = student_name.split()[0] if student_name.strip() else "Student"
    narrative = (
        f"{first} completed {total} questions and scored "
        f"{marks_earned:g}/{marks_max:g} marks ({score_pct}%). "
        f"{scored_correct} of {total} final answers were correct. "
        "The board working for every question is below."
    )
    return {
        "student": student_name,
        "total": total,
        "correct_count": scored_correct,
        "score_pct": score_pct,
        "marks_earned": marks_earned,
        "marks_max": marks_max,
        "written_graded": any(q.get("type") == "written" for q in questions),
        "questions_completed": total,
        "written_review": written_review,
        "worked_solutions": worked_solutions,
        "summary_narrative": narrative,
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
    if report.get("marks_max"):
        lines = [
            f"Score: {float(report['marks_earned']):g}/{float(report['marks_max']):g} marks "
            f"({report['score_pct']}%)\n"
        ]
    else:
        lines = [f"Score: {report['correct_count']}/{report['total']} ({report['score_pct']}%)\n"]
    if report.get("strengths"):
        lines.append("Doing well:")
        for s in report["strengths"]:
            lines.append(f"  • {s['name']} — {s['correct']}/{s['total']}")
    if report.get("needs_revision"):
        lines.append("Needs revision:")
        for s in report["needs_revision"]:
            lines.append(f"  • {s['name']} — {s['correct']}/{s['total']}")
    for item in report.get("worked_solutions") or []:
        mark = "correct" if item.get("correct") else "incorrect"
        lines.append(
            f"Q{item['number']} ({item.get('marks', '')} marks) — {mark}. "
            f"Your answer: {item.get('your_answer', '')}. Result: {item.get('correct_answer', '')}"
        )
        for step_i, step in enumerate(item.get("steps") or [], start=1):
            lines.append(f"  {step_i}. {step}")
    return "\n".join(lines)
