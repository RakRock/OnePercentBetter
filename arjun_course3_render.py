"""Render lesson markdown with inline diagrams at [DIAGRAM:key] markers."""

from __future__ import annotations

import re

import streamlit as st

import arjun_course3_content as c3

_DIAGRAM_TAG = re.compile(r"\[DIAGRAM:([a-z0-9_]+)\]")
_KEY_TAG = re.compile(r"\[KEY\]\s*(.*?)\s*\[/KEY\]", re.DOTALL)


def _strip_key_blocks(markdown: str) -> tuple[str, list[str]]:
    """Pull [KEY]...[/KEY] blocks for highlighted callouts; return body without them."""
    keys: list[str] = []
    for m in _KEY_TAG.finditer(markdown):
        keys.append(m.group(1).strip())
    body = _KEY_TAG.sub("", markdown)
    return body, keys


def _diagram_file(unit: dict, activity: dict, key: str) -> str | None:
    img_dir = c3.unit_images_dir(unit["id"])
    act_num = activity.get("number", 0)
    for item in activity.get("diagrams") or []:
        if item.get("key") == key:
            path = img_dir / item["file"]
            if path.is_file():
                return str(path)
    candidate = img_dir / f"activity_{act_num}_{key}.png"
    return str(candidate) if candidate.is_file() else None


def _caption_for(unit: dict, activity: dict, key: str) -> str:
    for item in activity.get("diagrams") or []:
        if item.get("key") == key:
            return item.get("caption", "")
    return ""


def render_markdown_with_diagrams(unit: dict, activity: dict, markdown: str) -> None:
    """Render markdown; highlight [KEY] blocks, then diagrams at [DIAGRAM:key] tags."""
    markdown, key_blocks = _strip_key_blocks(markdown)
    for block in key_blocks:
        st.info(block)

    pos = 0
    for m in _DIAGRAM_TAG.finditer(markdown):
        before = markdown[pos : m.start()]
        if before.strip():
            st.markdown(before)
        key = m.group(1)
        path = _diagram_file(unit, activity, key)
        cap = _caption_for(unit, activity, key)
        if path:
            st.image(path, use_container_width=True)
            if cap:
                st.caption(cap)
        else:
            st.caption(f"_(Run `python generate_unit2_diagrams.py --activity {activity.get('number', '')}` to create diagram: {key})_")
        pos = m.end()
    tail = markdown[pos:]
    if tail.strip():
        st.markdown(tail)
