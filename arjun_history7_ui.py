"""Streamlit quiz for Arjun's Grade 7 History, Unit 2."""

from __future__ import annotations

import html
import time

import streamlit as st

import arjun_history7 as hist
import database as db


def _esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def _user():
    name = st.session_state.get("selected_user")
    return name, db.get_user(name) if name else None


def _back_dashboard() -> None:
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_activity = None


def _back_home() -> None:
    st.session_state.current_page = "history_home"
    st.session_state.hist_questions = []
    st.session_state.hist_current = 0
    st.session_state.hist_answers = []
    st.session_state.hist_last_feedback = None


def start_quiz(questions: list[dict], label: str, retry: dict) -> None:
    st.session_state.current_page = "history_practice"
    st.session_state.hist_questions = questions
    st.session_state.hist_current = 0
    st.session_state.hist_answers = []
    st.session_state.hist_last_feedback = None
    st.session_state.hist_start_time = time.time()
    st.session_state.hist_score_saved = False
    st.session_state.hist_quiz_label = label
    st.session_state.hist_retry = retry


def render_home() -> None:
    name, user = _user()
    unit = hist.UNIT

    col_nav, _ = st.columns([1, 6])
    with col_nav:
        if st.button("← Back", key="hist_back_dash"):
            _back_dashboard()
            st.rerun()

    st.markdown(
        f"""
        <div style="text-align:center;padding:0.4rem 0 0.8rem 0;">
            <h1 style="font-size:2.4rem;margin-bottom:0.2rem;">📜 {_esc(name)}'s History</h1>
            <p style="color:#6b7280;font-size:1.1rem;margin:0;">
                Grade {hist.GRADE} · Unit {unit['id']}: {_esc(unit['name'])}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    today = db.get_today_scores(user["id"], activity_type=hist.ACTIVITY_TYPE) if user else []
    total = db.get_scores_history(user["id"], activity_type=hist.ACTIVITY_TYPE, days=365) if user else []
    best = max((row["score"] for row in today), default=None)

    stat1, stat2, stat3 = st.columns(3)
    with stat1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">📅 {len(today)}</div>'
            f'<div class="score-label">Quizzes Today</div></div>',
            unsafe_allow_html=True,
        )
    with stat2:
        best_label = f"{best}%" if best is not None else "—"
        st.markdown(
            f'<div class="score-card"><div class="score-number">🎯 {best_label}</div>'
            f'<div class="score-label">Today\'s Best</div></div>',
            unsafe_allow_html=True,
        )
    with stat3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {len(total)}</div>'
            f'<div class="score-label">Total Quizzes</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="padding:1rem 1.2rem;background:{unit['color']}12;border-radius:16px;
             border:2px solid {unit['color']};margin-bottom:0.8rem;">
            <div style="color:{unit['color']};font-size:0.85rem;font-weight:700;">
                UNIT {unit['id']}
            </div>
            <div style="font-size:1.35rem;margin-top:0.2rem;">
                {unit['emoji']} {_esc(unit['name'])}
            </div>
            <p style="color:#4b5563;margin:0.35rem 0 0 0;">{_esc(unit['blurb'])}</p>
            <p style="color:#6b7280;margin:0.35rem 0 0 0;">
                {len(hist.QUESTIONS)} multiple-choice questions · {len(hist.TOPICS)} topics
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        f"Unit {unit['id']} mix · {hist.UNIT_QUIZ_SIZE} questions",
        key="hist_unit_mix",
        type="primary",
    ):
        questions = hist.build_quiz(unit_mix=True)
        start_quiz(
            questions,
            f"Unit {unit['id']}: {unit['name']} mix",
            {"unit_mix": True, "label": f"Unit {unit['id']}: {unit['name']} mix"},
        )
        st.rerun()

    st.markdown("")
    st.markdown("### Topics")
    counts = hist.question_counts()
    cards = st.columns(3, gap="medium")
    for index, topic in enumerate(hist.TOPICS):
        available = counts[topic["id"]]
        with cards[index % 3]:
            st.markdown(
                f"""
                <div style="padding:1rem;border-radius:12px;border-top:5px solid {topic['color']};
                     background:{topic['color']}10;min-height:10.5rem;">
                    <div style="font-size:1.8rem;">{topic['emoji']}</div>
                    <strong style="color:{topic['color']};">{_esc(topic['name'])}</strong>
                    <p style="color:#6b7280;font-size:0.85rem;margin:0.35rem 0;">
                        {available} questions
                    </p>
                    <p style="color:#4b5563;font-size:0.9rem;margin:0;">{_esc(topic['blurb'])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            practice_n = min(hist.TOPIC_QUIZ_SIZE, available)
            if st.button(
                f"Practice · {practice_n} questions",
                key=f"hist_practice_{topic['id']}",
                width="stretch",
            ):
                questions = hist.build_quiz(topic_id=topic["id"])
                label = topic["name"]
                start_quiz(
                    questions,
                    label,
                    {"topic_id": topic["id"], "full_topic": False, "label": label},
                )
                st.rerun()
            if st.button(
                f"All {available} questions",
                key=f"hist_all_{topic['id']}",
                width="stretch",
            ):
                questions = hist.build_quiz(topic_id=topic["id"], full_topic=True)
                label = f"{topic['name']} · all questions"
                start_quiz(
                    questions,
                    label,
                    {"topic_id": topic["id"], "full_topic": True, "label": label},
                )
                st.rerun()


def render_practice() -> None:
    _, user = _user()
    questions = st.session_state.get("hist_questions") or []
    current = int(st.session_state.get("hist_current") or 0)
    total = len(questions)
    done = current >= total and total > 0
    label = st.session_state.get("hist_quiz_label") or hist.UNIT["name"]

    nav, mid, _ = st.columns([1, 4, 1])
    with nav:
        if st.button("← History", key="hist_back_home"):
            _back_home()
            st.rerun()
    with mid:
        if not done and total:
            elapsed = int(time.time() - st.session_state.hist_start_time) if st.session_state.get("hist_start_time") else 0
            st.markdown(
                f"""
                <div style="text-align:center;color:#6b7280;font-size:0.9rem;padding-top:0.5rem;">
                    Question {current + 1} of {total} &nbsp;|&nbsp; ⏱️ {elapsed}s
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
        <div style="text-align:center;margin-bottom:0.4rem;">
            <h1 style="color:{hist.UNIT['color']};margin:0.2rem 0;font-size:2rem;">📜 {_esc(label)}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    progress = (current / total) if total else 0
    st.markdown(
        f"""
        <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.2rem 0;">
            <div style="width:{progress * 100:.0f}%;height:100%;background:linear-gradient(90deg,#b45309,#d97706);
                 border-radius:10px;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if total == 0:
        st.info("This quiz has no questions yet.")
        return

    if not done:
        _render_question(questions[current], current, total)
        return

    _render_results(questions, user, total, label)


def _render_question(question: dict, current: int, total: int) -> None:
    topic = hist.topic_by_id(question["topic"])
    st.markdown(
        f"""
        <div class="gk-question-box">
            <span class="gk-topic-badge" style="background:{topic['color']}20;color:{topic['color']};">
                {topic['emoji']} {_esc(topic['name'])}
            </span>
            <div class="gk-question-text" style="margin-top:0.8rem;font-size:1.35rem;">
                {_esc(question['question'])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    feedback = st.session_state.get("hist_last_feedback")
    if feedback and feedback.get("idx") == current:
        if feedback["correct"]:
            st.markdown(
                f"""
                <div class="correct-answer" style="text-align:center;">
                    ✅ <strong>Correct!</strong>
                    <p style="color:#065f46;font-size:0.95rem;margin-top:0.3rem;">
                        {_esc(question.get('explanation', ''))}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="wrong-answer" style="text-align:center;">
                    Not quite. The answer is <strong>{_esc(feedback['correct_val'])}</strong>
                    <p style="color:#991b1b;font-size:0.95rem;margin-top:0.3rem;">
                        {_esc(question.get('explanation', ''))}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("")
        _, next_col, _ = st.columns([1, 2, 1])
        with next_col:
            if current < total - 1:
                if st.button("Next ➡️", key="hist_next", width="stretch", type="primary"):
                    st.session_state.hist_current += 1
                    st.session_state.hist_last_feedback = None
                    st.rerun()
            elif st.button("🎉 See Results", key="hist_results", width="stretch", type="primary"):
                st.session_state.hist_current = total
                st.session_state.hist_last_feedback = None
                st.rerun()
        return

    left, right = st.columns(2, gap="medium")
    for index, option in enumerate(question["options"]):
        column = left if index % 2 == 0 else right
        with column:
            if st.button(str(option), key=f"hist_opt_{current}_{index}", width="stretch", type="primary"):
                correct_val = question["options"][question["answer"]]
                is_correct = index == question["answer"]
                st.session_state.hist_answers.append(
                    {
                        "picked": option,
                        "correct_val": correct_val,
                        "correct": is_correct,
                    }
                )
                st.session_state.hist_last_feedback = {
                    "idx": current,
                    "correct_val": correct_val,
                    "correct": is_correct,
                }
                st.rerun()


def _render_results(questions: list[dict], user, total: int, label: str) -> None:
    answers = st.session_state.get("hist_answers") or []
    correct_count = sum(1 for answer in answers if answer["correct"])
    score_pct = int((correct_count / total) * 100) if total else 0
    time_spent = int(time.time() - st.session_state.hist_start_time) if st.session_state.get("hist_start_time") else 0
    minutes, seconds = divmod(time_spent, 60)

    if user and not st.session_state.get("hist_score_saved"):
        db.save_activity_score(
            user["id"],
            hist.ACTIVITY_TYPE,
            label,
            score_pct,
            100,
            f"{correct_count}/{total} correct",
            time_spent,
        )
        st.session_state.hist_score_saved = True

    if score_pct == 100:
        emoji, message, color = "🏆", "Perfect score. You know this unit.", "#10b981"
    elif score_pct >= 80:
        emoji, message, color = "🔥", "Excellent. The Rise of Islam is sticking.", "#3b82f6"
    elif score_pct >= 60:
        emoji, message, color = "📜", "Good work. Review the ones you missed.", "#f59e0b"
    else:
        emoji, message, color = "💪", "Keep going. Read each explanation and try the topic again.", "#ef4444"

    st.markdown(
        f"""
        <div style="text-align:center;padding:2rem;background:{color}10;border-radius:20px;
             border:3px solid {color};margin-top:0.5rem;">
            <div style="font-size:4.5rem;">{emoji}</div>
            <h2 style="color:{color};margin:0.4rem 0;">{correct_count} out of {total} correct</h2>
            <p style="font-size:1.15rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown("### Review")
    for index, (question, answer) in enumerate(zip(questions, answers)):
        if answer["correct"]:
            st.markdown(
                f"""
                <div class="correct-answer">
                    <strong>Q{index + 1}.</strong> {_esc(question['question'])}
                    &nbsp; ✅ <strong>{_esc(answer['correct_val'])}</strong>
                    <p style="color:#065f46;font-size:0.85rem;margin:0.3rem 0 0 0;">
                        {_esc(question.get('explanation', ''))}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="wrong-answer">
                    <strong>Q{index + 1}.</strong> {_esc(question['question'])}
                    &nbsp; You said <strong>{_esc(answer['picked'])}</strong>
                    &nbsp; ✅ <strong>{_esc(answer['correct_val'])}</strong>
                    <p style="color:#991b1b;font-size:0.85rem;margin:0.3rem 0 0 0;">
                        {_esc(question.get('explanation', ''))}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("")
    again, home, _ = st.columns([1, 1, 2])
    with again:
        if st.button("Try again", key="hist_retry_btn", width="stretch", type="primary"):
            retry = st.session_state.get("hist_retry") or {}
            questions = hist.build_quiz(
                topic_id=retry.get("topic_id"),
                full_topic=bool(retry.get("full_topic")),
                unit_mix=bool(retry.get("unit_mix")),
            )
            start_quiz(questions, retry.get("label") or label, retry)
            st.rerun()
    with home:
        if st.button("History home", key="hist_results_home", width="stretch"):
            _back_home()
            st.rerun()
