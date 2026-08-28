"""Render Class 10 unit teaching guides (parent / intro notes)."""

from __future__ import annotations

import streamlit as st

import harshit_class10_unit_notes as h10un
import harshit_class10_units as h10u
import harshit_math_components as hmc_ui


def render_unit_guide(unit_id: int) -> None:
    guide = h10un.get_unit_guide(unit_id)
    unit = h10u.get_unit(unit_id)
    if not guide or not unit:
        st.info("Unit guide coming soon for this chapter.")
        return

    hmc_ui.inject_harshit_styles()

    st.markdown(f"### {guide.get('title', unit['title'])}")
    if guide.get("subtitle"):
        st.caption(guide["subtitle"])

    pdf_path = h10u.unit_pdf_path(unit_id)
    if pdf_path and pdf_path.is_file():
        with st.expander("📄 NCERT chapter PDF", expanded=False):
            try:
                st.pdf(str(pdf_path))
            except Exception:
                st.caption(str(pdf_path))

    sections = guide.get("sections") or []
    if not sections:
        return

    labels = [s["title"] for s in sections]
    pick_key = f"hm10_guide_section_{unit_id}"
    if pick_key not in st.session_state:
        st.session_state[pick_key] = labels[0]

    choice = st.radio(
        "Guide section",
        labels,
        horizontal=True,
        key=pick_key,
        label_visibility="collapsed",
    )

    st.markdown("---")

    for sec in sections:
        if sec["title"] != choice:
            continue
        body = str(sec.get("body", "")).strip()
        if body:
            st.markdown(body)
        break

    st.markdown("---")
    st.caption(
        f"Use **Week Setup** to choose topics, then **Practice** when Harshit is ready. "
        f"Notes above follow NCERT Chapter {unit_id} and board-style questions."
    )
