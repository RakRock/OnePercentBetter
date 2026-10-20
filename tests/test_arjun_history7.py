"""Grade 7 History Unit 2 multiple-choice bank."""

from __future__ import annotations

import random
import unittest

import arjun_history7 as hist


class TestHistoryUnit2(unittest.TestCase):
    def test_unit_and_topics(self):
        self.assertEqual(hist.GRADE, 7)
        self.assertEqual(hist.UNIT["id"], 2)
        self.assertEqual(hist.UNIT["name"], "The Rise of Islam")
        self.assertEqual(len(hist.TOPICS), 6)
        self.assertEqual(len(hist.QUESTIONS), 100)
        self.assertEqual([question["id"] for question in hist.QUESTIONS], list(range(1, 101)))

    def test_each_question_is_multiple_choice(self):
        for question in hist.QUESTIONS:
            self.assertEqual(len(question["options"]), 4)
            self.assertEqual(len(set(question["options"])), 4)
            self.assertEqual(question["answer"], 0)
            self.assertTrue(question["question"].strip())
            self.assertTrue(question["explanation"].strip())
            self.assertIn(question["topic"], {topic["id"] for topic in hist.TOPICS})

    def test_topic_counts(self):
        counts = hist.question_counts()
        self.assertEqual(counts["geography"], 15)
        self.assertEqual(counts["muhammad"], 15)
        self.assertEqual(counts["pillars"], 20)
        self.assertEqual(counts["empire"], 20)
        self.assertEqual(counts["split"], 15)
        self.assertEqual(counts["golden"], 15)
        self.assertEqual(sum(counts.values()), 100)

    def test_known_answers_from_the_source_quiz(self):
        by_id = {question["id"]: question for question in hist.QUESTIONS}
        self.assertEqual(by_id[1]["options"][0], "Desert / Arid")
        self.assertEqual(by_id[16]["options"][0], "570 CE")
        self.assertEqual(by_id[24]["options"][0], "Hijrah")
        self.assertEqual(by_id[31]["options"][0], "Five")
        self.assertEqual(by_id[58]["options"][0], "Battle of Tours")
        self.assertEqual(by_id[77]["options"][0], "Battle of Karbala")
        self.assertEqual(by_id[86]["options"][0], "Algebra")
        self.assertEqual(by_id[100]["options"][0], "One Thousand and One Nights")

    def test_topic_quiz_shuffles_without_changing_the_bank(self):
        original = [list(question["options"]) for question in hist.questions_for_topic("pillars")]
        quiz = hist.build_quiz(topic_id="pillars", rng=random.Random(3))
        after = [list(question["options"]) for question in hist.questions_for_topic("pillars")]
        self.assertEqual(original, after)
        self.assertEqual(len(quiz), hist.TOPIC_QUIZ_SIZE)
        self.assertTrue(all(question["topic"] == "pillars" for question in quiz))
        self.assertTrue(any(question["answer"] != 0 for question in quiz))
        for question in quiz:
            self.assertEqual(
                question["options"][question["answer"]],
                next(item["options"][0] for item in hist.QUESTIONS if item["id"] == question["id"]),
            )

    def test_full_topic_uses_every_question_once(self):
        quiz = hist.build_quiz(topic_id="geography", full_topic=True, rng=random.Random(1))
        self.assertEqual(sorted(question["id"] for question in quiz), list(range(1, 16)))

    def test_unit_mix_draws_two_questions_from_each_topic(self):
        quiz = hist.build_quiz(unit_mix=True, rng=random.Random(7))
        self.assertEqual(len(quiz), hist.UNIT_QUIZ_SIZE)
        counts: dict[str, int] = {}
        for question in quiz:
            counts[question["topic"]] = counts.get(question["topic"], 0) + 1
        self.assertEqual(set(counts), {topic["id"] for topic in hist.TOPICS})
        self.assertTrue(all(count == 2 for count in counts.values()))

    def test_empty_request_returns_no_questions(self):
        self.assertEqual(hist.build_quiz(), [])

    def test_lesson_notes_cover_every_topic(self):
        self.assertEqual(len(hist.LESSONS), 5)
        covered = [topic_id for lesson in hist.LESSONS for topic_id in lesson["topic_ids"]]
        self.assertEqual(covered, [topic["id"] for topic in hist.TOPICS])
        for lesson in hist.LESSONS:
            text = hist.load_lesson_notes(lesson["id"])
            self.assertIn(f"Chapter {lesson['chapter']}", text)
            self.assertGreater(len(text), 200)
        review = hist.load_review_notes()
        self.assertIn("Hijrah", review)
        self.assertIn("Algebra", review)
        self.assertEqual(hist.lesson_for_topic("split")["id"], "empire")


class TestHistoryUnit3(unittest.TestCase):
    def test_unit_list_includes_west_africa(self):
        import arjun_history_unit3 as unit3

        units = hist.list_units()
        self.assertEqual([unit["id"] for unit in units], [2, 3])
        self.assertEqual(unit3.UNIT["name"], "The Gold and Salt Kingdoms of West Africa")
        self.assertIs(hist.content_for(3), unit3)
        self.assertEqual(len(unit3.LESSONS), 5)
        self.assertEqual(len(unit3.QUESTIONS), 100)
        by_id = {question["id"]: question for question in unit3.QUESTIONS}
        self.assertEqual(by_id[1]["options"][0], "Sahara Desert")
        self.assertEqual(by_id[18]["options"][0], "Battle of Kirina")
        self.assertEqual(by_id[42]["options"][0], "Battle of Tondibi")
        self.assertEqual(by_id[100]["options"][0], "They provide valuable insights into African history and culture")

    def test_notes_cover_the_three_empires_and_griots(self):
        import arjun_history_unit3 as unit3

        text = "\n".join(unit3.load_lesson_notes(lesson["id"]) for lesson in unit3.LESSONS)
        text += unit3.load_review_notes()
        for phrase in ("Taghaza", "Koumbi Saleh", "Sundiata", "Mansa Musa", "Tondibi", "griot"):
            self.assertIn(phrase, text)

    def test_practice_round_includes_every_chapter(self):
        import arjun_history_unit3 as unit3

        quiz = unit3.build_quiz(unit_mix=True, rng=random.Random(3))
        self.assertEqual(len(quiz), unit3.UNIT_QUIZ_SIZE)
        self.assertEqual({question["topic"] for question in quiz}, {topic["id"] for topic in unit3.TOPICS})
        for question in quiz:
            self.assertEqual(
                question["options"][question["answer"]],
                next(item["options"][0] for item in unit3.QUESTIONS if item["id"] == question["id"]),
            )
