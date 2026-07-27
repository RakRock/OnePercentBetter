"""LLM-generated linear equation practice questions via xAI Grok."""

from __future__ import annotations

import json
import random
import re
from typing import Callable

from openai import OpenAI

import arjun_linear_equation_strategies as leqs

XAI_BASE_URL = "https://api.x.ai/v1"
XAI_MODEL = "grok-3-mini"
_MAX_RETRIES = 3


def _get_client(xai_api_key: str) -> OpenAI:
    return OpenAI(api_key=xai_api_key, base_url=XAI_BASE_URL)


def _strategy_catalog_text() -> str:
    lines = []
    for sid in sorted(leqs.STRATEGIES):
        info = leqs.STRATEGIES[sid]
        lines.append(f"Strategy {sid}: {info['name']}")
        for lvl, desc in info["levels"].items():
            lines.append(f"  Level {lvl} — {desc}")
    return "\n".join(lines)


def _system_prompt() -> str:
    return f"""You are a Grade 8 math tutor creating multiple-choice linear equation practice for an 11-year-old student named Arjun.

STRATEGY & LEVEL CATALOG (match each question to the assigned strategy/level):
{_strategy_catalog_text()}

CRITICAL — use separate fields for the prompt and the math (do NOT embed the equation inside the instruction sentence):
- "instruction": short plain-English prompt shown ABOVE the equation (no math symbols).
- "equation": ONLY the math, e.g. "x + 6 = 26" or "x/5 = 8" or "3/4 x = 12".
- "followup": optional line below the equation, e.g. "What is x?" — leave "" for first-step questions.

EQUATION RULES BY STRATEGY (must match assigned level):
- Strategy 1 Inspection: solvable mentally; fractions as a/bx or x/a.
- Strategy 2 Level A: ONLY x + c = d or x - c = d (addition/subtraction on x).
- Strategy 2 Level B: ONLY ax = b or x/a = b (multiplication/division — no x + c).
- Strategy 2 Level C–E: two-step or negative/fraction coefficients as level describes.
- Strategy 5: equations with fractions to clear.
- Strategy 6: equations with y to isolate.
- Strategy 7: systems or elimination/substitution steps.

OTHER RULES:
- Write fractions as a/b or x/5 (not LaTeX).
- Exactly 4 options; "answer" is 0-based index of the correct option.
- Strategy 2 Level A/B: options describe operations ("Subtract 6", "Multiply both sides by 5"), NOT numeric x.
- Strategy 1 and solve-for-x items: correct option is the value of x unless asking for a step.
- Plausible wrong options; short explanation for each question.

Example (Strategy 2 Level B):
{{
  "strategy": 2,
  "level": "B",
  "instruction": "What is the first step to solve this equation?",
  "equation": "x/5 = 8",
  "followup": "",
  "options": ["Multiply both sides by 5", "Add 5 to both sides", "Divide both sides by 5", "Subtract 5 from both sides"],
  "answer": 0,
  "explanation": "x is divided by 5, so multiply both sides by 5 to undo it."
}}

Respond with ONLY a valid JSON array — one object per requested question, in order."""


def _equation_fits_slot(equation: str, sid: int, lvl: str) -> bool:
    eq = leqs._normalize_math_text(equation).replace(" ", "")
    if sid == 2 and lvl == "A":
        return bool(re.search(r"^x[+\-]", eq) and "=" in eq and not re.search(r"x/\d", eq) and not re.search(r"^\d+x", eq))
    if sid == 2 and lvl == "B":
        return bool(re.search(r"^(\d+x|x/\d+)", eq) and "=" in eq and not re.search(r"x[+\-]\d", eq))
    return bool(re.search(r"=", eq))


def _needs_vague_instruction_fix(instruction: str) -> bool:
    text = instruction.strip().lower().rstrip("?")
    return text in {
        "first step to solve",
        "first step",
        "solve",
        "solve mentally",
        "best first step",
    } or bool(re.fullmatch(r"first step to solve for y in", text))


def _normalize_llm_item(raw: dict, slot: tuple[int, str]) -> dict:
    sid, lvl = slot
    eq = str(raw.get("equation") or "").strip()
    instruction = str(raw.get("instruction") or "").strip()
    followup = str(raw.get("followup") or "").strip()

    if not eq:
        _, eq, followup_from_q = leqs.split_question(str(raw.get("question") or ""))
        if not instruction:
            instruction = str(raw.get("question") or "").split(eq)[0].strip() if eq else ""
        if not followup:
            followup = followup_from_q

    if not eq:
        raise ValueError("Missing equation in LLM question")

    if not _equation_fits_slot(eq, sid, lvl):
        raise ValueError(f"Equation '{eq}' does not match Strategy {sid} Level {lvl}")

    if not instruction or _needs_vague_instruction_fix(instruction):
        instruction = leqs.default_instruction_for_slot(sid, lvl)
    if not followup:
        followup = leqs.default_followup_for_slot(sid, lvl)

    return {
        "strategy": sid,
        "level": lvl,
        "instruction": instruction,
        "equation": eq,
        "followup": followup,
        "question": leqs.compose_question(instruction, eq, followup),
        "options": raw["options"],
        "answer": raw["answer"],
        "explanation": str(raw.get("explanation") or "").strip(),
    }


