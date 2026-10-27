"""Streamlit UI for Arjun's Friday Concept Check (Unit 1 I–V and Unit 6)."""

from __future__ import annotations

import os
import time
import uuid

import streamlit as st

import arjun_concept_check_form as ccform
import arjun_concept_check_form_llm as ccform_llm
import arjun_course3_answers as c3ans
import database as db
import edgenuity_practice_email as ec3mail

PRIMARY = "#0f766e"
PRIMARY_END = "#14b8a6"


def _xai_api_key() -> str | None:
    try:
        return st.secrets.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
    except Exception:
        return os.environ.get("XAI_API_KEY")


def _clear_session():
    st.session_state.acc_questions = []
    st.session_state.acc_current = 0
    st.session_state.acc_answers = []
    st.session_state.acc_last_feedback = None
    st.session_state.acc_saved = False
    st.session_state.acc_start_time = None
    st.session_state.acc_used_fallback = False
    st.session_state.acc_session_id = None


def _back_dashboard():
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_activity = None
    _clear_session()
    st.session_state.acc_section = None


def _start_section(section_id: str):
    info = ccform.get_section(section_id)
    if not info:
        st.error("Unknown Concept Check section.")
        return
    api_key = _xai_api_key()
    used_fallback = False
    try:
        if not api_key:
            raise RuntimeError("Add XAI_API_KEY to generate a fresh paper.")
        with st.spinner(
            f"Writing a new {info['roman']}) {info['title']} Concept Check from the lesson notes…"
        ):
            questions = ccform_llm.generate_section_set(api_key, section_id)
    except Exception as exc:
        st.warning(f"Grok could not write a fresh set ({exc}). Using the school-paper seeds this time.")
        questions = ccform_llm.fallback_seed_set(section_id)
        used_fallback = True
    if not questions:
        st.error("No questions available for this section.")
        return
    st.session_state.acc_section = section_id
    st.session_state.acc_questions = questions
    st.session_state.acc_current = 0
    st.session_state.acc_answers = []
    st.session_state.acc_last_feedback = None
    st.session_state.acc_saved = False
    st.session_state.acc_used_fallback = used_fallback
    st.session_state.acc_start_time = time.time()
    st.session_state.acc_session_id = str(uuid.uuid4())
    st.session_state.current_page = "concept_check_practice"
    st.rerun()


