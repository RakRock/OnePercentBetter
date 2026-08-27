"""Class 10 unit practice & weekly setup UI — modeled on PreReq buckets."""

from __future__ import annotations

import os
import time

import streamlit as st

import database as db
import edgenuity_practice_email as ec3mail
import google_sheets_sync as gss
import harshit_class10_practice as h10p
import harshit_class10_questions as h10q
import harshit_class10_topics as h10t
import harshit_class10_units as h10u
import harshit_math_answers as hma
import harshit_math_components as hmc_ui
import harshit_math_render as hmr


def _xai_api_key() -> str | None:
    try:
        return st.secrets.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
    except Exception:
        return os.environ.get("XAI_API_KEY")


def _ss_key(unit_id: int, name: str) -> str:
    return f"hm10_u{unit_id}_{name}"


def _clear_setup_widget_state(unit_id: int) -> None:
    """Drop Week Setup widget keys so the next render loads values from the DB."""
    st.session_state.pop(f"hm10_setup_label_{unit_id}", None)
    st.session_state.pop(f"hm10_setup_xai_{unit_id}", None)
    st.session_state.pop(f"hm10_setup_grok_mode_{unit_id}", None)
    for tid in h10t.topics_for_unit(unit_id):
        st.session_state.pop(f"hm10_setup_topic_{unit_id}_{tid}", None)


def ensure_week_config(unit_id: int) -> dict:
    config = db.get_harshit_class10_week_config(unit_id)
    if config.get("topics"):
        return config
    starter = h10t.default_week_config(unit_id)
    if not starter.get("topics"):
        return config
    db.save_harshit_class10_week_config(
        unit_id,
        starter["week_label"],
        starter["topics"],
        practice_difficulty=int(starter.get("practice_difficulty", 3)),
        use_chapter_llm=True,
        grok_fresh_only=False,
    )
    return db.get_harshit_class10_week_config(unit_id)


def _questions(unit_id: int) -> list[dict]:
    return st.session_state.get(_ss_key(unit_id, "questions"), [])


def _start_practice(unit_id: int) -> None:
    config = ensure_week_config(unit_id)
    api_key = _xai_api_key()
    use_xai = bool(config.get("use_chapter_llm", True))
    if use_xai and api_key:
        with st.spinner("Generating questions with Grok… (usually 15–45 sec)"):
            questions, grok_error = h10p.build_session_set(
                unit_id, config, xai_api_key=api_key
            )
    else:
        questions, grok_error = h10p.build_session_set(unit_id, config, xai_api_key=api_key)

    if not questions:
        st.session_state[_ss_key(unit_id, "error")] = grok_error or (
            "Configure topics and difficulty in Week Setup."
        )
        return

    st.session_state.pop(_ss_key(unit_id, "error"), None)
    if grok_error:
        st.session_state[_ss_key(unit_id, "warn")] = grok_error

    st.session_state[_ss_key(unit_id, "questions")] = questions
    st.session_state[_ss_key(unit_id, "config_snapshot")] = config
    st.session_state[_ss_key(unit_id, "current")] = 0
    st.session_state[_ss_key(unit_id, "answers")] = []
    st.session_state[_ss_key(unit_id, "feedback")] = None
    st.session_state[_ss_key(unit_id, "review_mode")] = False
    st.session_state[_ss_key(unit_id, "review_index")] = 0
    st.session_state[_ss_key(unit_id, "start_time")] = time.time()
    st.session_state[_ss_key(unit_id, "session_id")] = f"hm10-u{unit_id}-{time.time()}"
    st.session_state.hm10_unit_id = unit_id
    st.session_state.current_page = "harshit_class10_practice"


def _picked_index(q: dict, ans: dict | None) -> int | None:
    if not ans:
        return None
    picked = str(ans.get("picked", ""))
    for i, opt in enumerate(q.get("options", [])):
        if str(opt) == picked:
            return i
    return None


