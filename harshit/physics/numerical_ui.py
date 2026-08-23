"""Guided step-by-step mirror, lens, and power numericals for Stage 3."""

from __future__ import annotations

import streamlit as st


def _fmt_cm(value: float) -> str:
    if abs(value - round(value)) < 0.05:
        return f"{round(value)} cm"
    return f"{value:.1f} cm"


def render_mirror_guided(
    *,
    mirror: str = "concave",
    f_cm: float,
    u_cm: float,
    h_cm: float | None = None,
    label: str = "",
) -> None:
    """Interactive mirror formula walkthrough (NCERT sign convention)."""
    with st.expander("🔢 Guided mirror numerical", expanded=False):
        if label:
            st.caption(label)
        st.markdown("**Mirror formula:** `1/v + 1/u = 1/f`")

        mirror_type = st.selectbox(
            "Mirror type",
            ["concave", "convex"],
            index=0 if mirror == "concave" else 1,
            key=f"hp_num_mirror_type_{label}",
        )
        f_in = st.number_input(
            "Focal length f (cm) — enter with NCERT sign",
            value=float(f_cm),
            step=1.0,
            help="Concave: f negative. Convex: f positive.",
            key=f"hp_num_mirror_f_{label}",
        )
        u_in = st.number_input(
            "Object distance u (cm) — negative if object in front",
            value=float(u_cm),
            step=1.0,
            key=f"hp_num_mirror_u_{label}",
        )
        h_in = None
        if h_cm is not None:
            h_in = st.number_input(
                "Object height h (cm)",
                value=float(h_cm),
                min_value=0.1,
                step=0.5,
                key=f"hp_num_mirror_h_{label}",
            )

        if st.button("Check my steps", key=f"hp_num_mirror_go_{label}", type="primary"):
            if u_in == 0 or f_in == 0:
                st.error("u and f cannot be zero.")
                return
            inv_v = (1.0 / f_in) - (1.0 / u_in)
            if abs(inv_v) < 1e-9:
                st.warning("Image at infinity (1/v ≈ 0).")
                return
            v = 1.0 / inv_v
            st.markdown("**Step 1 — Signs**")
            st.write(
                f"Mirror: **{mirror_type}** · u = **{u_in} cm** · f = **{f_in} cm** "
                f"(object in front → u negative; concave f negative, convex f positive)."
            )
            st.markdown("**Step 2 — Apply formula**")
            st.latex(r"\frac{1}{v} = \frac{1}{f} - \frac{1}{u}")
            st.write(
                f"1/v = 1/({f_in}) − 1/({u_in}) = **{inv_v:.4f}**  →  v = **{_fmt_cm(v)}**"
            )
            st.markdown("**Step 3 — Interpret v**")
            if v < 0:
                if mirror_type == "concave":
                    st.success(
                        f"v = {_fmt_cm(v)} → **real image** {_fmt_cm(abs(v))} in front of the mirror "
                        "(screen can be placed here)."
                    )
                else:
                    st.info(f"v = {_fmt_cm(v)} — check signs; convex mirrors usually give v > 0 (virtual).")
            else:
                st.success(
                    f"v = +{_fmt_cm(v)} → **virtual image** behind the mirror (erect, diminished for convex)."
                )
            if h_in is not None and u_in != 0:
                m = -v / u_in
                h_prime = m * h_in
                st.markdown("**Step 4 — Size (m = −v/u)**")
                st.write(
                    f"m = −({v})/({u_in}) = **{m:.3f}** · h' = **{abs(h_prime):.1f} cm** "
                    f"({'inverted' if m < 0 else 'erect'})"
                )


