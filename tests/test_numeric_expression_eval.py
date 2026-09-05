"""Tests for numeric expression evaluation and MCQ answer-key verification."""

from __future__ import annotations

import unittest

from numeric_expression_eval import (
    compute_expected,
    ensure_numeric_answer_key,
    evaluate_numeric,
    extract_expression,
)


class TestNumericExpressionEval(unittest.TestCase):
    def test_pemdas_with_unicode_exponents(self) -> None:
        expr = extract_expression("Simplify: 4 + (5 - 2)^2 × 3⁰")
        self.assertIsNotNone(expr)
        assert expr is not None
        self.assertAlmostEqual(evaluate_numeric(expr), 13.0)

    def test_fix_wrong_exponent_answer_key(self) -> None:
        question = "Simplify: 4 + (5 - 2)^2 × 3⁰"
        options = ["7", "13", "9", "27"]
        fixed = ensure_numeric_answer_key(question, options, 0)
        self.assertEqual(fixed, 1)
        self.assertEqual(options[fixed], "13")

    def test_keeps_correct_answer_when_already_right(self) -> None:
        question = "Evaluate: 2 + 3 × 4"
        options = ["14", "20", "12", "10"]
        self.assertEqual(ensure_numeric_answer_key(question, options, 0), 0)

    def test_skips_non_numeric_questions(self) -> None:
        question = "Which expression shows the distributive property?"
        options = ["a", "b", "c", "d"]
        self.assertEqual(ensure_numeric_answer_key(question, options, 2), 2)

    def test_parentheses_and_caret_exponents(self) -> None:
        self.assertAlmostEqual(evaluate_numeric("(5-2)^2*3^0"), 9.0)


if __name__ == "__main__":
    unittest.main()
