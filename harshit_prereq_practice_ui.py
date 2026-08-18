"""PreReq practice & weekly setup UI — modeled on Edgenuity Linear Equations."""

from __future__ import annotations

import time
import uuid

import streamlit as st

import database as db
import edgenuity_practice_email as ec3mail
import google_sheets_sync as gss
import harshit_math_components as hmc_ui
import harshit_math_content as hmc
import harshit_math_prereqs as hmp
import harshit_prereq_practice as hpp
import harshit_prereq_topics as hpt


def _ss_key(prereq_id: int, name: str) -> str:
    return f"hm_pr{prereq_id}_{name}"


def _questions(prereq_id: int) -> list:
    return st.session_state.get(_ss_key(prereq_id, "questions"), [])


def _start_practice(prereq_id: int):
    config = db.get_harshit_prereq_week_config(prereq_id)
    questions = hpp.build_session_set(prereq_id, config)
    if not questions:
        st.session_state[_ss_key(prereq_id, "error")] = (
            "Select at least one topic and level in Week Setup."
        )
        return
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
    week_label = st.text_input(
        "Week label (optional)",
        value=current.get("week_label", ""),
        placeholder=f"e.g. Week 1 — {prereq['title'][:30]}",
        key=f"hm_setup_label_{prereq_id}",
    )

    warmup_count = st.slider(
        "Warm-up questions per session",
        min_value=0,
        max_value=hpp.MAX_WARMUP,
        value=int(current.get("warmup_count", 2)),
        help="Short Level-A checks before main practice (0 to disable).",
        key=f"hm_setup_warmup_{prereq_id}",
    )

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
            warmup_count=warmup_count,
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

    config = db.get_harshit_prereq_week_config(prereq_id)
    err = st.session_state.pop(_ss_key(prereq_id, "error"), None)
    if err:
        st.warning(err)

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
    mm = int(config.get("warmup_count", 0))
    main = hpp.DEFAULT_QUESTION_COUNT
    if mm:
        st.caption(f"{mm} warm-up(s) + {main} questions from your plan")
    else:
        st.caption(f"{main} questions from your plan")

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

    if not is_done:
        q = questions[current]
        st.markdown(
            f'<p style="color:var(--hm-text-secondary);font-size:0.88rem;">'
            f"Question {current + 1} of {total} · {q.get('category_label', '')}</p>",
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="hm-problem">{q["question"]}</div>', unsafe_allow_html=True)

        fb = st.session_state.get(_ss_key(prereq_id, "feedback"))
        if fb and fb.get("q_index") == current:
            if fb["correct"]:
                _render_soft_success(q.get("explanation", "Correct."))
            else:
                _render_soft_hint(q.get("explanation", "Try reviewing this topic in your notes."))
            if st.button("Continue", key=f"hm_pr_next_{prereq_id}", type="secondary"):
                st.session_state[_ss_key(prereq_id, "current")] += 1
                st.session_state[_ss_key(prereq_id, "feedback")] = None
                st.rerun()
        else:
            picked = _render_choices(q, current, prereq_id)
            if picked is not None:
                correct = picked == q["answer"]
                answers.append({"choice": picked, "correct": correct})
                st.session_state[_ss_key(prereq_id, "answers")] = answers
                st.session_state[_ss_key(prereq_id, "feedback")] = {
                    "q_index": current,
                    "correct": correct,
                }
                st.rerun()
    else:
        time_spent = int(
            time.time() - st.session_state.get(_ss_key(prereq_id, "start_time"), time.time())
        )
        report = hpp.build_session_report(questions, answers)
        meta = hpp.session_meta_from_config(prereq_id, config)

        st.markdown(
            f'<div class="hm-success">Session complete: '
            f'<strong>{report["correct_count"]}/{report["total"]}</strong> '
            f'({report["score_pct"]}%)</div>',
            unsafe_allow_html=True,
        )

        if report["strengths"]:
            st.markdown("**Doing well**")
            for item in report["strengths"]:
                st.markdown(f"- {item['name']} — {item['correct']}/{item['total']} ({item['pct']}%)")
        if report["needs_revision"]:
            st.markdown("**Needs revision**")
            for item in report["needs_revision"]:
                st.markdown(f"- {item['name']} — {item['correct']}/{item['total']} ({item['pct']}%)")

        if user:
            db.save_activity_score(
                user["id"],
                "HarshitMath",
                f"PreReq {prereq_id}: {title[:40]}",
                report["score_pct"],
                100,
                hpp.format_report_details(report),
                time_spent,
            )
            session_id = st.session_state.get(_ss_key(prereq_id, "session_id"), str(uuid.uuid4()))
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
            if ec3mail.email_configured():
                try:
                    ec3mail.send_practice_report_email(
                        student_name=name,
                        unit_title=f"PreReq {prereq_id}: {title}",
                        unit_subtitle=config.get("week_label") or "Weekly practice",
                        report=report,
                        time_spent_seconds=time_spent,
                        session_meta=meta,
                        questions=questions,
                        answers=answers,
                    )
                except Exception:
                    pass

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Practice again", key=f"hm_pr_again_{prereq_id}", use_container_width=True):
                _start_practice(prereq_id)
                st.rerun()
        with c2:
            if st.button("Back to bucket", key=f"hm_pr_done_{prereq_id}", use_container_width=True):
                st.session_state.current_page = "harshit_prereq_bucket"
                st.rerun()


def _render_soft_success(text: str) -> None:
    st.markdown(f'<div class="hm-success">{text}</div>', unsafe_allow_html=True)


def _render_soft_hint(text: str) -> None:
    st.markdown(f'<div class="hm-feedback">{text}</div>', unsafe_allow_html=True)


def _render_choices(q: dict, current: int, prereq_id: int) -> int | None:
    opts = q["options"]
    for i, opt in enumerate(opts):
        if st.button(
            opt,
            key=f"hm_pr_opt_{prereq_id}_{current}_{i}",
            use_container_width=True,
            type="secondary",
        ):
            return i
    return None
