"""Shared Week Setup panel for Arjun Course 3 and Edgenuity Course 3."""

from __future__ import annotations

from typing import Literal

import streamlit as st

import arjun_course3_content as c3
import arjun_course3_levels as c3lvl
import arjun_course3_practice as c3p
import arjun_course3_week as c3w
import arjun_edgenuity_course3_content as ec3
import arjun_edgenuity_course3_practice as ec3p
import arjun_edgenuity_course3_week as ec3w
import database as db

Track = Literal["course3", "edgenuity"]


def _xai_api_key() -> str | None:
    import os

    try:
        return st.secrets.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
    except Exception:
        import os

        return os.environ.get("XAI_API_KEY")


def ensure_week_config(track: Track, unit_id: int) -> dict:
    if track == "course3":
        config = db.get_arjun_course3_week_config(unit_id)
        valid = set(c3p.get_categories(unit_id).keys())
        normalized = c3lvl.normalize_week_config(config, valid, unit_id=unit_id)
        if normalized.get("topics"):
            return normalized
        starter = c3w.default_week_config(unit_id)
        if not starter.get("topics"):
            return normalized
        db.save_arjun_course3_week_config(
            unit_id,
            starter["week_label"],
            starter["topics"],
            question_count=int(starter.get("question_count", c3p.DEFAULT_SESSION_COUNT)),
            use_llm=bool(starter.get("use_llm", False)),
        )
        return c3lvl.normalize_week_config(
            db.get_arjun_course3_week_config(unit_id), valid, unit_id=unit_id
        )

    config = db.get_arjun_edgenuity_course3_week_config(unit_id)
    valid = set(ec3p.get_categories(unit_id).keys())
    normalized = c3lvl.normalize_week_config(config, valid, unit_id=unit_id)
    if normalized.get("topics"):
        return normalized
    starter = ec3w.default_week_config(unit_id)
    if not starter.get("topics"):
        return normalized
    db.save_arjun_edgenuity_course3_week_config(
        unit_id,
        starter["week_label"],
        starter["topics"],
        question_count=int(starter.get("question_count", 15)),
        use_llm=bool(starter.get("use_llm", False)),
    )
    return c3lvl.normalize_week_config(
        db.get_arjun_edgenuity_course3_week_config(unit_id), valid, unit_id=unit_id
    )


def _clear_setup_widget_state(track: Track, unit_id: int) -> None:
    prefix = "c3" if track == "course3" else "ec3"
    for key in list(st.session_state.keys()):
        if key.startswith(f"{prefix}_setup_{unit_id}_"):
            del st.session_state[key]


def render_setup_panel(track: Track, unit_id: int) -> None:
    if track == "course3":
        unit = c3.get_unit(unit_id)
        get_config = db.get_arjun_course3_week_config
        save_config = db.save_arjun_course3_week_config
        categories_meta = c3p.get_categories(unit_id)
        bank_count = c3p.question_count_for_unit(unit_id)
        guidance = c3w.weekly_guidance(unit_id)
        format_summary = c3w.format_week_plan_summary
        default_count = c3p.DEFAULT_SESSION_COUNT
        key_prefix = "c3"
    else:
        unit = ec3.get_unit(unit_id)
        get_config = db.get_arjun_edgenuity_course3_week_config
        save_config = db.save_arjun_edgenuity_course3_week_config
        categories_meta = ec3p.get_categories(unit_id)
        bank_count = ec3p.question_count_for_unit(unit_id)
        guidance = ec3w.weekly_guidance(unit_id)
        format_summary = ec3w.format_week_plan_summary
        default_count = 15
        key_prefix = "ec3"

    if not unit:
        st.error("Unit not found.")
        return

    if not categories_meta:
        st.info("Practice categories for this unit are not ready yet.")
        return

    valid = set(categories_meta.keys())
    current = c3lvl.normalize_week_config(get_config(unit_id), valid, unit_id=unit_id)

    st.markdown("### Weekly Plan Setup")
    st.caption(
        f"Choose practice topics, difficulty levels, and Grok generation for **{unit['title']}**. "
        "Daily practice rotates through the topic + level slots you select."
    )
    st.markdown(guidance)

    if bank_count:
        st.caption(f"Question bank: **{bank_count}** questions across all topics.")

    week_label = st.text_input(
        "Week label (optional)",
        value=current.get("week_label", ""),
        placeholder=f"e.g. Week 1 — {unit['title'][:28]}",
        key=f"{key_prefix}_setup_label_{unit_id}",
    )

    xai_key = _xai_api_key()
    if xai_key:
        st.caption("xAI (Grok) API key detected.")
    else:
        st.caption("Add `XAI_API_KEY` to `.streamlit/secrets.toml` for Grok generation.")

    use_llm = st.toggle(
        "Generate fresh questions with xAI Grok during practice",
        value=bool(current.get("use_llm", False)),
        key=f"{key_prefix}_setup_llm_{unit_id}",
    )

    question_count = st.slider(
        "Questions per session",
        min_value=5,
        max_value=30,
        value=int(current.get("question_count", default_count)),
        key=f"{key_prefix}_setup_count_{unit_id}",
    )

    st.markdown("---")
    st.markdown("#### Topics & difficulty levels")

    current_levels: dict[str, list[str]] = {}
    for item in current.get("topics") or []:
        current_levels[str(item.get("id", ""))] = list(item.get("levels") or [])

    new_topics: list[dict] = []
    for cat_id, info in categories_meta.items():
        level_options = {
            c3lvl.format_level_picker_label(lvl): lvl for lvl in c3lvl.LEVEL_ORDER
        }
        default = [
            c3lvl.format_level_picker_label(lvl)
            for lvl in c3lvl.LEVEL_ORDER
            if lvl in current_levels.get(cat_id, c3lvl.DEFAULT_LEVELS)
        ]
        if not default and cat_id in current_levels:
            default = [
                c3lvl.format_level_picker_label(lvl)
                for lvl in current_levels[cat_id]
                if lvl in c3lvl.LEVEL_ORDER
            ]
        picked = st.multiselect(
            f"{info.get('emoji', '')} **{info.get('name', cat_id)}**",
            options=list(level_options.keys()),
            default=default or [
                c3lvl.format_level_picker_label(lvl) for lvl in c3lvl.DEFAULT_LEVELS
            ],
            key=f"{key_prefix}_setup_topic_{unit_id}_{cat_id}",
        )
        levels = [level_options[p] for p in picked]
        if levels:
            new_topics.append({"id": cat_id, "levels": levels})

    if st.button("Save weekly plan", type="primary", key=f"{key_prefix}_setup_save_{unit_id}"):
        if not new_topics:
            st.warning("Select at least one topic with one difficulty level.")
        else:
            save_config(
                unit_id,
                week_label.strip(),
                new_topics,
                question_count=question_count,
                use_llm=use_llm,
            )
            _clear_setup_widget_state(track, unit_id)
            st.success("Weekly plan saved.")
            st.rerun()

    saved = c3lvl.normalize_week_config(get_config(unit_id), valid, unit_id=unit_id)
    if saved.get("topics"):
        st.markdown("**Current active plan**")
        st.code(format_summary(unit_id, saved), language=None)
