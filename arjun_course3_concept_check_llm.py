"""Generate concept-check MCQs via xAI Grok for Arjun Course 3."""

from __future__ import annotations

import json
import random
import re
import time

from openai import APIConnectionError, APITimeoutError, OpenAIError

import arjun_course3_concept_check as c3cc
import arjun_course3_concept_check_store as c3store
import arjun_course3_content as c3
import arjun_course3_levels as c3lvl
from llm_question_format import KID_NUMERIC_FORMAT_RULES, NUMERIC_RETRY_HINT, validate_numerical_format
from xai_client import make_xai_client

XAI_MODEL = "grok-3-mini"
_MAX_RETRIES = 3


def _get_client(xai_api_key: str):
    return make_xai_client(xai_api_key)


def _system_prompt(unit_id: int, categories: dict, revision_tips: dict, *, count: int = 1) -> str:
    unit = c3.get_unit(unit_id)
    title = unit["title"] if unit else f"Unit {unit_id}"
    topic_lines = []
    for cat_id, info in categories.items():
        tip = revision_tips.get(cat_id, "").strip()
        topic_lines.append(f"- **{cat_id}** ({info.get('name', cat_id)}): {tip}")

    level_lines = "\n".join(
        f"- Level {lvl}: {c3lvl.LEVEL_DESCRIPTIONS[lvl]}" for lvl in c3lvl.LEVEL_ORDER
    )

    return f"""You write Math 3 CONCEPT CHECK multiple-choice questions for an 11-year-old (Arjun).

UNIT: {title}

TOPICS (use exact category id on each question):
{chr(10).join(topic_lines)}

DIFFICULTY:
{level_lines}

{c3cc.concept_check_prompt_block()}

RULES:
- Return a JSON array with exactly {count} question object{"s" if count != 1 else ""}.
- Exactly 4 options; "answer" is 0-based index of the correct option.
- Include "explanation" with Step 1, Step 2 when math is involved.
- Self-contained full-sentence stems; no images — describe graphs/tables in words.
- Wrong options = plausible mistakes from the school's concept checks.
- Match the requested category and level exactly. Each stem must be unique.
{KID_NUMERIC_FORMAT_RULES}

Respond with ONLY a JSON array of {count} object{"s" if count != 1 else ""}:
[{{"category": "...", "level": "B", "question": "...", "options": ["...", "...", "...", "..."], "answer": 0, "explanation": "..."}}]"""


def _normalize_item(q: dict, unit_id: int, category: str, fallback_level: str, categories: dict) -> dict:
    if not isinstance(q, dict):
        raise ValueError("Question must be an object")
    cat = str(q.get("category", category)).strip()
    if cat not in categories:
        cat = category
    if not isinstance(q.get("options"), list) or len(q["options"]) != 4:
        raise ValueError("Need exactly 4 options")
    ans = q.get("answer")
    if not isinstance(ans, int) or ans not in range(4):
        raise ValueError("answer must be 0-3")
    validate_numerical_format(str(q.get("question", "")), [str(o) for o in q["options"]])
    correct = str(q["options"][ans])
    indices = list(range(4))
    random.shuffle(indices)
    options = [str(q["options"][j]) for j in indices]
    answer = options.index(correct)
    lvl = str(q.get("level") or fallback_level).strip().upper()[:1]
    if lvl not in c3lvl.LEVEL_ORDER:
        lvl = fallback_level
    stamp = int(time.time() * 1000) % 1_000_000
    return {
        "id": f"cc_ai_u{unit_id}_{category}_{stamp}_{random.randint(100, 999)}",
        "category": cat,
        "level": lvl,
        "question": str(q.get("question", "")).strip(),
        "options": options,
        "answer": answer,
        "explanation": str(q.get("explanation", "")).strip(),
        "source": "concept_check",
        "origin": "llm",
    }


def _parse_items(raw: str, unit_id: int, category: str, level: str, categories: dict) -> list[dict]:
    match = re.search(r"\[[\s\S]*\]", raw)
    if not match:
        raise ValueError("No JSON array in response")
    items = json.loads(match.group())
    if not isinstance(items, list) or not items:
        raise ValueError("Expected non-empty JSON array")
    out: list[dict] = []
    errors: list[str] = []
    for q in items:
        try:
            out.append(_normalize_item(q, unit_id, category, level, categories))
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(str(exc))
    if not out:
        raise ValueError(errors[0] if errors else "No valid questions")
    return out


def _parse_one(raw: str, unit_id: int, category: str, level: str, categories: dict) -> dict:
    return _parse_items(raw, unit_id, category, level, categories)[0]