def _render_review_choices(q: dict, ans: dict | None) -> None:
    opts = q["options"]
    picked_idx = _picked_index(q, ans)
    correct_idx = int(q["answer"])

    st.markdown(
        '<p style="color:#6366f1;font-size:0.88rem;font-weight:700;margin:1rem 0 0.75rem 0;">Your answers</p>',
        unsafe_allow_html=True,
    )
    for i, opt in enumerate(opts):
        letter = chr(65 + i)
        display = hmr.format_math_display(str(opt))
        if i == correct_idx:
            css, suffix = "correct-answer", " — correct answer"
        elif picked_idx is not None and i == picked_idx and i != correct_idx:
            css, suffix = "wrong-answer", " — your answer"
        else:
            css, suffix = "", ""
        if css:
            st.markdown(
                f'<div class="{css}" style="padding:0.85rem 1rem;border-radius:12px;margin-bottom:0.5rem;">'
                f"<strong>{letter}. {display}{suffix}</strong></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="padding:0.85rem 1rem;border-radius:12px;margin-bottom:0.5rem;'
                f'background:#f9fafb;border:2px solid #e5e7eb;color:#374151;">'
                f"<strong>{letter}.</strong> {display}</div>",
                unsafe_allow_html=True,
            )


def _render_review(unit_id: int, questions: list[dict], answers: list[dict]) -> None:
    total = len(questions)
    idx = st.session_state.get(_ss_key(unit_id, "review_index"), 0)
    idx = max(0, min(idx, total - 1))
    st.session_state[_ss_key(unit_id, "review_index")] = idx

    q = questions[idx]
    ans = answers[idx] if idx < len(answers) else None

    col_back, col_title, _ = st.columns([1, 4, 1])
    with col_back:
        if st.button("← Results", key=f"hm10_review_back_{unit_id}", use_container_width=True):
            st.session_state[_ss_key(unit_id, "review_mode")] = False
            st.rerun()
    with col_title:
        status = "✅ Correct" if ans and ans.get("correct") else "❌ Incorrect"
        st.markdown(
            f'<div style="text-align:center;color:#6b7280;font-size:0.95rem;padding-top:0.5rem;">'
            f"Review question {idx + 1} of {total} &nbsp;|&nbsp; {status}</div>",
            unsafe_allow_html=True,
        )

    progress = ((idx + 1) / total) if total else 0
    st.markdown(
        f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="background:linear-gradient(90deg,#6366f1,#8b5cf6);width:{progress * 100:.0f}%;height:100%;"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<p style="color:#6366f1;font-size:0.85rem;margin-bottom:0.25rem;">'
        f'{q.get("category_label", "")} · Level {q.get("level", "")}</p>',
        unsafe_allow_html=True,
    )
    hmr.render_question(q["question"])
    _render_review_choices(q, ans)

    if q.get("explanation"):
        expl = hmr.format_math_display(str(q["explanation"]))
        st.markdown(
            f'<div style="background:#eff6ff;border-left:4px solid #6366f1;padding:0.8rem 1rem;'
            f'border-radius:8px;margin-top:0.75rem;"><strong>Explanation:</strong> {expl}</div>',
            unsafe_allow_html=True,
        )

    nav1, _, nav3 = st.columns([1, 2, 1])
    with nav1:
        if idx > 0 and st.button("← Previous", key=f"hm10_rev_prev_{unit_id}", use_container_width=True):
            st.session_state[_ss_key(unit_id, "review_index")] = idx - 1
            st.rerun()
    with nav3:
        if idx < total - 1 and st.button("Next →", key=f"hm10_rev_next_{unit_id}", use_container_width=True):
            st.session_state[_ss_key(unit_id, "review_index")] = idx + 1
            st.rerun()


def _render_unit_header(unit_id: int, unit: dict) -> None:
    st.markdown(
        f'<p class="hm-prompt">Unit {unit_id} · {unit["title"]}</p>',
        unsafe_allow_html=True,
    )
    pdf_path = h10u.unit_pdf_path(unit_id)
    if pdf_path:
        st.caption(f"Chapter PDF: `{pdf_path.name}`")
        try:
            with st.expander("📄 NCERT chapter (PDF)", expanded=False):
                st.pdf(pdf_path)
        except Exception:
            st.caption(str(pdf_path))

    topics = h10t.topics_for_unit(unit_id)
    if topics:
        with st.expander("Topics in this unit", expanded=False):
            for tid in sorted(topics):
                info = topics[tid]
                st.markdown(f"- {info.get('emoji', '')} **{info['name']}**")


