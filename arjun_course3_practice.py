"""Arjun Course 3 Math — practice question banks and session builders (Units 1–5)."""

from __future__ import annotations

import random
from pathlib import Path

import arjun_course3_levels as c3lvl
import arjun_course3_answers as c3ans
from arjun_course3_concept_check import (
    daily_concept_check_quota,
    extend_bank,
    focus_concept_check_quota,
    is_concept_check,
    pick_or_generate_concept_check,
)

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
SCHOOL_PACKET_SOURCE = "school_packet_9_22"
SCHOOL_SEEDED_SOURCE = "school_seeded"
# Unit 1 daily practice: most items should look like the teacher worksheets.
SCHOOL_SESSION_RATIO = 0.7
SCHOOL_PACKET_SESSION_RATIO = 0.85
UNIT1_SEED_LIMIT = 8

_BASE_BANK_BY_UNIT: dict[int, list[dict]] = {
    1: UNIT1_QUESTION_BANK,
    2: UNIT2_QUESTION_BANK,
    3: UNIT3_QUESTION_BANK,
    4: UNIT4_QUESTION_BANK,
    5: UNIT5_QUESTION_BANK,
}

QUESTION_BANK_BY_UNIT: dict[int, list[dict]] = {
    uid: extend_bank(base, uid) for uid, base in _BASE_BANK_BY_UNIT.items()
}


def refresh_unit_bank(unit_id: int) -> int:
    """Reload merged bank (static + concept checks + AI JSON) after new questions are saved."""
    base = _BASE_BANK_BY_UNIT.get(unit_id)
    if not base:
        return 0
    QUESTION_BANK_BY_UNIT[unit_id] = extend_bank(base, unit_id)
    return len(QUESTION_BANK_BY_UNIT[unit_id])


def is_school_like(question: dict) -> bool:
    """True for teacher-packet clones or Grok items seeded from that packet."""
    source = question.get("source")
    return source in {SCHOOL_PACKET_SOURCE, SCHOOL_SEEDED_SOURCE} or question.get("style") == "school_packet"


def stem_family_for_question(question: str) -> str:
    """Group worksheet stems so Grok seeds cover rewrite, convert, nested-of, etc."""
    text = " ".join(str(question or "").lower().split())
    if "of those" in text or ("what fraction" in text and "of the" in text):
        return "nested_of"
    if "rewrite" in text or "exponential form" in text:
        return "rewrite"
    if "correct?" in text or ("correct" in text and text.startswith("was ")):
        return "was_correct"
    if "estimate" in text or "nearest tenth" in text:
        return "estimate"
    if "increasing" in text or "decreasing" in text:
        return "order"
    if "convert" in text or "repeating decimal" in text or "as a percent" in text:
        return "convert"
    if "simplest form" in text or text.startswith("complete"):
        return "simplest"
    if "name the rational" in text or "rational numbers in" in text:
        return "rational_set"
    if "figure 1" in text or "pattern" in text:
        return "pattern"
    if "product of powers" in text or "quotient of" in text:
        return "product_quotient"
    if "scientific notation" in text:
        return "sci_notation"
    if "compare using" in text or "which is greater" in text:
        return "compare"
    if text.startswith("evaluate") or "evaluate the expression" in text:
        return "evaluate"
    if "solve for" in text:
        return "solve"
    story_marks = ("recipe", "reading log", "yards of", "cups of", "lbs of", "tray of")
    if any(mark in text for mark in story_marks):
        return "word_story"
    return "other"


