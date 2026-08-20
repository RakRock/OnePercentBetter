"""PreReq practice & weekly setup UI — modeled on Edgenuity Linear Equations."""

from __future__ import annotations

import os
import time

import streamlit as st

import database as db
import edgenuity_practice_email as ec3mail
import google_sheets_sync as gss
import harshit_chapter_questions as hcq
import harshit_math_components as hmc_ui
import harshit_math_content as hmc
import harshit_math_answers as hma
import harshit_math_diagrams as hmd
import harshit_math_prereqs as hmp
import harshit_math_render as hmr
import harshit_prereq_practice as hpp
import harshit_prereq_topics as hpt


def _xai_api_key() -> str | None:
    try:
        return st.secrets.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
    except Exception:
        return os.environ.get("XAI_API_KEY")


def _ss_key(prereq_id: int, name: str) -> str:
    return f"hm_pr{prereq_id}_{name}"


def ensure_week_config(prereq_id: int) -> dict:
    """Return saved weekly plan, or seed a Level-A starter plan on first visit."""
    config = db.get_harshit_prereq_week_config(prereq_id)
    if config.get("topics"):
        return config
    starter = hpt.default_week_config(prereq_id)
    if not starter.get("topics"):
        return config
    db.save_harshit_prereq_week_config(
        prereq_id,
        starter["week_label"],
        starter["topics"],
        warmup_count=0,
        use_llm=True,
        use_chapter_llm=True,
    )
    return db.get_harshit_prereq_week_config(prereq_id)


def _questions(prereq_id: int) -> list:
    return st.session_state.get(_ss_key(prereq_id, "questions"), [])


def _start_practice(prereq_id: int):
    config = ensure_week_config(prereq_id)
    api_key = _xai_api_key()
    user = db.get_user(st.session_state.selected_user)
    user_id = user["id"] if user else None
    use_xai = bool(config.get("use_chapter_llm", True))
    grok_error = ""
    if use_xai and api_key:
        with st.spinner(
            "Generating questions with Grok… (usually 15–45 sec; all-fresh mode can take longer)"
        ):
            questions, grok_error = hpp.build_session_set(
                prereq_id, config, xai_api_key=api_key, user_id=user_id
            )
    else:
        questions, grok_error = hpp.build_session_set(
            prereq_id, config, xai_api_key=api_key, user_id=user_id
        )
    if not questions:
        if use_xai and api_key:
            detail = grok_error or "Check XAI_API_KEY and chapter PDFs, then try again."
            st.session_state[_ss_key(prereq_id, "error")] = f"Grok could not generate questions. {detail}"
        else:
            st.session_state[_ss_key(prereq_id, "error")] = (
                "Select at least one topic and level in Week Setup."
            )
        return
    if use_xai and api_key and len(questions) < hpp.DEFAULT_QUESTION_COUNT:
        detail = grok_error or "Try starting again."
        st.session_state[_ss_key(prereq_id, "error")] = (
            f"Grok generated {len(questions)} of {hpp.DEFAULT_QUESTION_COUNT} questions "
            f"(no bank fallback). {detail}"
        )
    else:
        st.session_state.pop(_ss_key(prereq_id, "error"), None)
    st.session_state[_ss_key(prereq_id, "questions")] = questions
    st.session_state[_ss_key(prereq_id, "config_snapshot")] = config
    st.session_state[_ss_key(prereq_id, "current")] = 0
    st.session_state[_ss_key(prereq_id, "answers")] = []
    st.session_state[_ss_key(prereq_id, "feedback")] = None
    st.session_state[_ss_key(prereq_id, "start_time")] = time.time()
    st.session_state[_ss_key(prereq_id, "session_id")] = f"hmpr{prereq_id}-{time.time()}"
    st.session_state[_ss_key(prereq_id, "review_mode")] = False
    st.session_state.hm_practice_prereq_id = prereq_id
    st.session_state.current_page = "harshit_prereq_practice"


