"""Quiz engine UI."""

from __future__ import annotations

import streamlit as st

from core.content_catalog import MODULES
from core.quiz_engine import (
    QUIZ_BANK,
    final_assessment_questions,
    grade_answer,
    questions_for_module,
    score_quiz,
)


def _render_question(q, prefix: str) -> list[int]:
    if q.qtype == "multi":
        picked = st.multiselect(q.prompt, list(range(len(q.choices))), format_func=lambda i: q.choices[i], key=f"{prefix}_{q.id}")
        return picked
    picked = st.radio(
        q.prompt,
        list(range(len(q.choices))),
        format_func=lambda i: q.choices[i],
        key=f"{prefix}_{q.id}",
        index=None,
    )
    return [picked] if picked is not None else []


def render(store, user_id: int, profile: str) -> None:
    st.header("✅ Quizzes")

    mode = st.radio("Mode", ["Module quiz", "Final assessment (50 questions)"], horizontal=True)

    if mode.startswith("Module"):
        mod_id = st.selectbox("Module", [m.id for m in MODULES], format_func=lambda i: next(m.title for m in MODULES if m.id == i))
        questions = questions_for_module(mod_id)[:10]
        quiz_id = f"module-{mod_id}"
    else:
        questions = final_assessment_questions(50)
        quiz_id = "final-50"

    st.caption(f"{len(questions)} questions · {len(QUIZ_BANK)} total in bank")

    answers: dict[str, list[int]] = {}
    with st.form("quiz_form"):
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}.** [{q.qtype}]")
            answers[q.id] = _render_question(q, "quiz")
        submit = st.form_submit_button("Submit quiz", type="primary")

    if submit:
        correct, total = score_quiz(questions, answers)
        pct = round(correct / total * 100, 1) if total else 0
        store.record_quiz_attempt(user_id, quiz_id, correct, total, answers)
        st.success(f"Score: {correct}/{total} ({pct}%)")
        with st.expander("Review answers"):
            for q in questions:
                ok = grade_answer(q, answers.get(q.id, []))
                icon = "✅" if ok else "❌"
                st.markdown(f"{icon} {q.prompt}")
                st.caption(q.explanation)

    if st.button("Retry incorrect only (last module quiz)"):
        st.info("Complete a quiz first — incorrect-only retry uses your last submission.")
