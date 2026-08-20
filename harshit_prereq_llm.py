"""Generate Harshit PreReq MCQs from NCERT chapter PDF text via xAI Grok."""

from __future__ import annotations

import json
import os
import random
import re
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

from openai import APIConnectionError, APITimeoutError, OpenAI, OpenAIError

import harshit_chapter_pdf as hcp
import harshit_chapter_questions as hcq
import harshit_math_render as hmr
import harshit_math_prereqs as hmp
import harshit_prereq_topics as hpt
from llm_question_format import (
    KID_NUMERIC_FORMAT_RULES,
    NUMERIC_RETRY_HINT,
    validate_practice_question,
)

XAI_BASE_URL = "https://api.x.ai/v1"
XAI_MODEL = "grok-3-mini"
_MAX_RETRIES = 3
DEFAULT_PARALLEL = 2
MAX_QUESTIONS_PER_CALL = 8
MAX_SLOT_EXCERPT_CHARS = 900
BATCH_SPLIT_THRESHOLD = 8
BATCH_MAX_TOKENS = 5000
BATCH_TIMEOUT_SEC = 90.0


def _parallel_workers(max_workers: int | None = None) -> int:
    if max_workers is not None and max_workers > 0:
        return max_workers
    try:
        return max(1, int(os.environ.get("XAI_MAX_PARALLEL", DEFAULT_PARALLEL)))
    except ValueError:
        return DEFAULT_PARALLEL


def _get_client(xai_api_key: str) -> OpenAI:
    """Same client pattern as Arjun Course 3 / Linear Equations / GK."""
    return OpenAI(api_key=xai_api_key, base_url=XAI_BASE_URL, timeout=BATCH_TIMEOUT_SEC)


def _batch_system_prompt() -> str:
    return f"""You are an NCERT Class 9 Mathematics tutor creating multiple-choice practice for a student named Harshit Sai.

SOURCE: Each question MUST be derived from the NCERT chapter excerpt provided for that slot.

RULES:
- Transform chapter ideas into a SOLVABLE problem the student can answer in one step (or one short chain).
- Use definitions, examples, and exercise styles from the excerpt — do not invent unrelated content.
- Class 9 difficulty; clear wording; one task per question; max ~2 sentences in the question.
- Exactly 4 options; "answer" is the 0-based index of the correct option.
- Options must be plausible mathematical answers (numbers, expressions, or short phrases like "Rational" / "Irrational").
- Include a short explanation referencing the chapter idea (1-2 sentences).
- Text-only; use plain notation: √3, (√3)^2, 2/3 — NEVER LaTeX (no \\sqrt, \\frac, \\text, \\displaystyle, or $...$).
- Optional "chapter_ref" field: section or example reference (e.g. "Ex 1.2 Q3 style").
- Vary wording and structure — do NOT repeat the same template across questions.

FORBIDDEN:
- Meta/categorization questions ("Which best describes this chapter example?").
- True/false or yes/no questions.
- LaTeX markup of any kind (\\sqrt, \\frac, \\text, $...$).
- Pasting "Solution:" text from the book into the question.
- Options like "A theorem with proof" or "Worked example from the NCERT chapter".
{KID_NUMERIC_FORMAT_RULES}

Respond with ONLY a valid JSON array — one object per requested question, in order:
[
  {{
    "question": "Full question text",
    "options": ["...", "...", "...", "..."],
    "answer": 0,
    "explanation": "Why this is correct, tied to the chapter.",
    "chapter_ref": "Section or exercise reference"
  }}
]"""


def _system_prompt(prereq_id: int, topic_id: int, level: str, chapter_num: int) -> str:
    topic = hpt.topics_for_prereq(prereq_id).get(topic_id, {})
    level_desc = topic.get("levels", {}).get(level, level)
    return f"""You are an NCERT Class 9 Mathematics tutor creating multiple-choice practice for a student named Harshit Sai.

SOURCE: Questions MUST be derived from the NCERT Class 9 Chapter {chapter_num} excerpt provided by the user.
Topic: {topic.get('name', topic_id)} — Level {level}: {level_desc}

RULES:
- Transform chapter ideas into a SOLVABLE problem the student can answer in one step (or one short chain).
- Use definitions, examples, and exercise styles from the excerpt — do not invent unrelated content.
- Class 9 difficulty; clear wording; one task per question; max ~2 sentences in the question.
- Exactly 4 options; "answer" is the 0-based index of the correct option.
- Options must be plausible mathematical answers (numbers, expressions, or short phrases like "Rational" / "Irrational").
- Include a short explanation referencing the chapter idea (1-2 sentences).
- Text-only; use plain notation: √3, (√3)^2, 2/3 — NEVER LaTeX (no \\sqrt, \\frac, \\text, \\displaystyle, or $...$).
- Optional "chapter_ref" field: section or example reference (e.g. "Ex 1.2 Q3 style").
- Vary wording and structure — do NOT repeat the same template every time.
{KID_NUMERIC_FORMAT_RULES}

Respond with ONLY a valid JSON array — one object per requested question:
[
  {{
    "question": "Full question text",
    "options": ["...", "...", "...", "..."],
    "answer": 0,
    "explanation": "Why this is correct, tied to the chapter.",
    "chapter_ref": "Section or exercise reference"
  }}
]"""


