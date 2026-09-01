"""NCERT-style spherical-mirror ray diagrams."""

from __future__ import annotations

import unittest

from harshit.physics import diagrams as hpd


class TestConcaveImageDiagram(unittest.TestCase):
    def test_between_c_and_f_has_book_labels(self) -> None:
        svg = hpd.svg_concave_image({"position": "between_C_F"})
        for token in ("P", "F", "C", "M", "N", "beyond C"):
            self.assertIn(token, svg)
        self.assertIn(">A</text>", svg)
        self.assertIn(">B</text>", svg)
        self.assertIn("A′", svg)
        self.assertIn("B′", svg)
        self.assertIn("polyline", svg)
        self.assertGreater(svg.count("marker-end"), 3)

    def test_virtual_image_is_behind_the_mirror(self) -> None:
        svg = hpd.svg_concave_image({"position": "between_F_P"})
        self.assertIn("behind the mirror", svg)
        self.assertIn("virtual", svg.lower())
        self.assertIn("stroke-dasharray", svg)
        self.assertIn("A′", svg)

    def test_labels_diagram_is_side_view(self) -> None:
        svg = hpd.svg_spherical_mirror_labels({"mirror_type": "concave"})
        self.assertIn('width="560"', svg)
        self.assertIn(">P</text>", svg)
        self.assertIn(">F</text>", svg)
        self.assertIn(">C</text>", svg)

    def test_axis_is_side_view_not_bowl(self) -> None:
        svg = hpd.svg_concave_image({"position": "between_C_F"})
        self.assertIn('width="560"', svg)
        self.assertGreater(svg.count("<line"), 8)

    def test_all_standard_positions_render(self) -> None:
        for pos in ("infinity", "beyond_C", "at_C", "between_C_F", "at_F", "between_F_P"):
            svg = hpd.svg_concave_image({"position": pos})
            self.assertTrue(svg.startswith("<svg") or "<svg" in svg)
            self.assertIn("</svg>", svg)

    def test_convex_is_virtual(self) -> None:
        svg = hpd.svg_concave_image({"mirror_type": "convex"})
        self.assertIn("virtual", svg.lower())
        self.assertIn("A′", svg)
        self.assertIn("B′", svg)

    def test_sequence_shows_table_9_1(self) -> None:
        svg = hpd.svg_concave_image({"mode": "sequence"})
        self.assertIn("At infinity", svg)
        self.assertIn("Between F and P", svg)
        self.assertIn("Table 9.1", svg)

    def test_virtual_highlight_defaults_inside_f(self) -> None:
        svg = hpd.svg_concave_image({"highlight": "virtual"})
        self.assertIn("behind the mirror", svg)

    def test_ray_rules_are_side_view(self) -> None:
        svg = hpd.svg_mirror_ray_rules({"rule": "parallel"})
        self.assertIn(">P</text>", svg)
        self.assertIn(">F</text>", svg)
        self.assertIn("Fig 9.3", svg)

    def test_sign_axis_uses_ncert_mirror(self) -> None:
        svg = hpd.svg_sign_axis({"highlight": "u"})
        self.assertIn("incident light", svg.lower())
        self.assertIn(">P</text>", svg)

    def test_lens_image_has_foci(self) -> None:
        svg = hpd.svg_lens_image({"lens_type": "convex", "position": "at_2F"})
        self.assertIn("F₁", svg)
        self.assertIn("F₂", svg)
        self.assertIn("A′", svg)

    def test_plane_mirror_has_hatch(self) -> None:
        svg = hpd.svg_plane_mirror_reflection({"highlight": "incident"})
        self.assertGreater(svg.count("<line"), 10)

    def test_every_unit1_visual_type_renders(self) -> None:
        from pathlib import Path
        import json

        schema = json.loads((Path(__file__).resolve().parents[1] / "HarshitPhysics" / "unit1" / "logic_schema.json").read_text())
        seen = 0
        for day in schema["days"]:
            for concept in day.get("concepts") or []:
                visual = concept.get("visual") or {}
                html = hpd.render_diagram_html(visual)
                self.assertIn("<svg", html, msg=concept.get("id"))
                seen += 1
        self.assertEqual(seen, 160)


if __name__ == "__main__":
    unittest.main()
