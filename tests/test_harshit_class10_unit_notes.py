"""Tests for Class 10 unit teaching guides."""

from __future__ import annotations

import unittest

import harshit_class10_unit_notes as h10un


class TestClass10UnitNotes(unittest.TestCase):
    def test_all_active_units_have_guides(self) -> None:
        import harshit_class10_units as h10u

        active = [u["id"] for u in h10u.list_units() if u.get("active")]
        for uid in active:
            with self.subTest(unit_id=uid):
                self.assertTrue(
                    h10un.unit_guide_available(uid),
                    f"Unit {uid} is active but has no unit guide",
                )
                guide = h10un.get_unit_guide(uid)
                assert guide is not None
                self.assertGreaterEqual(len(guide["sections"]), 5)
                ids = h10un.guide_section_ids(uid)
                for section_id in ("overview", "topics", "ncert", "formulas", "teaching"):
                    self.assertIn(section_id, ids)

    def test_unit1_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(1))
        guide = h10un.get_unit_guide(1)
        assert guide is not None
        self.assertIn("Real Numbers", guide["title"])

    def test_unit1_formulas_mention_hcf_lcm(self) -> None:
        guide = h10un.get_unit_guide(1)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("HCF", formulas["body"])
        self.assertIn("LCM", formulas["body"])

    def test_unit4_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(4))
        guide = h10un.get_unit_guide(4)
        assert guide is not None
        self.assertIn("Quadratic Equations", guide["title"])

    def test_unit4_formulas_mention_discriminant(self) -> None:
        guide = h10un.get_unit_guide(4)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("Δ", formulas["body"])
        self.assertIn("quadratic formula", formulas["body"].lower())

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

    def test_unit11_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(11))
        guide = h10un.get_unit_guide(11)
        assert guide is not None
        self.assertIn("Areas Related to Circles", guide["title"])

    def test_unit11_formulas_mention_sector(self) -> None:
        guide = h10un.get_unit_guide(11)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("θ/360", formulas["body"])
        self.assertIn("πr²", formulas["body"])

    def test_unit12_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(12))
        guide = h10un.get_unit_guide(12)
        assert guide is not None
        self.assertIn("Surface Areas and Volumes", guide["title"])

    def test_unit12_formulas_mention_cylinder(self) -> None:
        guide = h10un.get_unit_guide(12)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("2πrh", formulas["body"])
        self.assertIn("πr²h", formulas["body"])

    def test_unit13_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(13))
        guide = h10un.get_unit_guide(13)
        assert guide is not None
        self.assertIn("Statistics", guide["title"])

    def test_unit13_formulas_mention_median(self) -> None:
        guide = h10un.get_unit_guide(13)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("Median", formulas["body"])
        self.assertIn("Σfixi", formulas["body"])

    def test_unit14_guide_available(self) -> None:
        self.assertTrue(h10un.unit_guide_available(14))
        guide = h10un.get_unit_guide(14)
        assert guide is not None
        self.assertIn("Probability", guide["title"])

    def test_unit14_formulas_mention_complement(self) -> None:
        guide = h10un.get_unit_guide(14)
        assert guide is not None
        formulas = next(s for s in guide["sections"] if s["id"] == "formulas")
        self.assertIn("1 − P(E)", formulas["body"])
        self.assertIn("P(E)", formulas["body"])

    def test_guide_version_tracked_for_units_with_guides(self) -> None:
        self.assertEqual(h10un.guide_version(1), 1)
        self.assertEqual(h10un.guide_version(2), 1)
        self.assertEqual(h10un.guide_version(3), 1)
        self.assertEqual(h10un.guide_version(4), 1)
        self.assertEqual(h10un.guide_version(5), 1)
        self.assertEqual(h10un.guide_version(6), 1)
        self.assertEqual(h10un.guide_version(7), 1)
        self.assertEqual(h10un.guide_version(8), 1)
        self.assertEqual(h10un.guide_version(9), 1)
        self.assertEqual(h10un.guide_version(10), 1)
        self.assertEqual(h10un.guide_version(11), 1)
        self.assertEqual(h10un.guide_version(12), 1)
        self.assertEqual(h10un.guide_version(13), 1)
        self.assertEqual(h10un.guide_version(14), 1)
        self.assertEqual(h10un.guide_version(15), 0)


if __name__ == "__main__":
    unittest.main()
