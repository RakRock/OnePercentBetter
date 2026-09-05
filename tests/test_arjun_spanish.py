"""Tests for Arjun Spanish vocabulary and practice helpers."""

from __future__ import annotations

import random
import unittest

from arjun_spanish import content as es
from arjun_spanish import practice as esp


class TestSpanishContent(unittest.TestCase):
    def test_unique_card_ids(self) -> None:
        ids = [c["id"] for c in es.CARDS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_topic_has_enough_cards(self) -> None:
        for topic in es.TOPICS:
            cards = es.cards_for_topic(topic["id"])
            self.assertGreaterEqual(
                len(cards),
                4,
                msg=f"{topic['id']} needs at least 4 cards for a quiz",
            )
            self.assertTrue(all(c["spanish"] and c["english"] for c in cards))

    def test_school_packet_accents(self) -> None:
        spanish = " ".join(c["spanish"] for c in es.CARDS)
        for needle in ("días", "Cómo", "lápiz", "señor", "mañana", "miércoles", "sábado"):
            self.assertIn(needle, spanish, msg=f"missing accented form: {needle}")

    def test_classroom_articles(self) -> None:
        by_es = {c["spanish"]: c for c in es.cards_for_topic("classroom")}
        self.assertIn("el lápiz", by_es)
        self.assertIn("la carpeta", by_es)
        self.assertEqual(by_es["el lápiz"]["english"], "the pencil")

    def test_daily_mix_is_full_bank(self) -> None:
        self.assertEqual(len(es.cards_for_topic("daily")), es.total_cards())
        self.assertGreaterEqual(es.total_cards(), 100)


class TestSpanishPractice(unittest.TestCase):
    def test_typed_matches_forgiving_accents_and_articles(self) -> None:
        card = {"spanish": "el lápiz", "english": "the pencil"}
        self.assertTrue(esp.typed_matches("el lápiz", card))
        self.assertTrue(esp.typed_matches("el lapiz", card))
        self.assertTrue(esp.typed_matches("lápiz", card))
        self.assertTrue(esp.typed_matches("lapiz", card))
        self.assertFalse(esp.typed_matches("el libro", card))
        self.assertFalse(esp.typed_matches("", card))

    def test_strip_accents_keeps_n_tilde(self) -> None:
        self.assertEqual(esp.strip_accents("mañana"), "mañana")
        self.assertEqual(esp.strip_accents("Cómo"), "Como")
        self.assertEqual(esp.strip_accents(esp.normalize_answer("¿Cómo?")), "como")

    def test_mc_questions_have_four_options(self) -> None:
        rng = random.Random(7)
        cards = esp.pick_cards("greetings", es.QUIZ_SIZE, rng)
        qs = esp.make_mc_questions(cards, direction="es_en", rng=rng)
        self.assertGreaterEqual(len(qs), 4)
        for q in qs:
            self.assertEqual(len(q["options"]), 4)
            self.assertIn(q["answer"], q["options"])
            self.assertEqual(len(set(q["options"])), 4)

    def test_match_round_pairs(self) -> None:
        rng = random.Random(3)
        cards = esp.pick_cards("weather", 8, rng)
        round_ = esp.make_match_round(cards, pair_count=5, rng=rng)
        self.assertEqual(round_["pairs"], 5)
        self.assertEqual(len(round_["left"]), 5)
        self.assertEqual({x["id"] for x in round_["left"]}, {x["id"] for x in round_["right"]})


class TestSpanishSession(unittest.TestCase):
    def test_build_session_from_bank(self) -> None:
        from arjun_spanish import session as ess

        cfg = {
            "topics": ["greetings", "numbers"],
            "use_llm": False,
            "question_count": 6,
        }
        questions, err = ess.build_session_set(cfg, count=6)
        self.assertEqual(err, "")
        self.assertEqual(len(questions), 6)
        for q in questions:
            self.assertEqual(len(q["options"]), 4)
            self.assertIn(q["answer"], range(4))
            self.assertTrue(q.get("explanation"))

    def test_card_to_question_format(self) -> None:
        from arjun_spanish import bank as esbank

        card = es.cards_for_topic("greetings")[0]
        q = esbank.card_to_question(card, direction="es_en")
        self.assertIsNotNone(q)
        assert q is not None
        self.assertIn("Buenos días", q["question"])
        self.assertEqual(len(q["options"]), 4)


if __name__ == "__main__":
    unittest.main()