def render_setup_panel(unit_id: int) -> None:
    hmc_ui.inject_harshit_styles()
    unit = h10u.get_unit(unit_id)
    if not unit:
        st.error("Unit not found.")
        return

    st.markdown("### Weekly Plan Setup")
    st.caption(
        f"Choose topics, difficulty, and xAI generation for **{unit['title']}**. "
        "Grok uses the chapter PDF plus seed examples from your question bank."
    )

    current = db.get_harshit_class10_week_config(unit_id)
    stats = h10q.bank_stats(unit_id)
    if stats["total"]:
        st.caption(f"Question bank: {stats['total']} cached question(s).")
    else:
        st.caption("Bank empty — questions come from templates or Grok during practice.")

    week_label = st.text_input(
        "Week label (optional)",
        value=current.get("week_label", ""),
        placeholder=f"e.g. Week 1 — {unit['title'][:24]}",
        key=f"hm10_setup_label_{unit_id}",
    )

    topics_meta = h10t.topics_for_unit(unit_id)

    st.markdown("#### Question generation")
    xai_key = _xai_api_key()
    if xai_key:
        st.caption("xAI (Grok) API key detected.")
    else:
        st.caption("Add `XAI_API_KEY` to `.streamlit/secrets.toml` for Grok generation.")

    use_xai_live = st.toggle(
        "Generate questions with xAI (Grok) during practice",
        value=bool(current.get("use_chapter_llm", True)),
        key=f"hm10_setup_xai_{unit_id}",
    )
    grok_fresh_only = False
    if use_xai_live:
        grok_fresh_only = st.radio(
            "Grok mode",
            options=["fast", "fresh"],
            index=1 if current.get("grok_fresh_only") else 0,
            format_func=lambda x: (
                "Fast — Grok batch + bank fallback (recommended)"
                if x == "fast"
                else "All fresh — every question from Grok only"
            ),
            key=f"hm10_setup_grok_mode_{unit_id}",
        ) == "fresh"

    current_levels: dict[int, list[str]] = {}
    for item in current.get("topics", []):
        current_levels[int(item["id"])] = list(item.get("levels", []))

    st.markdown("---")
    st.markdown("#### Topics & difficulty levels")
    new_topics: list[dict] = []
    for tid in sorted(topics_meta):
        info = topics_meta[tid]
        level_options = {f"Level {k} — {v}": k for k, v in info["levels"].items()}
        default = [
            f"Level {k} — {v}"
            for k, v in info["levels"].items()
            if k in current_levels.get(tid, [])
        ]
        picked = st.multiselect(
            f"{info.get('emoji', '')} **T{tid}: {info['name']}**",
            options=list(level_options.keys()),
            default=default,
            key=f"hm10_setup_topic_{unit_id}_{tid}",
        )
        levels = [level_options[p] for p in picked]
        if levels:
            new_topics.append({"id": tid, "levels": levels})

    if st.button("Save weekly plan", type="primary", key=f"hm10_setup_save_{unit_id}"):
        db.save_harshit_class10_week_config(
            unit_id,
            week_label.strip(),
            new_topics,
            practice_difficulty=int(current.get("practice_difficulty", 3)),
            use_chapter_llm=use_xai_live,
            grok_fresh_only=grok_fresh_only,
        )
        _clear_setup_widget_state(unit_id)
        st.success("Weekly plan saved.")
        st.rerun()

    saved = db.get_harshit_class10_week_config(unit_id)
    if saved.get("topics"):
        st.markdown("**Current active plan**")
        st.code(h10t.format_week_plan_summary(unit_id, saved), language=None)


def render_practice_home(unit_id: int) -> None:
    config = ensure_week_config(unit_id)
    err = st.session_state.pop(_ss_key(unit_id, "error"), None)
    warn = st.session_state.pop(_ss_key(unit_id, "warn"), None)
    if err:
        st.warning(err)
    if warn:
        st.info(warn)

    stats = h10q.bank_stats(unit_id)
    if stats["total"]:
        st.success(h10q.bank_status_message(unit_id))
    else:
        st.warning(h10q.bank_status_message(unit_id))

    if not config.get("topics"):
        st.info("No weekly plan yet. Open **Week Setup** to choose topics, difficulty, and xAI.")
        return

    if config.get("week_label"):
        st.markdown(f"**{config['week_label']}**")

    st.markdown("**This week's focus**")
    for line in h10t.format_week_plan_summary(unit_id, config).split("\n"):
        if line.strip() and not line.startswith("Week:"):
            st.markdown(f"- {line.strip().lstrip('•').strip()}")

    st.markdown("### Practice session")
    xai_on = bool(config.get("use_chapter_llm", True))
    api_key = _xai_api_key()
    if xai_on and api_key:
        mode = "Grok + bank fallback" if not config.get("grok_fresh_only") else "all fresh Grok"
        st.caption(
            f"{h10p.DEFAULT_QUESTION_COUNT} questions · {mode} · {stats['total']} in bank"
        )
    else:
        st.caption(
            f"{h10p.DEFAULT_QUESTION_COUNT} questions · {stats['total']} bank item(s) · "
            "configure xAI in Week Setup"
        )

    if st.button("Start practice", key=f"hm10_start_{unit_id}", use_container_width=True):
        _start_practice(unit_id)
        st.rerun()


