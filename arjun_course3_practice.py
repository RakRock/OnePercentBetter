"""Arjun Course 3 Math — practice question banks and session builders (Units 1–5)."""

from __future__ import annotations

import random
from pathlib import Path

from arjun_course3_unit1_practice import (
    UNIT1_CATEGORIES,
    UNIT1_CATEGORY_ACTIVITY,
    UNIT1_QUESTION_BANK,
    UNIT1_REVISION_TIPS,
)
from arjun_course3_unit2_practice import (
    UNIT2_CATEGORIES,
    UNIT2_CATEGORY_ACTIVITY,
    UNIT2_QUESTION_BANK,
    UNIT2_REVISION_TIPS,
)
from arjun_course3_unit3_practice import (
    UNIT3_CATEGORIES,
    UNIT3_CATEGORY_ACTIVITY,
    UNIT3_QUESTION_BANK,
    UNIT3_REVISION_TIPS,
)
from arjun_course3_unit4_practice import (
    UNIT4_CATEGORIES,
    UNIT4_CATEGORY_ACTIVITY,
    UNIT4_QUESTION_BANK,
    UNIT4_REVISION_TIPS,
)
from arjun_course3_unit5_practice import (
    UNIT5_CATEGORIES,
    UNIT5_CATEGORY_ACTIVITY,
    UNIT5_QUESTION_BANK,
    UNIT5_REVISION_TIPS,
)

ROOT = Path(__file__).resolve().parent

STRENGTH_THRESHOLD_PCT = 80
DEFAULT_SESSION_COUNT = 15
FOCUS_SESSION_COUNT = 8
RECENT_SESSIONS_TO_AVOID = 2

QUESTION_BANK_BY_UNIT: dict[int, list[dict]] = {
    1: UNIT1_QUESTION_BANK,
    2: UNIT2_QUESTION_BANK,
    3: UNIT3_QUESTION_BANK,
    4: UNIT4_QUESTION_BANK,
    5: UNIT5_QUESTION_BANK,
}

CATEGORIES_BY_UNIT: dict[int, dict] = {
    1: UNIT1_CATEGORIES,
    2: UNIT2_CATEGORIES,
    3: UNIT3_CATEGORIES,
    4: UNIT4_CATEGORIES,
    5: UNIT5_CATEGORIES,
}

CATEGORY_ACTIVITY_BY_UNIT: dict[int, dict[str, str]] = {
    1: UNIT1_CATEGORY_ACTIVITY,
    2: UNIT2_CATEGORY_ACTIVITY,
    3: UNIT3_CATEGORY_ACTIVITY,
    4: UNIT4_CATEGORY_ACTIVITY,
    5: UNIT5_CATEGORY_ACTIVITY,
}

REVISION_TIPS_BY_UNIT: dict[int, dict[str, str]] = {
    1: UNIT1_REVISION_TIPS,
    2: UNIT2_REVISION_TIPS,
    3: UNIT3_REVISION_TIPS,
    4: UNIT4_REVISION_TIPS,
    5: UNIT5_REVISION_TIPS,
}


def get_categories(unit_id: int) -> dict:
    return CATEGORIES_BY_UNIT.get(unit_id, UNIT1_CATEGORIES)


def get_category_activity_slug(unit_id: int, category: str) -> str | None:
    return CATEGORY_ACTIVITY_BY_UNIT.get(unit_id, {}).get(category)


def _unit_practice(unit_id: int) -> dict:
    return {
        "bank": QUESTION_BANK_BY_UNIT.get(unit_id, UNIT1_QUESTION_BANK),
        "categories": get_categories(unit_id),
        "category_activity": CATEGORY_ACTIVITY_BY_UNIT.get(unit_id, {}),
        "revision_tips": REVISION_TIPS_BY_UNIT.get(unit_id, {}),
    }


def practice_image_path(image_key: str | None, unit_id: int = 1) -> str | None:
    """Reserved for future diagram-backed questions."""
    return None


def _weighted_pool(questions: list[dict], categories: dict) -> list[dict]:
    pool: list[dict] = []
    for q in questions:
        cat = categories.get(q["category"], {})
        w = cat.get("weight", 1)
        pool.extend([q] * w)
    random.shuffle(pool)
    return pool


def _question_available(
    q: dict,
    used_ids: set[str],
    avoid_ids: set[str],
    *,
    allow_recent: bool,
) -> bool:
    if q["id"] in used_ids:
        return False
    if not allow_recent and q["id"] in avoid_ids:
        return False
    return True


