"""15-minute board-format unit test UI for Class 10 Mathematics."""

from __future__ import annotations

import os
from pathlib import Path

import time

import streamlit as st
import streamlit.components.v1 as components

import database as db
import edgenuity_practice_email as ec3mail
import google_sheets_sync as gss
import harshit_class10_unit_test as h10ut
import harshit_class10_unit_test_grader as h10g
import harshit_class10_unit_test_uploads as h10utu
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
    return f"hm10_ut_u{unit_id}_{name}"


def _responses(unit_id: int) -> list[dict]:
    return st.session_state.get(_ss_key(unit_id, "responses"), [])


def _ensure_responses(unit_id: int, count: int) -> list[dict]:
    resp = _responses(unit_id)
    while len(resp) < count:
        resp.append({})
    st.session_state[_ss_key(unit_id, "responses")] = resp
    return resp


def _timer_html(remaining: int, total: int) -> str:
    mins, secs = divmod(remaining, 60)
    pct = int(100 * remaining / total) if total else 0
    color = "#10b981" if remaining > 180 else "#f59e0b" if remaining > 60 else "#ef4444"
    return f"""
<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:0.75rem 1rem;margin-bottom:1rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
    <span style="font-weight:700;color:#334155;">⏱️ Unit Test — 25 min limit</span>
    <span id="hm10-ut-clock" style="font-size:1.35rem;font-weight:700;color:{color};">{mins:02d}:{secs:02d}</span>
  </div>
  <div style="background:#e2e8f0;border-radius:6px;height:8px;margin-top:0.5rem;overflow:hidden;">
    <div style="background:{color};width:{pct}%;height:100%;transition:width 0.3s;"></div>
  </div>
</div>
<script>
(function() {{
  var rem = {remaining};
  var el = document.getElementById('hm10-ut-clock');
  if (!el) return;
  var t = setInterval(function() {{
    rem -= 1;
    if (rem < 0) {{ clearInterval(t); return; }}
    var m = Math.floor(rem / 60), s = rem % 60;
    el.textContent = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
  }}, 1000);
}})();
</script>
"""


def render_unit_test_home(unit_id: int) -> None:
    unit = h10u.get_unit(unit_id)
    if not unit:
        st.error("Unit not found.")
        return

    if not h10ut.unit_test_available(unit_id):
        st.info("Unit Test (board format) is coming soon for this chapter.")
        return

    st.markdown("### Unit Test — Practice 2")
    st.markdown(
        '<p style="color:#64748b;margin-bottom:0.75rem;">'
        "Timed **25-minute** paper in CBSE board format — all questions from this unit only.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<pre style="background:#f1f5f9;padding:0.85rem 1rem;border-radius:8px;font-size:0.88rem;">'
        f"{h10ut.blueprint_summary()}</pre>",
        unsafe_allow_html=True,
    )
    st.caption(h10ut.seed_source_line(unit_id))
    st.caption(
        "This is a **timed test**. Answers are not shown while you work. "
        "Write Sections B–D on paper, upload **one photo of the whole paper**, then submit. "
        "The examiner marks written work from that photo using the CBSE step-marking scheme."
    )

    if st.button("Start unit test", key=f"hm10_ut_start_{unit_id}", type="primary", use_container_width=True):
        questions, err = h10ut.build_unit_test(unit_id)
        if err or not questions:
            st.warning(err or "Could not build unit test.")
            return
        session_id = h10utu.new_session_id(unit_id)
        st.session_state[_ss_key(unit_id, "questions")] = questions
        st.session_state[_ss_key(unit_id, "responses")] = [{} for _ in questions]
        st.session_state[_ss_key(unit_id, "current")] = 0
        st.session_state[_ss_key(unit_id, "start_time")] = time.time()
        st.session_state[_ss_key(unit_id, "session_id")] = session_id
        st.session_state[_ss_key(unit_id, "work_images")] = []
        st.session_state[_ss_key(unit_id, "finished")] = False
        st.session_state[_ss_key(unit_id, "review_mode")] = False
        st.session_state.pop(_ss_key(unit_id, "ai_graded_for"), None)
        st.session_state.pop(_ss_key(unit_id, "ai_grade_error"), None)
        st.session_state.hm10_unit_id = unit_id
        st.session_state.current_page = "harshit_class10_unit_test"
        st.rerun()


def _render_section_header(q: dict, prev_section: str | None) -> str | None:
    section = q.get("section", "")
    if section != prev_section:
        st.markdown(
            f'<h4 style="color:#6366f1;margin:1.25rem 0 0.5rem 0;">{q.get("section_label", f"Section {section}")}</h4>',
            unsafe_allow_html=True,
        )
    return section