def render_home():
    name = st.session_state.get("selected_user", "Arjun")
    col_nav, _ = st.columns([1, 6])
    with col_nav:
        if st.button("← Back", key="acc_back_dash"):
            _back_dashboard()
            st.rerun()

    st.markdown(
        f"""
    <div style="text-align:center;padding:0.5rem 0 1rem 0;">
        <h1 style="margin:0;">📝 Concept Check</h1>
        <p style="color:#4b5563;font-size:1.05rem;">
            Friday Math 3 paper · pick one section · new questions every time
        </p>
        <p style="color:#6b7280;">Hi {name}. Pick a section. Fresh numbers from Grok.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.caption(
        "Pick a course unit, then a paper section. "
        "Unit 1 is CC1–CC5 (I–V). Unit 6 is VI-1–VI-3. Unit 7 is VII-1 multi-step equations."
    )

    _render_unit_group("Unit 1 — Numerical relationships", ("I", "II", "III"))
    _render_unit_group("Unit 1 (continued)", ("IV", "V"))
    _render_unit_group(
        "Unit 6 — Patterns and modeling",
        ("VI",),
        start_label="Start Unit 6",
    )
    _render_unit_group(
        "Unit 7 — Solving linear equations",
        ("VII",),
        start_label="Start Unit 7",
    )


def _section_heading(info: dict) -> str:
    title = info["title"]
    if title.startswith("Unit "):
        return title
    return f"{info['roman']}) {title}"


def _render_unit_group(heading: str, section_ids: tuple[str, ...], *, start_label: str | None = None) -> None:
    st.markdown(f"### {heading}")
    cols = st.columns(max(3, len(section_ids)), gap="large")
    for col, sid in zip(cols, section_ids):
        with col:
            info = ccform.get_section(sid)
            if not info:
                continue
            n = len(ccform.seeds_for_section(sid))
            st.markdown(
                f"""
            <div class="score-card" style="border-top: 5px solid {info['color']};">
                <div style="font-size:2.2rem;">{info['emoji']}</div>
                <h3 style="margin:0.4rem 0;">{_section_heading(info)}</h3>
                <p style="color:#6b7280;">{info['short']}</p>
                <p style="color:#9ca3af;font-size:0.85rem;">{n} paper seeds · {info['session_count']} fresh questions</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
            button_label = start_label or f"Start {info['roman']}"
            if st.button(
                button_label,
                key=f"acc_start_{sid}",
                width="stretch",
                type="primary",
            ):
                _start_section(sid)


def render_practice():
    name = st.session_state.get("selected_user", "Arjun")
    user = db.get_user(name) if name else None
    section_id = st.session_state.get("acc_section")
    info = ccform.get_section(section_id) if section_id else None
    questions = st.session_state.get("acc_questions") or []
    current = int(st.session_state.get("acc_current") or 0)
    total = len(questions)
    is_done = current >= total

    col_nav, mid, _ = st.columns([1, 4, 1])
    with col_nav:
        if st.button("← Sections", key="acc_back_home"):
            st.session_state.current_page = "concept_check_home"
            _clear_session()
            st.rerun()
    with mid:
        if info:
            st.markdown(
                f"<h3 style='text-align:center;margin:0;'>{_section_heading(info)}</h3>",
                unsafe_allow_html=True,
            )
            st.caption(
                f"Question {min(current + 1, total)} of {total}"
                + (" · school-paper seeds (Grok unavailable)" if st.session_state.get("acc_used_fallback") else " · fresh Grok set")
            )

    if not questions:
        st.warning("No questions loaded.")
        return

    progress = (current / total) if total else 0
    st.markdown(
        f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress * 100:.0f}%;height:100%;background:linear-gradient(90deg,{PRIMARY},{PRIMARY_END});
             border-radius:10px;"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if not is_done:
        q = questions[current]
        q_html = str(q.get("question", "")).replace("\n", "<br>")
        color = info["color"] if info else PRIMARY
        badge = f"{info['roman']}) {info['title']}" if info else "Concept Check"
        st.markdown(
            f"""
        <div class="gk-question-box">
            <span class="gk-topic-badge" style="background:{color}20;color:{color};">{badge}</span>
            <div class="gk-question-text" style="margin-top:0.8rem;font-size:1.25rem;">{q_html}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        last_feedback = st.session_state.get("acc_last_feedback")
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
                if st.button(label, key="acc_next", width="stretch", type="primary"):
                    st.session_state.acc_current = current + 1
                    st.session_state.acc_last_feedback = None
                    st.rerun()
        else:
            ans_col1, ans_col2 = st.columns(2, gap="medium")
            for i, opt in enumerate(q["options"]):
                col = ans_col1 if i % 2 == 0 else ans_col2
                with col:
                    if st.button(str(opt), key=f"acc_opt_{current}_{i}", width="stretch", type="primary"):
                        is_correct = c3ans.is_pick_correct(q, i)
                        st.session_state.acc_answers.append(
                            {
                                "picked": opt,
                                "correct_val": q["options"][q["answer"]],
                                "correct": is_correct,
                            }
                        )
                        st.session_state.acc_last_feedback = {
                            "idx": current,
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        }
                        st.rerun()
        return

    answers = st.session_state.get("acc_answers") or []
    correct_count = sum(1 for a in answers if a["correct"])
    score_pct = int((correct_count / total) * 100) if total else 0
    time_spent = int(time.time() - st.session_state.acc_start_time) if st.session_state.get("acc_start_time") else 0
    minutes, seconds = divmod(time_spent, 60)
    label = f"{info['roman']}) {info['title']}" if info else "Concept Check"
    report = ccform.build_session_report(questions, answers)
    session_id = st.session_state.get("acc_session_id")

    if user and not st.session_state.get("acc_saved"):
        db.save_activity_score(
            user["id"],
            "ConceptCheck",
            label,
            score_pct,
            100,
            f"{correct_count}/{total} correct",
            time_spent,
        )
        st.session_state.acc_saved = True

    if score_pct == 100:
        res_emoji, message, res_color = "🏆", "Perfect — Friday ready!", "#10b981"
    elif score_pct >= 80:
        res_emoji, message, res_color = "🔥", "Strong Concept Check.", PRIMARY
    elif score_pct >= 60:
        res_emoji, message, res_color = "📝", "Review the missed stems and try a fresh set.", "#f59e0b"
    else:
        res_emoji, message, res_color = "💪", "Read the lesson notes, then start a new paper.", "#ef4444"

    st.markdown(
        f"""
    <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;
         border:3px solid {res_color};margin-top:1rem;">
        <div style="font-size:5rem;">{res_emoji}</div>
        <h2 style="color:{res_color};margin:0.5rem 0;">{correct_count} out of {total} correct!</h2>
        <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
        <p style="color:#9ca3af;">⏱️ {minutes}m {seconds}s · Score: {score_pct}%</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if session_id and st.session_state.get("acc_email_sent_for") != session_id:
        st.session_state.acc_email_sent_for = session_id
        if ec3mail.practice_email_enabled():
            mail_result = ec3mail.send_concept_check_report_email(
                student_name=name,
                unit_title=label,
                unit_subtitle="Friday Concept Check",
                report=report,
                time_spent_seconds=time_spent,
                session_meta={
                    "section": section_id,
                    "origin": "seed_fallback" if st.session_state.get("acc_used_fallback") else "grok",
                },
                questions=questions,
                answers=answers,
            )
            ec3mail.render_practice_email_result(mail_result)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔁 Fresh paper (new Grok set)", key="acc_again", width="stretch", type="primary"):
            _start_section(section_id)
    with c2:
        if st.button("📋 Other sections", key="acc_other", width="stretch"):
            st.session_state.current_page = "concept_check_home"
            _clear_session()
            st.rerun()
