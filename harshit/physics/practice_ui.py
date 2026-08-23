"""Harshit Physics — practice session UI (15 MCQs, email on completion)."""

from __future__ import annotations

import os
import time

import streamlit as st

import database as db
import edgenuity_practice_email as ec3mail
import google_sheets_sync as gss
from . import components as hpco
from . import content as hpc
from . import practice as hpp
from . import questions as hpq
from . import topics as hpt


def _ss_key(name: str, unit_id: int | None = None) -> str:
    uid = unit_id if unit_id is not None else hpc.active_unit_id()
    return f"hp_u{uid}_{name}"


def _xai_api_key() -> str | None:
    try:
        return st.secrets.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
    except Exception:
        return os.environ.get("XAI_API_KEY")


def ensure_week_config(unit_id: int = 1) -> dict:
    config = db.get_harshit_physics_week_config(unit_id)
    if config.get("topics"):
        return config
    starter = hpt.default_week_config(unit_id)
    db.save_harshit_physics_week_config(
        unit_id,
        starter["week_label"],
        starter["topics"],
        practice_difficulty=int(starter.get("practice_difficulty", 3)),
        use_chapter_llm=bool(starter.get("use_chapter_llm", False)),
        grok_fresh_only=bool(starter.get("grok_fresh_only", False)),
    )
    return db.get_harshit_physics_week_config(unit_id)


def _clear_setup_widget_state(unit_id: int) -> None:
    """Drop Practice Setup widget keys so the next render loads values from the DB."""
    st.session_state.pop(f"hp_setup_label_{unit_id}", None)
    st.session_state.pop(f"hp_setup_grok_{unit_id}", None)
    st.session_state.pop(f"hp_setup_grok_mode_{unit_id}", None)
    for did in hpt.topics_for_unit(unit_id):
        st.session_state.pop(f"hp_setup_day_{unit_id}_{did}", None)


def _questions() -> list[dict]:
    return st.session_state.get(_ss_key("questions"), [])


def _start_practice(*, user_id: int | None = None, unit_id: int | None = None) -> None:
    uid = unit_id if unit_id is not None else hpc.active_unit_id()
    config = ensure_week_config(uid)
    api_key = _xai_api_key()
    use_grok = bool(config.get("use_chapter_llm", False))
    spinner_msg = (
        "Generating questions with Grok… (usually 15–45 sec)"
        if use_grok and api_key
        else "Building your 15-question practice set…"
    )
    with st.spinner(spinner_msg):
        questions, err = hpp.build_session_set(
            uid, config, user_id=user_id, xai_api_key=api_key
        )

    if not questions:
        st.session_state[_ss_key("error", uid)] = err or "Could not build practice session."
        return

    st.session_state.pop(_ss_key("error", uid), None)
    if err:
        st.session_state[_ss_key("warn", uid)] = err
    st.session_state[_ss_key("questions", uid)] = questions
    st.session_state[_ss_key("config_snapshot", uid)] = config
    st.session_state[_ss_key("current", uid)] = 0
    st.session_state[_ss_key("answers", uid)] = []
    st.session_state[_ss_key("feedback", uid)] = None
    st.session_state[_ss_key("review_mode", uid)] = False
    st.session_state[_ss_key("review_index", uid)] = 0
    st.session_state[_ss_key("start_time", uid)] = time.time()
    st.session_state[_ss_key("session_id", uid)] = f"hp-u{uid}-{time.time()}"
    st.session_state.hp_unit_id = uid
    st.session_state.current_page = "harshit_physics_practice"


