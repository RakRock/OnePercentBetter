"""Tests for Arjun Course 3 answer grading."""

from __future__ import annotations

import unittest

import arjun_course3_answers as c3ans
from arjun_course3_practice import QUESTION_BANK_BY_UNIT
from arjun_edgenuity_course3_practice import QUESTION_BANK_BY_UNIT as EC3_BANK_BY_UNIT
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

    def test_finalize_question_fixes_rational_ordering(self) -> None:
        q = {
            "question": "Order 3/4, 0.7, and 72% from greatest to least.",
            "options": [
                "3/4, 0.7, 72%",
                "3/4, 72%, 0.7",
                "72%, 3/4, 0.7",
                "0.7, 72%, 3/4",
            ],
            "answer": 0,
        }
        fixed = c3ans.finalize_question(q)
        self.assertEqual(fixed["answer"], 1)
        self.assertEqual(fixed["options"][1], "3/4, 72%, 0.7")

    def test_finalize_question_preserves_multi_answer_mcq(self) -> None:
        q = {
            "question": "Add: 3.4 × 10⁵ + 9.1 × 10⁵. Which answer(s) are correct?",
            "options": [
                "12.5 × 10⁵ only",
                "1.25 × 10⁶ only",
                "Both 12.5 × 10⁵ and 1.25 × 10⁶",
                "12.5 × 10¹⁰",
            ],
            "answer": 2,
        }
        fixed = c3ans.finalize_question(q)
        self.assertEqual(fixed["answer"], 2)

    def test_unit_bank_answer_keys_are_validated(self) -> None:
        for unit_id in range(1, 6):
            for q in QUESTION_BANK_BY_UNIT[unit_id]:
                finalized = c3ans.finalize_question(q)
                ans = finalized.get("answer")
                opts = finalized.get("options") or []
                self.assertIsInstance(ans, int)
                self.assertIn(ans, range(len(opts)))


    def test_edgenuity_bank_answer_keys_are_validated(self) -> None:
        for unit_id, bank in EC3_BANK_BY_UNIT.items():
            for q in bank:
                finalized = c3ans.finalize_question(q)
                ans = finalized.get("answer")
                opts = finalized.get("options") or []
                self.assertIsInstance(ans, int)
                self.assertIn(ans, range(len(opts)))


if __name__ == "__main__":
    unittest.main()
