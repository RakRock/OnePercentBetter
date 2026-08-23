"""Stage 2 MCQ bank and NCERT source mapping for Physics Unit 1."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def unit1_dir() -> Path:
    return ROOT / "HarshitPhysics" / "unit1"


def test_mcq_bank_active_with_40_questions(unit1_dir: Path) -> None:
    bank = json.loads((unit1_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    sessions = bank["sessions"]
    assert len(sessions) == 4
    assert sum(len(s["questions"]) for s in sessions) == 40
    for s in sessions:
        assert len(s["questions"]) == 10
        assert s.get("activity_refs") is not None


def test_ncert_source_maps_all_activities(unit1_dir: Path) -> None:
    src = json.loads((unit1_dir / "ncert_source.json").read_text(encoding="utf-8"))
    activities = src["activities"]
    ids = {a["id"] for a in activities}
    expected = {f"9.{i}" for i in range(1, 14)}
    assert ids == expected
    assert len(src.get("exercise_mcqs", [])) >= 6


def test_stage2_content_helpers() -> None:
    from harshit.physics import content as hpc

    assert hpc.stage2_available(1)
    assert len(hpc.list_mcq_sessions(1)) == 4
    day17 = hpc.get_mcq_session(17, 1)
    assert day17 and len(day17["questions"]) == 10
    acts = hpc.ncert_activities_for_stage2_day(17, 1)
    assert {a["id"] for a in acts} == {"9.1", "9.3", "9.4"}


def test_stage3_exercise_bank(unit1_dir: Path) -> None:
    bank = json.loads((unit1_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    qs = bank["questions"]
    assert len(qs) == 11
    nums = sorted(int(q["num"]) for q in qs)
    assert nums == list(range(7, 18))
    guided = [q for q in qs if q.get("guided_tool")]
    assert len(guided) >= 6


def test_stage3_content_helpers() -> None:
    from harshit.physics import content as hpc

    assert hpc.stage3_available(1)
    assert len(hpc.list_exercise_questions(1)) == 11
    q10 = hpc.get_exercise_question_by_num(10, 1)
    assert q10 and q10["guided_tool"]["type"] == "lens"


def test_pdf_present(unit1_dir: Path) -> None:
    assert (unit1_dir / "jesc109.pdf").is_file()


@pytest.fixture
def unit2_dir() -> Path:
    return ROOT / "HarshitPhysics" / "unit2"


def test_unit2_mcq_bank_active(unit2_dir: Path) -> None:
    bank = json.loads((unit2_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    assert len(bank["sessions"]) == 4
    assert sum(len(s["questions"]) for s in bank["sessions"]) == 40


def test_unit2_exercise_bank(unit2_dir: Path) -> None:
    bank = json.loads((unit2_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    qs = bank["questions"]
    assert len(qs) == 8
    assert [q["num"] for q in qs] == list(range(5, 13))


def test_unit2_stage2_and_stage3_helpers() -> None:
    from harshit.physics import content as hpc

    assert hpc.stage2_available(2)
    assert hpc.stage3_available(2)
    assert len(hpc.list_ncert_activities(2)) == 2
    acts = hpc.ncert_activities_for_stage2_day(19, 2)
    assert {a["id"] for a in acts} == {"10.1", "10.2"}


def test_unit2_pdf_present(unit2_dir: Path) -> None:
    assert (unit2_dir / "jesc110.pdf").is_file()
    assert (unit2_dir / "ncert_source.json").is_file()


@pytest.fixture
def unit3_dir() -> Path:
    return ROOT / "HarshitPhysics" / "unit3"


def test_unit3_mcq_bank_active(unit3_dir: Path) -> None:
    bank = json.loads((unit3_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    assert len(bank["sessions"]) == 4
    assert sum(len(s["questions"]) for s in bank["sessions"]) == 40


def test_unit3_exercise_bank(unit3_dir: Path) -> None:
    bank = json.loads((unit3_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    qs = bank["questions"]
    assert len(qs) == 14
    assert [q["num"] for q in qs] == list(range(5, 19))


def test_unit3_stage2_and_stage3_helpers() -> None:
    from harshit.physics import content as hpc

    assert hpc.stage2_available(3)
    assert hpc.stage3_available(3)
    assert len(hpc.list_ncert_activities(3)) == 6
    acts = hpc.ncert_activities_for_stage2_day(19, 3)
    assert {a["id"] for a in acts} == {"11.4", "11.5", "11.6"}


def test_unit3_pdf_present(unit3_dir: Path) -> None:
    assert (unit3_dir / "jesc111.pdf").is_file()
    assert (unit3_dir / "ncert_source.json").is_file()


@pytest.fixture
def unit4_dir() -> Path:
    return ROOT / "HarshitPhysics" / "unit4"


def test_unit4_mcq_bank_active(unit4_dir: Path) -> None:
    bank = json.loads((unit4_dir / "mcq_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    assert len(bank["sessions"]) == 4
    assert sum(len(s["questions"]) for s in bank["sessions"]) == 40


def test_unit4_exercise_bank(unit4_dir: Path) -> None:
    bank = json.loads((unit4_dir / "exercise_bank.json").read_text(encoding="utf-8"))
    assert bank["meta"]["active"] is True
    qs = bank["questions"]
    assert len(qs) == 6
    assert [q["num"] for q in qs] == list(range(4, 10))


def test_unit4_stage2_and_stage3_helpers() -> None:
    from harshit.physics import content as hpc

    assert hpc.stage2_available(4)
    assert hpc.stage3_available(4)
    assert len(hpc.list_ncert_activities(4)) == 7
    acts = hpc.ncert_activities_for_stage2_day(17, 4)
    assert {a["id"] for a in acts} == {"12.1", "12.2", "12.3"}


def test_unit4_pdf_present(unit4_dir: Path) -> None:
    assert (unit4_dir / "jesc112.pdf").is_file()
    assert (unit4_dir / "ncert_source.json").is_file()
