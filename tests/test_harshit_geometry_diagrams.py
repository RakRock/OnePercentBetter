"""Tests for Harshit geometry diagram inference and Example 6 figures."""

from __future__ import annotations

import unittest

import harshit_geometry_diagrams as hgd
import harshit_math_diagrams as hmd


class TestHarshitGeometryDiagrams(unittest.TestCase):
    def test_infer_example6_midpoint_diagram(self) -> None:
        q = {
            "prereq_id": 4,
            "topic": 3,
            "question": (
                "ABCD is a parallelogram with P and Q midpoints of AB and CD. "
                "AQ and DP intersect at S. Which quadrilateral is formed by APCQ?"
            ),
        }
        spec = hgd.infer_geometry_diagram(q)
        self.assertIsNotNone(spec)
        assert spec is not None
        self.assertEqual(spec["type"], "parallelogram_midpoints")
        self.assertEqual(spec["highlight"], "APCQ")

    def test_fix_rewrites_dense_stem_and_adds_diagram(self) -> None:
        q = {
            "question": (
                "ABCD is a parallelogram with P and Q midpoints of AB and CD. "
                "AQ and DP intersect at S. Which quadrilateral is formed by APCQ?"
            ),
            "options": ["trapezium", "parallelogram", "rhombus", "rectangle"],
            "answer": 1,
            "explanation": "AP || QC and AP = QC from midpoint properties.",
        }
        fixed = hmd.fix_parallelogram_midpoint_question(q)
        self.assertIn("Use the diagram", fixed["question"])
        self.assertIn("shaded", fixed["question"].lower())
        self.assertEqual(fixed["diagram"]["type"], "parallelogram_midpoints")
        self.assertIn("Step 1", fixed["explanation"])

    def test_render_example6_svg(self) -> None:
        svg = hgd.svg_parallelogram_midpoints(highlight="APCQ")
        self.assertIn("APCQ", svg)
        self.assertIn("<svg", svg)


if __name__ == "__main__":
    unittest.main()
