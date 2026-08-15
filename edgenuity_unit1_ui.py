"""Enhanced Unit 1 hub — learning path, activity cards, and focused practice."""

from __future__ import annotations

import streamlit as st

import arjun_edgenuity_course3_content as ec3
import arjun_edgenuity_course3_practice as ec3p
import database as db

FOCUS_QUESTION_COUNT = 8

# Maps each activity to its practice category and a kid-friendly one-liner.
ACTIVITY_GUIDE: list[dict] = [
    {
        "number": 1,
        "slug": "activity_1_coordinate_plane",
        "category": "coordinate_plane",
        "emoji": "📍",
        "title": "Coordinate Plane",
        "blurb": "Read (x, y) points, name quadrants, and spot points on the axes.",
        "exam_tip": "Always write x first, then y.",
    },
    {
        "number": 2,
        "slug": "activity_2_relations_functions",
        "category": "function_definition",
        "emoji": "🔀",
        "title": "Relations & Functions",
        "blurb": "Decide if a table or graph is a function — one input, one output.",
        "exam_tip": "Same x with two different y values → not a function.",
    },
    {
        "number": 3,
        "slug": "activity_3_graph_behavior",
        "category": "graph_behavior",
        "emoji": "📈",
        "title": "Graph Behavior",
        "blurb": "Describe graphs as increasing, decreasing, or flat (constant).",
        "exam_tip": "Read the graph left to right like a story over time.",
    },
    {
        "number": 4,
        "slug": "activity_4_linear_equations",
        "category": "linear_equations",
        "emoji": "📊",
        "title": "Linear Equations",
        "blurb": "Find unit rates and write equations like y = mx + b from tables or graphs.",
        "exam_tip": "Divide change in y by change in x to find the rate.",
    },
    {
        "number": 5,
        "slug": "activity_5_completing_tables",
        "category": "table_completion",
        "emoji": "📋",
        "title": "Completing Tables",
        "blurb": "Plug values into equations and match tables to graphs.",
        "exam_tip": "Substitute carefully — one wrong number breaks the whole row.",
    },
    {
        "number": 6,
        "slug": "activity_6_word_problems",
        "category": "word_problems",
        "emoji": "🌍",
        "title": "Word Problems",
        "blurb": "Compare two plans, solve “at least” problems, and work backward.",
        "exam_tip": "Write two equations first, then compare or solve.",
    },
]


def activity_for_category(category: str) -> dict | None:
    for item in ACTIVITY_GUIDE:
        if item["category"] == category:
            return item
    return None


def _last_unit_score(user_id: int | None) -> int | None:
    if not user_id:
        return None
    rows = db.get_scores_history(user_id, activity_type="EdgenuityCourse3", days=60)
    for row in rows:
        name = str(row.get("activity_name") or "")
        if "Unit 1" in name:
            try:
                return int(row.get("score", 0))
            except (TypeError, ValueError):
                return None
    return None


