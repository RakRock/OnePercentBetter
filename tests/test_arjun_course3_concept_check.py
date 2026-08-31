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


if __name__ == "__main__":
    unittest.main()
