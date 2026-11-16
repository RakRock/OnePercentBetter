"""NCERT practice uses 1-, 2-, 3-, and 5-mark chapter questions."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import harshit_class10_ncert as h10ncert
import harshit_class10_practice as h10p


ROOT = Path(__file__).resolve().parents[1]


class NcertCirclesPracticeTests(unittest.TestCase):
    def test_unit10_session_has_each_mark(self) -> None:
        session = h10ncert.build_session(10)
        marks = [int(q["marks"]) for q in session]
        self.assertEqual(marks, sorted(marks))
        self.assertEqual(set(marks), {1, 2, 3, 5})
        self.assertGreaterEqual(marks.count(1), 5)
        self.assertGreaterEqual(marks.count(2), 2)
        self.assertGreaterEqual(marks.count(3), 2)
        self.assertGreaterEqual(marks.count(5), 1)
        self.assertIn("1 mark", h10ncert.pattern_summary(10))
        self.assertIn("5 mark", h10ncert.pattern_summary(10))

    def test_other_units_are_not_loaded(self) -> None:
        self.assertFalse(h10ncert.ncert_available(11))
        self.assertEqual(h10ncert.build_session(11), [])

    def test_one_mark_items_are_distinct_mcqs(self) -> None:
        for question in h10ncert.build_session(10):
            if int(question["marks"]) != 1:
                continue
            self.assertEqual(question["type"], "mcq")
            options = question["options"]
            self.assertEqual(len(options), 4)
            self.assertEqual(len(set(options)), 4)
            self.assertIn(question["answer"], range(4))

    def test_written_results_match_the_working(self) -> None:
        by_id = {q["id"]: q for q in h10ncert.build_session(10)}
        expected_answers = {
            "ncert_u10_radius_3": "3 cm",
            "ncert_u10_chord_8": "8",
            "ncert_u10_radius_5": "5 cm",
            "ncert_u10_diameter_tangents_parallel": "tangents are parallel",
            "ncert_u10_perpendicular_through_centre": "passes through the centre",
            "ncert_u10_tangential_quad": "AB + CD = AD + BC",
            "ncert_u10_tangent_angles_supplementary": "the angles are supplementary",
            "ncert_u10_parallel_third_tangent": "90",
            "ncert_u10_triangle_sides": "AB 15 cm and AC 13 cm",
            "ncert_u10_opposite_sides_centre": "supplementary angles at the centre",
        }
        for qid, typed in expected_answers.items():
            question = by_id[qid]
            self.assertEqual(question["type"], "written")
            self.assertGreaterEqual(len(h10p.board_working_steps(question)), 3)
            self.assertTrue(h10p.fill_in_is_correct(question, typed), h10p.expected_fill_in(question))
            self.assertFalse(h10p.fill_in_is_correct(question, ""))

        figure = ROOT / by_id["ncert_u10_parallel_third_tangent"]["figure"]
        self.assertTrue(figure.is_file())


class NcertRealNumbersPracticeTests(unittest.TestCase):
    def test_unit1_has_the_missing_mark_mix(self) -> None:
        session = h10ncert.build_session(1)
        marks = [int(q["marks"]) for q in session]
        self.assertEqual(marks, sorted(marks))
        self.assertEqual(set(marks), {1, 2, 3, 5})
        self.assertGreaterEqual(len(session), 100)
        for question in session:
            if question["type"] == "mcq":
                options = question["options"]
                self.assertEqual(len(options), 4)
                self.assertEqual(len(set(options)), 4)
                self.assertNotIn("accept", question)

    def test_unit1_written_answers_match_the_working(self) -> None:
        raw = json.loads((ROOT / "HarshitMath/class10/ncert/unit_01.json").read_text(encoding="utf-8"))
        by_id = {q["id"]: q for q in h10ncert.build_session(1)}
        for question in raw["questions"]:
            if question["type"] != "written":
                continue
            wrapped = by_id[question["id"]]
            self.assertGreaterEqual(len(h10p.board_working_steps(wrapped)), 2)
            self.assertTrue(
                h10p.fill_in_is_correct(wrapped, question["accept"]),
                h10p.expected_fill_in(wrapped),
            )
            self.assertNotIn("accept", wrapped)
            if question["question"].lower().startswith("prove"):
                self.assertFalse(h10p.fill_in_is_correct(wrapped, "rational"))


class NcertPolynomialsPracticeTests(unittest.TestCase):
    def test_unit2_has_the_missing_mark_mix(self) -> None:
        session = h10ncert.build_session(2)
        marks = [int(q["marks"]) for q in session]
        self.assertEqual(marks, sorted(marks))
        self.assertEqual(set(marks), {1, 2, 3, 5})
        self.assertEqual(marks.count(1), 77)
        self.assertEqual(marks.count(2), 32)
        self.assertEqual(marks.count(3), 22)
        self.assertEqual(marks.count(5), 3)
        self.assertIn("5 mark", h10ncert.pattern_summary(2))
        for question in session:
            if question["type"] == "mcq":
                options = question["options"]
                self.assertEqual(len(options), 4)
                self.assertEqual(len(set(options)), 4)
                self.assertNotIn("accept", question)

    def test_unit2_written_answers_match_the_working(self) -> None:
        raw = json.loads((ROOT / "HarshitMath/class10/ncert/unit_02.json").read_text(encoding="utf-8"))
        by_id = {q["id"]: q for q in h10ncert.build_session(2)}
        accepts = {q["id"]: q.get("accept") for q in raw["questions"]}
        self.assertEqual(accepts["ncert_u2_twice_other_k"], "5/6, 5/3 and -8/9")
        self.assertEqual(accepts["ncert_u2_k_8"], "8")
        cubic = by_id["ncert_u2_formed_cubic_roots"]
        self.assertEqual(cubic["options"][cubic["answer"]], "3x^3 - 5x^2 - 11x - 3")
        for question in raw["questions"]:
            if question["type"] != "written":
                continue
            wrapped = by_id[question["id"]]
            self.assertGreaterEqual(len(h10p.board_working_steps(wrapped)), 2)
            self.assertTrue(
                h10p.fill_in_is_correct(wrapped, question["accept"]),
                h10p.expected_fill_in(wrapped),
            )
            self.assertNotIn("accept", wrapped)
            if question["question"].lower().startswith("prove"):
                self.assertFalse(h10p.fill_in_is_correct(wrapped, "rational"))


if __name__ == "__main__":
    unittest.main()
