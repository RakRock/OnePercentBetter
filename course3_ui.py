"""Streamlit UI for Arjun Course 3 Math lesson notes and practice."""

from __future__ import annotations

import os
import time
import uuid

import streamlit as st

import arjun_course3_content as c3
import arjun_course3_practice as c3p
import arjun_course3_render as c3r
import arjun_course3_week_ui as c3week_ui
import database as db
import edgenuity_practice_email as ec3mail
import google_sheets_sync as gss

FOCUS_QUESTION_COUNT = c3p.FOCUS_SESSION_COUNT
FULL_QUESTION_COUNT = c3p.DEFAULT_SESSION_COUNT

PRIMARY = "#6366f1"
PRIMARY_GRADIENT_END = "#8b5cf6"


def _xai_api_key() -> str | None:
    try:
        return st.secrets.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
    except Exception:
        return os.environ.get("XAI_API_KEY")


def _use_grok(unit_id: int) -> bool:
    config = c3week_ui.ensure_week_config("course3", unit_id)
    return bool(config.get("use_llm"))


def _week_config(unit_id: int) -> dict:
    return c3week_ui.ensure_week_config("course3", unit_id)


def _back_dashboard():
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_activity = None


def _open_unit(unit_id: int):
    st.session_state.c3_unit_id = unit_id
    st.session_state.c3_activity_slug = None
    st.session_state.current_page = "course3_unit"


def _open_notes(unit_id: int, activity_slug: str | None = None):
    st.session_state.c3_unit_id = unit_id
    st.session_state.c3_activity_slug = activity_slug
    st.session_state.current_page = "course3_notes"


def _reset_practice_state():
    st.session_state.c3_questions = []
    st.session_state.c3_current = 0
    st.session_state.c3_answers = []
    st.session_state.c3_last_feedback = None
    st.session_state.c3_review_mode = False
    st.session_state.c3_focus_category = None
    st.session_state.c3_focus_label = None
    st.session_state.c3_email_sent_for = None
    st.session_state.c3_persist_saved_for = None


def _start_practice(
    unit_id: int,
    *,
    focus_category: str | None = None,
    focus_label: str | None = None,
    show_spinner: bool = False,
):
    bank_size = c3p.question_count_for_unit(unit_id)
    if bank_size == 0:
        st.session_state.c3_warn = "No practice questions for this unit yet."
        return

    config = _week_config(unit_id)
    user = db.get_user(st.session_state.selected_user) if st.session_state.get("selected_user") else None
    exclude_ids = (
        db.get_recent_ec3_question_ids(
            user["id"],
            unit_id + gss.COURSE3_SESSION_UNIT_OFFSET,
            c3p.RECENT_SESSIONS_TO_AVOID,
        )
        if user
        else set()
    )

    api_key = _xai_api_key()
    use_llm = bool(config.get("use_llm"))

    def _build():
        if focus_category:
            question_count = min(FOCUS_QUESTION_COUNT, c3p.question_count_for_unit(unit_id, [focus_category]))
            return c3p.build_focus_set(
                unit_id,
                focus_category,
                count=question_count,
                exclude_ids=exclude_ids,
                use_llm=use_llm,
                xai_api_key=api_key,
            )
        questions, grok_error = c3p.build_session_set(
            unit_id,
            config,
            exclude_ids=exclude_ids,
            xai_api_key=api_key,
        )
        st.session_state.c3_grok_notice = grok_error
        return questions

    if show_spinner and use_llm and api_key:
        with st.spinner("Generating fresh questions with xAI Grok…"):
            questions = _build()
    else:
        questions = _build()

    grok_notice = st.session_state.pop("c3_grok_notice", None)

    if not questions:
        st.session_state.c3_warn = (
            f"Not enough questions for {focus_label or 'this unit'} — try full unit practice."
            if focus_category
            else "Could not load practice questions — check Week Setup topics."
        )
        return

    if grok_notice:
        st.session_state.c3_warn = grok_notice
    elif use_llm and not api_key:
        st.session_state.c3_warn = (
            "Grok is enabled in Week Setup but XAI_API_KEY is missing — used the built-in question bank."
        )
    else:
        st.session_state.pop("c3_warn", None)

    _reset_practice_state()
    st.session_state.c3_questions = questions
    st.session_state.c3_start_time = time.time()
    st.session_state.c3_session_id = str(uuid.uuid4())
    st.session_state.c3_email_sent_for = None
    st.session_state.c3_persist_saved_for = None
    st.session_state.c3_focus_category = focus_category
    st.session_state.c3_focus_label = focus_label
    st.session_state.current_page = "course3_practice"


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
                        key=f"c3_rev_{item['category']}",
                        use_container_width=True,
                    ):
                        _open_notes(unit_id, item["activity_slug"])
                        st.rerun()


