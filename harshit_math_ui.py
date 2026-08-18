"""Streamlit UI for Harshit Sai — NCERT Class 9 PreReqs + Phase 1 intervention."""

from __future__ import annotations

import time
import uuid

import streamlit as st

import database as db
import edgenuity_practice_email as ec3mail
import google_sheets_sync as gss
import harshit_math_components as hmc_ui
import harshit_math_content as hmc
import harshit_math_prereqs as hmp
import harshit_math_state as hms


def _back_dashboard():
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_activity = None


def _open_day(day_id: int):
    st.session_state.hm_day_id = day_id
    st.session_state.hm_problem_idx = 0
    st.session_state.current_page = "harshit_math_day"


def _open_prereq_bucket(prereq_id: int):
    st.session_state.hm_prereq_id = prereq_id
    st.session_state.current_page = "harshit_prereq_bucket"


def _open_prereq_chapter(prereq_id: int, chapter_num: int):
    st.session_state.hm_prereq_id = prereq_id
    st.session_state.hm_chapter_num = chapter_num
    st.session_state.current_page = "harshit_prereq_chapter"


def _open_problem(day_id: int, problem_id: str):
    st.session_state.hm_day_id = day_id
    st.session_state.hm_problem_id = problem_id
    st.session_state.current_page = "harshit_math_problem"
    key = f"hm_sm_{problem_id}"
    if key not in st.session_state:
        st.session_state[key] = hms.ProblemStateMachine(problem_id).to_dict()
    if f"hm_visual_done_{problem_id}" not in st.session_state:
        st.session_state[f"hm_visual_done_{problem_id}"] = False


def _get_sm(problem_id: str) -> hms.ProblemStateMachine:
    key = f"hm_sm_{problem_id}"
    data = st.session_state.get(key, {})
    return hms.ProblemStateMachine.from_dict(problem_id, data)


def _save_sm(sm: hms.ProblemStateMachine) -> None:
    st.session_state[f"hm_sm_{sm.problem_id}"] = sm.to_dict()


def _render_feedback(text: str | None, *, success: bool = False) -> None:
    if not text:
        return
    cls = "hm-success" if success else "hm-feedback"
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)


def _prereq_progress_label(prereq: dict, summary: dict) -> str:
    total = len(prereq.get("class9_chapters", []))
    pid = prereq["id"]
    bucket = summary.get(pid, {})
    done = bucket.get("complete", 0)
    if done >= total and total > 0:
        return "Complete"
    if bucket.get("in_progress") or done:
        return f"In progress · {done}/{total} chapters"
    return f"{total} chapter{'s' if total != 1 else ''}"


