"""CBSE-style AI marking of unit-test written work from a paper photo."""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path

from openai import APIConnectionError, APITimeoutError, OpenAIError

import harshit_class10_unit_test_uploads as h10utu
from xai_client import make_xai_client

XAI_VISION_MODEL = "grok-4.6"
GRADE_TIMEOUT_SEC = 180.0

CBSE_EXAMINER_RULES = """You are a CBSE Class 10 Mathematics (Standard, Code 041) examiner.
Follow the official Maths Standard Marking Scheme style (SQP 2025-26):

- Award marks only for steps that are visibly present in the student's written work.
- Use half-marks (0.5) where the marking scheme allows.
- Award method marks if the method is correct even when the final arithmetic is wrong.
- Do not award marks for a correct final answer reached by a wrong method.
- Accept any equivalent correct method (OR branch).
- For graphs and constructions: award figure/labels separately from calculation.
- If a written question is not visible in the photo, award 0 and note "not seen".
- Do not invent work that is not on the page.
"""


def clamp_half_mark(value: float, maximum: float) -> float:
    maximum = max(0.0, float(maximum))
    raw = max(0.0, min(float(value), maximum))
    return round(raw * 2.0) / 2.0


def marking_scheme_for_question(q: dict) -> dict:
    """Prefer curated MS steps; otherwise split rubric marks in ½-mark units."""
    existing = q.get("marking_scheme")
    if isinstance(existing, dict) and existing.get("steps"):
        steps = []
        for step in existing["steps"]:
            steps.append(
                {
                    "marks": float(step.get("marks", 0)),
                    "text": str(step.get("text", "")).strip(),
                }
            )
        return {
            "source": str(existing.get("source") or "seed"),
            "steps": steps,
            "or": list(existing.get("or") or []),
            "examiner_notes": list(existing.get("examiner_notes") or []),
        }

    marks = float(q.get("marks", 0))
    rubric = [str(item).strip() for item in (q.get("rubric") or []) if str(item).strip()]
    if not rubric:
        rubric = ["Correct complete solution with working"]
    units = max(1, int(round(marks * 2)))
    n = len(rubric)
    base, rem = divmod(units, n)
    steps = []
    for i, text in enumerate(rubric):
        extra = 1 if i < rem else 0
        steps.append({"marks": (base + extra) / 2.0, "text": text})
    return {
        "source": "rubric",
        "steps": steps,
        "or": [],
        "examiner_notes": [
            "Award method marks for a correct approach even if arithmetic slips."
        ],
    }


def _safe_image_bytes(path: str) -> tuple[bytes, str] | None:
    raw = Path(path)
    try:
        resolved = raw.resolve()
        root = h10utu.WORK_ROOT.resolve()
    except OSError:
        return None
    if root not in resolved.parents and resolved != root:
        return None
    ext = resolved.suffix.lower()
    if ext not in h10utu.ALLOWED_EXTENSIONS:
        return None
    if not resolved.is_file():
        return None
    data = resolved.read_bytes()
    if not data or len(data) > h10utu.MAX_FILE_BYTES:
        return None
    mime = "image/png" if ext == ".png" else "image/jpeg"
    return data, mime


def image_data_url(path: str) -> str | None:
    loaded = _safe_image_bytes(path)
    if not loaded:
        return None
    data, mime = loaded
    encoded = base64.standard_b64encode(data).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def parse_grade_payload(raw: str) -> dict:
    text = (raw or "").strip()
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fenced:
        text = fenced.group(1).strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object in examiner response.")
    data = json.loads(match.group())
    if not isinstance(data, dict):
        raise ValueError("Examiner JSON must be an object.")
    return data


