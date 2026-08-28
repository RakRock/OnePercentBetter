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

    def test_guide_version_tracked_for_units_with_guides(self) -> None:
        self.assertEqual(h10un.guide_version(2), 1)
        self.assertEqual(h10un.guide_version(3), 1)
        self.assertEqual(h10un.guide_version(6), 1)
        self.assertEqual(h10un.guide_version(1), 0)


if __name__ == "__main__":
    unittest.main()
