"""Solving Linear Equations tab — weekly strategy/level setup and practice."""

from __future__ import annotations

import os
import time

import streamlit as st

import arjun_linear_equation_practice as leqp
import arjun_linear_equation_strategies as leqs
import arjun_mental_math_drills as mmd
import database as db
import edgenuity_practice_email as ec3mail
import google_sheets_sync as gss


def _xai_api_key() -> str | None:
    try:
        return st.secrets.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
    except Exception:
        return os.environ.get("XAI_API_KEY")


def _render_math_text(text: str, tex: str | None = None, *, display: bool = True) -> None:
    """Show math with stacked fractions via LaTeX when fractions are present."""
    latex = tex or leqs.text_to_latex(text)
    prefix = r"\displaystyle " if display else r""
    normalized = leqs._normalize_math_text(text)
    if leqs.has_fraction_markup(text) or "\\frac" in latex or "=" in normalized:
        st.latex(prefix + latex)
    else:
        st.markdown(text)


_LEQ_OPTION_CSS = """
<style>
section.main [data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
    width: 100%;
    min-height: 3.25rem;
    padding: 0.8rem 1.15rem;
    text-align: center;
    justify-content: center;
    background: #ffffff !important;
    color: #1f2937 !important;
    border: 2px solid #e5e7eb !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.07);
    font-weight: 700 !important;
    font-size: 1.08rem !important;
    line-height: 1.35 !important;
    letter-spacing: 0.02em;
    transition: border-color 0.15s ease, background 0.15s ease, box-shadow 0.15s ease;
}
section.main [data-testid="stVerticalBlockBorderWrapper"] .stButton > button:hover {
    border-color: #6366f1 !important;
    background: #f5f3ff !important;
    color: #4338ca !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.16);
}
section.main [data-testid="stVerticalBlockBorderWrapper"] .stButton > button:active {
    border-color: #4f46e5 !important;
    background: #ede9fe !important;
}
</style>
"""


def _render_question(q: dict) -> None:
    """Instruction (markdown), equation (LaTeX), and follow-up (markdown)."""
    instruction = q.get("instruction", "")
    eq = q.get("equation", "")
    followup = q.get("followup", "")
    if not eq:
        instruction, eq, followup = leqs.split_question(q["question"])
    if eq:
        if instruction:
            st.markdown(f"### {instruction}")
        with st.container(border=True):
            st.latex(r"\displaystyle " + leqs.text_to_latex(eq))
        if followup:
            st.markdown(f"**{followup}**")
        return
    st.markdown(f"### {q['question']}")


def _format_option_display(option: str) -> str:
    """Readable option text — unicode minus and no ambiguous separators."""
    s = str(option).strip().replace("−", "-")
    if s.startswith("-"):
        return "\u2212" + s[1:]
    return s


def _option_button(index: int, option: str, current: int) -> bool:
    letter = chr(65 + index)
    display = _format_option_display(option)
    badge_col, btn_col = st.columns([0.55, 5.45], gap="small")
    with badge_col:
        st.markdown(
            f'<p style="font-weight:800;font-size:1.15rem;color:#6366f1;margin:0;'
            f'padding-top:0.72rem;text-align:center;line-height:1;">{letter}.</p>',
            unsafe_allow_html=True,
        )
    with btn_col:
        return st.button(
            display,
            key=f"leq_opt_{current}_{index}",
            use_container_width=True,
            type="secondary",
        )


def _render_answer_choices(q: dict, current: int) -> int | None:
    """Render answer choices in a centered grid; return selected index or None."""
    opts = q["options"]
    st.markdown(_LEQ_OPTION_CSS, unsafe_allow_html=True)

    long_text = any(len(str(o)) > 44 for o in opts)
    _, mid, _ = st.columns([1, 7, 1])
    with mid:
        with st.container(border=True):
            st.markdown(
                '<p style="color:#6366f1;font-size:0.88rem;font-weight:700;'
                'margin:0 0 0.75rem 0;text-transform:uppercase;letter-spacing:0.06em;">Choose your answer</p>',
                unsafe_allow_html=True,
            )
            if long_text:
                for i, opt in enumerate(opts):
                    if _option_button(i, opt, current):
                        return i
            else:
                for row_start in (0, 2):
                    if row_start >= len(opts):
                        break
                    c1, c2 = st.columns(2, gap="medium")
                    for col_idx, opt_idx in enumerate((row_start, row_start + 1)):
                        if opt_idx >= len(opts):
                            continue
                        with (c1 if col_idx == 0 else c2):
                            if _option_button(opt_idx, opts[opt_idx], current):
                                return opt_idx
    return None


