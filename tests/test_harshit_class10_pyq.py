"""Tests for PYQ catalog split and practice mixing."""

from __future__ import annotations

import unittest

import harshit_class10_practice as h10p
import harshit_class10_practice_pyq as h10pyq
import harshit_class10_pyq_catalog as cat
import harshit_class10_pyq_parse as parse
import harshit_class10_topics as h10t


class TestHarshitClass10Pyq(unittest.TestCase):
    def test_answer_key_pairs_mcq(self):
        sample = """
1. If HCF (850, 325) is 25, then LCM (850, 325) is :
(A) 442
(B) 11050
(C) 8450
(D) 2210
Answer
1. (B) 11050
"""
        parsed = parse.parse_chapter_block(1, sample, source_label="test")
        self.assertEqual(len(parsed["mcq"]), 1)
        self.assertEqual(parsed["mcq"][0]["answer"], 1)

    def test_written_requires_paired_model(self):
        sample = """
4. Prove that sqrt(5) is an irrational number. (3 Marks)
Answer
4. Assume sqrt(5) = p/q in lowest terms. Then 5q^2 = p^2, so 5 divides p and q. Contradiction.
"""
        parsed = parse.parse_chapter_block(1, sample, source_label="test")
        written = parsed["sa"] + parsed["vsa"] + parsed["la"]
        self.assertEqual(len(written), 1)
        self.assertIn("Contradiction", written[0]["model_answer"])

    def test_garbage_written_dropped(self):
        sample = """
1. Hence, our assumption is wrong.
Answer
1. Hence, our assumption is wrong.
"""
        parsed = parse.parse_chapter_block(1, sample, source_label="test")
        total_w = len(parsed["sa"]) + len(parsed["vsa"]) + len(parsed["la"])
        self.assertEqual(total_w, 0)

    def test_split_real_numbers_sample(self):
        sample = """Real Numbers
1. The HCF of 960 and 432 is:
(A) 48
(B) 54
(C) 72
(D) 36
Polynomials
1. If one of the zeroes of the quadratic polynomial x² + 3x + k is 2, then the value of k is:
(A) -10
(B) 10
(C) 5
(D) -5
"""
        blocks = cat.split_text_by_chapter(sample)
        self.assertTrue(blocks[1])
        parsed = parse.parse_chapter_block(1, blocks[1][0], source_label="test")
        self.assertGreaterEqual(len(parsed["mcq"]), 1)

    def test_practice_session_follows_mark_pattern(self):
        config = h10t.default_week_config(1)
        config["use_chapter_llm"] = False
        config["include_board_pyq"] = True
        qs, _ = h10p.build_session_set(1, config)
        self.assertEqual(len(qs), 10)
        marks = [int(q.get("marks") or 1) for q in qs]
        self.assertEqual(marks.count(1), 5)
        self.assertEqual(marks.count(5), 1)
        n_two, n_three = h10pyq.two_three_split(1)
        self.assertEqual(marks.count(2), n_two)
        self.assertEqual(marks.count(3), n_three)
        self.assertTrue(all(q.get("source") == "board_pyq" for q in qs))

    def test_pyq_disabled(self):
        config = h10t.default_week_config(1)
        config["use_chapter_llm"] = False
        config["include_board_pyq"] = False
        qs, _ = h10p.build_session_set(1, config, count=15)
        self.assertFalse(any(q.get("source") == "board_pyq" for q in qs))

    def test_pick_pyq_respects_written_slots(self):
        used: set[str] = set()
        batch = h10pyq.pick_pyq_questions(1, 4, written_slots=2, used_ids=used)
        written = [q for q in batch if q.get("type") == "written"]
        self.assertGreaterEqual(len(written), 1)

    def test_written_questions_are_listed_in_the_report(self):
        from practice_email.format import format_practice_report_email

        questions = [
            {"type": "mcq", "category_label": "Board PYQ (1 mark)", "question": "sin question", "marks": 1},
            {"type": "mcq", "category_label": "Board PYQ (1 mark)", "question": "cos question", "marks": 1},
            {
                "type": "written",
                "category_label": "Board PYQ (2 marks)",
                "question": "Find tan theta",
                "model_answer": "tan theta = 3/4",
                "marks": 2,
            },
            {
                "type": "written",
                "category_label": "Board PYQ (5 marks)",
                "question": "Prove the identity",
                "model_answer": "Start from sin squared",
                "marks": 5,
            },
        ]
        answers = [
            {"correct": True, "picked": "4/5", "correct_val": "4/5"},
            {"correct": False, "picked": "5/3", "correct_val": "4/5"},
            {"correct": True, "skipped_scoring": True, "self_checked": True, "picked": "self-check"},
            {"correct": True, "skipped_scoring": True, "self_checked": True, "picked": "self-check"},
        ]
        report = h10p.build_session_report(questions, answers, student_name="Harshit")
        self.assertEqual(report["correct_count"], 1)
        self.assertEqual(report["total"], 2)
        self.assertEqual([item["marks"] for item in report["written_review"]], [2, 5])
        self.assertFalse(any(row["total"] == 0 for row in report["needs_revision"] + report["strengths"]))
        _, plain, html = format_practice_report_email(
            student_name="Harshit Sai",
            unit_title="Class X Unit 8",
            unit_subtitle="Week 1",
            report=report,
            time_spent_seconds=55,
            program_name="Harshit Math",
            report_heading="Harshit Math Practice Report",
        )
        self.assertIn("Find tan theta", plain)
        self.assertIn("Prove the identity", html)
        self.assertIn("tan theta = 3/4", html)
        self.assertNotIn("0/0", html)


if __name__ == "__main__":
    unittest.main()
