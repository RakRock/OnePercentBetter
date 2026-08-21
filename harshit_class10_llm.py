"""Generate Class X unit MCQs from NCERT PDF via xAI Grok, using seed bank examples."""

from __future__ import annotations

import json
import random
import re

from openai import APIConnectionError, APITimeoutError, OpenAI, OpenAIError

import harshit_class10_questions as h10q
import harshit_class10_topics as h10t
import harshit_class10_units as h10u
import harshit_math_render as hmr
from llm_question_format import KID_NUMERIC_FORMAT_RULES, validate_practice_question

XAI_BASE_URL = "https://api.x.ai/v1"
XAI_MODEL = "grok-3-mini"
_MAX_RETRIES = 3
BATCH_MAX_TOKENS = 5000
BATCH_TIMEOUT_SEC = 90.0
MAX_EXCERPT_CHARS = 6000
MAX_SEED_EXAMPLES = 3


def _get_client(xai_api_key: str) -> OpenAI:
    return OpenAI(api_key=xai_api_key, base_url=XAI_BASE_URL, timeout=BATCH_TIMEOUT_SEC)


def _batch_system_prompt() -> str:
    return f"""You are an NCERT Class 10 Mathematics tutor creating multiple-choice practice for Harshit Sai.

SOURCE: Questions MUST follow the NCERT unit excerpt and match the topic/level described.

RULES:
- Solvable in one step or a short chain; Class 10 difficulty.
- Exactly 4 options; "answer" is 0-based index of the correct option.
- Plain notation: √2, 2/3 — no LaTeX.
- Short explanation (1-2 sentences).
- Use the SEED EXAMPLES as style/format guides — create NEW questions, do not copy them.
{KID_NUMERIC_FORMAT_RULES}

Respond with ONLY a valid JSON array:
[
  {{"question": "...", "options": ["...", "...", "...", "..."], "answer": 0, "explanation": "...", "chapter_ref": "..."}}
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
        question = hmr.sanitize_grok_math_text(str(q.get("question", "")))
        options = [hmr.sanitize_grok_math_text(str(o)) for o in q.get("options", [])]
        answer = int(q.get("answer", 0))
        if len(options) != 4 or answer not in range(4):
            raise ValueError(f"Question {i + 1} invalid options/answer")
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
                "explanation": hmr.sanitize_grok_math_text(str(q.get("explanation", ""))).strip(),
                "chapter_ref": str(q.get("chapter_ref", "")).strip(),
                "source": "chapter_llm",
            }
        )
    return validated


def _unit_excerpt(unit_id: int) -> str:
    bundle = h10u.extract_unit_text(unit_id, max_chars=MAX_EXCERPT_CHARS)
    text = bundle.get("text", "")
    if not text.strip():
        raise ValueError(
            f"No PDF text for unit {unit_id}. Add the chapter PDF under "
            f"HarshitMath/class10/units/unit_{unit_id:02d}/"
        )
    return text


def _seed_examples(unit_id: int, topic_id: int, level: str, n: int = MAX_SEED_EXAMPLES) -> list[dict]:
    bank = h10q.load_bank(unit_id, topic_id)
    pool = [q for q in bank.get("questions", {}).get(level, []) if isinstance(q, dict)]
    if not pool:
        for _ in range(n * 3):
            q = h10t.generate_question(unit_id, topic_id, level, templates_only=True)
            if q:
                pool.append(q)
            if len(pool) >= n:
                break
    if not pool:
        return []
    picks = random.sample(pool, min(n, len(pool)))
    return picks


def _slot_plan(config: dict, count: int) -> list[tuple[int, str]]:
    unit_id = int(config.get("unit_id", 0))
    topics_meta = h10t.topics_for_unit(unit_id)
    slots: list[tuple[int, str]] = []
    for item in config.get("topics", []):
        tid = int(item["id"])
        for lvl in item.get("levels", []):
            if tid in topics_meta and lvl in topics_meta[tid]["levels"]:
                slots.append((tid, lvl))
    if not slots:
        return []
    cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(cycle)
    return cycle[:count]


def _build_batch_message(
    unit_id: int,
    slots: list[tuple[int, str]],
    excerpt: str,
) -> str:
    topics = h10t.topics_for_unit(unit_id)
    lines = [
        f"Generate exactly {len(slots)} NEW multiple-choice questions (same order as below).",
        f"\nNCERT UNIT EXCERPT:\n{excerpt[:MAX_EXCERPT_CHARS]}\n",
    ]
    for i, (tid, lvl) in enumerate(slots, start=1):
        info = topics.get(tid, {})
        level_desc = info.get("levels", {}).get(lvl, lvl)
        seeds = _seed_examples(unit_id, tid, lvl)
        seed_block = ""
        if seeds:
            seed_lines = []
            for s in seeds:
                seed_lines.append(f"Q: {s.get('question')} | opts: {s.get('options')}")
            seed_block = "\nSeed examples (style only — write different questions):\n" + "\n".join(seed_lines)
        lines.append(
            f"\n{i}. Topic: {info.get('name', tid)} · Level {lvl} — {level_desc}{seed_block}"
        )
    lines.append("\nReturn ONLY the JSON array.")
    return "\n".join(lines)


def generate_session_questions_raw(
    xai_api_key: str,
    unit_id: int,
    config: dict,
    count: int,
) -> list[dict]:
    slots = _slot_plan(config, count)
    if not slots:
        return []
    excerpt = _unit_excerpt(unit_id)
    client = _get_client(xai_api_key)
    user_msg = _build_batch_message(unit_id, slots, excerpt)
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
                out.append(h10q.normalize_question(item, unit_id, tid, lvl))
            _cache_to_bank(unit_id, out)
            return out
        except (APIConnectionError, APITimeoutError, OpenAIError) as exc:
            last_error = str(exc) or "Connection error"
        except (ValueError, json.JSONDecodeError, KeyError) as exc:
            last_error = str(exc)
    raise ValueError(last_error or "Grok failed to generate questions")


def generate_bank_batch(
    xai_api_key: str,
    unit_id: int,
    topic_id: int,
    level: str,
    count: int = 8,
) -> int:
    """Generate questions into the unit bank for one topic/level."""
    config = {
        "unit_id": unit_id,
        "topics": [{"id": topic_id, "levels": [level]}],
    }
    slots = [(topic_id, level)] * count
    excerpt = _unit_excerpt(unit_id)
    client = _get_client(xai_api_key)
    user_msg = _build_batch_message(unit_id, slots, excerpt)
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
    batch = [h10q.normalize_question(dict(parsed[i]), unit_id, topic_id, level) for i in range(len(slots))]
    return h10q.add_questions(unit_id, topic_id, level, batch)


def _cache_to_bank(unit_id: int, questions: list[dict]) -> None:
    by_slot: dict[tuple[int, str], list[dict]] = {}
    for q in questions:
        tid = int(q.get("topic") or 0)
        lvl = str(q.get("level", ""))
        if tid and lvl:
            by_slot.setdefault((tid, lvl), []).append(q)
    for (tid, lvl), qs in by_slot.items():
        h10q.add_questions(unit_id, tid, lvl, qs)