def render_practice_home(*, stage1_done: bool, unit_id: int = 1) -> None:
    err = st.session_state.pop(_ss_key("error", unit_id), None)
    warn = st.session_state.pop(_ss_key("warn", unit_id), None)
    if err:
        st.warning(err)
    if warn:
        st.info(warn)

    stats = hpq.bank_stats(unit_id)
    if stats["total"]:
        st.success(hpq.bank_status_message(unit_id))
    else:
        st.warning(hpq.bank_status_message(unit_id))

    if not stage1_done:
        st.info(
            "Complete all Stage 1 concept days before starting practice. "
            "Concept learning builds the foundation — practice checks understanding."
        )
        return

    config = ensure_week_config(unit_id)
    st.markdown("### Practice session")
    use_grok = bool(config.get("use_chapter_llm", False))
    api_key = _xai_api_key()
    if use_grok and api_key:
        mode = "Grok + bank fallback" if not config.get("grok_fresh_only") else "all fresh Grok"
        st.caption(
            f"{hpp.DEFAULT_QUESTION_COUNT} questions · {mode} · {stats['total']} in bank"
        )
    elif use_grok:
        st.caption(
            f"{hpp.DEFAULT_QUESTION_COUNT} questions · Grok enabled — add XAI_API_KEY in Practice Setup"
        )
    else:
        st.caption(
            f"{hpp.DEFAULT_QUESTION_COUNT} questions from bank · {stats['total']} available"
        )

    if config.get("week_label"):
        st.markdown(f"**{config['week_label']}**")

    if st.button("Start practice", key=f"hp_start_practice_u{unit_id}", type="primary", use_container_width=True):
        uid = None
        name = st.session_state.get("selected_user")
        if name:
            user = db.get_user(name)
            uid = user["id"] if user else None
        _start_practice(user_id=uid, unit_id=unit_id)
        st.rerun()


def render_setup_panel(unit_id: int = 1) -> None:
    current = db.get_harshit_physics_week_config(unit_id)
    stats = hpq.bank_stats(unit_id)

    st.markdown("### Practice focus")
    st.caption(
        "Choose which topic days and difficulty levels appear in each 15-question session. "
        f"Bank: {stats['total']} questions."
    )

    week_label = st.text_input(
        "Session label (optional)",
        value=current.get("week_label", ""),
        placeholder="e.g. Mirrors & lenses review",
        key=f"hp_setup_label_{unit_id}",
    )

    st.markdown("#### Question generation")
    xai_key = _xai_api_key()
    if xai_key:
        st.caption("xAI (Grok) API key detected.")
    else:
        st.caption("Add `XAI_API_KEY` to `.streamlit/secrets.toml` or your shell environment.")

    use_grok = st.toggle(
        "Generate questions with xAI (Grok)",
        value=bool(current.get("use_chapter_llm", False)),
        help="Uses seed examples from the 200-question bank plus NCERT concept summaries to create fresh MCQs.",
        key=f"hp_setup_grok_{unit_id}",
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
            key=f"hp_setup_grok_mode_{unit_id}",
        ) == "fresh"

    topics_meta = hpt.topics_for_unit(unit_id)
    current_levels: dict[int, list[str]] = {}
    for item in current.get("topics", []):
        current_levels[int(item["id"])] = list(item.get("levels", []))

    st.markdown("#### Topic days & levels")
    new_topics: list[dict] = []
    for did in sorted(topics_meta):
        info = topics_meta[did]
        level_options = {f"Level {k} — {v}": k for k, v in info["levels"].items()}
        default = [
            f"Level {k} — {v}"
            for k, v in info["levels"].items()
            if k in current_levels.get(did, [])
        ]
        picked = st.multiselect(
            f"**Day {did}: {info['name']}**",
            options=list(level_options.keys()),
            default=default,
            key=f"hp_setup_day_{unit_id}_{did}",
        )
        levels = [level_options[p] for p in picked]
        if levels:
            new_topics.append({"id": did, "levels": levels})

    if st.button("Save practice focus", type="primary", key=f"hp_setup_save_{unit_id}"):
        db.save_harshit_physics_week_config(
            unit_id,
            week_label.strip(),
            new_topics,
            practice_difficulty=int(current.get("practice_difficulty", 3)),
            use_chapter_llm=use_grok,
            grok_fresh_only=grok_fresh_only,
        )
        _clear_setup_widget_state(unit_id)
        st.success("Practice focus saved.")
        st.rerun()

    saved = db.get_harshit_physics_week_config(unit_id)
    if saved.get("topics"):
        st.markdown("**Current focus**")
        st.code(hpt.format_week_plan_summary(unit_id, saved), language=None)


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

    for i, opt in enumerate(opts):
        letter = chr(65 + i)
        if i == correct_idx:
            css, suffix = "background:#ecfdf5;border:2px solid #10b981;", " — correct"
        elif picked_idx is not None and i == picked_idx:
            css, suffix = "background:#fef2f2;border:2px solid #ef4444;", " — your answer"
        else:
            css, suffix = "background:#f9fafb;border:2px solid #e5e7eb;", ""
        st.markdown(
            f'<div style="{css}padding:0.85rem 1rem;border-radius:12px;margin-bottom:0.5rem;">'
            f"<strong>{letter}.</strong> {opt}{suffix}</div>",
            unsafe_allow_html=True,
        )


