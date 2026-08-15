"""Render Edgenuity lesson markdown with inline diagrams at [DIAGRAM:key] markers."""

from __future__ import annotations

import re

import streamlit as st

import arjun_edgenuity_course3_content as ec3

_DIAGRAM_TAG = re.compile(r"\[DIAGRAM:([a-z0-9_]+)\]")
_KEY_TAG = re.compile(r"\[KEY\]\s*(.*?)\s*\[/KEY\]", re.DOTALL)
_CALLOUT_LINE = re.compile(
    r"^\*\*(What is this about|How to think about it|Why this works|Remember):\*\*\s*(.+)$",
    re.MULTILINE | re.IGNORECASE,
)
_EXAMPLE_HEADER = re.compile(r"^### Example .+$", re.MULTILINE)
_EXAM_PRACTICE_HEADER = re.compile(r"^### Exam-style practice\s*$", re.MULTILINE)
_TAIL_SECTION = re.compile(r"\n(### Common Mistakes|### Mini Summary)", re.MULTILINE)


def _strip_key_blocks(markdown: str) -> tuple[str, list[str]]:
    keys: list[str] = []
    for m in _KEY_TAG.finditer(markdown):
        keys.append(m.group(1).strip())
    body = _KEY_TAG.sub("", markdown)
    return body, keys


def _diagram_file(unit: dict, activity: dict, key: str) -> str | None:
    img_dir = ec3.unit_images_dir(unit["id"])
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


def _render_callouts(markdown: str) -> str:
    """Turn teaching callout lines into visible markdown blocks."""

    def _replace(match: re.Match[str]) -> str:
        label = match.group(1).strip().lower()
        text = match.group(2).strip()
        if label == "what is this about":
            prefix = "📖 **What is this about?**"
        elif label == "how to think about it":
            prefix = "💡 **How to think about it**"
        elif label == "why this works":
            prefix = "✅ **Why this works**"
        else:
            prefix = "⭐ **Remember**"
        return f"\n{prefix}\n\n{text}\n"

    return _CALLOUT_LINE.sub(_replace, markdown)


def _render_text_block(unit: dict, activity: dict, markdown: str) -> None:
    markdown = _render_callouts(markdown)
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
            st.caption(
                f"_(Run `python generate_edgenuity_unit1_diagrams.py` to create diagram: {key})_"
            )
        pos = m.end()
    tail = markdown[pos:]
    if tail.strip():
        st.markdown(tail)


def _split_example_tail(body: str) -> tuple[str, str, str]:
    """Return (example_body, exam_practice_section, closing_sections)."""
    exam_match = _EXAM_PRACTICE_HEADER.search(body)
    if not exam_match:
        tail_match = _TAIL_SECTION.search(body)
        if tail_match:
            return body[: tail_match.start()].strip(), "", body[tail_match.start() :].strip()
        return body.strip(), "", ""

    example_body = body[: exam_match.start()].strip()
    after_exam = body[exam_match.start() :]
    tail_match = _TAIL_SECTION.search(after_exam)
    if tail_match:
        exam_section = after_exam[: tail_match.start()].strip()
        closing = after_exam[tail_match.start() :].strip()
        return example_body, exam_section, closing
    return example_body, after_exam.strip(), ""


def render_markdown_with_diagrams(unit: dict, activity: dict, markdown: str) -> None:
    markdown, key_blocks = _strip_key_blocks(markdown)
    for block in key_blocks:
        st.info(block)

    parts = _EXAMPLE_HEADER.split(markdown)
    if len(parts) <= 1:
        _render_text_block(unit, activity, markdown)
        return

    intro = parts[0]
    if intro.strip():
        _render_text_block(unit, activity, intro)

    headers = _EXAMPLE_HEADER.findall(markdown)
    exam_block = ""
    closing = ""
    for idx, (header, body) in enumerate(zip(headers, parts[1:], strict=False)):
        if idx == len(headers) - 1:
            body, exam_block, closing = _split_example_tail(body)
        with st.expander(header.replace("### ", ""), expanded=(idx == 0)):
            _render_text_block(unit, activity, body.strip())

    if exam_block.strip():
        with st.expander("Exam-style practice", expanded=False):
            _render_text_block(unit, activity, exam_block.strip())

    if closing.strip():
        _render_text_block(unit, activity, closing)

