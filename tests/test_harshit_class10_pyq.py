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

    def test_practice_session_includes_pyq_when_enabled(self):
        config = h10t.default_week_config(1)
        config["use_chapter_llm"] = False
        config["include_board_pyq"] = True
        config["pyq_count"] = 4
        qs, _ = h10p.build_session_set(1, config, count=15)
        self.assertEqual(len(qs), 15)
        pyq_hits = [q for q in qs if q.get("source") == "board_pyq"]
        self.assertGreaterEqual(len(pyq_hits), 1)

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


if __name__ == "__main__":
    unittest.main()