def _parse_items(raw: str, count: int) -> list[dict]:
    match = re.search(r"\[[\s\S]*\]", raw)
    if not match:
        raise ValueError(f"No JSON array in LLM response:\n{raw[:400]}")
    items = json.loads(match.group())
    if not isinstance(items, list) or len(items) < count:
        raise ValueError(f"Expected {count} questions, got {len(items) if isinstance(items, list) else 0}")

    validated: list[dict] = []
    for i, q in enumerate(items[:count]):
        for field in ("question", "options", "answer"):
            if field not in q:
                raise ValueError(f"Question {i + 1} missing {field}")
        if not isinstance(q["options"], list) or len(q["options"]) != 4:
            raise ValueError(f"Question {i + 1} must have 4 options")
        answer = int(q["answer"])
        if answer not in range(4):
            raise ValueError(f"Question {i + 1} invalid answer index")

        question = hmr.sanitize_grok_math_text(str(q["question"]))
        options = [hmr.sanitize_grok_math_text(str(o)) for o in q["options"]]
        explanation = hmr.sanitize_grok_math_text(str(q.get("explanation", "")))
        validate_practice_question(question, options)

        correct = options[answer]
        order = list(range(4))
        random.shuffle(order)
        shuffled = [options[j] for j in order]
        validated.append(
            {
                "question": question.strip(),
                "options": shuffled,
                "answer": shuffled.index(correct),
                "explanation": explanation.strip(),
                "chapter_ref": str(q.get("chapter_ref", "")).strip(),
                "source": "chapter_llm",
            }
        )
    return validated


def _chapter_excerpt(prereq_id: int, topic_id: int, level: str) -> tuple[str, int, list[str]]:
    ch = hcq.chapter_for_topic(prereq_id, topic_id)
    if ch is None:
        return "", 0, []
    prereq = hmp.get_prereq(prereq_id)
    aliases = None
    if prereq:
        for c in prereq.get("class9_chapters", []):
            if c["number"] == ch:
                aliases = c.get("folder_aliases")
                break
    bundle = hcp.extract_chapter_text(ch, aliases)
    topic = hpt.topics_for_prereq(prereq_id).get(topic_id, {})
    level_desc = topic.get("levels", {}).get(level, level)
    excerpt = hcp.excerpt_for_topic(bundle["text"], topic.get("name", ""), level_desc)
    return excerpt, ch, bundle.get("sources", [])


def _slot_plan(config: dict, count: int) -> list[tuple[int, str]]:
    slots: list[tuple[int, str]] = []
    prereq_id = int(config.get("prereq_id", 0))
    topics = hpt.topics_for_prereq(prereq_id)
    for item in config.get("topics", []):
        tid = int(item["id"])
        for lvl in item.get("levels", []):
            if tid in topics and lvl in topics[tid]["levels"]:
                slots.append((tid, lvl))
    if not slots:
        return []
    cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(cycle)
    return cycle[:count]


def _compact_excerpt(prereq_id: int, topic_id: int, level: str) -> tuple[str, int]:
    excerpt, ch, _ = _chapter_excerpt(prereq_id, topic_id, level)
    if not excerpt:
        return "", ch
    if len(excerpt) > MAX_SLOT_EXCERPT_CHARS:
        excerpt = excerpt[:MAX_SLOT_EXCERPT_CHARS] + "…"
    return excerpt, ch


