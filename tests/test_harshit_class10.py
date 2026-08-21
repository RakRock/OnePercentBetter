"""Tests for Harshit Class 10 unit practice."""

from __future__ import annotations

import unittest

import harshit_class10_practice as h10p
import harshit_class10_topics as h10t
import harshit_class10_units as h10u


class TestHarshitClass10(unittest.TestCase):
    def test_unit_catalog_has_fifteen_units(self):
        units = h10u.list_units()
        self.assertEqual(len(units), 15)
        self.assertEqual(units[0]["title"], "Real Numbers")
        self.assertTrue(units[0].get("active"))

    def test_unit1_pdf_exists(self):
        path = h10u.unit_pdf_path(1)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh101.pdf")

    def test_unit2_pdf_exists(self):
        path = h10u.unit_pdf_path(2)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh102.pdf")

    def test_unit2_active_in_catalog(self):
        unit = h10u.get_unit(2)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Polynomials")

    def test_difficulty_maps_to_levels(self):
        self.assertEqual(h10t.DIFFICULTY_TO_LEVEL[1], "A")
        self.assertEqual(h10t.DIFFICULTY_TO_LEVEL[5], "E")

    def test_build_session_fifteen_questions(self):
        config = h10t.default_week_config(1)
        qs, _ = h10p.build_session_set(1, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_build_session_unit2(self):
        config = h10t.default_week_config(2)
        qs, _ = h10p.build_session_set(2, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_question_has_four_options(self):
        q = h10t.generate_question(1, 1, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(len(q["options"]), 4)
        self.assertGreaterEqual(q["answer"], 0)
        self.assertLess(q["answer"], 4)

    def test_generate_unit2_question(self):
        q = h10t.generate_question(2, 1, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 2)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 2 Polynomials")

    def test_unit3_pdf_exists(self):
        path = h10u.unit_pdf_path(3)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh103.pdf")

    def test_unit4_pdf_exists(self):
        path = h10u.unit_pdf_path(4)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh104.pdf")

    def test_build_session_unit3(self):
        config = h10t.default_week_config(3)
        qs, _ = h10p.build_session_set(3, config, count=15)
        self.assertEqual(len(qs), 15)

    def test_build_session_unit4(self):
        config = h10t.default_week_config(4)
        qs, _ = h10p.build_session_set(4, config, count=15)
        self.assertEqual(len(qs), 15)


if __name__ == "__main__":
    unittest.main()