def _render_review(questions: list[dict], answers: list[dict], unit_id: int) -> None:
    total = len(questions)
    idx = st.session_state.get(_ss_key("review_index", unit_id), 0)
    idx = max(0, min(idx, total - 1))
    st.session_state[_ss_key("review_index", unit_id)] = idx

    q = questions[idx]
    ans = answers[idx] if idx < len(answers) else None

    if st.button("← Results", key=f"hp_review_back_u{unit_id}"):
        st.session_state[_ss_key("review_mode", unit_id)] = False
        st.rerun()

    status = "✅ Correct" if ans and ans.get("correct") else "❌ Incorrect"
    st.caption(f"Review question {idx + 1} of {total} · {status}")

    st.markdown(f"**{q['question']}**")
    _render_review_choices(q, ans)
    if q.get("explanation"):
        st.info(f"**Explanation:** {q['explanation']}")

    c1, c2 = st.columns(2)
    with c1:
        if idx > 0 and st.button("← Previous", key=f"hp_rev_prev_u{unit_id}"):
            st.session_state[_ss_key("review_index", unit_id)] = idx - 1
            st.rerun()
    with c2:
        if idx < total - 1 and st.button("Next →", key=f"hp_rev_next_u{unit_id}"):
            st.session_state[_ss_key("review_index", unit_id)] = idx + 1
            st.rerun()


