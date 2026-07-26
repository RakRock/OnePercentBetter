"""Agent coach chat panel."""

from __future__ import annotations

import streamlit as st

from core.content_catalog import MODULES
from core.llm_client import llm_available
from core.planner_agent import COACH_SYSTEM_PROMPT, coach_reply
from core.rag_sources import OFFICIAL_DOCS


def _build_context() -> str:
    lines = ["Official docs:"] + [f"{k}: {v}" for k, v in OFFICIAL_DOCS.items()]
    lines.append("\nModules:")
    for m in MODULES[:6]:
        lines.append(f"- {m.title}: {m.concept[:200]}")
    return "\n".join(lines)


def render(store, user_id: int, profile: str) -> None:
    st.header("🤖 Agent Coach")
    if llm_available():
        st.caption("Claude coaching enabled (ANTHROPIC_API_KEY)")
    else:
        st.caption("Offline mode — set ANTHROPIC_API_KEY in ~/.zshrc or Streamlit secrets")

    if "nra_chat" not in st.session_state:
        st.session_state.nra_chat = []

    for msg in st.session_state.nra_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask about NVIDIA AI Enterprise RA…")
    if prompt:
        st.session_state.nra_chat.append({"role": "user", "content": prompt})
        reply = coach_reply(prompt, _build_context(), history=st.session_state.nra_chat[:-1])
        st.session_state.nra_chat.append({"role": "assistant", "content": reply})
        st.rerun()

    with st.expander("Coach system prompt"):
        st.code(COACH_SYSTEM_PROMPT)

    if st.button("Clear chat"):
        st.session_state.nra_chat = []
        st.rerun()
