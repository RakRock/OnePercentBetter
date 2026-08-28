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

    def test_unit5_pdf_exists(self):
        path = h10u.unit_pdf_path(5)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh105.pdf")

    def test_unit5_active_in_catalog(self):
        unit = h10u.get_unit(5)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Arithmetic Progressions")

    def test_build_session_unit5(self):
        config = h10t.default_week_config(5)
        qs, _ = h10p.build_session_set(5, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_unit5_question(self):
        q = h10t.generate_question(5, 2, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 5)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 5 Arithmetic Progressions")

    def test_unit6_pdf_exists(self):
        path = h10u.unit_pdf_path(6)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh106.pdf")

    def test_unit6_active_in_catalog(self):
        unit = h10u.get_unit(6)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Triangles")

    def test_build_session_unit6(self):
        config = h10t.default_week_config(6)
        qs, _ = h10p.build_session_set(6, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_unit6_question(self):
        q = h10t.generate_question(6, 2, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 6)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 6 Triangles")

    def test_unit7_pdf_exists(self):
        path = h10u.unit_pdf_path(7)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh107.pdf")

    def test_unit7_active_in_catalog(self):
        unit = h10u.get_unit(7)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Coordinate Geometry")

    def test_build_session_unit7(self):
        config = h10t.default_week_config(7)
        qs, _ = h10p.build_session_set(7, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_unit7_question(self):
        q = h10t.generate_question(7, 1, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 7)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 7 Coordinate Geometry")

    def test_unit8_pdf_exists(self):
        path = h10u.unit_pdf_path(8)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh108.pdf")

    def test_unit8_active_in_catalog(self):
        unit = h10u.get_unit(8)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Introduction to Trigonometry")

    def test_build_session_unit8(self):
        config = h10t.default_week_config(8)
        qs, _ = h10p.build_session_set(8, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_unit8_question(self):
        q = h10t.generate_question(8, 2, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 8)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 8 Introduction to Trigonometry")

    def test_unit9_pdf_exists(self):
        path = h10u.unit_pdf_path(9)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh109.pdf")

    def test_unit9_active_in_catalog(self):
        unit = h10u.get_unit(9)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Some Applications of Trigonometry")

    def test_build_session_unit9(self):
        config = h10t.default_week_config(9)
        qs, _ = h10p.build_session_set(9, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_unit9_question(self):
        q = h10t.generate_question(9, 2, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 9)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 9 Applications of Trigonometry")

    def test_unit10_pdf_exists(self):
        path = h10u.unit_pdf_path(10)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh110.pdf")

    def test_unit10_active_in_catalog(self):
        unit = h10u.get_unit(10)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Circles")

    def test_build_session_unit10(self):
        config = h10t.default_week_config(10)
        qs, _ = h10p.build_session_set(10, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_unit10_question(self):
        q = h10t.generate_question(10, 1, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 10)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 10 Circles")

    def test_unit11_pdf_exists(self):
        path = h10u.unit_pdf_path(11)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh111.pdf")

    def test_unit11_active_in_catalog(self):
        unit = h10u.get_unit(11)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Areas Related to Circles")

    def test_build_session_unit11(self):
        config = h10t.default_week_config(11)
        qs, _ = h10p.build_session_set(11, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_unit11_question(self):
        q = h10t.generate_question(11, 1, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 11)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 11 Areas Related to Circles")

    def test_unit12_pdf_exists(self):
        path = h10u.unit_pdf_path(12)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh112.pdf")

    def test_unit12_active_in_catalog(self):
        unit = h10u.get_unit(12)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Surface Areas and Volumes")

    def test_build_session_unit12(self):
        config = h10t.default_week_config(12)
        qs, _ = h10p.build_session_set(12, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_unit12_question(self):
        q = h10t.generate_question(12, 1, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 12)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 12 Surface Areas and Volumes")

    def test_unit13_pdf_exists(self):
        path = h10u.unit_pdf_path(13)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh113.pdf")

    def test_unit13_active_in_catalog(self):
        unit = h10u.get_unit(13)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Statistics")

    def test_build_session_unit13(self):
        config = h10t.default_week_config(13)
        qs, _ = h10p.build_session_set(13, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_unit13_question(self):
        q = h10t.generate_question(13, 1, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 13)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 13 Statistics")

    def test_unit14_pdf_exists(self):
        path = h10u.unit_pdf_path(14)
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "jemh114.pdf")

    def test_unit14_active_in_catalog(self):
        unit = h10u.get_unit(14)
        self.assertIsNotNone(unit)
        self.assertTrue(unit.get("active"))
        self.assertEqual(unit["title"], "Probability")

    def test_build_session_unit14(self):
        config = h10t.default_week_config(14)
        qs, _ = h10p.build_session_set(14, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertGreaterEqual(len({q["topic"] for q in qs}), 3)

    def test_generate_unit14_question(self):
        q = h10t.generate_question(14, 1, "B", templates_only=True)
        self.assertIsNotNone(q)
        self.assertEqual(q["unit_id"], 14)
        self.assertEqual(q["chapter_ref"], "NCERT Ch 14 Probability")

    def test_one_zero_accepts_either_root(self):
        import harshit_math_answers as hma

        q = {
            "question": "One zero of p(x) = x² + 3x - 10 is:",
            "options": ["-5", "2", "-3", "-10"],
            "answer": 1,
        }
        self.assertTrue(hma.is_pick_correct(q, 0))
        self.assertTrue(hma.is_pick_correct(q, 1))
        self.assertFalse(hma.is_pick_correct(q, 2))

    def test_other_zero_does_not_accept_both_roots(self):
        import harshit_math_answers as hma

        q = {
            "question": "One zero of p(x) = x² + 3x - 10 is 2. The other zero is:",
            "options": ["-5", "3", "-3", "-10"],
            "answer": 0,
        }
        self.assertTrue(hma.is_pick_correct(q, 0))
        self.assertFalse(hma.is_pick_correct(q, 1))


if __name__ == "__main__":
    unittest.main()