def seed_questions_for_category(
    unit_id: int,
    category: str,
    *,
    level: str | None = None,
    limit: int = 3,
) -> list[dict]:
    """Sample static base-bank questions to seed Grok (style guides, not copies)."""
    bank = _BASE_BANK_BY_UNIT.get(unit_id) or QUESTION_BANK_BY_UNIT.get(unit_id, [])
    pool = [q for q in bank if q.get("category") == category]
    if level:
        by_level = [q for q in pool if q.get("level") == level]
        if len(by_level) >= min(limit, 2):
            pool = by_level
    if not pool:
        return []
    families: dict[str, list[dict]] = {}
    for q in pool:
        families.setdefault(stem_family_for_question(q.get("question", "")), []).append(q)
    for family_id, items in families.items():
        school = [q for q in items if q.get("source") == SCHOOL_PACKET_SOURCE]
        other = [q for q in items if q.get("source") != SCHOOL_PACKET_SOURCE]
        random.shuffle(school)
        random.shuffle(other)
        families[family_id] = school + other
    family_order = list(families)
    random.shuffle(family_order)
    picked: list[dict] = []
    while len(picked) < limit and any(families.values()):
        progressed = False
        for family_id in family_order:
            bucket = families.get(family_id) or []
            if not bucket:
                continue
            picked.append(bucket.pop(0))
            progressed = True
            if len(picked) >= limit:
                break
        if not progressed:
            break
    return picked

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
            selected.append(c3ans.finalize_question(dict(q)))
            used_ids.add(q["id"])


def _normalized_config(unit_id: int, config: dict) -> dict:
    valid = set(get_categories(unit_id).keys())
    return c3lvl.normalize_week_config({**config, "unit_id": unit_id}, valid, unit_id=unit_id)


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


def _bank_for_config(bank: list[dict], config: dict, unit_id: int) -> list[dict]:
    norm = _normalized_config(unit_id, config)
    valid = set(get_categories(unit_id).keys())
    level_map = c3lvl.bank_level_map(bank)
    allowed_slots = set(c3lvl.active_slots(norm.get("topics") or [], valid))
    if not allowed_slots:
        return []
    return [
        q
        for q in bank
        if (str(q.get("category", "")), level_map.get(str(q.get("id", "")), "B")) in allowed_slots
    ]


