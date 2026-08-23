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


def render_myopia_correction_guided(*, far_point_cm: float, label: str = "") -> None:
    """Corrective lens power when far point is in front of the eye."""
    with st.expander("🔢 Guided myopia correction", expanded=False):
        if label:
            st.caption(label)
        fp = st.number_input(
            "Far point (cm in front of eye)",
            value=float(far_point_cm),
            min_value=1.0,
            step=5.0,
            key=f"hp_num_myopia_fp_{label}",
        )
        if st.button("Check my steps", key=f"hp_num_myopia_go_{label}", type="primary"):
            f_cm = -fp
            f_m = f_cm / 100
            p = 1.0 / f_m
            st.markdown("**Step 1 — Lens type:** Concave (diverging) for myopia.")
            st.markdown("**Step 2 — Focal length:** For infinity object, f = −(far point) = "
                         f"**{f_cm:.0f} cm** = **{f_m:.2f} m**.")
            st.markdown("**Step 3 — Power:** P = 1/f = **{:.2f} D**.".format(p))


def render_hypermetropia_correction_guided(
    *,
    near_point_cm: float,
    normal_near_cm: float = 25,
    label: str = "",
) -> None:
    """Corrective convex lens power for hypermetropia."""
    with st.expander("🔢 Guided hypermetropia correction", expanded=False):
        if label:
            st.caption(label)
        np_cm = st.number_input(
            "Hypermetropic near point (cm)",
            value=float(near_point_cm),
            min_value=1.0,
            step=5.0,
            key=f"hp_num_hyper_np_{label}",
        )
        nn = st.number_input(
            "Normal near point (cm)",
            value=float(normal_near_cm),
            min_value=1.0,
            step=1.0,
            key=f"hp_num_hyper_nn_{label}",
        )
        if st.button("Check my steps", key=f"hp_num_hyper_go_{label}", type="primary"):
            u = -nn
            v = -np_cm
            inv_f = (1.0 / v) - (1.0 / u)
            f_m = 1.0 / inv_f
            f_cm = f_m * 100
            p = 1.0 / f_m
            st.markdown("**Step 1 — Lens type:** Convex (converging) for hypermetropia.")
            st.markdown(
                f"**Step 2 — Object at normal near point u = {u} cm; "
                f"image at eye near point v = {v} cm.**"
            )
            st.latex(r"\frac{1}{f} = \frac{1}{v} - \frac{1}{u}")
            st.markdown(
                f"**Step 3 —** f ≈ **{f_cm:.1f} cm** ({f_m:.3f} m) · P ≈ **{p:.1f} D** (convex)."
            )


def render_ohms_law_guided(*, voltage_v: float, current_a: float, label: str = "") -> None:
    with st.expander("🔢 Guided Ohm's law (V = IR)", expanded=False):
        if label:
            st.caption(label)
        v = st.number_input("Voltage V (volts)", value=float(voltage_v), step=1.0, key=f"hp_num_ohm_v_{label}")
        i = st.number_input(
            "Current I (amperes)",
            value=float(current_a),
            format="%.4f",
            step=0.001,
            key=f"hp_num_ohm_i_{label}",
        )
        if st.button("Check my steps", key=f"hp_num_ohm_go_{label}", type="primary"):
            if i == 0:
                st.error("Current cannot be zero.")
                return
            r = v / i
            st.markdown("**Formula:** V = I × R  →  R = V / I")
            st.write(f"R = {v} / {i} = **{r:.0f} Ω**" if r > 100 else f"R = {v} / {i} = **{r:.2f} Ω**")


def render_resistivity_wire_guided(
    *,
    resistivity: float,
    diameter_mm: float,
    resistance_ohm: float,
    label: str = "",
) -> None:
    import math

    with st.expander("🔢 Guided resistivity wire (R = ρL/A)", expanded=False):
        if label:
            st.caption(label)
        rho = st.number_input(
            "Resistivity ρ (Ω·m)",
            value=float(resistivity),
            format="%.2e",
            key=f"hp_num_rho_{label}",
        )
        d_mm = st.number_input(
            "Diameter (mm)",
            value=float(diameter_mm),
            step=0.1,
            key=f"hp_num_d_{label}",
        )
        r_target = st.number_input(
            "Required resistance (Ω)",
            value=float(resistance_ohm),
            step=1.0,
            key=f"hp_num_rt_{label}",
        )
        if st.button("Check my steps", key=f"hp_num_rho_go_{label}", type="primary"):
            r_m = (d_mm / 1000) / 2
            area = math.pi * r_m * r_m
            length = (r_target * area) / rho
            st.markdown("**Step 1 —** A = πr² with r = diameter/2 (in metres).")
            st.write(f"A ≈ **{area:.3e} m²**")
            st.markdown("**Step 2 —** L = RA/ρ")
            st.write(f"L ≈ **{length:.1f} m**")
            st.markdown("**Step 3 — If diameter is doubled**, area ×4, so R × (1/4) for same length:")
            st.write(f"New R ≈ **{r_target / 4:.2f} Ω**")


def render_series_circuit_guided(*, voltage_v: float, resistors: list[float], label: str = "") -> None:
    with st.expander("🔢 Guided series circuit", expanded=False):
        if label:
            st.caption(label)
        v = st.number_input("Battery voltage (V)", value=float(voltage_v), step=1.0, key=f"hp_num_ser_v_{label}")
        rs = ", ".join(str(r) for r in resistors)
        rs_in = st.text_input("Resistances in series (Ω, comma-separated)", value=rs, key=f"hp_num_ser_r_{label}")
        if st.button("Check my steps", key=f"hp_num_ser_go_{label}", type="primary"):
            parts = [float(x.strip()) for x in rs_in.split(",") if x.strip()]
            total = sum(parts)
            if total <= 0:
                st.error("Total resistance must be positive.")
                return
            current = v / total
            st.markdown("**Step 1 —** R_total = R₁ + R₂ + … = **{:.2f} Ω**".format(total))
            st.markdown("**Step 2 —** I = V/R_total (same through every series resistor)")
            st.write(f"I = **{current:.3f} A**")


