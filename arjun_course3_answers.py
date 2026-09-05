"""Grade Arjun Course 3 MCQs with equivalent numeric/fraction forms."""

from __future__ import annotations

from numeric_expression_eval import options_equivalent


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
