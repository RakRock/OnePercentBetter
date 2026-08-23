"""Harshit Physics — Stage 2 structured MCQ sessions (days 17–20)."""

from __future__ import annotations

import re

import streamlit as st

import database as db
from . import components as hpco
from . import content as hpc
from . import state as hps


def _ss_key(name: str, unit_id: int | None = None) -> str:
    uid = unit_id if unit_id is not None else hpc.active_unit_id()
    return f"hp_mcq_u{uid}_{name}"


def _mcq_state_key(day_id: int, unit_id: int) -> str:
    return f"hp_mcq_state_{unit_id}_{day_id}"


def _open_unit_home(unit_id: int) -> None:
    st.session_state.hp_unit_id = unit_id
    st.session_state.current_page = f"harshit_physics_unit{unit_id}"


def _open_concept_by_id(concept_id: str, unit_id: int) -> None:
    m = re.match(r"u\d+_d(\d+)_", concept_id)
    if not m:
        return
    day_id = int(m.group(1))
    st.session_state.hp_unit_id = unit_id
    st.session_state.hp_day_id = day_id
    st.session_state.hp_mode = "concept"
    st.session_state.current_page = "harshit_physics_concept"
    key = f"hp_concept_{unit_id}_{day_id}"
    if key not in st.session_state:
        st.session_state[key] = hps.ConceptSessionState(day_id=day_id).to_dict()


def _get_mcq_state(day_id: int, unit_id: int) -> hps.MCQSessionState:
    key = _mcq_state_key(day_id, unit_id)
    return hps.MCQSessionState.from_dict(st.session_state.get(key, {"day_id": day_id}))


def _save_mcq_state(state: hps.MCQSessionState, unit_id: int) -> None:
    st.session_state[_mcq_state_key(state.day_id, unit_id)] = state.to_dict()


def _render_activities(stage2_day: int, unit_id: int) -> None:
    acts = hpc.ncert_activities_for_stage2_day(stage2_day, unit_id)
    if not acts:
        return
    with st.expander("🔬 NCERT Activities for this session", expanded=False):
        for act in acts:
            st.markdown(f"**Activity {act['id']} — {act.get('title', '')}**")
            st.caption(act.get("summary", ""))


def _activity_label(unit_id: int) -> str:
    acts = hpc.list_ncert_activities(unit_id)
    if not acts:
        return "NCERT Activities"
    ids = [a["id"] for a in acts]
    if len(ids) == 1:
        return f"Activity {ids[0]}"
    return f"Activities {ids[0]}–{ids[-1]}"


def render_stage2_home(*, stage1_done: bool, unit_id: int = 1) -> None:
    """List Stage 2 MCQ days (17–20) on the unit home."""
    if not hpc.stage2_available(unit_id):
        st.info("Stage 2 structured MCQs are not available for this unit yet.")
        return
    if not stage1_done:
        act_label = _activity_label(unit_id)
        st.info(
            "Complete all Stage 1 concept days to unlock Stage 2. "
            f"Stage 2 uses {act_label} and textbook exercise questions."
        )
        return

    st.markdown("### Stage 2 — NCERT check (Activities & exercises)")
    act_label = _activity_label(unit_id)
    st.caption(
        f"10 questions per session · includes NCERT Exercise MCQs and {act_label} · "
        "wrong answers show remediation hints"
    )
    ncert = hpc.ncert_source(unit_id)
    pdf_name = hpc.unit_meta(unit_id).get("pdf") or ncert.get("meta", {}).get("pdf")
    if pdf_name:
        pdf_path = hpc.unit_dir(unit_id) / pdf_name
        if pdf_path.is_file():
            with st.expander("📄 NCERT Chapter 9 PDF (Activities & questions)", expanded=False):
                try:
                    st.pdf(pdf_path)
                except Exception:
                    st.caption(str(pdf_path))

    for session in hpc.list_mcq_sessions(unit_id):
        if not session.get("active", True):
            continue
        questions = session.get("questions") or []
        if not questions:
            continue
        day_id = int(session["day"])
        acts = session.get("activity_refs") or []
        act_label = f" · Activities {', '.join(acts)}" if acts else ""
        ncert_count = sum(1 for q in questions if str(q.get("source", "")).startswith("NCERT"))
        with st.container(border=True):
            st.markdown(f"**Day {day_id} — {session.get('title', '')}**")
            st.caption(f"{len(questions)} MCQs{act_label} · {ncert_count} from NCERT exercises/intext")
            if st.button("Start session", key=f"hp_stage2_start_{unit_id}_{day_id}", type="primary"):
                st.session_state.hp_unit_id = unit_id
                st.session_state.hp_mcq_day_id = day_id
                st.session_state[_ss_key("questions", unit_id)] = questions
                st.session_state[_ss_key("current", unit_id)] = 0
                st.session_state[_ss_key("answers", unit_id)] = []
                st.session_state[_ss_key("remediation", unit_id)] = None
                _save_mcq_state(hps.MCQSessionState(day_id=day_id), unit_id)
                st.session_state.current_page = "harshit_physics_mcq"
                st.rerun()