def _render_prereqs_tab(user: dict | None):
    summary = db.get_harshit_prereq_summary(user["id"]) if user else {}

    st.markdown(
        '<p style="color:var(--hm-text-secondary);margin-bottom:1.5rem;">'
        "Six PreReq buckets — each has <strong>Week Setup</strong> (topics & levels) and "
        "<strong>Practice</strong> like Edgenuity linear equations.</p>",
        unsafe_allow_html=True,
    )

    search_paths = hmp.chapter_search_paths()
    if search_paths:
        st.caption("Chapter files loaded from: " + " · ".join(str(p) for p in search_paths))
    else:
        st.info(
            "Add chapter notes or PDFs to `HarshitMath/class9_chapters/chapter_XX/`. "
            "Optional: set `HARSHIT_CLASS9_CHAPTERS` env var for an external folder."
        )

    cols = st.columns(2, gap="large")
    for i, prereq in enumerate(hmp.list_prereqs()):
        ch_count = len(prereq.get("class9_chapters", []))
        g10 = prereq.get("feeds_into_grade10", {})
        g10_titles = ", ".join(
            f"Ch {c['number']}: {c['title']}" for c in g10.get("chapters", [])
        )
        progress = _prereq_progress_label(prereq, summary)
        wc = db.get_harshit_prereq_week_config(prereq["id"]) if user else {}
        plan_label = (
            f"Plan: {len(wc.get('topics', []))} topic(s)"
            if wc.get("topics")
            else "Plan: not configured"
        )

        with cols[i % 2]:
            st.markdown(
                f"""
<div style="background:var(--hm-bg-surface,#fff);border:1px solid var(--hm-border-subtle,#D8DEE6);
     border-radius:8px;padding:1.35rem;margin-bottom:0.75rem;min-height:11rem;">
  <div style="font-size:1.75rem;margin-bottom:0.35rem;">{prereq.get('emoji','')}</div>
  <div style="color:var(--hm-text-secondary);font-size:0.82rem;">PreReq {prereq['id']}</div>
  <div style="color:var(--hm-text-primary);font-size:1.05rem;font-weight:600;margin:0.35rem 0;">
    {prereq['title']}
  </div>
  <div style="color:var(--hm-text-secondary);font-size:0.88rem;line-height:1.45;">
    {prereq.get('summary','')}
  </div>
  <div style="color:var(--hm-text-secondary);font-size:0.8rem;margin-top:0.65rem;">
    Class 9: {ch_count} chapter{'s' if ch_count != 1 else ''} · {progress}<br>
    {plan_label}
  </div>
</div>
""",
                unsafe_allow_html=True,
            )
            if st.button(
                f"Open PreReq {prereq['id']}",
                key=f"hm_prereq_{prereq['id']}",
                use_container_width=True,
            ):
                _open_prereq_bucket(prereq["id"])
                st.rerun()

            with st.expander("Feeds into Grade 10"):
                st.caption(g10_titles)
                for topic in g10.get("topics", []):
                    st.markdown(f"- {topic}")


def _render_phase1_tab(user: dict | None):
    day_status = db.get_harshit_day_status(user["id"]) if user else {}

    st.markdown(
        '<p style="color:var(--hm-text-secondary);margin-bottom:1rem;">'
        "10-day Number Sense bootcamp — NCERT Chapter 1 deep practice "
        "(visual manipulatives, step-by-step, error-catching).</p>",
        unsafe_allow_html=True,
    )

    cols = st.columns(2, gap="large")
    for i, day in enumerate(hmc.list_days()):
        did = day["day"]
        status = day_status.get(did, {})
        st_status = status.get("status", "not_started")
        label = {
            "not_started": "Not started",
            "in_progress": "In progress",
            "complete": "Complete",
        }.get(st_status, st_status)

        with cols[i % 2]:
            st.markdown(
                f"""
<div style="background:var(--hm-bg-surface,#fff);border:1px solid var(--hm-border-subtle,#D8DEE6);
     border-radius:8px;padding:1.25rem;margin-bottom:0.75rem;">
  <div style="color:var(--hm-text-secondary);font-size:0.85rem;">Day {did}</div>
  <div style="color:var(--hm-text-primary);font-size:1.05rem;font-weight:600;margin:0.35rem 0;">
    {day['title']}
  </div>
  <div style="color:var(--hm-text-secondary);font-size:0.9rem;">{label}</div>
</div>
""",
                unsafe_allow_html=True,
            )
            if st.button(f"Open Day {did}", key=f"hm_day_{did}", use_container_width=True):
                _open_day(did)
                st.rerun()