def _pick_for_slots(
    bank: list[dict],
    config: dict,
    unit_id: int,
    count: int,
    used_ids: set[str],
    avoid_ids: set[str],
    *,
    xai_api_key: str | None = None,
) -> list[dict]:
    norm = _normalized_config(unit_id, config)
    valid = set(get_categories(unit_id).keys())
    plan = c3lvl.slot_plan(norm.get("topics") or [], valid, count)
    if not plan:
        return []
    level_map = c3lvl.bank_level_map(bank)
    by_slot: dict[tuple[str, str], list[dict]] = {}
    for q in bank:
        cat = str(q.get("category", ""))
        lvl = level_map.get(str(q.get("id", "")), "B")
        by_slot.setdefault((cat, lvl), []).append(q)
    for pool in by_slot.values():
        random.shuffle(pool)

    selected: list[dict] = []
    cc_quota = daily_concept_check_quota(count)
    cc_picked = 0

    def _topic_levels(cat: str) -> set[str]:
        return set(
            next(
                (item.get("levels") or [] for item in norm["topics"] if item.get("id") == cat),
                [],
            )
        )

    prefer_school_mix = unit_id == 1
    school_ratio = SCHOOL_SESSION_RATIO
    if prefer_school_mix and "school packet" in str(norm.get("week_label") or "").lower():
        school_ratio = SCHOOL_PACKET_SESSION_RATIO
    school_target = round(count * school_ratio) if prefer_school_mix else 0
    packet_target = round(school_target * 0.5) if school_target else 0
    school_picked = 0
    packet_picked = 0

    def _take_from_pool(pool: list[dict], *, prefer_concept_check: bool = False) -> dict | None:
        nonlocal school_picked, packet_picked
        packet_pool = [q for q in pool if q.get("source") == SCHOOL_PACKET_SOURCE]
        seeded_pool = [
            q for q in pool if is_school_like(q) and q.get("source") != SCHOOL_PACKET_SOURCE
        ]
        other_pool = [q for q in pool if not is_school_like(q)]
        school_like_pool = packet_pool + seeded_pool
        tiers: list[list[dict]] = []
        if prefer_school_mix and school_like_pool:
            if school_picked < school_target:
                if packet_picked < packet_target and packet_pool:
                    tiers = [packet_pool, seeded_pool, other_pool]
                else:
                    tiers = [seeded_pool, packet_pool, other_pool]
            else:
                tiers = [other_pool, seeded_pool, packet_pool]
        elif prefer_concept_check:
            cc_pool = [q for q in pool if is_concept_check(q)]
            leftover = [q for q in pool if not is_concept_check(q)]
            if cc_pool:
                tiers.append(cc_pool)
            tiers.append(leftover)
        else:
            tiers.append(pool)
        for tier in tiers:
            for allow_recent in (False, True):
                for q in tier:
                    if not _question_available(q, used_ids, avoid_ids, allow_recent=allow_recent):
                        continue
                    used_ids.add(q["id"])
                    if is_school_like(q):
                        school_picked += 1
                    if q.get("source") == SCHOOL_PACKET_SOURCE:
                        packet_picked += 1
                    return c3ans.finalize_question(dict(q))
        return None

    for cat, lvl in plan:
        if len(selected) >= count:
            break
        want_cc = (
            (not prefer_school_mix or school_picked >= school_target)
            and cc_picked < cc_quota
        )
        if want_cc:
            q = pick_or_generate_concept_check(
                unit_id,
                cat,
                lvl,
                bank,
                used_ids,
                avoid_ids,
                _topic_levels(cat),
                xai_api_key=xai_api_key,
            )
            if q:
                selected.append(q)
                cc_picked += 1
                continue
        q = _take_from_pool(by_slot.get((cat, lvl), []), prefer_concept_check=want_cc)
        if q:
            selected.append(q)
            if is_concept_check(q):
                cc_picked += 1
            continue
        # fallback: same category, any allowed level for that category
        topic_levels = _topic_levels(cat)
        for fallback_lvl in c3lvl.LEVEL_ORDER:
            if fallback_lvl not in topic_levels:
                continue
            if want_cc and cc_picked < cc_quota:
                q = pick_or_generate_concept_check(
                    unit_id,
                    cat,
                    fallback_lvl,
                    bank,
                    used_ids,
                    avoid_ids,
                    topic_levels,
                    xai_api_key=xai_api_key,
                )
                if q:
                    selected.append(q)
                    cc_picked += 1
                    break
            q = _take_from_pool(
                by_slot.get((cat, fallback_lvl), []),
                prefer_concept_check=want_cc,
            )
            if q:
                selected.append(q)
                if is_concept_check(q):
                    cc_picked += 1
                break

    if len(selected) < count:
        remainder = [q for q in _bank_for_config(bank, config, unit_id) if q["id"] not in used_ids]
        random.shuffle(remainder)
        cc_remainder = [q for q in remainder if is_concept_check(q)]
        other_remainder = [q for q in remainder if not is_concept_check(q)]
        while len(selected) < count and cc_picked < cc_quota and cc_remainder:
            q = cc_remainder.pop()
            if _question_available(q, used_ids, avoid_ids, allow_recent=True):
                selected.append(c3ans.finalize_question(dict(q)))
                used_ids.add(q["id"])
                cc_picked += 1
        _top_up(selected, count, used_ids, avoid_ids, cc_remainder + other_remainder)

    if len(selected) < count:
        filler = list(plan) or list(c3lvl.active_slots(norm.get("topics") or [], valid))
        guard = 0
        while filler and len(selected) < count and guard < count * 6:
            guard += 1
            cat, lvl = filler[guard % len(filler)]
            q = pick_or_generate_concept_check(
                unit_id,
                cat,
                lvl,
                bank,
                used_ids,
                avoid_ids,
                _topic_levels(cat),
                xai_api_key=xai_api_key,
            )
            if q:
                selected.append(q)

    random.shuffle(selected)
    return c3ans.finalize_questions(selected[:count])