def _render_mcq_or_ar(q: dict, unit_id: int, idx: int, resp: dict, *, disabled: bool) -> None:
    if q.get("type") == "assertion_reason":
        st.markdown(
            f'<p style="font-weight:600;margin-bottom:0.35rem;">Assertion (A):</p>'
            f'<p style="margin-left:0.5rem;">{hmr.format_math_display(q["assertion"])}</p>'
            f'<p style="font-weight:600;margin:0.75rem 0 0.35rem 0;">Reason (R):</p>'
            f'<p style="margin-left:0.5rem;margin-bottom:0.75rem;">{hmr.format_math_display(q["reason"])}</p>',
            unsafe_allow_html=True,
        )
    else:
        hmr.render_question(q["question"])

    current = resp.get("picked_index")
    opts = q.get("options", [])
    for i, opt in enumerate(opts):
        letter = chr(65 + i)
        label = f"{letter}. {hmr.format_math_display(str(opt))}"
        if st.button(
            label,
            key=f"hm10_ut_pick_{unit_id}_{idx}_{i}",
            use_container_width=True,
            disabled=disabled,
            type="primary" if current == i else "secondary",
        ):
            responses = _ensure_responses(unit_id, len(st.session_state[_ss_key(unit_id, "questions")]))
            responses[idx] = {**resp, "picked_index": i}
            st.session_state[_ss_key(unit_id, "responses")] = responses
            st.rerun()

    if current is not None and not disabled:
        letter = chr(65 + int(current))
        st.caption(f"Answer recorded: {letter}. You can change it until you submit.")


def _session_work_images(unit_id: int) -> list[dict]:
    return list(st.session_state.get(_ss_key(unit_id, "work_images")) or [])


def _try_finish_test(unit_id: int, questions: list[dict]) -> bool:
    images = _session_work_images(unit_id)
    if h10utu.test_requires_work_photo(questions) and not h10utu.has_session_work_upload(images):
        st.warning("Upload and save one photo of your written paper first.")
        return False
    if images:
        responses = _ensure_responses(unit_id, len(questions))
        for i, q in enumerate(questions):
            if q.get("type") == "written":
                responses[i] = {**responses[i], "work_images": images}
        st.session_state[_ss_key(unit_id, "responses")] = responses
    st.session_state[_ss_key(unit_id, "finished")] = True
    return True


def _render_session_work_upload(unit_id: int, questions: list[dict], *, disabled: bool) -> None:
    if not h10utu.test_requires_work_photo(questions):
        return

    images = _session_work_images(unit_id)
    st.markdown("##### 📷 Written paper (one photo for the whole test)")
    st.caption(h10utu.work_upload_label())

    if images:
        st.success("Paper photo saved for this test.")
        for meta in images:
            path = meta.get("path")
            if path and Path(path).is_file():
                st.image(path, caption=meta.get("filename", "Written paper"), use_container_width=True)

    if disabled:
        return

    uploaded = st.file_uploader(
        "Add one photo of your written paper (JPG or PNG)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False,
        key=f"hm10_ut_upload_paper_{unit_id}",
        help="On a phone: tap to take a picture or choose from gallery. 8 MB max.",
    )

    save_label = "Replace paper photo" if images else "Save paper photo"
    if uploaded and st.button(save_label, key=f"hm10_ut_save_paper_{unit_id}", type="primary"):
        session_id = st.session_state.get(_ss_key(unit_id, "session_id"), h10utu.new_session_id(unit_id))
        student = str(st.session_state.get("selected_user") or "Student")
        merged, err = h10utu.save_session_work_images(
            session_id=session_id,
            student_name=student,
            unit_id=unit_id,
            uploaded_files=uploaded,
            existing=images,
        )
        st.session_state[_ss_key(unit_id, "work_images")] = merged
        if err:
            st.warning(err)
        st.rerun()

    if not h10utu.has_session_work_upload(images):
        st.caption("Save one paper photo before you submit. Written answers are marked after submit.")


def _render_written(q: dict, unit_id: int, idx: int, resp: dict, *, disabled: bool) -> None:
    del unit_id, idx, resp, disabled
    hmr.render_question(q["question"])
    marks = int(q.get("marks", 0))
    if marks >= 5:
        st.caption(f"({marks} marks — write the full solution and diagrams on paper. No answers are shown during the test.)")
    else:
        st.caption(f"({marks} marks — write your working on paper. No answers are shown during the test.)")


def _question_complete(q: dict, resp: dict, *, paper_ready: bool = False) -> bool:
    if q.get("type") == "written":
        return paper_ready
    return resp.get("picked_index") is not None


