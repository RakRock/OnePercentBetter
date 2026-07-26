"""Design drills — system design for NVIDIA RA."""

from __future__ import annotations

import streamlit as st

from core.design_drills import DESIGN_DRILLS, get_drill


def render(store, user_id: int, profile: str) -> None:
    st.header("🔧 Design Drills")

    drill_id = st.selectbox(
        "Select drill",
        [d.id for d in DESIGN_DRILLS],
        format_func=lambda i: next(d.title for d in DESIGN_DRILLS if d.id == i),
    )
    d = get_drill(drill_id)
    if not d:
        return

    st.markdown(f"### {d.title}")
    st.caption(f"Difficulty: {d.difficulty}")

    tab_req, tab_work, tab_answer = st.tabs(["Requirements", "Your work", "Sample answer"])

    with tab_req:
        st.markdown("#### Requirements")
        for r in d.requirements:
            st.write(f"- {r}")
        st.markdown("#### Clarifying questions")
        for q in d.clarifying_questions:
            st.write(f"- {q}")
        st.markdown("#### Evaluation rubric")
        for r in d.rubric:
            st.write(f"- {r}")

    with tab_work:
        st.text_area("Your architecture (markdown)", height=200, key=f"drill_work_{d.id}")
        if st.button("Mark drill complete"):
            store.set_drill_completed(user_id, d.id, True, st.session_state.get(f"drill_work_{d.id}", ""))
            st.success("Marked complete.")

    with tab_answer:
        st.markdown("#### High-level architecture")
        st.write(d.architecture_outline)
        st.markdown("#### Components")
        st.write(", ".join(d.components))
        st.markdown("#### Tradeoffs")
        for t in d.tradeoffs:
            st.write(f"- {t}")
        st.markdown("#### Failure modes")
        for f in d.failure_modes:
            st.write(f"- {f}")
        with st.expander("Sample answer"):
            st.write(d.sample_answer)