def render_home():
    """Course 3 landing — pick Unit 1 through Unit 6."""
    name = st.session_state.selected_user
    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="c3_back_dash"):
            _back_dashboard()
            st.rerun()

    st.markdown(
        f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">📐 {name}'s Course 3 Math</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Units 1–5 — lesson notes, practice & Grok quizzes</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    row1 = st.columns(3, gap="large")
    row2 = st.columns(3, gap="large")
    for col, unit in zip(row1 + row2, c3.list_units()):
        with col:
            ready = c3.unit_notes_ready(unit)
            has_pdf = unit["pdf"].is_file()
            badge = "✅ Notes ready" if ready else ("📄 PDF only" if has_pdf else "🔜 Coming soon")
            border = PRIMARY if ready else "#94a3b8"
            st.markdown(
                f"""
                <div class="score-card" style="border-top: 5px solid {border}; min-height: 140px;">
                    <div style="font-size: 2rem;">📘</div>
                    <h3 style="margin: 0.4rem 0;">{unit['title']}</h3>
                    <p style="color: #6b7280; font-size: 0.9rem;">{unit.get('subtitle', '')}</p>
                    <p style="font-size: 0.85rem; margin-top: 0.5rem;"><strong>{badge}</strong></p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open {unit['title']}", key=f"c3_unit_{unit['id']}", width="stretch", type="primary"):
                _open_unit(unit["id"])
                st.rerun()


def render_unit():
    """Single unit hub — activities (Unit 2) or PDF placeholder."""
    unit_id = st.session_state.get("c3_unit_id", 2)
    unit = c3.get_unit(unit_id)
    if not unit:
        st.error("Unit not found.")
        return

    col_nav1, col_nav2, _ = st.columns([1, 1, 5])
    with col_nav1:
        if st.button("← All units", key="c3_unit_back_home"):
            st.session_state.current_page = "course3_home"
            st.rerun()
    with col_nav2:
        if unit["pdf"].is_file():
            with open(unit["pdf"], "rb") as f:
                st.download_button(
                    "📄 PDF",
                    data=f.read(),
                    file_name=unit["pdf"].name,
                    mime="application/pdf",
                    key=f"c3_unit_pdf_{unit_id}",
                )

    st.markdown(f"## {unit['title']}")
    if unit.get("subtitle"):
        st.caption(unit["subtitle"])

    if not c3.unit_notes_ready(unit):
        st.info(
            "Lesson review notes for this unit are not built yet. "
            "You can download the textbook PDF above. "
            "**Units 1–5** have full activity notes with diagrams."
        )
        if not unit["pdf"].is_file():
            st.warning("No PDF found for this unit yet.")
        return

    if unit.get("combined_notes") and unit["combined_notes"].is_file():
        if st.button("📋 Unit overview & cheat sheet", key=f"c3_overview_{unit_id}", width="stretch"):
            _open_notes(unit_id, None)
            st.rerun()

    c3week_ui.ensure_week_config("course3", unit_id)
    tab_activities, tab_practice, tab_setup = st.tabs(["📚 Activities", "🎯 Practice", "📅 Week Setup"])

    with tab_activities:
        st.markdown("### Activities")
        st.caption("Tap an activity to open its review notes.")
        for act in unit["activities"]:
            label = f"Activity {act['number']}: {act['title']}"
            if act.get("inline_diagrams"):
                label += " 🎨"
            if st.button(label, key=f"c3_open_{unit_id}_{act['slug']}", width="stretch"):
                _open_notes(unit_id, act["slug"])
                st.rerun()

    with tab_practice:
        bank_size = c3p.question_count_for_unit(unit_id)
        week_cfg = _week_config(unit_id)
        filtered_size = c3p.question_count_for_unit(unit_id, week_cfg.get("categories"))
        if bank_size:
            st.markdown("### Practice")
            session_count = int(week_cfg.get("question_count", FULL_QUESTION_COUNT))
            st.caption(
                f"**{bank_size}** questions in the bank — weekly plan uses **{filtered_size}** "
                f"across {len(week_cfg.get('categories', []))} topic(s), **{session_count}** per session."
            )

            if week_cfg.get("use_llm"):
                if _xai_api_key():
                    st.caption(
                        "✅ **Grok is ON** (Week Setup) — each practice start generates fresh questions."
                    )
                else:
                    st.warning(
                        "**Grok is ON** in Week Setup but **XAI_API_KEY** is missing — "
                        "will fall back to the built-in question bank."
                    )
            else:
                st.caption("Using the built-in question bank. Enable Grok in **Week Setup** for fresh AI questions.")

            if st.button(
                f"🎯 Start unit practice ({min(session_count, filtered_size or session_count)} questions)",
                key=f"c3_practice_full_{unit_id}",
                type="primary",
                use_container_width=True,
            ):
                _start_practice(unit_id, show_spinner=bool(week_cfg.get("use_llm")))
                st.rerun()

            categories = c3p.get_categories(unit_id)
            cat_cols = st.columns(2)
            for i, (cat_id, info) in enumerate(categories.items()):
                with cat_cols[i % 2]:
                    label = f"{info.get('emoji', '📝')} {info.get('name', cat_id)} quiz"
                    if st.button(label, key=f"c3_focus_{unit_id}_{cat_id}", use_container_width=True):
                        _start_practice(
                            unit_id,
                            focus_category=cat_id,
                            focus_label=info.get("name", cat_id),
                            show_spinner=bool(week_cfg.get("use_llm")),
                        )
                        st.rerun()
        else:
            st.info("Practice questions for this unit are coming soon.")

    with tab_setup:
        c3week_ui.render_setup_panel("course3", unit_id)


def render_notes():
    unit_id = st.session_state.get("c3_unit_id", 2)
    slug = st.session_state.get("c3_activity_slug")
    unit = c3.get_unit(unit_id) or c3.UNIT_2

    col_nav1, col_nav2, _ = st.columns([1, 1, 5])
    with col_nav1:
        if st.button(f"← {unit['title']}", key="c3_notes_back_unit"):
            st.session_state.current_page = "course3_unit"
            st.session_state.c3_activity_slug = None
            st.rerun()
    with col_nav2:
        if slug and st.button("Unit overview", key="c3_to_overview"):
            st.session_state.c3_activity_slug = None
            st.rerun()

    if slug:
        activity = next((a for a in unit["activities"] if a["slug"] == slug), None)
        if not activity:
            st.error("Activity not found.")
            return
        st.markdown(f"### Activity {activity['number']}: {activity['title']}")
        md = c3.load_activity_markdown(unit, activity)
        if activity.get("inline_diagrams"):
            c3r.render_markdown_with_diagrams(unit, activity, md)
        else:
            for path, cap in c3.activity_diagrams(unit, activity):
                st.image(path, caption=cap, use_container_width=True)
            st.markdown(md)
    else:
        path = unit.get("combined_notes")
        if path and path.is_file():
            st.markdown(path.read_text(encoding="utf-8"))
        else:
            st.warning("Combined notes not available.")

    if unit.get("activities"):
        st.markdown("---")
        st.markdown("**Other activities in this unit**")
        for act in unit["activities"]:
            if act["slug"] != slug:
                if st.button(
                    f"Activity {act['number']}: {act['title']}",
                    key=f"c3_jump_{unit_id}_{act['slug']}",
                ):
                    st.session_state.c3_activity_slug = act["slug"]
                    st.rerun()


def render_practice():
    """Multiple-choice practice session for a Course 3 unit."""
    name = st.session_state.selected_user
    user = db.get_user(name)
    unit_id = st.session_state.get("c3_unit_id", 1)
    unit = c3.get_unit(unit_id)
    if not unit:
        st.error("Unit not found.")
        return

    questions = st.session_state.get("c3_questions", [])
    current = st.session_state.get("c3_current", 0)
    total = len(questions)
    is_done = current >= total

    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button(f"← {unit['title']}", key="c3_practice_back"):
            st.session_state.current_page = "course3_unit"
            _reset_practice_state()
            st.rerun()
    with col_nav_mid:
        if not is_done and total:
            elapsed = int(time.time() - st.session_state.c3_start_time) if st.session_state.get("c3_start_time") else 0
            st.markdown(
                f'<div style="text-align:center;color:#6b7280;font-size:0.9rem;padding-top:0.5rem;">'
                f"Question {current + 1} of {total} &nbsp;|&nbsp; ⏱️ {elapsed}s</div>",
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: {PRIMARY}; margin: 0.3rem 0; font-size: 2.2rem;">📐 Course 3 Practice</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )

    focus_label = st.session_state.get("c3_focus_label")
    if focus_label:
        st.caption(f"🎯 **Topic focus:** {focus_label} · {total} questions")
    else:
        st.caption(f"**{unit['title']}** mixed review · {total} questions")
    if questions and questions[0].get("source") == "llm":
        st.caption("✨ Questions generated by xAI Grok for this session.")

    warn = st.session_state.pop("c3_warn", None)
    if warn:
        st.warning(warn)

    if not questions:
        st.warning("No questions loaded.")
        return

    progress = (current / total) if total > 0 else 0
    st.markdown(
        f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress * 100:.0f}%;height:100%;background:linear-gradient(90deg,{PRIMARY},{PRIMARY_GRADIENT_END});
             border-radius:10px;"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if not is_done:
        q = questions[current]
        cat_info = c3p.get_categories(unit_id).get(q["category"], {})
        cat_color = cat_info.get("color", PRIMARY)
        cat_emoji = cat_info.get("emoji", "📐")
        cat_name = cat_info.get("name", "Math")

        q_col, review_col = st.columns([3, 1])
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
        with review_col:
            act_slug = c3p.get_category_activity_slug(unit_id, q.get("category", ""))
            if act_slug and st.button("📘 Lesson", key=f"c3_lesson_{current}", use_container_width=True):
                st.session_state.current_page = "course3_notes"
                st.session_state.c3_activity_slug = act_slug
                st.rerun()

        last_feedback = st.session_state.get("c3_last_feedback")
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
                if st.button(label, key="c3_next", use_container_width=True, type="primary"):
                    if current < total - 1:
                        st.session_state.c3_current += 1
                    else:
                        st.session_state.c3_current = total
                    st.session_state.c3_last_feedback = None
                    st.rerun()
        else:
            ans_col1, ans_col2 = st.columns(2, gap="medium")
            for i, opt in enumerate(q["options"]):
                col = ans_col1 if i % 2 == 0 else ans_col2
                with col:
                    if st.button(str(opt), key=f"c3_opt_{current}_{i}", use_container_width=True, type="primary"):
                        is_correct = i == q["answer"]
                        st.session_state.c3_answers.append({
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        })
                        st.session_state.c3_last_feedback = {
                            "idx": current,
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        }
                        st.rerun()
    else:
        answers = st.session_state.get("c3_answers", [])
        correct_count = sum(1 for a in answers if a["correct"])
        score_pct = int((correct_count / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.c3_start_time) if st.session_state.get("c3_start_time") else 0
        report = c3p.build_session_report(questions, answers, unit_id=unit_id)
        minutes, seconds = divmod(time_spent, 60)

        if user:
            db.save_activity_score(
                user["id"],
                "Course3Math",
                f"Unit {unit_id} Practice",
                score_pct,
                100,
                c3p.format_report_details(report),
                time_spent,
                flush_sheets=False,
            )

        session_id = st.session_state.get("c3_session_id")
        if user and session_id and st.session_state.get("c3_persist_saved_for") != session_id:
            st.session_state.c3_persist_saved_for = session_id
            failed = ec3mail.build_failed_questions(questions, answers)
            _, sheet_err = gss.persist_course3_practice(
                user_name=name,
                user_id=user["id"],
                session_id=session_id,
                unit_id=unit_id,
                unit_label=f"Course 3 · Unit {unit_id}: {unit['title']}",
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
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s · Score: {score_pct}%</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        _render_session_report(report, unit_id, unit)

        if session_id and st.session_state.get("c3_email_sent_for") != session_id:
            st.session_state.c3_email_sent_for = session_id
            if ec3mail.practice_email_enabled():
                mail_result = ec3mail.send_course3_report_email(
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
            categories = c3p.get_categories(unit_id)
            for idx, (q, ans) in enumerate(zip(questions, answers)):
                css = "correct-answer" if ans["correct"] else "wrong-answer"
                mark = "✅" if ans["correct"] else f"❌ You: {ans['picked']} — ✅ {ans['correct_val']}"
                cat_info = categories.get(q.get("category", ""), {})
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

        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("🔄 Try again", key="c3_retry", use_container_width=True, type="primary"):
                focus_cat = st.session_state.get("c3_focus_category")
                focus_lbl = st.session_state.get("c3_focus_label")
                _start_practice(
                    unit_id,
                    focus_category=focus_cat,
                    focus_label=focus_lbl,
                    show_spinner=_use_grok(unit_id),
                )
                st.rerun()
        with btn2:
            if st.button("← Back to unit", key="c3_done_back", use_container_width=True):
                st.session_state.current_page = "course3_unit"
                _reset_practice_state()
                st.rerun()
