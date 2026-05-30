"""Streamlit UI for Arjun Course 3 Math lesson notes."""

from __future__ import annotations

import streamlit as st

import arjun_course3_content as c3
import arjun_course3_render as c3r


def _back_dashboard():
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_activity = None


def _open_unit(unit_id: int):
    st.session_state.c3_unit_id = unit_id
    st.session_state.c3_activity_slug = None
    st.session_state.current_page = "course3_unit"


def _open_notes(unit_id: int, activity_slug: str | None = None):
    st.session_state.c3_unit_id = unit_id
    st.session_state.c3_activity_slug = activity_slug
    st.session_state.current_page = "course3_notes"


def render_home():
    """Course 3 landing — pick Unit 1 through Unit 6."""
    name = st.session_state.selected_user
    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="c3_back_dash"):
            _back_dashboard()
            st.rerun()

    st.markdown(
        f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">📐 {name}'s Course 3 Math</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Choose a unit to review</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    row1 = st.columns(3, gap="large")
    row2 = st.columns(3, gap="large")
    for col, unit in zip(row1 + row2, c3.list_units()):
        with col:
            ready = c3.unit_notes_ready(unit)
            has_pdf = unit["pdf"].is_file()
            badge = "✅ Notes ready" if ready else ("📄 PDF only" if has_pdf else "🔜 Coming soon")
            border = "#14b8a6" if ready else "#94a3b8"
            st.markdown(
                f"""
                <div class="score-card" style="border-top: 5px solid {border}; min-height: 140px;">
                    <div style="font-size: 2rem;">📘</div>
                    <h3 style="margin: 0.4rem 0;">{unit['title']}</h3>
                    <p style="color: #6b7280; font-size: 0.9rem;">{unit.get('subtitle', '')}</p>
                    <p style="font-size: 0.85rem; margin-top: 0.5rem;"><strong>{badge}</strong></p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open {unit['title']}", key=f"c3_unit_{unit['id']}", width="stretch", type="primary"):
                _open_unit(unit["id"])
                st.rerun()


def render_unit():
    """Single unit hub — activities (Unit 2) or PDF placeholder."""
    unit_id = st.session_state.get("c3_unit_id", 2)
    unit = c3.get_unit(unit_id)
    if not unit:
        st.error("Unit not found.")
        return

    col_nav1, col_nav2, _ = st.columns([1, 1, 5])
    with col_nav1:
        if st.button("← All units", key="c3_unit_back_home"):
            st.session_state.current_page = "course3_home"
            st.rerun()
    with col_nav2:
        if unit["pdf"].is_file():
            with open(unit["pdf"], "rb") as f:
                st.download_button(
                    "📄 PDF",
                    data=f.read(),
                    file_name=unit["pdf"].name,
                    mime="application/pdf",
                    key=f"c3_unit_pdf_{unit_id}",
                )

    st.markdown(f"## {unit['title']}")
    if unit.get("subtitle"):
        st.caption(unit["subtitle"])

    if not c3.unit_notes_ready(unit):
        st.info(
            "Lesson review notes for this unit are not built yet. "
            "You can download the textbook PDF above. "
            "**Units 1–5** have full activity notes with diagrams."
        )
        if not unit["pdf"].is_file():
            st.warning("No PDF found for this unit yet.")
        return

    if unit.get("combined_notes") and unit["combined_notes"].is_file():
        if st.button("📋 Unit overview & cheat sheet", key=f"c3_overview_{unit_id}", width="stretch"):
            _open_notes(unit_id, None)
            st.rerun()

    st.markdown("### Activities")
    st.caption("Tap an activity to open its review notes.")

    for act in unit["activities"]:
        label = f"Activity {act['number']}: {act['title']}"
        if act.get("inline_diagrams"):
            label += " 🎨"
        if st.button(label, key=f"c3_open_{unit_id}_{act['slug']}", width="stretch"):
            _open_notes(unit_id, act["slug"])
            st.rerun()


def render_notes():
    unit_id = st.session_state.get("c3_unit_id", 2)
    slug = st.session_state.get("c3_activity_slug")
    unit = c3.get_unit(unit_id) or c3.UNIT_2

    col_nav1, col_nav2, _ = st.columns([1, 1, 5])
    with col_nav1:
        if st.button(f"← {unit['title']}", key="c3_notes_back_unit"):
            st.session_state.current_page = "course3_unit"
            st.session_state.c3_activity_slug = None
            st.rerun()
    with col_nav2:
        if slug and st.button("Unit overview", key="c3_to_overview"):
            st.session_state.c3_activity_slug = None
            st.rerun()

    if slug:
        activity = next((a for a in unit["activities"] if a["slug"] == slug), None)
        if not activity:
            st.error("Activity not found.")
            return
        st.markdown(f"### Activity {activity['number']}: {activity['title']}")
        md = c3.load_activity_markdown(unit, activity)
        if activity.get("inline_diagrams"):
            c3r.render_markdown_with_diagrams(unit, activity, md)
        else:
            for path, cap in c3.activity_diagrams(unit, activity):
                st.image(path, caption=cap, use_container_width=True)
            st.markdown(md)
    else:
        path = unit.get("combined_notes")
        if path and path.is_file():
            st.markdown(path.read_text(encoding="utf-8"))
        else:
            st.warning("Combined notes not available.")

    if unit.get("activities"):
        st.markdown("---")
        st.markdown("**Other activities in this unit**")
        for act in unit["activities"]:
            if act["slug"] != slug:
                if st.button(
                    f"Activity {act['number']}: {act['title']}",
                    key=f"c3_jump_{unit_id}_{act['slug']}",
                ):
                    st.session_state.c3_activity_slug = act["slug"]
                    st.rerun()
