"""Tests for Arjun Friday Concept Check I–V seeds."""

from __future__ import annotations

import unittest

import arjun_concept_check_form as ccform
import arjun_concept_check_form_llm as ccform_llm


class TestArjunConceptCheckForm(unittest.TestCase):
    def test_sections_are_i_through_vi(self):
        ids = [s["id"] for s in ccform.list_sections()]
        self.assertEqual(ids, ["I", "II", "III", "IV", "V", "VI", "VII"])

    def test_every_section_has_seeds(self):
        for sid in ("I", "II", "III", "IV", "V", "VI", "VII"):
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
            "cc_iii_cc6_1": "2.879458134, 1.345̅, 17/8, √64, and ∛64",
            "cc_iii_cc6_2": "11.8",
            "cc_iii_cc6_3": "7/90",
            "cc_iv_cc5_8": "1/8²",
            "cc_iv_cc5_9": "x³⁰ y⁸",
            "cc_iv_cc5_10": "x = 20",
            "cc_iv_cc6_5": "x³²",
            "cc_iv_cc6_5_slip": "x³²",
            "cc_iv_cc6_5b": "x¹⁹",
            "cc_iv_cc6_6": "b⁷⁰ / a²",
            "cc_iv_cc6_6b": "n¹² / m²",
            "cc_iv_cc6_4": "1",
            "cc_iv_cc6_7": "3¹⁰⁰",
            "cc_iv_cc6_8": "x = 5/3",
            "cc_iv_cc6_8_slip": "Set 12x = 20, so x = 5/3",
            "cc_iv_cc6_8b": "x = 3",
            "cc_v_cc6_9": "0.0000189",
            "cc_v_cc6_10": "No — rewrite as 9.24 × 10⁹",
            "cc_v_cc6_11": "1.07 × 10⁴³",
            "cc_v_cc6_12": "2.1 × 10¹⁰ burritos",
            "cc_v_later_4": "6 × 10⁷",
            "cc_v_later_5": "1.24 × 10¹⁹",
            "cc_v_later_6": "8.36 × 10⁴ seconds",
            "cc_v_est": "8.35 × 10¹²",
            "cc_v_add": "6.52 × 10¹⁵",
            "cc_v_div": "7.5 × 10²³",
            "cc_v_to_standard": "420,000",
            "cc_v_form_check": "3.5 × 10⁴",
            "cc_vi_vi1_expr": "2n − 1",
            "cc_vi_vi1_sub": "n = 3",
            "cc_vi_vi1_far": "199",
            "cc_vi_vi1_name": "a constant difference",
            "cc_vi_vi1_table": "11",
            "cc_vi_pracA_d": "2",
            "cc_vi_pracA_expr": "2n + 1",
            "cc_vi_pracA_51": "103",
            "cc_vi_pracB_expr": "2n + 1",
            "cc_vi_pracB_100": "201",
            "cc_vi2_sq_next": "16, 25, 36",
            "cc_vi2_sq_nth": "n²",
            "cc_vi2_sq_40": "1600",
            "cc_vi2_rect_nth": "n(n + 1)",
            "cc_vi2_rect_99": "9900",
            "cc_vi2_tri_nth": "n(n + 1) / 2",
            "cc_vi2_classify_72": "Rectangular only (8 × 9)",
            "cc_vi2_pent_10": "32 cm",
            "cc_vi2_pent_50": "152 cm",
            "cc_vi2_oct_40": "242 m",
            "cc_vi3_bag_count": "2",
            "cc_vi3_bag_eq": "2x + 3 = 7",
            "cc_vi3_three_bags": "4",
            "cc_vi3_eq3": "3x = 12",
            "cc_vi3_two_bags_four": "3",
            "cc_vi3_eq4": "2x + 4 = 10",
            "cc_vi3_solve_check": "x = 3",
            "cc_vii1_scale_eq": "5x + 2 = 3x + 4",
            "cc_vii1_scale_x": "1",
            "cc_vii1_ex1": "x = −2",
            "cc_vii1_combine": "x = −5",
            "cc_vii1_dist": "x = 2",
            "cc_vii1_neg_dist": "x = 7",
            "cc_vii1_both_dist": "x = −2",
            "cc_vii1_frac": "x = −3",
            "cc_vii1_half": "x = 1/2",
            "cc_vii1_zero": "x = 0",
            "cc_vii1_mixed": "x = 18/5",
            "cc_vii2_scale_inf": "Infinite solutions — leftover cubes match, so every bag size works",
            "cc_vii2_scale_none": "No solution — 5 cubes do not equal 2 cubes",
            "cc_vii2_n1": "Infinite solutions (−2 = −2)",
            "cc_vii2_n2": "No solution (−4 = −3)",
            "cc_vii2_n4": "One solution: x = 0",
            "cc_vii2_yt1": "No solution (6 = 0)",
            "cc_vii2_yt2": "Infinite solutions (−2 = −2)",
            "cc_vii2_yt5": "x = −1/2",
            "cc_vii2_yt7": "One solution: x = 0",
            "cc_vii2_yt10": "No solution (5 = 4)",
            "cc_vii2_fill_inf": "12",
            "cc_vii2_fill_none": "−7",
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

    def test_unit6_is_one_mixed_section(self):
        info = ccform.get_section("VI")
        self.assertEqual(info["unit_id"], 6)
        self.assertEqual(info["title"], "Unit 6 — Patterns and Modeling")
        self.assertEqual(ccform.get_section("VI-2")["id"], "VI")
        self.assertEqual(ccform.get_section("VI-3")["id"], "VI")
        notes = ccform_llm._notes_for_section("VI")
        self.assertIn("constant difference", notes.lower())
        self.assertIn("2n", notes)
        self.assertIn("n²", notes)
        self.assertIn("3n + 2", notes)
        self.assertIn("2x + 3 = 7", notes)
        seeds = ccform.seeds_for_section("VI")
        papers = {q["paper"] for q in seeds}
        self.assertTrue({"VI-1", "VI-2", "VI-3"} <= papers)
        self.assertTrue(all(q["section"] == "VI" for q in seeds))
        questions = ccform_llm.fallback_seed_set("VI")
        self.assertEqual(len(questions), 5)
        import arjun_course3_content as c3
        unit = c3.get_unit(6)
        slugs = [a["slug"] for a in unit["activities"]]
        self.assertEqual(
            slugs,
            [
                "activity_1_representing_patterns",
                "activity_2_using_patterns_expressions",
                "activity_3_solving_equations_with_models",
            ],
        )

    def test_unit7_is_one_mixed_section(self):
        info = ccform.get_section("VII")
        self.assertEqual(info["unit_id"], 7)
        self.assertEqual(info["title"], "Unit 7 — Solving Linear Equations")
        self.assertEqual(ccform.get_section("VII-1")["id"], "VII")
        self.assertEqual(ccform.get_section("VII-2")["id"], "VII")
        notes = ccform_llm._notes_for_section("VII")
        self.assertIn("variables on both sides", notes.lower())
        self.assertIn("x = −5", notes)
        self.assertIn("x = 18/5", notes)
        self.assertIn("infinite", notes.lower())
        self.assertIn("no solution", notes.lower())
        self.assertIn("x = −1/2", notes)
        seeds = ccform.seeds_for_section("VII")
        papers = {q["paper"] for q in seeds}
        self.assertTrue({"VII-1", "VII-2"} <= papers)
        self.assertTrue(all(q["section"] == "VII" for q in seeds))
        questions = ccform_llm.fallback_seed_set("VII")
        self.assertEqual(len(questions), 5)
        import arjun_course3_content as c3
        unit = c3.get_unit(7)
        slugs = [a["slug"] for a in unit["activities"]]
        self.assertEqual(
            slugs,
            [
                "activity_1_multistep_equations",
                "activity_2_infinite_no_solutions",
            ],
        )

    def test_cc6_papers_and_iv_misses(self):
        self.assertEqual(ccform.session_count_for_section("IV"), 5)
        papers_iii = {q["paper"] for q in ccform.seeds_for_section("III")}
        papers_iv = {q["paper"] for q in ccform.seeds_for_section("IV")}
        papers_v = {q["paper"] for q in ccform.seeds_for_section("V")}
        self.assertIn("CC6", papers_iii)
        self.assertIn("CC6", papers_iv)
        self.assertIn("CC6", papers_v)
        iv_stems = {q["stem"] for q in ccform.seeds_for_section("IV")}
        self.assertTrue(
            {"power_of_power_product", "power_of_power_slip", "power_equation_slip"}
            <= iv_stems
        )
        notes = ccform_llm._notes_for_section("IV")
        self.assertIn("x³²", notes)
        self.assertIn("5/3", notes)
        questions = ccform_llm.fallback_seed_set("IV")
        self.assertEqual(len(questions), 5)
        self.assertTrue(all(q["section"] == "IV" for q in questions))

    def test_unit5_session_is_five_questions(self):
        self.assertEqual(ccform.session_count_for_section("V"), 5)
        self.assertGreaterEqual(len(ccform.seeds_for_section("V")), 5)
        questions = ccform_llm.fallback_seed_set("V")
        self.assertEqual(len(questions), 5)
        self.assertTrue(all(q["section"] == "V" for q in questions))

    def test_short_set_is_topped_up_to_session_count(self):
        seed = dict(ccform.seeds_for_section("V")[0])
        filled = ccform_llm._top_up_from_seeds("V", [seed], 5)
        self.assertEqual(len(filled), 5)

    def test_session_report_includes_score(self):
        questions = ccform.seeds_for_section("V")[:3]
        answers = [
            {"correct": True, "picked": questions[0]["options"][0], "correct_val": questions[0]["options"][0]},
            {"correct": False, "picked": questions[1]["options"][1], "correct_val": questions[1]["options"][0]},
            {"correct": True, "picked": questions[2]["options"][0], "correct_val": questions[2]["options"][0]},
        ]
        report = ccform.build_session_report(questions, answers)
        self.assertEqual(report["correct_count"], 2)
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["score_pct"], 66)


if __name__ == "__main__":
    unittest.main()
