"""Lesson 5 gas-properties practice from the class slides and chart."""

from __future__ import annotations

import unittest

import arjun_gas_lesson5 as lesson


class TestGasLesson5(unittest.TestCase):
    def test_chart_and_reference_table(self):
        chart = {row[0]: row[1:] for row in lesson.INVESTIGATION_CHART["rows"]}
        self.assertIn("Puts the flame out", chart["Helium"][0])
        self.assertIn("0.179", chart["Helium"][1])
        self.assertIn("Denser than air", chart["Bath bomb gas"][1])
        gases = {row[0]: row[1] for row in lesson.COMMON_GASES["rows"]}
        self.assertEqual(gases["Helium"], "0.179")
        self.assertEqual(gases["Carbon dioxide"], "1.960")
        self.assertEqual(gases["Air"], "1.160")

    def test_quiz_keeps_order_and_the_correct_choice(self):
        original = [list(question["options"]) for question in lesson.QUESTIONS]
        quiz = lesson.build_quiz()
        self.assertEqual([question["id"] for question in quiz], [question["id"] for question in lesson.QUESTIONS])
        for question, source in zip(quiz, lesson.QUESTIONS):
            self.assertEqual(question["options"][question["answer"]], source["options"][0])
            self.assertIn("table", question)
        self.assertEqual([list(question["options"]) for question in lesson.QUESTIONS], original)
