"""
Chemical Reactions Assessment 1, Part 6, from Arjun's study guide.

The saved PDF shows Investigation A and Investigation B. Each paper prompt
becomes one checked question, and the data table stays on screen.
"""

from __future__ import annotations

import copy
import random

TITLE = "Chemical Reactions Assessment 1"

INVESTIGATION_A = {
    "title": "Investigation A · Open and closed systems",
    "intro": "Students mixed the same amounts of two substances.",
    "columns": ["System", "Mass before", "Mass after", "Change"],
    "rows": [
        ["Sealed bottle", "156.8 g", "156.8 g", "0.0 g"],
        ["Open cup", "156.8 g", "154.9 g", "-1.9 g"],
    ],
}

INVESTIGATION_B = {
    "title": "Investigation B · Bath bomb combination tests",
    "intro": "Each row is one test. Bubbles tells whether the mix fizzed.",
    "columns": ["Combination", "Observation", "Bubbles"],
    "rows": [
        ["Baking soda + water", "Powder partly dissolved", "No"],
        ["Citric acid + water", "Solid dissolved", "No"],
        ["Baking soda + citric acid dry", "Powders mixed; little visible change", "No"],
        ["Baking soda + citric acid + water", "Immediate fizzing and many bubbles", "Yes"],
        ["Baking soda + citric acid + oil", "Powders settled; little visible change", "No"],
    ],
}


def _q(question_id: str, topic: str, table: dict, question: str, options: list[str], explanation: str) -> dict:
    return {
        "id": question_id,
        "topic": topic,
        "table": table,
        "question": question,
        "options": options,
        "answer": 0,
        "explanation": explanation,
    }


# Correct choice is options[0]. build_quiz shuffles a copy and keeps question order.
QUESTIONS: list[dict] = [
    _q(
        "a-closed",
        "Investigation A",
        INVESTIGATION_A,
        "Which system is closed? Use the mass data as evidence.",
        [
            "The sealed bottle, because its mass stayed 156.8 g",
            "The open cup, because its mass fell by 1.9 g",
            "Both, because they started at the same mass",
            "Neither, because both held a mixture",
        ],
        "A closed system does not let matter in or out. The sealed bottle's change is 0.0 g, so the matter stayed inside.",
    ),
    _q(
        "a-open-loss",
        "Investigation A",
        INVESTIGATION_A,
        "Why might the open cup have a lower final mass?",
        [
            "A gas made by the reaction left the open cup",
            "The scale removed 1.9 g on its own",
            "The sealed bottle took mass from the cup",
            "The matter in the cup was destroyed",
        ],
        "The open cup went from 156.8 g to 154.9 g. The same mix in the sealed bottle lost nothing, so the missing mass left the open system.",
    ),
    _q(
        "a-not-destroyed",
        "Investigation A",
        INVESTIGATION_A,
        "Why do these results not show that matter was destroyed?",
        [
            "The sealed bottle kept all 156.8 g, so the matter was still there",
            "The open cup ended heavier than it started",
            "Both systems lost 1.9 g",
            "The change column shows new matter was created",
        ],
        "If the reaction destroyed matter, the sealed bottle would lose mass too. Its change is 0.0 g. The open cup lost mass because material escaped.",
    ),
    _q(
        "b-claim",
        "Investigation B",
        INVESTIGATION_B,
        "Which materials are needed for strong bubbling?",
        [
            "Baking soda, citric acid, and water",
            "Baking soda and water only",
            "Citric acid and water only",
            "Baking soda, citric acid, and oil",
        ],
        "Only baking soda + citric acid + water fizzed immediately, and that is the only row with Bubbles = Yes.",
    ),
    _q(
        "b-evidence",
        "Investigation B",
        INVESTIGATION_B,
        "Which two rows best support that claim?",
        [
            "Baking soda + citric acid + water (Yes) and baking soda + citric acid dry (No)",
            "Baking soda + water (No) and citric acid + water (No)",
            "Baking soda + citric acid + oil (No) and citric acid + water (No)",
            "Baking soda + water (No) and baking soda + citric acid + oil (No)",
        ],
        "The water row shows the strong reaction. The dry row shows the same two powders do not bubble without water. Those two rows together name all three materials.",
    ),
    _q(
        "b-oil",
        "Investigation B",
        INVESTIGATION_B,
        "What does the oil row show?",
        [
            "Oil does not make baking soda and citric acid bubble the way water does",
            "Oil causes the strongest bubbles",
            "Oil destroys the citric acid",
            "Oil seals the cup so mass cannot change",
        ],
        "Baking soda + citric acid + oil settled with little visible change, and Bubbles = No. Water, not just any liquid, is the third material.",
    ),
]


def build_quiz() -> list[dict]:
    """Return every study-guide question, with choices shuffled. Does not change the bank."""
    quiz = []
    for question in QUESTIONS:
        item = copy.deepcopy(question)
        correct = item["options"][item["answer"]]
        options = list(item["options"])
        random.shuffle(options)
        item["options"] = options
        item["answer"] = options.index(correct)
        quiz.append(item)
    return quiz
