"""Chemical Reactions Assessment 1 practice from the study-guide data tables."""

from __future__ import annotations

import unittest

import arjun_chem_assessment1 as guide


class TestChemicalReactionsAssessment(unittest.TestCase):
    def test_investigation_tables_match_the_study_guide(self):
        self.assertEqual(guide.INVESTIGATION_A["rows"][0], ["Sealed bottle", "156.8 g", "156.8 g", "0.0 g"])
        self.assertEqual(guide.INVESTIGATION_A["rows"][1], ["Open cup", "156.8 g", "154.9 g", "-1.9 g"])
        bubbles = {row[0]: row[2] for row in guide.INVESTIGATION_B["rows"]}
        self.assertEqual(bubbles["Baking soda + citric acid + water"], "Yes")
        self.assertEqual(bubbles["Baking soda + citric acid dry"], "No")
        self.assertEqual(bubbles["Baking soda + citric acid + oil"], "No")

    def test_each_prompt_keeps_its_table_and_a_correct_choice(self):
        ids = [question["id"] for question in guide.QUESTIONS]
        self.assertEqual(ids, ["a-closed", "a-open-loss", "a-not-destroyed", "b-claim", "b-evidence", "b-oil"])
        for question in guide.QUESTIONS:
            self.assertEqual(len(question["options"]), 4)
            self.assertEqual(question["answer"], 0)
            self.assertEqual(question["table"]["columns"][0] in ("System", "Combination"), True)

    def test_quiz_keeps_order_and_does_not_rewrite_the_bank(self):
        original = [list(question["options"]) for question in guide.QUESTIONS]
        quiz = guide.build_quiz()
        self.assertEqual([question["id"] for question in quiz], [question["id"] for question in guide.QUESTIONS])
        for question, source in zip(quiz, guide.QUESTIONS):
            self.assertEqual(question["options"][question["answer"]], source["options"][0])
        self.assertEqual([list(question["options"]) for question in guide.QUESTIONS], original)
