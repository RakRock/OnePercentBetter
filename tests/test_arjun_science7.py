"""Grade 7 Science Corner curriculum and week pointer."""

from __future__ import annotations

import os
import tempfile
import unittest

import arjun_science7 as sci
import database as db
import science_content as bank


class TestScience7Curriculum(unittest.TestCase):
    def test_six_units_cover_36_lessons(self):
        self.assertEqual(len(sci.UNITS), 6)
        self.assertEqual(len(sci.LESSONS), 36)
        covered = [lesson_id for unit in sci.UNITS for lesson_id in unit["lesson_ids"]]
        self.assertEqual(covered, list(range(1, 37)))

    def test_every_lesson_names_activity_and_ixl(self):
        for lesson in sci.LESSONS:
            self.assertTrue(lesson["activity"].strip())
            self.assertGreaterEqual(len(lesson["ixl"]), 1)
            self.assertEqual(sci.unit_for_lesson(lesson["id"])["id"], lesson["unit_id"])

    def test_grade6_questions_are_placed_or_dropped(self):
        source_ids = {q["id"] for q in bank.QUESTION_BANK}
        kept = {q["id"] for q in sci.QUESTIONS if q["id"] < 1000}
        self.assertTrue(sci.DROPPED.isdisjoint(kept))
        self.assertEqual(source_ids - sci.DROPPED, kept)
        self.assertIn(202, sci.DROPPED)
        self.assertNotIn(202, kept)

    def test_filled_units_have_a_full_lesson_quiz(self):
        counts = sci.question_counts()
        for unit_id in (1, 2, 5):
            for lesson_id in sci.unit_by_id(unit_id)["lesson_ids"]:
                self.assertGreaterEqual(
                    counts[lesson_id],
                    sci.LESSON_QUIZ_SIZE,
                    f"lesson {lesson_id}",
                )

    def test_lesson_quiz_does_not_rewrite_the_bank(self):
        original = [list(q["options"]) for q in sci.questions_for_lesson(6)]
        quiz = sci.build_quiz(lesson_id=6)
        self.assertEqual(len(quiz), sci.LESSON_QUIZ_SIZE)
        after = [list(q["options"]) for q in sci.questions_for_lesson(6)]
        self.assertEqual(original, after)
        self.assertTrue(all(q["lesson"] == 6 for q in quiz))

    def test_unit_mix_draws_across_the_unit(self):
        quiz = sci.build_quiz(unit_id=2)
        self.assertEqual(len(quiz), sci.UNIT_QUIZ_SIZE)
        lessons = {q["lesson"] for q in quiz}
        self.assertTrue(lessons <= set(sci.unit_by_id(2)["lesson_ids"]))

    def test_empty_lesson_quiz_is_empty(self):
        self.assertEqual(sci.build_quiz(lesson_id=36), [])

    def test_clamp_lesson(self):
        self.assertEqual(sci.clamp_lesson(0), 1)
        self.assertEqual(sci.clamp_lesson(36), 36)
        self.assertEqual(sci.clamp_lesson(99), 36)


class TestScienceWeekPointer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._db_fd, cls._db_path = tempfile.mkstemp(suffix=".db")
        os.close(cls._db_fd)
        cls._prev_path = db.DB_PATH
        db.DB_PATH = cls._db_path
        db.init_db()

    @classmethod
    def tearDownClass(cls):
        db.DB_PATH = cls._prev_path
        os.unlink(cls._db_path)

    def test_pointer_defaults_and_moves(self):
        self.assertEqual(db.get_arjun_science_lesson(7), 1)
        self.assertEqual(db.set_arjun_science_lesson(7, 12), 12)
        self.assertEqual(db.get_arjun_science_lesson(7), 12)
        self.assertEqual(db.set_arjun_science_lesson(7, 0), 1)
        self.assertEqual(db.set_arjun_science_lesson(7, 80), 36)
        self.assertEqual(db.get_arjun_science_lesson(7), 36)