def render_unit_test_session() -> None:
    hmc_ui.inject_harshit_styles()
    unit_id = int(st.session_state.get("hm10_unit_id", 1))
    unit = h10u.get_unit(unit_id)
    questions = st.session_state.get(_ss_key(unit_id, "questions"), [])
    if not questions:
        st.warning("No unit test loaded.")
        if st.button("← Back to unit", key=f"hm10_ut_empty_back_{unit_id}"):
            st.session_state.current_page = "harshit_class10_unit"
            st.rerun()
        return

    start = float(st.session_state.get(_ss_key(unit_id, "start_time"), time.time()))
    remaining = h10ut.remaining_seconds(start)
    time_up = remaining <= 0
    finished = bool(st.session_state.get(_ss_key(unit_id, "finished")))
    responses = _ensure_responses(unit_id, len(questions))

    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("← Exit test", key=f"hm10_ut_back_{unit_id}"):
            st.session_state.current_page = "harshit_class10_unit"
            for key in (
                "questions",
                "responses",
                "current",
                "start_time",
                "finished",
                "review_mode",
                "session_id",
                "work_images",
                "ai_graded_for",
                "ai_grade_error",
            ):
                st.session_state.pop(_ss_key(unit_id, key), None)
            st.rerun()

    title = unit["title"] if unit else f"Unit {unit_id}"
    st.markdown(f'<p class="hm-prompt" style="text-align:center;">Unit Test · {title}</p>', unsafe_allow_html=True)

    if finished:
        _render_results(unit_id, questions, responses, start)
        return

    components.html(_timer_html(remaining, h10ut.UNIT_TEST_DURATION_SEC), height=90)

    if time_up:
        st.warning("Time is up! Submit your test to see results.")
        _render_session_work_upload(unit_id, questions, disabled=False)
        if st.button("Submit test", key=f"hm10_ut_submit_{unit_id}", type="primary", use_container_width=True):
            if _try_finish_test(unit_id, questions):
                st.rerun()
        return

    current = int(st.session_state.get(_ss_key(unit_id, "current"), 0))
    current = max(0, min(current, len(questions) - 1))
    st.session_state[_ss_key(unit_id, "current")] = current

    paper_ready = h10utu.has_session_work_upload(_session_work_images(unit_id))
    answered = sum(
        1 for q, r in zip(questions, responses) if _question_complete(q, r, paper_ready=paper_ready)
    )
    st.caption(f"Question {current + 1} of {len(questions)} · {answered}/{len(questions)} attempted · 15 marks total")

    prev_section: str | None = None
    q = questions[current]
    resp = responses[current]
    prev_section = _render_section_header(q, prev_section)

    st.markdown(
        f'<p style="font-weight:700;color:#1e293b;margin-bottom:0.5rem;">'
        f"Q{q.get('q_num', current + 1)} · {q.get('marks', 1)} mark{'s' if q.get('marks', 1) != 1 else ''}"
        f"{' · ' + str(q.get('source', '')) if q.get('source') else ''}</p>",
        unsafe_allow_html=True,
    )

    if q.get("type") == "written":
        _render_written(q, unit_id, current, resp, disabled=False)
    else:
        _render_mcq_or_ar(q, unit_id, current, resp, disabled=False)

    st.markdown("---")
    nav1, nav2, nav3 = st.columns([1, 2, 1])
    with nav1:
        if current > 0 and st.button("← Previous", key=f"hm10_ut_prev_{unit_id}", use_container_width=True):
            st.session_state[_ss_key(unit_id, "current")] = current - 1
            st.rerun()
    with nav3:
        if current < len(questions) - 1 and st.button("Next →", key=f"hm10_ut_next_{unit_id}", use_container_width=True):
            st.session_state[_ss_key(unit_id, "current")] = current + 1
            st.rerun()

    _render_session_work_upload(unit_id, questions, disabled=False)

    all_done = all(
        _question_complete(q, r, paper_ready=paper_ready) for q, r in zip(questions, responses)
    )
    submit_label = "Submit test early" if not all_done else "Submit test"
    if st.button(submit_label, key=f"hm10_ut_finish_{unit_id}", type="primary", use_container_width=True):
        if _try_finish_test(unit_id, questions):
            st.rerun()


