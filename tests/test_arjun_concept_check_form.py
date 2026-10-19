"""Tests for Arjun Friday Concept Check I–V seeds."""

from __future__ import annotations

import unittest

import arjun_concept_check_form as ccform
import arjun_concept_check_form_llm as ccform_llm


class TestArjunConceptCheckForm(unittest.TestCase):
    def test_sections_are_i_through_v(self):
        ids = [s["id"] for s in ccform.list_sections()]
        self.assertEqual(ids, ["I", "II", "III", "IV", "V"])

    def test_every_section_has_seeds(self):
        for sid in ("I", "II", "III", "IV", "V"):
            seeds = ccform.seeds_for_section(sid)
            self.assertTrue(seeds, sid)
            self.assertEqual(len({q["id"] for q in seeds}), len(seeds), sid)

    def test_seed_mcqs_are_well_formed(self):
        for q in ccform.FORM_SEED_QUESTIONS:
            self.assertEqual(len(q["options"]), 4, q["id"])
            self.assertIn(q["answer"], range(4), q["id"])
            self.assertTrue(q["explanation"], q["id"])

    def test_cc1_cc5_keyed_answers(self):
        by_id = {q["id"]: q for q in ccform.FORM_SEED_QUESTIONS}
        keyed = {
            "cc_i_cc1_1": "4 7/12",
            "cc_i_cc1_2": "18",
            "cc_i_cc1_3": "108, 12, 4",
            "cc_i_cc1_5": "9",
            "cc_i_cc2_1": "1 1/12 lb",
            "cc_i_cc2_2": "1/24",
            "cc_i_cc2_3": "3 1/9",
            "cc_i_cc4_1": "4 1/24",
            "cc_i_cc4_2": "76/101",
            "cc_i_cc4_3": "7/18",
            "cc_ii_cc2_6": "7 ft",
            "cc_ii_cc2_8": "40",
            "cc_ii_cc4_5": "x = 9",
            "cc_ii_cc4_7": "2 in",
            "cc_ii_cc4_8": "−31",
            "cc_ii_cc5_1": "36 cm²",
            "cc_ii_cc5_2": "2 ft",
            "cc_ii_cc5_3": "−59",
            "cc_ii_cc5_4": "−2",
            "cc_iii_cc4_9": "√65",
            "cc_iii_cc4_12": "3.2",
            "cc_iii_cc4_13": "11/45",
            "cc_iii_cc5_6": "8.4",
            "cc_iii_cc5_7": "2/165",
            "cc_iv_cc5_8": "1/8²",
            "cc_iv_cc5_9": "x³⁰ y⁸",
            "cc_iv_cc5_10": "x = 20",
            "cc_v_later_4": "6 × 10⁷",
            "cc_v_later_5": "1.24 × 10¹⁹",
            "cc_v_later_6": "8.36 × 10⁴ seconds",
        }
        for qid, expected in keyed.items():
            q = by_id[qid]
            self.assertEqual(q["options"][q["answer"]], expected, qid)

    def test_section_iii_only_returns_iii_seeds(self):
        seeds = ccform.seeds_for_section("III")
        self.assertTrue(all(q["section"] == "III" for q in seeds))
        self.assertGreaterEqual(len(seeds), 5)

    def test_fallback_set_stays_in_section(self):
        questions = ccform_llm.fallback_seed_set("II")
        self.assertEqual(len(questions), ccform.session_count_for_section("II"))
        self.assertTrue(all(q["section"] == "II" for q in questions))
        for q in questions:
            self.assertEqual(len(q["options"]), 4)

    def test_i_and_ii_papers_are_present(self):
        papers_i = {q["paper"] for q in ccform.seeds_for_section("I")}
        papers_ii = {q["paper"] for q in ccform.seeds_for_section("II")}
        self.assertTrue({"CC1", "CC2", "CC4"} <= papers_i)
        self.assertTrue({"CC2", "CC4", "CC5"} <= papers_ii)


if __name__ == "__main__":
    unittest.main()
