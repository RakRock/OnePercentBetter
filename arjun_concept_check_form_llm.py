"""Generate a fresh Math 3 Concept Check MCQ set from CC1–CC5 seeds + lesson notes."""

from __future__ import annotations

import json
import random
import re
import time

from openai import APIConnectionError, APITimeoutError, OpenAIError

import arjun_concept_check_form as ccform
import arjun_course3_answers as c3ans
import arjun_course3_content as c3
from llm_question_format import KID_NUMERIC_FORMAT_RULES, NUMERIC_RETRY_HINT, validate_numerical_format
from numeric_expression_eval import (
    ensure_numeric_answer_key,
    ensure_simplest_form_answer,
    validate_distinct_options,
    validate_explanation_matches_key,
)
from xai_client import make_xai_client

XAI_MODEL = "grok-3-mini"
_MAX_RETRIES = 3
_NOTES_CHAR_LIMIT = 12000


def _notes_for_section(section_id: str) -> str:
    info = ccform.get_section(section_id)
    if not info:
        return ""
    unit_id = int(info.get("unit_id") or 1)
    unit = c3.get_unit(unit_id)
    wanted = list(info.get("note_files") or [])
    activities = {str(a.get("file")): a for a in (unit or {}).get("activities") or []}
    parts: list[str] = []
    for fname in wanted:
        act = activities.get(fname)
        if act and unit:
            text = c3.load_activity_markdown(unit, act)
            title = act.get("title", fname)
        else:
            path = c3.unit_notes_dir(unit_id) / fname
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
            title = fname
        text = re.sub(r"\[KEY\]|\[/KEY\]", "", text)
        text = re.sub(r"\[DIAGRAM:[^\]]+\]", "", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if text:
            parts.append(f"# {title}\n{text}")
    joined = "\n\n".join(parts)
    return joined[:_NOTES_CHAR_LIMIT]


def _seed_block(seeds: list[dict]) -> str:
    lines = [
        "SEED PROBLEMS from Arjun's actual Friday Concept Check papers (CC1–CC5) "
        "or the Unit 6 packets VI-1 Representing Patterns, VI-2 Using Patterns, "
        "and VI-3 Solving Linear Equations with Models, or Unit 7 packet VII-1 Multi-Step Equations.",
        "Match these stem types. Do NOT copy the numbers, names, or stories.",
    ]
    for i, seed in enumerate(seeds, start=1):
        lines.append(
            f"{i}. [{seed.get('stem')}] ({seed.get('paper')}) {seed.get('question')} "
            f"| correct: {seed['options'][seed['answer']]}"
        )
    return "\n".join(lines)


def _system_prompt(section: dict, count: int) -> str:
    return f"""You write Math 3 CONCEPT CHECK multiple-choice questions for an 11-year-old (Arjun).

This is a Friday Concept Check for ONE section of the school paper:
{section['roman']}) {section['title']} — {section['short']}

School directions (put the same idea in every stem):
Complete each problem. Show the key steps in the explanation. All answers in simplest form.
Final exponential answers use only positive exponents. Scientific notation must be a × 10ⁿ with 1 ≤ |a| < 10.

RULES:
- Return a JSON array with exactly {count} question objects.
- Exactly 4 options; "answer" is the 0-based index of the correct option.
- Cover DIFFERENT seed stem types. Do not write {count} questions of the same type.
- New numbers, names, and stories every time. Never reuse a seed's numbers.
- No images — describe figures in words (for example "Figure 1 has 1 square, Figure 2 has 4").
- Wrong options = the slips kids make on these papers (forgot LCD, treated perimeter as area, left a negative exponent, forgot to rewrite 12.4×10¹⁸ as 1.24×10¹⁹).
- Explanation must include Step 1 and Step 2 and land on the correct option.
- For repeating-decimal seeds, say clearly which digits have the bar.
- For Representing Patterns (VI-1): describe figures in words (Figure 1 has __ dots). Ask for the expression in n, the constant difference, n to substitute, or a far figure (51st/100th). Do not ask the student to draw.
- For Using Patterns (VI-2): square n², rectangular n(n+1), triangular n(n+1)/2. Square/rect/triangle counts do NOT have a constant difference. Joined-polygon perimeters DO: pentagons add 3 (hide 2 sides), octagons add 6. Describe figures in words. Do not ask the student to draw.
- For Solving Equations with Models (VI-3): a bag is x cubes, a cube is 1, a balanced scale is an equation. Ask for the equation, cubes per bag, or the inverse-operation steps. Describe pans in words (do not ask the student to draw).
- For Multi-Step Equations (VII-1): variables on both sides. Steps: simplify/distribute, move variables, move constants, solve. Include a bags-and-cubes stem and a “too many bags → combine like terms” stem. Wrong options = dropped a distribute sign, combined unlike terms, or divided before moving the other variable. Do not ask the student to draw.
{KID_NUMERIC_FORMAT_RULES}

Respond with ONLY a JSON array:
[{{"stem": "evaluate_mixed", "question": "...", "options": ["...", "...", "...", "..."], "answer": 0, "explanation": "..."}}]
"""


def _normalize(q: dict, section_id: str, allowed_stems: set[str]) -> dict:
    if not isinstance(q, dict):
        raise ValueError("Question must be an object")
    if not isinstance(q.get("options"), list) or len(q["options"]) != 4:
        raise ValueError("Need exactly 4 options")
    ans = q.get("answer")
    if not isinstance(ans, int) or ans not in range(4):
        raise ValueError("answer must be 0-3")
    options_raw = [str(o) for o in q["options"]]
    question = str(q.get("question", "")).strip()
    if not question:
        raise ValueError("Empty question")
    validate_numerical_format(question, options_raw)
    validate_distinct_options(options_raw)
    explanation = str(q.get("explanation", "")).strip()
    ans = ensure_numeric_answer_key(question, options_raw, ans)
    ans = ensure_simplest_form_answer(question, options_raw, ans)
    validate_explanation_matches_key(explanation, options_raw, ans)
    correct = options_raw[ans]
    indices = list(range(4))
    random.shuffle(indices)
    options = [options_raw[j] for j in indices]
    answer = options.index(correct)
    stem = str(q.get("stem") or "mixed").strip()
    if stem not in allowed_stems:
        stem = "mixed"
    stamp = int(time.time() * 1000) % 1_000_000
    item = {
        "id": f"ccform_{section_id}_{stamp}_{random.randint(100, 999)}",
        "section": section_id,
        "stem": stem,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "source": "concept_check_form",
        "origin": "llm",
        "category_label": stem.replace("_", " ").title(),
    }
    return c3ans.finalize_question(item)


def _parse(raw: str, section_id: str, allowed_stems: set[str]) -> list[dict]:
    match = re.search(r"\[[\s\S]*\]", raw or "")
    if not match:
        raise ValueError("No JSON array in response")
    items = json.loads(match.group())
    if not isinstance(items, list) or not items:
        raise ValueError("Expected a non-empty JSON array")
    out: list[dict] = []
    errors: list[str] = []
    for q in items:
        try:
            out.append(_normalize(q, section_id, allowed_stems))
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(str(exc))
    if not out:
        raise ValueError(errors[0] if errors else "No valid questions")
    return out


def generate_section_set(xai_api_key: str, section_id: str, *, count: int | None = None) -> list[dict]:
    """Fresh Grok MCQs for one Concept Check section. Raises on hard API failure."""
    section = ccform.get_section(section_id)
    if not section:
        raise ValueError(f"Unknown section {section_id}")
    seeds = ccform.seeds_for_section(section["id"])
    n = int(count or section["session_count"])
    allowed = {str(s.get("stem")) for s in seeds}
    notes = _notes_for_section(section["id"])
    user_msg = (
        f"Generate exactly {n} different Concept Check questions for "
        f"{section['roman']}) {section['title']}.\n\n"
        f"{_seed_block(seeds)}\n\n"
        f"LESSON NOTES (use the methods taught here):\n{notes}\n\n"
        f"Session seed: {random.randint(1000, 9999)} — new numbers this time.\n"
        "Return ONLY the JSON array."
    )
    system = _system_prompt(section, n)
    client = make_xai_client(xai_api_key)
    last_err = ""
    last_partial: list[dict] = []
    for _attempt in range(_MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=XAI_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=4500,
                temperature=0.95,
            )
            raw = (resp.choices[0].message.content or "").strip()
            out = _parse(raw, section["id"], allowed)
            if len(out) >= n:
                return out[:n]
            last_partial = out
            raise ValueError(f"Got {len(out)} valid questions, need {n}")
        except (APIConnectionError, APITimeoutError, OpenAIError) as exc:
            last_err = str(exc)
            break
        except (ValueError, json.JSONDecodeError, KeyError, TypeError) as exc:
            last_err = str(exc)
            user_msg += f"\n\nInvalid prior response ({last_err}). Need exactly {n} valid questions. {NUMERIC_RETRY_HINT}"
    if last_partial:
        return _top_up_from_seeds(section["id"], last_partial, n)
    raise RuntimeError(last_err or "Grok did not return a usable set")


def _shuffle_seed(seed: dict) -> dict:
    item = dict(seed)
    opts = list(item["options"])
    correct = opts[item["answer"]]
    random.shuffle(opts)
    item["options"] = opts
    item["answer"] = opts.index(correct)
    item["origin"] = item.get("origin") or "seed_fallback"
    item.setdefault("category_label", str(item.get("stem", "")).replace("_", " ").title())
    return c3ans.finalize_question(item)


def _top_up_from_seeds(section_id: str, questions: list[dict], count: int) -> list[dict]:
    """Fill a short set from unused paper seeds so the session always has `count` items."""
    out = list(questions)
    if len(out) >= count:
        return out[:count]
    used_ids = {str(q.get("id")) for q in out}
    used_text = {str(q.get("question", "")).strip().lower() for q in out}
    extras = []
    for seed in ccform.seeds_for_section(section_id):
        qid = str(seed.get("id"))
        text = str(seed.get("question", "")).strip().lower()
        if qid in used_ids or text in used_text:
            continue
        extras.append(_shuffle_seed(seed))
        used_ids.add(qid)
        used_text.add(text)
    random.shuffle(extras)
    out.extend(extras)
    if len(out) < count:
        # Recycle remaining seeds rather than return a short paper.
        pool = [_shuffle_seed(s) for s in ccform.seeds_for_section(section_id)]
        random.shuffle(pool)
        i = 0
        while len(out) < count and pool:
            extra = dict(pool[i % len(pool)])
            extra["id"] = f"{extra.get('id', 'seed')}_fill_{len(out)}"
            out.append(extra)
            i += 1
    return out[:count]


def fallback_seed_set(section_id: str, *, count: int | None = None) -> list[dict]:
    """Shuffled copies of the paper seeds if Grok is unavailable."""
    section = ccform.get_section(section_id)
    n = int(count or (section["session_count"] if section else 5))
    return _top_up_from_seeds(section_id, [], n)
