"""MCQ practice session UI for Arjun Spanish (Grok + bank, email on completion)."""

from __future__ import annotations

import os
import time
import uuid

import streamlit as st

import database as db
import edgenuity_practice_email as ec3mail
import google_sheets_sync as gss
from arjun_spanish import bank as esbank
from arjun_spanish import config as escfg
from arjun_spanish import content as es
from arjun_spanish import session as ess

PRIMARY = "#c2410c"


def _ss_key(name: str) -> str:
    return f"es_mcq_{name}"


def _xai_api_key() -> str | None:
    try:
        return st.secrets.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
    except Exception:
        return os.environ.get("XAI_API_KEY")


def ensure_config() -> dict:
    cfg = escfg.ensure_config()
    if cfg.get("topics"):
        return cfg
    starter = escfg.default_config()
    escfg.save_config(starter)
    return starter


def _start_session(*, user_id: int | None = None) -> None:
    config = ensure_config()
    api_key = _xai_api_key()
    use_grok = bool(config.get("use_llm", False))
    count = int(config.get("question_count", es.DEFAULT_SESSION_COUNT))
    spinner_msg = (
        f"Generating {count} questions with Grok… (usually 15–45 sec)"
        if use_grok and api_key
        else f"Building your {count}-question Spanish practice…"
    )
    with st.spinner(spinner_msg):
        questions, err = ess.build_session_set(config, count=count, user_id=user_id, xai_api_key=api_key)

    if not questions:
        st.session_state[_ss_key("error")] = err or "Could not build practice session."
        return

    st.session_state.pop(_ss_key("error"), None)
    if err:
        st.session_state[_ss_key("warn")] = err
    st.session_state[_ss_key("questions")] = questions
    st.session_state[_ss_key("config_snapshot")] = config
    st.session_state[_ss_key("current")] = 0
    st.session_state[_ss_key("answers")] = []
    st.session_state[_ss_key("review_mode")] = False
    st.session_state[_ss_key("review_index")] = 0
    st.session_state[_ss_key("start_time")] = time.time()
    st.session_state[_ss_key("session_id")] = str(uuid.uuid4())
    st.session_state[_ss_key("email_sent_for")] = None
    st.session_state[_ss_key("persist_saved_for")] = None
    st.session_state[_ss_key("feedback")] = None
    st.session_state[_ss_key("last_pick")] = None
    st.session_state.current_page = "arjun_spanish_session"


def render_practice_home_panel() -> None:
    err = st.session_state.pop(_ss_key("error"), None)
    warn = st.session_state.pop(_ss_key("warn"), None)
    if err:
        st.warning(err)
    if warn:
        st.info(warn)

    config = ensure_config()
    count = int(config.get("question_count", es.DEFAULT_SESSION_COUNT))
    st.success(esbank.bank_status_message())

    if ec3mail.practice_email_enabled():
        st.caption(f"📧 {ec3mail.email_status_message()}")
    else:
        st.caption("📧 Email not configured — reports show on screen only.")

    use_grok = bool(config.get("use_llm", False))
    api_key = _xai_api_key()
    if use_grok and api_key:
        mode = "Grok + bank fallback" if not config.get("grok_fresh_only") else "all fresh Grok"
        st.caption(f"{count} questions · {mode} · {len(config.get('topics', []))} topics selected")
    elif use_grok:
        st.caption(f"{count} questions · Grok enabled — add XAI_API_KEY in Practice Setup")
    else:
        st.caption(f"{count} questions from vocabulary bank")

    if config.get("week_label"):
        st.markdown(f"**{config['week_label']}**")

    if st.button("▶️ Start practice", key="es_start_mcq", type="primary", use_container_width=True):
        user_id = None
        name = st.session_state.get("selected_user")
        if name:
            user = db.get_user(name)
            user_id = user["id"] if user else None
        _start_session(user_id=user_id)
        st.rerun()