def render_unit1_hub(
    unit: dict,
    *,
    week_cfg: dict,
    xai_configured: bool,
    on_open_notes,
    on_start_full_practice,
    on_start_focus_practice,
) -> None:
    """Rich Unit 1 landing page (notes + practice modes)."""
    user = db.get_user(st.session_state.selected_user) if st.session_state.get("selected_user") else None
    last_score = _last_unit_score(user["id"] if user else None)

    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#eef2ff 0%,#f5f3ff 100%);
             border-radius:16px;padding:1.25rem 1.5rem;margin-bottom:1rem;border:1px solid #e0e7ff;">
            <h2 style="margin:0;color:#4338ca;">{unit['title']}: {unit.get('subtitle', '')}</h2>
            <p style="color:#4b5563;margin:0.5rem 0 0 0;">
                Six activities build the skills Edgenuity tests on this unit — coordinates, functions,
                graph behavior, equations, tables, and real-world problems.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stat_cols = st.columns(3)
    with stat_cols[0]:
        st.metric("Activities", "6", help="Lesson notes with diagrams and worked examples")
    with stat_cols[1]:
        st.metric("Exam-style practice", "15 Q", help="Full unit mix, or 8 questions per topic")
    with stat_cols[2]:
        if last_score is not None:
            st.metric("Last full practice", f"{last_score}%")
        else:
            st.metric("Last full practice", "—", help="Complete a practice set to track progress")

    if week_cfg.get("use_llm"):
        if xai_configured:
            st.info(
                "🤖 **AI mode is ON** (Week Setup) — each practice start generates **fresh questions** via xAI Grok. "
                "Turn off in **Week Setup** to use graph-heavy questions from the built-in bank."
            )
        else:
            st.warning(
                "AI mode is ON in Week Setup but **XAI_API_KEY** is missing — practice will use the built-in bank."
            )

    top_cols = st.columns([1, 1, 2])
    with top_cols[0]:
        if unit.get("combined_notes") and unit["combined_notes"].is_file():
            if st.button("📋 Unit overview", key="u1_overview", use_container_width=True):
                on_open_notes(None)
    with top_cols[1]:
        if unit["pdf"].is_file():
            with open(unit["pdf"], "rb") as f:
                st.download_button(
                    "📄 Exam PDF",
                    data=f.read(),
                    file_name=unit["pdf"].name,
                    mime="application/pdf",
                    key="u1_exam_pdf",
                    use_container_width=True,
                )

    st.markdown("### 📝 Practice this unit")
    practice_cols = st.columns([2, 1])
    with practice_cols[0]:
        if week_cfg.get("use_llm") and xai_configured:
            st.caption("Starts a **new AI-generated** 15-question mixed review across all six topics.")
        else:
            st.caption(
                "15 questions with **at least 9 graphs/diagrams** — matches Edgenuity exam format. "
                "Enable AI in Week Setup for fresh questions each time."
            )
    with practice_cols[1]:
        if st.button("🎯 Full unit practice (15)", key="u1_full_practice", type="primary", use_container_width=True):
            on_start_full_practice()

    st.markdown("---")
    st.markdown("### 📚 Learning path — pick an activity")
    st.caption("Read the lesson notes first, then drill that topic with a short quiz.")

    row_pairs = [ACTIVITY_GUIDE[i : i + 2] for i in range(0, len(ACTIVITY_GUIDE), 2)]
    for pair in row_pairs:
        cols = st.columns(2, gap="medium")
        for col, guide in zip(cols, pair, strict=False):
            with col:
                st.markdown(
                    f"""
                    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;
                         padding:1rem 1.1rem;min-height:168px;border-top:4px solid #6366f1;">
                        <div style="font-size:1.6rem;">{guide['emoji']}</div>
                        <strong>Activity {guide['number']}: {guide['title']}</strong>
                        <p style="color:#6b7280;font-size:0.9rem;margin:0.4rem 0;">{guide['blurb']}</p>
                        <p style="color:#4338ca;font-size:0.82rem;margin:0;">💡 {guide['exam_tip']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                btn1, btn2 = st.columns(2)
                with btn1:
                    if st.button("📘 Notes", key=f"u1_notes_{guide['slug']}", use_container_width=True):
                        on_open_notes(guide["slug"])
                with btn2:
                    if st.button(
                        f"🎯 Quiz ({FOCUS_QUESTION_COUNT})",
                        key=f"u1_focus_{guide['category']}",
                        use_container_width=True,
                    ):
                        on_start_focus_practice(guide["category"], guide["title"])


def render_activity_nav(unit_id: int, current_slug: str | None, on_select) -> None:
    """Quick activity picker on Unit 1 notes pages."""
    if unit_id != 1:
        return
    st.markdown("**Activities**")
    nav_cols = st.columns(6)
    for col, guide in zip(nav_cols, ACTIVITY_GUIDE, strict=False):
        with col:
            active = guide["slug"] == current_slug
            if st.button(
                f"{guide['emoji']} {guide['number']}",
                key=f"u1_nav_{guide['slug']}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):
                on_select(guide["slug"])


def render_notes_footer(unit_id: int, activity_slug: str | None, on_focus_practice) -> None:
    """Practice-this-topic call-to-action after activity notes."""
    if unit_id != 1 or not activity_slug:
        return
    guide = next((g for g in ACTIVITY_GUIDE if g["slug"] == activity_slug), None)
    if not guide:
        return
    st.markdown("---")
    st.markdown(f"#### 🎯 Ready to try it?")
    st.caption(f"Short {FOCUS_QUESTION_COUNT}-question quiz on **{guide['title']}** only.")
    if st.button(
        f"Start {guide['title']} quiz",
        key=f"u1_notes_quiz_{guide['category']}",
        type="primary",
        use_container_width=True,
    ):
        on_focus_practice(guide["category"], guide["title"])
