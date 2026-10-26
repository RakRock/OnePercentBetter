"""
Lesson 5 Day 2: properties of gases and the bath-bomb investigation.

The handout chart is the three rows students fill in. The common-gases table
is the reference from the class slides. Correct choice is options[0].
"""

from __future__ import annotations

import copy
import random

TITLE = "Lesson 5 · Gas properties"

INVESTIGATION_CHART = {
    "title": "Gas Properties Investigation",
    "intro": "Air and helium come from the known-gas tests. Bath-bomb gas put the flame out and was denser than air.",
    "columns": ["Investigation", "Flammability?", "Density?"],
    "rows": [
        ["Air", "Keeps a flame burning", "1.160 g/L, the air around the bottle"],
        ["Helium", "Puts the flame out", "0.179 g/L, less than air, so it floats up"],
        ["Bath bomb gas", "Puts the flame out", "Denser than air, so it sinks"],
    ],
}

COMMON_GASES = {
    "title": "Some common gases",
    "intro": "Density is in g/L at 0°C. Flammability is how the gas interacts with a flame.",
    "columns": ["Gas", "Density (g/L)", "Flame"],
    "rows": [
        ["Nitrogen", "1.250", "Puts a flame out"],
        ["Oxygen", "1.430", "Makes a flame bigger"],
        ["Argon", "1.780", "Puts a flame out"],
        ["Carbon dioxide", "1.960", "Puts a flame out"],
        ["Neon", "0.900", "Puts a flame out"],
        ["Helium", "0.179", "Puts a flame out"],
        ["Methane", "0.714", "Makes a flame bigger; can explode"],
        ["Hydrogen", "0.090", "Makes a flame bigger; can explode"],
        ["Propane", "2.000", "Makes a flame bigger; can explode"],
        ["Air", "1.160", "Keeps a flame burning"],
    ],
}


def _q(question_id, question, options, explanation, table):
    return {
        "id": question_id,
        "topic": "Lesson 5",
        "table": table,
        "question": question,
        "options": options,
        "answer": 0,
        "explanation": explanation,
    }


QUESTIONS: list[dict] = [
    _q(
        "focus",
        "What question is this investigation trying to answer?",
        [
            "What gas could be coming from the bath bomb?",
            "Which liquid is the least dense in a column?",
            "How many sensors fit on an ocean float?",
            "What is the mass of a carrot?",
        ],
        "The lesson focus is the gas made when the bath bomb reacts.",
        INVESTIGATION_CHART,
    ),
    _q(
        "air-flame",
        "On the investigation chart, what does air do to a flame?",
        [
            "It keeps the flame burning",
            "It always puts the flame out",
            "It makes the flame explode",
            "It has no particles, so the flame cannot burn",
        ],
        "The common-gases table says air can maintain an open flame. That is the air row on the chart.",
        INVESTIGATION_CHART,
    ),
    _q(
        "helium-flame",
        "What does helium do to a flame?",
        [
            "It puts the flame out",
            "It makes the flame bigger",
            "It keeps the flame burning the same way air does",
            "It turns the flame into carbon dioxide",
        ],
        "Helium is listed as a gas that will extinguish a flame.",
        COMMON_GASES,
    ),
    _q(
        "cross-off",
        "The bath-bomb gas put the flame out. Which gases should be crossed off?",
        [
            "Oxygen, methane, hydrogen, and propane, because they make a flame bigger",
            "Helium and carbon dioxide, because they put a flame out",
            "Only air, because air is a mixture",
            "Every gas on the table",
        ],
        "A gas that makes a flame bigger cannot be the bath-bomb gas. Oxygen, methane, hydrogen, and propane do that. Air keeps a flame burning, so it is crossed off too.",
        COMMON_GASES,
    ),
    _q(
        "still-possible",
        "After the flame test, which gas is still a possible bath-bomb gas?",
        [
            "Helium, because it also puts a flame out",
            "Oxygen, because it makes a flame bigger",
            "Propane, because it is denser than air",
            "Air, because the test was done in a room",
        ],
        "Helium, nitrogen, argon, carbon dioxide, and neon all put a flame out, so the flame test does not choose among them.",
        COMMON_GASES,
    ),
    _q(
        "helium-density",
        "How does helium’s density compare with air, and what does it do?",
        [
            "0.179 g/L is less than air’s 1.160 g/L, so helium floats upward",
            "0.179 g/L is greater than air, so helium sinks",
            "Helium and air have the same density",
            "Helium has no density because it puts flames out",
        ],
        "Key model idea 7: a less dense gas floats upward when the gas around it is denser.",
        COMMON_GASES,
    ),
    _q(
        "idea-8",
        "Key model idea 8 says a denser gas…",
        [
            "Sinks when the gas around it is less dense",
            "Always floats, no matter what is around it",
            "Changes its density each time it is tested",
            "Stops being matter",
        ],
        "Denser gases and liquids sink downward when they are surrounded by less dense ones.",
        INVESTIGATION_CHART,
    ),
    _q(
        "idea-6",
        "Key model idea 6 says…",
        [
            "Properties do not change for a substance",
            "Each test gives a substance a new density",
            "A gas can be flammable on one day and not the next",
            "Only solids have properties",
        ],
        "A property is a characteristic of a substance that stays the same. Helium’s density stays 0.179 g/L.",
        COMMON_GASES,
    ),
    _q(
        "bath-density",
        "The bath-bomb gas sank. What does that add to the flame result?",
        [
            "It is denser than air, so a less-dense gas such as helium is ruled out",
            "It is less dense than air, so it must be helium",
            "Sinking proves the gas is oxygen",
            "Density and flammability are the same property",
        ],
        "Helium and neon are less dense than air, so they would float. A gas that sinks is denser than air.",
        INVESTIGATION_CHART,
    ),
    _q(
        "not-proof",
        "Both properties fit carbon dioxide. Why is that not a complete identification?",
        [
            "Argon also puts a flame out and is denser than air, so more evidence is needed",
            "Carbon dioxide makes flames bigger, so it is already ruled out",
            "One property is enough to name any gas",
            "Air and carbon dioxide have the same density",
        ],
        "Carbon dioxide is 1.960 g/L and puts flames out. Argon is 1.780 g/L and also puts flames out. Two matching properties still leave more than one candidate.",
        COMMON_GASES,
    ),
]


def _shuffle_choices(question: dict) -> dict:
    item = copy.deepcopy(question)
    correct = item["options"][item["answer"]]
    options = list(item["options"])
    random.shuffle(options)
    item["options"] = options
    item["answer"] = options.index(correct)
    return item


def build_quiz() -> list[dict]:
    return [_shuffle_choices(question) for question in QUESTIONS]