def _build_batch_user_message(
    slots: list[tuple[int, str]],
    prereq_id: int,
    seed: int,
) -> str:
    """Compact per-slot excerpts — much smaller than full chapter dumps (Arjun-sized prompts)."""
    lines = [
        f"Generate exactly {len(slots)} multiple-choice questions for practice session {seed}.",
        "Each question MUST match the topic, level, and short chapter excerpt listed (same order):",
    ]
    topics = hpt.topics_for_prereq(prereq_id)
    for i, (tid, lvl) in enumerate(slots, start=1):
        excerpt, ch = _compact_excerpt(prereq_id, tid, lvl)
        if not excerpt:
            raise ValueError(f"No chapter text found for topic {tid} level {lvl} (Ch {ch})")
        info = topics.get(tid, {})
        level_desc = info.get("levels", {}).get(lvl, lvl)
        lines.append(
            f"\n{i}. **{info.get('name', tid)}** · Level {lvl} — {level_desc} · Chapter {ch}\n"
            f"Excerpt: {excerpt}"
        )
    lines.append("\nReturn ONLY the JSON array, in the same order as the numbered list above.")
    return "\n".join(lines)


def _generate_batch_call_once(
    xai_api_key: str,
    prereq_id: int,
    slots: list[tuple[int, str]],
) -> list[dict]:
    """Single Grok API call for a batch of slots."""
    if not slots:
        return []

    client = _get_client(xai_api_key)
    seed = random.randint(1000, 9999)
    user_msg = _build_batch_user_message(slots, prereq_id, seed)
    last_error = ""

    for attempt in range(_MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {"role": "system", "content": _batch_system_prompt()},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=BATCH_MAX_TOKENS,
                temperature=0.85,
            )
            raw = response.choices[0].message.content.strip()
            parsed = _parse_items(raw, len(slots))
            out: list[dict] = []
            for i, (tid, lvl) in enumerate(slots):
                item = dict(parsed[i])
                ch = hcq.chapter_for_topic(prereq_id, tid)
                item["chapter_num"] = ch
                out.append(hcq.normalize_question(item, prereq_id, tid, lvl))
            return out
        except (APIConnectionError, APITimeoutError, OpenAIError) as exc:
            last_error = str(exc) or "Connection error"
            break
        except (ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
            last_error = str(exc)
            user_msg = (
                _build_batch_user_message(slots, prereq_id, seed)
                + f"\n\nYour previous response was invalid ({last_error}). "
                f"Return ONLY a valid JSON array with exactly {len(slots)} questions. "
                + NUMERIC_RETRY_HINT
            )

    raise ValueError(last_error or "LLM question generation failed")


def _generate_batch_call(
    xai_api_key: str,
    prereq_id: int,
    slots: list[tuple[int, str]],
) -> list[dict]:
    """One or two parallel Grok calls — faster than one huge prompt for 15 questions."""
    if not slots:
        return []
    if len(slots) <= BATCH_SPLIT_THRESHOLD:
        return _generate_batch_call_once(xai_api_key, prereq_id, slots)

    mid = (len(slots) + 1) // 2
    left, right = slots[:mid], slots[mid:]
    with ThreadPoolExecutor(max_workers=2) as pool:
        f_left = pool.submit(_generate_batch_call_once, xai_api_key, prereq_id, left)
        f_right = pool.submit(_generate_batch_call_once, xai_api_key, prereq_id, right)
        return f_left.result() + f_right.result()


def generate_for_slot(
    xai_api_key: str,
    prereq_id: int,
    topic_id: int,
    level: str,
    count: int = 1,
) -> list[dict]:
    """Generate for one topic/level slot (used by bank builder and warm-ups)."""
    excerpt, chapter_num, _sources = _chapter_excerpt(prereq_id, topic_id, level)
    if not excerpt:
        raise ValueError(f"No chapter text found for PreReq {prereq_id} topic {topic_id} (Ch {chapter_num})")

    topic = hpt.topics_for_prereq(prereq_id).get(topic_id, {})
    level_desc = topic.get("levels", {}).get(level, level)
    client = _get_client(xai_api_key)
    user_msg = (
        f"Generate exactly {count} multiple-choice question(s).\n"
        f"Topic: {topic.get('name')} · Level {level} — {level_desc}\n"
        f"Chapter {chapter_num} excerpt:\n\n{excerpt}\n\n"
        "Return ONLY the JSON array."
    )
    last_error = ""
    for attempt in range(_MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {"role": "system", "content": _system_prompt(prereq_id, topic_id, level, chapter_num)},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=min(600 + 750 * count, 16_000),
                temperature=0.85,
            )
            raw = resp.choices[0].message.content.strip()
            items = _parse_items(raw, count)
            out: list[dict] = []
            for item in items:
                item["chapter_num"] = chapter_num
                out.append(hcq.normalize_question(item, prereq_id, topic_id, level))
            return out
        except (APIConnectionError, APITimeoutError, OpenAIError) as exc:
            last_error = str(exc) or "Connection error"
            break
        except (ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
            last_error = str(exc)
            user_msg += f"\n\nPrevious response invalid ({last_error}). {NUMERIC_RETRY_HINT}"
    raise ValueError(last_error or "LLM generation failed")


def generate_for_slots_parallel(
    xai_api_key: str,
    prereq_id: int,
    slot_counts: list[tuple[int, str, int]],
    *,
    max_workers: int | None = None,
) -> tuple[dict[tuple[int, str], list[dict]], list[str]]:
    """Parallel per-slot generation — used by offline bank builder only."""
    tasks: list[tuple[int, str, int]] = []
    for topic_id, level, count in slot_counts:
        remaining = count
        while remaining > 0:
            batch = min(remaining, MAX_QUESTIONS_PER_CALL)
            tasks.append((topic_id, level, batch))
            remaining -= batch

    if not tasks:
        return {}, []

    results: dict[tuple[int, str], list[dict]] = {}
    errors: list[str] = []
    workers = min(_parallel_workers(max_workers), len(tasks))

    def _run(topic_id: int, level: str, count: int) -> tuple[tuple[int, str], list[dict]]:
        qs = generate_for_slot(xai_api_key, prereq_id, topic_id, level, count=count)
        return (topic_id, level), qs

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_run, tid, lvl, cnt) for tid, lvl, cnt in tasks]
        for fut in as_completed(futures):
            try:
                key, qs = fut.result()
                results.setdefault(key, []).extend(qs)
            except ValueError as exc:
                errors.append(str(exc))
            time.sleep(0.2)

    return results, errors


