"""Low-sensory visual components for Harshit Math (Streamlit HTML)."""

from __future__ import annotations

import streamlit.components.v1 as components

import harshit_math_content as hmc

_CSS = hmc.css_variables_block()


def inject_harshit_styles() -> None:
    import streamlit as st

    st.markdown(
        f"""
<style>
{_CSS}
.hm-screen {{
  background: var(--hm-bg-page);
  padding: var(--hm-spacing-screen) 0;
}}
.hm-problem {{
  font-family: var(--hm-font-math);
  font-size: 1.35rem;
  color: var(--hm-text-equation);
  line-height: 1.6;
  margin-bottom: var(--hm-spacing-block);
}}
.hm-prompt {{
  color: var(--hm-text-primary);
  font-size: 1.05rem;
  margin-bottom: 1rem;
}}
.hm-feedback {{
  background: var(--hm-feedback-amber);
  color: var(--hm-feedback-amber-text);
  padding: 1rem 1.25rem;
  border-radius: var(--hm-radius);
  margin-top: 1rem;
  border: 1px solid #E8D4A8;
  font-size: 0.98rem;
  line-height: 1.5;
}}
.hm-success {{
  background: var(--hm-success-soft);
  color: var(--hm-success-text);
  padding: 1rem 1.25rem;
  border-radius: var(--hm-radius);
  margin-top: 1rem;
  border: 1px solid var(--hm-border-subtle);
}}
.hm-nl-track {{
  position: relative;
  height: 4px;
  background: var(--hm-number-line-track);
  margin: 3rem 1rem 2rem;
  border-radius: 2px;
}}
.hm-nl-tick {{
  position: absolute;
  width: 2px;
  height: 12px;
  background: var(--hm-number-line-tick);
  top: -4px;
  transform: translateX(-50%);
}}
.hm-nl-label {{
  position: absolute;
  top: 16px;
  transform: translateX(-50%);
  font-size: 0.85rem;
  color: var(--hm-text-secondary);
}}
.hm-nl-marker {{
  position: absolute;
  width: 14px;
  height: 14px;
  background: var(--hm-number-line-marker);
  border-radius: 50%;
  top: -5px;
  transform: translateX(-50%);
  border: 2px solid var(--hm-bg-surface);
}}
.hm-frac-grid {{
  display: grid;
  gap: 1px;
  background: var(--hm-fraction-grid-line);
  border: 1px solid var(--hm-fraction-grid-line);
  max-width: 280px;
  margin: 1.5rem auto;
}}
.hm-frac-cell {{
  aspect-ratio: 1;
  background: var(--hm-bg-surface);
  cursor: pointer;
  min-height: 28px;
}}
.hm-frac-cell.shade-a {{ background: var(--hm-fraction-shade-a); }}
.hm-frac-cell.shade-b {{ background: var(--hm-fraction-shade-b); }}
.hm-frac-cell.overlap {{ background: #7B8FA3; }}
</style>
""",
        unsafe_allow_html=True,
    )


def render_number_line_static(
    *,
    min_val: float = -10,
    max_val: float = 10,
    marker: float | None = None,
    markers: list[float] | None = None,
    height: int = 120,
) -> None:
    """Read-only number line visualization."""
    span = max_val - min_val
    ticks = []
    step = 1 if span <= 20 else max(1, int(span / 10))
    v = min_val
    while v <= max_val + 0.001:
        pct = (v - min_val) / span * 100 if span else 50
        ticks.append(f'<div class="hm-nl-tick" style="left:{pct}%"></div>')
        ticks.append(f'<div class="hm-nl-label" style="left:{pct}%">{v:g}</div>')
        v += step

    marker_html = ""
    for m in markers or ([marker] if marker is not None else []):
        pct = (m - min_val) / span * 100 if span else 50
        marker_html += f'<div class="hm-nl-marker" style="left:{pct}%"></div>'

    html = f"""
<div class="hm-screen">
  <div class="hm-nl-track">{''.join(ticks)}{marker_html}</div>
</div>
"""
    components.html(html, height=height, scrolling=False)


def render_fraction_grid_static(*, rows: int, cols: int, shaded_rows: int = 0, shaded_cols: int = 0) -> None:
    cells = []
    for r in range(rows):
        for c in range(cols):
            cls = "hm-frac-cell"
            if r < shaded_rows and c < shaded_cols:
                cls += " overlap"
            elif r < shaded_rows:
                cls += " shade-a"
            elif c < shaded_cols:
                cls += " shade-b"
            cells.append(f'<div class="{cls}"></div>')

    html = f"""
<div class="hm-frac-grid" style="grid-template-columns: repeat({cols}, 1fr); grid-template-rows: repeat({rows}, 1fr);">
  {''.join(cells)}
</div>
"""
    components.html(html, height=min(320, 40 * rows + 40), scrolling=False)
