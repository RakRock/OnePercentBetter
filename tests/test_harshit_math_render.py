"""Tests for Harshit math display (subscripts vs exponents, stacked ratios)."""

from __future__ import annotations

import unittest

import harshit_math_render as hmr


class TestCoeffRatioDisplay(unittest.TestCase):
    def test_unicode_ratio_is_not_superscript(self) -> None:
        html = hmr.format_math_display("a₁/a₂ ≠ b₁/b₂")
        self.assertNotIn("<sup", html)
        self.assertIn("border-bottom", html)
        self.assertIn("<sub", html)
        self.assertIn("a", html)

    def test_ascii_ratio_becomes_stacked_fraction(self) -> None:
        html = hmr.format_math_display("a1/a2 = b1/b2 != c1/c2")
        self.assertIn("border-bottom", html)
        self.assertNotIn("<sup", html)

    def test_plain_keeps_subscripts_not_exponents(self) -> None:
        plain = hmr.format_math_plain("a₁/a₂ ≠ b₁/b₂")
        self.assertIn("a₁", plain)
        self.assertIn("a₂", plain)
        self.assertNotIn("a¹", plain)
        self.assertNotIn("a²", plain)

    def test_ascii_plain_uses_subscripts(self) -> None:
        plain = hmr.format_math_plain("a1/a2")
        self.assertEqual(plain, "a₁/a₂")

    def test_implicit_poly_exponent_still_works(self) -> None:
        html = hmr.format_math_display("3x2 + u3")
        self.assertIn("<sup", html)
        plain = hmr.format_math_plain("3x2")
        self.assertIn("²", plain)

    def test_explanation_line(self) -> None:
        html = hmr.format_math_display(
            "a₁/a₂ ≠ b₁/b₂ confirms intersecting lines at one point."
        )
        self.assertIn("border-bottom", html)
        self.assertIn("intersecting", html)
        self.assertNotIn("<sup", html)


if __name__ == "__main__":
    unittest.main()
