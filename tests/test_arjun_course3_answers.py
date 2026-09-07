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

    def test_rejects_improper_scientific_notation_pick(self) -> None:
        q = {
            "question": "Write the estimate in scientific notation.",
            "options": ["12 × 10⁹", "1.2 × 10¹⁰", "1.4 × 10¹⁰", "1.12 × 10¹¹"],
            "answer": 1,
        }
        self.assertTrue(c3ans.is_pick_correct(q, 1))
        self.assertFalse(c3ans.is_pick_correct(q, 0))

    def test_rejects_whole_number_when_mixed_fraction_is_keyed(self) -> None:
        q = {
            "question": "A sequence starts 6 1/3, 7, 7 2/3, … Each term adds the same amount. What is the next term?",
            "options": ["9 1/3", "8", "8 1/3", "Cannot tell from the given information"],
            "answer": 2,
        }
        self.assertTrue(c3ans.is_pick_correct(q, 2))
        self.assertFalse(c3ans.is_pick_correct(q, 1))

    def test_rejects_cubed_exponent_when_tripling_is_keyed(self) -> None:
        q = {
            "question": "If you triple 3⁹⁹, what is the result?",
            "options": ["3²⁹⁷", "3⁹⁹ + 3", "9⁹⁹", "3¹⁰⁰"],
            "answer": 3,
        }
        self.assertTrue(c3ans.is_pick_correct(q, 3))
        self.assertFalse(c3ans.is_pick_correct(q, 0))
        self.assertFalse(c3ans.is_pick_correct(q, 1))

    def test_rejects_wrong_linear_expression(self) -> None:
        q = {
            "question": (
                "A dot pattern has 4 dots in figure 1, 7 in figure 2, and 10 in figure 3 "
                "(each new figure adds 3 dots). Which expression gives the dots in figure n?"
            ),
            "options": ["4n - 3", "n + 3", "3n - 1", "3n + 1"],
            "answer": 3,
        }
        self.assertTrue(c3ans.is_pick_correct(q, 3))
        self.assertFalse(c3ans.is_pick_correct(q, 2))

    def test_rejects_base_when_zero_exponent_keyed(self) -> None:
        q = {
            "id": "cc_u1_exp_zero",
            "question": "Simplify: 1,456,789,874,500⁰",
            "options": ["1,456,789,874,500", "1", "Cannot simplify", "0"],
            "answer": 1,
        }
        self.assertTrue(c3ans.is_pick_correct(q, 1))
        self.assertFalse(c3ans.is_pick_correct(q, 0))

    def test_finalize_fixes_improper_sci_notation_sum_key(self) -> None:
        q = {
            "question": (
                "Add the numbers: (6.8 × 10³) + (4.5 × 10⁵). "
                "First align the powers of 10, then give the sum in scientific notation."
            ),
            "options": ["11.3 × 10⁵", "456.8 × 10³", "4.568 × 10⁵", "4.568 × 10³"],
            "answer": 1,
        }
        fixed = c3ans.finalize_question(q)
        self.assertEqual(fixed["answer"], 2)

    def test_finalize_fixes_same_exponent_sci_notation_sum(self) -> None:
        q = {
            "question": (
                "Add the numbers: (2.5 × 10⁴) + (1.3 × 10⁴). "
                "Align the powers of 10 and give the sum in scientific notation."
            ),
            "options": ["3.8 × 10⁵", "38 × 10³", "3.8 × 10⁴", "2.5 + 1.3 × 10⁴"],
            "answer": 1,
        }
        fixed = c3ans.finalize_question(q)
        self.assertEqual(fixed["answer"], 2)
        self.assertFalse(c3ans.is_pick_correct(fixed, 1))

    def test_rejects_wrong_equation_system_setup(self) -> None:
        q = {
            "question": (
                "At a school fair, Maya buys 3 bags of popcorn and 2 drinks for $11. "
                "Sam buys 2 bags of popcorn and 4 drinks for $12. "
                "Which system sets up the prices without solving?"
            ),
            "options": [
                "3p + 4d = 11 and 2p + 2d = 12",
                "3p + 2d = 11 and 2p + 4d = 12",
                "3p + 2d = 12 and 2p + 4d = 11",
                "p + d = 11 and 3p + 2d = 12",
            ],
            "answer": 1,
        }
        self.assertTrue(c3ans.is_pick_correct(q, 1))
        self.assertFalse(c3ans.is_pick_correct(q, 0))

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