def render_mcq_session() -> None:
    unit_id = hpc.active_unit_id()
    umeta = hpc.unit_meta(unit_id)
    hpco.inject_physics_styles(unit_id)
    day_id = int(st.session_state.get("hp_mcq_day_id", 17))
    session = hpc.get_mcq_session(day_id, unit_id)
    questions = st.session_state.get(_ss_key("questions", unit_id), [])
    if not questions and session:
        questions = session.get("questions") or []
        st.session_state[_ss_key("questions", unit_id)] = questions

    user = db.get_user("Harshit Sai")
    state = _get_mcq_state(day_id, unit_id)

    if st.button(f"← Unit {unit_id}"):
        st.session_state.current_page = f"harshit_physics_unit{unit_id}"
        st.session_state.pop(_ss_key("questions", unit_id), None)
        st.session_state.pop(_ss_key("remediation", unit_id), None)
        st.rerun()

    title = session.get("title", "") if session else ""
    st.markdown(f"## Stage 2 · Day {day_id} — {title}")
    st.caption(f"Unit {unit_id} — {umeta['title']}")
    _render_activities(day_id, unit_id)

    if not questions:
        st.warning("No questions loaded for this session.")
        return

    remediation = st.session_state.get(_ss_key("remediation", unit_id))
    if remediation:
        _render_remediation(remediation, unit_id, day_id, state)
        return

    current = int(st.session_state.get(_ss_key("current", unit_id), 0))
    total = len(questions)
    if current >= total:
        _render_complete(questions, unit_id, day_id)
        return

    st.progress((current / total) if total else 0, text=f"Question {current + 1} of {total}")
    q = questions[current]
    src = q.get("source", "")
    if src.startswith("NCERT") or q.get("ncert_ref"):
        st.caption(f"📖 {q.get('ncert_ref') or src}")
    elif src == "concept_bank":
        st.caption("From concept question bank (chapter-aligned)")
    st.markdown(f"**{q['question']}**")

    picked = None
    cols = st.columns(2)
    for idx, opt in enumerate(q["options"]):
        with cols[idx % 2]:
            if st.button(str(opt), key=f"hp_mcq_u{unit_id}_d{day_id}_q{current}_{idx}", use_container_width=True):
                picked = idx

    if picked is None:
        return

    correct = picked == int(q["answer"])
    answers = st.session_state.get(_ss_key("answers", unit_id), [])
    answers.append({"picked": picked, "correct": correct, "question_id": q.get("id")})
    st.session_state[_ss_key("answers", unit_id)] = answers

    if user:
        db.save_harshit_physics_mcq_attempt(
            user["id"],
            unit_id=unit_id,
            day_id=day_id,
            question_id=str(q.get("id", "")),
            selected=q["options"][picked],
            correct=correct,
            misconception="" if correct else str(q.get("misconception", "")),
            concept_reviewed=q.get("concept_id", "") if not correct else "",
        )

    if correct:
        st.session_state[_ss_key("current", unit_id)] = current + 1
        st.rerun()

    misc = str(q.get("misconception", ""))
    machine = hpc.misconception_machine(misc, unit_id) if misc else None
    concept_id = q.get("concept_id") or ""
    if machine and machine.get("concept_ids"):
        concept_id = machine["concept_ids"][0]
    st.session_state[_ss_key("remediation", unit_id)] = {
        "question": q,
        "picked": picked,
        "machine": machine,
        "concept_id": concept_id,
    }
    st.rerun()


def _render_remediation(payload: dict, unit_id: int, day_id: int, state: hps.MCQSessionState) -> None:
    q = payload["question"]
    machine = payload.get("machine")
    st.error("Not quite — let's look at this again.")
    if machine:
        st.markdown(machine.get("feedback", ""))
        if machine.get("calm_prompt"):
            st.info(machine["calm_prompt"])
    elif q.get("explanation"):
        st.info(q["explanation"])

    concept_id = payload.get("concept_id") or ""
    if concept_id:
        if st.button("Review related concept", key=f"hp_mcq_review_concept_{unit_id}"):
            _open_concept_by_id(concept_id, unit_id)
            st.session_state.pop(_ss_key("remediation", unit_id), None)
            st.rerun()

    if st.button("Continue to next question →", type="primary", key=f"hp_mcq_continue_{unit_id}"):
        st.session_state.pop(_ss_key("remediation", unit_id), None)
        current = int(st.session_state.get(_ss_key("current", unit_id), 0))
        st.session_state[_ss_key("current", unit_id)] = current + 1
        st.rerun()


def _render_complete(questions: list[dict], unit_id: int, day_id: int) -> None:
    answers = st.session_state.get(_ss_key("answers", unit_id), [])
    correct = sum(1 for a in answers if a.get("correct"))
    total = len(questions)
    st.success(f"Session complete — {correct}/{total} correct.")
    if st.button("Back to Unit home", type="primary"):
        _open_unit_home(unit_id)
        st.session_state.pop(_ss_key("questions", unit_id), None)
        st.session_state.pop(_ss_key("answers", unit_id), None)
        st.session_state.pop(_ss_key("current", unit_id), None)
        st.rerun()
