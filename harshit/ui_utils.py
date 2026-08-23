"""Shared Streamlit UI helpers for Harshit Physics/Chemistry."""

from __future__ import annotations

import streamlit as st

_SCROLL_KEY = "_harshit_scroll_to_top"


def request_scroll_to_top() -> None:
    """On the next rerun, scroll the app view back to the top."""
    st.session_state[_SCROLL_KEY] = True


def render_scroll_to_top_if_requested() -> None:
    """Scroll to top once after ``request_scroll_to_top()`` (e.g. Next concept)."""
    if not st.session_state.pop(_SCROLL_KEY, False):
        return
    st.components.v1.html(
        """
        <script>
        (function () {
            const doc = window.parent.document;
            const targets = [
                doc.querySelector('[data-testid="stAppViewContainer"]'),
                doc.querySelector('[data-testid="stMain"]'),
                doc.querySelector("section.main"),
                doc.documentElement,
                doc.body,
            ];
            for (const el of targets) {
                if (!el) continue;
                el.scrollTop = 0;
                if (el.scrollTo) el.scrollTo(0, 0);
            }
            window.parent.scrollTo(0, 0);
        })();
        </script>
        """,
        height=0,
    )
