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
