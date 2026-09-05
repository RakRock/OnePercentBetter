"""Tests for Harshit PreReq lesson notes."""

from __future__ import annotations

import unittest

import harshit_geometry_diagrams as hgd
import harshit_prereq_unit_notes as hpun


class TestPrereq4LinesAnglesNotes(unittest.TestCase):
    def test_topic_guide_covers_four_ideas(self) -> None:
        guide = hpun.get_topic_guide(4, 1)
        self.assertIsNotNone(guide)
        titles = " ".join(s["title"] for s in guide["sections"])
        for needle in ("two points", "Complementary", "Vertically opposite", "transversal"):
            self.assertIn(needle, titles)
        body = " ".join(s["body"] for s in guide["sections"])
        for needle in ("90°", "180°", "vertically opposite", "corresponding", "co-interior"):
            self.assertIn(needle, body.lower() if needle.islower() else body)

    def test_triangles_guide_covers_core_ideas(self) -> None:
        guide = hpun.get_topic_guide(4, 2)
        self.assertIsNotNone(guide)
        titles = " ".join(s["title"] for s in guide["sections"])
        for needle in ("180°", "Exterior", "Congruence", "Isosceles", "Inequalities"):
            self.assertIn(needle, titles)
        body = " ".join(s["body"] for s in guide["sections"])
        for needle in ("SSS", "SAS", "ASA", "RHS", "Triangle inequality"):
            self.assertIn(needle, body)

    def test_quadrilaterals_guide_covers_core_ideas(self) -> None:
        guide = hpun.get_topic_guide(4, 3)
        self.assertIsNotNone(guide)
        titles = " ".join(s["title"] for s in guide["sections"])
        for needle in ("quadrilateral", "Parallelogram", "Rectangle", "Trapezium", "Mid-point"):
            self.assertIn(needle, titles)
        body = " ".join(s["body"] for s in guide["sections"])
        for needle in ("360°", "bisect", "rhombus", "kite"):
            self.assertIn(needle, body)

    def test_circles_guide_covers_core_ideas(self) -> None:
        guide = hpun.get_topic_guide(4, 4)
        self.assertIsNotNone(guide)
        titles = " ".join(s["title"] for s in guide["sections"])
        for needle in ("Parts of a circle", "Equal chords", "Perpendicular", "centre vs the rim", "Cyclic", "sector"):
            self.assertIn(needle, titles)
        body = " ".join(s["body"] for s in guide["sections"])
        for needle in ("diameter", "2πr", "SSS", "bisects", "twice", "180°", "segment"):
            self.assertIn(needle, body)

    def test_note_diagrams_render(self) -> None:
        for topic_id in (1, 2, 3, 4):
            guide = hpun.get_topic_guide(4, topic_id)
            for sec in guide["sections"]:
                for spec in sec.get("diagrams") or []:
                    svg = hgd.render_geometry_svg(spec)
                    self.assertTrue(svg and svg.startswith("<svg"), msg=spec)


if __name__ == "__main__":
    unittest.main()