def render_setup_panel(prereq_id: int):
    hmc_ui.inject_harshit_styles()
    prereq = hmp.get_prereq(prereq_id)
    if not prereq:
        st.error("PreReq not found.")
        return

    st.markdown("### Weekly Plan Setup")
    st.caption(
        f"Choose topics and difficulty levels for **{prereq['title']}**. "
        "Practice sessions draw questions from your selections."
    )
    try:
        if gss.is_configured():
            st.caption(
                f"Plans sync to Google Sheet tab **{gss.HARSHIT_PREREQ_PLAN_WORKSHEET}** (one row per PreReq)."
            )
    except Exception:
        pass

    current = db.get_harshit_prereq_week_config(prereq_id)
    bank = hcq.bank_stats(prereq_id)
    if bank["total"]:
        st.caption(f"Chapter question bank: {bank['total']} cached question(s) from NCERT PDFs.")
    else:
        st.caption(
            "No cached chapter questions yet. Add PDFs under `HarshitMath/class9_chapters/` "
            "and run `python3 scripts/build_harshit_chapter_questions.py --prereq N`, "
            "or enable live generation below (requires XAI_API_KEY)."
        )

    week_label = st.text_input(
        "Week label (optional)",
        value=current.get("week_label", ""),
        placeholder=f"e.g. Week 1 — {prereq['title'][:30]}",
        key=f"hm_setup_label_{prereq_id}",
    )

    st.markdown("#### Question generation")
    xai_key = _xai_api_key()
    if xai_key:
        st.caption("xAI (Grok) API key detected — live generation is available.")
    else:
        st.caption(
            "Add `XAI_API_KEY` to `.streamlit/secrets.toml` to enable live Grok generation."
        )

    use_xai_live = st.toggle(
        "Generate questions with xAI (Grok) during practice",
        value=bool(current.get("use_chapter_llm", True)),
        help=(
            "When on, Grok generates questions from chapter PDFs. "
            "Use Fast mode (default) for Arjun-style speed with bank fallback. "
            "Use All-fresh mode only when you want every question live from Grok."
        ),
        key=f"hm_setup_xai_live_{prereq_id}",
    )
    grok_fresh_only = False
    if use_xai_live:
        grok_fresh_only = st.radio(
            "Grok mode",
            options=["fast", "fresh"],
            index=1 if current.get("grok_fresh_only") else 0,
            format_func=lambda x: (
                "Fast — one Grok batch, chapter bank fills gaps (like Arjun)"
                if x == "fast"
                else "All fresh — every question from Grok only (slower)"
            ),
            key=f"hm_setup_grok_mode_{prereq_id}",
        ) == "fresh"
    if use_xai_live and not xai_key:
        st.warning("Turn on xAI generation after adding XAI_API_KEY — until then, templates are used.")

    if ec3mail.practice_email_enabled():
        ready, _, _ = ec3mail.delivery_ready()
        if ready:
            st.caption(f"📧 {ec3mail.email_status_message()}")
        else:
            st.warning(f"📧 {ec3mail.email_status_message()}")

    current_levels: dict[int, list[str]] = {}
    for item in current.get("topics", []):
        current_levels[int(item["id"])] = list(item.get("levels", []))

    st.markdown("---")
    st.markdown("#### Topics & difficulty levels")

    new_topics: list[dict] = []
    topics = hpt.topics_for_prereq(prereq_id)
    for tid in sorted(topics):
        info = topics[tid]
        level_options = {f"Level {k} — {v}": k for k, v in info["levels"].items()}
        default = [
            f"Level {k} — {v}"
            for k, v in info["levels"].items()
            if k in current_levels.get(tid, [])
        ]
        picked = st.multiselect(
            f"{info.get('emoji', '')} **{info['name']}**",
            options=list(level_options.keys()),
            default=default,
            key=f"hm_setup_topic_{prereq_id}_{tid}",
        )
        levels = [level_options[p] for p in picked]
        if levels:
            new_topics.append({"id": tid, "levels": levels})

    if st.button("Save weekly plan", type="primary", key=f"hm_setup_save_{prereq_id}"):
        db.save_harshit_prereq_week_config(
            prereq_id,
            week_label.strip(),
            new_topics,
            warmup_count=0,
            use_llm=use_xai_live,
            use_chapter_llm=use_xai_live,
            grok_fresh_only=grok_fresh_only,
        )
        st.success("Weekly plan saved.")
        st.rerun()

    if current.get("topics"):
        st.markdown("**Current active plan**")
        st.code(hpt.format_week_plan_summary(prereq_id, current), language=None)


