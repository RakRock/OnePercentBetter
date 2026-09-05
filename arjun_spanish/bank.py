"""Built-in Spanish vocabulary MCQs from the school packet bank."""

from __future__ import annotations

import random
import uuid
from typing import Any

from arjun_spanish import content as es
from arjun_spanish import practice as esp


def _stem(card: dict[str, str], direction: str) -> str:
    if direction == "es_en":
        return f"What is the English meaning of: **{card['spanish']}**"
    return f"What is the Spanish for: **{card['english']}**"


def card_to_question(
    card: dict[str, str],
    *,
    direction: str,
    rng: random.Random | None = None,
) -> dict[str, Any] | None:
    """Turn one vocabulary card into a standard 4-option MCQ."""
    rng = rng or random.Random()
    built = esp.make_mc_questions([card], direction=direction, rng=rng)
    if not built:
        return None
    raw = built[0]
    options = list(raw["options"])
    answer_idx = options.index(raw["answer"])
    topic = es.topic_by_id(card["topic"])
    return {
        "id": f"es_bank_{card['id']}_{direction}",
        "category": card["topic"],
        "category_label": f"{topic.get('emoji', '')} {topic['title']}".strip(),
        "question": _stem(card, direction),
        "options": options,
        "answer": answer_idx,
        "explanation": raw.get("hint") or f"'{card['spanish']}' = {card['english']}",
        "direction": direction,
        "card_id": card["id"],
        "source": "bank",
        "level": "B",
    }


def pick_bank_question(
    topic_id: str,
    direction: str,
    *,
    used_ids: set[str],
    seen_fps: set[str],
    rng: random.Random | None = None,
) -> dict[str, Any] | None:
    from practice_quality.dedup import fingerprints_for_question, is_duplicate_of_any

    rng = rng or random.Random()
    pool = list(es.cards_for_topic(topic_id))
    rng.shuffle(pool)
    for card in pool:
        q = card_to_question(card, direction=direction, rng=rng)
        if not q or q["id"] in used_ids:
            continue
        fps = fingerprints_for_question(q)
        if is_duplicate_of_any(q, seen_fps):
            continue
        return q
    return None


def normalize_llm_question(item: dict, *, topic_id: str, direction: str) -> dict[str, Any]:
    topic = es.topic_by_id(topic_id)
    options = [str(o).strip() for o in item.get("options", [])]
    answer = int(item.get("answer", 0))
    return {
        "id": item.get("id") or f"es_ai_{topic_id}_{uuid.uuid4().hex[:10]}",
        "category": topic_id,
        "category_label": f"{topic.get('emoji', '')} {topic['title']}".strip(),
        "question": str(item.get("question", "")).strip(),
        "options": options,
        "answer": answer,
        "explanation": str(item.get("explanation", "")).strip(),
        "direction": direction,
        "source": item.get("source", "llm"),
        "level": str(item.get("level", "B")),
    }


def bank_stats() -> dict[str, int]:
    return {"total": es.total_cards(), "topics": len(es.TOPICS)}


def bank_status_message() -> str:
    stats = bank_stats()
    return f"{stats['total']} vocabulary cards across {stats['topics']} topics"