def render_setup_panel() -> None:
    current = ensure_config()
    st.markdown("### Practice focus")
    st.caption("Choose topics and whether Grok generates fresh vocabulary questions each session.")

    week_label = st.text_input(
        "Session label (optional)",
        value=current.get("week_label", ""),
        placeholder="e.g. Greetings & classroom words",
        key="es_setup_label",
    )

    st.markdown("#### Question generation")
    xai_key = _xai_api_key()
    if xai_key:
        st.caption("xAI (Grok) API key detected.")
    else:
        st.caption("Add `XAI_API_KEY` to `.streamlit/secrets.toml`.")

    use_grok = st.toggle(
        "Generate questions with xAI (Grok)",
        value=bool(current.get("use_llm", True)),
        key="es_setup_grok",
    )
    grok_fresh_only = False
    if use_grok:
        grok_fresh_only = st.radio(
            "Grok mode",
            options=["fast", "fresh"],
            index=1 if current.get("grok_fresh_only") else 0,
            format_func=lambda x: (
                "Fast — Grok batch + bank fallback (recommended)"
                if x == "fast"
                else "All fresh — every question from Grok only"
            ),
            key="es_setup_grok_mode",
        ) == "fresh"

    count = st.slider(
        "Questions per session",
        min_value=5,
        max_value=20,
        value=int(current.get("question_count", es.DEFAULT_SESSION_COUNT)),
        key="es_setup_count",
    )

    selected = set(current.get("topics", []))
    st.markdown("#### Topics")
    new_topics: list[str] = []
    for topic in es.TOPICS:
        on = st.checkbox(
            f"{topic['emoji']} {topic['title']}",
            value=topic["id"] in selected,
            key=f"es_setup_topic_{topic['id']}",
        )
        if on:
            new_topics.append(topic["id"])

    if st.button("Save practice setup", key="es_save_setup", type="primary"):
        if not new_topics:
            st.warning("Select at least one topic.")
            return
        escfg.save_config(
            {
                "week_label": week_label,
                "topics": new_topics,
                "use_llm": use_grok,
                "grok_fresh_only": grok_fresh_only,
                "question_count": count,
            }
        )
        st.success("Practice setup saved.")
        st.rerun()


def _render_review(questions: list[dict], answers: list[dict]) -> None:
    total = len(questions)
    idx = st.session_state.get(_ss_key("review_index"), 0)
    idx = max(0, min(idx, total - 1))
    st.session_state[_ss_key("review_index")] = idx

    q = questions[idx]
    ans = answers[idx] if idx < len(answers) else None

    if st.button("← Results", key="es_review_back"):
        st.session_state[_ss_key("review_mode")] = False
        st.rerun()

    status = "✅ Correct" if ans and ans.get("correct") else "❌ Incorrect"
    st.caption(f"Review question {idx + 1} of {total} · {status}")
    st.markdown(f"**{q['question']}**")
    if ans:
        st.markdown(f"Your answer: **{ans.get('picked', '?')}** · Correct: **{ans.get('correct_val', '?')}**")
    if q.get("explanation"):
        st.info(f"**Tip:** {q['explanation']}")

    c1, c2 = st.columns(2)
    with c1:
        if idx > 0 and st.button("← Previous", key="es_rev_prev"):
            st.session_state[_ss_key("review_index")] = idx - 1
            st.rerun()
    with c2:
        if idx < total - 1 and st.button("Next →", key="es_rev_next"):
            st.session_state[_ss_key("review_index")] = idx + 1
            st.rerun()


