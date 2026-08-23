"""Streamlit UI — Harshit Chemistry, Unit 1 (Chemical Reactions and Equations)."""

from __future__ import annotations

import streamlit as st

import database as db
from . import components as hpco
from . import content as hpc
from . import state as hps


def _back_dashboard():
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_activity = None


def _open_chemistry_home():
    st.session_state.current_page = "harshit_chemistry_home"


def _unit_id() -> int:
    return int(st.session_state.get("hc_unit_id", hpc.UNIT_ID))


def _open_unit_home(unit_id: int) -> None:
    st.session_state.hc_unit_id = unit_id
    st.session_state.current_page = f"harshit_chemistry_unit{unit_id}"


def _open_unit1_home():
    _open_unit_home(1)


def _open_unit2_home():
    _open_unit_home(2)


def _open_unit3_home():
    _open_unit_home(3)


def _open_unit4_home():
    _open_unit_home(4)


def _concept_state_key(day_id: int, unit_id: int | None = None) -> str:
    uid = unit_id if unit_id is not None else _unit_id()
    return f"hc_concept_{uid}_{day_id}"


def _open_concept_day(day_id: int, *, show_menu: bool = True, unit_id: int | None = None) -> None:
    uid = unit_id if unit_id is not None else _unit_id()
    st.session_state.hc_unit_id = uid
    st.session_state.hc_day_id = day_id
    st.session_state.hc_mode = "concept"
    st.session_state.current_page = "harshit_chemistry_concept"
    key = _concept_state_key(day_id, uid)
    if key not in st.session_state:
        st.session_state[key] = hps.ConceptSessionState(day_id=day_id).to_dict()
    if show_menu:
        st.session_state.hc_show_day_menu = day_id
    else:
        st.session_state.pop("hc_show_day_menu", None)


def _concepts_viewed_for_day(day_id: int, unit_id: int | None = None) -> int:
    uid = unit_id if unit_id is not None else _unit_id()
    viewed = _all_viewed_ids(uid)
    return sum(1 for c in hpc.concepts_for_day(day_id, unit_id=uid) if c["id"] in viewed)


def _is_first_visit(day_id: int, unit_id: int | None = None) -> bool:
    uid = unit_id if unit_id is not None else _unit_id()
    state = _get_concept_state(day_id, uid)
    if state.concept_index > 0 or state.viewed:
        return False
    return _concepts_viewed_for_day(day_id, uid) == 0


def _reset_concept_day(day_id: int, *, concept_index: int = 0, unit_id: int | None = None) -> None:
    uid = unit_id if unit_id is not None else _unit_id()
    state = _get_concept_state(day_id, uid)
    state.concept_index = concept_index
    state.show_simpler = False
    state.show_example = False
    state.show_visual_again = False
    _save_concept_state(state, uid)
    st.session_state.pop("hc_show_day_menu", None)


def _get_concept_state(day_id: int, unit_id: int | None = None) -> hps.ConceptSessionState:
    uid = unit_id if unit_id is not None else _unit_id()
    key = _concept_state_key(day_id, uid)
    return hps.ConceptSessionState.from_dict(st.session_state.get(key, {"day_id": day_id}))


def _save_concept_state(state: hps.ConceptSessionState, unit_id: int | None = None) -> None:
    uid = unit_id if unit_id is not None else _unit_id()
    st.session_state[_concept_state_key(state.day_id, uid)] = state.to_dict()


def _user_id() -> int | None:
    user = db.get_user("Harshit Sai")
    return user["id"] if user else None


def _all_viewed_ids(unit_id: int | None = None) -> set[str]:
    uid = unit_id if unit_id is not None else _unit_id()
    user = db.get_user("Harshit Sai")
    if not user:
        return set()
    return set(db.get_harshit_chemistry_viewed_concepts(user["id"], unit_id=uid))


def _persist_concept_view(concept_id: str, *, marked_review: bool, unit_id: int | None = None) -> None:
    uid = unit_id if unit_id is not None else _unit_id()
    user = db.get_user("Harshit Sai")
    if not user:
        return
    db.save_harshit_chemistry_concept_status(
        user["id"],
        unit_id=uid,
        concept_id=concept_id,
        viewed=True,
        marked_review=marked_review,
    )


