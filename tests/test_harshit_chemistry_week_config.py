"""Tests for Harshit Chemistry practice focus save/restore."""

from __future__ import annotations

import os
import tempfile
import unittest

import database as db
import harshit.chemistry.content as hcc
import harshit.chemistry.topics as hct


class TestHarshitChemistryWeekConfig(unittest.TestCase):
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
            conn.execute("DELETE FROM harshit_chemistry_week_config")

    def test_default_week_config_unit1(self):
        starter = hct.default_week_config(1)
        self.assertEqual(len(starter["topics"]), 16)
        db.save_harshit_chemistry_week_config(
            1,
            starter["week_label"],
            starter["topics"],
            use_chapter_llm=False,
        )
        restored = db.get_harshit_chemistry_week_config(1)
        self.assertEqual(restored["week_label"], starter["week_label"])
        self.assertEqual(restored["topics"], starter["topics"])

    def test_unit2_content_loaded(self):
        self.assertEqual(hcc.unit_meta(2)["title"], "Acids, Bases and Salts")
        self.assertEqual(hcc.total_concept_cards(active_only=True, unit_id=2), 160)

    def test_default_week_config_unit2(self):
        starter = hct.default_week_config(2)
        self.assertEqual(len(starter["topics"]), 16)
        db.save_harshit_chemistry_week_config(
            2,
            starter["week_label"],
            starter["topics"],
            use_chapter_llm=False,
        )
        restored = db.get_harshit_chemistry_week_config(2)
        self.assertEqual(restored["week_label"], starter["week_label"])

    def test_unit3_content_loaded(self):
        self.assertEqual(hcc.unit_meta(3)["title"], "Metals and Non-metals")
        self.assertEqual(hcc.total_concept_cards(active_only=True, unit_id=3), 160)

    def test_default_week_config_unit3(self):
        starter = hct.default_week_config(3)
        self.assertEqual(len(starter["topics"]), 16)
        db.save_harshit_chemistry_week_config(
            3,
            starter["week_label"],
            starter["topics"],
            use_chapter_llm=False,
        )
        restored = db.get_harshit_chemistry_week_config(3)
        self.assertEqual(restored["week_label"], starter["week_label"])

    def test_unit4_content_loaded(self):
        self.assertEqual(hcc.unit_meta(4)["title"], "Carbon and its Compounds")
        self.assertEqual(hcc.total_concept_cards(active_only=True, unit_id=4), 160)

    def test_default_week_config_unit4(self):
        starter = hct.default_week_config(4)
        self.assertEqual(len(starter["topics"]), 16)
        db.save_harshit_chemistry_week_config(
            4,
            starter["week_label"],
            starter["topics"],
            use_chapter_llm=False,
        )
        restored = db.get_harshit_chemistry_week_config(4)
        self.assertEqual(restored["week_label"], starter["week_label"])


if __name__ == "__main__":
    unittest.main()
