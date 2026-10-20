"""Streamlit pages for Arjun's Grade 7 History units."""

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


def _clear_quiz() -> None:
    st.session_state.hist_questions = []
    st.session_state.hist_current = 0
    st.session_state.hist_answers = []
    st.session_state.hist_last_feedback = None


def start_quiz(questions: list[dict], label: str, retry: dict) -> None:
    st.session_state.current_page = "history_home"
    st.session_state.hist_tab = "practice"
    st.session_state.hist_questions = questions
    st.session_state.hist_current = 0
    st.session_state.hist_answers = []
    st.session_state.hist_last_feedback = None
    st.session_state.hist_start_time = time.time()
    st.session_state.hist_score_saved = False
    st.session_state.hist_quiz_label = label
    st.session_state.hist_retry = retry


def _content():
    unit_id = st.session_state.get("hist_unit_id")
    if not unit_id:
        return None
    return hist.content_for(int(unit_id))


def _open_unit(unit_id: int) -> None:
    st.session_state.hist_unit_id = int(unit_id)
    st.session_state.hist_tab = "notes"
    _clear_quiz()


def _render_lesson_notes(content) -> None:
    st.caption(f"{len(content.LESSONS)} short chapters.")
    for lesson in content.LESSONS:
        st.markdown(content.load_lesson_notes(lesson["id"]))
        st.markdown("---")
    st.markdown(content.load_review_notes())


def _render_practice_tab(user, content) -> None:
    questions = st.session_state.get("hist_questions") or []
    current = int(st.session_state.get("hist_current") or 0)
    total = len(questions)
    done = current >= total and total > 0
    unit = content.UNIT
    label = st.session_state.get("hist_quiz_label") or f"Unit {unit['id']}: {unit['name']}"

    if total == 0:
        today = db.get_today_scores(user["id"], activity_type=hist.ACTIVITY_TYPE) if user else []
        best = max((row["score"] for row in today), default=None)
        best_label = f"{best}%" if best is not None else "—"
        st.markdown(
            f"{len(content.QUESTIONS)} multiple-choice questions. "
            f"Each round is {content.UNIT_QUIZ_SIZE} questions. Today's best: {best_label}."
        )
        if st.button(
            f"Start practice · {content.UNIT_QUIZ_SIZE} questions",
            key="hist_start_practice",
            type="primary",
        ):
            quiz_label = f"Unit {unit['id']}: {unit['name']}"
            start_quiz(
                content.build_quiz(unit_mix=True),
                quiz_label,
                {"unit_mix": True, "unit_id": unit["id"], "label": quiz_label},
            )
            st.rerun()
        return

    if not done:
        elapsed = int(time.time() - st.session_state.hist_start_time) if st.session_state.get("hist_start_time") else 0
        st.markdown(
            f"""
            <div style="text-align:center;color:#6b7280;font-size:0.9rem;padding-top:0.2rem;">
                Question {current + 1} of {total} &nbsp;|&nbsp; ⏱️ {elapsed}s
            </div>
            """,
            unsafe_allow_html=True,
        )

    progress = (current / total) if total else 0
    st.markdown(
        f"""
        <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0.4rem 0 1.2rem 0;">
            <div style="width:{progress * 100:.0f}%;height:100%;background:linear-gradient(90deg,{unit['color']},#d97706);
                 border-radius:10px;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not done:
        _render_question(questions[current], current, total)
        return

    _render_results(questions, user, total, label)


def _render_unit_list() -> None:
    col_nav, _ = st.columns([1, 6])
    with col_nav:
        if st.button("← Back", key="hist_back_dash"):
            _back_dashboard()
            st.rerun()

    st.markdown(
        f"""
        <div style="padding:0.2rem 0 0.8rem 0;">
            <h1 style="font-size:2.2rem;margin:0.15rem 0;">📜 Grade {hist.GRADE} History</h1>
            <p style="color:#6b7280;margin:0;">Choose a unit.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for unit in hist.list_units():
        st.markdown(
            f"""
            <div style="padding:0.9rem 1rem;border-radius:12px;border-top:5px solid {unit['color']};
                 background:{unit['color']}10;margin-bottom:0.35rem;">
                <div style="font-size:1.5rem;">{unit['emoji']}</div>
                <strong>Unit {unit['id']} — {_esc(unit['name'])}</strong>
                <p style="color:#4b5563;margin:0.35rem 0 0 0;">{_esc(unit['blurb'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"Open Unit {unit['id']}", key=f"hist_open_unit_{unit['id']}", type="primary"):
            _open_unit(unit["id"])
            st.rerun()


def render_home() -> None:
    content = _content()
    if content is None:
        _render_unit_list()
        return

    _, user = _user()
    unit = content.UNIT
    tab = st.session_state.get("hist_tab") or "notes"

    col_nav, _ = st.columns([1, 6])
    with col_nav:
        if st.button("← Units", key="hist_back_units"):
            st.session_state.hist_unit_id = None
            st.session_state.hist_tab = "notes"
            _clear_quiz()
            st.rerun()

    st.markdown(
        f"""
        <div style="padding:0.2rem 0 0.6rem 0;">
            <div style="color:{unit['color']};font-size:0.85rem;font-weight:700;">
                GRADE {hist.GRADE} HISTORY
            </div>
            <h1 style="font-size:2.2rem;margin:0.15rem 0;">
                {unit['emoji']} Unit {unit['id']} — {_esc(unit['name'])}
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    notes_col, practice_col = st.columns(2)
    with notes_col:
        if st.button(
            "Lesson notes",
            key="hist_tab_notes",
            width="stretch",
            type="primary" if tab == "notes" else "secondary",
        ):
            st.session_state.hist_tab = "notes"
            st.rerun()
    with practice_col:
        if st.button(
            "Practice questions",
            key="hist_tab_practice",
            width="stretch",
            type="primary" if tab == "practice" else "secondary",
        ):
            st.session_state.hist_tab = "practice"
            st.rerun()

    st.markdown("---")
    if tab == "practice":
        _render_practice_tab(user, content)
    else:
        _render_lesson_notes(content)


def render_notes() -> None:
    st.session_state.hist_tab = "notes"
    st.session_state.current_page = "history_home"
    render_home()


def render_practice() -> None:
    st.session_state.hist_tab = "practice"
    st.session_state.current_page = "history_home"
    render_home()


def _render_question(question: dict, current: int, total: int) -> None:
    st.markdown(
        f"""
        <div class="gk-question-box">
            <div class="gk-question-text" style="font-size:1.35rem;">
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
        emoji, message, color = "💪", "Keep going. Read each explanation and try another round.", "#ef4444"

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
            content = hist.content_for(int(retry.get("unit_id") or st.session_state.get("hist_unit_id") or 2))
            questions = content.build_quiz(unit_mix=True)
            start_quiz(questions, retry.get("label") or label, retry)
            st.rerun()
    with home:
        if st.button("Back to start", key="hist_results_home", width="stretch"):
            st.session_state.hist_tab = "practice"
            _clear_quiz()
            st.rerun()