def _back_edgenuity_home():
    st.session_state.current_page = "edgenuity_course3_home"


def _start_linear_practice(*, show_spinner: bool = False):
    config = db.get_linear_eq_week_config()
    api_key = _xai_api_key()

    def _build():
        return leqp.build_session_set(config, count=leqp.DEFAULT_QUESTION_COUNT, xai_api_key=api_key)

    if show_spinner and config.get("use_llm") and api_key:
        with st.spinner("Generating questions with xAI Grok…"):
            questions = _build()
    else:
        questions = _build()

    if not questions:
        st.session_state.leq_error = (
            "Configure at least one equation strategy/level or mental math drill for this week."
        )
        return

    if config.get("use_llm") and not api_key:
        st.session_state.leq_warn = (
            "AI generation is enabled but XAI_API_KEY is missing — used built-in question templates instead."
        )
    elif config.get("use_llm") and questions and questions[0].get("source") == "template":
        st.session_state.leq_warn = "AI generation failed — used built-in question templates instead."
    else:
        st.session_state.pop("leq_warn", None)

    st.session_state.leq_questions = questions
    st.session_state.leq_config_snapshot = config
    st.session_state.leq_current = 0
    st.session_state.leq_answers = []
    st.session_state.leq_last_feedback = None
    st.session_state.leq_start_time = time.time()
    st.session_state.leq_session_id = f"leq-{time.time()}"
    st.session_state.leq_email_sent_for = None
    st.session_state.leq_persist_saved_for = None
    st.session_state.leq_review_mode = False
    st.session_state.leq_review_index = 0
    st.session_state.current_page = "edgenuity_linear_equations_practice"


def _render_leq_review_choices(q: dict, ans: dict | None, review_index: int) -> None:
    """Show answer choices read-only with correct/wrong highlighting."""
    opts = q["options"]
    picked_idx = ans.get("choice") if ans else None
    correct_idx = q["answer"]

    st.markdown(_LEQ_OPTION_CSS, unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 7, 1])
    with mid:
        with st.container(border=True):
            st.markdown(
                '<p style="color:#6366f1;font-size:0.88rem;font-weight:700;'
                'margin:0 0 0.75rem 0;text-transform:uppercase;letter-spacing:0.06em;">Your answers</p>',
                unsafe_allow_html=True,
            )
            for i, opt in enumerate(opts):
                letter = chr(65 + i)
                display = _format_option_display(opt)
                if i == correct_idx:
                    css = "correct-answer"
                    suffix = " — correct answer"
                elif picked_idx is not None and i == picked_idx and i != correct_idx:
                    css = "wrong-answer"
                    suffix = " — your answer"
                else:
                    css = ""
                    suffix = ""
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


def _render_leq_review(questions: list, answers: list) -> None:
    """Walk through graded linear-equation questions to review mistakes."""
    total = len(questions)
    idx = st.session_state.get("leq_review_index", 0)
    idx = max(0, min(idx, total - 1))
    st.session_state.leq_review_index = idx

    q = questions[idx]
    ans = answers[idx] if idx < len(answers) else None

    col_back, col_title, _ = st.columns([1, 4, 1])
    with col_back:
        if st.button("← Results", key="leq_review_back_results", use_container_width=True):
            st.session_state.leq_review_mode = False
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
        <div style="background:linear-gradient(90deg,#6366f1,#8b5cf6);width:{progress*100:.0f}%;height:100%;"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<p style="color:#6366f1;font-size:0.85rem;margin-bottom:0.25rem;">'
        f'{q.get("category_label", "")}</p>',
        unsafe_allow_html=True,
    )
    _render_question(q)
    _render_leq_review_choices(q, ans, idx)

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
        if idx > 0 and st.button("⬅️ Previous", key="leq_review_prev", use_container_width=True):
            st.session_state.leq_review_index = idx - 1
            st.rerun()
    with col_next:
        if idx < total - 1 and st.button("Next ➡️", key="leq_review_next", use_container_width=True, type="primary"):
            st.session_state.leq_review_index = idx + 1
            st.rerun()
    with col_mid:
        wrong_indices = [i for i, a in enumerate(answers) if not a.get("correct")]
        if wrong_indices and st.button("Jump to next mistake", key="leq_review_jump_wrong", use_container_width=True):
            next_wrong = next((i for i in wrong_indices if i > idx), wrong_indices[0])
            st.session_state.leq_review_index = next_wrong
            st.rerun()


