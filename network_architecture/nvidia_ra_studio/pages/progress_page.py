"""Progress tracking and export."""

from __future__ import annotations

import streamlit as st

from core.content_catalog import MODULES
from core.exporter import export_progress_json, export_progress_markdown


def render(store, user_id: int, profile: str) -> None:
    st.header("📈 Progress & Export")

    stats = store.dashboard_summary(user_id, len(MODULES))
    st.json(stats)

    prog_md = export_progress_markdown(store, user_id, profile)
    prog_json = export_progress_json(store, user_id, profile)

    st.download_button("Export progress (Markdown)", prog_md, f"progress-{profile}.md", "text/markdown")
    st.download_button("Export progress (JSON)", prog_json, f"progress-{profile}.json", "application/json")

    if plan := store.latest_plan(user_id):
        st.download_button(
            "Export latest learning plan",
            plan["markdown"],
            f"plan-{profile}.md",
            "text/markdown",
        )

    st.markdown("### Bookmarks")
    for b in store.list_bookmarks(user_id):
        st.write(f"- {b['ref_type']}:{b['ref_id']}")
