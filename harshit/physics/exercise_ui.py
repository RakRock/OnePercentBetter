"""Harshit Physics — Stage 3 NCERT written exercises."""

from __future__ import annotations

import re

import streamlit as st

from . import components as hpco
from . import content as hpc
from . import numerical_ui as hpnum


_TYPE_LABELS = {
    "numerical": "Numerical",
    "numerical_diagram": "Numerical + diagram",
    "numerical_graph": "Graph + numerical",
    "explain": "Explain",
    "explain_diagram": "Explain + diagram",
}


def _ss_key(name: str, unit_id: int) -> str:
    return f"hp_ex_u{unit_id}_{name}"


def _checklist_key(question_id: str, unit_id: int) -> str:
    return f"hp_ex_check_{unit_id}_{question_id}"


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
        from . import state as hps

        st.session_state[key] = hps.ConceptSessionState(day_id=day_id).to_dict()


def _hint_level_key(question_id: str, unit_id: int) -> str:
    return _ss_key(f"hints_{question_id}", unit_id)


def _type_badge(qtype: str) -> str:
    return _TYPE_LABELS.get(qtype, qtype.replace("_", " ").title())


def render_stage3_home(*, stage1_done: bool, unit_id: int = 1) -> None:
    """List NCERT written exercises on the unit home."""
    if not hpc.stage3_available(unit_id):
        st.info("Stage 3 written exercises are not available for this unit yet.")
        return

    bank = hpc.exercise_bank(unit_id)
    ex_range = bank.get("meta", {}).get("range", "written exercises")
    if not stage1_done:
        st.info(
            "Complete all Stage 1 concept days to unlock Stage 3 written practice. "
            f"These are the long-form NCERT exercise questions ({ex_range}) used in board exams."
        )
        return

    questions = hpc.list_exercise_questions(unit_id)
    st.markdown("### Stage 3 — NCERT written (exam-style)")
    st.caption(
        f"{bank.get('meta', {}).get('range', 'Written exercises')} · "
        "Attempt on paper first, then use hints, guided numericals, and model answers."
    )

    numerical_count = sum(1 for q in questions if q.get("guided_tool"))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Questions", len(questions))
    with c2:
        st.metric("With guided numerical", numerical_count)
    with c3:
        done = sum(
            1
            for q in questions
            if st.session_state.get(_checklist_key(q["id"], unit_id), {}).get("done")
        )
        st.metric("Self-marked done", f"{done}/{len(questions)}")

    for q in questions:
        qid = q["id"]
        done = bool(st.session_state.get(_checklist_key(qid, unit_id), {}).get("done"))
        badge = _type_badge(str(q.get("type", "")))
        marks = q.get("marks")
        marks_txt = f" · {marks} marks" if marks else ""
        with st.container(border=True):
            st.markdown(f"**Q{q['num']}** — {badge}{marks_txt}{' · ✓' if done else ''}")
            preview = str(q.get("question", "")).split("\n")[0]
            if len(preview) > 120:
                preview = preview[:117] + "…"
            st.caption(preview)
            if st.button("Open question", key=f"hp_ex_open_{unit_id}_{qid}", type="primary"):
                st.session_state.hp_unit_id = unit_id
                st.session_state.hp_exercise_id = qid
                st.session_state.current_page = "harshit_physics_exercise"
                st.rerun()


def render_exercise_question() -> None:
    unit_id = hpc.active_unit_id()
    umeta = hpc.unit_meta(unit_id)
    hpco.inject_physics_styles(unit_id)
    qid = str(st.session_state.get("hp_exercise_id", ""))
    q = hpc.get_exercise_question(qid, unit_id)
    if not q:
        st.warning("Question not found.")
        if st.button("← Unit home"):
            _open_unit_home(unit_id)
            st.rerun()
        return

    if st.button(f"← Unit {unit_id}"):
        _open_unit_home(unit_id)
        st.rerun()

    st.markdown(f"## Stage 3 · NCERT Q{q['num']}")
    st.caption(f"Unit {unit_id} — {umeta['title']} · {_type_badge(str(q.get('type', '')))}")
    if q.get("ncert_ref"):
        st.caption(f"📖 {q['ncert_ref']}")

    st.info("✏️ **Try this on paper first** — then open hints and compare with the model answer.")

    st.markdown(q["question"])

    hpnum.render_guided_for_question(q)

    hints = list(q.get("hints") or [])
    hint_level = int(st.session_state.get(_hint_level_key(qid, unit_id), 0))
    if hints:
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            if hint_level < len(hints) and st.button(
                f"Show hint {hint_level + 1} of {len(hints)}",
                key=f"hp_ex_hint_{unit_id}_{qid}",
            ):
                st.session_state[_hint_level_key(qid, unit_id)] = hint_level + 1
                st.rerun()
        with col_h2:
            if hint_level > 0 and st.button("Reset hints", key=f"hp_ex_hint_reset_{unit_id}_{qid}"):
                st.session_state[_hint_level_key(qid, unit_id)] = 0
                st.rerun()
        for i in range(hint_level):
            st.markdown(f"**Hint {i + 1}:** {hints[i]}")

    show_answer = st.session_state.get(_ss_key(f"show_answer_{qid}", unit_id), False)
    if st.button(
        "Show model answer" if not show_answer else "Hide model answer",
        key=f"hp_ex_answer_{unit_id}_{qid}",
    ):
        st.session_state[_ss_key(f"show_answer_{qid}", unit_id)] = not show_answer
        st.rerun()

    if show_answer:
        st.markdown("---")
        st.markdown("### Model answer")
        st.markdown(q.get("model_answer", ""))
        mistakes = q.get("common_mistakes") or []
        if mistakes:
            with st.expander("Common mistakes", expanded=False):
                for m in mistakes:
                    st.markdown(f"- {m}")

    marking = list(q.get("marking_points") or [])
    if marking:
        st.markdown("---")
        st.markdown("**Self-mark checklist** (tick what you included in your answer):")
        ck_key = _checklist_key(qid, unit_id)
        if ck_key not in st.session_state:
            st.session_state[ck_key] = {"checks": {}, "done": False}
        state = st.session_state[ck_key]
        checks = state.get("checks") or {}
        for i, point in enumerate(marking):
            cid = f"{qid}_{i}"
            checks[cid] = st.checkbox(point, value=bool(checks.get(cid)), key=f"hp_ex_ck_{unit_id}_{cid}")
        state["checks"] = checks
        state["done"] = all(checks.values()) and len(checks) == len(marking)
        st.session_state[ck_key] = state
        if state["done"]:
            st.success("You checked all marking points — great exam prep!")

    concept_ids = list(q.get("concept_ids") or [])
    if concept_ids:
        st.markdown("---")
        if st.button("Review related concept", key=f"hp_ex_concept_{unit_id}_{qid}"):
            _open_concept_by_id(concept_ids[0], unit_id)
            st.rerun()

    misc = str(q.get("misconception", ""))
    if misc and show_answer:
        machine = hpc.misconception_machine(misc, unit_id)
        if machine and machine.get("feedback"):
            st.markdown("---")
            st.markdown("**If you struggled here**")
            st.info(machine["feedback"])