def render_parallel_count_guided(
    *,
    voltage_v: float,
    current_a: float,
    resistor_ohm: float,
    label: str = "",
) -> None:
    with st.expander("🔢 Guided parallel resistors count", expanded=False):
        if label:
            st.caption(label)
        v = st.number_input("Line voltage (V)", value=float(voltage_v), step=10.0, key=f"hp_num_par_v_{label}")
        i = st.number_input("Total current (A)", value=float(current_a), step=1.0, key=f"hp_num_par_i_{label}")
        r = st.number_input("Each resistor (Ω)", value=float(resistor_ohm), step=1.0, key=f"hp_num_par_r_{label}")
        if st.button("Check my steps", key=f"hp_num_par_go_{label}", type="primary"):
            if r <= 0 or i <= 0 or v <= 0:
                st.error("Voltage, current, and resistance must be positive.")
                return
            r_total = v / i
            n_exact = (r * i) / v
            st.markdown("**Step 1 —** R_total = V/I = **{:.1f} Ω**".format(r_total))
            st.markdown("**Step 2 —** For n equal resistors in parallel: R_total = R/n  →  n = R/R_total = R×I/V")
            st.write(f"n = **{n_exact:.1f}** → need **{int(round(n_exact))}** resistors of {r:.0f} Ω")


def render_heating_power_guided(*, current_a: float, resistance_ohm: float, label: str = "") -> None:
    with st.expander("🔢 Guided heating power (P = I²R)", expanded=False):
        if label:
            st.caption(label)
        i = st.number_input("Current I (A)", value=float(current_a), step=1.0, key=f"hp_num_heat_i_{label}")
        r = st.number_input("Resistance R (Ω)", value=float(resistance_ohm), step=1.0, key=f"hp_num_heat_r_{label}")
        if st.button("Check my steps", key=f"hp_num_heat_go_{label}", type="primary"):
            p = i * i * r
            st.markdown("**Rate of heat (power):** P = I²R = VI = V²/R")
            st.write(f"P = ({i})² × {r} = **{p:.0f} W**")


def render_energy_compare_guided(
    *,
    power1_w: float,
    hours1: float,
    power2_w: float,
    minutes2: float,
    label: str = "",
) -> None:
    with st.expander("🔢 Guided energy comparison (E = Pt)", expanded=False):
        if label:
            st.caption(label)
        p1 = st.number_input("Device 1 power (W)", value=float(power1_w), key=f"hp_num_e1p_{label}")
        t1 = st.number_input("Device 1 time (hours)", value=float(hours1), key=f"hp_num_e1t_{label}")
        p2 = st.number_input("Device 2 power (W)", value=float(power2_w), key=f"hp_num_e2p_{label}")
        t2 = st.number_input("Device 2 time (minutes)", value=float(minutes2), key=f"hp_num_e2t_{label}")
        if st.button("Check my steps", key=f"hp_num_energy_go_{label}", type="primary"):
            e1 = p1 * t1 * 3600
            e2 = p2 * (t2 / 60) * 3600
            st.write(f"E₁ = P₁ × t = **{p1 * t1:.0f} Wh**")
            st.write(f"E₂ = P₂ × t = **{p2 * t2 / 60:.0f} Wh**")
            st.success("**{}** uses more energy.".format("Device 1" if e1 > e2 else "Device 2"))


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
    elif kind == "myopia_correction":
        render_myopia_correction_guided(
            far_point_cm=float(defaults.get("far_point_cm", 80)),
            label=label,
        )
    elif kind == "hypermetropia_correction":
        render_hypermetropia_correction_guided(
            near_point_cm=float(defaults.get("near_point_cm", 100)),
            normal_near_cm=float(defaults.get("normal_near_cm", 25)),
            label=label,
        )
    elif kind == "ohms_law":
        render_ohms_law_guided(
            voltage_v=float(defaults.get("voltage_v", 12)),
            current_a=float(defaults.get("current_a", 0.0025)),
            label=label,
        )
    elif kind == "resistivity_wire":
        render_resistivity_wire_guided(
            resistivity=float(defaults.get("resistivity", 1.6e-8)),
            diameter_mm=float(defaults.get("diameter_mm", 0.5)),
            resistance_ohm=float(defaults.get("resistance_ohm", 10)),
            label=label,
        )
    elif kind == "series_circuit":
        render_series_circuit_guided(
            voltage_v=float(defaults.get("voltage_v", 9)),
            resistors=list(defaults.get("resistors") or [0.2, 0.3, 0.4, 0.5, 12]),
            label=label,
        )
    elif kind == "parallel_count":
        render_parallel_count_guided(
            voltage_v=float(defaults.get("voltage_v", 220)),
            current_a=float(defaults.get("current_a", 5)),
            resistor_ohm=float(defaults.get("resistor_ohm", 176)),
            label=label,
        )
    elif kind == "heating_power":
        render_heating_power_guided(
            current_a=float(defaults.get("current_a", 5)),
            resistance_ohm=float(defaults.get("resistance_ohm", 44)),
            label=label,
        )
    elif kind == "energy_compare":
        render_energy_compare_guided(
            power1_w=float(defaults.get("power1_w", 250)),
            hours1=float(defaults.get("hours1", 1)),
            power2_w=float(defaults.get("power2_w", 1200)),
            minutes2=float(defaults.get("minutes2", 10)),
            label=label,
        )
