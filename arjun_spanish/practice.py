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


def pick_cards(
    topic_id: str,
    count: int,
    rng: random.Random | None = None,
    prefer_ids: list[str] | set[str] | None = None,
) -> list[dict[str, str]]:
    rng = rng or random.Random()
    pool = list(es.cards_for_topic(topic_id))
    if not pool:
        return []
    prefer = set(prefer_ids or [])
    preferred = [c for c in pool if c["id"] in prefer]
    others = [c for c in pool if c["id"] not in prefer]
    rng.shuffle(preferred)
    rng.shuffle(others)
    ordered = preferred + others
    if len(ordered) <= count:
        rng.shuffle(ordered)
        return ordered
    chosen = ordered[:count]
    rng.shuffle(chosen)
    return chosen


def typed_sentence_matches(user_text: str, prompt: dict[str, Any]) -> bool:
    """Accept the target sentence or listed variants; forgive accents, keep articles."""
    if len(user_text or "") > MAX_TYPED_LEN:
        return False
    got = normalize_answer(user_text)
    if not got:
        return False
    targets = [prompt.get("spanish", ""), *(prompt.get("variants") or [])]
    accepted: set[str] = set()
    for raw in targets:
        target = normalize_answer(str(raw))
        if not target:
            continue
        accepted.add(target)
        accepted.add(strip_accents(target))
    got_forms = {got, strip_accents(got)}
    return bool(got_forms & accepted)


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


def _activity_distractors(act: dict[str, str], rng: random.Random) -> list[str]:
    others = [a["infinitive"] for a in es.GUSTAR_ACTIVITIES if a["id"] != act["id"]]
    rng.shuffle(others)
    return others[:3]


def make_likes_questions(
    count: int = es.LIKES_SIZE,
    rng: random.Random | None = None,
) -> list[dict[str, Any]]:
    rng = rng or random.Random()
    acts = list(es.GUSTAR_ACTIVITIES)
    rng.shuffle(acts)
    questions: list[dict[str, Any]] = []
    kinds = ("type_like", "type_dislike", "prefer", "choice")
    for i, act in enumerate(acts[:count]):
        kind = kinds[i % len(kinds)]
        card_id = f"gustar:{act['infinitive']}"
        if kind == "type_like":
            questions.append(
                {
                    "kind": "type",
                    "prompt": f"Type Spanish for: I like {act['english']}.",
                    "spanish": f"Me gusta {act['infinitive']}.",
                    "emoji": act["emoji"],
                    "hint": "Me gusta + infinitive.",
                    "card_id": card_id,
                }
            )
        elif kind == "type_dislike":
            questions.append(
                {
                    "kind": "type",
                    "prompt": f"Type Spanish for: I don't like {act['english']}.",
                    "spanish": f"No me gusta {act['infinitive']}.",
                    "emoji": act["emoji"],
                    "hint": "No me gusta + infinitive.",
                    "card_id": card_id,
                }
            )
        elif kind == "prefer":
            questions.append(
                {
                    "kind": "prefer",
                    "prompt": f"Do you like {act['english']}?",
                    "infinitive": act["infinitive"],
                    "english": act["english"],
                    "emoji": act["emoji"],
                    "hint": "Pick Me gusta or No me gusta, then type the sentence.",
                    "card_id": card_id,
                }
            )
        else:
            options = [act["infinitive"], *_activity_distractors(act, rng)]
            rng.shuffle(options)
            questions.append(
                {
                    "kind": "choice",
                    "prompt": f"Complete: Me gusta ______. ({act['english']})",
                    "options": options,
                    "answer": act["infinitive"],
                    "emoji": act["emoji"],
                    "hint": "The infinitive does not change after Me gusta.",
                    "card_id": card_id,
                }
            )
    if questions:
        ask = {
            "kind": "type",
            "prompt": "Ask a friend: What do you like to do?",
            "spanish": "¿Qué te gusta hacer?",
            "emoji": "❓",
            "hint": "¿Qué te gusta hacer?",
            "card_id": "gustar:¿Qué te gusta hacer?",
        }
        if len(questions) >= 2:
            questions[-1] = ask
        else:
            questions.append(ask)
    rng.shuffle(questions)
    return questions[:count]


def make_describe_questions(
    count: int = es.DESCRIBE_SIZE,
    rng: random.Random | None = None,
) -> list[dict[str, Any]]:
    rng = rng or random.Random()
    adjs = list(es.PERSONALITY_ADJECTIVES)
    rng.shuffle(adjs)
    questions: list[dict[str, Any]] = []
    kinds = ("gender_f", "gender_m", "ser", "sentence")
    ser_items = (
        ("Yo", "soy", "I am"),
        ("Tú", "eres", "You are (informal)"),
        ("Ella", "es", "She is"),
        ("Él", "es", "He is"),
    )
    for i in range(count):
        adj = adjs[i % len(adjs)]
        kind = kinds[i % len(kinds)]
        card_id = f"personality:{adj['m']}"
        if kind == "gender_f":
            questions.append(
                {
                    "kind": "type",
                    "prompt": f"Make this describe a girl: {adj['m']}",
                    "spanish": adj["f"],
                    "emoji": "👧",
                    "hint": f"{adj['m']} → {adj['f']} ({adj['english']})",
                    "card_id": card_id,
                }
            )
        elif kind == "gender_m":
            questions.append(
                {
                    "kind": "type",
                    "prompt": f"Make this describe a boy: {adj['f']}",
                    "spanish": adj["m"],
                    "emoji": "👦",
                    "hint": f"{adj['f']} → {adj['m']} ({adj['english']})",
                    "card_id": card_id,
                }
            )
        elif kind == "ser":
            pronoun, form, english = ser_items[i % len(ser_items)]
            options = ["soy", "eres", "es", "somos"]
            rng.shuffle(options)
            questions.append(
                {
                    "kind": "choice",
                    "prompt": f"{english}: {pronoun} ______ {adj['m'] if pronoun != 'Ella' else adj['f']}.",
                    "options": options,
                    "answer": form,
                    "emoji": "🪞",
                    "hint": "yo soy · tú eres · él/ella es",
                    "card_id": f"personality:{form}",
                }
            )
        else:
            girl = i % 2 == 0
            form = adj["f"] if girl else adj["m"]
            who = "She" if girl else "He"
            pronoun = "Ella" if girl else "Él"
            spanish = f"{pronoun} es {form}."
            questions.append(
                {
                    "kind": "type",
                    "prompt": f"{who} is {adj['english']}.",
                    "spanish": spanish,
                    "variants": [f"Es {form}."],
                    "emoji": "🪞",
                    "hint": f"{pronoun} es {form}.",
                    "card_id": card_id,
                }
            )
    rng.shuffle(questions)
    return questions[:count]


def make_sentence_questions(
    topic_id: str,
    count: int = es.SENTENCE_SIZE,
    rng: random.Random | None = None,
) -> list[dict[str, Any]]:
    rng = rng or random.Random()
    pool = list(es.sentences_for_topic(topic_id))
    rng.shuffle(pool)
    return [dict(item) | {"kind": "type"} for item in pool[:count]]


def pick_reading(
    topic_id: str,
    rng: random.Random | None = None,
) -> dict[str, Any] | None:
    rng = rng or random.Random()
    pool = list(es.readings_for_topic(topic_id))
    if not pool:
        return None
    reading = dict(rng.choice(pool))
    reading["questions"] = [dict(q) for q in reading.get("questions") or []]
    return reading
