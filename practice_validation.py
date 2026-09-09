"""Generate practice questions, simulate random answers, and email validation audits."""

from __future__ import annotations

import os
import random
from dataclasses import dataclass
from typing import Callable

import arjun_course3_answers as c3ans
import arjun_course3_content as c3
import arjun_course3_practice as c3p
import arjun_course3_week as c3week
import arjun_edgenuity_course3_content as ec3
import arjun_edgenuity_course3_practice as ec3p
import arjun_edgenuity_course3_week as ec3week
from arjun_course3_concept_check_store import question_dedup_key


@dataclass(frozen=True)
class PracticeAppSpec:
    key: str
    label: str
    student_name: str
    unit_count: int
    unit_id_label: str
    default_config: Callable[[int], dict]
    get_unit_info: Callable[[int], dict]
    get_categories: Callable[[int], dict]
    build_batch: Callable[..., list[dict]]
    build_report: Callable[..., dict]
    is_pick_correct: Callable[[dict, int], bool]
    fill_from_bank: Callable[..., None] | None = None


def _c3_batch(
    unit_id: int,
    batch_size: int,
    config: dict,
    exclude_ids: set[str],
    use_llm: bool,
    api_key: str | None,
) -> list[dict]:
    return c3p.build_daily_set(
        count=batch_size,
        unit_id=unit_id,
        exclude_ids=exclude_ids,
        use_llm=use_llm,
        xai_api_key=api_key,
        week_config=config,
    )


def _ec3_batch(
    unit_id: int,
    batch_size: int,
    config: dict,
    exclude_ids: set[str],
    use_llm: bool,
    api_key: str | None,
) -> list[dict]:
    return ec3p.build_daily_set(
        count=batch_size,
        unit_id=unit_id,
        exclude_ids=exclude_ids,
        use_llm=use_llm,
        xai_api_key=api_key,
        week_config=config,
    )


def _c3_fill(unit_id: int, questions: list[dict], seen_keys: set[str], count: int) -> None:
    bank = c3p.QUESTION_BANK_BY_UNIT.get(unit_id, [])
    _shuffle_fill_bank(bank, questions, seen_keys, count)


def _ec3_fill(unit_id: int, questions: list[dict], seen_keys: set[str], count: int) -> None:
    bank = ec3p.QUESTION_BANK_BY_UNIT.get(unit_id, [])
    _shuffle_fill_bank(bank, questions, seen_keys, count)


def _harshit_prereq_batch(
    unit_id: int,
    batch_size: int,
    config: dict,
    exclude_ids: set[str],
    use_llm: bool,
    api_key: str | None,
) -> list[dict]:
    import harshit_prereq_practice as hpp

    cfg = {**config, "_exclude_ids": list(exclude_ids), "prereq_id": unit_id}
    questions, _err = hpp.build_session_set(
        unit_id,
        cfg,
        count=batch_size,
        xai_api_key=api_key if use_llm else None,
    )
    return questions


def _harshit_prereq_fill(unit_id: int, questions: list[dict], seen_keys: set[str], count: int) -> None:
    import harshit_prereq_practice as hpp
    import harshit_prereq_topics as hpt

    cfg = hpt.default_week_config(unit_id)
    pool = hpp._fill_from_bank_and_templates(unit_id, cfg, max(count, 50))
    _merge_pool(pool, questions, seen_keys, count)


def _harshit_prereq_unit(prereq_id: int) -> dict:
    titles = {
        1: "Number Systems",
        2: "Algebra",
        3: "Coordinate Geometry",
        4: "Geometry",
        5: "Mensuration",
        6: "Data Handling",
    }
    return {"title": titles.get(prereq_id, f"PreReq {prereq_id}"), "subtitle": "NCERT Math PreReq"}


def _harshit_prereq_categories(prereq_id: int) -> dict:
    import harshit_prereq_topics as hpt

    return {
        str(tid): {"name": info.get("name", str(tid))}
        for tid, info in hpt.topics_for_prereq(prereq_id).items()
    }