def render_setup_panel():
    """Parent/admin: pick strategies and levels for the week."""
    st.markdown("### 📅 Weekly Plan Setup")
    st.caption("Choose which strategies and levels Arjun practices this week. Questions are generated from your selections.")
    try:
        import google_sheets_sync as gss

        if gss.is_configured():
            st.caption(
                f"Plans sync to Google Sheet tab **{gss.WEEK_PLAN_WORKSHEET}** and reload automatically on app start."
            )
    except Exception:
        pass

    current = db.get_linear_eq_week_config()
    week_label = st.text_input(
        "Week label (optional)",
        value=current.get("week_label", ""),
        placeholder="e.g. Week of Jul 28 — Inspection + Inverse Ops",
        key="leq_week_label",
    )

    use_llm = st.toggle(
        "Generate questions with AI (xAI Grok)",
        value=bool(current.get("use_llm", False)),
        help=(
            "When enabled, **Start Practice** and **Start Daily Practice** on every Edgenuity unit "
            "create fresh multiple-choice questions via xAI Grok instead of the built-in bank."
        ),
        key="leq_use_llm",
    )
    if use_llm:
        if _xai_api_key():
            st.caption(
                "✅ XAI_API_KEY found — new questions are generated each time you start a practice session "
                "(all Course 3 units + Solving Linear Equations)."
            )
        else:
            st.warning(
                "XAI_API_KEY not set in `.streamlit/secrets.toml` or environment. "
                "Practice will fall back to built-in templates."
            )

    current_levels: dict[int, list[str]] = {}
    for item in current.get("strategies", []):
        current_levels[int(item["id"])] = list(item.get("levels", []))

    current_mm_levels: dict[str, list[str]] = {}
    for item in current.get("mental_math", []):
        current_mm_levels[str(item["id"])] = list(item.get("levels", []))

    st.markdown("---")
    st.markdown("#### ⚡ Mental Math Muscle Memory")
    st.caption(
        "Turn on drills and pick levels — these drive quick warm-up questions at the start of each "
        "practice session (linear equations and Course 3 units when AI mode is on)."
    )

    mm_count_default = int(current.get("mental_math_count", mmd.MENTAL_MATH_PER_SESSION))
    mental_math_count = st.slider(
        "Mental math questions per session",
        min_value=0,
        max_value=mmd.MENTAL_MATH_COUNT_MAX,
        value=mm_count_default,
        help="How many warm-up questions to prepend when at least one drill is enabled.",
        key="leq_mm_count",
    )

    new_mental: list[dict] = []
    for group_idx, (group_name, drill_ids) in enumerate(mmd.DRILL_GROUPS.items()):
        with st.expander(f"**{group_name}**", expanded=(group_idx == 0)):
            for did in drill_ids:
                info = mmd.DRILLS[did]
                level_options = {f"Level {k} — {v}": k for k, v in info["levels"].items()}
                saved_levels = current_mm_levels.get(did, [])
                enabled_default = bool(saved_levels)
                col_on, col_lv = st.columns([1, 4])
                with col_on:
                    enabled = st.checkbox(
                        "On",
                        value=enabled_default,
                        key=f"leq_mm_on_{did}",
                        label_visibility="collapsed",
                    )
                with col_lv:
                    default = [
                        f"Level {k} — {v}"
                        for k, v in info["levels"].items()
                        if k in saved_levels
                    ]
                    picked = st.multiselect(
                        f"{info['emoji']} {info['name']}",
                        options=list(level_options.keys()),
                        default=default if enabled_default else [],
                        disabled=not enabled,
                        key=f"leq_mm_{did}",
                    )
                if enabled:
                    levels = [level_options[p] for p in picked]
                    if levels:
                        new_mental.append({"id": did, "levels": levels})
                    elif saved_levels:
                        st.caption("Pick at least one level, or turn this drill off.")

    st.markdown("---")
    st.markdown("#### ⚖️ Linear Equation Strategies")

    new_strategies: list[dict] = []
    for sid in sorted(leqs.STRATEGIES):
        info = leqs.STRATEGIES[sid]
        level_options = {f"Level {k} — {v}": k for k, v in info["levels"].items()}
        default = [f"Level {k} — {v}" for k, v in info["levels"].items() if k in current_levels.get(sid, [])]
        picked = st.multiselect(
            f"**Strategy {sid}: {info['name']}**",
            options=list(level_options.keys()),
            default=default,
            key=f"leq_strat_{sid}",
        )
        levels = [level_options[p] for p in picked]
        if levels:
            new_strategies.append({"id": sid, "levels": levels})

    if st.button("💾 Save weekly plan", type="primary", key="leq_save_plan"):
        db.save_linear_eq_week_config(
            week_label.strip(),
            new_strategies,
            mental_math=new_mental,
            mental_math_count=mental_math_count,
            use_llm=use_llm,
        )
        st.success("Weekly plan saved.")
        st.rerun()

    if current.get("strategies") or current.get("mental_math"):
        st.markdown("**Current active plan**")
        st.code(leqs.format_week_plan_summary(current), language=None)