def _ensure_written_graded(unit_id: int, questions: list[dict], responses: list[dict]) -> list[dict]:
    written = [q for q in questions if q.get("type") == "written"]
    session_id = st.session_state.get(_ss_key(unit_id, "session_id"))
    if not written or not session_id:
        return responses
    if st.session_state.get(_ss_key(unit_id, "ai_graded_for")) == session_id:
        return responses

    paths = [str(m.get("path")) for m in _session_work_images(unit_id) if m.get("path")]
    with st.spinner("Examiner is marking your written paper (CBSE step marks)…"):
        grades, err = h10g.grade_written_paper(
            written_questions=written,
            image_paths=paths,
            api_key=str(_xai_api_key() or ""),
        )
    if err:
        st.session_state[_ss_key(unit_id, "ai_grade_error")] = err
        st.warning(err)
    responses = h10g.apply_grades_to_responses(questions, responses, grades)
    st.session_state[_ss_key(unit_id, "responses")] = responses
    st.session_state[_ss_key(unit_id, "ai_graded_for")] = session_id
    return responses


def _render_question_review(q: dict, resp: dict) -> None:
    q_num = q.get("q_num")
    marks = float(q.get("marks", 0))
    if q.get("type") in ("mcq", "assertion_reason"):
        opts = q.get("options") or []
        picked = resp.get("picked_index")
        correct_i = q.get("answer")
        picked_txt = opts[int(picked)] if picked is not None and 0 <= int(picked) < len(opts) else "Not attempted"
        correct_txt = opts[int(correct_i)] if correct_i is not None and 0 <= int(correct_i) < len(opts) else ""
        ok = picked is not None and hma.is_pick_correct(q, int(picked))
        st.markdown(f"**Q{q_num}** — {marks:g} mark · {'✅' if ok else '❌'}")
        if q.get("type") == "assertion_reason":
            st.caption(f"A: {q.get('assertion', '')}")
            st.caption(f"R: {q.get('reason', '')}")
        else:
            st.caption(hmr.format_math_display(str(q.get("question", ""))))
        st.markdown(f"Your answer: {hmr.format_math_display(str(picked_txt))}")
        if not ok:
            st.markdown(f"Correct: {hmr.format_math_display(str(correct_txt))}")
            if q.get("explanation"):
                st.caption(hmr.format_math_display(str(q["explanation"])))
        return

    grade = resp.get("ai_grade") or {}
    earned = float(grade.get("earned", h10ut.written_earned(q, resp)))
    st.markdown(f"**Q{q_num}** — {earned:g}/{marks:g} marks (examiner)")
    st.caption(hmr.format_math_display(str(q.get("question", ""))))
    for step in grade.get("steps") or []:
        st.markdown(
            f"- {step.get('awarded', 0):g}/{step.get('max', 0):g} — {step.get('text', '')}"
            + (f" · {step['note']}" if step.get("note") else "")
        )
    if grade.get("feedback"):
        st.markdown(f"**Feedback:** {grade['feedback']}")
    if grade.get("corrections"):
        st.markdown(f"**Correction:** {grade['corrections']}")
    if q.get("model_answer"):
        st.markdown(
            f'<div style="background:#eff6ff;border-left:4px solid #6366f1;padding:0.75rem 1rem;'
            f'border-radius:8px;margin:0.5rem 0;"><strong>Expected working:</strong><br>'
            f"{hmr.format_math_display(str(q.get('model_answer', '')))}</div>",
            unsafe_allow_html=True,
        )