def _harshit_class10_batch(
    unit_id: int,
    batch_size: int,
    config: dict,
    exclude_ids: set[str],
    use_llm: bool,
    api_key: str | None,
) -> list[dict]:
    import harshit_class10_practice as h10p

    cfg = {**config, "unit_id": unit_id, "_exclude_ids": list(exclude_ids)}
    questions, _err = h10p.build_session_set(
        unit_id,
        cfg,
        count=batch_size,
        xai_api_key=api_key if use_llm else None,
    )
    return questions


def _harshit_class10_fill(unit_id: int, questions: list[dict], seen_keys: set[str], count: int) -> None:
    import harshit_class10_practice as h10p
    import harshit_class10_topics as h10t

    cfg = h10t.default_week_config(unit_id)
    pool = h10p._fill_from_bank(unit_id, cfg, max(count, 50))
    _merge_pool(pool, questions, seen_keys, count)


def _harshit_class10_unit(unit_id: int) -> dict:
    import harshit_class10_units as h10u

    unit = h10u.get_unit(unit_id) or {}
    return {
        "title": unit.get("title", f"Unit {unit_id}"),
        "subtitle": unit.get("subtitle", "Class 10 Math"),
    }


def _harshit_class10_categories(unit_id: int) -> dict:
    import harshit_class10_topics as h10t

    return {
        str(tid): {"name": info.get("name", str(tid))}
        for tid, info in h10t.topics_for_unit(unit_id).items()
    }


def _science_batch(
    module_name: str,
    unit_id: int,
    batch_size: int,
    config: dict,
    exclude_ids: set[str],
    use_llm: bool,
    api_key: str | None,
) -> list[dict]:
    import importlib

    mod = importlib.import_module(f"harshit.{module_name}.practice")
    cfg = {**config, "unit_id": unit_id}
    questions, _err = mod.build_session_set(
        unit_id,
        cfg,
        count=batch_size,
        xai_api_key=api_key if use_llm else None,
    )
    return questions


def _science_fill(module_name: str, unit_id: int, questions: list[dict], seen_keys: set[str], count: int) -> None:
    import importlib

    topics_mod = importlib.import_module(f"harshit.{module_name}.topics")
    practice_mod = importlib.import_module(f"harshit.{module_name}.practice")
    cfg = topics_mod.default_week_config(unit_id)
    plan = practice_mod._slot_plan(unit_id, cfg, max(count, 50))
    pool: list[dict] = []
    used_ids: set[str] = set()
    used_keys: set[str] = set()
    for day_id, lvl in plan:
        slot = practice_mod._slot_dict(unit_id, day_id, lvl)
        q = practice_mod._generate_for_slot(slot, used_ids, used_keys)
        if q:
            pool.append(q)
            used_ids.add(str(q.get("id", "")))
    _merge_pool(pool, questions, seen_keys, count)


def _science_unit(module_name: str, unit_id: int) -> dict:
    import importlib

    content = importlib.import_module(f"harshit.{module_name}.content")
    meta = content.unit_meta(unit_id)
    return {"title": meta.get("title", f"Unit {unit_id}"), "subtitle": meta.get("subtitle", "")}


def _science_categories(module_name: str, unit_id: int) -> dict:
    import importlib

    topics_mod = importlib.import_module(f"harshit.{module_name}.topics")
    return {
        str(tid): {"name": info.get("name", str(tid))}
        for tid, info in topics_mod.topics_for_unit(unit_id).items()
    }


def _science_batch_physics(*args, **kwargs) -> list[dict]:
    return _science_batch("physics", *args, **kwargs)


def _science_batch_biology(*args, **kwargs) -> list[dict]:
    return _science_batch("biology", *args, **kwargs)


def _science_batch_chemistry(*args, **kwargs) -> list[dict]:
    return _science_batch("chemistry", *args, **kwargs)


def _science_fill_physics(unit_id, questions, seen_keys, count):
    return _science_fill("physics", unit_id, questions, seen_keys, count)


