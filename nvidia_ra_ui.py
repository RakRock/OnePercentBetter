"""Streamlit UI — Network Architecture hub and NVIDIA RA Learning Studio (Rakesh)."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

STUDIO_ROOT = Path(__file__).resolve().parent / "network_architecture" / "nvidia_ra_studio"
if str(STUDIO_ROOT) not in sys.path:
    sys.path.insert(0, str(STUDIO_ROOT))

from core.progress_store import ProgressStore  # noqa: E402
from ui.session import init_session, inject_styles, nav_sidebar, profile_selector  # noqa: E402
from pages import (  # noqa: E402
    agent_coach,
    architecture_map,
    dashboard,
    design_drills,
    learning_path,
    module_viewer,
    progress_page,
    quizzes,
)

PAGES = {
    "dashboard": dashboard.render,
    "learning_path": learning_path.render,
    "architecture_map": architecture_map.render,
    "modules": module_viewer.render,
    "quizzes": quizzes.render,
    "design_drills": design_drills.render,
    "agent_coach": agent_coach.render,
    "progress": progress_page.render,
}


def _back_to_dash():
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_activity = None
    st.rerun()


def _back_to_network_hub():
    st.session_state.current_page = "network_arch_home"
    st.rerun()


def render_network_arch_home():
    """Network Architecture — pick a reference architecture."""
    name = st.session_state.selected_user
    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="netarch_back_dash"):
            _back_to_dash()

    st.markdown(
        f"""
        <div style="text-align:center;padding:0.5rem 0 1rem 0;">
            <h1 style="font-size:2.5rem;">🌐 {name}'s Network Architecture</h1>
            <p style="color:#6b7280;">Reference architectures for enterprise platforms</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="score-card" style="border-top:5px solid #76b900;">
            <div style="font-size:3rem;">🟢</div>
            <h3 style="margin:0.5rem 0;">NVDA Reference Architecture</h3>
            <p style="color:#6b7280;">
                NVIDIA AI Enterprise RA — modules, quizzes, architecture map, design drills, and AI coach
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🟢 Open NVIDIA AI Enterprise RA Studio", key="open_nvda_ra", type="primary", use_container_width=True):
        st.session_state.current_page = "nvidia_ra_studio"
        st.session_state.nra_page = "dashboard"
        st.rerun()

    st.caption("More reference architectures can be added here (e.g. cloud landing zones, zero-trust networking).")


def render_nvidia_ra_studio(anthropic_key: str | None = None):
    """Full learning studio embedded in OnePercent."""
    from core.llm_client import get_anthropic_api_key, llm_available

    if anthropic_key:
        st.session_state.nra_anthropic_key = anthropic_key
    col_nav1, col_nav2, _ = st.columns([1, 1, 5])
    with col_nav1:
        if st.button("← Network Architecture", key="nra_back_hub"):
            _back_to_network_hub()
    with col_nav2:
        if st.button("← Dashboard", key="nra_back_dash"):
            _back_to_dash()

    inject_styles()
    store = ProgressStore()
    store, user_id, profile = init_session(store)
    if st.session_state.nra_profile == "default" and st.session_state.selected_user:
        st.session_state.nra_profile = st.session_state.selected_user
        user_id = store.get_or_create_user(st.session_state.nra_profile)
    profile_selector(store)

    page = nav_sidebar()
    PAGES.get(page, dashboard.render)(store, user_id, st.session_state.nra_profile)

    if llm_available():
        st.sidebar.success("Claude connected")
    else:
        st.sidebar.caption("Add ANTHROPIC_API_KEY to ~/.zshrc or secrets for Claude")
