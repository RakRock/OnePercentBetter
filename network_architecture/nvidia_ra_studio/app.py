"""
NVIDIA AI Enterprise RA Learning Studio — standalone entry point.

Run from this directory:
    streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from core.progress_store import ProgressStore
from core.llm_client import get_anthropic_api_key, llm_available
from ui.session import init_session, inject_styles, nav_sidebar, profile_selector
from pages import (
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

st.set_page_config(
    page_title="NVIDIA AI Enterprise RA Learning Studio",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()
if get_anthropic_api_key():
    st.sidebar.success("Claude connected")
else:
    st.sidebar.caption("Set ANTHROPIC_API_KEY in ~/.zshrc or secrets")
store = ProgressStore()
store, user_id, profile = init_session(store)
profile_selector(store)
page = nav_sidebar()
PAGES.get(page, dashboard.render)(store, user_id, profile)
