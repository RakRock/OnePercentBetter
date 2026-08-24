"""Biology concept visuals — labeled SVG (primary) + optional cached HF illustrations."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from . import content as hpc
from . import diagrams as hpd

ROOT = Path(__file__).resolve().parent


def _diagrams_dir(unit_id: int | None = None) -> Path:
    uid = unit_id if unit_id is not None else hpc.active_unit_id()
    return hpc.unit_dir(uid) / "diagrams"


def inject_biology_styles(unit_id: int | None = None) -> None:
    css = hpc.css_variables_block(unit_id)
    st.markdown(
        f"""
<style>
{css}
.hp-screen {{ padding: var(--hb-spacing-screen) 0; }}
.hp-concept-name {{
  font-size: 1.45rem; color: var(--hb-text-primary); font-weight: 600; margin-bottom: 0.75rem;
}}
.hp-section-label {{
  font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--hb-text-secondary); margin: 1.1rem 0 0.35rem;
}}
.hp-body {{ color: var(--hb-text-primary); line-height: 1.55; font-size: 1.02rem; }}
.hp-remember {{
  background: var(--hb-bg-muted); padding: 0.85rem 1rem; border-radius: var(--hb-radius);
  border-left: 3px solid var(--hb-accent-teal); margin-top: 0.75rem;
}}
.hp-confusion {{
  background: #FFFBEB; padding: 0.85rem 1rem; border-radius: var(--hb-radius);
  border-left: 3px solid #F59E0B; margin-top: 0.75rem; color: #92400E;
}}
.hp-feedback {{
  background: var(--hb-feedback-amber); color: var(--hb-feedback-amber-text);
  padding: 1rem 1.25rem; border-radius: var(--hb-radius); margin-top: 1rem;
  border: 1px solid #E8D4A8; line-height: 1.5;
}}
.hp-diagram-wrap {{
  background: var(--hb-bg-surface); border: 1px solid var(--hb-border-subtle);
  border-radius: var(--hb-radius); padding: 0.75rem; margin: 1rem 0;
}}
.hp-glossary {{
  font-size: 0.92rem; color: var(--hb-text-secondary);
}}
.hp-diagram-caption {{
  font-size: 0.85rem; color: var(--hb-text-secondary); text-align: center; margin-top: 0.35rem;
}}
</style>
""",
        unsafe_allow_html=True,
    )


def _cached_hf_image(concept_id: str, unit_id: int | None = None) -> Path | None:
    path = _diagrams_dir(unit_id) / f"{concept_id}.png"
    return path if path.is_file() else None


def render_concept_visual(
    visual: dict, *, concept_id: str = "", concept_name: str = "", unit_id: int | None = None
) -> None:
    """Prefer accurate labeled SVG; show HF illustration underneath when pre-generated."""
    st.markdown(hpd.render_diagram_html(visual), unsafe_allow_html=True)

    cached = _cached_hf_image(concept_id, unit_id) if concept_id else None
    if cached:
        with st.expander("Everyday picture (optional)", expanded=False):
            st.image(str(cached), use_container_width=True)
            st.caption("Illustration only — use the labeled diagram above for angles and ray rules.")


def render_glossary_sidebar(glossary: list[dict], *, open_default: bool = False) -> None:
    import html as html_lib

    with st.expander("📖 Glossary", expanded=open_default):
        for item in glossary:
            st.markdown(
                f'<div class="hp-glossary"><strong>{html_lib.escape(item["term"])}</strong> — '
                f'{html_lib.escape(item["definition"])}</div>',
                unsafe_allow_html=True,
            )
