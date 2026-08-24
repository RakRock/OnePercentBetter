"""Generate Biology Unit 1 MCQs via xAI Grok, seeded from the 200-question bank."""

from __future__ import annotations

import json
import random
import re
import uuid

from openai import APIConnectionError, APITimeoutError, OpenAI, OpenAIError

from . import content as hpc
from . import questions as hpq
from . import topics as hpt
from llm_question_format import validate_practice_question

XAI_BASE_URL = "https://api.x.ai/v1"
XAI_MODEL = "grok-3-mini"
_MAX_RETRIES = 3
BATCH_MAX_TOKENS = 5000
BATCH_TIMEOUT_SEC = 90.0
MAX_CONCEPT_EXCERPT_CHARS = 4500
MAX_SEED_EXAMPLES = 3


def _get_client(xai_api_key: str) -> OpenAI:
    return OpenAI(api_key=xai_api_key, base_url=XAI_BASE_URL, timeout=BATCH_TIMEOUT_SEC)


def _batch_system_prompt(unit_id: int) -> str:
    umeta = hpc.unit_meta(unit_id)
    topics_by_unit = {
        1: """SOURCE: NCERT Class 10 Ch 5 — Life Processes:
nutrition, photosynthesis, digestion, respiration, transport (xylem/phloem, blood/heart),
excretion (kidney, nephron).""",
        2: """SOURCE: NCERT Class 10 Ch 6 — Control and Coordination:
nervous system, neurons, synapse, reflex arc, brain regions, hormones (adrenaline, insulin),
plant tropisms, coordination in plants.""",
        3: """SOURCE: NCERT Class 10 Ch 7 — How do Organisms Reproduce?:
asexual reproduction (budding, fission, fragmentation, spores), sexual reproduction,
human male/female reproductive systems, fertilisation, contraception, reproductive health.""",
        4: """SOURCE: NCERT Class 10 Ch 8 — Heredity:
Mendel's experiments, dominant/recessive traits, monohybrid/dihybrid crosses, Punnett squares,
sex determination, variation, inherited vs acquired traits.""",
    }
    topics = topics_by_unit.get(unit_id, topics_by_unit[1])
    chapter_ref = umeta.get("chapter_ref", "NCERT Class 10 Biology")
    return f"""You are an NCERT Class 10 Science (Biology) tutor creating multiple-choice practice
for Harshit Sai — Unit {unit_id}: {umeta['title']}.

{topics}

RULES:
- Solvable at Class 10 level; one clear concept per question.
- Exactly 4 distinct options; "answer" is 0-based index of the correct option.
- Plain language — no LaTeX. Use correct chemical formulae (e.g. H₂O, CO₂) as plain text where needed.
- Short explanation (1-2 sentences) referencing the biology idea.
- Use SEED EXAMPLES as style/format guides — write NEW questions, do not copy them.

Respond with ONLY a valid JSON array:
[
  {{"question": "...", "options": ["...", "...", "...", "..."], "answer": 0, "explanation": "...", "chapter_ref": "{chapter_ref}"}}
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
        question = str(q.get("question", "")).strip()
        options = [str(o).strip() for o in q.get("options", [])]
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
                "question": question,
                "options": shuffled,
                "answer": shuffled.index(correct),
                "explanation": str(q.get("explanation", "")).strip(),
                "chapter_ref": str(q.get("chapter_ref", hpc.unit_meta(unit_id).get("chapter_ref", "NCERT Biology"))).strip(),
                "source": "chapter_llm",
            }
        )
    return validated


def _day_concept_excerpt(day_id: int, unit_id: int) -> str:
    day = hpc.get_day(day_id, unit_id=unit_id)
    if not day:
        return ""
    lines = [f"Day {day_id}: {day.get('title', '')}"]
    for c in hpc.concepts_for_day(day_id, unit_id=unit_id):
        name = c.get("name", "")
        simple = str(c.get("simple_answer", ""))[:220]
        remember = str(c.get("remember", ""))[:120]
        lines.append(f"- {name}: {simple}")
        if remember:
            lines.append(f"  Remember: {remember}")
    text = "\n".join(lines)
    return text[:MAX_CONCEPT_EXCERPT_CHARS]


def _seed_examples(day_id: int, level: str, unit_id: int, n: int = MAX_SEED_EXAMPLES) -> list[dict]:
    pool = list(hpq.pool_for(day_id, level, unit_id))
    if not pool:
        for lvl in ("A", "B", "C"):
            pool.extend(hpq.pool_for(day_id, lvl, unit_id))
    if not pool:
        return []
    picks = random.sample(pool, min(n, len(pool)))
    return picks


def _slot_plan(config: dict, count: int) -> list[tuple[int, str]]:
    unit_id = int(config.get("unit_id", hpc.UNIT_ID))
    topics_meta = hpt.topics_for_unit(unit_id)
    slots: list[tuple[int, str]] = []
    for item in config.get("topics", []):
        did = int(item["id"])
        for lvl in item.get("levels", []):
            if did in topics_meta and lvl in topics_meta[did]["levels"]:
                slots.append((did, lvl))
    if not slots:
        return []
    cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(cycle)
    return cycle[:count]


def _build_batch_message(
    unit_id: int,
    slots: list[tuple[int, str]],
) -> str:
    topics = hpt.topics_for_unit(unit_id)
    seen_days: set[int] = set()
    excerpt_parts: list[str] = []
    for did, _ in slots:
        if did not in seen_days:
            seen_days.add(did)
            block = _day_concept_excerpt(did, unit_id)
            if block:
                excerpt_parts.append(block)
    excerpt = "\n\n".join(excerpt_parts)[:MAX_CONCEPT_EXCERPT_CHARS]

    lines = [
        f"Generate exactly {len(slots)} NEW multiple-choice questions (same order as below).",
        f"\nNCERT UNIT {unit_id} CONCEPT SUMMARY:\n{excerpt}\n",
    ]
    for i, (did, lvl) in enumerate(slots, start=1):
        info = topics.get(did, {})
        level_desc = info.get("levels", {}).get(lvl, lvl)
        seeds = _seed_examples(did, lvl, unit_id)
        seed_block = ""
        if seeds:
            seed_lines = [f"Q: {s.get('question')} | opts: {s.get('options')}" for s in seeds]
            seed_block = "\nSeed examples (style only — write different questions):\n" + "\n".join(seed_lines)
        lines.append(
            f"\n{i}. Day {did}: {info.get('name', did)} · Level {lvl} — {level_desc}{seed_block}"
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
    client = _get_client(xai_api_key)
    user_msg = _build_batch_message(unit_id, slots)
    last_error = ""

    for attempt in range(_MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {"role": "system", "content": _batch_system_prompt(unit_id)},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=BATCH_MAX_TOKENS,
                temperature=0.85,
            )
            raw = response.choices[0].message.content.strip()
            parsed = _parse_items(raw, len(slots))
            out: list[dict] = []
            for i, (did, lvl) in enumerate(slots):
                item = dict(parsed[i])
                item["day_id"] = did
                item["level"] = lvl
                item["concept_id"] = item.get("concept_id", "")
                item["id"] = f"u{unit_id}_d{did}_{lvl.lower()}_grok_{uuid.uuid4().hex[:8]}"
                out.append(hpq.normalize_question(item, unit_id))
            hpq.add_questions(out, unit_id)
            return out
        except (APIConnectionError, APITimeoutError, OpenAIError) as exc:
            last_error = str(exc) or "Connection error"
        except (ValueError, json.JSONDecodeError, KeyError) as exc:
            last_error = str(exc)
    raise ValueError(last_error or "Grok failed to generate questions")
