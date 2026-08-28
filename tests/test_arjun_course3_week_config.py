"""Tests for Arjun Course 3 weekly plan configuration."""

from __future__ import annotations

import os
import tempfile
import unittest

import arjun_course3_practice as c3p
import arjun_course3_week as c3w
import arjun_edgenuity_course3_practice as ec3p
import arjun_edgenuity_course3_week as ec3w
import database as db


class TestArjunCourse3WeekConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._db_fd, cls._db_path = tempfile.mkstemp(suffix=".db")
        os.close(cls._db_fd)
        cls._prev_db = os.environ.get("ONEPERCENT_DB")
        os.environ["ONEPERCENT_DB"] = cls._db_path
        db.init_db()

    @classmethod
    def tearDownClass(cls):
        if cls._prev_db is None:
            os.environ.pop("ONEPERCENT_DB", None)
        else:
            os.environ["ONEPERCENT_DB"] = cls._prev_db
        os.unlink(cls._db_path)

    def setUp(self):
        with db.get_connection() as conn:
            conn.execute("DELETE FROM arjun_course3_week_config")
            conn.execute("DELETE FROM arjun_edgenuity_course3_week_config")

    def test_course3_default_week_config_covers_all_categories(self):
        for unit_id in range(1, 6):
            config = c3w.default_week_config(unit_id)
            cats = c3p.get_categories(unit_id)
            self.assertTrue(config["categories"], f"unit {unit_id} should have categories")
            self.assertEqual(set(config["categories"]), set(cats.keys()))
            self.assertEqual(config["question_count"], c3p.DEFAULT_SESSION_COUNT)

    def test_edgenuity_default_week_config_covers_all_categories(self):
        for unit_id in range(1, 7):
            config = ec3w.default_week_config(unit_id)
            cats = ec3p.get_categories(unit_id)
            self.assertTrue(config["categories"], f"unit {unit_id} should have categories")
            self.assertEqual(set(config["categories"]), set(cats.keys()))

    def test_course3_build_session_set_respects_category_filter(self):
        unit_id = 2
        full = c3w.default_week_config(unit_id)
        questions, err = c3p.build_session_set(unit_id, full)
        self.assertTrue(questions)
        self.assertIsNone(err)
        self.assertLessEqual(len(questions), full["question_count"])

        narrow = dict(full)
        narrow["categories"] = ["slope"]
        slope_only, _ = c3p.build_session_set(unit_id, narrow)
        self.assertTrue(slope_only)
        self.assertTrue(all(q["category"] == "slope" for q in slope_only))

    def test_course3_week_config_persistence(self):
        starter = c3w.default_week_config(1)
        db.save_arjun_course3_week_config(
            1,
            starter["week_label"],
            starter["categories"][:4],
            question_count=10,
            use_llm=True,
        )
        loaded = db.get_arjun_course3_week_config(1)
        self.assertEqual(loaded["week_label"], starter["week_label"])
        self.assertEqual(len(loaded["categories"]), 4)
        self.assertEqual(loaded["question_count"], 10)
        self.assertTrue(loaded["use_llm"])

    def test_edgenuity_week_config_persistence(self):
        starter = ec3w.default_week_config(2)
        db.save_arjun_edgenuity_course3_week_config(
            2,
            "Unit 2 review week",
            starter["categories"][:3],
            question_count=12,
            use_llm=False,
        )
        loaded = db.get_arjun_edgenuity_course3_week_config(2)
        self.assertEqual(loaded["week_label"], "Unit 2 review week")
        self.assertEqual(len(loaded["categories"]), 3)
        self.assertEqual(loaded["question_count"], 12)


if __name__ == "__main__":
    unittest.main()
