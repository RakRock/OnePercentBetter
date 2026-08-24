"""Stage 2 MCQ bank and Stage 3 exercise bank for Harshit Biology units 1–4."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def unit1_dir() -> Path:
    return ROOT / "HarshitBiology" / "unit1"


def test_unit1_mcq_bank_active_with_40_questions(unit1_dir: Path) -> None:
    bank = json.loads((unit1_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    sessions = bank["sessions"]
    assert len(sessions) == 4
    assert sum(len(s["questions"]) for s in sessions) == 40


def test_unit1_exercise_bank(unit1_dir: Path) -> None:
    bank = json.loads((unit1_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    qs = bank["questions"]
    assert len(qs) == 9
    assert [q["num"] for q in qs] == list(range(5, 14))


def test_unit1_stage2_and_stage3_helpers() -> None:
    from harshit.biology import content as hpb

    assert hpb.stage2_available(1)
    assert hpb.stage3_available(1)
    assert hpb.total_concept_cards(active_only=True, unit_id=1) == 160
    acts = hpb.ncert_activities_for_stage2_day(17, 1)
    assert {a["id"] for a in acts} == {"5.1", "5.2"}


def test_unit1_pdf_present(unit1_dir: Path) -> None:
    assert (unit1_dir / "jesc105.pdf").is_file()


@pytest.fixture
def unit2_dir() -> Path:
    return ROOT / "HarshitBiology" / "unit2"


def test_unit2_biology_mcq_and_written(unit2_dir: Path) -> None:
    from harshit.biology import content as hpb

    bank = json.loads((unit2_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    assert sum(len(s["questions"]) for s in bank["sessions"]) == 40
    ex = json.loads((unit2_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert len(ex["questions"]) == 9
    assert [q["num"] for q in ex["questions"]] == list(range(4, 13))
    assert hpb.stage2_available(2) and hpb.stage3_available(2)
    assert (unit2_dir / "jesc106.pdf").is_file()


@pytest.fixture
def unit3_dir() -> Path:
    return ROOT / "HarshitBiology" / "unit3"


def test_unit3_biology_mcq_and_written(unit3_dir: Path) -> None:
    from harshit.biology import content as hpb

    bank = json.loads((unit3_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert sum(len(s["questions"]) for s in bank["sessions"]) == 40
    ex = json.loads((unit3_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert len(ex["questions"]) == 8
    assert [q["num"] for q in ex["questions"]] == list(range(4, 12))
    assert hpb.stage2_available(3) and hpb.stage3_available(3)
    assert (unit3_dir / "jesc107.pdf").is_file()


@pytest.fixture
def unit4_dir() -> Path:
    return ROOT / "HarshitBiology" / "unit4"


def test_unit4_biology_mcq_and_written(unit4_dir: Path) -> None:
    from harshit.biology import content as hpb

    bank = json.loads((unit4_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert sum(len(s["questions"]) for s in bank["sessions"]) == 40
    ex = json.loads((unit4_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert len(ex["questions"]) == 3
    assert [q["num"] for q in ex["questions"]] == [2, 3, 4]
    assert hpb.stage2_available(4) and hpb.stage3_available(4)
    assert (unit4_dir / "jesc108.pdf").is_file()


def test_all_biology_units_stage2_stage3() -> None:
    from harshit.biology import content as hpb

    expected_written = {1: 9, 2: 9, 3: 8, 4: 3}
    for uid in range(1, 5):
        assert hpb.stage2_available(uid), f"unit {uid} stage2"
        assert hpb.stage3_available(uid), f"unit {uid} stage3"
        assert hpb.total_concept_cards(active_only=True, unit_id=uid) == 160
        assert sum(len(s["questions"]) for s in hpb.list_mcq_sessions(uid)) == 40
        assert len(hpb.list_exercise_questions(uid)) == expected_written[uid]
