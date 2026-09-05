"""Generate Spanish vocabulary MCQs via xAI Grok, seeded from the school packet."""

from __future__ import annotations

import json
import random
import re
import uuid

from openai import APIConnectionError, APITimeoutError, OpenAIError

import arjun_spanish.bank as esbank
import arjun_spanish.content as es
import arjun_spanish.store as esstore
from xai_client import make_xai_client

XAI_MODEL = "grok-3-mini"
_MAX_RETRIES = 3
BATCH_MAX_TOKENS = 4500
MAX_SEED_EXAMPLES = 4


def _seed_lines(topic_id: str, count: int = MAX_SEED_EXAMPLES) -> str:
    cards = es.cards_for_topic(topic_id)
    random.shuffle(cards)
    lines = []
    for card in cards[:count]:
        lines.append(f"- {card['spanish']} = {card['english']}")
    return "\n".join(lines)


def _system_prompt() -> str:
    return """You write beginner Spanish vocabulary multiple-choice questions for an 11-year-old (Arjun).

SOURCE: Realidades / Auténtico *Para empezar* — greetings, classroom, numbers, time, weather.

RULES:
- Exactly ONE clear task per question (translate a word/phrase OR pick the best response in context).
- Mix Spanish→English and English→Spanish across the batch.
- Exactly 4 distinct options; "answer" is 0-based index of the correct option.
- Keep Spanish accents (á, é, í, ó, ú, ñ, ¿, ¡) in questions and options.
- Short explanation (1-2 sentences) with a memory tip when helpful.
- Use SEED VOCABULARY as the word list — write NEW questions, do not copy seed examples verbatim.
- No true/false, no "all of the above", no meta questions about the textbook.

Respond with ONLY a JSON array:
[{"question": "...", "options": ["...", "...", "...", "..."], "answer": 0, "explanation": "...", "direction": "es_en"}]

direction must be "es_en" or "en_es"."""


def _validate_spanish_item(q: dict) -> None:
    question = str(q.get("question", "")).strip()
    options = [str(o).strip() for o in q.get("options", [])]
    answer = int(q.get("answer", -1))
    if len(question) < 8 or len(question) > 220:
        raise ValueError("Question length out of range")
    if len(options) != 4 or len({o.lower() for o in options}) < 4:
        raise ValueError("Need 4 distinct options")
    if answer not in range(4):
        raise ValueError("answer must be 0-3")
    if not str(q.get("explanation", "")).strip():
        raise ValueError("Missing explanation")
    direction = str(q.get("direction", "es_en"))
    if direction not in ("es_en", "en_es"):
        raise ValueError("direction must be es_en or en_es")


def _parse_items(raw: str, count: int) -> list[dict]:
    match = re.search(r"\[[\s\S]*\]", raw)
    if not match:
        raise ValueError("No JSON array in response")
    items = json.loads(match.group())
    if not isinstance(items, list) or len(items) < count:
        raise ValueError(f"Expected {count} questions, got {len(items) if isinstance(items, list) else 0}")
    out: list[dict] = []
    for i, item in enumerate(items[:count]):
        if not isinstance(item, dict):
            raise ValueError(f"Item {i + 1} is not an object")
        _validate_spanish_item(item)
        out.append(item)
    return out


def _build_user_message(slots: list[dict]) -> str:
    lines = [f"Generate exactly {len(slots)} Spanish vocabulary MCQs.\n"]
    for i, slot in enumerate(slots, start=1):
        topic_id = slot["topic_id"]
        topic = es.topic_by_id(topic_id)
        direction = slot["direction"]
        dir_label = "Spanish → English" if direction == "es_en" else "English → Spanish"
        lines.append(
            f"\n{i}. Topic: **{topic['title']}** ({topic_id}) · {dir_label}\n"
            f"Seed vocabulary:\n{_seed_lines(topic_id)}"
        )
    lines.append("\nReturn ONLY the JSON array.")
    return "\n".join(lines)


def generate_session_questions_raw(
    xai_api_key: str,
    slots: list[dict],
) -> list[dict]:
    if not slots:
        return []
    client = make_xai_client(xai_api_key, timeout=90.0)
    user_msg = _build_user_message(slots)
    last_error = ""

    for attempt in range(_MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {"role": "system", "content": _system_prompt()},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=BATCH_MAX_TOKENS,
                temperature=0.85,
            )
            raw = response.choices[0].message.content.strip()
            parsed = _parse_items(raw, len(slots))
            out: list[dict] = []
            for i, slot in enumerate(slots):
                item = dict(parsed[i])
                item["id"] = f"es_grok_{slot['topic_id']}_{uuid.uuid4().hex[:10]}"
                item["source"] = "llm"
                out.append(
                    esbank.normalize_llm_question(
                        item,
                        topic_id=slot["topic_id"],
                        direction=str(item.get("direction", slot["direction"])),
                    )
                )
            esstore.add_questions(out)
            return out
        except (APIConnectionError, APITimeoutError, OpenAIError) as exc:
            last_error = str(exc) or "Connection error"
        except (ValueError, json.JSONDecodeError, KeyError) as exc:
            last_error = str(exc)
            user_msg += f"\n\nPrior response invalid ({last_error}). Fix JSON and accents."
    raise ValueError(last_error or "Grok failed to generate Spanish questions")
