"""Interactive architecture map with illustrated student lesson notes."""

from __future__ import annotations

import streamlit as st

from core.architecture_lesson_notes import OVERVIEW_NOTES, get_lesson_notes
from core.architecture_notes import get_lesson, lessons_by_number
from core.architecture_render import render_diagram_gallery, render_lesson_markdown
from core.content_catalog import MODULES
from core.models import ARCHITECTURE_LAYERS
from core.rag_sources import doc_url


def _render_lesson_nav() -> str:
    st.sidebar.markdown("### 📖 Architecture Course")
    lesson_order = lessons_by_number()
    layer_by_id = {layer["id"]: layer for layer in ARCHITECTURE_LAYERS}

    if "nra_layer" not in st.session_state:
        st.session_state.nra_layer = lesson_order[0].layer_id

    for lesson in lesson_order:
        layer = layer_by_id.get(lesson.layer_id, {})
        label = f"L{lesson.lesson_number}: {layer.get('name', lesson.title)}"
        if st.sidebar.button(label, key=f"layer_{lesson.layer_id}", use_container_width=True):
            st.session_state.nra_layer = lesson.layer_id

    return st.session_state.nra_layer


def _render_layer_context(layer: dict, lesson) -> None:
    st.markdown("#### Layer summary")
    st.write(layer["summary"])

    st.markdown("#### Dependencies")
    if layer["dependencies"]:
        for dep_id in layer["dependencies"]:
            dep = next((x for x in ARCHITECTURE_LAYERS if x["id"] == dep_id), None)
            st.write(f"- {dep['name'] if dep else dep_id}")
    else:
        st.write("Foundation layer — no upstream software dependencies in the RA model.")

    st.markdown("#### Common failure modes (operations)")
    for fm in layer["failure_modes"]:
        st.write(f"- {fm}")

    st.markdown("#### Official documentation")
    for key in layer["doc_keys"]:
        st.markdown(f"- [{key.replace('_', ' ').title()}]({doc_url(key)})")

    if lesson and lesson.related_modules:
        st.markdown("#### Related modules in this studio")
        for mid in lesson.related_modules:
            mod = next((m for m in MODULES if m.id == mid), None)
            if mod:
                st.markdown(f"- **Module {mod.id}:** {mod.title}")


def _render_lesson(lesson, layer: dict) -> None:
    notes_md = get_lesson_notes(lesson.layer_id)
    st.caption(f"{lesson.subtitle} · RA layer: **{layer['name']}** · ~{sum(1 for _ in lesson.lecture_sections)} sections + diagrams")

    tab_notes, tab_gallery, tab_context = st.tabs(
        ["📓 Lesson notes", "🖼️ Diagram sheet", "🔗 Context & docs"]
    )

    with tab_notes:
        if notes_md:
            render_lesson_markdown(lesson.layer_id, notes_md)
        else:
            st.warning("Lesson notes not available for this layer.")

    with tab_gallery:
        st.markdown("#### Visual review — study all diagrams for this lesson")
        st.caption("Use this tab before exams or design reviews to recall the full picture at a glance.")
        render_diagram_gallery(lesson.layer_id)

    with tab_context:
        _render_layer_context(layer, lesson)


def render(store, user_id: int, profile: str) -> None:
    st.header("🏗️ Architecture Map")
    st.caption("Illustrated lesson notes — read each lesson like a college course handout")

    layer_id = _render_lesson_nav()

    show_overview = st.toggle(
        "Show course overview",
        value=st.session_state.get("nra_show_arch_overview", True),
    )
    st.session_state.nra_show_arch_overview = show_overview
    if show_overview:
        render_lesson_markdown(None, OVERVIEW_NOTES)
        st.markdown("---")

    layer = next(l for l in ARCHITECTURE_LAYERS if l["id"] == layer_id)
    lesson = get_lesson(layer_id)
    if lesson:
        st.markdown(f"## {lesson.title}")
        _render_lesson(lesson, layer)
    else:
        st.markdown(f"## {layer['name']}")
        st.write(layer["summary"])
        _render_layer_context(layer, None)

    st.markdown("---")
    st.markdown("**Full stack (top → bottom)**")
    for lyr in ARCHITECTURE_LAYERS:
        les = get_lesson(lyr["id"])
        num = f"L{les.lesson_number} · " if les else ""
        marker = "👉 " if lyr["id"] == layer_id else "   "
        st.markdown(f"{marker}{num}**{lyr['name']}**")