def _science_fill_biology(unit_id, questions, seen_keys, count):
    return _science_fill("biology", unit_id, questions, seen_keys, count)


def _science_fill_chemistry(unit_id, questions, seen_keys, count):
    return _science_fill("chemistry", unit_id, questions, seen_keys, count)


def _harshit_report(questions: list[dict], answers: list[dict], unit_id: int) -> dict:
    import harshit_prereq_practice as hpp

    return hpp.build_session_report(questions, answers, student_name="Harshit")


PRACTICE_APPS: dict[str, PracticeAppSpec] = {
    "course3": PracticeAppSpec(
        key="course3",
        label="Course 3 Math",
        student_name="Arjun",
        unit_count=5,
        unit_id_label="Unit",
        default_config=c3week.default_week_config,
        get_unit_info=lambda uid: c3.get_unit(uid) or {"title": f"Unit {uid}", "subtitle": ""},
        get_categories=c3p.get_categories,
        build_batch=_c3_batch,
        build_report=lambda qs, ans, uid: c3p.build_session_report(qs, ans, unit_id=uid),
        is_pick_correct=c3ans.is_pick_correct,
        fill_from_bank=_c3_fill,
    ),
    "edgenuity": PracticeAppSpec(
        key="edgenuity",
        label="Edgenuity Course 3",
        student_name="Arjun",
        unit_count=6,
        unit_id_label="Unit",
        default_config=ec3week.default_week_config,
        get_unit_info=lambda uid: ec3.get_unit(uid) or {"title": f"Unit {uid}", "subtitle": ""},
        get_categories=ec3p.get_categories,
        build_batch=_ec3_batch,
        build_report=lambda qs, ans, uid: ec3p.build_session_report(qs, ans, unit_id=uid),
        is_pick_correct=c3ans.is_pick_correct,
        fill_from_bank=_ec3_fill,
    ),
    "harshit_prereq": PracticeAppSpec(
        key="harshit_prereq",
        label="Harshit Math PreReq",
        student_name="Harshit",
        unit_count=6,
        unit_id_label="PreReq",
        default_config=lambda uid: __import__("harshit_prereq_topics", fromlist=["default_week_config"]).default_week_config(uid),
        get_unit_info=_harshit_prereq_unit,
        get_categories=_harshit_prereq_categories,
        build_batch=_harshit_prereq_batch,
        build_report=_harshit_report,
        is_pick_correct=__import__("harshit_math_answers", fromlist=["is_pick_correct"]).is_pick_correct,
        fill_from_bank=_harshit_prereq_fill,
    ),
    "harshit_class10": PracticeAppSpec(
        key="harshit_class10",
        label="Harshit Class 10 Math",
        student_name="Harshit",
        unit_count=14,
        unit_id_label="Unit",
        default_config=lambda uid: __import__("harshit_class10_topics", fromlist=["default_week_config"]).default_week_config(uid),
        get_unit_info=_harshit_class10_unit,
        get_categories=_harshit_class10_categories,
        build_batch=_harshit_class10_batch,
        build_report=_harshit_report,
        is_pick_correct=__import__("harshit_math_answers", fromlist=["is_pick_correct"]).is_pick_correct,
        fill_from_bank=_harshit_class10_fill,
    ),
    "harshit_physics": PracticeAppSpec(
        key="harshit_physics",
        label="Harshit Physics",
        student_name="Harshit",
        unit_count=4,
        unit_id_label="Unit",
        default_config=lambda uid: __import__("harshit.physics.topics", fromlist=["default_week_config"]).default_week_config(uid),
        get_unit_info=lambda uid: _science_unit("physics", uid),
        get_categories=lambda uid: _science_categories("physics", uid),
        build_batch=_science_batch_physics,
        build_report=_harshit_report,
        is_pick_correct=__import__("harshit_math_answers", fromlist=["is_pick_correct"]).is_pick_correct,
        fill_from_bank=_science_fill_physics,
    ),
    "harshit_biology": PracticeAppSpec(
        key="harshit_biology",
        label="Harshit Biology",
        student_name="Harshit",
        unit_count=4,
        unit_id_label="Unit",
        default_config=lambda uid: __import__("harshit.biology.topics", fromlist=["default_week_config"]).default_week_config(uid),
        get_unit_info=lambda uid: _science_unit("biology", uid),
        get_categories=lambda uid: _science_categories("biology", uid),
        build_batch=_science_batch_biology,
        build_report=_harshit_report,
        is_pick_correct=__import__("harshit_math_answers", fromlist=["is_pick_correct"]).is_pick_correct,
        fill_from_bank=_science_fill_biology,
    ),
    "harshit_chemistry": PracticeAppSpec(
        key="harshit_chemistry",
        label="Harshit Chemistry",
        student_name="Harshit",
        unit_count=4,
        unit_id_label="Unit",
        default_config=lambda uid: __import__("harshit.chemistry.topics", fromlist=["default_week_config"]).default_week_config(uid),
        get_unit_info=lambda uid: _science_unit("chemistry", uid),
        get_categories=lambda uid: _science_categories("chemistry", uid),
        build_batch=_science_batch_chemistry,
        build_report=_harshit_report,
        is_pick_correct=__import__("harshit_math_answers", fromlist=["is_pick_correct"]).is_pick_correct,
        fill_from_bank=_science_fill_chemistry,
    ),
}

