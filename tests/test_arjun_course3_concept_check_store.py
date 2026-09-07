"""Tests for Arjun Course 3 concept-check AI bank persistence."""

from __future__ import annotations

import unittest

from arjun_course3_concept_check_store import reconcile_all_ai_banks


class TestArjunCourse3ConceptCheckStore(unittest.TestCase):
    def test_reconcile_all_ai_banks_is_idempotent(self) -> None:
        first = reconcile_all_ai_banks()
        second = reconcile_all_ai_banks()
        self.assertEqual(first, second)
        for unit_id in range(1, 6):
            self.assertIn(unit_id, first)


if __name__ == "__main__":
    unittest.main()
