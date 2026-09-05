"""Render PreReq topic lesson notes (parent / intro)."""

from __future__ import annotations

import streamlit as st

import harshit_geometry_diagrams as hgd
import harshit_prereq_topics as hpt
import harshit_prereq_unit_notes as hpun


def render_prereq_notes(prereq_id: int) -> None:
    topic_ids = hpun.topics_with_notes(prereq_id)
    if not topic_ids:
        st.info("Lesson notes for this PreReq are coming next. Use Practice for now.")
        return

    topic_labels = {
        tid: hpt.TOPICS.get(prereq_id, {}).get(tid, {}).get("name", f"Topic {tid}")
        for tid in topic_ids
    }
    pick_key = f"hm_pr_notes_topic_{prereq_id}"
    if len(topic_ids) > 1:
        choice = st.radio(
            "Topic",
            topic_ids,
            format_func=lambda tid: f"{topic_labels[tid]}",
            horizontal=True,
            key=pick_key,
        )
    else:
        choice = topic_ids[0]

    guide = hpun.get_topic_guide(prereq_id, int(choice))
    if not guide:
        st.info("Notes for this topic are not ready yet.")
        return

    st.markdown(f"### {guide['title']}")
    if guide.get("subtitle"):
        st.caption(guide["subtitle"])

    sections = guide.get("sections") or []
    labels = [s["title"] for s in sections]
    sec_key = f"hm_pr_notes_sec_{prereq_id}_{choice}"
    if labels:
        selected = st.radio(
            "Section",
            labels,
            horizontal=True,
            key=sec_key,
            label_visibility="collapsed",
        )
    else:
        selected = None

    st.markdown("---")
    for sec in sections:
        if selected and sec["title"] != selected:
            continue
        for spec in sec.get("diagrams") or []:
            svg = hgd.render_geometry_svg(spec)
            if svg:
                st.markdown(svg, unsafe_allow_html=True)
        body = str(sec.get("body", "")).strip()
        if body:
            st.markdown(body)
        break

    topic_name = topic_labels.get(int(choice), "this topic")
    st.caption(f"Read a section together, then switch to **Practice** — {topic_name}, Level A.")
