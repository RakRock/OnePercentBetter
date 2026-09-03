"""Tests for Arjun Course 3 weekly plan configuration."""

from __future__ import annotations

import os
import tempfile
import unittest

import arjun_course3_levels as c3lvl
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

    def test_course3_default_week_config_has_topics_and_levels(self):
        for unit_id in range(1, 6):
            config = c3w.default_week_config(unit_id)
            cats = c3p.get_categories(unit_id)
            self.assertTrue(config["topics"], f"unit {unit_id} should have topics")
            topic_ids = {t["id"] for t in config["topics"]}
            self.assertEqual(topic_ids, set(cats.keys()))
            for topic in config["topics"]:
                self.assertEqual(topic["levels"], c3lvl.DEFAULT_LEVELS)

    def test_edgenuity_default_week_config_has_topics_and_levels(self):
        for unit_id in range(1, 7):
            config = ec3w.default_week_config(unit_id)
            cats = ec3p.get_categories(unit_id)
            self.assertTrue(config["topics"], f"unit {unit_id} should have topics")
            topic_ids = {t["id"] for t in config["topics"]}
            self.assertEqual(topic_ids, set(cats.keys()))

    def test_legacy_categories_migrate_to_topics(self):
        legacy = {
            "week_label": "Legacy",
            "categories": ["patterns", "fractions"],
            "question_count": 12,
        }
        valid = set(c3p.get_categories(1).keys())
        normalized = c3lvl.normalize_week_config(legacy, valid)
        self.assertEqual(len(normalized["topics"]), 2)
        self.assertEqual(normalized["topics"][0]["levels"], c3lvl.DEFAULT_LEVELS)

    def test_course3_build_session_set_respects_topic_levels(self):
        unit_id = 2
        full = c3w.default_week_config(unit_id)
        questions, err = c3p.build_session_set(unit_id, full)
        self.assertTrue(questions)
        self.assertIsNone(err)

        narrow = dict(full)
        narrow["topics"] = [{"id": "slope", "levels": ["B"]}]
        slope_only, _ = c3p.build_session_set(unit_id, narrow)
        self.assertTrue(slope_only)
        self.assertTrue(all(q["category"] == "slope" for q in slope_only))
        level_map = c3lvl.bank_level_map(c3p.QUESTION_BANK_BY_UNIT[unit_id])

        def _resolved_level(q: dict) -> str:
            tagged = q.get("level")
            if tagged in c3lvl.LEVEL_ORDER:
                return str(tagged)
            return level_map.get(q["id"], "B")

        self.assertTrue(all(_resolved_level(q) == "B" for q in slope_only))

    def test_unit1_session_keeps_15_when_static_bank_is_small(self):
        """Week 1 topics at level C only match 8 bank items — still build 15."""
        cfg = c3w.default_week_config(1)
        cfg["topics"] = [
            {"id": "patterns", "levels": ["C"]},
            {"id": "fractions", "levels": ["C"]},
            {"id": "powers_roots", "levels": ["C"]},
            {"id": "rational_numbers", "levels": ["C"]},
        ]
        cfg["question_count"] = 8
        self.assertEqual(c3p.question_count_for_unit(1, config=cfg), 8)
        questions, err = c3p.build_session_set(1, cfg)
        self.assertIsNone(err)
        self.assertEqual(len(questions), 15)

    def test_course3_week_config_persistence(self):
        starter = c3w.default_week_config(1)
        topics = starter["topics"][:2]
        topics[0] = {"id": topics[0]["id"], "levels": ["A", "C"]}
        db.save_arjun_course3_week_config(
            1,
            starter["week_label"],
            topics,
            question_count=10,
            use_llm=True,
        )
        loaded = db.get_arjun_course3_week_config(1)
        self.assertEqual(loaded["week_label"], starter["week_label"])
        self.assertEqual(len(loaded["topics"]), 2)
        self.assertEqual(loaded["topics"][0]["levels"], ["A", "C"])
        self.assertEqual(loaded["question_count"], 10)
        self.assertTrue(loaded["use_llm"])

    def test_edgenuity_week_config_persistence(self):
        starter = ec3w.default_week_config(2)
        topics = starter["topics"][:3]
        db.save_arjun_edgenuity_course3_week_config(
            2,
            "Unit 2 review week",
            topics,
            question_count=12,
            use_llm=False,
        )
        loaded = db.get_arjun_edgenuity_course3_week_config(2)
        self.assertEqual(loaded["week_label"], "Unit 2 review week")
        self.assertEqual(len(loaded["topics"]), 3)
        self.assertEqual(loaded["question_count"], 12)


if __name__ == "__main__":
    unittest.main()