def generate_concept_check_llm(
    xai_api_key: str,
    unit_id: int,
    category: str,
    level: str,
    *,
    categories: dict | None = None,
    revision_tips: dict | None = None,
    persist: bool = False,
    verbose: bool = False,
) -> dict | None:
    """Generate one concept-check MCQ; optionally save to JSON bank."""
    import arjun_course3_practice as c3p

    cfg = c3p._unit_practice(unit_id)
    cats = categories or cfg["categories"]
    tips = revision_tips or cfg["revision_tips"]
    if category not in cats:
        return None

    archetype = c3cc.archetype_hint(category, level)
    user_msg = (
        f"Generate exactly 1 concept-check question.\n"
        f"category: **{category}** ({cats[category].get('name', category)})\n"
        f"level: **{level}** — {c3lvl.LEVEL_DESCRIPTIONS.get(level, level)}\n"
        f"Archetype: {archetype}\n"
        f"Session seed: {random.randint(1000, 9999)} — make it unique.\n"
        "Return ONLY the JSON array."
    )
    system = _system_prompt(unit_id, cats, tips, count=1)
    client = _get_client(xai_api_key)
    last_err: str | None = None

    for attempt in range(_MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=1200,
                temperature=0.9,
            )
            raw = resp.choices[0].message.content.strip()
            out = _parse_one(raw, unit_id, category, level, cats)
            if persist:
                c3store.add_questions(unit_id, [out])
            return out
        except (APIConnectionError, APITimeoutError, OpenAIError) as exc:
            last_err = str(exc)
            break
        except (ValueError, json.JSONDecodeError, KeyError, TypeError) as exc:
            last_err = str(exc)
            user_msg += f"\n\nInvalid prior response ({last_err}). {NUMERIC_RETRY_HINT}"

    if verbose and last_err:
        print(f"    reason: {last_err}")
    return None


def generate_concept_check_batch_llm(
    xai_api_key: str,
    unit_id: int,
    category: str,
    levels: list[str],
    *,
    categories: dict | None = None,
    revision_tips: dict | None = None,
    persist: bool = False,
    verbose: bool = False,
) -> list[dict]:
    """Generate several concept-check MCQs for one category in a single Grok call."""
    import arjun_course3_practice as c3p

    if not levels:
        return []
    cfg = c3p._unit_practice(unit_id)
    cats = categories or cfg["categories"]
    tips = revision_tips or cfg["revision_tips"]
    if category not in cats:
        return []

    count = len(levels)
    level_list = ", ".join(levels)
    archetypes = "\n".join(
        f"- Item {i + 1} (Level {lvl}): {c3cc.archetype_hint(category, lvl)}"
        for i, lvl in enumerate(levels)
    )
    style_extra = ""
    if unit_id >= 4:
        style_extra = (
            "\nMatch Units 1–3 school concept-check style:\n"
            "- Concrete numbers a kid can compute (tables, percents, y=mx+b).\n"
            "- Kid-friendly story (sports, food, school, games) — not a vague description.\n"
            "- Wrong options = common slips (swap slope/intercept, use row vs table total).\n"
            "- Each explanation must have Step 1 and Step 2.\n"
        )
    user_msg = (
        f"Generate exactly {count} different concept-check questions for one category.\n"
        f"category: **{category}** ({cats[category].get('name', category)})\n"
        f"Levels in order: {level_list}\n"
        f"{archetypes}\n"
        f"{style_extra}"
        f"Session seed: {random.randint(1000, 9999)} — make each stem unique.\n"
        "Return ONLY a JSON array with that many objects."
    )
    system = _system_prompt(unit_id, cats, tips, count=count)
    client = _get_client(xai_api_key)
    last_err: str | None = None
    fallback_level = levels[0]

    for attempt in range(_MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=3500,
                temperature=0.9,
            )
            raw = (resp.choices[0].message.content or "").strip()
            out = _parse_items(raw, unit_id, category, fallback_level, cats)
            if persist:
                c3store.add_questions(unit_id, out)
            return out[:count]
        except (APIConnectionError, APITimeoutError, OpenAIError) as exc:
            last_err = str(exc)
            break
        except (ValueError, json.JSONDecodeError, KeyError, TypeError) as exc:
            last_err = str(exc)
            user_msg += f"\n\nInvalid prior response ({last_err}). {NUMERIC_RETRY_HINT}"

    if verbose and last_err:
        print(f"    reason: {last_err}")
    return []


def generate_batch_for_unit(
    xai_api_key: str,
    unit_id: int,
    *,
    per_category: int = 4,
    levels: list[str] | None = None,
) -> list[dict]:
    """Generate multiple concept-check questions across all unit categories."""
    import arjun_course3_practice as c3p

    cfg = c3p._unit_practice(unit_id)
    cats = cfg["categories"]
    lvls = levels or ["B", "C", "D"]
    out: list[dict] = []
    for cat_id in cats:
        wanted = [lvls[i % len(lvls)] for i in range(per_category)]
        batch = generate_concept_check_batch_llm(
            xai_api_key,
            unit_id,
            cat_id,
            wanted,
            categories=cats,
            revision_tips=cfg["revision_tips"],
            persist=False,
        )
        out.extend(batch)
        for i, lvl in enumerate(wanted[len(batch) :]):
            q = generate_concept_check_llm(
                xai_api_key,
                unit_id,
                cat_id,
                lvl,
                categories=cats,
                revision_tips=cfg["revision_tips"],
                persist=False,
            )
            if q:
                out.append(q)
    return out
