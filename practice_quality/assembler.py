"""Assemble validated, deduplicated practice sessions with slot-preserving replacement."""

from __future__ import annotations

import random
from collections.abc import Callable
from typing import Any

from practice_quality.dedup import fingerprints_for_question, is_duplicate_of_any, register_fingerprints
from practice_quality.validator import ValidationResult, validate_question


def _attach_slot(q: dict, slot: dict[str, Any]) -> dict:
    out = dict(q)
    for key, val in slot.items():
        if key.startswith("_"):
            continue
        out.setdefault(key, val)
    return out


def _try_accept(
    q: dict | None,
    *,
    slot: dict[str, Any],
    used_ids: set[str],
    seen_fps: set[str],
    program: str,
) -> dict | None:
    if not q:
        return None
    q = _attach_slot(q, slot)
    qid = str(q.get("id", ""))
    if qid and qid in used_ids:
        return None
    if is_duplicate_of_any(q, seen_fps):
        return None
    vr = validate_question(q, program=program)
    if not vr.ok:
        return None
    if vr.verified_answer is not None:
        q = dict(q)
        q["answer"] = vr.verified_answer
    used_ids.add(qid)
    register_fingerprints(q, seen_fps)
    return q


def qa_and_assemble(
    slots: list[dict[str, Any]],
    generate_for_slot: Callable[[dict[str, Any], set[str], set[str]], dict | None],
    *,
    initial: list[dict | None] | None = None,
    exclude_ids: set[str] | None = None,
    exclude_keys: set[str] | None = None,
    program: str = "auto",
    max_attempts_per_slot: int = 28,
) -> list[dict]:
    """
    Build a session preserving slot order and strategy/difficulty distribution.

    For each slot, accept a validated unique question or generate replacements until
    max_attempts. Never shrinks the session — always returns len(slots) questions
    when generation can satisfy constraints.
    """
    used_ids: set[str] = set(exclude_ids or ())
    seen_fps: set[str] = set(exclude_keys or ())
    result: list[dict | None] = [None] * len(slots)

    initial = initial or []
    for i, slot in enumerate(slots):
        if i < len(initial) and initial[i]:
            accepted = _try_accept(
                initial[i], slot=slot, used_ids=used_ids, seen_fps=seen_fps, program=program
            )
            if accepted:
                result[i] = accepted

    for i, slot in enumerate(slots):
        if result[i] is not None:
            continue
        for _ in range(max_attempts_per_slot):
            candidate = generate_for_slot(slot, used_ids, seen_fps)
            accepted = _try_accept(
                candidate, slot=slot, used_ids=used_ids, seen_fps=seen_fps, program=program
            )
            if accepted:
                result[i] = accepted
                break

    missing = [i for i, q in enumerate(result) if q is None]
    if missing:
        raise ValueError(
            f"Could not fill {len(missing)} slot(s) after validation/dedup "
            f"(indices: {missing[:5]}{'...' if len(missing) > 5 else ''})"
        )

    # Final QA sweep — replace any duplicate that slipped through.
    for i in range(len(result)):
        other_fps = {fp for k, q in enumerate(result) if k != i for fp in fingerprints_for_question(q)}
        if is_duplicate_of_any(result[i], other_fps):
            slot = slots[i]
            replaced = None
            for _ in range(max_attempts_per_slot):
                candidate = generate_for_slot(slot, used_ids, seen_fps)
                accepted = _try_accept(
                    candidate, slot=slot, used_ids=used_ids, seen_fps=seen_fps, program=program
                )
                if accepted and not is_duplicate_of_any(accepted, other_fps):
                    replaced = accepted
                    break
            if replaced:
                result[i] = replaced
            else:
                raise ValueError(f"Final QA found duplicate at slot {i} and could not replace")

    random.shuffle(result)
    return result  # type: ignore[return-value]


def validate_batch(questions: list[dict], *, program: str = "auto") -> list[ValidationResult]:
    return [validate_question(q, program=program) for q in questions]