def render_home():
    hmc_ui.inject_harshit_styles()
    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="hm_back_dash"):
            _back_dashboard()
            st.rerun()

    st.markdown(
        f"""
<div style="text-align:center;padding:1.5rem 0 1.25rem;">
  <h1 style="font-size:2rem;color:var(--hm-text-primary,#1E293B);font-weight:600;">
    {name} — PreReq
  </h1>
  <p style="color:var(--hm-text-secondary,#64748B);max-width:40rem;margin:0.5rem auto;">
    NCERT Class 9 foundations — six units before 10th grade.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    tab_prereqs, tab_phase1 = st.tabs(["📚 PreReq Units", "🔢 Phase 1 — Number Sense"])
    with tab_prereqs:
        _render_prereqs_tab(user)
    with tab_phase1:
        _render_phase1_tab(user)


def render_prereq_bucket():
    hmc_ui.inject_harshit_styles()
    prereq_id = st.session_state.get("hm_prereq_id", 1)
    prereq = hmp.get_prereq(prereq_id)
    if not prereq:
        st.error("PreReq not found.")
        return

    user = db.get_user(st.session_state.selected_user)
    chapter_status = db.get_harshit_prereq_chapter_status(user["id"], prereq_id) if user else {}

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← PreReqs", key="hm_back_prereqs"):
            st.session_state.current_page = "harshit_math_home"
            st.rerun()

    st.markdown(
        f'<p class="hm-prompt">PreReq {prereq_id} · {prereq["title"]}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p style="color:var(--hm-text-secondary);">{prereq.get("summary","")}</p>', unsafe_allow_html=True)

    tab_overview, tab_practice, tab_setup = st.tabs(["📘 Chapters", "🎯 Practice", "📅 Week Setup"])

    with tab_overview:
        _render_prereq_overview(prereq, prereq_id, chapter_status)

    with tab_practice:
        import harshit_prereq_practice_ui as hppui

        hppui.render_practice_home(prereq_id)

    with tab_setup:
        import harshit_prereq_practice_ui as hppui

        hppui.render_setup_panel(prereq_id)


def _render_prereq_overview(prereq: dict, prereq_id: int, chapter_status: dict):
    st.markdown("**Focus areas**")
    for item in prereq.get("focus", []):
        st.markdown(f"- {item}")

    g10 = prereq.get("feeds_into_grade10", {})
    if g10.get("chapters"):
        st.markdown("**Feeds into Grade 10**")
        for ch in g10["chapters"]:
            st.markdown(f"- Chapter {ch['number']}: {ch['title']}")
        for topic in g10.get("topics", []):
            st.caption(f"→ {topic}")

    if prereq.get("phase1_link"):
        st.markdown("---")
        st.markdown("**Phase 1 bootcamp** — interactive Number Sense for Chapter 1.")
        if st.button("Open Phase 1 (Days 1–10)", key="hm_goto_phase1", type="secondary"):
            st.session_state.current_page = "harshit_math_home"
            st.rerun()

    st.markdown("---")
    st.markdown("**Class 9 chapters**")
    for ch in prereq.get("class9_chapters", []):
        num = ch["number"]
        assets = hmp.resolve_chapter_assets(num, ch.get("folder_aliases"))
        st_label = chapter_status.get(num, {}).get("status", "not_started")
        status_label = {
            "not_started": "Not started",
            "in_progress": "In progress",
            "complete": "Complete",
        }.get(st_label, st_label)
        content_label = hmp.chapter_status_label(assets)

        st.markdown(
            f"""
<div style="background:var(--hm-bg-surface,#fff);border:1px solid var(--hm-border-subtle,#D8DEE6);
     border-radius:8px;padding:1rem 1.15rem;margin-bottom:0.65rem;">
  <div style="font-weight:600;color:var(--hm-text-primary);">
    Chapter {num}: {ch['title']}
  </div>
  <div style="color:var(--hm-text-secondary);font-size:0.88rem;margin-top:0.35rem;">
    {content_label} · {status_label}
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        if st.button(f"Open Chapter {num}", key=f"hm_ch_{prereq_id}_{num}", use_container_width=True):
            _open_prereq_chapter(prereq_id, num)
            st.rerun()


def render_prereq_chapter():
    hmc_ui.inject_harshit_styles()
    prereq_id = st.session_state.get("hm_prereq_id", 1)
    chapter_num = st.session_state.get("hm_chapter_num", 1)
    prereq = hmp.get_prereq(prereq_id)
    user = db.get_user(st.session_state.selected_user)

    ch_meta = None
    if prereq:
        ch_meta = next(
            (c for c in prereq.get("class9_chapters", []) if c["number"] == chapter_num),
            None,
        )
    title = ch_meta["title"] if ch_meta else f"Chapter {chapter_num}"
    aliases = ch_meta.get("folder_aliases") if ch_meta else None
    assets = hmp.resolve_chapter_assets(chapter_num, aliases)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Bucket", key="hm_back_bucket"):
            st.session_state.current_page = "harshit_prereq_bucket"
            st.rerun()

    st.markdown(
        f'<div class="hm-problem">Chapter {chapter_num}: {title}</div>',
        unsafe_allow_html=True,
    )
    if prereq:
        st.caption(f"PreReq {prereq_id} — {prereq['title']}")

    if user:
        saved = db.get_harshit_prereq_chapter_status(user["id"], prereq_id).get(chapter_num, {})
        status = st.selectbox(
            "Your progress",
            options=["not_started", "in_progress", "complete"],
            index=["not_started", "in_progress", "complete"].index(
                saved.get("status", "not_started")
            ),
            format_func=lambda s: {
                "not_started": "Not started",
                "in_progress": "In progress",
                "complete": "Complete",
            }[s],
            key=f"hm_ch_status_{prereq_id}_{chapter_num}",
        )
        if st.button("Save progress", key=f"hm_save_ch_{prereq_id}_{chapter_num}", type="secondary"):
            db.save_harshit_prereq_chapter_status(
                user["id"], prereq_id, chapter_num, status=status
            )
            st.rerun()

    st.markdown("---")

    if prereq_id == 1 and chapter_num == 1:
        st.markdown("**Interactive practice** — Phase 1 Number Sense bootcamp for this chapter.")
        if st.button("Start Phase 1 Day 1", key="hm_ch1_phase1", type="secondary"):
            _open_day(1)
            st.rerun()

    if not assets["has_content"]:
        st.info(
            "No chapter files found yet. Add notes or PDFs to "
            "`HarshitMath/class9_chapters/chapter_XX/` "
            "(supported: `.md`, `.txt`, `.pdf`)."
        )
        return

    if assets["markdown"]:
        st.markdown("**Chapter notes**")
        for md_path in assets["markdown"]:
            with st.expander(md_path.name, expanded=len(assets["markdown"]) == 1):
                st.markdown(hmp.read_markdown_preview(md_path))

    if assets["pdfs"]:
        st.markdown("**PDF materials**")
        for pdf_path in assets["pdfs"]:
            st.markdown(f"- `{pdf_path.name}`")
            try:
                st.pdf(pdf_path)
            except Exception:
                st.caption(f"PDF at: {pdf_path}")


def render_day():
    hmc_ui.inject_harshit_styles()
    day_id = st.session_state.get("hm_day_id", 1)
    day = hmc.get_day(day_id)
    if not day:
        st.error("Day not found.")
        return

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Phase 1", key="hm_back_home"):
            st.session_state.current_page = "harshit_math_home"
            st.rerun()

    st.markdown(
        f'<p class="hm-prompt">Day {day_id} · {day["title"]}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p style="color:var(--hm-text-secondary);">{day["core_concept"]}</p>', unsafe_allow_html=True)
    st.caption(day.get("ncert_reference", ""))

    prob = day.get("ncert_problem", {})
    if st.button("Begin problem", key="hm_begin_prob", type="secondary"):
        _open_problem(day_id, prob["id"])
        st.rerun()

    st.markdown("---")
    st.markdown(f'**Today\'s problem:** {prob.get("statement", "")}')


def render_problem():
    hmc_ui.inject_harshit_styles()
    day_id = st.session_state.get("hm_day_id", 1)
    problem_id = st.session_state.get("hm_problem_id", "d2_p1")
    day = hmc.get_day(day_id)
    user = db.get_user(st.session_state.selected_user)

    sm = _get_sm(problem_id)
    node = sm.node()

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Day", key="hm_back_day"):
            st.session_state.current_page = "harshit_math_day"
            st.rerun()

    prob = day.get("ncert_problem", {}) if day else {}
    st.markdown(f'<div class="hm-problem">{prob.get("statement", "")}</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="hm-prompt">{node.get("prompt", "")}</p>', unsafe_allow_html=True)

    feedback_key = f"hm_feedback_{problem_id}"

    if sm.is_complete():
        _render_feedback("This problem is complete.", success=True)
        if user:
            db.save_harshit_problem_progress(
                user["id"],
                day_id,
                problem_id,
                current_node=sm.current_node,
                step_index=99,
                visual_complete=True,
                state=sm.to_dict(),
                completed=True,
            )
            db.update_harshit_day_status(
                user["id"],
                day_id,
                status="complete",
                problems_completed=1,
                problems_total=1,
            )
        if st.button("Return to day", key="hm_done_back"):
            st.session_state.current_page = "harshit_math_day"
            st.rerun()
        return

    if sm.requires_visual():
        cfg = node.get("config", {})
        vmin = float(cfg.get("min", -10))
        vmax = float(cfg.get("max", 10))
        mode = cfg.get("mode", "single_marker")

        if mode == "interval_select":
            st.caption("Select the interval by choosing low and high bounds.")
            c1, c2 = st.columns(2)
            with c1:
                lo = st.number_input("Lower bound", value=1.0, step=1.0, key=f"hm_lo_{problem_id}")
            with c2:
                hi = st.number_input("Upper bound", value=2.0, step=1.0, key=f"hm_hi_{problem_id}")
            if st.button("Confirm interval", key=f"hm_vis_{problem_id}"):
                ok, tkey, fb = sm.validate_visual(None, interval=(lo, hi))
                if ok:
                    sm.advance_after_visual(tkey or "interval_correct")
                    st.session_state[feedback_key] = fb
                    st.session_state[f"hm_visual_done_{problem_id}"] = True
                else:
                    st.session_state[feedback_key] = fb
                _save_sm(sm)
                st.rerun()
        else:
            val = st.slider(
                "Place marker on number line",
                min_value=vmin,
                max_value=vmax,
                value=float(cfg.get("target", 0)),
                step=0.5,
                key=f"hm_slider_{problem_id}_{sm.current_node}",
            )
            hmc_ui.render_number_line_static(min_val=vmin, max_val=vmax, marker=val)
            if st.button("Confirm placement", key=f"hm_vis_{problem_id}_{sm.current_node}"):
                ok, tkey, fb = sm.validate_visual(val)
                if ok:
                    sm.advance_after_visual(tkey or "visual_correct")
                    st.session_state[f"hm_visual_done_{problem_id}"] = True
                st.session_state[feedback_key] = fb if not ok else fb
                _save_sm(sm)
                st.rerun()

    elif node.get("type") in ("intermediate_input", "final_input"):
        ans = st.text_input(
            "Your answer",
            key=f"hm_input_{problem_id}_{sm.current_node}",
            label_visibility="collapsed",
        )
        if st.button("Continue", key=f"hm_submit_{problem_id}_{sm.current_node}", type="secondary"):
            ok, fb = sm.validate_input(ans)
            st.session_state[feedback_key] = fb
            _save_sm(sm)
            if ok and sm.is_complete() and user:
                elapsed = int(time.time() - st.session_state.get("hm_start_time", time.time()))
                report = {"score_pct": 100, "strengths": [{"name": day.get("title", ""), "pct": 100}]}
                try:
                    ec3mail.send_practice_report_email(
                        student_name=st.session_state.selected_user,
                        unit_title=f"Harshit Day {day_id}",
                        unit_subtitle=hmc.PHASE_TITLE,
                        report=report,
                        time_spent_seconds=elapsed,
                        session_meta={"problem_id": problem_id},
                    )
                except Exception:
                    pass
                try:
                    gss.persist_ec3_practice_result(
                        user_name=st.session_state.selected_user,
                        user_id=user["id"],
                        session_id=str(uuid.uuid4()),
                        session_kind="harshit_phase1",
                        unit_id=day_id + hmc.SESSION_UNIT_OFFSET,
                        unit_label=f"Day {day_id}: {day.get('title', '')}",
                        score_pct=100,
                        correct_count=1,
                        total_count=1,
                        time_spent_seconds=elapsed,
                        report=report,
                        failed=[],
                        question_ids=[problem_id],
                    )
                except Exception:
                    pass
                db.save_activity_score(
                    user["id"],
                    "HarshitMath",
                    f"Day {day_id}",
                    score=100,
                    max_score=100,
                    time_spent_seconds=elapsed,
                )
            st.rerun()

    _render_feedback(st.session_state.get(feedback_key))