def render_practice_home(prereq_id: int):
    hmc_ui.inject_harshit_styles()
    prereq = hmp.get_prereq(prereq_id)
    if not prereq:
        return

    config = ensure_week_config(prereq_id)
    err = st.session_state.pop(_ss_key(prereq_id, "error"), None)
    if err:
        st.warning(err)

    stats = hcq.bank_stats(prereq_id)
    if stats["total"]:
        st.success(hcq.bank_status_message(prereq_id))
    else:
        st.warning(hcq.bank_status_message(prereq_id))

    if not config.get("topics"):
        st.info("No weekly plan yet. Open **Week Setup** to choose topics and levels.")
        return

    if config.get("week_label"):
        st.markdown(f"**{config['week_label']}**")

    st.markdown("**This week's focus**")
    for line in hpt.format_week_plan_summary(prereq_id, config).split("\n"):
        if line.strip() and not line.startswith("Week:"):
            st.markdown(f"- {line.strip().lstrip('•').strip()}")

    st.markdown("### Practice session")
    stats = hcq.bank_stats(prereq_id)
    if ec3mail.practice_email_enabled():
        ready, _, _ = ec3mail.delivery_ready()
        if ready:
            st.caption(f"📧 {ec3mail.email_status_message()}")
        else:
            st.warning(f"📧 {ec3mail.email_status_message()}")
    xai_on = bool(config.get("use_chapter_llm", True))
    fresh_only = bool(config.get("grok_fresh_only", False))
    api_key = _xai_api_key()
    if xai_on and api_key and fresh_only:
        st.caption(
            f"{hpp.DEFAULT_QUESTION_COUNT} questions · all fresh from Grok "
            f"(~30–90 sec) · {stats['total']} item(s) in bank"
        )
    elif xai_on and api_key:
        st.caption(
            f"{hpp.DEFAULT_QUESTION_COUNT} questions · Grok batch + chapter bank fallback (like Arjun) "
            f"· {stats['total']} cached item(s)"
        )
    elif stats["total"]:
        st.caption(
            f"{hpp.DEFAULT_QUESTION_COUNT} unique questions · drawn from {stats['total']} chapter-bank item(s)"
        )
    elif xai_on and not api_key:
        st.caption(
            f"{hpp.DEFAULT_QUESTION_COUNT} questions · xAI enabled but no API key — using templates only"
        )
    else:
        st.caption(
            f"{hpp.DEFAULT_QUESTION_COUNT} questions · template bank only "
            "(enable xAI in Week Setup for live chapter questions)"
        )

    if st.button("Start practice", key=f"hm_pr_start_{prereq_id}", use_container_width=True):
        _start_practice(prereq_id)
        st.rerun()