def normalize_question_grades(payload: dict, written: list[dict]) -> dict[int, dict]:
    by_num: dict[int, dict] = {}
    items = payload.get("questions")
    if not isinstance(items, list):
        items = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            q_num = int(item.get("q_num"))
        except (TypeError, ValueError):
            continue
        by_num[q_num] = item

    out: dict[int, dict] = {}
    for q in written:
        q_num = int(q.get("q_num", 0))
        max_marks = float(q.get("marks", 0))
        scheme = marking_scheme_for_question(q)
        raw = by_num.get(q_num, {})
        steps_out = []
        raw_steps = raw.get("steps") if isinstance(raw.get("steps"), list) else []
        for i, step in enumerate(scheme["steps"]):
            step_max = float(step.get("marks", 0))
            awarded = 0.0
            note = "not seen"
            if i < len(raw_steps) and isinstance(raw_steps[i], dict):
                try:
                    awarded = float(raw_steps[i].get("awarded", 0))
                except (TypeError, ValueError):
                    awarded = 0.0
                note = str(raw_steps[i].get("note") or "").strip() or note
            steps_out.append(
                {
                    "text": step["text"],
                    "awarded": clamp_half_mark(awarded, step_max),
                    "max": step_max,
                    "note": note,
                }
            )
        if raw and "earned" in raw:
            try:
                earned = clamp_half_mark(float(raw.get("earned", 0)), max_marks)
            except (TypeError, ValueError):
                earned = sum(s["awarded"] for s in steps_out)
        else:
            earned = sum(s["awarded"] for s in steps_out)
        earned = clamp_half_mark(earned, max_marks)
        out[q_num] = {
            "earned": earned,
            "max": max_marks,
            "steps": steps_out,
            "feedback": str(raw.get("feedback") or "").strip(),
            "corrections": str(raw.get("corrections") or "").strip(),
            "confidence": str(raw.get("confidence") or "medium").strip().lower(),
        }
    return out


def _written_prompt(written: list[dict]) -> str:
    blocks = []
    for q in written:
        scheme = marking_scheme_for_question(q)
        step_lines = "\n".join(
            f"  - {step['marks']:g} mark(s): {step['text']}" for step in scheme["steps"]
        )
        notes = scheme.get("examiner_notes") or []
        note_line = "; ".join(str(n) for n in notes) if notes else "None"
        blocks.append(
            f"Q{q.get('q_num')} · Section {q.get('section')} · {q.get('marks')} marks\n"
            f"Question: {q.get('question')}\n"
            f"Examiner key (for marking only): {q.get('model_answer')}\n"
            f"Marking scheme:\n{step_lines}\n"
            f"Notes: {note_line}"
        )
    joined = "\n\n".join(blocks)
    return f"""{CBSE_EXAMINER_RULES}

The attached photo is the student's written paper for Sections B–D of a 15-mark unit test.
Grade ONLY the written questions below.

{joined}

Return JSON only:
{{
  "questions": [
    {{
      "q_num": 6,
      "earned": 1.5,
      "max": 2,
      "steps": [
        {{"text": "scheme step", "awarded": 1, "max": 1, "note": "why"}}
      ],
      "feedback": "what was correct",
      "corrections": "what to fix, in brief",
      "confidence": "high"
    }}
  ]
}}
Use the same q_num values. awarded + earned must be 0.5 increments and never exceed max.
"""


def grade_written_paper(
    *,
    written_questions: list[dict],
    image_paths: list[str],
    api_key: str,
) -> tuple[dict[int, dict], str | None]:
    """Mark all written questions from the paper photo(s). Returns q_num -> grade."""
    if not written_questions:
        return {}, None
    if not api_key:
        return {}, "AI examiner is not configured (missing XAI_API_KEY)."

    urls: list[str] = []
    for path in image_paths:
        url = image_data_url(path)
        if url:
            urls.append(url)
    if not urls:
        return {}, "Could not read the saved paper photo."

    content: list[dict] = [{"type": "text", "text": _written_prompt(written_questions)}]
    for url in urls:
        content.append({"type": "image_url", "image_url": {"url": url, "detail": "high"}})

    try:
        client = make_xai_client(api_key, timeout=GRADE_TIMEOUT_SEC)
        response = client.chat.completions.create(
            model=XAI_VISION_MODEL,
            messages=[{"role": "user", "content": content}],
            temperature=0,
        )
        raw = (response.choices[0].message.content or "").strip()
        payload = parse_grade_payload(raw)
        return normalize_question_grades(payload, written_questions), None
    except (APIConnectionError, APITimeoutError) as exc:
        return {}, f"Could not reach the examiner model: {exc}"
    except (OpenAIError, ValueError, json.JSONDecodeError) as exc:
        return {}, f"Examiner marking failed: {exc}"


def apply_grades_to_responses(
    questions: list[dict],
    responses: list[dict],
    grades: dict[int, dict],
) -> list[dict]:
    out = []
    for q, resp in zip(questions, responses):
        row = dict(resp)
        if q.get("type") == "written":
            q_num = int(q.get("q_num", 0))
            if q_num in grades:
                row["ai_grade"] = grades[q_num]
        out.append(row)
    return out
