"""Streamlit UI for Arjun Edgenuity Course 3 Math — notes and daily practice."""

from __future__ import annotations

import os
import time

import streamlit as st

import arjun_edgenuity_course3_content as ec3
import arjun_edgenuity_course3_practice as ec3p
import arjun_edgenuity_course3_render as ec3r
import edgenuity_practice_email as ec3mail
import database as db
import google_sheets_sync as gss

try:
    import edgenuity_unit1_ui as u1ui
except ImportError:
    u1ui = None  # type: ignore[assignment]


def _xai_api_key() -> str | None:
    try:
        return st.secrets.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
    except Exception:
        return os.environ.get("XAI_API_KEY")


def _week_config() -> dict:
    return db.get_linear_eq_week_config()


def _back_dashboard():
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_activity = None


def _open_unit(unit_id: int):
    st.session_state.ec3_unit_id = unit_id
    st.session_state.ec3_activity_slug = None
    st.session_state.current_page = "edgenuity_course3_unit"


def _open_notes(unit_id: int, activity_slug: str | None = None):
    st.session_state.ec3_unit_id = unit_id
    st.session_state.ec3_activity_slug = activity_slug
    st.session_state.current_page = "edgenuity_course3_notes"


def _render_session_report(report: dict, unit_id: int, unit: dict):
    """Concise post-practice report: strengths, weak topics, revision links."""
    st.markdown("### 📊 Session Report")

    if report["score_pct"] == 100 and not report["needs_revision"]:
        st.success("**All topics strong today** — great work across every category.")

    col_str, col_rev = st.columns(2, gap="medium")

    with col_str:
        st.markdown("#### ✅ Doing well")
        if report["strengths"]:
            for item in report["strengths"]:
                st.markdown(
                    f"""
                    <div style="background:#ecfdf5;border-left:4px solid #10b981;padding:0.6rem 0.8rem;
                         border-radius:8px;margin-bottom:0.5rem;">
                        <strong>{item['emoji']} {item['name']}</strong>
                        <span style="color:#047857;"> — {item['correct']}/{item['total']} ({item['pct']}%)</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No topic hit 80% yet — focus on the review list below.")

    with col_rev:
        st.markdown("#### 📚 Needs revision")
        if report["needs_revision"]:
            for item in report["needs_revision"]:
                st.markdown(
                    f"""
                    <div style="background:#fff7ed;border-left:4px solid #f59e0b;padding:0.6rem 0.8rem;
                         border-radius:8px;margin-bottom:0.5rem;">
                        <strong>{item['emoji']} {item['name']}</strong>
                        <span style="color:#b45309;"> — {item['correct']}/{item['total']} ({item['pct']}%)</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.caption("Nothing flagged — keep practicing to stay exam-ready.")

    if report.get("tip"):
        st.info(f"**Focus next:** {report['tip']}")

    weak_with_notes = [
        r for r in report.get("needs_revision", [])
        if r.get("activity_slug") and unit.get("activities")
    ]
    if weak_with_notes:
        st.markdown("**Quick revision**")
        rev_cols = st.columns(min(len(weak_with_notes), 3))
        for i, item in enumerate(weak_with_notes[:3]):
            act = next(
                (a for a in unit["activities"] if a["slug"] == item["activity_slug"]),
                None,
            )
            if act and i < len(rev_cols):
                with rev_cols[i]:
                    if st.button(
                        f"📘 Activity {act['number']}: {act['title'][:28]}…"
                        if len(act["title"]) > 28
                        else f"📘 Activity {act['number']}: {act['title']}",
                        key=f"ec3_rev_{item['category']}",
                        use_container_width=True,
                    ):
                        _open_notes(unit_id, item["activity_slug"])
                        st.rerun()


def _start_practice(
    unit_id: int,
    *,
    show_spinner: bool = False,
    focus_category: str | None = None,
    focus_label: str | None = None,
    count: int | None = None,
):
    user = db.get_user(st.session_state.selected_user) if st.session_state.get("selected_user") else None
    exclude_ids = (
        db.get_recent_ec3_question_ids(user["id"], unit_id, ec3p.RECENT_SESSIONS_TO_AVOID)
        if user
        else set()
    )
    config = _week_config()
    api_key = _xai_api_key()
    use_llm = bool(config.get("use_llm"))
    question_count = count or (
        (u1ui.FOCUS_QUESTION_COUNT if u1ui and focus_category else 15)
    )

    def _build():
        if focus_category:
            return ec3p.build_focus_set(
                unit_id,
                focus_category,
                count=question_count,
                exclude_ids=exclude_ids,
                use_llm=use_llm,
                xai_api_key=api_key,
            )
        return ec3p.build_daily_set(
            count=question_count,
            unit_id=unit_id,
            exclude_ids=exclude_ids,
            use_llm=use_llm,
            xai_api_key=api_key,
        )

    if show_spinner and use_llm and api_key:
        with st.spinner("Generating fresh questions with xAI Grok…"):
            questions = _build()
    else:
        questions = _build()

    if not questions:
        st.session_state.ec3_warn = (
            f"Not enough questions for {focus_label or 'this unit'} — try full unit practice."
            if focus_category
            else "Could not load practice questions."
        )
        return

    if use_llm and not api_key:
        st.session_state.ec3_warn = (
            "AI generation is enabled in Week Setup but XAI_API_KEY is missing — "
            "used the built-in question bank instead."
        )
    elif use_llm and questions and questions[0].get("source") != "llm":
        st.session_state.ec3_warn = (
            "AI generation failed — used the built-in question bank instead."
        )
    else:
        st.session_state.pop("ec3_warn", None)

    st.session_state.ec3_unit_id = unit_id
    st.session_state.ec3_focus_category = focus_category
    st.session_state.ec3_focus_label = focus_label
    st.session_state.ec3_questions = questions
    st.session_state.ec3_current = 0
    st.session_state.ec3_answers = []
    st.session_state.ec3_last_feedback = None
    st.session_state.ec3_start_time = time.time()
    st.session_state.ec3_session_id = f"{unit_id}-{time.time()}"
    st.session_state.ec3_email_sent_for = None
    st.session_state.ec3_persist_saved_for = None
    st.session_state.ec3_review_mode = False
    st.session_state.ec3_review_index = 0
    st.session_state.current_page = "edgenuity_course3_practice"


def _render_ec3_review(questions: list, answers: list, unit_id: int, unit: dict):
    """Walk through graded questions one at a time to see mistakes."""
    total = len(questions)
    idx = st.session_state.get("ec3_review_index", 0)
    idx = max(0, min(idx, total - 1))
    st.session_state.ec3_review_index = idx

    q = questions[idx]
    ans = answers[idx] if idx < len(answers) else None
    cat_info = ec3p.get_categories(unit_id).get(q["category"], {})
    cat_color = cat_info.get("color", "#6366f1")
    cat_emoji = cat_info.get("emoji", "📐")
    cat_name = cat_info.get("name", "Math")

    col_back, col_title, _ = st.columns([1, 4, 1])
    with col_back:
        if st.button("← Results", key="ec3_review_back_results", use_container_width=True):
            st.session_state.ec3_review_mode = False
            st.rerun()
    with col_title:
        status = "✅ Correct" if ans and ans.get("correct") else "❌ Incorrect"
        st.markdown(
            f'<div style="text-align:center;color:#6b7280;font-size:0.95rem;padding-top:0.5rem;">'
            f"Review question {idx + 1} of {total} &nbsp;|&nbsp; {status}</div>",
            unsafe_allow_html=True,
        )

    progress = ((idx + 1) / total) if total > 0 else 0
    st.markdown(
        f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress * 100:.0f}%;height:100%;background:linear-gradient(90deg,#6366f1,#8b5cf6);
             border-radius:10px;"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    img_path = ec3p.practice_image_path(q.get("image"), unit_id=unit_id)
    has_img = img_path and os.path.exists(img_path)
    if has_img:
        q_col, img_col = st.columns([3, 2], gap="medium")
        with q_col:
            st.markdown(
                f"""
            <div class="gk-question-box">
                <span class="gk-topic-badge" style="background:{cat_color}20;color:{cat_color};">
                    {cat_emoji} {cat_name}
                </span>
                <div class="gk-question-text" style="margin-top:0.8rem;font-size:1.3rem;">{q['question']}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with img_col:
            st.image(img_path, use_container_width=True)
    else:
        st.markdown(
            f"""
        <div class="gk-question-box">
            <span class="gk-topic-badge" style="background:{cat_color}20;color:{cat_color};">
                {cat_emoji} {cat_name}
            </span>
            <div class="gk-question-text" style="margin-top:0.8rem;font-size:1.3rem;">{q['question']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    correct_idx = q["answer"]
    picked = ans.get("picked") if ans else None
    ans_col1, ans_col2 = st.columns(2, gap="medium")
    for i, opt in enumerate(q["options"]):
        col = ans_col1 if i % 2 == 0 else ans_col2
        with col:
            if i == correct_idx:
                css = "correct-answer"
                label = f"✅ {opt} — correct answer"
            elif picked is not None and str(opt) == str(picked) and i != correct_idx:
                css = "wrong-answer"
                label = f"❌ {opt} — your answer"
            else:
                css = ""
                label = str(opt)
            if css:
                st.markdown(
                    f'<div class="{css}" style="padding:0.85rem 1rem;border-radius:12px;margin-bottom:0.5rem;">'
                    f"<strong>{label}</strong></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="padding:0.85rem 1rem;border-radius:12px;margin-bottom:0.5rem;'
                    f'background:#f9fafb;border:2px solid #e5e7eb;color:#374151;">{label}</div>',
                    unsafe_allow_html=True,
                )

    if q.get("explanation"):
        st.markdown(
            f"""
        <div style="background:#eff6ff;border-left:4px solid #6366f1;padding:0.8rem 1rem;
             border-radius:8px;margin-top:0.5rem;">
            <strong>Explanation:</strong> {q['explanation']}
        </div>
        """,
            unsafe_allow_html=True,
        )

    col_prev, col_mid, col_next = st.columns([1, 2, 1])
    with col_prev:
        if idx > 0 and st.button("⬅️ Previous", key="ec3_review_prev", use_container_width=True):
            st.session_state.ec3_review_index = idx - 1
            st.rerun()
    with col_next:
        if idx < total - 1 and st.button("Next ➡️", key="ec3_review_next", use_container_width=True, type="primary"):
            st.session_state.ec3_review_index = idx + 1
            st.rerun()
    with col_mid:
        wrong_indices = [i for i, a in enumerate(answers) if not a.get("correct")]
        if wrong_indices and st.button("Jump to next mistake", key="ec3_review_jump_wrong", use_container_width=True):
            next_wrong = next((i for i in wrong_indices if i > idx), wrong_indices[0])
            st.session_state.ec3_review_index = next_wrong
            st.rerun()


def render_home():
    name = st.session_state.selected_user
    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="ec3_back_dash"):
            _back_dashboard()
            st.rerun()

    st.markdown(
        f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">🎓 {name}'s Edgenuity Course 3</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Grade 8 Mathematics — units & linear equation strategies</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    tab_units, tab_linear, tab_setup = st.tabs([
        "📘 Course Units",
        "⚖️ Solving Linear Equations",
        "📅 Week Setup",
    ])

    with tab_units:
        _render_units_grid()

    with tab_linear:
        import edgenuity_linear_equations_ui as leq_ui

        leq_ui.render_practice_home()

    with tab_setup:
        import edgenuity_linear_equations_ui as leq_ui

        leq_ui.render_setup_panel()


def _render_units_grid():
    row1 = st.columns(3, gap="large")
    row2 = st.columns(3, gap="large")
    row3 = st.columns(3, gap="large")
    row4 = st.columns(1, gap="large")
    cols = row1 + row2 + row3 + row4

    for col, unit in zip(cols, ec3.list_units()):
        with col:
            ready = ec3.unit_notes_ready(unit)
            has_pdf = unit["pdf"].is_file()
            badge = "✅ Ready" if ready else ("📄 PDF only" if has_pdf else "🔜 Coming soon")
            border = "#6366f1" if ready else "#94a3b8"
            st.markdown(
                f"""
                <div class="score-card" style="border-top: 5px solid {border}; min-height: 130px;">
                    <div style="font-size: 2rem;">📘</div>
                    <h3 style="margin: 0.4rem 0;">{unit['title']}</h3>
                    <p style="color: #6b7280; font-size: 0.9rem;">{unit.get('subtitle', '')}</p>
                    <p style="font-size: 0.85rem; margin-top: 0.5rem;"><strong>{badge}</strong></p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open {unit['title']}", key=f"ec3_unit_{unit['id']}", use_container_width=True, type="primary"):
                _open_unit(unit["id"])
                st.rerun()


def render_unit():
    unit_id = st.session_state.get("ec3_unit_id", 1)
    unit = ec3.get_unit(unit_id)
    if not unit:
        st.error("Unit not found.")
        return

    if unit_id == 1 and u1ui is not None:
        col_nav1, _ = st.columns([1, 5])
        with col_nav1:
            if st.button("← All units", key="ec3_unit_back_home"):
                st.session_state.current_page = "edgenuity_course3_home"
                st.rerun()

        if not ec3.unit_notes_ready(unit):
            st.info("Lesson notes for this unit are coming soon.")
            return

        def _go_full():
            _start_practice(unit_id, show_spinner=True)
            st.rerun()

        def _go_focus(cat: str, label: str):
            _start_practice(unit_id, show_spinner=True, focus_category=cat, focus_label=label)
            st.rerun()

        def _open_notes_page(slug):
            _open_notes(unit_id, slug)
            st.rerun()

        u1ui.render_unit1_hub(
            unit,
            week_cfg=_week_config(),
            xai_configured=bool(_xai_api_key()),
            on_open_notes=_open_notes_page,
            on_start_full_practice=_go_full,
            on_start_focus_practice=_go_focus,
        )
        return

    col_nav1, col_nav2, _ = st.columns([1, 1, 5])
    with col_nav1:
        if st.button("← All units", key="ec3_unit_back_home"):
            st.session_state.current_page = "edgenuity_course3_home"
            st.rerun()
    with col_nav2:
        if unit["pdf"].is_file():
            with open(unit["pdf"], "rb") as f:
                st.download_button(
                    "📄 Exam PDF",
                    data=f.read(),
                    file_name=unit["pdf"].name,
                    mime="application/pdf",
                    key=f"ec3_unit_pdf_{unit_id}",
                )

    st.markdown(f"## {unit['title']}")
    if unit.get("subtitle"):
        st.caption(unit["subtitle"])

    if not ec3.unit_notes_ready(unit):
        st.info("Lesson notes for this unit are coming soon.")
        if not unit["pdf"].is_file():
            st.warning("No PDF found for this unit yet.")
        return

    if unit.get("combined_notes") and unit["combined_notes"].is_file():
        if st.button("📋 Unit overview", key=f"ec3_overview_{unit_id}", use_container_width=True):
            _open_notes(unit_id, None)
            st.rerun()

    st.markdown("### 📝 Daily Practice")
    week_cfg = _week_config()
    if week_cfg.get("use_llm"):
        if _xai_api_key():
            st.caption(
                "15 **fresh AI-generated** questions (xAI Grok) — new set each time you start. "
                "Turn off AI in **Week Setup** to use the built-in bank with graphs."
            )
        else:
            st.caption(
                "AI is enabled in Week Setup but XAI_API_KEY is missing — will use the built-in question bank."
            )
    else:
        st.caption(
            "15 questions — at least 9 include graphs/diagrams like the Edgenuity exam. "
            "Enable **Generate with AI** in Week Setup for fresh questions each session."
        )
    if st.button("🎯 Start Daily Practice", key=f"ec3_practice_{unit_id}", use_container_width=True, type="primary"):
        _start_practice(unit_id, show_spinner=True)
        st.rerun()

    st.markdown("---")
    st.markdown("### Activities")
    for act in unit["activities"]:
        label = f"Activity {act['number']}: {act['title']}"
        if act.get("inline_diagrams"):
            label += " 🎨"
        if st.button(label, key=f"ec3_open_{unit_id}_{act['slug']}", use_container_width=True):
            _open_notes(unit_id, act["slug"])
            st.rerun()


def render_notes():
    unit_id = st.session_state.get("ec3_unit_id", 1)
    slug = st.session_state.get("ec3_activity_slug")
    unit = ec3.get_unit(unit_id) or ec3.UNITS[0]

    col_nav1, col_nav2, _ = st.columns([1, 1, 5])
    with col_nav1:
        if st.button(f"← {unit['title']}", key="ec3_notes_back_unit"):
            st.session_state.current_page = "edgenuity_course3_unit"
            st.session_state.ec3_activity_slug = None
            st.rerun()
    with col_nav2:
        if slug and st.button("Unit overview", key="ec3_to_overview"):
            st.session_state.ec3_activity_slug = None
            st.rerun()

    if unit_id == 1 and u1ui is not None and slug:

        def _jump_activity(target_slug: str):
            st.session_state.ec3_activity_slug = target_slug
            st.rerun()

        u1ui.render_activity_nav(unit_id, slug, _jump_activity)

    if slug:
        activity = next((a for a in unit["activities"] if a["slug"] == slug), None)
        if not activity:
            st.error("Activity not found.")
            return
        st.markdown(f"### Activity {activity['number']}: {activity['title']}")
        md = ec3.load_activity_markdown(unit, activity)
        if activity.get("inline_diagrams"):
            ec3r.render_markdown_with_diagrams(unit, activity, md)
        else:
            for path, cap in ec3.activity_diagrams(unit, activity):
                st.image(path, caption=cap, use_container_width=True)
            st.markdown(md)

        if unit_id == 1 and u1ui is not None:

            def _quiz_from_notes(cat: str, label: str):
                _start_practice(unit_id, show_spinner=True, focus_category=cat, focus_label=label)
                st.rerun()

            u1ui.render_notes_footer(unit_id, slug, _quiz_from_notes)
    else:
        path = unit.get("combined_notes")
        if path and path.is_file():
            st.markdown(path.read_text(encoding="utf-8"))
        else:
            st.warning("Combined notes not available.")

    if unit.get("activities"):
        st.markdown("---")
        st.markdown("**Other activities**")
        for act in unit["activities"]:
            if act["slug"] != slug:
                if st.button(
                    f"Activity {act['number']}: {act['title']}",
                    key=f"ec3_jump_{unit_id}_{act['slug']}",
                ):
                    st.session_state.ec3_activity_slug = act["slug"]
                    st.rerun()


def render_practice():
    name = st.session_state.selected_user
    user = db.get_user(name)
    unit_id = st.session_state.get("ec3_unit_id", 1)
    unit = ec3.get_unit(unit_id) or ec3.UNITS[0]
    questions = st.session_state.get("ec3_questions", [])
    current = st.session_state.get("ec3_current", 0)
    total = len(questions)
    is_done = current >= total

    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button(f"← {unit['title']}", key="ec3_practice_back"):
            st.session_state.current_page = "edgenuity_course3_unit"
            st.session_state.ec3_questions = []
            st.session_state.ec3_current = 0
            st.session_state.ec3_answers = []
            st.session_state.ec3_last_feedback = None
            st.session_state.ec3_review_mode = False
            st.session_state.ec3_review_index = 0
            st.session_state.ec3_focus_category = None
            st.session_state.ec3_focus_label = None
            st.rerun()
    with col_nav_mid:
        if not is_done and total:
            elapsed = int(time.time() - st.session_state.ec3_start_time) if st.session_state.get("ec3_start_time") else 0
            st.markdown(
                f'<div style="text-align:center;color:#6b7280;font-size:0.9rem;padding-top:0.5rem;">'
                f"Question {current + 1} of {total} &nbsp;|&nbsp; ⏱️ {elapsed}s</div>",
                unsafe_allow_html=True,
            )

    st.markdown(
        """
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: #6366f1; margin: 0.3rem 0; font-size: 2.2rem;">🎓 Edgenuity Daily Practice</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )

    focus_label = st.session_state.get("ec3_focus_label")
    if focus_label:
        st.caption(f"🎯 **Topic focus:** {focus_label} · {total} questions")
    elif unit_id == 1:
        st.caption(f"**Unit 1** mixed review · {total} questions")

    warn = st.session_state.pop("ec3_warn", None)
    if warn:
        st.warning(warn)
    elif questions and questions[0].get("source") == "llm":
        st.caption("🤖 Fresh questions generated by xAI Grok for this session.")

    if not questions:
        st.warning("No questions loaded.")
        return

    answers = st.session_state.get("ec3_answers", [])
    if is_done and st.session_state.get("ec3_review_mode"):
        _render_ec3_review(questions, answers, unit_id, unit)
        return

    progress = (current / total) if total > 0 else 0
    st.markdown(
        f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress * 100:.0f}%;height:100%;background:linear-gradient(90deg,#6366f1,#8b5cf6);
             border-radius:10px;"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if not is_done:
        q = questions[current]
        cat_info = ec3p.get_categories(unit_id).get(q["category"], {})
        cat_color = cat_info.get("color", "#6366f1")
        cat_emoji = cat_info.get("emoji", "📐")
        cat_name = cat_info.get("name", "Math")

        lesson_col, review_col = st.columns([3, 1])
        with review_col:
            act_slug = ec3p.get_category_activity_slug(unit_id, q.get("category", ""))
            if act_slug and st.button("📘 Lesson", key=f"ec3_lesson_{current}", use_container_width=True):
                st.session_state.current_page = "edgenuity_course3_notes"
                st.session_state.ec3_activity_slug = act_slug
                st.rerun()

        img_path = ec3p.practice_image_path(q.get("image"), unit_id=unit_id)
        has_img = img_path and os.path.exists(img_path)

        if has_img:
            q_col, img_col = st.columns([3, 2], gap="medium")
            with q_col:
                st.markdown(
                    f"""
                <div class="gk-question-box">
                    <span class="gk-topic-badge" style="background:{cat_color}20;color:{cat_color};">
                        {cat_emoji} {cat_name}
                    </span>
                    <div class="gk-question-text" style="margin-top:0.8rem;font-size:1.3rem;">{q['question']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with img_col:
                st.image(img_path, use_container_width=True)
        else:
            st.markdown(
                f"""
            <div class="gk-question-box">
                <span class="gk-topic-badge" style="background:{cat_color}20;color:{cat_color};">
                    {cat_emoji} {cat_name}
                </span>
                <div class="gk-question-text" style="margin-top:0.8rem;font-size:1.3rem;">{q['question']}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        last_feedback = st.session_state.get("ec3_last_feedback")
        if last_feedback and last_feedback.get("idx") == current:
            if last_feedback["correct"]:
                st.markdown(
                    f"""
                <div class="correct-answer" style="text-align:center;">
                    ✅ <strong>Correct!</strong>
                    <p style="color:#065f46;font-size:0.9rem;margin-top:0.3rem;">{q.get('explanation', '')}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div class="wrong-answer" style="text-align:center;">
                    Not quite! The answer is <strong>{last_feedback['correct_val']}</strong>
                    <p style="color:#991b1b;font-size:0.9rem;margin-top:0.3rem;">{q.get('explanation', '')}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            _, col_next, _ = st.columns([1, 2, 1])
            with col_next:
                label = "Next ➡️" if current < total - 1 else "🎉 See Results!"
                if st.button(label, key="ec3_next", use_container_width=True, type="primary"):
                    if current < total - 1:
                        st.session_state.ec3_current += 1
                    else:
                        st.session_state.ec3_current = total
                    st.session_state.ec3_last_feedback = None
                    st.rerun()
        else:
            ans_col1, ans_col2 = st.columns(2, gap="medium")
            for i, opt in enumerate(q["options"]):
                col = ans_col1 if i % 2 == 0 else ans_col2
                with col:
                    if st.button(str(opt), key=f"ec3_opt_{current}_{i}", use_container_width=True, type="primary"):
                        is_correct = i == q["answer"]
                        st.session_state.ec3_answers.append({
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        })
                        st.session_state.ec3_last_feedback = {
                            "idx": current,
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        }
                        st.rerun()
    else:
        answers = st.session_state.get("ec3_answers", [])
        correct_count = sum(1 for a in answers if a["correct"])
        score_pct = int((correct_count / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.ec3_start_time) if st.session_state.get("ec3_start_time") else 0
        minutes, seconds = divmod(time_spent, 60)
        report = ec3p.build_session_report(questions, answers, unit_id=unit_id)

        if user:
            db.save_activity_score(
                user["id"],
                "EdgenuityCourse3",
                f"Unit {unit_id} Practice",
                score_pct,
                100,
                ec3p.format_report_details(report),
                time_spent,
                flush_sheets=False,
            )

        session_id = st.session_state.get("ec3_session_id")
        if user and session_id and st.session_state.get("ec3_persist_saved_for") != session_id:
            st.session_state.ec3_persist_saved_for = session_id
            failed = ec3mail.build_failed_questions(questions, answers)
            _, sheet_err = gss.persist_edgenuity_practice(
                user_name=name,
                user_id=user["id"],
                session_id=session_id,
                session_kind="unit",
                unit_id=unit_id,
                unit_label=f"Unit {unit_id}: {unit['title']}",
                report=report,
                failed_questions=failed,
                time_spent_seconds=time_spent,
                question_ids=[q["id"] for q in questions],
            )
            if sheet_err:
                st.warning(f"Google Sheet sync failed (saved locally): {sheet_err}")

        if score_pct == 100:
            res_emoji, message, res_color = "🏆", "Perfect score!", "#10b981"
        elif score_pct >= 80:
            res_emoji, message, res_color = "🔥", "Great job — exam ready!", "#6366f1"
        elif score_pct >= 60:
            res_emoji, message, res_color = "📐", "Good progress — keep practicing!", "#f59e0b"
        else:
            res_emoji, message, res_color = "💪", "Review the lesson notes and try again!", "#ef4444"

        st.markdown(
            f"""
        <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;
             border:3px solid {res_color};margin-top:1rem;">
            <div style="font-size:5rem;">{res_emoji}</div>
            <h2 style="color:{res_color};margin:0.5rem 0;">{correct_count} out of {total} correct!</h2>
            <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        _render_session_report(report, unit_id, unit)

        session_id = st.session_state.get("ec3_session_id")
        if session_id and st.session_state.get("ec3_email_sent_for") != session_id:
            st.session_state.ec3_email_sent_for = session_id
            if ec3mail.practice_email_enabled():
                mail_result = ec3mail.send_practice_report_email(
                    student_name=name,
                    unit_title=unit["title"],
                    unit_subtitle=unit.get("subtitle", ""),
                    report=report,
                    time_spent_seconds=time_spent,
                    questions=questions,
                    answers=answers,
                )
                ec3mail.render_practice_email_result(mail_result)

        with st.expander("📋 Question-by-question review", expanded=False):
            for idx, (q, ans) in enumerate(zip(questions, answers)):
                css = "correct-answer" if ans["correct"] else "wrong-answer"
                mark = "✅" if ans["correct"] else f"❌ You: {ans['picked']} — ✅ {ans['correct_val']}"
                cat_info = ec3p.CATEGORIES.get(q.get("category", ""), {})
                cat_label = cat_info.get("name", "")
                st.markdown(
                    f"""
                <div class="{css}">
                    <strong>Q{idx + 1}</strong>{f' · {cat_label}' if cat_label else ''}: {q['question']} &nbsp; {mark}
                    <p style="font-size:0.85rem;margin:0.3rem 0 0 0;">{q.get('explanation', '')}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            if st.button("🔍 Review Answers", key="ec3_review_start", use_container_width=True, type="primary"):
                st.session_state.ec3_review_mode = True
                st.session_state.ec3_review_index = 0
                st.rerun()
        with col_r2:
            if st.button("🎯 Practice Again", key="ec3_again", use_container_width=True):
                _start_practice(unit_id, show_spinner=True)
                st.rerun()
        with col_r3:
            if st.button("📘 Back to Unit", key="ec3_results_unit", use_container_width=True):
                st.session_state.current_page = "edgenuity_course3_unit"
                st.session_state.ec3_questions = []
                st.session_state.ec3_review_mode = False
                st.rerun()
