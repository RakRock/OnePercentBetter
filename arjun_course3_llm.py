"""LLM-generated Course 3 Math unit practice questions via xAI Grok."""

from __future__ import annotations

import json
import random
import re
import time
from typing import Callable

from openai import APIConnectionError, APITimeoutError, OpenAI, OpenAIError

import arjun_course3_content as c3
from llm_question_format import KID_NUMERIC_FORMAT_RULES, NUMERIC_RETRY_HINT, validate_numerical_format

XAI_BASE_URL = "https://api.x.ai/v1"
XAI_MODEL = "grok-3-mini"
_MAX_RETRIES = 3


def _get_client(xai_api_key: str) -> OpenAI:
    return OpenAI(api_key=xai_api_key, base_url=XAI_BASE_URL)


def _category_plan(categories: dict, count: int) -> list[str]:
    weighted: list[str] = []
    for cat_id, info in categories.items():
        weight = max(1, int(info.get("weight", 1)))
        weighted.extend([cat_id] * weight)
    if not weighted:
        return []
    random.shuffle(weighted)
    cycle = weighted * ((count // len(weighted)) + 1)
    return cycle[:count]


def _activity_blurbs(unit_id: int) -> str:
    unit = c3.get_unit(unit_id)
    if not unit:
        return ""
    lines = []
    for act in unit.get("activities") or []:
        lines.append(f"  Activity {act['number']}: {act['title']}")
    return "\n".join(lines)


def _system_prompt(
    *,
    unit_title: str,
    unit_subtitle: str,
    categories: dict,
    revision_tips: dict,
    activity_blurbs: str,
) -> str:
    topic_lines = []
    for cat_id, info in categories.items():
        tip = revision_tips.get(cat_id, "").strip()
        topic_lines.append(f"- **{cat_id}** ({info.get('name', cat_id)}): {tip}")

    return f"""You are a Grade 8 math tutor creating multiple-choice practice for an 11-year-old student named Arjun.

UNIT: {unit_title} — {unit_subtitle}

LESSON ACTIVITIES IN THIS UNIT:
{activity_blurbs or "(see topic list below)"}

TOPICS — each question MUST use one of these exact category ids:
{chr(10).join(topic_lines)}

RULES:
- Grade 8 difficulty; use clear, kid-friendly wording in full sentences (especially for patterns and word problems).
- For fraction operations, state the operation explicitly: "Add …", "Subtract …", or "Multiply …".
- Exactly 4 answer options per question; "answer" is the 0-based index of the correct option.
- Include a short "explanation" (1-3 sentences) teaching the idea.
- Text-only questions (no images) — describe tables or number lines in words when needed.
- Numbers should be reasonable integers or simple fractions/decimals.
- Wrong options must be plausible common mistakes.
- Do NOT repeat the same scenario or identical math across questions.
- Answer choices must be self-contained full phrases — never say "Both A and B", "Option C", or use letter labels.
- Explain proportional vs linear clearly: proportional means through (0, 0); a starting fee means NOT proportional.
- Use plain language kids understand (e.g., "the $5 entry fee" instead of "flat fee").
{KID_NUMERIC_FORMAT_RULES}

Respond with ONLY a valid JSON array — one object per requested question, in order:
[
  {{
    "category": "patterns",
    "question": "Full question text shown to the student",
    "options": ["A text", "B text", "C text", "D text"],
    "answer": 0,
    "explanation": "Why the correct option works."
  }}
]"""


def _parse_llm_questions(raw: str, expected_categories: list[str], categories: dict) -> list[dict]:
    json_match = re.search(r"\[[\s\S]*\]", raw)
    if not json_match:
        raise ValueError(f"No JSON array found in response:\n{raw[:500]}")

    items = json.loads(json_match.group())
    if not isinstance(items, list) or not items:
        raise ValueError("Expected a non-empty JSON array of questions")

    validated: list[dict] = []
    for i, q in enumerate(items):
        if not isinstance(q, dict):
            raise ValueError(f"Question {i + 1} is not an object")
        for field in ("category", "question", "options", "answer"):
            if field not in q:
                raise ValueError(f"Question {i + 1} missing field: {field}")
        cat = str(q["category"]).strip()
        expected = expected_categories[i] if i < len(expected_categories) else cat
        if cat not in categories:
            cat = expected if expected in categories else cat
        if cat not in categories:
            raise ValueError(f"Question {i + 1} has unknown category: {cat}")

        if not isinstance(q["options"], list) or len(q["options"]) != 4:
            raise ValueError(f"Question {i + 1} must have exactly 4 options")
        if not isinstance(q["answer"], int) or q["answer"] not in range(4):
            raise ValueError(f"Question {i + 1} has invalid answer index")

        correct_text = str(q["options"][q["answer"]])
        indices = list(range(4))
        random.shuffle(indices)
        options = [str(q["options"][j]) for j in indices]
        answer = options.index(correct_text)

        validate_numerical_format(str(q["question"]).strip(), options)

        validated.append(
            {
                "category": cat,
                "question": str(q["question"]).strip(),
                "options": options,
                "answer": answer,
                "explanation": str(q.get("explanation") or "").strip(),
            }
        )

    if len(validated) < len(expected_categories):
        raise ValueError(f"Expected at least {len(expected_categories)} questions, got {len(validated)}")

    return validated[: len(expected_categories)]


def _to_session_question(q: dict, unit_id: int, categories: dict) -> dict:
    cat = q["category"]
    info = categories.get(cat, {})
    stamp = int(time.time() * 1000) % 1_000_000
    return {
        "id": f"c3_llm_u{unit_id}_{cat}_{stamp}_{random.randint(100, 999)}",
        "category": cat,
        "question": q["question"],
        "options": q["options"],
        "answer": q["answer"],
        "explanation": q.get("explanation", ""),
        "source": "llm",
        "category_label": info.get("name", cat),
    }


def _build_user_message(slots: list[str], categories: dict, seed: int) -> str:
    lines = [
        f"Generate exactly {len(slots)} multiple-choice questions for practice session {seed}.",
        "Each question MUST use the exact category id listed (one question per line, same order):",
    ]
    for i, cat_id in enumerate(slots, start=1):
        name = categories.get(cat_id, {}).get("name", cat_id)
        lines.append(f"{i}. category **{cat_id}** — {name}")
    lines.append("Return ONLY the JSON array, in the same order as the list above.")
    return "\n".join(lines)


def generate_session_questions(
    xai_api_key: str,
    unit_id: int,
    count: int,
    *,
    categories: dict,
    revision_tips: dict,
    unit_title: str = "",
    unit_subtitle: str = "",
    focus_category: str | None = None,
    fallback: Callable[[], list[dict]] | None = None,
) -> list[dict]:
    """Generate a full unit practice session via xAI Grok."""
    if focus_category and focus_category in categories:
        slots = [focus_category] * count
    else:
        slots = _category_plan(categories, count)
    if not slots:
        return fallback() if fallback else []

    unit = c3.get_unit(unit_id)
    title = unit_title or (unit["title"] if unit else f"Unit {unit_id}")
    subtitle = unit_subtitle or (unit.get("subtitle", "") if unit else "")

    client = _get_client(xai_api_key)
    seed = random.randint(1000, 9999)
    system = _system_prompt(
        unit_title=title,
        unit_subtitle=subtitle,
        categories=categories,
        revision_tips=revision_tips,
        activity_blurbs=_activity_blurbs(unit_id),
    )
    user_msg = _build_user_message(slots, categories, seed)
    last_error: str | None = None

    for attempt in range(_MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=5000,
                temperature=0.85,
            )
            raw = response.choices[0].message.content.strip()
            parsed = _parse_llm_questions(raw, slots, categories)
            questions = [_to_session_question(parsed[i], unit_id, categories) for i in range(len(slots))]
            random.shuffle(questions)
            return questions[:count]
        except (APIConnectionError, APITimeoutError, OpenAIError) as exc:
            last_error = str(exc)
            break
        except (ValueError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            last_error = str(exc)
            user_msg = (
                _build_user_message(slots, categories, seed)
                + f"\n\nYour previous response was invalid ({last_error}). "
                "Return ONLY a valid JSON array with category, question, options (4), answer (0-3), explanation. "
                + NUMERIC_RETRY_HINT
            )

    if fallback:
        return fallback()
    raise ValueError(last_error or "LLM question generation failed")
