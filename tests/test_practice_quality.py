"""Tests for practice quality pipeline."""

from __future__ import annotations

from practice_quality.dedup import (
    fingerprints_for_question,
    is_duplicate_of_any,
    linear_equation_signature,
    normalize_equation,
)
from practice_quality.report import build_learning_report


def _eq_q(text: str, **extra) -> dict:
    return {"question": text, "equation": text, "strategy": 4, "level": "B", **extra}


def test_spacing_and_unicode_duplicates():
    a = _eq_q("8 - 3(2x - 5) = 11")
    b = _eq_q("8 − 3(2x−5)=11")
    fps_a = fingerprints_for_question(a)
    fps_b = fingerprints_for_question(b)
    assert fps_a & fps_b


def test_equivalent_fraction_structure():
    a = _eq_q("1/2 x + 4 = 3/4 x - 2")
    b = _eq_q("2/4 x + 4 = 6/8 x - 2")
    sig_a = linear_equation_signature(a["equation"])
    sig_b = linear_equation_signature(b["equation"])
    assert sig_a == sig_b
    assert normalize_equation(a["equation"]) != normalize_equation(b["equation"]) or sig_a == sig_b


def test_instruction_suffix_duplicate():
    a = _eq_q("8 - 3(2x - 5) = 11")
    b = {
        "question": "Solve for x. 8 - 3(2x - 5) = 11",
        "equation": "8 - 3(2x - 5) = 11",
        "strategy": 4,
        "level": "B",
    }
    assert is_duplicate_of_any(b, fingerprints_for_question(a))


def test_report_scores_match_answers():
    questions = [
        {"question": "x+1=2", "category": "s2_A", "category_label": "Inv · A", "options": ["1", "2", "3", "4"], "answer": 0, "explanation": "x=1"},
        {"question": "x+2=4", "category": "s2_B", "category_label": "Inv · B", "options": ["2", "3", "4", "5"], "answer": 0, "explanation": "x=2"},
    ]
    answers = [{"correct": True}, {"correct": False, "choice": 1}]
    report = build_learning_report(questions, answers, student_name="Arjun")
    assert report["correct_count"] == 1
    assert report["total"] == 2
    assert report["score_pct"] == 50
    assert report["summary_narrative"].startswith("Arjun")


def test_coaching_concepts_in_report_and_email():
    questions = [
        {
            "question": "Solve: 1/4 x = 6. What is x?",
            "equation": "1/4 x = 6",
            "strategy": 2,
            "level": "D",
            "category": "s2_D",
            "category_label": "Inverse · D",
            "options": ["6", "24", "12", "3"],
            "answer": 1,
            "explanation": "Multiply both sides by 4.",
        },
        {
            "question": "Solve: 8 - 3(2x - 5) = 11. What is x?",
            "equation": "8 - 3(2x - 5) = 11",
            "strategy": 4,
            "level": "B",
            "category": "s4_B",
            "category_label": "Distributive · B",
            "options": ["2", "3", "1", "4"],
            "answer": 0,
            "explanation": "Distribute -3.",
        },
    ]
    answers = [
        {"correct": False, "choice": 0, "picked": "6", "correct_val": "24"},
        {"correct": False, "choice": 1, "picked": "3", "correct_val": "2"},
    ]
    report = build_learning_report(questions, answers, student_name="Arjun")
    concepts = report.get("coaching_concepts") or []
    assert len(concepts) >= 2
    titles = {c["title"] for c in concepts}
    assert "Signs and negatives" in titles or "Finish isolating the variable" in titles

    from practice_email.format import format_practice_report_email

    _, plain, html = format_practice_report_email(
        student_name="Arjun",
        unit_title="Linear Equations",
        unit_subtitle="Week 1",
        report=report,
        time_spent_seconds=600,
    )
    assert "GO OVER TOGETHER" in plain
    assert "Go over together" in html
