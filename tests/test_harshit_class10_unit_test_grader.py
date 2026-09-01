"""Tests for CBSE-style unit-test written grading."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import harshit_class10_board_seeds as h10bs
import harshit_class10_unit_test as h10ut
import harshit_class10_unit_test_grader as h10g
import harshit_class10_unit_test_uploads as h10utu


class TestUnitTestGrader(unittest.TestCase):
    def test_clamp_half_mark(self) -> None:
        self.assertEqual(h10g.clamp_half_mark(1.2, 2), 1.0)
        self.assertEqual(h10g.clamp_half_mark(1.4, 2), 1.5)
        self.assertEqual(h10g.clamp_half_mark(9, 2), 2.0)
        self.assertEqual(h10g.clamp_half_mark(-1, 2), 0.0)

    def test_marking_scheme_from_rubric(self) -> None:
        scheme = h10g.marking_scheme_for_question(
            {"marks": 3, "rubric": ["Step A", "Step B", "Step C"]}
        )
        self.assertEqual([s["marks"] for s in scheme["steps"]], [1.0, 1.0, 1.0])
        self.assertEqual(sum(s["marks"] for s in scheme["steps"]), 3)

    def test_marking_scheme_prefers_seed(self) -> None:
        scheme = h10g.marking_scheme_for_question(
            {
                "marks": 2,
                "rubric": ["ignored"],
                "marking_scheme": {
                    "source": "MS",
                    "steps": [
                        {"marks": 1, "text": "Ratio test"},
                        {"marks": 1, "text": "k = 2"},
                    ],
                },
            }
        )
        self.assertEqual(scheme["source"], "MS")
        self.assertEqual(scheme["steps"][1]["text"], "k = 2")

    def test_parse_and_normalize_payload(self) -> None:
        written = [
            {
                "q_num": 6,
                "marks": 2,
                "rubric": ["Method", "Answer"],
            }
        ]
        raw = """```json
        {"questions":[{"q_num":6,"earned":1.5,"max":2,"steps":[
          {"awarded":1,"note":"ok"},{"awarded":0.5,"note":"slip"}
        ],"feedback":"Good method","corrections":"Finish the value","confidence":"high"}]}
        ```"""
        payload = h10g.parse_grade_payload(raw)
        grades = h10g.normalize_question_grades(payload, written)
        self.assertEqual(grades[6]["earned"], 1.5)
        self.assertEqual(grades[6]["steps"][1]["awarded"], 0.5)
        self.assertIn("Finish", grades[6]["corrections"])

    def test_written_earned_prefers_ai_grade(self) -> None:
        q = {"marks": 5, "type": "written"}
        self.assertEqual(h10ut.written_earned(q, {"ai_grade": {"earned": 3.5}}), 3.5)
        self.assertEqual(h10ut.written_earned(q, {"self_rating": "full"}), 5.0)
        self.assertEqual(h10ut.written_earned(q, {}), 0.0)

    def test_report_uses_ai_grade(self) -> None:
        questions, err = h10ut.build_unit_test(2)
        self.assertIsNone(err)
        responses = []
        for q in questions:
            if q["type"] == "written":
                responses.append({"ai_grade": {"earned": q["marks"]}})
            else:
                responses.append({"picked_index": q["answer"]})
        report = h10ut.build_unit_test_report(questions, responses)
        self.assertEqual(report["earned"], report["max_marks"])

    def test_unit3_written_seeds_have_marking_scheme(self) -> None:
        h10bs._CACHE.pop(3, None)
        data = h10bs.load_unit_seeds(3)
        for bucket in ("vsa", "sa", "la"):
            for item in data[bucket]:
                self.assertTrue(item.get("marking_scheme", {}).get("steps"), item.get("id"))

    def test_image_data_url_rejects_outside_work_root(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
            tmp.write(b"\xff\xd8\xff")
            tmp.flush()
            self.assertIsNone(h10g.image_data_url(tmp.name))

    def test_image_data_url_accepts_work_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(h10utu, "WORK_ROOT", Path(tmp)):
                path = Path(tmp) / "paper.jpg"
                path.write_bytes(b"\xff\xd8\xff jpeg")
                url = h10g.image_data_url(str(path))
                self.assertIsNotNone(url)
                self.assertTrue(url.startswith("data:image/jpeg;base64,"))

    def test_grade_written_paper_missing_key(self) -> None:
        grades, err = h10g.grade_written_paper(
            written_questions=[{"q_num": 6, "marks": 2, "question": "x", "model_answer": "1"}],
            image_paths=["/nope.jpg"],
            api_key="",
        )
        self.assertEqual(grades, {})
        self.assertIn("XAI_API_KEY", err or "")


if __name__ == "__main__":
    unittest.main()
