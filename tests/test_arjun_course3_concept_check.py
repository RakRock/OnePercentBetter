"""Tests for Arjun Course 3 concept-check templates."""

from __future__ import annotations

import unittest

import arjun_course3_concept_check as c3cc
import arjun_course3_practice as c3p


class TestConceptCheckBank(unittest.TestCase):
    def test_unit1_bank_includes_concept_check_questions(self) -> None:
        bank = c3p.QUESTION_BANK_BY_UNIT[1]
        cc = [q for q in bank if q.get("source") == "concept_check"]
        self.assertGreaterEqual(len(cc), 15)

    def test_daily_practice_includes_concept_check_quota(self) -> None:
        import arjun_course3_week as c3w

        for unit_id in range(1, 6):
            cfg = c3w.default_week_config(unit_id)
            counts = []
            for _ in range(15):
                qs = c3p.build_daily_set(count=15, unit_id=unit_id, week_config=cfg, use_llm=False)
                counts.append(sum(1 for q in qs if q.get("source") == "concept_check"))
            avg = sum(counts) / len(counts)
            self.assertGreaterEqual(
                avg,
                5,
                msg=f"Unit {unit_id} avg concept-check {avg:.1f}/15 — expected ≥5",
            )

    def test_focus_practice_prefers_concept_check(self) -> None:
        qs = c3p.build_focus_set(1, "fractions", count=8, use_llm=False)
        cc = sum(1 for q in qs if q.get("source") == "concept_check")
        self.assertGreaterEqual(cc, 3)

    def test_all_units_have_concept_check_categories(self) -> None:
        for unit_id in range(1, 6):
            cats = c3cc.categories_for_unit(unit_id)
            self.assertTrue(cats, msg=f"unit {unit_id} has no concept-check categories")
            for cat in cats:
                self.assertIn(
                    cat,
                    c3cc._DYNAMIC_BY_CATEGORY,
                    msg=f"unit {unit_id} category {cat} missing dynamic generator",
                )

    def test_load_full_bank_includes_builtin(self) -> None:
        for unit_id in range(1, 6):
            bank = c3cc.load_full_concept_check_bank(unit_id)
            self.assertGreaterEqual(len(bank), 4, msg=f"unit {unit_id} concept-check bank too small")

        for q in c3cc.build_concept_check_bank(1):
            self.assertEqual(len(q["options"]), 4)
            self.assertIn(q["answer"], range(4))
            self.assertTrue(q["question"].strip())
            self.assertEqual(q.get("source"), "concept_check")

    def test_archetype_hint_nonempty(self) -> None:
        hint = c3cc.archetype_hint("fractions", "C")
        self.assertIn("fraction", hint.lower())

    def test_unit2_solving_equations_canonical(self) -> None:
        bank = c3cc.build_concept_check_bank(2)
        eq = next(q for q in bank if q["id"] == "cc_u2_eq_multi")
        self.assertIn("−18x", eq["question"])
        self.assertIn("Step", eq["explanation"])

    def test_later_unit_banks_cover_school_concept_checks(self) -> None:
        for unit_id, minimum in ((2, 12), (3, 30), (4, 20), (5, 16)):
            bank = c3cc.build_concept_check_bank(unit_id)
            self.assertGreaterEqual(len(bank), minimum, msg=f"unit {unit_id} bank too small")
            for q in bank:
                self.assertEqual(len(q["options"]), 4)
                self.assertIn(q["answer"], range(4))
                self.assertEqual(q.get("source"), "concept_check")

    def test_systems_include_setup_and_solve(self) -> None:
        bank = c3cc.build_concept_check_bank(2)
        ids = {q["id"] for q in bank}
        self.assertIn("cc_u2_sys_solve", ids)
        self.assertIn("cc_u2_sys_setup_pies", ids)
        self.assertIn("cc_u2_sys_write_point", ids)
        setup = next(q for q in bank if q["id"] == "cc_u2_sys_setup_pies")
        self.assertIn("Do NOT solve", setup["question"])

    def test_unit3_includes_prism_and_pythagorean_3d(self) -> None:
        bank = c3cc.build_concept_check_bank(3)
        ids = {q["id"] for q in bank}
        self.assertIn("cc_u3_pyth_3d", ids)
        self.assertIn("cc_u3_sa_prism_lat", ids)
        self.assertIn("cc_u3_vol_cone", ids)
        self.assertIn("cc_u3_ang_exterior", ids)
        self.assertIn("cc_u3_tr_compose1", ids)
        self.assertIn("cc_u3_sim_area", ids)

    def test_unit4_includes_table_and_discrete(self) -> None:
        bank = c3cc.build_concept_check_bank(4)
        ids = {q["id"] for q in bank}
        self.assertIn("cc_u4_lin_table", ids)
        self.assertIn("cc_u4_fn_discrete", ids)
        self.assertIn("cc_u4_con_tickets", ids)
        self.assertIn("cc_u4_lin_bathtub_zero", ids)
        self.assertIn("cc_u4_fn_eval", ids)
        self.assertIn("cc_u4_compare_total", ids)

    def test_unit5_includes_school_style_stats(self) -> None:
        bank = c3cc.build_concept_check_bank(5)
        ids = {q["id"] for q in bank}
        self.assertIn("cc_u5_tw_burger", ids)
        self.assertIn("cc_u5_tw_seatbelt", ids)
        self.assertIn("cc_u5_mad_compute", ids)
        self.assertIn("cc_u5_bv_predict", ids)
        self.assertIn("cc_u5_sc_outlier", ids)

    def test_dynamic_later_units_stay_well_formed(self) -> None:
        for category in (
            "systems",
            "angles",
            "transformations",
            "similarity",
            "pythagorean",
            "volume",
            "surface_area",
            "function_basics",
            "linear_functions",
            "constructing",
        ):
            for _ in range(8):
                q = c3cc.generate_concept_check_question(3 if category != "systems" else 2, category, "C")
                if category in {"function_basics", "linear_functions", "constructing"}:
                    q = c3cc.generate_concept_check_question(4, category, "C")
                self.assertIsNotNone(q)
                assert q is not None
                self.assertEqual(len(q["options"]), 4)
                self.assertEqual(len(set(q["options"])), 4)
                self.assertIn(q["answer"], range(4))


if __name__ == "__main__":
    unittest.main()