def build_session_set(
    unit_id: int,
    config: dict,
    exclude_ids: set[str] | None = None,
    *,
    xai_api_key: str | None = None,
) -> tuple[list[dict], str | None]:
    """Build a practice session from weekly plan config."""
    norm = _normalized_config(unit_id, config)
    valid = set(get_categories(unit_id).keys())
    if not c3lvl.active_slots(norm.get("topics") or [], valid):
        return [], "Select topics and difficulty levels in Week Setup."
    count = DEFAULT_SESSION_COUNT
    use_llm = bool(norm.get("use_llm"))
    # Do not cap to the static bank — concept-check generators (and Grok) can
    # fill a 15-question session when Week Setup only matches a handful of items.
    grok_error: str | None = None
    if use_llm and xai_api_key:
        questions = build_daily_set(
            count=count,
            unit_id=unit_id,
            exclude_ids=exclude_ids,
            use_llm=True,
            xai_api_key=xai_api_key,
            week_config=norm,
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
            week_config=norm,
        )
    if not questions:
        return [], grok_error or "Could not build a practice set — check Week Setup."
    return questions, grok_error


def build_daily_set(
    count: int = DEFAULT_SESSION_COUNT,
    unit_id: int = 1,
    exclude_ids: set[str] | None = None,
    *,
    use_llm: bool = False,
    xai_api_key: str | None = None,
    category_filter: list[str] | None = None,
    week_config: dict | None = None,
) -> list[dict]:
    cfg = _unit_practice(unit_id)
    config = week_config or (
        {"categories": category_filter} if category_filter else {}
    )
    norm = _normalized_config(unit_id, config)
    categories = _filter_categories(cfg["categories"], norm.get("categories"))
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
                week_config=norm,
                fallback=lambda: _build_bank_daily_set(
                    count=count,
                    unit_id=unit_id,
                    exclude_ids=exclude_ids,
                    week_config=norm,
                    xai_api_key=xai_api_key,
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
        week_config=norm,
        xai_api_key=xai_api_key,
    )


def _build_bank_daily_set(
    count: int = DEFAULT_SESSION_COUNT,
    unit_id: int = 1,
    exclude_ids: set[str] | None = None,
    category_filter: list[str] | None = None,
    week_config: dict | None = None,
    *,
    xai_api_key: str | None = None,
) -> list[dict]:
    cfg = _unit_practice(unit_id)
    config = week_config or (
        {"categories": category_filter} if category_filter else {}
    )
    norm = _normalized_config(unit_id, config)
    bank = _bank_for_config(cfg["bank"], norm, unit_id)
    if not bank:
        return []
    avoid_ids = set(exclude_ids or ())
    used_ids: set[str] = set()
    return _pick_for_slots(
        cfg["bank"], norm, unit_id, count, used_ids, avoid_ids, xai_api_key=xai_api_key
    )


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
                    xai_api_key=xai_api_key,
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
        xai_api_key=xai_api_key,
    )


def _build_bank_focus_set(
    unit_id: int,
    category: str,
    count: int = FOCUS_SESSION_COUNT,
    exclude_ids: set[str] | None = None,
    *,
    xai_api_key: str | None = None,
) -> list[dict]:
    cfg = _unit_practice(unit_id)
    bank = [q for q in cfg["bank"] if q.get("category") == category]
    avoid_ids = set(exclude_ids or ())
    used_ids: set[str] = set()
    selected: list[dict] = []
    cc_quota = focus_concept_check_quota(count)
    cc_pool = [q for q in bank if is_concept_check(q)]
    other_pool = [q for q in bank if not is_concept_check(q)]

    for _ in range(cc_quota):
        picked = _pick_unique(cc_pool, 1, used_ids, avoid_ids)
        if picked:
            selected.extend(picked)
        else:
            generated = pick_or_generate_concept_check(
                unit_id,
                category,
                "C",
                bank,
                used_ids,
                avoid_ids,
                set(c3lvl.LEVEL_ORDER),
                xai_api_key=xai_api_key,
            )
            if generated:
                selected.append(generated)

    if len(selected) < count:
        _top_up(selected, count, used_ids, avoid_ids, other_pool + cc_pool)
    random.shuffle(selected)
    return c3ans.finalize_questions(selected[:count])


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


def question_count_for_unit(
    unit_id: int,
    category_filter: list[str] | None = None,
    *,
    config: dict | None = None,
) -> int:
    bank = QUESTION_BANK_BY_UNIT.get(unit_id, [])
    if config:
        return len(_bank_for_config(bank, config, unit_id))
    return len(_filter_bank(bank, category_filter))
