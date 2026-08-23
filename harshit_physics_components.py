"""Physics concept visuals — labeled SVG (primary) + optional cached HF illustrations."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

import harshit_physics_content as hpc
import harshit_physics_diagrams as hpd

ROOT = Path(__file__).resolve().parent
DIAGRAMS_DIR = ROOT / "HarshitPhysics" / "unit1" / "diagrams"
_CSS = hpc.css_variables_block()


def inject_physics_styles() -> None:
    st.markdown(
        f"""
<style>
{_CSS}
.hp-screen {{ padding: var(--hp-spacing-screen) 0; }}
.hp-concept-name {{
  font-size: 1.45rem; color: var(--hp-text-primary); font-weight: 600; margin-bottom: 0.75rem;
}}
.hp-section-label {{
  font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--hp-text-secondary); margin: 1.1rem 0 0.35rem;
}}
.hp-body {{ color: var(--hp-text-primary); line-height: 1.55; font-size: 1.02rem; }}
.hp-remember {{
  background: var(--hp-bg-muted); padding: 0.85rem 1rem; border-radius: var(--hp-radius);
  border-left: 3px solid var(--hp-accent-indigo); margin-top: 0.75rem;
}}
.hp-confusion {{
  background: #FFFBEB; padding: 0.85rem 1rem; border-radius: var(--hp-radius);
  border-left: 3px solid #F59E0B; margin-top: 0.75rem; color: #92400E;
}}
.hp-feedback {{
  background: var(--hp-feedback-amber); color: var(--hp-feedback-amber-text);
  padding: 1rem 1.25rem; border-radius: var(--hp-radius); margin-top: 1rem;
  border: 1px solid #E8D4A8; line-height: 1.5;
}}
.hp-diagram-wrap {{
  background: var(--hp-bg-surface); border: 1px solid var(--hp-border-subtle);
  border-radius: var(--hp-radius); padding: 0.75rem; margin: 1rem 0;
}}
.hp-glossary {{
  font-size: 0.92rem; color: var(--hp-text-secondary);
}}
.hp-diagram-caption {{
  font-size: 0.85rem; color: var(--hp-text-secondary); text-align: center; margin-top: 0.35rem;
}}
</style>
""",
        unsafe_allow_html=True,
    )


def _cached_hf_image(concept_id: str) -> Path | None:
    path = DIAGRAMS_DIR / f"{concept_id}.png"
    return path if path.is_file() else None


def render_concept_visual(visual: dict, *, concept_id: str = "", concept_name: str = "") -> None:
    """Prefer accurate labeled SVG; show HF illustration underneath when pre-generated."""
    st.markdown(hpd.render_diagram_html(visual), unsafe_allow_html=True)

    cached = _cached_hf_image(concept_id) if concept_id else None
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
