"""Grade Arjun Course 3 MCQs with equivalent numeric/fraction forms."""

from __future__ import annotations

import re

from numeric_expression_eval import (
    ensure_numeric_answer_key,
    ensure_simplest_form_answer,
    options_equivalent,
)

_MULTI_ANSWER_RE = re.compile(
    r"which answer\(s\)|all of the above|more than one|both .+ and",
    re.I,
)


def finalize_question(question: dict) -> dict:
    """Validate and auto-correct numeric answer keys before serving an MCQ."""
    out = dict(question)
    opts = out.get("options")
    ans = out.get("answer")
    if not isinstance(opts, list) or len(opts) != 4:
        return out
    if not isinstance(ans, int) or ans not in range(4):
        return out
    options_raw = [str(o) for o in opts]
    stem = str(out.get("question", ""))
    if _MULTI_ANSWER_RE.search(stem) or re.search(r"\bboth\b", options_raw[ans], re.I):
        return out
    try:
        ans = ensure_numeric_answer_key(stem, options_raw, ans)
    except ValueError:
        pass
    try:
        ans = ensure_simplest_form_answer(stem, options_raw, ans)
    except ValueError:
        pass
    out["answer"] = ans
    return out


def finalize_questions(questions: list[dict]) -> list[dict]:
    return [finalize_question(q) for q in questions]


def is_pick_correct(question: dict, picked_index: int) -> bool:
    """True when the picked option matches the keyed answer or an equivalent value."""
    keyed = question.get("answer")
    if not isinstance(keyed, int):
        return False
    if picked_index == keyed:
        return True
    opts = question.get("options") or []
    if picked_index < 0 or picked_index >= len(opts) or keyed < 0 or keyed >= len(opts):
        return False
    picked = str(opts[picked_index])
    correct = str(opts[keyed])
    return options_equivalent(picked, correct)