def render_practice_home():
    """Student view: show plan summary and start practice."""
    config = db.get_linear_eq_week_config()
    err = st.session_state.pop("leq_error", None)
    warn = st.session_state.pop("leq_warn", None)
    if err:
        st.warning(err)
    if warn:
        st.warning(warn)

    if not config.get("strategies") and not config.get("mental_math"):
        st.info("No weekly plan yet. Use **Week Setup** to choose strategies and levels.")
        return

    if config.get("week_label"):
        st.markdown(f"**{config['week_label']}**")

    st.markdown("**This week's focus**")
    for line in leqs.format_week_plan_summary(config).split("\n"):
        if line.strip() and not line.startswith("Week:"):
            st.markdown(f"- {line}")

    st.markdown("### 📝 Practice Session")
    source = "xAI Grok" if config.get("use_llm") else "built-in templates"
    mm_count = mmd.get_mental_math_count(config)
    eq_count = leqp.DEFAULT_QUESTION_COUNT
    if mm_count and config.get("strategies"):
        q_desc = f"{mm_count} mental math warm-ups + {eq_count} equation questions"
    elif mm_count:
        q_desc = f"{mm_count} mental math questions"
    else:
        q_desc = f"{eq_count} questions"
    st.caption(f"{q_desc} from your weekly plan · Source: **{source}**")
    if st.button("🎯 Start Practice", type="primary", key="leq_start", use_container_width=True):
        _start_linear_practice(show_spinner=True)
        st.rerun()


