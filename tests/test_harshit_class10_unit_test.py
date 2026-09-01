"""Tests for Class 10 board-format unit tests."""

from __future__ import annotations

import unittest

import harshit_class10_board_seeds as h10bs
import harshit_class10_unit_test as h10ut


class TestClass10UnitTest(unittest.TestCase):
    def test_board_seeds_loaded(self) -> None:
        for uid in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
            self.assertTrue(h10bs.seeds_available(uid))
            data = h10bs.load_unit_seeds(uid)
            self.assertGreaterEqual(len(data["mcq"]), 3)
            self.assertGreaterEqual(len(data["la"]), 1)

    def test_available_for_active_units(self) -> None:
        for uid in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
            self.assertTrue(h10ut.unit_test_available(uid))

    def test_build_unit_test_structure(self) -> None:
        questions, err = h10ut.build_unit_test(1)
        self.assertIsNone(err)
        self.assertEqual(len(questions), 8)
        self.assertEqual(sum(q["marks"] for q in questions), h10ut.UNIT_TEST_TOTAL_MARKS)
        self.assertEqual(h10ut.UNIT_TEST_DURATION_SEC, 25 * 60)

        types = [q["type"] for q in questions]
        self.assertEqual(types.count("mcq"), 4)
        self.assertEqual(types.count("assertion_reason"), 1)
        self.assertEqual(types.count("written"), 3)

        sections = [q["section"] for q in questions]
        self.assertEqual(sections, ["A", "A", "A", "A", "A", "B", "C", "D"])

    def test_questions_cite_board_sources(self) -> None:
        questions, _ = h10ut.build_unit_test(3)
        sourced = [q for q in questions if q.get("source")]
        self.assertGreaterEqual(len(sourced), 6)

    def test_report_scoring(self) -> None:
        questions, _ = h10ut.build_unit_test(2)
        responses = []
        for q in questions:
            if q["type"] == "written":
                responses.append({"self_rating": "full"})
            else:
                responses.append({"picked_index": q["answer"]})
        report = h10ut.build_unit_test_report(questions, responses)
        self.assertEqual(report["earned"], report["max_marks"])
        self.assertEqual(report["score_pct"], 100)

    def test_enrich_report_for_sync(self) -> None:
        questions, _ = h10ut.build_unit_test(1)
        responses = []
        for q in questions:
            if q["type"] == "written":
                responses.append(
                    {
                        "ai_grade": {"earned": q["marks"] / 2, "feedback": "Method only"},
                        "work_images": [{"path": "/x.jpg"}],
                    }
                )
            elif q["type"] == "assertion_reason":
                responses.append({"picked_index": 0 if q["answer"] != 0 else 1})
            else:
                responses.append({"picked_index": q["answer"]})
        base = h10ut.build_unit_test_report(questions, responses)
        sync = h10ut.enrich_report_for_sync(base, questions, responses, student_name="Harshit")
        self.assertEqual(sync["session_type"], "unit_test")
        self.assertIn("summary_narrative", sync)
        self.assertGreater(len(sync["failed_questions"]), 0)
        details = h10ut.format_unit_test_report_details(sync)
        self.assertIn("Unit test:", details)


if __name__ == "__main__":
    unittest.main()
