"""Tests for harshit_class10 exam type generators."""

from __future__ import annotations

import unittest

import harshit_class10_exam_generators as h10eg
import harshit_class10_exam_types as h10et
import harshit_class10_topics as h10t


def _assert_valid_mcq(test: unittest.TestCase, q: dict, exam_type_id: str) -> None:
    test.assertIsInstance(q, dict)
    test.assertEqual(q.get("exam_type"), exam_type_id)
    test.assertEqual(q.get("source"), "exam_template")
    opts = q.get("options") or []
    test.assertEqual(len(opts), 4, msg=f"{exam_type_id}: expected 4 options")
    test.assertIn(q.get("answer"), range(4), msg=f"{exam_type_id}: answer index out of range")
    test.assertEqual(len({str(o).strip().lower() for o in opts}), 4, msg=f"{exam_type_id}: options not distinct")
    test.assertTrue(str(q.get("question", "")).strip(), msg=f"{exam_type_id}: empty question")


class TestExamTypeGenerators(unittest.TestCase):
    def test_registry_covers_all_exam_types(self) -> None:
        registered = set(h10eg.all_generators())
        expected = {t.id for t in h10et.EXAM_TYPES}
        self.assertEqual(registered, expected)

    def test_surd_zero_polynomial_canonical_example(self) -> None:
        """Board-style: zeroes (5−2√3) and (5+2√3) → x²−10x+13."""
        def _norm(s: str) -> str:
            return s.replace(" ", "").replace("−", "-").replace("–", "-")

        for _ in range(20):
            q = h10eg.generate("u2_surd_zero_polynomial")
            self.assertIsNotNone(q)
            opts = q["options"]
            ans_idx = int(q["answer"])
            correct_text = opts[ans_idx]
            if "5 − 2√3" in q["question"] and "5 + 2√3" in q["question"]:
                self.assertEqual(_norm(correct_text), _norm("x² − 10x + 13"))
                self.assertIn("Step 1", q.get("explanation", ""))
                return
        self.skipTest("Random surd variant did not hit canonical (5±2√3) stem in 20 tries")

    def test_cubic_factor_canonical_example(self) -> None:
        """Board-style: p(x)=2x³+x²−5x+2, factor (x−1) → zeroes 1, 1/2, −2."""
        for _ in range(25):
            q = h10eg.generate("u2_cubic_factor_all_zeroes")
            self.assertIsNotNone(q)
            if "2x³ + x² - 5x + 2" in q["question"] or "2x³ + x² − 5x + 2" in q["question"]:
                opts = q["options"]
                ans_idx = int(q["answer"])
                correct = opts[ans_idx].replace(" ", "").replace("−", "-")
                self.assertIn("1/2", correct)
                self.assertIn("-2", correct)
                self.assertIn("Step 1", q.get("explanation", ""))
                return
        self.skipTest("Canonical cubic did not appear in 25 tries")

    def test_u1_euclid_first_remainder_canonical(self) -> None:
        """Board-style: Euclid on 135 and 225 → first remainder 90."""
        for _ in range(25):
            q = h10eg.generate("u1_euclid_first_remainder")
            self.assertIsNotNone(q)
            if "135" in q["question"] and "225" in q["question"]:
                opts = q["options"]
                ans_idx = int(q["answer"])
                self.assertEqual(opts[ans_idx], "90")
                self.assertIn("Step 1", q.get("explanation", ""))
                return
        self.skipTest("Canonical Euclid pair (135, 225) did not appear in 25 tries")

    def test_u3_substitution_full_has_steps(self) -> None:
        q = h10eg.generate("u3_substitution_full")
        self.assertIsNotNone(q)
        _assert_valid_mcq(self, q, "u3_substitution_full")
        self.assertIn("Step 1", q.get("explanation", ""))

    def test_u3_consistency_ratios(self) -> None:
        q = h10eg.generate("u3_consistency_ratios")
        self.assertIsNotNone(q)
        _assert_valid_mcq(self, q, "u3_consistency_ratios")
        opts = q["options"]
        ans_idx = int(q["answer"])
        correct = opts[ans_idx]
        self.assertTrue(
            "Unique" in correct or "No solution" in correct or "Infinitely" in correct,
            msg=f"unexpected consistency answer: {correct}",
        )

    def test_all_exam_types_produce_valid_mcq(self) -> None:
        for et in h10et.EXAM_TYPES:
            q = h10eg.generate(et.id)
            self.assertIsNotNone(q, msg=f"generate({et.id}) returned None")
            _assert_valid_mcq(self, q, et.id)

    def test_generate_for_slot_units_1_to_12(self) -> None:
        for unit_id in range(1, 13):
            topics = h10t.topics_for_unit(unit_id)
            self.assertTrue(topics, msg=f"unit {unit_id} has no topics")
            found = False
            for topic_id in topics:
                for level in h10t.LEVEL_ORDER:
                    if level not in h10t.TOPICS.get(unit_id, {}).get(topic_id, {}).get("levels", {}):
                        continue
                    if not h10et.exam_types_for_slot(unit_id, topic_id, level):
                        continue
                    q = h10eg.generate_for_slot(unit_id, topic_id, level)
                    self.assertIsNotNone(
                        q,
                        msg=f"generate_for_slot({unit_id}, {topic_id}, {level}) returned None",
                    )
                    _assert_valid_mcq(self, q, str(q.get("exam_type")))
                    found = True
            self.assertTrue(found, msg=f"no exam slots found for unit {unit_id}")


if __name__ == "__main__":
    unittest.main()