# Back-compat alias
ARJUN_APPS = {k: v for k, v in PRACTICE_APPS.items() if v.student_name == "Arjun"}


def list_apps() -> list[PracticeAppSpec]:
    return list(PRACTICE_APPS.values())


def resolve_app(app_key: str) -> PracticeAppSpec:
    key = str(app_key).strip().lower()
    if key not in PRACTICE_APPS:
        allowed = ", ".join(sorted(PRACTICE_APPS))
        raise ValueError(f"Unknown app '{app_key}'. Choose one of: {allowed}")
    return PRACTICE_APPS[key]


def _question_dedup_key(q: dict) -> str:
    return question_dedup_key(str(q.get("question", "")), q.get("options"))


def _shuffle_fill_bank(
    bank: list[dict],
    questions: list[dict],
    seen_keys: set[str],
    count: int,
) -> None:
    pool = list(bank)
    random.shuffle(pool)
    for q in pool:
        if len(questions) >= count:
            break
        key = _question_dedup_key(q)
        if key in seen_keys:
            continue
        questions.append(dict(q))
        seen_keys.add(key)


def _merge_pool(
    pool: list[dict],
    questions: list[dict],
    seen_keys: set[str],
    count: int,
) -> None:
    random.shuffle(pool)
    for q in pool:
        if len(questions) >= count:
            break
        key = _question_dedup_key(q)
        if key in seen_keys:
            continue
        questions.append(dict(q))
        seen_keys.add(key)


def load_base_seed_questions(app_key: str, unit_id: int) -> list[dict]:
    """Static unit bank + built-in concept-check generators (excludes AI JSON bank)."""
    spec = resolve_app(app_key)
    if unit_id < 1 or unit_id > spec.unit_count:
        raise ValueError(f"{spec.unit_id_label} must be 1–{spec.unit_count} for {spec.label}")

    if app_key == "course3":
        from arjun_course3_concept_check import build_concept_check_bank
        from arjun_course3_practice import _BASE_BANK_BY_UNIT

        static = list(_BASE_BANK_BY_UNIT.get(unit_id, []))
        builtin = build_concept_check_bank(unit_id)
        return c3ans.finalize_questions(static + builtin)

    if app_key == "edgenuity":
        import arjun_edgenuity_course3_practice as ec3p

        return list(ec3p.QUESTION_BANK_BY_UNIT.get(unit_id, []))

    raise ValueError(f"Base-seed validation is not supported for app '{app_key}'")


