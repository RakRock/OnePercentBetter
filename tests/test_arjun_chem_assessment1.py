"""Chemical Reactions Assessment 1 practice from the full study guide."""

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
        self.assertEqual(len(guide.CHOICE_QUESTIONS), 30)
        self.assertEqual(guide.DENSITY_COLUMN["rows"][0][1], "0.85 g/mL")
        self.assertEqual(guide.DENSITY_COLUMN["rows"][-1][1], "1.30 g/mL")

    def test_calculated_answers(self):
        by_id = {question["id"]: question for question in guide.DATA_QUESTIONS}
        self.assertEqual(by_id["c-volume"]["options"][0], "22.5 mL")
        self.assertEqual(by_id["c-density"]["options"][0], "1.20 g/mL")
        self.assertIn("24.9 kg", by_id["f-a"]["options"][0])
        self.assertIn("26.8 kg", by_id["f-b"]["options"][0])

    def test_each_part_has_one_correct_choice(self):
        for section in ("choice", "words", "data", "cer"):
            questions = guide.questions_for(section)
            self.assertGreaterEqual(len(questions), 5)
            ids = [question["id"] for question in questions]
            self.assertEqual(len(ids), len(set(ids)))
            for question in questions:
                self.assertEqual(len(question["options"]), 4)
                self.assertEqual(question["answer"], 0)

    def test_choice_sample_does_not_rewrite_the_bank(self):
        original = [list(question["options"]) for question in guide.CHOICE_QUESTIONS]
        quiz = guide.build_quiz("choice")
        self.assertEqual(len(quiz), guide.CHOICE_QUIZ_SIZE)
        by_id = {question["id"]: question for question in guide.CHOICE_QUESTIONS}
        for question in quiz:
            self.assertEqual(question["options"][question["answer"]], by_id[question["id"]]["options"][0])
        self.assertEqual([list(question["options"]) for question in guide.CHOICE_QUESTIONS], original)

    def test_data_quiz_keeps_packet_order(self):
        quiz = guide.build_quiz("data")
        self.assertEqual(
            [question["id"] for question in quiz],
            [question["id"] for question in guide.DATA_QUESTIONS],
        )
