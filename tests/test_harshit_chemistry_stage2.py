"""Stage 2 MCQ bank and Stage 3 exercise bank for Harshit Chemistry units 1–4."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def unit1_dir() -> Path:
    return ROOT / "HarshitChemistry" / "unit1"


def test_unit1_mcq_bank_active_with_40_questions(unit1_dir: Path) -> None:
    bank = json.loads((unit1_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    sessions = bank["sessions"]
    assert len(sessions) == 4
    assert sum(len(s["questions"]) for s in sessions) == 40
    for s in sessions:
        assert len(s["questions"]) == 10
        assert s.get("activity_refs") is not None


def test_unit1_ncert_source_activities(unit1_dir: Path) -> None:
    src = json.loads((unit1_dir / "ncert_source.json").read_text(encoding="utf-8"))
    activities = src["activities"]
    ids = {a["id"] for a in activities}
    assert ids == {f"1.{i}" for i in range(1, 12)}
    assert len(src.get("exercise_mcqs", [])) >= 3


def test_unit1_stage2_and_stage3_helpers() -> None:
    from harshit.chemistry import content as hpc

    assert hpc.stage2_available(1)
    assert hpc.stage3_available(1)
    assert len(hpc.list_mcq_sessions(1)) == 4
    day17 = hpc.get_mcq_session(17, 1)
    assert day17 and len(day17["questions"]) == 10
    acts = hpc.ncert_activities_for_stage2_day(17, 1)
    assert {a["id"] for a in acts} == {"1.1", "1.2", "1.3"}


def test_unit1_exercise_bank(unit1_dir: Path) -> None:
    bank = json.loads((unit1_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    qs = bank["questions"]
    assert len(qs) == 17
    nums = sorted(int(q["num"]) for q in qs)
    assert nums == list(range(4, 21))


def test_unit1_pdf_present(unit1_dir: Path) -> None:
    assert (unit1_dir / "jesc101.pdf").is_file()


@pytest.fixture
def unit2_dir() -> Path:
    return ROOT / "HarshitChemistry" / "unit2"


def test_unit2_mcq_bank_active(unit2_dir: Path) -> None:
    bank = json.loads((unit2_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    assert len(bank["sessions"]) == 4
    assert sum(len(s["questions"]) for s in bank["sessions"]) == 40


def test_unit2_exercise_bank(unit2_dir: Path) -> None:
    bank = json.loads((unit2_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    qs = bank["questions"]
    assert len(qs) == 11
    assert [q["num"] for q in qs] == list(range(5, 16))


def test_unit2_stage2_and_stage3_helpers() -> None:
    from harshit.chemistry import content as hpc

    assert hpc.stage2_available(2)
    assert hpc.stage3_available(2)
    assert len(hpc.list_ncert_activities(2)) == 15


@pytest.fixture
def unit3_dir() -> Path:
    return ROOT / "HarshitChemistry" / "unit3"


def test_unit3_mcq_bank_active(unit3_dir: Path) -> None:
    bank = json.loads((unit3_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    assert len(bank["sessions"]) == 4
    assert sum(len(s["questions"]) for s in bank["sessions"]) == 40


def test_unit3_exercise_bank(unit3_dir: Path) -> None:
    bank = json.loads((unit3_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    qs = bank["questions"]
    assert len(qs) == 12
    assert [q["num"] for q in qs] == list(range(5, 17))


def test_unit3_stage2_and_stage3_helpers() -> None:
    from harshit.chemistry import content as hpc

    assert hpc.stage2_available(3)
    assert hpc.stage3_available(3)
    assert len(hpc.list_ncert_activities(3)) == 13


@pytest.fixture
def unit4_dir() -> Path:
    return ROOT / "HarshitChemistry" / "unit4"


def test_unit4_mcq_bank_active(unit4_dir: Path) -> None:
    bank = json.loads((unit4_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    assert len(bank["sessions"]) == 4
    assert sum(len(s["questions"]) for s in bank["sessions"]) == 40


def test_unit4_exercise_bank(unit4_dir: Path) -> None:
    bank = json.loads((unit4_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    qs = bank["questions"]
    assert len(qs) == 12
    assert [q["num"] for q in qs] == list(range(4, 16))


def test_unit4_stage2_and_stage3_helpers() -> None:
    from harshit.chemistry import content as hpc

    assert hpc.stage2_available(4)
    assert hpc.stage3_available(4)
    assert len(hpc.list_ncert_activities(4)) == 12


def test_all_chemistry_units_stage2_stage3() -> None:
    from harshit.chemistry import content as hpc

    for uid in range(1, 5):
        assert hpc.stage2_available(uid), f"unit {uid} stage2"
        assert hpc.stage3_available(uid), f"unit {uid} stage3"
        assert sum(len(s["questions"]) for s in hpc.list_mcq_sessions(uid)) == 40
