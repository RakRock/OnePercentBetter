"""
Academic vocabulary practice for Arjun — ordered Tier 2-style words with definitions.

Questions are multiple choice (4 options): pick the meaning that matches the word.
"""

from __future__ import annotations

import json
import os
import random
from typing import Any

_DIR = os.path.dirname(os.path.abspath(__file__))
_JSON_PATH = os.path.join(_DIR, "arjun_vocabulary.json")

WORDS: list[dict[str, str]] = []

WORDS_PER_QUIZ = 10


def _load_words() -> list[dict[str, str]]:
    global WORDS
    if WORDS:
        return WORDS
    with open(_JSON_PATH, encoding="utf-8") as f:
        WORDS = json.load(f)
    if len(WORDS) != 200:
        raise ValueError(f"Expected 200 vocabulary entries, got {len(WORDS)}")
    return WORDS


def total_words() -> int:
    return len(_load_words())


def build_quiz(start_index: int) -> tuple[list[dict[str, Any]], int]:
    """
    Build WORDS_PER_QUIZ multiple-choice questions starting at start_index (wraps at end).

    Returns (questions, next_start_index_after_this_batch).
    """
    bank = _load_words()
    n = len(bank)
    k = WORDS_PER_QUIZ
    all_defs = [entry["definition"] for entry in bank]

    questions = []
    for i in range(k):
        idx = (start_index + i) % n
        entry = bank[idx]
        correct = entry["definition"]
        wrong_pool = [d for j, d in enumerate(all_defs) if j != idx]
        wrong = random.sample(wrong_pool, 3)
        options = [correct] + wrong
        random.shuffle(options)
        answer_idx = options.index(correct)
        questions.append({
            "word": entry["word"],
            "definition": correct,
            "options": options,
            "answer": answer_idx,
        })

    next_start = (start_index + k) % n
    return questions, next_start


def quiz_position_blurb(start_index: int) -> str:
    n = total_words()
    return (
        f"This quiz has **{WORDS_PER_QUIZ}** words in order, starting at "
        f"word **{start_index + 1}** of **{n}** (after word {n} it continues from word 1)."
    )