def render_practice():
    name = st.session_state.selected_user
    user = db.get_user(name) if name else None
    questions = st.session_state.get("leq_questions", [])
    config = st.session_state.get("leq_config_snapshot") or db.get_linear_eq_week_config()
    current = st.session_state.get("leq_current", 0)
    total = len(questions)
    is_done = current >= total

    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← Back", key="leq_practice_back"):
            st.session_state.current_page = "edgenuity_course3_home"
            st.session_state.leq_questions = []
            st.session_state.leq_current = 0
            st.session_state.leq_answers = []
            st.session_state.leq_last_feedback = None
            st.session_state.leq_review_mode = False
            st.session_state.leq_review_index = 0
            st.rerun()
    with col_nav_mid:
        if not is_done and total:
            elapsed = int(time.time() - st.session_state.leq_start_time) if st.session_state.get("leq_start_time") else 0
            st.markdown(
                f'<div style="text-align:center;color:#6b7280;font-size:0.9rem;padding-top:0.5rem;">'
                f"Question {current + 1} of {total} &nbsp;|&nbsp; ⏱️ {elapsed}s</div>",
                unsafe_allow_html=True,
            )

    st.markdown(
        """
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: #6366f1; margin: 0.3rem 0; font-size: 2.2rem;">⚖️ Solving Linear Equations</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if config.get("week_label"):
        st.caption(config["week_label"])

    if not questions:
        st.warning("No questions loaded.")
        return

    answers = st.session_state.get("leq_answers", [])
    if is_done and st.session_state.get("leq_review_mode"):
        _render_leq_review(questions, answers)
        return

    progress = (current / total) if total > 0 else 0
    st.markdown(
        f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="background:linear-gradient(90deg,#6366f1,#8b5cf6);width:{progress*100:.0f}%;height:100%;"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if not is_done:
        q = questions[current]
        st.markdown(
            f'<p style="color:#6366f1;font-size:0.85rem;margin-bottom:0.25rem;">'
            f'{q.get("category_label", "")}</p>',
            unsafe_allow_html=True,
        )
        _render_question(q)

        last_feedback = st.session_state.get("leq_last_feedback")
        if last_feedback and last_feedback.get("q_index") == current:
            if last_feedback["correct"]:
                st.success(f"✅ Correct! {q.get('explanation', '')}")
            else:
                st.error(f"❌ Not quite. {q.get('explanation', '')}")
            if st.button("Next →", key="leq_next", use_container_width=True, type="primary"):
                st.session_state.leq_current += 1
                st.session_state.leq_last_feedback = None
                st.rerun()
        else:
            picked = _render_answer_choices(q, current)
            if picked is not None:
                correct = picked == q["answer"]
                st.session_state.leq_answers.append({"choice": picked, "correct": correct})
                st.session_state.leq_last_feedback = {"q_index": current, "correct": correct}
                st.rerun()
    else:
        answers = st.session_state.get("leq_answers", [])
        time_spent = int(time.time() - st.session_state.leq_start_time) if st.session_state.get("leq_start_time") else 0
        report = leqp.build_session_report(questions, answers)
        meta = leqp.session_meta_from_config(config)

        st.balloons()
        st.markdown(f"## 🎉 Done! **{report['correct_count']}/{report['total']}** ({report['score_pct']}%)")

        st.markdown("#### ✅ Doing well")
        if report["strengths"]:
            for item in report["strengths"]:
                st.markdown(f"- {item['emoji']} {item['name']} — {item['correct']}/{item['total']} ({item['pct']}%)")
        else:
            st.caption("Keep practicing — aim for 80%+ per strategy/level.")

        if report["needs_revision"]:
            st.markdown("#### 📚 Needs revision")
            for item in report["needs_revision"]:
                st.markdown(f"- {item['emoji']} {item['name']} — {item['correct']}/{item['total']} ({item['pct']}%)")

        if user:
            db.save_activity_score(
                user["id"],
                "EdgenuityCourse3",
                "Linear Equations Practice",
                report["score_pct"],
                100,
                leqp.format_report_details(report),
                time_spent,
                flush_sheets=False,
            )

        session_id = st.session_state.get("leq_session_id")
        if user and session_id and st.session_state.get("leq_persist_saved_for") != session_id:
            st.session_state.leq_persist_saved_for = session_id
            week_label = meta.get("week_label") or "Practice"
            failed = ec3mail.build_failed_questions(questions, answers)
            _, sheet_err = gss.persist_edgenuity_practice(
                user_name=name,
                user_id=user["id"],
                session_id=session_id,
                session_kind="linear_equations",
                unit_id=None,
                unit_label=f"Linear Equations — {week_label}",
                report=report,
                failed_questions=failed,
                time_spent_seconds=time_spent,
            )
            if sheet_err:
                st.warning(f"Google Sheet sync failed (saved locally): {sheet_err}")

        session_id = st.session_state.get("leq_session_id")
        if session_id and st.session_state.get("leq_email_sent_for") != session_id:
            st.session_state.leq_email_sent_for = session_id
            if ec3mail.practice_email_enabled():
                mail_result = ec3mail.send_linear_equation_report_email(
                    student_name=name,
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
            if st.button("🔍 Review Answers", key="leq_review_start", use_container_width=True, type="primary"):
                st.session_state.leq_review_mode = True
                st.session_state.leq_review_index = 0
                st.rerun()
        with c2:
            if st.button("🎯 Practice Again", key="leq_again", use_container_width=True):
                _start_linear_practice(show_spinner=True)
                st.rerun()
        with c3:
            if st.button("← Back to Linear Equations", key="leq_done_back", use_container_width=True):
                st.session_state.current_page = "edgenuity_course3_home"
                st.session_state.leq_questions = []
                st.session_state.leq_review_mode = False
                st.rerun()