def validate_question_structure(
    q: dict,
    *,
    is_pick_correct: Callable[[dict, int], bool],
) -> list[str]:
    """Return structural/key issues for one MCQ (empty list = OK)."""
    issues: list[str] = []
    qid = str(q.get("id", "?"))
    opts = list(q.get("options") or [])
    if len(opts) != 4:
        issues.append(f"{qid}: expected 4 options, got {len(opts)}")
    if not str(q.get("question", "")).strip():
        issues.append(f"{qid}: empty question stem")
    if not str(q.get("explanation", "")).strip():
        issues.append(f"{qid}: empty explanation")
    ans = q.get("answer")
    if not isinstance(ans, int) or ans not in range(4):
        issues.append(f"{qid}: answer index {ans!r} out of range")
    if len(opts) == 4:
        try:
            from numeric_expression_eval import validate_distinct_options

            validate_distinct_options([str(o) for o in opts])
        except Exception as exc:
            issues.append(f"{qid}: {exc}")
        if isinstance(ans, int) and ans in range(4) and not is_pick_correct(q, ans):
            issues.append(f"{qid}: keyed answer fails grading check")
    return issues


def run_base_seed_validation_audit(
    app_key: str,
    unit_id: int,
    *,
    seed: int | None = None,
    student_name: str | None = None,
) -> dict:
    """Validate every static + built-in seed question for a unit."""
    spec = resolve_app(app_key)
    unit = spec.get_unit_info(unit_id)
    questions = load_base_seed_questions(app_key, unit_id)
    structural_issues: list[str] = []
    for q in questions:
        structural_issues.extend(
            validate_question_structure(q, is_pick_correct=spec.is_pick_correct)
        )
    answers = simulate_random_answers(
        questions, is_pick_correct=spec.is_pick_correct, seed=seed
    )
    report = spec.build_report(questions, answers, unit_id)
    audit_rows = build_validation_audit_rows(
        questions,
        answers,
        categories=spec.get_categories(unit_id),
    )
    subtitle = unit.get("subtitle", "")
    if subtitle:
        subtitle = f"{subtitle} · base seed bank"
    else:
        subtitle = "base seed bank"
    return {
        "app": spec,
        "student_name": student_name or spec.student_name,
        "unit_id": unit_id,
        "unit_title": unit.get("title", f"{spec.unit_id_label} {unit_id}"),
        "unit_subtitle": subtitle,
        "questions": questions,
        "answers": answers,
        "report": report,
        "audit_rows": audit_rows,
        "generated_count": len(questions),
        "requested_count": len(questions),
        "structural_issues": structural_issues,
        "base_seed": True,
    }


def generate_validation_questions(
    app_key: str,
    unit_id: int,
    count: int = 100,
    *,
    use_llm: bool = False,
    xai_api_key: str | None = None,
    week_config: dict | None = None,
    seed: int | None = None,
) -> list[dict]:
    """Build up to ``count`` unique MCQs using the same paths as live practice."""
    if seed is not None:
        random.seed(seed)

    spec = resolve_app(app_key)
    if unit_id < 1 or unit_id > spec.unit_count:
        raise ValueError(f"{spec.unit_id_label} must be 1–{spec.unit_count} for {spec.label}")

    config = week_config or spec.default_config(unit_id)
    exclude_ids: set[str] = set()
    questions: list[dict] = []
    seen_keys: set[str] = set()
    stall_rounds = 0
    api_key = xai_api_key or os.environ.get("XAI_API_KEY")

    while len(questions) < count and stall_rounds < 8:
        batch_size = min(15, count - len(questions))
        batch = spec.build_batch(
            unit_id,
            batch_size,
            config,
            exclude_ids,
            use_llm and bool(api_key),
            api_key if use_llm else None,
        )
        added = 0
        for q in batch:
            key = _question_dedup_key(q)
            if key in seen_keys:
                continue
            questions.append(dict(q))
            seen_keys.add(key)
            qid = str(q.get("id", ""))
            if qid:
                exclude_ids.add(qid)
            added += 1
            if len(questions) >= count:
                break
        if added == 0:
            stall_rounds += 1
            if stall_rounds >= 3:
                exclude_ids.clear()
        else:
            stall_rounds = 0

    if len(questions) < count and spec.fill_from_bank:
        spec.fill_from_bank(unit_id, questions, seen_keys, count)

    return questions[:count]