def render_unit_home(unit_id: int) -> None:
    import harshit_class10_unit_notes as h10un
    import harshit_class10_unit_notes_ui as h10ung_ui
    import harshit_class10_unit_test_ui as h10ut_ui

    hmc_ui.inject_harshit_styles()
    unit = h10u.get_unit(unit_id)
    if not unit:
        st.error("Unit not found.")
        return

    ensure_week_config(unit_id)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Class X", key=f"hm10_back_{unit_id}"):
            st.session_state.current_page = "harshit_class10_home"
            st.rerun()

    _render_unit_header(unit_id, unit)

    section_key = f"hm10_unit_section_{unit_id}"
    has_guide = h10un.unit_guide_available(unit_id)
    section_options = ["🎯 Practice", "📝 Unit Test", "📅 Week Setup"]
    if has_guide:
        section_options = ["📖 Unit Guide"] + section_options

    if section_key not in st.session_state:
        st.session_state[section_key] = "📖 Unit Guide" if has_guide else "🎯 Practice"
    elif st.session_state[section_key] not in section_options:
        st.session_state[section_key] = section_options[0]

    section = st.radio(
        "Section",
        section_options,
        horizontal=True,
        key=section_key,
        label_visibility="collapsed",
    )

    st.markdown("---")

    if section == "📖 Unit Guide":
        h10ung_ui.render_unit_guide(unit_id)
    elif section == "🎯 Practice":
        render_practice_home(unit_id)
    elif section == "📝 Unit Test":
        h10ut_ui.render_unit_test_home(unit_id)
    else:
        render_setup_panel(unit_id)