def render_lens_guided(
    *,
    f_cm: float,
    u_cm: float | None = None,
    v_cm: float | None = None,
    h_cm: float | None = None,
    label: str = "",
) -> None:
    """Interactive lens formula walkthrough."""
    with st.expander("🔢 Guided lens numerical", expanded=False):
        if label:
            st.caption(label)
        st.markdown("**Lens formula:** `1/v − 1/u = 1/f`")

        f_in = st.number_input(
            "Focal length f (cm)",
            value=float(f_cm),
            step=1.0,
            help="Convex/converging: f > 0. Concave/diverging: f < 0.",
            key=f"hp_num_lens_f_{label}",
        )
        mode = "Find image distance v" if u_cm is not None else "Find object distance u"
        if u_cm is not None and v_cm is not None:
            mode = st.radio(
                "Solve for",
                ["Find image distance v", "Find object distance u"],
                key=f"hp_num_lens_mode_{label}",
            )

        u_in = u_cm
        v_in = v_cm
        if mode == "Find image distance v":
            u_in = st.number_input(
                "Object distance u (cm) — negative in front of lens",
                value=float(u_cm if u_cm is not None else -25),
                step=1.0,
                key=f"hp_num_lens_u_{label}",
            )
        else:
            v_in = st.number_input(
                "Image distance v (cm) — negative if virtual on object side",
                value=float(v_cm if v_cm is not None else -10),
                step=1.0,
                key=f"hp_num_lens_v_{label}",
            )
        h_in = None
        if h_cm is not None:
            h_in = st.number_input(
                "Object height h (cm)",
                value=float(h_cm),
                min_value=0.1,
                step=0.5,
                key=f"hp_num_lens_h_{label}",
            )

        if st.button("Check my steps", key=f"hp_num_lens_go_{label}", type="primary"):
            if f_in == 0:
                st.error("f cannot be zero.")
                return
            if mode == "Find image distance v":
                assert u_in is not None
                if u_in == 0:
                    st.error("u cannot be zero.")
                    return
                inv_v = (1.0 / f_in) + (1.0 / u_in)
                v = 1.0 / inv_v
                st.markdown("**Step 1 — Signs**")
                st.write(f"f = **{f_in} cm**, u = **{u_in} cm**")
                st.markdown("**Step 2 — Lens formula**")
                st.latex(r"\frac{1}{v} - \frac{1}{u} = \frac{1}{f}")
                st.write(
                    f"1/v = 1/f + 1/u = **{inv_v:.4f}**  →  v = **{_fmt_cm(v)}**"
                )
                if v > 0:
                    st.success("v > 0 → **real image** on the opposite side of the lens.")
                else:
                    st.success("v < 0 → **virtual image** on the same side as the object.")
                if h_in is not None and u_in != 0:
                    m = v / u_in
                    h_prime = m * h_in
                    st.markdown("**Step 3 — Magnification m = v/u**")
                    st.write(
                        f"m = **{m:.3f}** · |h'| = **{abs(h_prime):.1f} cm** "
                        f"({'inverted' if m < 0 else 'erect'})"
                    )
            else:
                assert v_in is not None
                if v_in == 0:
                    st.error("v cannot be zero.")
                    return
                inv_u = (1.0 / v_in) - (1.0 / f_in)
                u = 1.0 / inv_u
                st.markdown("**Step 1 — Given**")
                st.write(f"f = **{f_in} cm**, v = **{v_in} cm**")
                st.markdown("**Step 2 — Rearrange for u**")
                st.latex(r"\frac{1}{u} = \frac{1}{v} - \frac{1}{f}")
                st.write(f"u = **{_fmt_cm(u)}** → object **{abs(u):.0f} cm** in front of the lens.")


def render_power_guided(*, power_d: float, label: str = "") -> None:
    """Power ↔ focal length."""
    with st.expander("🔢 Guided power / focal length", expanded=False):
        if label:
            st.caption(label)
        p_in = st.number_input(
            "Power P (dioptre, D)",
            value=float(power_d),
            step=0.5,
            key=f"hp_num_power_p_{label}",
        )
        if st.button("Check my steps", key=f"hp_num_power_go_{label}", type="primary"):
            if p_in == 0:
                st.error("Power cannot be zero.")
                return
            f_m = 1.0 / p_in
            f_cm = f_m * 100
            st.markdown("**Formula:** P = 1/f  (f in **metres**)")
            st.write(f"f = 1/({p_in}) = **{f_m:.3f} m** = **{f_cm:.1f} cm**")
            if p_in > 0:
                st.success("P > 0 → **converging (convex)** lens.")
            else:
                st.success("P < 0 → **diverging (concave)** lens.")


def render_guided_for_question(q: dict) -> None:
    tool = q.get("guided_tool")
    if not tool:
        return
    defaults = tool.get("defaults") or {}
    label = str(defaults.get("label") or q.get("id", ""))
    kind = tool.get("type")
    if kind == "mirror":
        render_mirror_guided(
            mirror=str(defaults.get("mirror", "concave")),
            f_cm=float(defaults.get("f_cm", -15)),
            u_cm=float(defaults.get("u_cm", -20)),
            h_cm=float(defaults["h_cm"]) if defaults.get("h_cm") is not None else None,
            label=label,
        )
    elif kind == "lens":
        render_lens_guided(
            f_cm=float(defaults.get("f_cm", 10)),
            u_cm=float(defaults["u_cm"]) if defaults.get("u_cm") is not None else None,
            v_cm=float(defaults["v_cm"]) if defaults.get("v_cm") is not None else None,
            h_cm=float(defaults["h_cm"]) if defaults.get("h_cm") is not None else None,
            label=label,
        )
    elif kind == "power":
        render_power_guided(
            power_d=float(defaults.get("power_d", 1.5)),
            label=label,
        )
