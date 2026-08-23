"""Shared Streamlit UI helpers for Harshit Physics/Chemistry."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

_CONCEPT_TOP_ANCHOR_ID = "harshit-concept-top"
_SCROLL_PENDING_KEY = "_harshit_scroll_pending"
_SCROLL_NONCE_KEY = "_harshit_scroll_nonce"


def request_scroll_to_top() -> None:
    """On the next rerun, scroll the app view back to the top."""
    st.session_state[_SCROLL_PENDING_KEY] = True
    st.session_state[_SCROLL_NONCE_KEY] = int(st.session_state.get(_SCROLL_NONCE_KEY, 0)) + 1


def render_concept_top_anchor() -> None:
    """Invisible anchor at the top of the concept card (parent document)."""
    st.markdown(
        f'<div id="{_CONCEPT_TOP_ANCHOR_ID}" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )


def render_scroll_to_top_if_requested() -> None:
    """Scroll to top once after ``request_scroll_to_top()`` — call at end of page."""
    if not st.session_state.pop(_SCROLL_PENDING_KEY, False):
        return
    nonce = int(st.session_state.get(_SCROLL_NONCE_KEY, 0))
    anchor_id = _CONCEPT_TOP_ANCHOR_ID
    components.html(
        f"""
        <div id="harshit-scroll-{nonce}" style="height:0;margin:0;padding:0;"></div>
        <script>
        (function () {{
            const anchorId = "{anchor_id}";
            function scrollTop() {{
                const doc = window.parent.document;
                const anchor = doc.getElementById(anchorId);
                if (anchor) {{
                    anchor.scrollIntoView({{ block: "start", inline: "nearest", behavior: "auto" }});
                }}
                const selectors = [
                    '[data-testid="stAppViewContainer"]',
                    '[data-testid="stMain"]',
                    '[data-testid="stMainBlockContainer"]',
                    "section.main",
                    ".main",
                ];
                for (const sel of selectors) {{
                    const el = doc.querySelector(sel);
                    if (!el) continue;
                    el.scrollTop = 0;
                    if (el.scrollTo) el.scrollTo({{ top: 0, left: 0, behavior: "auto" }});
                }}
                if (window.parent.scrollTo) window.parent.scrollTo(0, 0);
            }}
            scrollTop();
            [0, 80, 200, 400, 800].forEach(function (ms) {{
                setTimeout(scrollTop, ms);
            }});
        }})();
        </script>
        """,
        height=1,
        scrolling=False,
    )