def render_practice() -> None:
    unit_id = hpc.active_unit_id()
    umeta = hpc.unit_meta(unit_id)
    hpco.inject_physics_styles(unit_id)
    name = st.session_state.get("selected_user")
    user = db.get_user(name) if name else None

    questions = st.session_state.get(_ss_key("questions", unit_id), [])
    config = st.session_state.get(_ss_key("config_snapshot", unit_id)) or ensure_week_config(unit_id)
    current = st.session_state.get(_ss_key("current", unit_id), 0)
    total = len(questions)
    is_done = current >= total

    if st.button(f"← Unit {unit_id}"):
        st.session_state.current_page = f"harshit_physics_unit{unit_id}"
        st.session_state[_ss_key("questions", unit_id)] = []
        st.session_state[_ss_key("current", unit_id)] = 0
        st.session_state[_ss_key("answers", unit_id)] = []
        st.session_state[_ss_key("review_mode", unit_id)] = False
        st.rerun()

    st.markdown(f"## Unit {unit_id} Practice — {umeta['title']}")
    if config.get("week_label"):
        st.caption(config["week_label"])

    if not questions:
        st.warning("No questions loaded.")
        return

    answers = st.session_state.get(_ss_key("answers", unit_id), [])

    if is_done and st.session_state.get(_ss_key("review_mode", unit_id)):
        _render_review(questions, answers, unit_id)
        return

    if not is_done:
        progress = (current / total) if total > 0 else 0
        st.progress(progress, text=f"Question {current + 1} of {total}")
        q = questions[current]
        src = q.get("source", "bank")
        src_label = {
            "chapter_llm": "Generated with Grok",
            "bank": "Practice question",
        }.get(src, src)
        st.caption(f"{q.get('category_label', '')} · {src_label}")
        st.markdown(f"**{q['question']}**")

        picked = None
        cols = st.columns(2)
        for idx, opt in enumerate(q["options"]):
            with cols[idx % 2]:
                if st.button(str(opt), key=f"hp_u{unit_id}_choice_{current}_{idx}", use_container_width=True):
                    picked = idx

        if picked is not None:
            correct = picked == int(q["answer"])
            answers.append(
                {
                    "picked": q["options"][picked],
                    "correct": correct,
                    "correct_val": q["options"][int(q["answer"])],
                    "concept_id": q.get("concept_id", ""),
                    "category": q.get("category_label", ""),
                }
            )
            st.session_state[_ss_key("answers", unit_id)] = answers
            if user:
                db.save_harshit_physics_mcq_attempt(
                    user["id"],
                    unit_id=unit_id,
                    day_id=int(q.get("day_id", 0)),
                    question_id=str(q.get("id", "")),
                    selected=q["options"][picked],
                    correct=correct,
                    misconception="" if correct else q.get("category", ""),
                    concept_reviewed=q.get("concept_id", "") if not correct else "",
                )
            st.session_state[_ss_key("current", unit_id)] = current + 1
            st.rerun()
        return

    # --- Session complete ---
    elapsed = time.time() - st.session_state.get(_ss_key("start_time", unit_id), time.time())
    time_spent = int(elapsed)
    report = hpp.build_session_report(questions, answers, student_name=name or "Student")
    meta = hpp.session_meta_from_config(unit_id, config)
    _, session_kind_mcq = hpc.session_kinds(unit_id)

    st.success(f"Practice complete — {report['correct_count']}/{report['total']} ({report['score_pct']}%)")

    if report.get("strengths"):
        st.markdown("#### ✅ Doing well")
        for item in report["strengths"]:
            st.markdown(f"- {item['name']} — {item['correct']}/{item['total']} ({item['pct']}%)")
    if report.get("needs_revision"):
        st.markdown("#### 📚 Review these topics")
        for item in report["needs_revision"]:
            st.markdown(f"- {item['name']} — {item['correct']}/{item['total']} ({item['pct']}%)")

    session_id = st.session_state.get(_ss_key("session_id", unit_id))
    if user and session_id and st.session_state.get(_ss_key("persist_saved_for", unit_id)) != session_id:
        st.session_state[_ss_key("persist_saved_for", unit_id)] = session_id
        week_label = config.get("week_label") or f"Unit {unit_id} practice"
        failed = ec3mail.build_failed_questions(questions, answers)
        try:
            _, sheet_err = gss.persist_edgenuity_practice(
                user_name=name,
                user_id=user["id"],
                session_id=session_id,
                session_kind=session_kind_mcq,
                unit_id=hpc.SESSION_UNIT_OFFSET + unit_id,
                unit_label=f"Physics Unit {unit_id}: {umeta['title']} — {week_label}",
                report=report,
                failed_questions=failed,
                time_spent_seconds=time_spent,
                question_ids=[str(q.get("id", "")) for q in questions],
            )
            if sheet_err:
                st.warning(f"Google Sheet sync note: {sheet_err}")
        except Exception as exc:
            st.warning(f"Google Sheet sync failed (saved locally): {exc}")

        db.save_ec3_practice_session(user["id"], hpc.SESSION_UNIT_OFFSET + unit_id, [str(q.get("id", "")) for q in questions])

        db.save_activity_score(
            user["id"],
            "HarshitPhysics",
            f"Unit {unit_id} Practice: {umeta['title'][:40]}",
            report["score_pct"],
            100,
            hpp.format_report_details(report),
            time_spent,
            flush_sheets=False,
        )

    if session_id and st.session_state.get(_ss_key("email_sent_for", unit_id)) != session_id:
        st.session_state[_ss_key("email_sent_for", unit_id)] = session_id
        if ec3mail.practice_email_enabled():
            mail_result = ec3mail.send_harshit_report_email(
                student_name=name or "Student",
                unit_title=f"Physics Unit {unit_id}: {umeta['title']}",
                unit_subtitle=config.get("week_label") or "Practice session",
                report=report,
                time_spent_seconds=time_spent,
                session_meta=meta,
                questions=questions,
                answers=answers,
            )
            ec3mail.render_practice_email_result(mail_result)
        else:
            st.caption("Email not configured — report shown on screen only.")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔍 Review answers", type="primary", use_container_width=True, key=f"hp_review_u{unit_id}"):
            st.session_state[_ss_key("review_mode", unit_id)] = True
            st.session_state[_ss_key("review_index", unit_id)] = 0
            st.rerun()
    with c2:
        if st.button("Practice again", use_container_width=True, key=f"hp_again_u{unit_id}"):
            uid = user["id"] if user else None
            _start_practice(user_id=uid, unit_id=unit_id)
            st.rerun()
    with c3:
        if st.button(f"← Unit {unit_id} home", use_container_width=True, key=f"hp_home_u{unit_id}"):
            st.session_state.current_page = f"harshit_physics_unit{unit_id}"
            st.session_state[_ss_key("questions", unit_id)] = []
            st.rerun()
