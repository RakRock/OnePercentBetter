"""Tests for numeric expression evaluation and MCQ answer-key verification."""

from __future__ import annotations

import unittest

from numeric_expression_eval import (
    compute_expected,
    compute_fraction_of_remainder,
    compute_linear_expression,
    compute_scientific_notation_sum,
    ensure_numeric_answer_key,
    evaluate_numeric,
    extract_expression,
    option_numeric_value,
    options_equivalent,
    parse_scientific_notation_value,
    system_options_equivalent,
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

    def test_order_rationals_greatest_to_least(self) -> None:
        question = "Order 3/4, 0.7, and 72% from greatest to least."
        options = [
            "3/4, 0.7, 72%",
            "3/4, 72%, 0.7",
            "72%, 3/4, 0.7",
            "0.7, 72%, 3/4",
        ]
        self.assertEqual(ensure_numeric_answer_key(question, options, 0), 1)

    def test_scientific_notation_addition(self) -> None:
        question = "Add 4.5 × 10⁶ and 3.2 × 10⁵. Give the sum in scientific notation."
        options = ["7.7 × 10⁶", "4.82 × 10⁶", "7.7 × 10⁵", "48.2 × 10⁵"]
        self.assertEqual(ensure_numeric_answer_key(question, options, 0), 1)
        self.assertAlmostEqual(parse_scientific_notation_value("4.82 × 10⁶"), 4820000.0)

    def test_scientific_notation_same_exponent(self) -> None:
        question = "Add 4.5 × 10³ and 3.2 × 10³ in scientific notation."
        options = ["7.7 × 10³", "4.82 × 10³", "77 × 10²", "1.45 × 10⁴"]
        self.assertEqual(ensure_numeric_answer_key(question, options, 1), 0)

    def test_improper_scientific_notation_not_equivalent_to_proper(self) -> None:
        self.assertFalse(options_equivalent("12 × 10⁹", "1.2 × 10¹⁰"))
        self.assertTrue(options_equivalent("1.2 × 10¹⁰", "1.20 × 10¹⁰"))

    def test_mixed_number_parsing(self) -> None:
        from numeric_expression_eval import option_numeric_value, parse_mixed_number_value

        self.assertAlmostEqual(parse_mixed_number_value("8 1/3"), 25 / 3)
        self.assertAlmostEqual(parse_mixed_number_value("6 1/3"), 19 / 3)
        self.assertAlmostEqual(option_numeric_value("8 1/3"), 25 / 3)
        self.assertFalse(options_equivalent("8", "8 1/3"))

    def test_power_expression_parsing(self) -> None:
        from numeric_expression_eval import _parse_power_term, power_options_equivalent

        self.assertEqual(_parse_power_term("3¹⁰⁰"), (3.0, 100.0))
        self.assertEqual(_parse_power_term("3²⁹⁷"), (3.0, 297.0))
        self.assertFalse(power_options_equivalent("3²⁹⁷", "3¹⁰⁰"))
        self.assertTrue(power_options_equivalent("3¹⁰⁰", "3^100"))
        self.assertFalse(options_equivalent("3²⁹⁷", "3¹⁰⁰"))
        self.assertFalse(options_equivalent("3⁹⁹ + 3", "3¹⁰⁰"))

    def test_linear_n_expression_parsing(self) -> None:
        from numeric_expression_eval import _parse_linear_n_expression, linear_n_options_equivalent

        self.assertEqual(_parse_linear_n_expression("3n + 1"), (3, 1))
        self.assertEqual(_parse_linear_n_expression("3n - 1"), (3, -1))
        self.assertEqual(_parse_linear_n_expression("n + 3"), (1, 3))
        self.assertFalse(linear_n_options_equivalent("3n - 1", "3n + 1"))
        self.assertTrue(linear_n_options_equivalent("3n + 1", "3n+1"))
        self.assertFalse(options_equivalent("3n - 1", "3n + 1"))

    def test_thousands_separator_parsing(self) -> None:
        from numeric_expression_eval import option_numeric_value

        self.assertEqual(option_numeric_value("1,456,789,874,500"), 1456789874500.0)
        self.assertFalse(options_equivalent("1,456,789,874,500", "1"))

    def test_sci_notation_sum_prefers_proper_form_key(self) -> None:
        question = (
            "Add the numbers: (6.8 × 10³) + (4.5 × 10⁵). "
            "First align the powers of 10, then give the sum in scientific notation."
        )
        options = ["11.3 × 10⁵", "456.8 × 10³", "4.568 × 10⁵", "4.568 × 10³"]
        self.assertEqual(ensure_numeric_answer_key(question, options, 1), 2)

    def test_equation_system_options_not_collapsed_to_leading_coefficient(self) -> None:
        opts = [
            "3p + 4d = 11 and 2p + 2d = 12",
            "3p + 2d = 11 and 2p + 4d = 12",
            "3p + 2d = 12 and 2p + 4d = 11",
            "p + d = 11 and 3p + 2d = 12",
        ]
        self.assertIsNone(option_numeric_value(opts[0]))
        self.assertFalse(options_equivalent(opts[0], opts[1]))
        self.assertTrue(system_options_equivalent(opts[1], "2p + 4d = 12 and 3p + 2d = 11"))

    def test_linear_expression_figure_45(self) -> None:
        question = (
            "A table shows figure number n and number of tiles: 3n+1. "
            "How many tiles are in figure 45?"
        )
        options = ["139 tiles", "136 tiles", "135", "130"]
        self.assertEqual(ensure_numeric_answer_key(question, options, 0), 1)

    def test_exponent_pemdas_expression(self) -> None:
        question = "Simplify: (4³ - 2⁴) × 2²."
        options = ["128", "320", "192", "256"]
        self.assertEqual(ensure_numeric_answer_key(question, options, 1), 2)

    def test_rejects_contradictory_explanation(self) -> None:
        from numeric_expression_eval import validate_explanation_matches_key

        explanation = (
            "4³=64, 2⁴=16; 64-16=48; 48×2²=48×4=192? Wait, recalculate: correct path yields 320"
        )
        options = ["128", "320", "192", "256"]
        with self.assertRaises(ValueError):
            validate_explanation_matches_key(explanation, options, 1)

    def test_fraction_of_remainder_chocolate_bar(self) -> None:
        question = (
            "After eating 1/8 of a chocolate bar, 4/9 of the remaining chocolate was hidden. "
            "What fraction of the original bar is hidden?"
        )
        self.assertAlmostEqual(compute_fraction_of_remainder(question), 7 / 18)
        options = ["1/2", "7/18", "4/72", "28/72"]
        self.assertEqual(ensure_numeric_answer_key(question, options, 0), 1)

    def test_skips_non_numeric_questions(self) -> None:
        question = "Which expression shows the distributive property?"
        options = ["a", "b", "c", "d"]
        self.assertEqual(ensure_numeric_answer_key(question, options, 2), 2)

    def test_parentheses_and_caret_exponents(self) -> None:
        self.assertAlmostEqual(evaluate_numeric("(5-2)^2*3^0"), 9.0)


if __name__ == "__main__":
    unittest.main()
