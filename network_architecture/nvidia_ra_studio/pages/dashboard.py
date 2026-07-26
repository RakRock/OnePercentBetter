"""Dashboard — progress overview and continue learning."""

from __future__ import annotations

import streamlit as st

from core.content_catalog import MODULES
from core.quiz_engine import QUIZ_BANK
from ui.session import inject_styles


def render(store, user_id: int, profile: str) -> None:
    inject_styles()
    stats = store.dashboard_summary(user_id, len(MODULES))
    prog = store.get_module_progress(user_id)

    st.markdown(
        f"""
        <div class="studio-hero">
            <h1 style="margin:0;">NVIDIA AI Enterprise RA Learning Studio</h1>
            <p style="margin:0.5rem 0 0 0; opacity:0.9;">Profile: {profile} · {len(QUIZ_BANK)} quiz questions · {len(MODULES)} modules</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Progress", f"{stats['progress_pct']}%")
    c2.metric("Modules done", f"{stats['modules_completed']}/{stats['modules_total']}")
    c3.metric("Quiz average", f"{stats['quiz_average_pct']}%")
    c4.metric("Drills done", stats["drills_completed"])

    st.progress(stats["progress_pct"] / 100)

    # Recommended next lesson
    next_mod = next((m for m in MODULES if not prog.get(m.id, {}).get("completed")), MODULES[0])
    st.markdown("### ▶️ Continue learning")
    st.info(f"**Next up:** {next_mod.title} ({next_mod.difficulty}, ~{next_mod.minutes} min)")
    if st.button("Open module", key="dash_continue"):
        st.session_state.nra_selected_module = next_mod.id
        st.session_state.nra_page = "modules"
        st.rerun()

    st.markdown("### 📌 Weak areas (study more)")
    incomplete = [m.domain for m in MODULES if not prog.get(m.id, {}).get("completed")]
    for d in incomplete[:3]:
        st.markdown(f"- {d}")

    st.markdown("### 🔥 Study streak")
    st.caption("Placeholder — log in daily to build your streak in a future release.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate learning path", use_container_width=True):
            st.session_state.nra_page = "learning_path"
            st.rerun()
    with col2:
        if st.button("Architecture map", use_container_width=True):
            st.session_state.nra_page = "architecture_map"
            st.rerun()
