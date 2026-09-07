"""Tests for practice validation audits."""

from __future__ import annotations

import unittest

import arjun_course3_answers as c3ans
from practice_validation import (
    PRACTICE_APPS,
    build_validation_audit_rows,
    generate_validation_questions,
    list_apps,
    resolve_app,
    run_validation_audit,
    simulate_random_answers,
)


class TestPracticeValidation(unittest.TestCase):
    def test_resolve_app_course3(self) -> None:
        spec = resolve_app("course3")
        self.assertEqual(spec.label, "Course 3 Math")
        self.assertEqual(spec.unit_count, 5)

    def test_generate_questions_unit1(self) -> None:
        questions = generate_validation_questions("course3", 1, 20, seed=42)
        self.assertGreaterEqual(len(questions), 15)
        for q in questions:
            self.assertEqual(len(q.get("options") or []), 4)
            self.assertIn(q.get("answer"), range(4))

    def test_simulate_random_answers_shape(self) -> None:
        q = {
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "answer": 1,
        }
        answers = simulate_random_answers([q], seed=0)
        self.assertEqual(len(answers), 1)
        self.assertIn("picked", answers[0])
        self.assertIn("correct_val", answers[0])
        self.assertIn("correct", answers[0])

    def test_audit_rows_include_keyed_and_picked(self) -> None:
        q = {
            "id": "test_q",
            "category": "fractions",
            "question": "Order 3/4, 0.7, and 72% from greatest to least.",
            "options": ["3/4, 0.7, 72%", "3/4, 72%, 0.7", "72%, 3/4, 0.7", "0.7, 72%, 3/4"],
            "answer": 1,
            "explanation": "0.75 > 0.72 > 0.7",
        }
        answers = [{"picked": "3/4, 0.7, 72%", "picked_index": 0, "correct_val": "3/4, 72%, 0.7", "keyed_index": 1, "correct": False}]
        rows = build_validation_audit_rows([q], answers)
        self.assertEqual(rows[0]["keyed_answer"], "3/4, 72%, 0.7")
        self.assertFalse(rows[0]["correct"])
        self.assertIn("0.75", rows[0]["explanation"])

    def test_run_validation_audit_dry_payload(self) -> None:
        payload = run_validation_audit("course3", 1, 10, seed=99)
        self.assertEqual(payload["generated_count"], 10)
        self.assertEqual(len(payload["audit_rows"]), 10)
        self.assertEqual(len(payload["questions"]), len(payload["answers"]))

    def test_finalize_applied_to_generated_questions(self) -> None:
        q = {
            "question": "Order 3/4, 0.7, and 72% from greatest to least.",
            "options": ["3/4, 0.7, 72%", "3/4, 72%, 0.7", "72%, 3/4, 0.7", "0.7, 72%, 3/4"],
            "answer": 0,
        }
        fixed = c3ans.finalize_question(q)
        self.assertEqual(fixed["answer"], 1)

    def test_list_apps_includes_harshit(self) -> None:
        keys = {spec.key for spec in list_apps()}
        self.assertIn("harshit_prereq", keys)
        self.assertIn("harshit_class10", keys)

    def test_resolve_app_harshit_prereq(self) -> None:
        spec = resolve_app("harshit_prereq")
        self.assertEqual(spec.student_name, "Harshit")
        self.assertEqual(spec.unit_id_label, "PreReq")

    def test_generate_harshit_prereq_questions(self) -> None:
        questions = generate_validation_questions("harshit_prereq", 4, 10, seed=7)
        self.assertGreaterEqual(len(questions), 6)

    def test_run_harshit_prereq_audit(self) -> None:
        payload = run_validation_audit("harshit_prereq", 4, 8, seed=11)
        self.assertGreaterEqual(payload["generated_count"], 5)
        self.assertEqual(payload["student_name"], "Harshit")

    def test_all_registered_apps_have_specs(self) -> None:
        for key, spec in PRACTICE_APPS.items():
            self.assertEqual(spec.key, key)
            self.assertGreater(spec.unit_count, 0)


if __name__ == "__main__":
    unittest.main()
