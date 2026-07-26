"""Shared UI styles and session helpers."""

from __future__ import annotations

import streamlit as st

from core.progress_store import ProgressStore

STUDIO_CSS = """
<style>
.studio-hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #76b900 120%);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}
.studio-card {
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    background: #fafafa;
    margin-bottom: 0.75rem;
}
.studio-badge {
    display: inline-block;
    background: #76b900;
    color: #0f172a;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
}
</style>
"""


def inject_styles() -> None:
    st.markdown(STUDIO_CSS, unsafe_allow_html=True)


def init_session(store: ProgressStore | None = None) -> tuple[ProgressStore, int, str]:
    if "nra_page" not in st.session_state:
        st.session_state.nra_page = "dashboard"
    if "nra_profile" not in st.session_state:
        st.session_state.nra_profile = "default"
    if store is None:
        store = ProgressStore()
    uid = store.get_or_create_user(st.session_state.nra_profile)
    return store, uid, st.session_state.nra_profile


def profile_selector(store: ProgressStore) -> str:
    if "nra_profile" not in st.session_state:
        st.session_state.nra_profile = "default"
    profiles = store.list_profiles() or ["default"]
    if st.session_state.nra_profile not in profiles:
        profiles = [st.session_state.nra_profile] + profiles
    choice = st.sidebar.selectbox("Profile", profiles, key="nra_profile_select")
    if choice != st.session_state.nra_profile:
        st.session_state.nra_profile = choice
        store.get_or_create_user(choice)
    new = st.sidebar.text_input("New profile name")
    if st.sidebar.button("Add profile") and new.strip():
        st.session_state.nra_profile = new.strip()
        store.get_or_create_user(new.strip())
        st.rerun()
    return st.session_state.nra_profile


def nav_sidebar() -> str:
    st.sidebar.markdown("### 🎓 Learning Studio")
    pages = {
        "dashboard": "📊 Dashboard",
        "learning_path": "🗺️ Learning Path",
        "architecture_map": "🏗️ Architecture Map",
        "modules": "📚 Modules",
        "quizzes": "✅ Quizzes",
        "design_drills": "🔧 Design Drills",
        "agent_coach": "🤖 Agent Coach",
        "progress": "📈 Progress & Export",
    }
    for key, label in pages.items():
        if st.sidebar.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.nra_page = key
            st.rerun()
    return st.session_state.nra_page