def _parse_llm_questions(raw: str, expected_slots: list[tuple[int, str]]) -> list[dict]:
    json_match = re.search(r"\[[\s\S]*\]", raw)
    if not json_match:
        raise ValueError(f"No JSON array found in response:\n{raw[:500]}")

    items = json.loads(json_match.group())
    if not isinstance(items, list) or not items:
        raise ValueError("Expected a non-empty JSON array of questions")

    validated: list[dict] = []
    for i, q in enumerate(items):
        for field in ("strategy", "level", "options", "answer"):
            if field not in q:
                raise ValueError(f"Question {i + 1} missing field: {field}")
        if not (q.get("equation") or q.get("question")):
            raise ValueError(f"Question {i + 1} needs 'equation' or 'question'")
        if not isinstance(q["options"], list) or len(q["options"]) != 4:
            raise ValueError(f"Question {i + 1} must have exactly 4 options")
        if not isinstance(q["answer"], int) or q["answer"] not in range(4):
            raise ValueError(f"Question {i + 1} has invalid answer index")

        slot = expected_slots[i] if i < len(expected_slots) else (int(q["strategy"]), str(q["level"]).upper())
        correct_text = str(q["options"][q["answer"]])
        indices = list(range(4))
        random.shuffle(indices)
        options = [str(q["options"][j]) for j in indices]
        answer = options.index(correct_text)

        normalized = _normalize_llm_item(
            {**q, "options": options, "answer": answer},
            slot,
        )
        validated.append(normalized)

    if len(validated) < len(expected_slots):
        raise ValueError(f"Expected at least {len(expected_slots)} questions, got {len(validated)}")

    return validated[: len(expected_slots)]


def _to_session_question(q: dict, slot: tuple[int, str]) -> dict:
    sid, lvl = slot
    question = q["question"]
    return {
        "id": f"leq_llm_s{sid}_{lvl}_{random.randint(1000, 9999)}",
        "strategy": sid,
        "level": lvl,
        "instruction": q["instruction"],
        "equation": q["equation"],
        "followup": q.get("followup", ""),
        "question": question,
        "question_tex": leqs.text_to_latex(q["equation"]),
        "options": q["options"],
        "options_tex": [leqs.text_to_latex(o) for o in q["options"]],
        "answer": q["answer"],
        "explanation": q.get("explanation", ""),
        "category": f"s{sid}_{lvl}",
        "category_label": leqs.format_strategy_level_label(sid, lvl),
        "source": "llm",
    }


def _slot_plan(config: dict, count: int) -> list[tuple[int, str]]:
    slots: list[tuple[int, str]] = []
    for item in config.get("strategies", []):
        sid = int(item["id"])
        for lvl in item.get("levels", []):
            if sid in leqs.STRATEGIES and lvl in leqs.STRATEGIES[sid]["levels"]:
                slots.append((sid, lvl))
    if not slots:
        return []
    slot_cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(slot_cycle)
    return slot_cycle[:count]


def _procedural_for_slot(slot: tuple[int, str]) -> dict | None:
    sid, lvl = slot
    q = leqs.generate_question(sid, lvl)
    if not q:
        return None
    q = dict(q)
    q["category"] = f"s{sid}_{lvl}"
    q["category_label"] = leqs.format_strategy_level_label(sid, lvl)
    q["source"] = "template"
    return q


def _build_user_message(slots: list[tuple[int, str]], seed: int) -> str:
    lines = [
        f"Generate exactly {len(slots)} multiple-choice questions for session {seed}.",
        "Use instruction / equation / followup fields — keep the equation OUT of the instruction text.",
        "Each question MUST use the exact strategy number and level letter listed:",
    ]
    for i, (sid, lvl) in enumerate(slots, start=1):
        info = leqs.STRATEGIES[sid]
        lines.append(
            f"{i}. Strategy {sid} ({info['short']}), Level {lvl} — {info['levels'][lvl]}"
        )
    lines.append("Return ONLY the JSON array, in the same order as the list above.")
    return "\n".join(lines)


def generate_session_questions(
    xai_api_key: str,
    config: dict,
    count: int,
    *,
    fallback: Callable[[dict, int], list[dict]] | None = None,
) -> list[dict]:
    """Generate a full practice session via xAI Grok. Falls back on failure."""
    slots = _slot_plan(config, count)
    if not slots:
        return []

    client = _get_client(xai_api_key)
    seed = random.randint(1000, 9999)
    user_msg = _build_user_message(slots, seed)
    last_error: str | None = None

    for attempt in range(_MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {"role": "system", "content": _system_prompt()},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=4500,
                temperature=0.85,
            )
            raw = response.choices[0].message.content.strip()
            parsed = _parse_llm_questions(raw, slots)
            questions: list[dict] = []
            for i, slot in enumerate(slots):
                try:
                    questions.append(_to_session_question(parsed[i], slot))
                except (ValueError, KeyError):
                    fallback_q = _procedural_for_slot(slot)
                    if fallback_q:
                        questions.append(fallback_q)
            if len(questions) >= count:
                random.shuffle(questions)
                return questions[:count]
            raise ValueError("Too many LLM questions failed validation")
        except (ValueError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            last_error = str(exc)
            user_msg = (
                _build_user_message(slots, seed)
                + f"\n\nYour previous response was invalid ({last_error}). "
                "Use separate instruction and equation fields. Return ONLY a valid JSON array."
            )

    if fallback:
        return fallback(config, count)

    raise ValueError(last_error or "LLM question generation failed")
