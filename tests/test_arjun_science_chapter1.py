"""Chapter 1 knowledge-graph quiz from Arjun's Spectrum Science notes."""

from __future__ import annotations

import unittest

import arjun_science_chapter1 as chapter


class TestChapter1KnowledgeGraph(unittest.TestCase):
    def test_sections_match_the_packet(self):
        self.assertEqual(
            [section["id"] for section in chapter.SECTIONS],
            ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9"],
        )
        for section in chapter.SECTIONS:
            self.assertGreaterEqual(len(chapter.ideas_for_section(section["id"])), 3)

    def test_each_link_is_a_question(self):
        ids = [idea["id"] for idea in chapter.IDEAS]
        self.assertEqual(len(ids), len(set(ids)))
        for idea in chapter.IDEAS:
            self.assertEqual(len(idea["options"]), 4)
            self.assertEqual(idea["answer"], 0)
            self.assertTrue(idea["link"].strip())
            self.assertTrue(idea["explanation"].strip())
            self.assertIn(idea["section"], idea["topic"])

    def test_quiz_shuffles_a_copy_and_keeps_the_correct_choice(self):
        original = [list(idea["options"]) for idea in chapter.IDEAS]
        quiz = chapter.build_quiz()
        self.assertEqual(len(quiz), chapter.QUIZ_SIZE)
        by_id = {idea["id"]: idea for idea in chapter.IDEAS}
        for question in quiz:
            correct = by_id[question["id"]]["options"][0]
            self.assertEqual(question["options"][question["answer"]], correct)
        self.assertEqual([list(idea["options"]) for idea in chapter.IDEAS], original)