def render_practice():
    hmc_ui.inject_harshit_styles()
    prereq_id = st.session_state.get("hm_practice_prereq_id", 1)
    prereq = hmp.get_prereq(prereq_id)
    name = st.session_state.selected_user
    user = db.get_user(name) if name else None

    questions = _questions(prereq_id)
    config = st.session_state.get(_ss_key(prereq_id, "config_snapshot")) or db.get_harshit_prereq_week_config(prereq_id)
    current = st.session_state.get(_ss_key(prereq_id, "current"), 0)
    total = len(questions)
    is_done = current >= total

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key=f"hm_pr_back_{prereq_id}"):
            st.session_state.current_page = "harshit_prereq_bucket"
            st.session_state[_ss_key(prereq_id, "questions")] = []
            st.session_state[_ss_key(prereq_id, "current")] = 0
            st.session_state[_ss_key(prereq_id, "answers")] = []
            st.session_state[_ss_key(prereq_id, "review_mode")] = False
            st.rerun()

    title = prereq["title"] if prereq else f"PreReq {prereq_id}"
    st.markdown(
        f'<p class="hm-prompt" style="text-align:center;">{title}</p>',
        unsafe_allow_html=True,
    )
    if config.get("week_label"):
        st.caption(config["week_label"])

    if not questions:
        st.warning("No questions loaded.")
        return

    answers = st.session_state.get(_ss_key(prereq_id, "answers"), [])

    progress = (current / total) if total > 0 else 0
    st.markdown(
        f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="background:linear-gradient(90deg,#6366f1,#8b5cf6);width:{progress * 100:.0f}%;height:100%;"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if not is_done:
        q = questions[current]
        src = q.get("source", "template")
        src_label = {
            "chapter_pdf": "NCERT chapter bank",
            "chapter_llm": "Generated from chapter PDF",
            "chapter_seed": "Chapter practice bank",
            "template": "Practice question",
        }.get(src, src)
        st.markdown(
            f'<p style="color:#6b7280;font-size:0.88rem;text-align:center;">'
            f"Question {current + 1} of {total} · {q.get('category_label', '')} · "
            f"Level {q.get('level', '')} · {src_label}</p>",
            unsafe_allow_html=True,
        )
        svg = hmd.render_svg(q)
        if svg:
            st.markdown(hmd.wrap_svg(svg), unsafe_allow_html=True)
        hmr.render_question(q["question"])

        fb = st.session_state.get(_ss_key(prereq_id, "feedback"))
        if fb and fb.get("q_index") == current:
            if fb["correct"]:
                st.markdown(
                    f"""
                <div class="correct-answer" style="text-align:center;">
                    ✅ <strong>Correct!</strong> The answer is <strong>{fb["correct_val"]}</strong> 🎉
                    <p style="color:#065f46;font-size:0.9rem;margin-top:0.3rem;">{q.get("explanation", "")}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div class="wrong-answer" style="text-align:center;">
                    Not quite! You picked <strong>{fb["picked"]}</strong>.
                    The answer is <strong>{fb["correct_val"]}</strong> 💪
                    <p style="color:#991b1b;font-size:0.9rem;margin-top:0.3rem;">{q.get("explanation", "")}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            _, col_next, _ = st.columns([1, 2, 1])
            with col_next:
                label = "Next ➡️" if current < total - 1 else "🎉 See Results!"
                if st.button(label, key=f"hm_pr_next_{prereq_id}", use_container_width=True, type="primary"):
                    if current < total - 1:
                        st.session_state[_ss_key(prereq_id, "current")] += 1
                    else:
                        st.session_state[_ss_key(prereq_id, "current")] = total
                    st.session_state[_ss_key(prereq_id, "feedback")] = None
                    st.rerun()
        else:
            picked = _render_choices(q, current, prereq_id)
            if picked is not None:
                is_correct = hma.is_pick_correct(q, picked)
                picked_val = q["options"][picked]
                correct_val = q["options"][q["answer"]]
                answers.append({
                    "picked": picked_val,
                    "correct_val": correct_val,
                    "correct": is_correct,
                })
                st.session_state[_ss_key(prereq_id, "answers")] = answers
                st.session_state[_ss_key(prereq_id, "feedback")] = {
                    "q_index": current,
                    "correct": is_correct,
                    "picked": picked_val,
                    "correct_val": correct_val,
                }
                st.rerun()
    else:
        time_spent = int(
            time.time() - st.session_state.get(_ss_key(prereq_id, "start_time"), time.time())
        )
        report = hpp.build_session_report(questions, answers)
        meta = hpp.session_meta_from_config(prereq_id, config)
        score_pct = report["score_pct"]
        correct_count = report["correct_count"]

        if score_pct == 100:
            res_emoji, message, res_color = "🏆", "Perfect score — great work!", "#10b981"
        elif score_pct >= 80:
            res_emoji, message, res_color = "🌟", "Strong session — keep it up!", "#3b82f6"
        elif score_pct >= 60:
            res_emoji, message, res_color = "👍", "Good effort — review the topics below.", "#f59e0b"
        else:
            res_emoji, message, res_color = "💪", "Keep practicing — you will get there!", "#ef4444"

        minutes, seconds = divmod(time_spent, 60)
        st.markdown(
            f"""
        <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;
             border:3px solid {res_color};margin-top:1rem;">
            <div style="font-size:5rem;">{res_emoji}</div>
            <h2 style="color:{res_color};margin:0.5rem 0;">{correct_count} out of {report["total"]} correct!</h2>
            <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
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
                if ans.get("correct"):
                    mark = "✅"
                else:
                    picked = ans.get("picked", "?")
                    correct_val = ans.get("correct_val", "?")
                    mark = f"❌ You: {picked} — ✅ {correct_val}"
                st.markdown(
                    f"""
                <div class="{css}">
                    <strong>Q{idx + 1}</strong> · {q_item.get("category_label", "")}: {q_item["question"]} &nbsp; {mark}
                    <p style="font-size:0.85rem;margin:0.3rem 0 0 0;">{q_item.get("explanation", "")}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        if user:
            db.save_activity_score(
                user["id"],
                "HarshitMath",
                f"PreReq {prereq_id}: {title[:40]}",
                report["score_pct"],
                100,
                hpp.format_report_details(report),
                time_spent,
                flush_sheets=False,
            )
            db.save_harshit_practice_session(
                user["id"],
                prereq_id,
                [str(q.get("id", "")) for q in questions],
                [str(q.get("question", "")).strip() for q in questions],
            )

        session_id = st.session_state.get(_ss_key(prereq_id, "session_id"))
        if user and session_id and st.session_state.get(_ss_key(prereq_id, "persist_saved_for")) != session_id:
            st.session_state[_ss_key(prereq_id, "persist_saved_for")] = session_id
            try:
                gss.persist_edgenuity_practice(
                    user_name=name,
                    user_id=user["id"],
                    session_id=session_id,
                    session_kind="harshit_prereq",
                    unit_id=prereq_id + hmc.SESSION_UNIT_OFFSET,
                    unit_label=f"PreReq {prereq_id} — {title}",
                    report=report,
                    failed_questions=ec3mail.build_failed_questions(questions, answers),
                    time_spent_seconds=time_spent,
                )
            except Exception:
                pass

        if session_id and st.session_state.get(_ss_key(prereq_id, "email_sent_for")) != session_id:
            st.session_state[_ss_key(prereq_id, "email_sent_for")] = session_id
            if ec3mail.practice_email_enabled():
                mail_result = ec3mail.send_harshit_report_email(
                    student_name=name or "Student",
                    unit_title=f"PreReq {prereq_id}: {title}",
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

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Practice again", key=f"hm_pr_again_{prereq_id}", use_container_width=True):
                _start_practice(prereq_id)
                st.rerun()
        with c2:
            if st.button("Back to bucket", key=f"hm_pr_done_{prereq_id}", use_container_width=True):
                st.session_state.current_page = "harshit_prereq_bucket"
                st.rerun()


def _render_choices(q: dict, current: int, prereq_id: int) -> int | None:
    opts = q["options"]
    ans_col1, ans_col2 = st.columns(2, gap="medium")
    for i, opt in enumerate(opts):
        col = ans_col1 if i % 2 == 0 else ans_col2
        with col:
            if st.button(
                hmr.format_option_label(str(opt)),
                key=f"hm_pr_opt_{prereq_id}_{current}_{i}",
                use_container_width=True,
                type="primary",
            ):
                return i
    return None