def _cache_generated_to_bank(prereq_id: int, questions: list[dict]) -> None:
    by_slot: dict[tuple[int, str], list[dict]] = {}
    for q in questions:
        tid = int(q.get("topic_id") or q.get("topic") or 0)
        lvl = str(q.get("level", ""))
        if tid and lvl:
            by_slot.setdefault((tid, lvl), []).append(q)
    for (tid, lvl), qs in by_slot.items():
        ch = hcq.chapter_for_topic(prereq_id, tid)
        hcq.add_questions(prereq_id, tid, lvl, qs, chapter_num=ch)


def generate_session_questions(
    xai_api_key: str,
    prereq_id: int,
    config: dict,
    count: int,
    *,
    fallback: Callable[[dict, int], list[dict]] | None = None,
    max_workers: int | None = None,
    exclude_ids: set[str] | None = None,
    exclude_text: set[str] | None = None,
    max_rounds: int = 1,
) -> list[dict]:
    """Generate a practice session via one Grok call (Arjun-style), with optional bank fallback."""
    del max_workers  # batch path uses a single API call
    config = {**config, "prereq_id": prereq_id}
    used: set[str] = set(exclude_ids or set())
    used_text: set[str] = set(exclude_text or set())
    questions: list[dict] = []
    last_error = ""

    rounds = max(1, max_rounds if fallback is None else 1)
    for _round in range(rounds):
        if len(questions) >= count:
            break
        need = count - len(questions)
        slots = _slot_plan(config, need)
        if not slots:
            break
        try:
            batch = _generate_batch_call(xai_api_key, prereq_id, slots)
        except ValueError as exc:
            last_error = str(exc)
            break

        for q in batch:
            if hcq.is_question_excluded(q, exclude_ids=used, exclude_text=used_text):
                continue
            questions.append(q)
            used.add(str(q.get("id", "")))
            used_text.add(hcq.question_dedup_key(str(q.get("question", ""))))
            if len(questions) >= count:
                break

    if questions:
        _cache_generated_to_bank(prereq_id, questions)

    if len(questions) < count and fallback:
        fb_config = {**config, "_exclude_ids": used, "_exclude_keys": used_text}
        extra = fallback(fb_config, count - len(questions))
        for q in extra:
            if hcq.is_question_excluded(q, exclude_ids=used, exclude_text=used_text):
                continue
            questions.append(q)
            used.add(str(q.get("id", "")))
            used_text.add(hcq.question_dedup_key(str(q.get("question", ""))))

    if not questions and fallback is None:
        raise ValueError(last_error or "Grok returned no valid questions")

    random.shuffle(questions)
    return questions[:count]
