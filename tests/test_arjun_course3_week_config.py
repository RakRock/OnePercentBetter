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
            if unit_id == 1:
                self.assertIn("exponents", topic_ids)
                self.assertNotIn("scientific_notation", topic_ids)
                self.assertIn("School packet", config["week_label"])
            else:
                self.assertEqual(topic_ids, set(cats.keys()))
            for topic in config["topics"]:
                self.assertTrue(topic["levels"])

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
        """A 15-question session is still built when the week plan is narrower than the full unit."""
        cfg = c3w.default_week_config(1)
        cfg["topics"] = [
            {"id": "patterns", "levels": ["C"]},
            {"id": "fractions", "levels": ["C"]},
            {"id": "powers_roots", "levels": ["C"]},
            {"id": "rational_numbers", "levels": ["C"]},
        ]
        cfg["question_count"] = 8
        self.assertGreaterEqual(c3p.question_count_for_unit(1, config=cfg), 8)
        questions, err = c3p.build_session_set(1, cfg)
        self.assertIsNone(err)
        self.assertEqual(len(questions), 15)

    def test_unit1_school_packet_week_config(self):
        cfg = c3w.school_packet_week_config(1)
        self.assertIsNotNone(cfg)
        topic_ids = [t["id"] for t in cfg["topics"]]
        self.assertIn("exponents", topic_ids)
        self.assertNotIn("scientific_notation", topic_ids)
        self.assertIsNone(c3w.school_packet_week_config(2))
        questions, err = c3p.build_session_set(1, cfg)
        self.assertIsNone(err)
        self.assertEqual(len(questions), 15)
        self.assertTrue(all(q["category"] in topic_ids for q in questions))

    def test_unit1_default_daily_practice_mixes_school_packet(self):
        cfg = c3w.default_week_config(1)
        questions, err = c3p.build_session_set(1, cfg)
        self.assertIsNone(err)
        self.assertEqual(len(questions), 15)
        schoolish = sum(1 for q in questions if c3p.is_school_like(q))
        packet = sum(1 for q in questions if q.get("source") == "school_packet_9_22")
        self.assertGreaterEqual(schoolish, 13)
        self.assertGreaterEqual(packet, 13)

    def test_unit1_week_template_defaults_to_13_of_15_school_packet(self):
        cfg = c3w.default_week_config(1)
        self.assertEqual(cfg["question_count"], 15)
        self.assertEqual(cfg["school_packet_count"], 13)
        school = c3w.school_packet_week_config(1)
        self.assertEqual(school["school_packet_count"], 13)
        generic = {
            "week_label": "Numerical Relationships — Week 1",
            "topics": [{"id": "exponents", "levels": ["B", "C", "D"]}],
            "question_count": 15,
        }
        self.assertEqual(c3p.resolved_school_packet_count(generic, count=15, unit_id=1), 13)
        self.assertIn("School packet: 13 of 15", c3w.format_week_plan_summary(1, cfg))

    def test_unit1_seed_questions_prefer_school_packet(self):
        seeds = c3p.seed_questions_for_category(1, "fractions", limit=4)
        self.assertTrue(seeds)
        self.assertGreaterEqual(
            sum(1 for q in seeds if q.get("source") == "school_packet_9_22"),
            1,
        )

    def test_unit1_school_packet_session_uses_school_stems(self):
        cfg = c3w.school_packet_week_config(1)
        questions, err = c3p.build_session_set(1, cfg)
        self.assertIsNone(err)
        self.assertEqual(len(questions), 15)
        schoolish = sum(1 for q in questions if c3p.is_school_like(q))
        packet = sum(1 for q in questions if q.get("source") == "school_packet_9_22")
        self.assertGreaterEqual(schoolish, 13)
        self.assertGreaterEqual(packet, 13)

    def test_unit1_school_packet_questions_are_valid_mcqs(self):
        from arjun_course3_unit1_school_packet import SCHOOL_PACKET_UNIT1_QUESTIONS

        ids = [q["id"] for q in SCHOOL_PACKET_UNIT1_QUESTIONS]
        self.assertEqual(len(ids), len(set(ids)))
        for q in SCHOOL_PACKET_UNIT1_QUESTIONS:
            self.assertEqual(len(q["options"]), 4, q["id"])
            self.assertIn(q["answer"], range(4), q["id"])
            self.assertTrue(q["explanation"], q["id"])

    def test_unit1_exponent_properties_iv_packet_in_bank(self):
        from arjun_course3_unit1_school_packet import SCHOOL_PACKET_UNIT1_QUESTIONS

        by_id = {q["id"]: q for q in SCHOOL_PACKET_UNIT1_QUESTIONS}
        sheets = {q.get("school_sheet") for q in SCHOOL_PACKET_UNIT1_QUESTIONS}
        self.assertTrue({"IV-1", "IV-2", "IV-3", "IV-R"} <= sheets)
        self.assertGreaterEqual(
            sum(1 for q in SCHOOL_PACKET_UNIT1_QUESTIONS if q.get("school_sheet") in {"IV-2", "IV-3", "IV-R"}),
            20,
        )
        keyed = {
            "u1_sch_iv1_recap": "4 · 5 · 4×4×4×4×4 · 4⁵ · 1024",
            "u1_sch_iv1_a1": "5⁶",
            "u1_sch_iv1_d": "3¹²",
            "u1_sch_iv1_f": "5²",
            "u1_sch_iv2_b": "1",
            "u1_sch_iv2_d": "1/4⁵",
            "u1_sch_iv2_j": "7⁶",
            "u1_sch_iv2_m": "1",
            "u1_sch_iv3_b": "6² x²",
            "u1_sch_iv3_c": "5⁸ x¹² y¹⁶",
            "u1_sch_iv3_i": "x³⁰ y²⁰ / z⁴⁰",
            "u1_sch_ivr_8": "x⁸",
            "u1_sch_ivr_12": "−x¹⁵",
        }
        for qid, expected in keyed.items():
            q = by_id[qid]
            self.assertEqual(q["options"][q["answer"]], expected, qid)

    def test_unit1_school_packet_week_includes_exponent_stretch(self):
        cfg = c3w.school_packet_week_config(1)
        exp = next(t for t in cfg["topics"] if t["id"] == "exponents")
        self.assertIn("D", exp["levels"])

    def test_should_refresh_generic_or_stale_unit1_plan(self):
        school = c3w.school_packet_week_config(1)
        self.assertFalse(c3w.should_refresh_unit1_school_plan(school))
        self.assertTrue(c3w.should_refresh_unit1_school_plan({}))
        self.assertTrue(
            c3w.should_refresh_unit1_school_plan(
                {
                    "week_label": "Numerical Relationships — Week 1",
                    "topics": [{"id": "patterns", "levels": ["B", "C"]}],
                }
            )
        )
        self.assertTrue(
            c3w.should_refresh_unit1_school_plan(
                {
                    "week_label": "School packet through 9/22 — Numerical Relationships",
                    "topics": [{"id": "exponents", "levels": ["B", "C"]}],
                }
            )
        )
        self.assertFalse(
            c3w.should_refresh_unit1_school_plan(
                {
                    "week_label": "Fractions only this week",
                    "topics": [{"id": "fractions", "levels": ["B", "C"]}],
                }
            )
        )

    def test_ensure_week_config_loads_school_packet_by_default(self):
        import arjun_course3_week_ui as c3wui

        db.save_arjun_course3_week_config(
            1,
            "Numerical Relationships — Week 1",
            [
                {"id": "patterns", "levels": ["B", "C"]},
                {"id": "scientific_notation", "levels": ["B"]},
            ],
        )
        cfg = c3wui.ensure_week_config("course3", 1)
        self.assertIn("School packet", cfg["week_label"])
        ids = {t["id"] for t in cfg["topics"]}
        self.assertIn("exponents", ids)
        self.assertNotIn("scientific_notation", ids)
        self.assertEqual(cfg.get("school_packet_count"), 13)
        saved = db.get_arjun_course3_week_config(1)
        self.assertEqual(saved.get("school_packet_count"), 13)

    def test_unit1_week_config_save_defaults_school_packet_count(self):
        topics = [{"id": "fractions", "levels": ["B", "C"]}]
        db.save_arjun_course3_week_config(1, "Fractions only this week", topics)
        loaded = db.get_arjun_course3_week_config(1)
        self.assertEqual(loaded["school_packet_count"], 13)

    def test_unit1_rational_irrational_iii_packet_in_bank(self):
        from arjun_course3_unit1_school_packet import SCHOOL_PACKET_UNIT1_QUESTIONS

        by_id = {q["id"]: q for q in SCHOOL_PACKET_UNIT1_QUESTIONS}
        sheets = {q.get("school_sheet") for q in SCHOOL_PACKET_UNIT1_QUESTIONS}
        self.assertTrue({"III-1", "III-2", "III-3", "III-4", "III-R"} <= sheets)
        keyed = {
            "u1_sch_iii1_2": "0.94 and 47/50",
            "u1_sch_iii1_3": "80% and 0.8",
            "u1_sch_iii1_4": "2/3 > 16/27",
            "u1_sch_iii1_5": "330% and 33/10",
            "u1_sch_iii2_a": "23/45",
            "u1_sch_iii2_c": "236/999",
            "u1_sch_iii2_d": "0.055555…",
            "u1_sch_iii3_b": "6.5",
            "u1_sch_iii3_c": "9.9",
            "u1_sch_iii3_d": "2.7",
            "u1_sch_iii3_e": "√8",
            "u1_sch_iii4_d": "8.1, √71, √84, 9.3",
            "u1_sch_iii4_g": "7 < √50",
            "u1_sch_iiir_1": "√12, π, √65",
            "u1_sch_iiir_5": "4.9",
            "u1_sch_iiir_11": "2.65, ∛19, π, 4",
        }
        for qid, expected in keyed.items():
            q = by_id[qid]
            self.assertEqual(q["options"][q["answer"]], expected, qid)

    def test_unit1_first_quarter_review_in_bank(self):
        from arjun_course3_unit1_school_packet import SCHOOL_PACKET_UNIT1_QUESTIONS

        by_id = {q["id"]: q for q in SCHOOL_PACKET_UNIT1_QUESTIONS}
        sheets = {q.get("school_sheet") for q in SCHOOL_PACKET_UNIT1_QUESTIONS}
        self.assertTrue({"Q1-PR", "Q1-RI", "IV-R"} <= sheets)
        keyed = {
            "u1_sch_q1pr_1": "0.64",
            "u1_sch_q1pr_2": "343",
            "u1_sch_q1pr_4": "4",
            "u1_sch_q1pr_5": "x = 14 or x = −14",
            "u1_sch_q1pr_9": "Area 64, perimeter 32, volume 512",
            "u1_sch_q1pr_11": "25 in²",
            "u1_sch_q1pr_12": "4/3 cm",
            "u1_sch_q1ri_1": "46% and 23/50",
            "u1_sch_q1ri_3": "0.57 and 57%",
            "u1_sch_q1ri_4": "37/99",
            "u1_sch_q1ri_5": "17/333",
            "u1_sch_q1ri_6": "5.5",
            "u1_sch_q1ri_8": "11.0",
            "u1_sch_q1ri_10": "3.8",
            "u1_sch_q1ri_11": "√5, 2.3, √7",
            "u1_sch_ivr_5": "4/9 y¹⁰",
            "u1_sch_ivr_5b": "x⁵",
        }
        for qid, expected in keyed.items():
            q = by_id[qid]
            self.assertEqual(q["options"][q["answer"]], expected, qid)

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
