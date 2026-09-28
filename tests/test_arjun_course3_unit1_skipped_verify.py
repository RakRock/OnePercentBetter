"""Verification tests for Unit 1 questions the local math checker cannot prove."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from arjun_course3_concept_check_store import load_ai_bank
from arjun_course3_unit1_audit import collect_unverified_unit1_questions, independent_answer_index

REPORT = Path(__file__).resolve().parents[1] / "ArjunCourse3" / "concept_checks" / "unit_1_skipped_verify.json"

# Independent Grok pass (hidden keys) then human adjudication of disagreements.
_FIXED_KEYS = {
    "cc_ai_u1_powers_roots_424885_566": "256",
    "cc_ai_u1_scientific_notation_564030_279": "9.55 × 10^6",
    "cc_ai_u1_scientific_notation_564031_134": "8.08 × 10^7",
    "cc_ai_u1_fractions_771873_792": "5/12",
    "cc_ai_u1_fractions_156514_794": "4/15",
    "cc_ai_u1_fractions_213893_340": "1/4",
    "cc_ai_u1_fractions_213895_907": "7/18",
    "cc_ai_u1_powers_roots_324790_768": "Yes — (36²) ÷ 16 gives the correct area",
    "cc_ai_u1_exponents_775119_721": "Yes, he is correct",
    "cc_ai_u1_exponents_775122_759": "Yes, he is correct",
}
_DROPPED = {
    "cc_ai_u1_patterns_348903_429",
    "cc_ai_u1_scientific_notation_828117_545",
    "cc_ai_u1_rational_numbers_558324_636",
    "cc_ai_u1_exponents_704116_200",
}


class TestUnit1SkippedVerification(unittest.TestCase):
    def test_unverified_questions_are_valid_mcqs(self) -> None:
        questions = collect_unverified_unit1_questions()
        self.assertGreater(len(questions), 50)
        ids = [q.get("id") for q in questions]
        self.assertEqual(len(ids), len(set(ids)))
        for q in questions:
            self.assertEqual(len(q.get("options") or []), 4, q.get("id"))
            self.assertIn(q.get("answer"), range(4), q.get("id"))
            self.assertTrue(str(q.get("question", "")).strip(), q.get("id"))
            idx, _how = independent_answer_index(q)
            self.assertIsNone(idx, q.get("id"))

    def test_grok_verification_report_covers_unverified_set(self) -> None:
        self.assertTrue(REPORT.is_file(), "Grok skipped-question report missing")
        data = json.loads(REPORT.read_text(encoding="utf-8"))
        results = data.get("results") or {}
        summary = data.get("summary") or {}
        self.assertEqual(summary.get("checked"), 322)
        self.assertGreaterEqual(summary.get("agree", 0), 300)
        self.assertEqual(len(results), 322)

    def test_adjudicated_grok_fixes_are_in_ai_bank(self) -> None:
        bank = {str(q.get("id")): q for q in load_ai_bank(1)}
        for qid in _DROPPED:
            self.assertNotIn(qid, bank)
        for qid, expected in _FIXED_KEYS.items():
            self.assertIn(qid, bank, qid)
            q = bank[qid]
            self.assertEqual(q["options"][q["answer"]], expected, qid)


if __name__ == "__main__":
    unittest.main()
