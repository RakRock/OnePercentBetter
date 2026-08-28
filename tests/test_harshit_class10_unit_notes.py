"""Tests for Class 10 unit teaching guides."""

from __future__ import annotations

import unittest

import harshit_class10_unit_notes as h10un


class TestClass10UnitNotes(unittest.TestCase):
    def test_unit2_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(2))
        self.assertFalse(h10un.unit_guide_available(99))

    def test_unit2_sections(self) -> None:
        guide = h10un.get_unit_guide(2)
        self.assertIsNotNone(guide)
        assert guide is not None
        ids = h10un.guide_section_ids(2)
        self.assertIn("overview", ids)
        self.assertIn("formulas", ids)
        self.assertGreaterEqual(len(guide["sections"]), 4)

    def test_unit2_formulas_mention_sum_product(self) -> None:
        guide = h10un.get_unit_guide(2)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("α + β", formulas["body"])
        self.assertIn("αβ", formulas["body"])

    def test_unit3_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(3))
        guide = h10un.get_unit_guide(3)
        assert guide is not None
        self.assertIn("Pair of Linear Equations", guide["title"])

    def test_unit3_formulas_mention_ratio_test(self) -> None:
        guide = h10un.get_unit_guide(3)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("a₁/a₂", formulas["body"])
        self.assertIn("Substitution", formulas["body"])

    def test_unit5_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(5))
        guide = h10un.get_unit_guide(5)
        assert guide is not None
        self.assertIn("Arithmetic Progressions", guide["title"])

    def test_unit5_formulas_mention_nth_term(self) -> None:
        guide = h10un.get_unit_guide(5)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("aₙ = a + (n − 1)d", formulas["body"])
        self.assertIn("Sₙ", formulas["body"])

    def test_unit6_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(6))
        guide = h10un.get_unit_guide(6)
        assert guide is not None
        self.assertIn("Triangles", guide["title"])

    def test_unit6_formulas_mention_bpt(self) -> None:
        guide = h10un.get_unit_guide(6)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("AD/DB", formulas["body"])
        self.assertIn("AAA", formulas["body"])

    def test_unit7_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(7))
        guide = h10un.get_unit_guide(7)
        assert guide is not None
        self.assertIn("Coordinate Geometry", guide["title"])

    def test_unit7_formulas_mention_distance(self) -> None:
        guide = h10un.get_unit_guide(7)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("√[(x₂ − x₁)²", formulas["body"])
        self.assertIn("Mid-point", formulas["body"])

    def test_unit8_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(8))
        guide = h10un.get_unit_guide(8)
        assert guide is not None
        self.assertIn("Trigonometry", guide["title"])

    def test_unit8_formulas_mention_identity(self) -> None:
        guide = h10un.get_unit_guide(8)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("sin²θ + cos²θ", formulas["body"])
        self.assertIn("30°", formulas["body"])

    def test_unit9_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(9))
        guide = h10un.get_unit_guide(9)
        assert guide is not None
        self.assertIn("Applications", guide["title"])

    def test_unit9_formulas_mention_elevation(self) -> None:
        guide = h10un.get_unit_guide(9)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("Elevation", formulas["body"])
        self.assertIn("tan θ", formulas["body"])

    def test_unit10_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(10))
        guide = h10un.get_unit_guide(10)
        assert guide is not None
        self.assertIn("Circles", guide["title"])

    def test_unit10_formulas_mention_tangent(self) -> None:
        guide = h10un.get_unit_guide(10)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("OP² − r²", formulas["body"])
        self.assertIn("Theorem 10.2", formulas["body"])

    def test_guide_version_tracked_for_units_with_guides(self) -> None:
        self.assertEqual(h10un.guide_version(2), 1)
        self.assertEqual(h10un.guide_version(3), 1)
        self.assertEqual(h10un.guide_version(5), 1)
        self.assertEqual(h10un.guide_version(6), 1)
        self.assertEqual(h10un.guide_version(7), 1)
        self.assertEqual(h10un.guide_version(8), 1)
        self.assertEqual(h10un.guide_version(9), 1)
        self.assertEqual(h10un.guide_version(10), 1)
        self.assertEqual(h10un.guide_version(1), 0)


if __name__ == "__main__":
    unittest.main()