def render_practice() -> None:
    hmc_ui.inject_harshit_styles()
    unit_id = st.session_state.get("hm10_unit_id", 1)
    unit = h10u.get_unit(unit_id)
    name = st.session_state.selected_user
    user = db.get_user(name) if name else None

    questions = _questions(unit_id)
    config = st.session_state.get(_ss_key(unit_id, "config_snapshot")) or db.get_harshit_class10_week_config(unit_id)
    current = st.session_state.get(_ss_key(unit_id, "current"), 0)
    total = len(questions)
    is_done = current >= total

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key=f"hm10_pr_back_{unit_id}"):
            st.session_state.current_page = "harshit_class10_unit"
            st.session_state[_ss_key(unit_id, "questions")] = []
            st.session_state[_ss_key(unit_id, "current")] = 0
            st.session_state[_ss_key(unit_id, "answers")] = []
            st.session_state[_ss_key(unit_id, "review_mode")] = False
            st.session_state[_ss_key(unit_id, "review_index")] = 0
            st.rerun()

    title = unit["title"] if unit else f"Unit {unit_id}"
    st.markdown(f'<p class="hm-prompt" style="text-align:center;">{title}</p>', unsafe_allow_html=True)
    if config.get("week_label"):
        st.caption(config["week_label"])

    if not questions:
        st.warning("No questions loaded.")
        return

    answers = st.session_state.get(_ss_key(unit_id, "answers"), [])
    if is_done and st.session_state.get(_ss_key(unit_id, "review_mode")):
        _render_review(unit_id, questions, answers)
        return

    if not is_done:
        progress = (current / total) if total > 0 else 0
        st.markdown(
            f"""
        <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
            <div style="background:linear-gradient(90deg,#6366f1,#8b5cf6);width:{progress * 100:.0f}%;height:100%;"></div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        q = questions[current]
        src = q.get("source", "template")
        src_label = {
            "chapter_llm": "Generated from chapter PDF",
            "template": "Practice question",
        }.get(src, src)
        st.markdown(
            f'<p style="color:#6b7280;font-size:0.88rem;text-align:center;">'
            f"Question {current + 1} of {total} · {q.get('category_label', '')} · "
            f"Level {q.get('level', '')} · {src_label}</p>",
            unsafe_allow_html=True,
        )
        hmr.render_question(q["question"])

        fb = st.session_state.get(_ss_key(unit_id, "feedback"))
        if fb and fb.get("q_index") == current:
            picked_disp = hmr.format_math_display(str(fb["picked"]))
            correct_disp = hmr.format_math_display(str(fb["correct_val"]))
            expl_disp = hmr.format_math_display(str(q.get("explanation", "")))
            if fb["correct"]:
                st.markdown(
                    f'<div class="correct-answer" style="text-align:center;">'
                    f'✅ <strong>Correct!</strong> The answer is <strong>{correct_disp}</strong>'
                    f'<p style="color:#065f46;font-size:0.9rem;">{expl_disp}</p></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="wrong-answer" style="text-align:center;">'
                    f'Not quite! You picked <strong>{picked_disp}</strong>. '
                    f'Answer: <strong>{correct_disp}</strong>'
                    f'<p style="color:#991b1b;font-size:0.9rem;">{expl_disp}</p></div>',
                    unsafe_allow_html=True,
                )
            _, col_next, _ = st.columns([1, 2, 1])
            with col_next:
                label = "Next ➡️" if current < total - 1 else "🎉 See Results!"
                if st.button(label, key=f"hm10_next_{unit_id}", use_container_width=True, type="primary"):
                    if current < total - 1:
                        st.session_state[_ss_key(unit_id, "current")] += 1
                    else:
                        st.session_state[_ss_key(unit_id, "current")] = total
                    st.session_state[_ss_key(unit_id, "feedback")] = None
                    st.rerun()
        else:
            picked = _render_choices(q, current, unit_id)
            if picked is not None:
                is_correct = hma.is_pick_correct(q, picked)
                picked_val = q["options"][picked]
                correct_val = q["options"][q["answer"]]
                answers.append({"picked": picked_val, "correct_val": correct_val, "correct": is_correct})
                st.session_state[_ss_key(unit_id, "answers")] = answers
                st.session_state[_ss_key(unit_id, "feedback")] = {
                    "q_index": current,
                    "correct": is_correct,
                    "picked": picked_val,
                    "correct_val": correct_val,
                }
                st.rerun()
    else:
        time_spent = int(time.time() - st.session_state.get(_ss_key(unit_id, "start_time"), time.time()))
        report = h10p.build_session_report(questions, answers, student_name=name or "Student")
        meta = h10p.session_meta_from_config(unit_id, config)
        score_pct = report["score_pct"]
        correct_count = report["correct_count"]

        if score_pct == 100:
            res_emoji, message, res_color = "🏆", "Perfect score — great work!", "#10b981"
        elif score_pct >= 80:
            res_emoji, message, res_color = "🌟", "Strong session — keep it up!", "#3b82f6"
        elif score_pct >= 60:
            res_emoji, message, res_color = "👍", "Good effort — review below.", "#f59e0b"
        else:
            res_emoji, message, res_color = "💪", "Keep practicing — you will get there!", "#ef4444"

        minutes, seconds = divmod(time_spent, 60)
        st.markdown(
            f"""
        <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;
             border:3px solid {res_color};margin-top:1rem;">
            <div style="font-size:5rem;">{res_emoji}</div>
            <h2 style="color:{res_color};">{correct_count} / {report['total']} correct</h2>
            <p>{message}</p>
            <p style="color:#9ca3af;">⏱️ {minutes}m {seconds}s</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if report["strengths"]:
            st.markdown("#### ✅ Doing well")
            for item in report["strengths"]:
                st.markdown(f"- {item['name']} — {item['correct']}/{item['total']} ({item['pct']}%)")
        if report["needs_revision"]:
            st.markdown("#### 📚 Needs revision")
            for item in report["needs_revision"]:
                st.markdown(f"- {item['name']} — {item['correct']}/{item['total']} ({item['pct']}%)")

        with st.expander("📋 Question-by-question review", expanded=False):
            for idx, (q_item, ans) in enumerate(zip(questions, answers)):
                css = "correct-answer" if ans.get("correct") else "wrong-answer"
                q_disp = hmr.format_math_display(str(q_item["question"]))
                expl_disp = hmr.format_math_display(str(q_item.get("explanation", "")))
                if ans.get("correct"):
                    mark = "✅"
                else:
                    picked = hmr.format_math_plain(str(ans.get("picked", "?")))
                    correct_val = hmr.format_math_plain(str(ans.get("correct_val", "?")))
                    mark = f"❌ You: {picked} — ✅ {correct_val}"
                st.markdown(
                    f"""
                <div class="{css}">
                    <strong>Q{idx + 1}</strong> · {q_item.get("category_label", "")}: {q_disp} &nbsp; {mark}
                    <p style="font-size:0.85rem;margin:0.3rem 0 0 0;">{expl_disp}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        if user:
            db.save_activity_score(
                user["id"],
                "HarshitMath",
                f"Class X Unit {unit_id}: {title[:40]}",
                report["score_pct"],
                100,
                h10p.format_report_details(report),
                time_spent,
                flush_sheets=False,
            )

        session_id = st.session_state.get(_ss_key(unit_id, "session_id"))
        if user and session_id and st.session_state.get(_ss_key(unit_id, "persist_saved_for")) != session_id:
            st.session_state[_ss_key(unit_id, "persist_saved_for")] = session_id
            week_label = config.get("week_label") or "Weekly practice"
            failed = ec3mail.build_failed_questions(questions, answers)
            try:
                _, sheet_err = gss.persist_edgenuity_practice(
                    user_name=name,
                    user_id=user["id"],
                    session_id=session_id,
                    session_kind="harshit_class10",
                    unit_id=100 + unit_id,
                    unit_label=f"Class X Unit {unit_id}: {title} — {week_label}",
                    report=report,
                    failed_questions=failed,
                    time_spent_seconds=time_spent,
                    question_ids=[str(q.get("id", "")) for q in questions],
                )
                if sheet_err:
                    st.warning(f"Google Sheet sync note: {sheet_err}")
            except Exception as exc:
                st.warning(f"Google Sheet sync failed (saved locally): {exc}")

        if session_id and st.session_state.get(_ss_key(unit_id, "email_sent_for")) != session_id:
            st.session_state[_ss_key(unit_id, "email_sent_for")] = session_id
            if ec3mail.practice_email_enabled():
                mail_result = ec3mail.send_harshit_report_email(
                    student_name=name or "Student",
                    unit_title=f"Class X Unit {unit_id}: {title}",
                    unit_subtitle=config.get("week_label") or "Weekly practice",
                    report=report,
                    time_spent_seconds=time_spent,
                    session_meta=meta,
                    questions=questions,
                    answers=answers,
                )
                ec3mail.render_practice_email_result(mail_result)
            else:
                st.caption("Email not configured — practice report saved on screen only.")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔍 Review Answers", key=f"hm10_review_start_{unit_id}", use_container_width=True, type="primary"):
                st.session_state[_ss_key(unit_id, "review_mode")] = True
                st.session_state[_ss_key(unit_id, "review_index")] = 0
                st.rerun()
        with c2:
            if st.button("Practice again", key=f"hm10_again_{unit_id}", use_container_width=True):
                _start_practice(unit_id)
                st.rerun()
        with c3:
            if st.button("← Back to unit", key=f"hm10_done_back_{unit_id}", use_container_width=True):
                st.session_state.current_page = "harshit_class10_unit"
                st.session_state[_ss_key(unit_id, "questions")] = []
                st.session_state[_ss_key(unit_id, "review_mode")] = False
                st.rerun()


def _render_choices(q: dict, current: int, unit_id: int) -> int | None:
    st.markdown(
        """
<style>
section.main [data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
    width: 100%; min-height: 3.25rem; font-weight: 700;
}
</style>
""",
        unsafe_allow_html=True,
    )
    cols = st.columns(2, gap="medium")
    for idx, opt in enumerate(q["options"]):
        with cols[idx % 2]:
            if st.button(
                hmr.format_math_plain(str(opt)),
                key=f"hm10_choice_{unit_id}_{current}_{idx}",
                use_container_width=True,
            ):
                return idx
    return None
