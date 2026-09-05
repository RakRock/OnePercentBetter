"""Independent question validation — separate from generation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)
    verified_answer: int | None = None


def _require_fields(q: dict, names: list[str]) -> list[str]:
    return [f"Missing field: {name}" for name in names if not q.get(name) and q.get(name) != 0]


def validate_question(q: dict, *, program: str = "auto") -> ValidationResult:
    """Validate structure, metadata, and (when possible) independently verify the answer."""
    errors: list[str] = []
    options = q.get("options") or []
    if not isinstance(options, list) or len(options) != 4:
        errors.append("Must have exactly 4 options")
    elif len({str(o).strip().lower() for o in options}) < 4:
        errors.append("Options must be distinct")

    answer = q.get("answer")
    if not isinstance(answer, int) or answer not in range(4):
        errors.append("Answer must be an integer index 0-3")

    if not str(q.get("question", "")).strip() and not q.get("equation"):
        errors.append("Missing question text")

    if program in ("linear", "auto") and (q.get("equation") or q.get("strategy")):
        return _validate_linear(q, errors)

    if program in ("harshit", "generic", "auto"):
        return _validate_generic(q, errors)

    if program == "spanish":
        return _validate_spanish(q, errors)

    return ValidationResult(ok=not errors, errors=errors)


def _validate_spanish(q: dict, errors: list[str]) -> ValidationResult:
    text = str(q.get("question", "")).strip()
    options = [str(o).strip() for o in q.get("options", [])]
    if len(text) < 8:
        errors.append("Question too short")
    if len(options) != 4 or len({o.lower() for o in options}) < 4:
        errors.append("Need 4 distinct options")
    answer = q.get("answer")
    if not isinstance(answer, int) or answer not in range(4):
        errors.append("Answer must be 0-3")
    if not str(q.get("explanation", "")).strip():
        errors.append("Missing explanation")
    if not (q.get("category") or q.get("category_label")):
        errors.append("Missing category metadata")
    return ValidationResult(ok=not errors, errors=errors)


def _validate_linear(q: dict, errors: list[str]) -> ValidationResult:
    import arjun_linear_equation_strategies as leqs

    sid = q.get("strategy")
    lvl = q.get("level")
    if sid is None or not lvl:
        errors.extend(_require_fields(q, ["strategy", "level"]))
        sid, lvl = sid or 0, lvl or "?"

    q = leqs.attach_question_parts(dict(q))
    eq = str(q.get("equation", "")).strip()
    if not eq and not str(q.get("question", "")).strip():
        errors.append("Missing question text")

    if eq and sid and lvl and sid in leqs.STRATEGIES:
        try:
            from arjun_linear_equation_llm import _equation_fits_slot

            if not _equation_fits_slot(eq, int(sid), str(lvl)):
                errors.append(f"Equation does not fit strategy {sid} level {lvl}")
        except Exception:
            pass

    options = [str(o) for o in q.get("options", [])]
    verified: int | None = None
    if eq and len(options) == 4:
        verified = leqs.resolve_x_answer_index(
            eq,
            options,
            sid=int(sid) if sid else 0,
            lvl=str(lvl),
            instruction=str(q.get("instruction", "")),
            followup=str(q.get("followup", "")),
        )
        if verified is not None and isinstance(q.get("answer"), int) and verified != q["answer"]:
            errors.append(
                f"Answer key mismatch: indexed {q['answer']} but equation verifies index {verified}"
            )
        elif verified is None and leqs.question_asks_for_x_value(
            int(sid) if sid else 0,
            str(lvl),
            str(q.get("instruction", "")),
            str(q.get("followup", "")),
        ) and leqs.options_look_like_x_values(options):
            errors.append("Could not independently verify numeric x answer")

    if not str(q.get("explanation", "")).strip():
        errors.append("Missing explanation")

    return ValidationResult(ok=not errors, errors=errors, verified_answer=verified)


def _validate_generic(q: dict, errors: list[str]) -> ValidationResult:
    from llm_question_format import is_quality_practice_question, validate_numerical_format

    text = str(q.get("question", "")).strip()
    options = [str(o) for o in q.get("options", [])]
    if text and options:
        try:
            validate_numerical_format(text, options)
        except ValueError as exc:
            errors.append(str(exc))
        if not is_quality_practice_question(text, options):
            errors.append("Question failed quality filter")

    if not str(q.get("explanation", "")).strip():
        errors.append("Missing explanation")

    category = q.get("category") or q.get("category_label")
    if not category:
        errors.append("Missing category metadata")

    return ValidationResult(ok=not errors, errors=errors)
