"""Parsers and daily-practice mixing for Class 10 PYQ seeds."""

from __future__ import annotations

import unittest

import harshit_pyq_books as books
from harshit.chemistry import practice as chem_practice
from harshit.chemistry import topics as chem_topics
from harshit.science_pyq import inject_pyq_into_session


class TestPyqBookParsers(unittest.TestCase):
    def test_objective_mcq_pairs_thus_letter(self):
        sample = """
1. The sum of exponents of prime factors in the prime-factorisation of 196 is
(a) 3
(b) 4
(c) 5
(d) 2
Ans :
Prime factors of 196 give exponents 2 and 2.
Thus (b) is correct option.
"""
        items = books.parse_objective_mcq_page(1, sample, source_label="test")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["answer"], 1)
        self.assertEqual(items[0]["options"][1], "4")

    def test_inline_written_keeps_model_answer(self):
        sample = """
Real Numbers
1) Show that n, n+2 and n+4 leave different remainders when divided by 3.
2012/2014 [2 marks]
Let n be any positive integer. Then n is 3q, 3q+1 or 3q+2, and exactly one of n, n+2, n+4 is divisible by 3.
"""
        buckets = books.parse_inline_written(sample, source_label="test")
        written = buckets[1]["vsa"]
        self.assertEqual(len(written), 1)
        self.assertIn("divisible by 3", written[0]["model_answer"])

    def test_science_short_answer_maps_chapter(self):
        self.assertEqual(books.science_unit_for(1, "Chemical Reactions and Equations")[0], "chemistry")
        self.assertEqual(books.science_unit_for(12, "Electricity")[0], "physics")
        self.assertEqual(books.science_unit_for(6, "Life Process")[1], 1)
        sample = """
ONE MARK QUESTIONS
1.
In electrolysis of water, why is the volume of gas collected over one electrode double that of the other?
Ans :
[CBSE 2018]
Water contains hydrogen and oxygen in the ratio 2 : 1, so hydrogen volume is double.
"""
        items = books.parse_science_short_answers(
            sample, subject="chemistry", unit_id=1, source_label="test"
        )
        self.assertEqual(len(items), 1)
        self.assertIn("hydrogen", items[0]["model_answer"].lower())
        self.assertEqual(items[0]["marks"], 1)

    def test_science_session_mixes_short_answers(self):
        bank = [
            {
                "id": f"bank_{i}",
                "type": "mcq",
                "question": f"Bank question {i}?",
                "options": ["A", "B", "C", "D"],
                "answer": 0,
                "source": "bank",
            }
            for i in range(15)
        ]
        mixed = inject_pyq_into_session(
            "chemistry",
            1,
            bank,
            used_ids=set(),
            session_count=15,
        )
        self.assertEqual(len(mixed), 15)
        pyq = [q for q in mixed if q.get("source") == "board_pyq"]
        # Seeds may be absent in a fresh checkout; when present they must enter the session.
        from harshit.science_pyq import seeds_available

        if seeds_available("chemistry", 1):
            self.assertGreaterEqual(len(pyq), 1)
            self.assertTrue(any(q.get("type") == "short_answer" for q in pyq))

    def test_chemistry_practice_includes_pyq_when_seeded(self):
        from harshit.science_pyq import seeds_available

        if not seeds_available("chemistry", 1):
            self.skipTest("chemistry PYQ seeds not built")
        config = chem_topics.default_week_config(1)
        config["use_chapter_llm"] = False
        qs, _err = chem_practice.build_session_set(1, config, count=15)
        self.assertEqual(len(qs), 15)
        self.assertTrue(any(q.get("source") == "board_pyq" for q in qs))


if __name__ == "__main__":
    unittest.main()