def _pick_unique(
    pool: list[dict],
    count: int,
    used_ids: set[str],
    avoid_ids: set[str],
) -> list[dict]:
    picked: list[dict] = []
    for allow_recent in (False, True):
        if len(picked) >= count:
            break
        for q in pool:
            if len(picked) >= count:
                break
            if not _question_available(q, used_ids, avoid_ids, allow_recent=allow_recent):
                continue
            picked.append(dict(q))
            used_ids.add(q["id"])
    return picked


def _top_up(
    selected: list[dict],
    count: int,
    used_ids: set[str],
    avoid_ids: set[str],
    candidates: list[dict],
) -> None:
    random.shuffle(candidates)
    for allow_recent in (False, True):
        if len(selected) >= count:
            break
        for q in candidates:
            if len(selected) >= count:
                break
            if not _question_available(q, used_ids, avoid_ids, allow_recent=allow_recent):
                continue
            selected.append(dict(q))
            used_ids.add(q["id"])


def _filter_bank(bank: list[dict], category_filter: list[str] | None) -> list[dict]:
    if not category_filter:
        return bank
    allowed = set(category_filter)
    return [q for q in bank if q.get("category") in allowed]


def _filter_categories(categories: dict, category_filter: list[str] | None) -> dict:
    if not category_filter:
        return categories
    allowed = set(category_filter)
    return {k: v for k, v in categories.items() if k in allowed}


def build_session_set(
    unit_id: int,
    config: dict,
    exclude_ids: set[str] | None = None,
    *,
    xai_api_key: str | None = None,
) -> tuple[list[dict], str | None]:
    """Build a practice session from weekly plan config."""
    category_filter = config.get("categories") or None
    count = int(config.get("question_count", DEFAULT_SESSION_COUNT))
    use_llm = bool(config.get("use_llm"))
    bank_size = question_count_for_unit(unit_id, category_filter)
    if bank_size == 0 and not use_llm:
        return [], "Configure topics in Week Setup — no questions match the selected categories."
    count = min(count, bank_size) if bank_size else count
    grok_error: str | None = None
    if use_llm and xai_api_key:
        questions = build_daily_set(
            count=count,
            unit_id=unit_id,
            exclude_ids=exclude_ids,
            use_llm=True,
            xai_api_key=xai_api_key,
            category_filter=category_filter,
        )
        if questions and questions[0].get("source") != "llm":
            grok_error = "Grok generation failed — used the built-in question bank instead."
    else:
        if use_llm and not xai_api_key:
            grok_error = "AI is enabled but XAI_API_KEY is missing — used the built-in question bank."
        questions = build_daily_set(
            count=count,
            unit_id=unit_id,
            exclude_ids=exclude_ids,
            use_llm=False,
            xai_api_key=xai_api_key,
            category_filter=category_filter,
        )
    if not questions:
        return [], grok_error or "Could not build a practice set — check Week Setup categories."
    return questions, grok_error


def build_daily_set(
    count: int = DEFAULT_SESSION_COUNT,
    unit_id: int = 1,
    exclude_ids: set[str] | None = None,
    *,
    use_llm: bool = False,
    xai_api_key: str | None = None,
    category_filter: list[str] | None = None,
) -> list[dict]:
    if use_llm and xai_api_key:
        cfg = _unit_practice(unit_id)
        categories = _filter_categories(cfg["categories"], category_filter)
        try:
            import arjun_course3_content as c3
            from arjun_course3_llm import generate_session_questions

            unit = c3.get_unit(unit_id)
            questions = generate_session_questions(
                xai_api_key,
                unit_id,
                count,
                categories=categories,
                revision_tips=cfg["revision_tips"],
                unit_title=unit["title"] if unit else f"Unit {unit_id}",
                unit_subtitle=unit.get("subtitle", "") if unit else "",
                fallback=lambda: _build_bank_daily_set(
                    count=count,
                    unit_id=unit_id,
                    exclude_ids=exclude_ids,
                    category_filter=category_filter,
                ),
            )
            if questions:
                return questions
        except Exception:
            pass

    return _build_bank_daily_set(
        count=count,
        unit_id=unit_id,
        exclude_ids=exclude_ids,
        category_filter=category_filter,
    )


def _build_bank_daily_set(
    count: int = DEFAULT_SESSION_COUNT,
    unit_id: int = 1,
    exclude_ids: set[str] | None = None,
    category_filter: list[str] | None = None,
) -> list[dict]:
    cfg = _unit_practice(unit_id)
    bank = _filter_bank(cfg["bank"], category_filter)
    categories = _filter_categories(cfg["categories"], category_filter)
    if not bank:
        return []
    avoid_ids = set(exclude_ids or ())

    used_ids: set[str] = set()
    selected = _pick_unique(_weighted_pool(bank, categories), count, used_ids, avoid_ids)

    if len(selected) < count:
        remainder = [q for q in bank if q["id"] not in used_ids]
        _top_up(selected, count, used_ids, avoid_ids, remainder)

    random.shuffle(selected)
    return selected[:count]


