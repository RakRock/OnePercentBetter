"""Tests for Arjun Course 3 answer grading."""

from __future__ import annotations

import unittest

import arjun_course3_answers as c3ans
from numeric_expression_eval import ensure_simplest_form_answer, validate_distinct_options


class TestArjunCourse3Answers(unittest.TestCase):
    def test_accepts_equivalent_fractions(self) -> None:
        q = {
            "question": "Write 0.454545… as a fraction in simplest form.",
            "options": ["4/9", "45/99", "5/11", "9/20"],
            "answer": 2,
        }
        self.assertTrue(c3ans.is_pick_correct(q, 1))
        self.assertTrue(c3ans.is_pick_correct(q, 2))

    def test_rejects_wrong_fraction(self) -> None:
        q = {
            "question": "Write 0.454545… as a fraction in simplest form.",
            "options": ["4/9", "45/99", "5/11", "9/20"],
            "answer": 2,
        }
        self.assertFalse(c3ans.is_pick_correct(q, 0))

    def test_rejects_duplicate_equivalent_options(self) -> None:
        with self.assertRaises(ValueError):
            validate_distinct_options(["5/11", "45/99", "4/9", "2/3"])

    def test_simplest_form_key_points_at_reduced_fraction(self) -> None:
        options = ["4/9", "45/99", "5/11", "9/20"]
        idx = ensure_simplest_form_answer(
            "Write 0.454545… as a fraction in simplest form.",
            options,
            1,
        )
        self.assertEqual(idx, 2)
        self.assertEqual(options[idx], "5/11")


if __name__ == "__main__":
    unittest.main()