def _render_results(unit_id: int, questions: list[dict], responses: list[dict], start: float) -> None:
    unit = h10u.get_unit(unit_id)
    title = unit["title"] if unit else f"Unit {unit_id}"
    name = st.session_state.get("selected_user") or "Student"
    user = db.get_user(name) if name else None
    responses = _ensure_written_graded(unit_id, questions, responses)

    base_report = h10ut.build_unit_test_report(questions, responses)
    report = h10ut.enrich_report_for_sync(
        base_report, questions, responses, student_name=name or "Student"
    )
    elapsed = int(time.time() - start)
    mins, secs = divmod(elapsed, 60)
    earned = report["earned"]
    max_marks = report["max_marks"]
    pct = report["score_pct"]
    session_id = st.session_state.get(_ss_key(unit_id, "session_id"))

    if pct >= 80:
        emoji, color, msg = "🏆", "#10b981", "Strong board-style performance!"
    elif pct >= 60:
        emoji, color, msg = "👍", "#3b82f6", "Good effort — review written steps."
    else:
        emoji, color, msg = "💪", "#f59e0b", "Keep practicing — focus on model answers."

    st.markdown(
        f"""
<div style="text-align:center;padding:2rem;background:{color}10;border-radius:16px;border:2px solid {color};">
  <div style="font-size:4rem;">{emoji}</div>
  <h2 style="color:{color};">{earned:g} / {max_marks:g} marks ({pct}%)</h2>
  <p>{msg}</p>
  <p style="color:#64748b;">Time used: {mins}m {secs}s · Limit 25m</p>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.session_state.get(_ss_key(unit_id, "ai_grade_error")):
        st.caption("Written marks could not be auto-awarded. Objective questions are still scored.")

    st.markdown("#### Question breakdown")
    for item in report["breakdown"]:
        line = (
            f"- **Q{item['q_num']}** (Section {item['section']}, {item['marks']} marks) — "
            f"**{item['earned']:g}/{item['marks']:g}**"
        )
        st.markdown(line)

    st.markdown("#### Review")
    for q, resp in zip(questions, responses):
        with st.expander(f"Q{q.get('q_num')} · Section {q.get('section')} · {q.get('marks')} marks", expanded=False):
            _render_question_review(q, resp)

    paper_photos = _session_work_images(unit_id)
    if paper_photos:
        st.caption("Written paper photo uploaded for this test.")
        with st.expander("📷 Submitted written paper", expanded=False):
            for meta in paper_photos:
                path = meta.get("path")
                if path and Path(path).is_file():
                    st.image(path, caption=meta.get("filename"), use_container_width=True)

    if user and session_id and st.session_state.get(_ss_key(unit_id, "activity_saved_for")) != session_id:
        st.session_state[_ss_key(unit_id, "activity_saved_for")] = session_id
        db.save_activity_score(
            user["id"],
            "HarshitMath",
            f"Class X Unit {unit_id} Unit Test: {title[:36]}",
            int(round(float(earned))),
            int(max_marks),
            h10ut.format_unit_test_report_details(report),
            elapsed,
            flush_sheets=True,
        )

    if user and session_id and st.session_state.get(_ss_key(unit_id, "persist_saved_for")) != session_id:
        st.session_state[_ss_key(unit_id, "persist_saved_for")] = session_id
        sheet_unit_id = h10ut.UNIT_TEST_SHEET_UNIT_OFFSET + unit_id
        try:
            _, sheet_err = gss.persist_edgenuity_practice(
                user_name=name,
                user_id=user["id"],
                session_id=session_id,
                session_kind="harshit_class10_unit_test",
                unit_id=sheet_unit_id,
                unit_label=f"Class X Unit {unit_id}: {title} — Unit Test (25 min)",
                report=report,
                failed_questions=report.get("failed_questions") or [],
                time_spent_seconds=elapsed,
                question_ids=[str(q.get("id", "")) for q in questions],
            )
            if sheet_err:
                st.warning(f"Google Sheet sync note: {sheet_err}")
        except Exception as exc:
            st.warning(f"Google Sheet sync failed (saved locally): {exc}")

    if session_id and st.session_state.get(_ss_key(unit_id, "email_sent_for")) != session_id:
        st.session_state[_ss_key(unit_id, "email_sent_for")] = session_id
        if ec3mail.practice_email_enabled():
            mail_result = ec3mail.send_harshit_unit_test_report_email(
                student_name=name or "Student",
                unit_title=f"Class X Unit {unit_id}: {title}",
                report=report,
                time_spent_seconds=elapsed,
                session_meta={"unit_id": unit_id, "session_type": "unit_test", "session_id": session_id},
                questions=questions,
                answers=responses,
            )
            ec3mail.render_practice_email_result(mail_result)
        else:
            st.caption("Email not configured — unit test report saved on screen only.")

    if st.button("Take another unit test", key=f"hm10_ut_retry_{unit_id}", use_container_width=True):
        for key in (
            "questions",
            "responses",
            "current",
            "start_time",
            "finished",
            "review_mode",
            "session_id",
            "work_images",
            "persist_saved_for",
            "email_sent_for",
            "activity_saved_for",
            "ai_graded_for",
            "ai_grade_error",
        ):
            st.session_state.pop(_ss_key(unit_id, key), None)
        st.session_state.current_page = "harshit_class10_unit"
        st.session_state[f"hm10_unit_section_{unit_id}"] = "📝 Unit Test"
        st.rerun()

    if st.button("← Back to unit", key=f"hm10_ut_done_back_{unit_id}", use_container_width=True):
        for key in (
            "questions",
            "responses",
            "current",
            "start_time",
            "finished",
            "review_mode",
            "session_id",
            "work_images",
            "persist_saved_for",
            "email_sent_for",
            "activity_saved_for",
            "ai_graded_for",
            "ai_grade_error",
        ):
            st.session_state.pop(_ss_key(unit_id, key), None)
        st.session_state.current_page = "harshit_class10_unit"
        st.rerun()
