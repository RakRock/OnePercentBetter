"""Quiz, typing, and match-game helpers for Arjun Spanish."""

from __future__ import annotations

import random
import re
import unicodedata
from typing import Any

from arjun_spanish import content as es

_PUNCT_RE = re.compile(r"[¿?¡!.,;:…\"“”']+")
_ARTICLE_RE = re.compile(r"^(el|la|los|las|un|una)\s+")
MAX_TYPED_LEN = 80


def normalize_answer(text: str) -> str:
    """Lowercase, strip punctuation/extra space — keep letters including ñ."""
    cleaned = _PUNCT_RE.sub(" ", (text or "").strip().lower())
    cleaned = cleaned.replace("ud.", "usted").replace("sr.", "señor")
    cleaned = cleaned.replace("sra.", "señora").replace("srta.", "señorita")
    return " ".join(cleaned.split())


def strip_accents(text: str) -> str:
    """Remove accent marks but keep ñ (a different letter in Spanish)."""
    held = (text or "").replace("ñ", "\x00").replace("Ñ", "\x00")
    nfkd = unicodedata.normalize("NFD", held)
    stripped = "".join(ch for ch in nfkd if unicodedata.category(ch) != "Mn")
    return stripped.replace("\x00", "ñ")


def _without_article(text: str) -> str:
    return _ARTICLE_RE.sub("", text)


def typed_matches(user_text: str, card: dict[str, str]) -> bool:
    """Accept exact Spanish, missing accents, or missing el/la."""
    if len(user_text or "") > MAX_TYPED_LEN:
        return False
    got = normalize_answer(user_text)
    if not got:
        return False
    target = normalize_answer(card["spanish"])
    variants = {
        target,
        strip_accents(target),
        _without_article(target),
        strip_accents(_without_article(target)),
    }
    got_forms = {got, strip_accents(got), _without_article(got), strip_accents(_without_article(got))}
    return bool(got_forms & variants)


def pick_cards(topic_id: str, count: int, rng: random.Random | None = None) -> list[dict[str, str]]:
    rng = rng or random.Random()
    pool = list(es.cards_for_topic(topic_id))
    if not pool:
        return []
    if len(pool) <= count:
        rng.shuffle(pool)
        return pool
    return rng.sample(pool, count)


def make_mc_questions(
    cards: list[dict[str, str]],
    *,
    direction: str = "es_en",
    rng: random.Random | None = None,
) -> list[dict[str, Any]]:
    """Build 4-choice questions. direction is es_en or en_es."""
    rng = rng or random.Random()
    bank = list(es.CARDS)
    questions: list[dict[str, Any]] = []
    for card in cards:
        prompt = card["spanish"] if direction == "es_en" else card["english"]
        answer = card["english"] if direction == "es_en" else card["spanish"]
        distractor_key = "english" if direction == "es_en" else "spanish"
        others = [
            c[distractor_key]
            for c in bank
            if c["id"] != card["id"] and c[distractor_key] != answer
        ]
        rng.shuffle(others)
        options = [answer, *others[:3]]
        if len(options) < 4:
            continue
        rng.shuffle(options)
        questions.append(
            {
                "card_id": card["id"],
                "prompt": prompt,
                "answer": answer,
                "options": options,
                "direction": direction,
                "emoji": card.get("emoji", ""),
                "hint": card.get("hint", ""),
            }
        )
    return questions


def make_type_questions(
    cards: list[dict[str, str]],
    rng: random.Random | None = None,
) -> list[dict[str, Any]]:
    rng = rng or random.Random()
    items = list(cards)
    rng.shuffle(items)
    return [
        {
            "card_id": card["id"],
            "prompt": card["english"],
            "spanish": card["spanish"],
            "emoji": card.get("emoji", ""),
            "hint": card.get("hint", ""),
        }
        for card in items
    ]


def make_match_round(
    cards: list[dict[str, str]],
    pair_count: int = es.MATCH_PAIRS,
    rng: random.Random | None = None,
) -> dict[str, Any]:
    rng = rng or random.Random()
    chosen = list(cards)
    rng.shuffle(chosen)
    chosen = chosen[:pair_count]
    left = [{"id": c["id"], "text": c["spanish"], "emoji": c.get("emoji", "")} for c in chosen]
    right = [{"id": c["id"], "text": c["english"]} for c in chosen]
    rng.shuffle(left)
    rng.shuffle(right)
    return {"left": left, "right": right, "pairs": len(chosen)}
