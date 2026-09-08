"""Render Class 10 unit teaching guides (parent / intro notes)."""

from __future__ import annotations

import streamlit as st

import harshit_class10_revision_notes as h10rn
import harshit_class10_unit_notes as h10un
import harshit_class10_units as h10u
import harshit_math_components as hmc_ui


def _render_guide_sections(guide: dict, section_key: str, unit_id: int) -> None:
    st.markdown(f"### {guide.get('title', f'Unit {unit_id}')}")
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
    choice = st.radio(
        "Section",
        labels,
        horizontal=True,
        key=section_key,
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


def render_unit_guide(unit_id: int) -> None:
    unit = h10u.get_unit(unit_id)
    if not unit:
        st.info("Unit not found.")
        return

    hmc_ui.inject_harshit_styles()

    revision = h10rn.get_unit_revision_guide(unit_id)
    full = h10un.get_unit_guide(unit_id)

    if revision:
        _render_guide_sections(revision, f"hm10_rev_section_{unit_id}", unit_id)
        if full:
            with st.expander("📚 Detailed unit guide (all sections)", expanded=False):
                for sec in full.get("sections") or []:
                    st.markdown(f"#### {sec.get('title', 'Section')}")
                    body = str(sec.get("body", "")).strip()
                    if body:
                        st.markdown(body)
                    st.markdown("---")
        st.caption(
            "Use this revision sheet before each practice session. "
            "Export printable copies from `HarshitMath/class10/revision_notes/`."
        )
        return

    if full:
        _render_guide_sections(
            {"title": full.get("title", unit["title"]), "subtitle": full.get("subtitle"), "sections": full.get("sections", [])},
            f"hm10_guide_section_{unit_id}",
            unit_id,
        )
        st.caption(
            f"Use **Week Setup** to choose topics, then **Practice** when Harshit is ready. "
            f"Notes follow NCERT Chapter {unit_id}."
        )
        return

    st.info("Unit guide coming soon for this chapter.")
