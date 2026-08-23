"""Tests for Class 10 weekly plan save/restore."""

from __future__ import annotations

import os
import tempfile
import unittest

import database as db
import harshit_class10_topics as h10t
import harshit_class10_units as h10u


class TestHarshitClass10WeekConfig(unittest.TestCase):
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
            conn.execute("DELETE FROM harshit_class10_week_config")

    def _assert_roundtrip(self, unit_id: int, payload: dict) -> None:
        db.save_harshit_class10_week_config(
            unit_id,
            payload["week_label"],
            payload["topics"],
            practice_difficulty=payload.get("practice_difficulty", 3),
            use_chapter_llm=payload.get("use_chapter_llm", True),
            grok_fresh_only=payload.get("grok_fresh_only", False),
        )
        restored = db.get_harshit_class10_week_config(unit_id)
        self.assertEqual(restored["week_label"], payload["week_label"])
        self.assertEqual(restored["topics"], payload["topics"])
        self.assertEqual(restored["practice_difficulty"], payload.get("practice_difficulty", 3))
        self.assertEqual(restored["use_chapter_llm"], payload.get("use_chapter_llm", True))
        self.assertEqual(restored["grok_fresh_only"], payload.get("grok_fresh_only", False))
        self.assertEqual(restored["unit_id"], unit_id)

    def test_default_week_config_active_units(self):
        active = [u["id"] for u in h10u.list_units() if u.get("active")]
        self.assertGreaterEqual(len(active), 4)
        for unit_id in active:
            catalog = h10t.topics_for_unit(unit_id)
            if not catalog:
                continue
            starter = h10t.default_week_config(unit_id)
            self.assertTrue(starter["topics"], f"Unit {unit_id} should seed topics")
            saved_ids = {int(item["id"]) for item in starter["topics"]}
            self.assertEqual(saved_ids, set(catalog.keys()))
            self._assert_roundtrip(unit_id, starter)

    def test_custom_levels_and_grok_flags(self):
        payload = h10t.default_week_config(1)
        payload["topics"] = [{"id": 1, "levels": ["A", "E"]}, {"id": 2, "levels": ["C"]}]
        payload["week_label"] = "Custom Week 2"
        payload["practice_difficulty"] = 5
        payload["use_chapter_llm"] = False
        payload["grok_fresh_only"] = True
        self._assert_roundtrip(1, payload)

    def test_each_active_unit_independent(self):
        u1 = h10t.default_week_config(1)
        u1["week_label"] = "Unit 1 plan"
        u2 = h10t.default_week_config(2)
        u2["week_label"] = "Unit 2 plan"
        self._assert_roundtrip(1, u1)
        self._assert_roundtrip(2, u2)
        self.assertEqual(db.get_harshit_class10_week_config(1)["week_label"], "Unit 1 plan")
        self.assertEqual(db.get_harshit_class10_week_config(2)["week_label"], "Unit 2 plan")


if __name__ == "__main__":
    unittest.main()
