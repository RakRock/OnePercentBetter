"""Module viewer with notes and completion."""

from __future__ import annotations

import streamlit as st

from core.content_catalog import MODULES, get_module
from core.rag_sources import doc_url


def render(store, user_id: int, profile: str) -> None:
    st.header("📚 Modules")

    mod_id = st.session_state.get("nra_selected_module", MODULES[0].id)
    mod_id = st.selectbox(
        "Select module",
        [m.id for m in MODULES],
        index=[m.id for m in MODULES].index(mod_id),
        format_func=lambda i: next(m.title for m in MODULES if m.id == i),
    )
    m = get_module(mod_id)
    if not m:
        st.warning("Module not found.")
        return

    prog = store.get_module_progress(user_id).get(m.id, {})
    st.markdown(f"### {m.title}")
    st.caption(f"{m.domain} · {m.difficulty} · ~{m.minutes} min")

    tab1, tab2, tab3, tab4 = st.tabs(["Concept", "Architecture", "Practice", "Notes"])

    with tab1:
        st.markdown(m.concept)
        st.markdown("#### Why it matters")
        st.info(m.why_it_matters)
        st.markdown("#### Key terms")
        st.write(", ".join(f"`{t}`" for t in m.key_terms))

    with tab2:
        st.code(m.diagram_text)
        st.markdown("#### Official reading")
        for k in m.doc_keys:
            st.markdown(f"- [{k}]({doc_url(k)})")

    with tab3:
        st.markdown("#### Hands-on exercise")
        st.write(m.hands_on)
        st.markdown("#### Design / interview questions")
        for q in m.interview_questions:
            st.write(f"- {q}")

    with tab4:
        notes = st.text_area("Personal notes", value=prog.get("notes", ""), height=120)
        done = st.checkbox("Mark complete", value=prog.get("completed", False))
        if st.button("Save", type="primary"):
            store.set_module_completed(user_id, m.id, done, notes)
            st.success("Saved.")