def render_session() -> None:
    name = st.session_state.get("selected_user")
    user = db.get_user(name) if name else None
    questions = st.session_state.get(_ss_key("questions"), [])
    config = st.session_state.get(_ss_key("config_snapshot")) or ensure_config()
    current = int(st.session_state.get(_ss_key("current"), 0))
    total = len(questions)

    if st.button("← Spanish home", key="es_session_home"):
        st.session_state.current_page = "arjun_spanish_home"
        st.session_state[_ss_key("questions")] = []
        st.session_state[_ss_key("current")] = 0
        st.session_state[_ss_key("answers")] = []
        st.session_state[_ss_key("review_mode")] = False
        st.session_state[_ss_key("feedback")] = None
        st.session_state[_ss_key("last_pick")] = None
        st.rerun()

    st.markdown("## 🇪🇸 Spanish Practice")
    if config.get("week_label"):
        st.caption(config["week_label"])

    if not questions:
        st.warning("No questions loaded — start a session from Spanish home.")
        return

    answers = st.session_state.get(_ss_key("answers"), [])
    is_done = current >= total

    if is_done and st.session_state.get(_ss_key("review_mode")):
        _render_review(questions, answers)
        return

    if not is_done:
        st.progress((current / total) if total else 0, text=f"Question {current + 1} of {total}")
        q = questions[current]
        src = q.get("source", "bank")
        src_label = {"llm": "Generated with Grok", "ai_bank": "Saved Grok question", "bank": "Vocabulary bank"}.get(
            src, src
        )
        st.caption(f"{q.get('category_label', '')} · {src_label}")
        st.markdown(f"**{q['question']}**")

        feedback = st.session_state.get(_ss_key("feedback"))
        if feedback is None:
            picked = None
            cols = st.columns(2)
            for idx, opt in enumerate(q["options"]):
                with cols[idx % 2]:
                    if st.button(str(opt), key=f"es_choice_{current}_{idx}", use_container_width=True):
                        picked = idx

            if picked is not None:
                correct = picked == int(q["answer"])
                answers.append(
                    {
                        "picked": q["options"][picked],
                        "correct": correct,
                        "correct_val": q["options"][int(q["answer"])],
                        "category": q.get("category_label", ""),
                    }
                )
                st.session_state[_ss_key("answers")] = answers
                st.session_state[_ss_key("feedback")] = "ok" if correct else "no"
                st.session_state[_ss_key("last_pick")] = picked
                st.rerun()
            return

        correct_answer = q["options"][int(q["answer"])]
        if feedback == "ok":
            st.success(f"✅ Correct! **{correct_answer}**")
        else:
            pick_idx = st.session_state.get(_ss_key("last_pick"))
            picked_text = (
                q["options"][pick_idx] if isinstance(pick_idx, int) and 0 <= pick_idx < len(q["options"]) else "?"
            )
            st.error(f"❌ Wrong — you chose **{picked_text}**. The answer is **{correct_answer}**.")
        if q.get("explanation"):
            st.info(f"💡 {q['explanation']}")
        if st.button("Next →", key=f"es_mcq_next_{current}", use_container_width=True, type="primary"):
            st.session_state[_ss_key("feedback")] = None
            st.session_state[_ss_key("last_pick")] = None
            st.session_state[_ss_key("current")] = current + 1
            st.rerun()
        return

    # --- Complete ---
    elapsed = time.time() - st.session_state.get(_ss_key("start_time"), time.time())
    time_spent = int(elapsed)
    report = ess.build_session_report(questions, answers, student_name=name or "Arjun")
    meta = ess.session_meta_from_config(config)
    minutes, seconds = divmod(time_spent, 60)

    if report["score_pct"] == 100:
        emoji, message, color = "🏆", "¡Perfecto!", "#10b981"
    elif report["score_pct"] >= 80:
        emoji, message, color = "🔥", "¡Muy bien!", PRIMARY
    elif report["score_pct"] >= 60:
        emoji, message, color = "📚", "Good progress — keep practicing!", "#f59e0b"
    else:
        emoji, message, color = "💪", "Review the topics below and try again!", "#ef4444"

    st.markdown(
        f"""
        <div style="text-align:center;padding:1.6rem;background:{color}10;border-radius:20px;
             border:3px solid {color};margin-top:0.5rem;">
            <div style="font-size:4rem;">{emoji}</div>
            <h2 style="color:{color};margin:0.4rem 0;">
                {report['correct_count']} of {report['total']} correct ({report['score_pct']}%)
            </h2>
            <p style="font-size:1.1rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ {minutes}m {seconds}s</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if report.get("strengths"):
        st.markdown("#### ✅ Doing well")
        for item in report["strengths"]:
            st.markdown(f"- {item['name']} — {item['correct']}/{item['total']} ({item['pct']}%)")
    if report.get("needs_revision"):
        st.markdown("#### 📚 Review these topics")
        for item in report["needs_revision"]:
            st.markdown(f"- {item['name']} — {item['correct']}/{item['total']} ({item['pct']}%)")
    if report.get("tip"):
        st.info(f"**Focus next:** {report['tip']}")

    session_id = st.session_state.get(_ss_key("session_id"))
    if user and session_id and st.session_state.get(_ss_key("persist_saved_for")) != session_id:
        st.session_state[_ss_key("persist_saved_for")] = session_id
        week_label = config.get("week_label") or "Spanish practice"
        failed = ec3mail.build_failed_questions(questions, answers)
        try:
            _, sheet_err = gss.persist_edgenuity_practice(
                user_name=name,
                user_id=user["id"],
                session_id=session_id,
                session_kind="spanish_mcq",
                unit_id=es.SESSION_UNIT_OFFSET,
                unit_label=f"Spanish — {week_label}",
                report=report,
                failed_questions=failed,
                time_spent_seconds=time_spent,
                question_ids=[str(q.get("id", "")) for q in questions],
            )
            if sheet_err:
                st.warning(f"Google Sheet sync note: {sheet_err}")
        except Exception as exc:
            st.warning(f"Google Sheet sync failed (saved locally): {exc}")

        db.save_ec3_practice_session(user["id"], es.SESSION_UNIT_OFFSET, [str(q.get("id", "")) for q in questions])
        db.save_activity_score(
            user["id"],
            "Spanish",
            f"Practice: {week_label[:48]}",
            report["score_pct"],
            100,
            ess.format_report_details(report),
            time_spent,
            flush_sheets=False,
        )

    if session_id and st.session_state.get(_ss_key("email_sent_for")) != session_id:
        st.session_state[_ss_key("email_sent_for")] = session_id
        if ec3mail.practice_email_enabled():
            mail_result = ec3mail.send_spanish_report_email(
                student_name=name or "Arjun",
                unit_title="Spanish Vocabulary",
                unit_subtitle=config.get("week_label") or "Daily practice",
                report=report,
                time_spent_seconds=time_spent,
                session_meta=meta,
                questions=questions,
                answers=answers,
            )
            ec3mail.render_practice_email_result(mail_result)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 Review answers", key="es_review_start", use_container_width=True, type="primary"):
            st.session_state[_ss_key("review_mode")] = True
            st.session_state[_ss_key("review_index")] = 0
            st.rerun()
    with c2:
        if st.button("▶️ Practice again", key="es_session_again", use_container_width=True):
            uid = user["id"] if user else None
            _start_session(user_id=uid)
            st.rerun()
