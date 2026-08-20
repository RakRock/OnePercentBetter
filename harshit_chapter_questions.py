"""Chapter-derived question banks for Harshit PreReq practice."""

from __future__ import annotations

import json
import random
import re
import uuid
from pathlib import Path

import harshit_math_render as hmr
import harshit_prereq_topics as hpt
from llm_question_format import is_quality_practice_question

ROOT = Path(__file__).resolve().parent
BANK_DIR = ROOT / "HarshitMath" / "question_banks"

# Which NCERT chapter each practice topic draws from
TOPIC_CHAPTER: dict[tuple[int, int], int] = {
    (1, 1): 1,
    (1, 2): 1,
    (1, 3): 1,
    (1, 4): 1,
    (1, 5): 1,
    (2, 1): 2,
    (2, 2): 2,
    (2, 3): 2,
    (2, 4): 4,
    (2, 5): 4,
    (2, 6): 4,
    (2, 7): 4,
    (3, 1): 3,
    (3, 2): 3,
    (4, 1): 5,
    (4, 2): 7,
    (4, 3): 8,
    (4, 4): 10,
    (5, 1): 12,
    (5, 2): 13,
    (5, 3): 13,
    (6, 1): 14,
    (6, 2): 14,
    (6, 3): 15,
}


def chapter_for_topic(prereq_id: int, topic_id: int) -> int | None:
    return TOPIC_CHAPTER.get((prereq_id, topic_id))


def bank_path(prereq_id: int, topic_id: int) -> Path:
    return BANK_DIR / f"prereq_{prereq_id:02d}" / f"topic_{topic_id:02d}.json"


def load_bank(prereq_id: int, topic_id: int) -> dict:
    path = bank_path(prereq_id, topic_id)
    if not path.is_file():
        return {"questions": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"questions": {}}
    if not isinstance(data, dict):
        return {"questions": {}}
    data.setdefault("questions", {})
    return data