def build_focus_set(
    unit_id: int,
    category: str,
    count: int = FOCUS_SESSION_COUNT,
    exclude_ids: set[str] | None = None,
    *,
    use_llm: bool = False,
    xai_api_key: str | None = None,
) -> list[dict]:
    cfg = _unit_practice(unit_id)
    categories = cfg["categories"]
    if category not in categories:
        return _build_bank_daily_set(count=count, unit_id=unit_id, exclude_ids=exclude_ids)

    if use_llm and xai_api_key:
        try:
            import arjun_course3_content as c3
            from arjun_course3_llm import generate_session_questions

            unit = c3.get_unit(unit_id)
            questions = generate_session_questions(
                xai_api_key,
                unit_id,
                count,
                categories=categories,
                revision_tips=cfg["revision_tips"],
                unit_title=unit["title"] if unit else f"Unit {unit_id}",
                unit_subtitle=unit.get("subtitle", "") if unit else "",
                focus_category=category,
                fallback=lambda: _build_bank_focus_set(
                    unit_id=unit_id,
                    category=category,
                    count=count,
                    exclude_ids=exclude_ids,
                ),
            )
            if questions:
                return questions
        except Exception:
            pass

    return _build_bank_focus_set(
        unit_id=unit_id,
        category=category,
        count=count,
        exclude_ids=exclude_ids,
    )


def _build_bank_focus_set(
    unit_id: int,
    category: str,
    count: int = FOCUS_SESSION_COUNT,
    exclude_ids: set[str] | None = None,
) -> list[dict]:
    cfg = _unit_practice(unit_id)
    bank = [q for q in cfg["bank"] if q.get("category") == category]
    avoid_ids = set(exclude_ids or ())
    used_ids: set[str] = set()
    selected = _pick_unique(bank, count, used_ids, avoid_ids)
    if len(selected) < count:
        _top_up(selected, count, used_ids, avoid_ids, bank)
    random.shuffle(selected)
    return selected[:count]


def build_session_report(
    questions: list[dict],
    answers: list[dict],
    unit_id: int = 1,
) -> dict:
    cfg = _unit_practice(unit_id)
    categories = cfg["categories"]
    category_activity = cfg["category_activity"]
    revision_tips = cfg["revision_tips"]

    by_cat: dict[str, dict] = {}
    for q, ans in zip(questions, answers):
        cat = q.get("category", "unknown")
        bucket = by_cat.setdefault(cat, {"correct": 0, "total": 0})
        bucket["total"] += 1
        if ans.get("correct"):
            bucket["correct"] += 1

    strengths: list[dict] = []
    needs_revision: list[dict] = []
    for cat, stats in by_cat.items():
        info = categories.get(cat, {})
        pct = int(100 * stats["correct"] / stats["total"]) if stats["total"] else 0
        entry = {
            "category": cat,
            "name": info.get("name", cat.replace("_", " ").title()),
            "emoji": info.get("emoji", "📐"),
            "color": info.get("color", "#6366f1"),
            "correct": stats["correct"],
            "total": stats["total"],
            "pct": pct,
            "activity_slug": category_activity.get(cat),
            "tip": revision_tips.get(cat, "Review the matching lesson notes and try again."),
        }
        if pct >= STRENGTH_THRESHOLD_PCT:
            strengths.append(entry)
        else:
            needs_revision.append(entry)

    strengths.sort(key=lambda e: (-e["pct"], e["name"]))
    needs_revision.sort(key=lambda e: (e["pct"], e["name"]))

    correct_count = sum(1 for a in answers if a.get("correct"))
    total = len(answers)
    score_pct = int(100 * correct_count / total) if total else 0

    if needs_revision:
        tip = f"{needs_revision[0]['name']}: {needs_revision[0]['tip']}"
    elif score_pct == 100:
        tip = "Perfect run — try another set to keep skills sharp."
    else:
        tip = "Solid session. One more practice set will help lock in the harder topics."

    return {
        "correct_count": correct_count,
        "total": total,
        "score_pct": score_pct,
        "strengths": strengths,
        "needs_revision": needs_revision,
        "tip": tip,
    }


def format_report_details(report: dict) -> str:
    base = f"{report['correct_count']}/{report['total']} correct"
    weak = [r["name"] for r in report.get("needs_revision", [])]
    if weak:
        return f"{base} | Review: {', '.join(weak)}"
    return base


def question_count_for_unit(unit_id: int, category_filter: list[str] | None = None) -> int:
    bank = QUESTION_BANK_BY_UNIT.get(unit_id, [])
    return len(_filter_bank(bank, category_filter))