def simulate_random_answers(
    questions: list[dict],
    *,
    is_pick_correct: Callable[[dict, int], bool] | None = None,
    seed: int | None = None,
) -> list[dict]:
    """Pick a random option for each question (same shape as live session answers)."""
    if seed is not None:
        random.seed(seed)

    grade = is_pick_correct or c3ans.is_pick_correct
    answers: list[dict] = []
    for q in questions:
        opts = list(q.get("options") or [])
        if len(opts) != 4:
            answers.append({"picked": "?", "correct_val": "?", "correct": False})
            continue
        picked_idx = random.randrange(4)
        keyed_idx = q.get("answer")
        if not isinstance(keyed_idx, int) or keyed_idx not in range(4):
            keyed_idx = 0
        answers.append(
            {
                "picked": str(opts[picked_idx]),
                "picked_index": picked_idx,
                "correct_val": str(opts[keyed_idx]),
                "keyed_index": keyed_idx,
                "correct": grade(q, picked_idx),
            }
        )
    return answers


def build_validation_audit_rows(
    questions: list[dict],
    answers: list[dict],
    *,
    categories: dict | None = None,
) -> list[dict]:
    """One review row per question for parent validation emails."""
    rows: list[dict] = []
    for idx, (q, ans) in enumerate(zip(questions, answers), start=1):
        cat_id = str(q.get("category", ""))
        cat_info = (categories or {}).get(cat_id, {})
        if not cat_info and cat_id.isdigit():
            cat_info = (categories or {}).get(int(cat_id), {})
        cat_label = q.get("category_label") or cat_info.get("name") or cat_id.replace("_", " ").title()
        opts = [str(o) for o in (q.get("options") or [])]
        keyed_idx = ans.get("keyed_index", q.get("answer"))
        if not isinstance(keyed_idx, int) or keyed_idx not in range(len(opts)):
            keyed_idx = int(q.get("answer", 0)) if isinstance(q.get("answer"), int) else 0
        rows.append(
            {
                "number": idx,
                "id": str(q.get("id", "")),
                "source": str(q.get("source", "")),
                "category": cat_label,
                "question": str(q.get("question", "")).strip(),
                "options": opts,
                "keyed_index": keyed_idx,
                "keyed_answer": opts[keyed_idx] if keyed_idx < len(opts) else "?",
                "picked": str(ans.get("picked", "?")),
                "picked_index": ans.get("picked_index"),
                "correct": bool(ans.get("correct")),
                "explanation": str(q.get("explanation", "")).strip(),
            }
        )
    return rows


def run_validation_audit(
    app_key: str,
    unit_id: int,
    count: int = 100,
    *,
    use_llm: bool = False,
    xai_api_key: str | None = None,
    week_config: dict | None = None,
    seed: int | None = None,
    student_name: str | None = None,
) -> dict:
    """Generate questions, simulate answers, and return a report payload for email."""
    spec = resolve_app(app_key)
    unit = spec.get_unit_info(unit_id)
    questions = generate_validation_questions(
        app_key,
        unit_id,
        count,
        use_llm=use_llm,
        xai_api_key=xai_api_key,
        week_config=week_config,
        seed=seed,
    )
    answers = simulate_random_answers(questions, is_pick_correct=spec.is_pick_correct, seed=seed)
    report = spec.build_report(questions, answers, unit_id)
    audit_rows = build_validation_audit_rows(
        questions,
        answers,
        categories=spec.get_categories(unit_id),
    )
    return {
        "app": spec,
        "student_name": student_name or spec.student_name,
        "unit_id": unit_id,
        "unit_title": unit.get("title", f"{spec.unit_id_label} {unit_id}"),
        "unit_subtitle": unit.get("subtitle", ""),
        "questions": questions,
        "answers": answers,
        "report": report,
        "audit_rows": audit_rows,
        "generated_count": len(questions),
        "requested_count": count,
    }
