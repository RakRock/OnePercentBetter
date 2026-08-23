"""Tests for PreReq weekly plan save/restore and preset coverage."""

from __future__ import annotations

import os
import tempfile
import unittest

import database as db
import harshit_prereq_coverage as hpc
import harshit_prereq_topics as hpt


class TestHarshitPrereqWeekConfig(unittest.TestCase):
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
            conn.execute("DELETE FROM harshit_prereq_week_config")

    def _assert_roundtrip(self, prereq_id: int, payload: dict) -> None:
        db.save_harshit_prereq_week_config(
            prereq_id,
            payload["week_label"],
            payload["topics"],
            warmup_count=payload.get("warmup_count", 0),
            use_llm=payload.get("use_llm", True),
            use_chapter_llm=payload.get("use_chapter_llm", True),
            grok_fresh_only=payload.get("grok_fresh_only", False),
        )
        restored = db.get_harshit_prereq_week_config(prereq_id)
        self.assertEqual(restored["week_label"], payload["week_label"])
        self.assertEqual(restored["topics"], payload["topics"])
        self.assertEqual(restored["warmup_count"], payload.get("warmup_count", 0))
        self.assertEqual(restored["use_llm"], payload.get("use_llm", True))
        self.assertEqual(restored["use_chapter_llm"], payload.get("use_chapter_llm", True))
        self.assertEqual(restored["grok_fresh_only"], payload.get("grok_fresh_only", False))
        self.assertEqual(restored["prereq_id"], prereq_id)

    def test_default_week_config_all_prereqs(self):
        for prereq_id in range(1, 7):
            starter = hpt.default_week_config(prereq_id)
            catalog = hpt.topics_for_prereq(prereq_id)
            self.assertTrue(starter["topics"], f"PreReq {prereq_id} should seed topics")
            saved_ids = {int(item["id"]) for item in starter["topics"]}
            self.assertEqual(saved_ids, set(catalog.keys()))
            self._assert_roundtrip(prereq_id, starter)

    def test_prereq2_all_week_presets(self):
        for key in hpc.PREREQ2_WEEK_PRESETS:
            applied = hpc.apply_preset(key)
            self._assert_roundtrip(hpc.PREREQ2_ID, applied)
            stats = hpc.coverage_stats(hpc.PREREQ2_ID, applied)
            preset = hpc.PREREQ2_WEEK_PRESETS[key]
            if key in ("polynomials_only", "linear_only"):
                expected_topics = len(preset["levels_by_topic"])
            else:
                expected_topics = hpc.PREREQ2_STRATEGY_COUNT
            self.assertEqual(len(applied["topics"]), expected_topics, key)
            self.assertGreater(stats["configured"], 0, key)

    def test_generic_week_presets_all_prereqs(self):
        for prereq_id in (1, 3, 4, 5, 6):
            catalog = hpt.topics_for_prereq(prereq_id)
            for key in hpc.GENERIC_WEEK_PRESETS:
                applied = hpc.apply_generic_preset(prereq_id, key)
                self._assert_roundtrip(prereq_id, applied)
                self.assertEqual(len(applied["topics"]), len(catalog), f"p{prereq_id} {key}")

    def test_grok_flags_persist(self):
        payload = hpt.default_week_config(2)
        payload["use_llm"] = False
        payload["use_chapter_llm"] = False
        payload["grok_fresh_only"] = True
        self._assert_roundtrip(2, payload)

    def test_migrate_legacy_prereq2_topic4_split(self):
        legacy = {
            "week_label": "Legacy plan",
            "topics": [
                {"id": 1, "levels": ["A"]},
                {"id": 4, "levels": ["A", "B", "C", "D", "E"]},
            ],
            "warmup_count": 0,
            "use_llm": True,
            "use_chapter_llm": True,
            "grok_fresh_only": False,
        }
        migrated = hpc.migrate_week_config(2, legacy)
        by_id = {int(item["id"]): item["levels"] for item in migrated["topics"]}
        self.assertEqual(by_id[4], ["A", "B"])
        self.assertEqual(by_id[5], ["C"])
        self.assertEqual(by_id[6], ["D"])
        self.assertEqual(by_id[7], ["E"])

    def test_merge_missing_topics_adds_new_catalog_entries(self):
        catalog = hpt.topics_for_prereq(3)
        partial = {
            "week_label": "Partial",
            "topics": [{"id": 1, "levels": ["A"]}],
        }
        merged = hpc.merge_missing_topics(3, partial)
        ids = {int(item["id"]) for item in merged["topics"]}
        self.assertEqual(ids, set(catalog.keys()))
        by_id = {int(item["id"]): item["levels"] for item in merged["topics"]}
        self.assertEqual(by_id[1], ["A"])
        self.assertEqual(by_id[2], ["A", "B"])


if __name__ == "__main__":
    unittest.main()
