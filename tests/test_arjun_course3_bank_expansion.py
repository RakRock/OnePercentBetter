"""Tests for Course 3 bank seeding and refresh."""

from __future__ import annotations

import unittest

import arjun_course3_practice as c3p


class TestCourse3BankSeeding(unittest.TestCase):
    def test_unit1_has_seed_questions_per_category(self) -> None:
        cats = c3p.get_categories(1)
        for cat_id in cats:
            seeds = c3p.seed_questions_for_category(1, cat_id, limit=2)
            self.assertGreaterEqual(len(seeds), 1, msg=cat_id)
            for s in seeds:
                self.assertEqual(s.get("category"), cat_id)
                self.assertEqual(len(s.get("options") or []), 4)

    def test_seed_respects_level_when_available(self) -> None:
        seeds = c3p.seed_questions_for_category(1, "patterns", level="B", limit=3)
        self.assertGreaterEqual(len(seeds), 1)
        for s in seeds:
            self.assertEqual(s.get("category"), "patterns")

    def test_refresh_unit_bank_keeps_at_least_static_count(self) -> None:
        before = len(c3p.QUESTION_BANK_BY_UNIT[1])
        after = c3p.refresh_unit_bank(1)
        self.assertEqual(before, after)
        self.assertGreater(after, 40)

    def test_unit1_merged_bank_size(self) -> None:
        self.assertGreaterEqual(len(c3p.QUESTION_BANK_BY_UNIT[1]), 100)


if __name__ == "__main__":
    unittest.main()
