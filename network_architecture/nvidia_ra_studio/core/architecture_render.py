"""Render architecture lesson markdown with inline [KEY] and [DIAGRAM] markers."""

from __future__ import annotations

import re

import streamlit as st

from core.architecture_diagrams import diagram_caption, diagram_path, images_dir

_DIAGRAM_TAG = re.compile(r"\[DIAGRAM:([a-z0-9_]+)\]")
_KEY_TAG = re.compile(r"\[KEY\]\s*(.*?)\s*\[/KEY\]", re.DOTALL)


def render_lesson_markdown(layer_id: str | None, markdown: str) -> None:
    """Render student lesson notes: KEY callouts, markdown sections, inline diagrams."""
    key_blocks = [m.group(1).strip() for m in _KEY_TAG.finditer(markdown)]
    body = _KEY_TAG.sub("", markdown)

    for block in key_blocks:
        st.markdown(
            f"""
            <div style="background:#ecfdf5;border-left:4px solid #76b900;padding:0.75rem 1rem;
                        border-radius:6px;margin:0.5rem 0 1rem 0;">
                <strong>📌 Key takeaway</strong><br/>{block}
            </div>
            """,
            unsafe_allow_html=True,
        )

    pos = 0
    for m in _DIAGRAM_TAG.finditer(body):
        before = body[pos : m.start()]
        if before.strip():
            st.markdown(before)
        key = m.group(1)
        path = diagram_path(layer_id, key)
        cap = diagram_caption(layer_id, key)
        if path and path.is_file():
            st.image(str(path), use_container_width=True)
            if cap:
                st.caption(cap)
        else:
            hint = f"`python generate_architecture_diagrams.py`"
            st.caption(f"_(Diagram `{key}` not found — run {hint} in nvidia_ra_studio/)_")
        pos = m.end()

    tail = body[pos:]
    if tail.strip():
        st.markdown(tail)


def render_diagram_gallery(layer_id: str | None) -> None:
    """Show all diagrams for a lesson as a visual review sheet."""
    from core.architecture_diagrams import LESSON_DIAGRAMS, OVERVIEW_DIAGRAMS

    specs = OVERVIEW_DIAGRAMS if layer_id is None else LESSON_DIAGRAMS.get(layer_id, [])
    if not specs:
        st.caption("No diagrams for this section.")
        return
    cols = st.columns(2)
    for i, spec in enumerate(specs):
        path = images_dir() / spec.file
        with cols[i % 2]:
            if path.is_file():
                st.image(str(path), use_container_width=True)
                st.caption(f"**{spec.key.replace('_', ' ').title()}** — {spec.caption}")
            else:
                st.caption(f"Missing: {spec.file}")
