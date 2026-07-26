"""Learning path generator."""

from __future__ import annotations

import streamlit as st

from core.llm_client import get_anthropic_api_key, llm_available
from core.models import LEVELS, ROLES, GOALS, TIMEFRAMES_WEEKS, LearningPlanInput
from core.planner_agent import generate_plan


def render(store, user_id: int, profile: str) -> None:
    st.header("🗺️ Learning Path Generator")
    if llm_available():
        st.caption("Claude-powered plan generation (ANTHROPIC_API_KEY)")
    else:
        st.caption("Template plan — set ANTHROPIC_API_KEY in ~/.zshrc or Streamlit secrets for Claude plans")

    with st.form("plan_form"):
        c1, c2 = st.columns(2)
        with c1:
            role = st.selectbox("Role", ROLES)
            level = st.selectbox("Level", LEVELS)
            goal = st.selectbox("Goal", GOALS)
        with c2:
            weeks = st.selectbox("Timeframe (weeks)", TIMEFRAMES_WEEKS)
            hours = st.slider("Hours per week", 2, 20, 6)
        focus = st.multiselect(
            "Focus areas",
            [
                "GPU Operator",
                "NIM",
                "NeMo",
                "RAG",
                "KServe",
                "Network Operator",
                "Lifecycle",
                "Security",
                "Observability",
            ],
        )
        skills = st.text_input("Existing skills (comma-separated)", "Kubernetes, Linux")
        constraints = st.text_area("Constraints", "Lab cluster only; no production access")
        submitted = st.form_submit_button("Generate plan", type="primary")

    if submitted:
        inp = LearningPlanInput(
            role=role,
            level=level,
            goal=goal,
            weeks=int(weeks),
            hours_per_week=hours,
            focus_areas=focus,
            existing_skills=[s.strip() for s in skills.split(",") if s.strip()],
            constraints=constraints,
        )
        plan = generate_plan(profile, inp, api_key=get_anthropic_api_key())
        store.save_plan(user_id, {"weeks": plan.weeks, "input": inp.__dict__}, plan.markdown)
        st.session_state.nra_last_plan_md = plan.markdown
        st.success("Plan generated!")

    if md := st.session_state.get("nra_last_plan_md"):
        st.markdown(md)
        st.download_button(
            "Download plan (Markdown)",
            md,
            file_name=f"nvidia-ra-plan-{profile}.md",
            mime="text/markdown",
        )
    elif latest := store.latest_plan(user_id):
        st.markdown(latest["markdown"])
