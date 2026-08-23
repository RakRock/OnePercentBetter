"""Tests for Harshit Physics practice focus save/restore."""

from __future__ import annotations

import os
import tempfile
import unittest

import database as db
from harshit.physics import content as hpc
from harshit.physics import topics as hpt


class TestHarshitPhysicsWeekConfig(unittest.TestCase):
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
            conn.execute("DELETE FROM harshit_physics_week_config")

    def _assert_roundtrip(self, unit_id: int, payload: dict) -> None:
        db.save_harshit_physics_week_config(
            unit_id,
            payload["week_label"],
            payload["topics"],
            practice_difficulty=payload.get("practice_difficulty", 3),
            use_chapter_llm=payload.get("use_chapter_llm", False),
            grok_fresh_only=payload.get("grok_fresh_only", False),
        )
        restored = db.get_harshit_physics_week_config(unit_id)
        self.assertEqual(restored["week_label"], payload["week_label"])
        self.assertEqual(restored["topics"], payload["topics"])
        self.assertEqual(restored["practice_difficulty"], payload.get("practice_difficulty", 3))
        self.assertEqual(restored["use_chapter_llm"], payload.get("use_chapter_llm", False))
        self.assertEqual(restored["grok_fresh_only"], payload.get("grok_fresh_only", False))
        self.assertEqual(restored["unit_id"], unit_id)

    def test_default_week_config_all_units(self):
        for unit_id in sorted(hpc.UNITS):
            catalog = hpt.topics_for_unit(unit_id)
            if not catalog:
                continue
            starter = hpt.default_week_config(unit_id)
            self.assertTrue(starter["topics"], f"Unit {unit_id} should seed topics")
            saved_ids = {int(item["id"]) for item in starter["topics"]}
            self.assertEqual(saved_ids, set(catalog.keys()))
            self._assert_roundtrip(unit_id, starter)

    def test_grok_flags_persist(self):
        payload = hpt.default_week_config(1)
        payload["use_chapter_llm"] = True
        payload["grok_fresh_only"] = True
        payload["week_label"] = "Grok-only review"
        self._assert_roundtrip(1, payload)

    def test_units_store_independently(self):
        if len(hpc.UNITS) < 2:
            self.skipTest("Need at least 2 physics units")
        u1 = hpt.default_week_config(1)
        u1["week_label"] = "Physics Unit 1"
        u2 = hpt.default_week_config(2)
        u2["week_label"] = "Physics Unit 2"
        self._assert_roundtrip(1, u1)
        self._assert_roundtrip(2, u2)
        self.assertEqual(db.get_harshit_physics_week_config(1)["week_label"], "Physics Unit 1")
        self.assertEqual(db.get_harshit_physics_week_config(2)["week_label"], "Physics Unit 2")


if __name__ == "__main__":
    unittest.main()
