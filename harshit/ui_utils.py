"""Shared Streamlit UI helpers for Harshit Physics/Chemistry."""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st
import streamlit.components.v1 as components

_CONCEPT_TOP_ANCHOR_ID = "harshit-concept-top"
_SCROLL_PENDING_KEY = "_harshit_scroll_pending"
_SCROLL_NONCE_KEY = "_harshit_scroll_nonce"


def render_subject_unit_tiles(
    units: list[dict],
    *,
    accent: str = "#6366F1",
    key_prefix: str = "unit",
) -> None:
    """Render units as a 2×2 grid of large tiles (best for four units).

    Each unit dict: ``id``, ``title``, ``on_open`` (callable), optional ``subtitle``,
    ``button_label``, ``featured`` (bool).
    """
    st.markdown(
        f"""
<style>
.harshit-unit-tile-wrap {{ margin-bottom: 0.35rem; }}
.harshit-unit-tile {{
  background: #FFFFFF;
  border: 1px solid #D8DEE6;
  border-top: 5px solid {accent};
  border-radius: 12px;
  padding: 1.85rem 1.35rem 1.15rem;
  min-height: 148px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
}}
.harshit-unit-tile.featured {{
  background: linear-gradient(145deg, #EEF2FF 0%, #FFFFFF 55%);
}}
.harshit-unit-num {{
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: {accent};
  margin-bottom: 0.4rem;
}}
.harshit-unit-title {{
  font-size: 1.2rem;
  font-weight: 600;
  color: #1E293B;
  line-height: 1.35;
  margin: 0 0 0.55rem 0;
}}
.harshit-unit-sub {{
  font-size: 0.9rem;
  color: #64748B;
  margin: 0;
  line-height: 1.4;
}}
div[data-testid="column"] .stButton > button {{
  min-height: 3.1rem;
  font-size: 1.02rem;
  font-weight: 600;
  border-radius: 10px;
}}
</style>
""",
        unsafe_allow_html=True,
    )

    for row in range(2):
        cols = st.columns(2, gap="large")
        for col_idx in range(2):
            idx = row * 2 + col_idx
            if idx >= len(units):
                continue
            unit = units[idx]
            uid = int(unit["id"])
            featured = bool(unit.get("featured", idx == 0))
            tile_class = "harshit-unit-tile featured" if featured else "harshit-unit-tile"
            subtitle = str(unit.get("subtitle") or "16 concept days · Practice · Stage 2 & 3")
            with cols[col_idx]:
                st.markdown(
                    f"""
<div class="harshit-unit-tile-wrap">
  <div class="{tile_class}">
    <div class="harshit-unit-num">Unit {uid}</div>
    <div class="harshit-unit-title">{unit["title"]}</div>
    <p class="harshit-unit-sub">{subtitle}</p>
  </div>
</div>
""",
                    unsafe_allow_html=True,
                )
                label = str(unit.get("button_label") or f"Start Unit {uid}")
                if st.button(
                    label,
                    type="primary" if featured else "secondary",
                    use_container_width=True,
                    key=f"{key_prefix}_tile_{uid}",
                ):
                    on_open: Callable[[], None] = unit["on_open"]
                    on_open()
                    st.rerun()


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
