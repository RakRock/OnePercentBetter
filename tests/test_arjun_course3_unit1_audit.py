"""Independent Unit 1 answer-key checks."""

from __future__ import annotations

import unittest

from arjun_course3_unit1_audit import independent_answer_index
from numeric_expression_eval import ensure_numeric_answer_key


class TestUnit1AnswerAudit(unittest.TestCase):
    def test_decreasing_order_with_percent(self) -> None:
        question = "Place the numbers in DECREASING order: 3/5, 0.33, 33.5%"
        options = [
            "3/5, 33.5%, 0.33",
            "0.33, 33.5%, 3/5",
            "33.5%, 3/5, 0.33",
            "3/5, 0.33, 33.5%",
        ]
        self.assertEqual(ensure_numeric_answer_key(question, options, 2), 0)

    def test_root_between_claim_is_true(self) -> None:
        q = {
            "question": "Liam says √75 is between 8 and 9 because 64 < 75 < 81. Was Liam correct? Explain.",
            "options": [
                "No — √81=9 and 75<81, so √75 is a little less than 9",
                "Yes — round up from 64",
                "No — √75 is about 10",
                "Yes — √64=8 and √81=9",
            ],
            "answer": 0,
        }
        idx, how = independent_answer_index(q)
        self.assertEqual(how, "was-root-between")
        self.assertEqual(idx, 3)

    def test_remaining_mixed_pounds(self) -> None:
        q = {
            "question": "A bag has 7/8 pound of trail mix. Dad eats 1/4 pound and Mom eats 3/8 pound. How much trail mix remains?",
            "options": ["3/8", "1/4", "1/2", "5/8"],
            "answer": 0,
        }
        idx, how = independent_answer_index(q)
        self.assertEqual(how, "remaining")
        self.assertEqual(idx, 1)

    def test_arithmetic_fifth_term(self) -> None:
        q = {
            "question": "The sequence begins at 1/3 and adds 2/3 to each term. What is the 5th term?",
            "options": ["8/3", "3", "7/3", "11/3"],
            "answer": 0,
        }
        idx, how = independent_answer_index(q)
        self.assertEqual(how, "arithmetic-nth")
        self.assertEqual(idx, 1)

    def test_square_area_from_perimeter_with_units(self) -> None:
        q = {
            "question": "A square garden has a perimeter of 36 m. What is the area of the garden in square meters?",
            "options": ["81 m²", "18 m²", "1296 m²", "324 m²"],
            "answer": 0,
        }
        idx, how = independent_answer_index(q)
        self.assertEqual(how, "square-perimeter-area")
        self.assertEqual(idx, 0)


if __name__ == "__main__":
    unittest.main()