def render_home() -> None:
    hpco.inject_chemistry_styles()
    if st.button("← Back to dashboard"):
        _back_dashboard()
        st.rerun()

    st.markdown("## 🧪 Chemistry")
    st.caption("NCERT Class 10 · building confidence through concepts first")
    st.markdown("")

    st.markdown(
        """
        <div style="background:#EEF1F5;padding:1.25rem;border-radius:8px;border-left:4px solid #6366F1;">
          <strong>Chemistry Confidence</strong> — understand and visualize before practice.
          No timers, no scores during concept learning.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")

    if st.button(
        "Unit 1 — Chemical Reactions and Equations",
        type="primary",
        use_container_width=True,
    ):
        _open_unit1_home()
        st.rerun()

    if st.button(
        "Unit 2 — Acids, Bases and Salts",
        use_container_width=True,
    ):
        _open_unit2_home()
        st.rerun()

    if st.button(
        "Unit 3 — Metals and Non-metals",
        use_container_width=True,
    ):
        _open_unit3_home()
        st.rerun()

    if st.button(
        "Unit 4 — Carbon and its Compounds",
        use_container_width=True,
    ):
        _open_unit4_home()
        st.rerun()


def render_unit_home(unit_id: int) -> None:
    umeta = hpc.unit_meta(unit_id)
    meta = hpc.meta(unit_id)
    hpco.inject_chemistry_styles(unit_id)
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← Chemistry"):
            _open_chemistry_home()
            st.rerun()

    st.markdown(f"## Unit {unit_id} — {umeta['title']}")
    st.caption(f"{meta.get('ncert', umeta['ncert'])} · 16 concept days + practice")
    pdf_name = umeta.get("pdf", "jesc101.pdf")
    pdf_path = hpc.unit_dir(unit_id) / pdf_name
    if pdf_path.is_file():
        with st.expander("📄 NCERT chapter (PDF)", expanded=False):
            try:
                st.pdf(pdf_path)
            except Exception:
                st.caption(str(pdf_path))
    st.markdown("")

    viewed = _all_viewed_ids(unit_id)
    total_active = hpc.total_concept_cards(active_only=True, unit_id=unit_id)
    stage1_done = hpc.practice_unlocked(viewed, unit_id=unit_id)
    user = db.get_user("Harshit Sai")
    review_ids = db.get_harshit_chemistry_review_concepts(user["id"], unit_id=unit_id) if user else []

    c1, c2, c3 = st.columns(3)
    with c1:
        all_ids = {
            c["id"]
            for d in hpc.list_days(stage=1, unit_id=unit_id)
            if d.get("active")
            for c in d.get("concepts", [])
        }
        st.metric("Concepts viewed", f"{len(viewed & all_ids)}/{total_active}")
    with c2:
        st.metric("Marked for review", len(review_ids))
    with c3:
        st.metric("Practice", "Ready" if stage1_done else "Locked")

    section_key = f"hc_unit{unit_id}_section"
    if section_key not in st.session_state:
        st.session_state[section_key] = "📚 Learn"

    section = st.radio(
        "Section",
        ["📚 Learn", "🎯 Practice", "⚙️ Practice Setup"],
        horizontal=True,
        key=section_key,
        label_visibility="collapsed",
    )

    st.markdown("---")

    if section == "🎯 Practice":
        from . import practice_ui as hppui

        hppui.render_practice_home(stage1_done=stage1_done, unit_id=unit_id)
        return

    if section == "⚙️ Practice Setup":
        from . import practice_ui as hppui

        if not stage1_done:
            st.info("Complete Stage 1 concept days to unlock practice.")
        else:
            hppui.render_setup_panel(unit_id=unit_id)
        return

    _render_unit_learn(viewed, review_ids, unit_id=unit_id)


def render_unit1_home() -> None:
    render_unit_home(1)


def render_unit2_home() -> None:
    render_unit_home(2)


def render_unit3_home() -> None:
    render_unit_home(3)


def render_unit4_home() -> None:
    render_unit_home(4)


def _render_unit_learn(viewed: set[str], review_ids: list[str], *, unit_id: int) -> None:
    st.markdown("### Stage 1 — Learn concepts")
    st.caption("Exposure and familiarization — not reported as mastery.")

    for day in hpc.list_days(stage=1, unit_id=unit_id):
        day_id = day["day"]
        concepts = day.get("concepts") or []
        active = day.get("active", False)
        done = sum(1 for c in concepts if c["id"] in viewed)
        total = len(concepts)
        label = f"Day {day_id} — {day['title']}"
        if not active:
            label += " (coming soon)"
        progress = f"{done}/{total} viewed" if active else "Not yet available"

        cols = st.columns([4, 1])
        with cols[0]:
            st.markdown(f"**{label}**")
            st.caption(progress)
        with cols[1]:
            if active and st.button("Open", key=f"hc_open_u{unit_id}_day_{day_id}"):
                _open_concept_day(day_id, unit_id=unit_id)
                st.rerun()

    if review_ids:
        st.markdown("---")
        with st.expander("Cards marked for review"):
            for cid in review_ids:
                concept = hpc.get_concept(cid, unit_id=unit_id)
                if concept and st.button(f"Review: {concept['name']}", key=f"hc_rev_u{unit_id}_{cid}"):
                    day = next(
                        d
                        for d in hpc.list_days(unit_id=unit_id)
                        if any(c["id"] == cid for c in d.get("concepts", []))
                    )
                    _open_concept_day(day["day"], show_menu=False, unit_id=unit_id)
                    _reset_concept_day(
                        day["day"],
                        concept_index=next(i for i, c in enumerate(day["concepts"]) if c["id"] == cid),
                        unit_id=unit_id,
                    )
                    st.rerun()


def _render_day_menu(day_id: int, day: dict, *, unit_id: int) -> None:
    """Let Harshit start from the beginning, continue, or pick a concept."""
    concepts = day.get("concepts") or []
    state = _get_concept_state(day_id, unit_id)
    total = len(concepts)
    viewed_count = _concepts_viewed_for_day(day_id, unit_id)
    idx = min(state.concept_index, total)
    at_end = state.concept_index >= total

    st.markdown(f"### Day {day_id} — {day['title']}")
    st.caption(f"{viewed_count}/{total} concepts viewed · exposure only, not mastery")

    if st.button(f"← Unit {unit_id}"):
        st.session_state.pop("hc_show_day_menu", None)
        _open_unit_home(unit_id)
        st.rerun()

    st.markdown("")
    if st.button("Start from concept 1", type="primary", use_container_width=True):
        _reset_concept_day(day_id, concept_index=0, unit_id=unit_id)
        st.rerun()

    if not at_end and idx > 0:
        name = concepts[idx]["name"] if idx < total else ""
        label = f"Continue from concept {idx + 1}"
        if name:
            label += f" — {name}"
        if st.button(label, use_container_width=True):
            st.session_state.pop("hc_show_day_menu", None)
            st.rerun()

    st.markdown("**Jump to a concept**")
    options = [f"{i + 1}. {c['name']}" for i, c in enumerate(concepts)]
    pick = st.selectbox("Choose a concept", options, label_visibility="collapsed", key=f"hc_pick_u{unit_id}_{day_id}")
    if st.button("Open selected concept", use_container_width=True):
        pick_idx = options.index(pick)
        _reset_concept_day(day_id, concept_index=pick_idx, unit_id=unit_id)
        st.rerun()


def _simpler_text(concept: dict) -> str:
    base = concept.get("simple_answer", "")
    first = base.split(".")[0].strip()
    return first + "." if first else base


def render_concept_card() -> None:
    unit_id = _unit_id()
    umeta = hpc.unit_meta(unit_id)
    hpco.inject_chemistry_styles(unit_id)
    day_id = st.session_state.get("hc_day_id", 1)
    day = hpc.get_day(day_id, unit_id=unit_id)
    if not day or not day.get("active"):
        st.warning("This day is not available yet.")
        if st.button(f"← Unit {unit_id}"):
            _open_unit_home(unit_id)
            st.rerun()
        return

    show_menu = st.session_state.get("hc_show_day_menu") == day_id
    if show_menu and not _is_first_visit(day_id, unit_id):
        _render_day_menu(day_id, day, unit_id=unit_id)
        return
    if show_menu and _is_first_visit(day_id, unit_id):
        st.session_state.pop("hc_show_day_menu", None)

    state = _get_concept_state(day_id, unit_id)
    concepts = day.get("concepts") or []
    concept = state.current_concept()
    if not concept:
        st.success("You have viewed all concepts in this session.")
        st.caption("Start again from concept 1, or pick any concept to revisit.")
        if st.button("Choose where to start", type="primary"):
            st.session_state.hc_show_day_menu = day_id
            st.rerun()
        if st.button(f"← Unit {unit_id} home"):
            _open_unit_home(unit_id)
            st.rerun()
        return

    idx = state.concept_index
    st.caption(f"Unit {unit_id} · Day {day_id} · {day['title']} · Concept {idx + 1} of {len(concepts)}")

    if st.button(f"← Unit {unit_id}"):
        _open_unit_home(unit_id)
        st.rerun()

    hpco.render_glossary_sidebar(hpc.glossary(unit_id))

    st.markdown(f'<div class="hp-concept-name">{concept["name"]}</div>', unsafe_allow_html=True)

    if state.show_visual_again or not state.show_simpler:
        hpco.render_concept_visual(
            concept.get("visual") or {},
            concept_id=concept.get("id", ""),
            concept_name=concept.get("name", ""),
            unit_id=unit_id,
        )

    st.markdown('<div class="hp-section-label">Simple answer</div>', unsafe_allow_html=True)
    text = _simpler_text(concept) if state.show_simpler else concept.get("simple_answer", "")
    st.markdown(f'<div class="hp-body">{text}</div>', unsafe_allow_html=True)

    if concept.get("why"):
        st.markdown('<div class="hp-section-label">Why it matters</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hp-body">{concept["why"]}</div>', unsafe_allow_html=True)

    if state.show_example and concept.get("example"):
        st.markdown('<div class="hp-section-label">Example</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hp-body">{concept["example"]}</div>', unsafe_allow_html=True)

    if concept.get("remember"):
        st.markdown(
            f'<div class="hp-remember"><strong>Remember:</strong> {concept["remember"]}</div>',
            unsafe_allow_html=True,
        )

    if concept.get("common_confusion"):
        st.markdown(
            f'<div class="hp-confusion"><strong>Common confusion:</strong> {concept["common_confusion"]}</div>',
            unsafe_allow_html=True,
        )

    if concept.get("optional_detail"):
        with st.expander("Explain more"):
            st.markdown(concept["optional_detail"])

    st.markdown("---")
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("Show me an example"):
            state.show_example = True
            _save_concept_state(state, unit_id)
            st.rerun()
    with b2:
        if st.button("Explain more simply"):
            state.show_simpler = True
            _save_concept_state(state, unit_id)
            st.rerun()
    with b3:
        if st.button("Show the visual again"):
            state.show_visual_again = True
            _save_concept_state(state, unit_id)
            st.rerun()

    marked = concept["id"] in state.marked_review
    if st.button("★ Mark for review" if not marked else "✓ Marked for review"):
        state.toggle_review(concept["id"])
        _save_concept_state(state, uid)
        _persist_concept_view(concept["id"], marked_review=concept["id"] in state.marked_review, unit_id=unit_id)
        st.rerun()

    st.markdown("")
    is_last = idx >= len(concepts) - 1
    btn_label = "Done" if is_last else "Next concept →"
    if st.button(btn_label, type="primary", use_container_width=True):
        cid = concept["id"]
        _persist_concept_view(cid, marked_review=cid in state.marked_review, unit_id=unit_id)
        state.advance()
        _save_concept_state(state, unit_id)
        if is_last:
            user = db.get_user("Harshit Sai")
            if user:
                db.update_harshit_chemistry_day_status(
                    user["id"],
                    unit_id=unit_id,
                    day_id=day_id,
                    status="complete",
                    concepts_viewed=len(concepts),
                    concepts_total=len(concepts),
                )
            _open_unit_home(unit_id)
        st.rerun()
