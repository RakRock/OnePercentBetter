"""Streamlit UI for AI Forge (embedded in OnePercent)."""

from __future__ import annotations

import streamlit as st

import ai_forge_content as af


def _init_state():
    if "af_chat" not in st.session_state:
        st.session_state.af_chat = []
    if "af_personality" not in st.session_state:
        st.session_state.af_personality = "teacher"
    if "af_project_slug" not in st.session_state:
        st.session_state.af_project_slug = None
    if "af_completed" not in st.session_state:
        st.session_state.af_completed = {}


def render_home(anthropic_key: str | None, live_mentor: bool):
    _init_state()
    name = st.session_state.selected_user

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="aiforge_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(
        f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">⚒️ {name}'s AI Forge</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">
            Build real AI systems — RAG, agents, deployment — with a Claude mentor
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if live_mentor:
        st.success("Claude mentor is connected.")
    else:
        st.info(
            "Demo mode: add `ANTHROPIC_API_KEY` to `.streamlit/secrets.toml` on Streamlit Cloud "
            "for live mentor replies."
        )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            """
            <div class="score-card" style="border-top: 5px solid #8b5cf6;">
                <div style="font-size: 3rem;">🧠</div>
                <h3 style="margin: 0.5rem 0;">AI Mentor</h3>
                <p style="color: #6b7280;">Socratic hints — teacher, architect, debugger</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🧠 Open Mentor", key="af_btn_mentor", width="stretch", type="primary"):
            st.session_state.current_page = "ai_forge_mentor"
            st.rerun()
    with c2:
        st.markdown(
            """
            <div class="score-card" style="border-top: 5px solid #06b6d4;">
                <div style="font-size: 3rem;">🧪</div>
                <h3 style="margin: 0.5rem 0;">Project Labs</h3>
                <p style="color: #6b7280;">Hands-on milestones & scaffolding</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🧪 Browse Projects", key="af_btn_projects", width="stretch", type="primary"):
            st.session_state.current_page = "ai_forge_projects"
            st.rerun()

    st.markdown("#### Featured lab")
    proj = af.PROJECTS[0]
    st.markdown(f"**{proj['title']}** — {proj['summary']}")
    if st.button(f"▶️ Start {proj['title']}", key="af_feat_proj", width="stretch"):
        st.session_state.af_project_slug = proj["slug"]
        st.session_state.current_page = "ai_forge_project"
        st.rerun()


def render_mentor(anthropic_key: str | None):
    _init_state()
    name = st.session_state.selected_user
    project = (
        af.get_project(st.session_state.af_project_slug)
        if st.session_state.af_project_slug
        else None
    )

    col_nav1, col_nav2, _ = st.columns([1, 1, 5])
    with col_nav1:
        if st.button("← Forge", key="af_mentor_back"):
            st.session_state.current_page = "ai_forge_home"
            st.rerun()
    with col_nav2:
        if st.button("Clear chat", key="af_mentor_clear"):
            st.session_state.af_chat = []
            st.rerun()

    st.markdown("### 🧠 AI Mentor")
    if project:
        st.caption(f"Project context: **{project['title']}**")

    personality = st.selectbox(
        "Mentor mode",
        af.PERSONALITIES,
        index=af.PERSONALITIES.index(st.session_state.af_personality),
        format_func=lambda p: p.title(),
        key="af_personality_select",
    )
    st.session_state.af_personality = personality

    for msg in st.session_state.af_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("What are you stuck on?")
    if prompt:
        st.session_state.af_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("Thinking…"):
            reply = af.mentor_chat(
                anthropic_key,
                prompt,
                personality=personality,
                history=st.session_state.af_chat[:-1],
                project=project,
                user_name=name,
            )
        st.session_state.af_chat.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.rerun()


def render_projects():
    _init_state()

    if st.button("← Back to Forge", key="af_proj_list_back"):
        st.session_state.current_page = "ai_forge_home"
        st.rerun()

    st.markdown("### 🧪 Project Labs")
    for proj in af.PROJECTS:
        st.markdown(f"#### {proj['title']}")
        st.caption(f"{proj['difficulty'].title()} · {', '.join(proj['stack'])}")
        st.write(proj["summary"])
        if st.button("Open lab →", key=f"af_open_{proj['slug']}"):
            st.session_state.af_project_slug = proj["slug"]
            st.session_state.current_page = "ai_forge_project"
            st.rerun()
        st.markdown("---")


def render_project():
    _init_state()
    slug = st.session_state.af_project_slug or "rag-assistant"
    proj = af.get_project(slug)
    if not proj:
        st.error("Project not found.")
        if st.button("← Back", key="af_proj_nf_back"):
            st.session_state.current_page = "ai_forge_projects"
            st.rerun()
        return

    completed = st.session_state.af_completed.get(slug, [])

    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        if st.button("← Labs", key="af_proj_back"):
            st.session_state.current_page = "ai_forge_projects"
            st.rerun()
    with c2:
        if st.button("🧠 Ask mentor", key="af_proj_mentor"):
            st.session_state.current_page = "ai_forge_mentor"
            st.rerun()

    st.markdown(f"### {proj['title']}")
    st.write(proj["summary"])
    st.progress(len(completed) / max(len(proj["checkpoints"]), 1))

    with st.expander("📖 Concept", expanded=False):
        st.write(proj["concept"])
    with st.expander("🏗️ Architecture", expanded=False):
        st.code(proj["architecture_mermaid"], language=None)

    st.markdown("#### Milestones")
    for i, cp in enumerate(proj["checkpoints"]):
        done = i in completed
        icon = "✅" if done else "⬜"
        st.markdown(f"{icon} **{cp['title']}**")
        st.caption(cp["description"])
        for t in cp["tasks"]:
            st.markdown(f"- {t}")
        if not done and st.button("Mark complete", key=f"af_cp_done_{slug}_{i}"):
            completed = list(completed)
            if i not in completed:
                completed.append(i)
            st.session_state.af_completed[slug] = sorted(completed)
            st.rerun()
        st.markdown("")

    with st.expander("📁 Scaffold files", expanded=False):
        for fname, body in proj.get("scaffold", {}).items():
            st.markdown(f"**{fname}**")
            st.code(body, language="markdown")
