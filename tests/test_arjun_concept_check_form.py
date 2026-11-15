"""Tests for Arjun Friday Concept Check I–V seeds."""

from __future__ import annotations

import unittest

import arjun_concept_check_form as ccform
import arjun_concept_check_form_llm as ccform_llm


class TestArjunConceptCheckForm(unittest.TestCase):
    def test_sections_are_i_through_vi(self):
        ids = [s["id"] for s in ccform.list_sections()]
        self.assertEqual(ids, ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"])

    def test_section_cards_are_numbered_1_through_7(self):
        titles = [ccform.section_card_title(s["id"]) for s in ccform.list_sections()]
        self.assertEqual(
            titles,
            [
                "1) Numerical Relationships",
                "2) Powers and Roots",
                "3) Rational and Irrational Numbers",
                "4) Exponent Properties",
                "5) Scientific Notation",
                "6) Patterns and Modeling",
                "7) Solving Linear Equations",
                "8) Slope and Linear Equations",
            ],
        )
        self.assertEqual(
            [ccform.paper_number(s["id"]) for s in ccform.list_sections()],
            [1, 2, 3, 4, 5, 6, 7, 8],
        )

    def test_every_section_has_seeds(self):
        for sid in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII"):
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
            "cc_iv_cc8_1": "x¹⁰",
            "cc_iv_cc8_2": "x³⁵",
            "cc_iv_cc8_3": "x⁸⁴",
            "cc_iv_cc8_4": "x¹⁶ / y²⁶",
            "cc_iv_cc8_5": "x = 33/2",
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
            "cc_vi_cc8_table": "6, 10, 14",
            "cc_vi_cc8_diff": "Yes — the common difference is 4",
            "cc_vi_cc8_expr": "6 + 4(n − 1)  or  4n + 2",
            "cc_vi_cc8_30": "122",
            "cc_vi_cc8_bags": "2",
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
            "cc_vii_cc8_14": "Infinite solutions (10 = 10)",
            "cc_vii_cc8_15": "One solution: x = 0",
            "cc_vii_cc8_15_slip": "x = 0 (one solution)",
            "cc_vii_cc8_16": "x = 2",
            "cc_vii_cc8_17": "x = −1/4",
            "cc_vii4_walk": "100 + 10m = 270, so m = 17",
            "cc_vii4_save": "3",
            "cc_vii4_fence": "320 yards",
            "cc_vii4_nfc24": "45",
            "cc_vii4_nfc24_who": "49ers 24, Packers 21 — 49ers by 3",
            "cc_vii4_boat": "20/3 hours",
            "cc_vii4_churros": "50",
            "cc_vii4_shop": "300",
            "cc_vii4_spent": "5000 rupees",
            "cc_vii4_profit": "1000 rupees",
            "cc_vii4_triangle": "360 cm",
            "cc_vii4_stream": "4",
            "cc_vii4_nfc13": "76",
            "cc_vii4_nfc13_who": "Packers 31, 49ers 45 — Packers lost by 14",
            "cc_vii3_n1": "x = 32",
            "cc_vii3_n2": "x = 34",
            "cc_vii3_yt1": "x = 5",
            "cc_vii3_yt3": "Infinite solutions (50 = 50)",
            "cc_vii3_yt4": "x = 9/13",
            "cc_vii3_yt5": "x = −3",
            "cc_vii3_yt8": "x = −24",
            "cc_vii5_n1": "y = −3x + 12",
            "cc_vii5_n2": "y = (4/3)x − 4",
            "cc_vii5_n3": "y = −12x + 51",
            "cc_vii5_n4": "y = 40x − 84",
            "cc_vii5_n5": "y = (−5x − 7)/6",
            "cc_vii5_yt2": "y = −(5/4)x + 5",
            "cc_vii5_yt4": "y = 9x − 13",
            "cc_vii5_n6": "y = x − 2",
            "cc_vii5_yt8": "y = 78x − 72",
            "cc_vii5_yt11": "y = −x − 11",
            "cc_vii5_yt12": "y = 5x − 20",
            "cc_iv_rev_recip": "81",
            "cc_iv_rev_mixed": "7¹⁶ / 2⁷",
            "cc_iv_rev_powmon": "512 x¹² y³",
            "cc_iv_rev_quot": "x⁷ / (3y)",
            "cc_iv_rev_quad": "4¹⁰",
            "cc_iv_rev_prod_eq": "x = 891",
            "cc_iv_rev_pow_eq": "x = 15/2",
            "cc_iv_viir_z0": "24 x² y¹⁰",
            "cc_iv_viir_negden": "(3x⁹)/2",
            "cc_v_rev_14": "8.31 × 10⁻⁴",
            "cc_v_rev_15": "9.09 × 10⁴",
            "cc_v_rev_16": "18,300",
            "cc_v_rev_17": "0.0000924",
            "cc_v_rev_18": "2.6 × 10⁻⁴",
            "cc_v_rev_19": "4.323 × 10¹⁰",
            "cc_v_rev_20": "2.83 × 10¹⁰⁰⁰",
            "cc_v_rev_21": "1.913 × 10⁻⁴",
            "cc_v_rev_22": "4 × 10⁻²¹",
            "cc_v_viir_17": "5.66 × 10¹⁰⁰",
            "cc_v_viir_18": "2.28 × 10¹⁹⁹",
            "cc_vi_viir_expr": "5n − 3",
            "cc_vi_viir_155": "772",
            "cc_vii_r1": "x = 2",
            "cc_vii_r2": "x = −4/15",
            "cc_vii_r3": "x = −24",
            "cc_vii_r4": "No solution (0 = 4)",
            "cc_vii_r5": "No solution (50 = 60)",
            "cc_vii_r6": "x = 38/35",
            "cc_vii_r7": "x = 48/13",
            "cc_vii_r8": "Infinite solutions (8 = 8)",
            "cc_vii_r9": "9",
            "cc_vii_r10": "57",
            "cc_vii_r11": "49ers 37, Packers 20 — 49ers by 17",
            "cc_viii1_missing_y": "78",
            "cc_viii1_check_pt": "No — 2(4) − 14 = −6, not 9",
            "cc_viii1_yt6": "No — 2(5) − 7 = 3, not −3",
            "cc_viii1_yt7": "Yes — 5(10) + 12 = 62",
            "cc_viii1_horiz": "A horizontal line; y is always 5",
            "cc_viii1_vert": "A vertical line; x is always −3",
            "cc_viii1_table": "(−1, 3), (0, 1), (1, −1)",
            "cc_viii1_frac_x": "Multiples of 4, such as −4, 0, 4",
            "cc_viii1_steep": "y = −4x",
            "cc_viii1_yt8": "−1",
            "cc_viii2_graph1": "1/3",
            "cc_viii2_graph2": "−1/5",
            "cc_viii2_zero": "0",
            "cc_viii2_eight": "8",
            "cc_viii2_undef": "undefined",
            "cc_viii2_table": "−2/3",
            "cc_viii2_steeper_a": "A, because |7/3| > 2",
            "cc_viii2_steeper_b": "B, because |−8| = 8 > 5",
            "cc_viii2_tri_len": "AC = 3, BC = 2",
            "cc_viii2_similar": "The triangles are similar — both have slope 2/3",
            "cc_viii2p_g1": "5/2",
            "cc_viii2p_n5": "−14/5",
            "cc_viii2p_n6": "−19/14",
            "cc_viii2p_steepest": "Steepest −14/5; least steep −2/3",
            "cc_viii2p_t8": "−7/6",
            "cc_viii2p_t9": "2/5",
            "cc_viii2p_colin": "Yes — AB and BC both have slope 2",
            "cc_viii2p_k": "11",
            "cc_viii2p_samex": "The x-coordinates are the same, so the line is vertical",
            "cc_viii2p_oct": "6n + 2; 302",
            "cc_viii2p_belda": "120",
            "cc_viii2p_nfc": "T = 45; 49ers 37, Packers 8",
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
        self.assertTrue({"VI-1", "VI-2", "VI-3", "VII-R"} <= papers)
        self.assertTrue(all(q["section"] == "VI" for q in seeds))
        questions = ccform_llm.fallback_seed_set("VI")
        self.assertEqual(len(questions), 10)
        self.assertEqual(ccform.session_count_for_section("VI"), 10)
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
        self.assertEqual(ccform.get_section("VII-4")["id"], "VII")
        self.assertEqual(ccform.get_section("VII-3")["id"], "VII")
        self.assertEqual(ccform.get_section("VII-5")["id"], "VII")
        notes = ccform_llm._notes_for_section("VII")
        self.assertIn("variables on both sides", notes.lower())
        self.assertIn("x = −5", notes)
        self.assertIn("x = 18/5", notes)
        self.assertIn("infinite", notes.lower())
        self.assertIn("no solution", notes.lower())
        self.assertIn("x = −1/2", notes)
        self.assertIn("verbal model", notes.lower())
        self.assertIn("320", notes)
        self.assertIn("38/35", notes)
        self.assertIn("Camping", notes)
        self.assertIn("clear", notes.lower())
        self.assertIn("x = 32", notes)
        self.assertIn("y = mx + b", notes)
        self.assertIn("78x − 72", notes)
        seeds = ccform.seeds_for_section("VII")
        papers = {q["paper"] for q in seeds}
        self.assertTrue({"VII-1", "VII-2", "VII-3", "VII-4", "VII-5", "CC8", "VII-R"} <= papers)
        self.assertTrue(all(q["section"] == "VII" for q in seeds))
        self.assertEqual(ccform.get_section("VII-R")["id"], "VII")
        questions = ccform_llm.fallback_seed_set("VII")
        self.assertEqual(len(questions), 10)
        self.assertEqual(ccform.session_count_for_section("VII"), 10)
        import arjun_course3_content as c3
        unit = c3.get_unit(7)
        slugs = [a["slug"] for a in unit["activities"]]
        self.assertEqual(
            slugs,
            [
                "activity_1_multistep_equations",
                "activity_2_infinite_no_solutions",
                "activity_5_clear_decimals_fractions",
                "activity_3_word_problems",
                "activity_6_solve_for_y",
                "activity_4_algebra_review",
            ],
        )

    def test_unit8_is_one_mixed_section(self):
        info = ccform.get_section("VIII")
        self.assertEqual(info["unit_id"], 8)
        self.assertEqual(info["title"], "Unit 8 — Slope and Linear Equations")
        self.assertEqual(ccform.get_section("VIII-1")["id"], "VIII")
        self.assertEqual(ccform.get_section("VIII-2")["id"], "VIII")
        self.assertEqual(ccform.get_section("VIII-2P")["id"], "VIII")
        notes = ccform_llm._notes_for_section("VIII")
        self.assertIn("linear equation", notes.lower())
        self.assertIn("y = x + 1", notes)
        self.assertIn("78", notes)
        self.assertIn("horizontal", notes.lower())
        self.assertIn("vertical", notes.lower())
        self.assertIn("y = 5", notes)
        self.assertIn("x = −3", notes)
        self.assertIn("rise/run", notes)
        self.assertIn("−1/5", notes)
        self.assertIn("undefined", notes.lower())
        self.assertIn("−2/3", notes)
        self.assertIn("similar", notes.lower())
        self.assertIn("k = 11", notes)
        self.assertIn("6n + 2", notes)
        self.assertIn("302", notes)
        self.assertIn("120", notes)
        self.assertIn("T = 45", notes)
        seeds = ccform.seeds_for_section("VIII")
        papers = {q["paper"] for q in seeds}
        self.assertTrue({"VIII-1", "VIII-2", "VIII-2P"} <= papers)
        self.assertTrue(all(q["section"] == "VIII" for q in seeds))
        questions = ccform_llm.fallback_seed_set("VIII")
        self.assertEqual(len(questions), 10)
        self.assertEqual(ccform.session_count_for_section("VIII"), 10)
        import arjun_course3_content as c3
        unit = c3.get_unit(8)
        slugs = [a["slug"] for a in unit["activities"]]
        self.assertEqual(
            slugs,
            [
                "activity_1_graphing_linear_equations",
                "activity_2_slope",
                "activity_3_slope_practice",
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
        self.assertIn("CC8", papers_iv)
        papers_vi = {q["paper"] for q in ccform.seeds_for_section("VI")}
        papers_vii = {q["paper"] for q in ccform.seeds_for_section("VII")}
        self.assertIn("CC8", papers_v)
        self.assertIn("CC8", papers_vi)
        self.assertIn("CC8", papers_vii)
        iv_stems = {q["stem"] for q in ccform.seeds_for_section("IV")}
        self.assertTrue(
            {"power_of_power_product", "power_of_power_slip", "power_equation_slip"}
            <= iv_stems
        )
        notes = ccform_llm._notes_for_section("IV")
        self.assertIn("x³²", notes)
        self.assertIn("5/3", notes)
        self.assertIn("891", notes)
        papers_iv = {q["paper"] for q in ccform.seeds_for_section("IV")}
        self.assertIn("IV+V review", papers_iv)
        self.assertIn("VII-R", papers_iv)
        questions = ccform_llm.fallback_seed_set("IV")
        self.assertEqual(len(questions), 5)
        self.assertTrue(all(q["section"] == "IV" for q in questions))

    def test_unit5_session_is_five_questions(self):
        self.assertEqual(ccform.session_count_for_section("V"), 5)
        self.assertGreaterEqual(len(ccform.seeds_for_section("V")), 20)
        papers_v = {q["paper"] for q in ccform.seeds_for_section("V")}
        self.assertTrue({"CC6", "CC8", "later form", "IV+V review", "VII-R"} <= papers_v)
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

    def test_practice_screen_formats_scientific_notation(self):
        from arjun_concept_check_form_ui import _math_button, _math_html

        html = _math_html(r"Convert 7.8 × 10^{-4} to standard form.")
        self.assertIn("<sup", html)
        self.assertIn("⁻⁴", html)
        self.assertNotIn("^{-4}", html)
        self.assertEqual(_math_button("7.8 × 10^{-4}"), "7.8 × 10⁻⁴")


if __name__ == "__main__":
    unittest.main()
