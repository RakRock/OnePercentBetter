"""Solving Linear Equations tab — weekly strategy/level setup and practice."""

from __future__ import annotations

import os
import time

import streamlit as st

import arjun_linear_equation_practice as leqp
import arjun_linear_equation_strategies as leqs
import database as db
import edgenuity_practice_email as ec3mail


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


def _render_option_row(index: int, option: str, option_tex: str | None, current: int) -> bool:
    """Render one answer choice as a full-width button with letter + value together."""
    label = chr(65 + index)
    return st.button(
        f"{label}. {option}",
        key=f"leq_opt_{current}_{index}",
        use_container_width=True,
        type="primary",
    )


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
        st.session_state.leq_error = "Configure at least one strategy and level for this week."
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
    st.session_state.current_page = "edgenuity_linear_equations_practice"


def render_setup_panel():
    """Parent/admin: pick strategies and levels for the week."""
    st.markdown("### 📅 Weekly Plan Setup")
    st.caption("Choose which strategies and levels Arjun practices this week. Questions are generated from your selections.")

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
        help="When enabled, practice sessions call xAI Grok to create fresh questions matching your strategy/level plan.",
        key="leq_use_llm",
    )
    if use_llm:
        if _xai_api_key():
            st.caption("✅ XAI_API_KEY found — AI generation will run at practice start.")
        else:
            st.warning(
                "XAI_API_KEY not set in `.streamlit/secrets.toml` or environment. "
                "Practice will fall back to built-in templates."
            )

    current_levels: dict[int, list[str]] = {}
    for item in current.get("strategies", []):
        current_levels[int(item["id"])] = list(item.get("levels", []))

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
        db.save_linear_eq_week_config(week_label.strip(), new_strategies, use_llm=use_llm)
        st.success("Weekly plan saved.")
        st.rerun()

    if current.get("strategies"):
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

    if not config.get("strategies"):
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
    st.caption(
        f"{leqp.DEFAULT_QUESTION_COUNT} questions from your weekly plan · Source: **{source}**"
    )
    if st.button("🎯 Start Practice", type="primary", key="leq_start", use_container_width=True):
        _start_linear_practice(show_spinner=True)
        st.rerun()


def render_practice():
    name = st.session_state.selected_user
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
            options_tex = q.get("options_tex") or []
            for i, opt in enumerate(q["options"]):
                opt_tex = options_tex[i] if i < len(options_tex) else None
                if _render_option_row(i, opt, opt_tex, current):
                    correct = i == q["answer"]
                    st.session_state.leq_answers.append({"choice": i, "correct": correct})
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

        session_id = st.session_state.get("leq_session_id")
        if session_id and st.session_state.get("leq_email_sent_for") != session_id:
            st.session_state.leq_email_sent_for = session_id
            if ec3mail.email_configured():
                mail_result = ec3mail.send_linear_equation_report_email(
                    student_name=name,
                    report=report,
                    time_spent_seconds=time_spent,
                    session_meta=meta,
                )
                if mail_result.ok:
                    st.success(f"📧 Report emailed to {mail_result.recipient}")
                elif not mail_result.skipped:
                    st.warning(f"Email failed: {mail_result.error}")
            else:
                st.caption("Email not configured — practice report saved on screen only.")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎯 Practice Again", key="leq_again", use_container_width=True, type="primary"):
                _start_linear_practice(show_spinner=True)
                st.rerun()
        with c2:
            if st.button("← Back to Linear Equations", key="leq_done_back", use_container_width=True):
                st.session_state.current_page = "edgenuity_course3_home"
                st.session_state.leq_questions = []
                st.rerun()