def save_bank(prereq_id: int, topic_id: int, bank: dict) -> Path:
    path = bank_path(prereq_id, topic_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def bank_stats(prereq_id: int) -> dict:
    topics = hpt.topics_for_prereq(prereq_id)
    total = 0
    by_topic: dict[int, int] = {}
    for tid in topics:
        bank = load_bank(prereq_id, tid)
        count = sum(len(v) for v in bank.get("questions", {}).values() if isinstance(v, list))
        by_topic[tid] = count
        total += count
    return {"total": total, "by_topic": by_topic}


def bank_status_message(prereq_id: int) -> str:
    stats = bank_stats(prereq_id)
    if stats["total"]:
        return f"Chapter question bank: {stats['total']} practice question(s) cached."
    return (
        "Chapter question bank: **empty** — practice is using built-in templates (limited variety). "
        "Add PDFs to `HarshitMath/class9_chapters/` and run "
        "`python3 scripts/build_harshit_chapter_questions.py --prereq "
        f"{prereq_id}`."
    )


def add_questions(
    prereq_id: int,
    topic_id: int,
    level: str,
    questions: list[dict],
    *,
    chapter_num: int | None = None,
    source_pdf: str = "",
) -> int:
    bank = load_bank(prereq_id, topic_id)
    bank.setdefault("meta", {})
    bank["meta"].update(
        {
            "prereq_id": prereq_id,
            "topic_id": topic_id,
            "chapter_num": chapter_num or chapter_for_topic(prereq_id, topic_id),
            "source_pdf": source_pdf or bank["meta"].get("source_pdf", ""),
        }
    )
    bucket = bank.setdefault("questions", {}).setdefault(level, [])
    existing_ids = {q.get("id") for q in bucket if isinstance(q, dict)}
    existing_keys = {
        question_dedup_key(str(q.get("question", "")))
        for q in bucket
        if isinstance(q, dict)
    }
    added = 0
    for raw in questions:
        q = normalize_question(raw, prereq_id, topic_id, level)
        key = question_dedup_key(str(q.get("question", "")))
        if q["id"] in existing_ids or key in existing_keys:
            continue
        bucket.append(q)
        existing_ids.add(q["id"])
        existing_keys.add(key)
        added += 1
    save_bank(prereq_id, topic_id, bank)
    return added


def question_dedup_key(text: str) -> str:
    """Normalize question text for repeat detection across levels and sessions."""
    t = str(text or "").strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t.rstrip(".?!").strip()


def is_question_excluded(
    q: dict,
    *,
    exclude_ids: set[str] | None = None,
    exclude_text: set[str] | None = None,
) -> bool:
    """True if question id or normalized text was already used."""
    exclude_ids = exclude_ids or set()
    exclude_text = exclude_text or set()
    qid = str(q.get("id") or "")
    if qid and qid in exclude_ids:
        return True
    raw = str(q.get("question", "")).strip()
    if raw in exclude_text:
        return True
    key = question_dedup_key(raw)
    return key in exclude_text or any(question_dedup_key(t) == key for t in exclude_text)


def normalize_question(raw: dict, prereq_id: int, topic_id: int, level: str) -> dict:
    options = [hmr.sanitize_grok_math_text(str(o)) for o in raw.get("options", [])]
    answer = int(raw.get("answer", 0))
    if len(options) != 4 or answer not in range(4):
        raise ValueError("Question must have 4 options and answer index 0-3")
    if len({o.strip().lower() for o in options}) < 4:
        raise ValueError("Question must have 4 distinct options")

    qid = str(raw.get("id") or f"p{prereq_id}_t{topic_id}_{level}_{uuid.uuid4().hex[:8]}")
    ch = chapter_for_topic(prereq_id, topic_id)
    return {
        "id": qid,
        "question": hmr.sanitize_grok_math_text(str(raw.get("question", ""))).strip(),
        "options": options,
        "answer": answer,
        "explanation": hmr.sanitize_grok_math_text(str(raw.get("explanation", ""))).strip(),
        "topic": topic_id,
        "level": level,
        "prereq_id": prereq_id,
        "category": f"p{prereq_id}_t{topic_id}_{level}",
        "category_label": hpt.format_topic_level_label(prereq_id, topic_id, level),
        "source": raw.get("source", "chapter_pdf"),
        "chapter_num": raw.get("chapter_num", ch),
        "chapter_ref": raw.get("chapter_ref", ""),
    }


def pick_question(
    prereq_id: int,
    topic_id: int,
    level: str,
    *,
    exclude_ids: set[str] | None = None,
    exclude_text: set[str] | None = None,
    quality_only: bool = True,
) -> dict | None:
    bank = load_bank(prereq_id, topic_id)
    pool = list(bank.get("questions", {}).get(level, []))
    if not pool:
        pool = [
            q
            for lvl, qs in bank.get("questions", {}).items()
            if isinstance(qs, list)
            for q in qs
        ]
    if not pool:
        return None
    exclude_ids = exclude_ids or set()
    exclude_text = exclude_text or set()

    def _excluded(q: dict) -> bool:
        return is_question_excluded(q, exclude_ids=exclude_ids, exclude_text=exclude_text)

    def _quality_ok(q: dict) -> bool:
        if not quality_only:
            return True
        opts = q.get("options") or []
        return is_quality_practice_question(str(q.get("question", "")), [str(o) for o in opts])

    candidates = [q for q in pool if not _excluded(q) and _quality_ok(q)]
    if not candidates and quality_only:
        candidates = [q for q in pool if not _excluded(q)]
    if not candidates:
        return None
    raw = random.choice(candidates)
    try:
        normalized = normalize_question(raw, prereq_id, topic_id, level)
        if quality_only and not is_quality_practice_question(
            normalized["question"], normalized["options"]
        ):
            return None
        return normalized
    except (ValueError, TypeError, KeyError):
        return None


def purge_low_quality_banks() -> int:
    """Remove placeholder/meta questions from all cached banks. Returns count removed."""
    removed = 0
    if not BANK_DIR.is_dir():
        return 0
    for path in BANK_DIR.rglob("topic_*.json"):
        m_pre = re.search(r"prereq_(\d+)", path.as_posix())
        m_top = re.search(r"topic_(\d+)", path.name)
        if not m_pre or not m_top:
            continue
        prereq_id = int(m_pre.group(1))
        topic_id = int(m_top.group(1))
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        questions = data.get("questions", {})
        if not isinstance(questions, dict):
            continue
        changed = False
        for level, bucket in list(questions.items()):
            if not isinstance(bucket, list):
                continue
            kept = []
            for q in bucket:
                if not isinstance(q, dict):
                    continue
                opts = q.get("options") or []
                if is_quality_practice_question(str(q.get("question", "")), [str(o) for o in opts]):
                    kept.append(q)
                else:
                    removed += 1
                    changed = True
            questions[level] = kept
        if changed:
            save_bank(prereq_id, topic_id, data)
    return removed
