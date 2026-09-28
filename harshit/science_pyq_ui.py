"""Streamlit controls for science previous-year short answers."""

from __future__ import annotations

import streamlit as st


def is_short_answer(q: dict) -> bool:
    return q.get("type") == "short_answer"


def render_model_answer(q: dict) -> None:
    model = str(q.get("model_answer") or q.get("explanation") or "").strip()
    if not model:
        return
    st.markdown("**Model answer**")
    st.markdown(model)


def render_short_answer_choice(q: dict, *, key: str) -> str | None:
    """Return 'got_it', 'review', or None while the student is still working."""
    st.caption("Previous-year question. Solve it, open the model answer, then mark yourself.")
    with st.expander("Model answer", expanded=False):
        render_model_answer(q)
    got, review = st.columns(2)
    with got:
        if st.button("I got it", key=f"{key}_got", use_container_width=True):
            return "got_it"
    with review:
        if st.button("Need to review", key=f"{key}_review", use_container_width=True):
            return "review"
    return None


def short_answer_record(q: dict, verdict: str) -> dict:
    correct = verdict == "got_it"
    model = str(q.get("model_answer") or "")
    return {
        "picked": "I got it" if correct else "Need to review",
        "correct": correct,
        "correct_val": model[:500],
        "concept_id": q.get("concept_id", ""),
        "category": q.get("category_label", ""),
    }
