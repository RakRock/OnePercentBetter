"""Streamlit UI for Arjun's daily Spanish practice."""

from __future__ import annotations

import html
import random
import time

import streamlit as st

import database as db
from arjun_spanish import content as es
from arjun_spanish import practice as esp

PRIMARY = "#c2410c"
GOLD = "#d97706"
MODES = (
    ("flash", "🃏 Flash cards"),
    ("quiz", "✅ Quiz"),
    ("type", "⌨️ Type it"),
    ("match", "🔗 Match"),
)

_SESSION_KEYS = (
    "es_topic",
    "es_mode",
    "es_cards",
    "es_index",
    "es_flipped",
    "es_known",
    "es_learning",
    "es_questions",
    "es_feedback",
    "es_choice",
    "es_score",
    "es_total",
    "es_start_time",
    "es_saved",
    "es_match",
    "es_pick_left",
    "es_pick_right",
    "es_matched",
    "es_match_misses",
    "es_type_checked",
)


def _esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def _back_dashboard() -> None:
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_activity = None


def _back_home() -> None:
    st.session_state.current_page = "arjun_spanish_home"
    _clear_round()


def _clear_round() -> None:
    for key in _SESSION_KEYS:
        if key in st.session_state:
            del st.session_state[key]


def _topic_meta(topic_id: str) -> dict:
    try:
        return es.topic_by_id(topic_id)
    except KeyError:
        return dict(es.DAILY_TOPIC)


def _start(topic_id: str, mode: str) -> None:
    rng = random.Random()
    pool = es.cards_for_topic(topic_id)
    if mode == "flash":
        count = es.FLASH_SIZE if topic_id == "daily" else min(len(pool), 16)
        cards = esp.pick_cards(topic_id, count, rng)
    elif mode == "quiz":
        cards = esp.pick_cards(topic_id, es.QUIZ_SIZE, rng)
        direction = rng.choice(("es_en", "en_es"))
        st.session_state.es_questions = esp.make_mc_questions(cards, direction=direction, rng=rng)
    elif mode == "type":
        cards = esp.pick_cards(topic_id, es.TYPE_SIZE, rng)
        st.session_state.es_questions = esp.make_type_questions(cards, rng)
    else:
        cards = esp.pick_cards(topic_id, max(es.MATCH_PAIRS, 6), rng)
        st.session_state.es_match = esp.make_match_round(cards, es.MATCH_PAIRS, rng)
        st.session_state.es_matched = []
        st.session_state.es_pick_left = None
        st.session_state.es_pick_right = None
        st.session_state.es_match_misses = 0

    st.session_state.es_topic = topic_id
    st.session_state.es_mode = mode
    st.session_state.es_cards = cards
    st.session_state.es_index = 0
    st.session_state.es_flipped = False
    st.session_state.es_known = []
    st.session_state.es_learning = []
    st.session_state.es_feedback = None
    st.session_state.es_choice = None
    st.session_state.es_score = 0
    st.session_state.es_total = 0
    st.session_state.es_start_time = time.time()
    st.session_state.es_saved = False
    st.session_state.es_type_checked = False
    st.session_state.current_page = "arjun_spanish_practice"


def _save_score(activity_name: str, score: int, max_score: int, details: str) -> None:
    if st.session_state.get("es_saved"):
        return
    name = st.session_state.get("selected_user")
    user = db.get_user(name) if name else None
    if not user or max_score <= 0:
        st.session_state.es_saved = True
        return
    spent = int(time.time() - (st.session_state.get("es_start_time") or time.time()))
    db.save_activity_score(
        user["id"],
        "Spanish",
        activity_name,
        int(round(100 * score / max_score)),
        100,
        details,
        spent,
    )
    st.session_state.es_saved = True


def render_home() -> None:
    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav, _ = st.columns([1, 6])
    with col_nav:
        if st.button("← Back", key="es_back_dash"):
            _back_dashboard()
            st.rerun()

    st.markdown(
        f"""
        <div style="text-align:center;padding:0.4rem 0 0.8rem 0;">
            <h1 style="font-size:2.5rem;margin:0;">🇪🇸 { _esc(name) }'s Spanish</h1>
            <p style="color:#6b7280;font-size:1.1rem;margin:0.4rem 0 0 0;">
                Practice a little every day — greetings, class words, and new vocabulary.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    today = db.get_today_scores(user["id"], activity_type="Spanish") if user else []
    history = db.get_scores_history(user["id"], activity_type="Spanish", days=365) if user else []
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">📅 {len(today)}</div>'
            f'<div class="score-label">Rounds today</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        if today:
            best = max(s["score"] for s in today)
            st.markdown(
                f'<div class="score-card"><div class="score-number">🎯 {best}%</div>'
                f'<div class="score-label">Today\'s best</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="score-card"><div class="score-number">🎯 —</div>'
                '<div class="score-label">Today\'s best</div></div>',
                unsafe_allow_html=True,
            )
    with col3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {len(history)}</div>'
            f'<div class="score-label">All-time rounds</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,{PRIMARY},{GOLD});border-radius:20px;
             padding:1.2rem 1.4rem;color:white;margin-bottom:0.6rem;">
            <div style="font-size:2rem;">🔥 Daily mix</div>
            <div style="opacity:0.95;margin-top:0.25rem;">
                {es.FLASH_SIZE} cards from the whole bank · {es.total_cards()} words ready
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    m1, m2, m3, m4 = st.columns(4)
    for col, (mode, label) in zip((m1, m2, m3, m4), MODES):
        with col:
            if st.button(label, key=f"es_daily_{mode}", width="stretch", type="primary"):
                _start("daily", mode)
                st.rerun()

    st.markdown("")
    st.markdown("### School packet")
    st.caption("From Arjun's first Spanish homework — *Para empezar / En la escuela*.")
    _topic_grid([t for t in es.TOPICS if t["source"] == "school"])

    st.markdown("### Extra vocabulary")
    st.caption("New words to grow beyond the first packet.")
    _topic_grid([t for t in es.TOPICS if t["source"] == "extra"])

    with st.expander("🔊 Pronunciation cheat sheet"):
        st.markdown(
            """
- **Vowels:** a *ah* · e *eh* · i *ee* · o *oh* · u *oo*
- **h** is silent: *hola* sounds like *ola*
- **j** and **g** (before e/i) are a scratchy *h*: *jueves*, *gente*
- **ñ** is *ny*: *mañana* → *ma-NYA-na*
- **ll** is like *y*: *me llamo* → *me YA-mo*
- **rr** is a rolled r: *perro*
- **c** is *s* before e/i (*cinco*), and *k* before a/o/u (*casa*)
- Formal **usted (Ud.)** with adults; informal **tú** with friends
            """
        )


def _topic_grid(topics: list[dict]) -> None:
    for i in range(0, len(topics), 3):
        cols = st.columns(3, gap="large")
        for col, topic in zip(cols, topics[i : i + 3]):
            with col:
                n = len(es.cards_for_topic(topic["id"]))
                st.markdown(
                    f"""
                    <div class="score-card" style="border-top:5px solid {_esc(topic['color'])};">
                        <div style="font-size:2.4rem;">{_esc(topic['emoji'])}</div>
                        <h3 style="margin:0.4rem 0 0.2rem 0;">{_esc(topic['title'])}</h3>
                        <p style="color:#6b7280;margin:0;">{_esc(topic['subtitle'])}</p>
                        <p style="color:#9ca3af;margin:0.35rem 0 0 0;font-size:0.85rem;">{n} words</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Practice", key=f"es_topic_{topic['id']}", width="stretch"):
                    _start(topic["id"], "flash")
                    st.rerun()


def render_practice() -> None:
    topic_id = st.session_state.get("es_topic") or "daily"
    mode = st.session_state.get("es_mode") or "flash"
    topic = _topic_meta(topic_id)

    nav, mid, _ = st.columns([1, 4, 1])
    with nav:
        if st.button("← Spanish home", key="es_back_home"):
            _back_home()
            st.rerun()
    with mid:
        st.markdown(
            f"<div style='padding-top:0.35rem;color:#6b7280;'>"
            f"{_esc(topic['emoji'])} <b>{_esc(topic['title'])}</b></div>",
            unsafe_allow_html=True,
        )

    mode_cols = st.columns(len(MODES))
    for col, (mode_id, label) in zip(mode_cols, MODES):
        with col:
            is_on = mode_id == mode
            if st.button(label, key=f"es_switch_{mode_id}", width="stretch", type="primary" if is_on else "secondary"):
                if mode_id != mode:
                    _start(topic_id, mode_id)
                    st.rerun()

    if mode == "flash":
        _render_flash()
    elif mode == "quiz":
        _render_quiz()
    elif mode == "type":
        _render_type()
    else:
        _render_match()


def _progress_label(current: int, total: int) -> None:
    st.progress(min(1.0, current / total) if total else 0)
    st.caption(f"Card {min(current, total)} of {total}")


def _done_box(title: str, body: str, score: int, total: int) -> None:
    pct = int(round(100 * score / total)) if total else 0
    st.markdown(
        f"""
        <div style="text-align:center;padding:1.6rem;background:#fff7ed;
             border-radius:20px;border:3px solid {PRIMARY};margin-top:0.8rem;">
            <div style="font-size:4rem;">🌟</div>
            <h2 style="color:{PRIMARY};margin:0.4rem 0;">{_esc(title)}</h2>
            <p style="font-size:1.2rem;color:#4b5563;">{_esc(body)}</p>
            <p style="font-size:1.6rem;font-weight:800;color:{GOLD};">{pct}%</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔁 Play again", key="es_again", width="stretch", type="primary"):
            _start(st.session_state.es_topic, st.session_state.es_mode)
            st.rerun()
    with c2:
        if st.button("🏠 Spanish home", key="es_done_home", width="stretch"):
            _back_home()
            st.rerun()


def _render_flash() -> None:
    cards = st.session_state.get("es_cards") or []
    index = int(st.session_state.get("es_index") or 0)
    if index >= len(cards):
        known = len(st.session_state.get("es_known") or [])
        learning = st.session_state.get("es_learning") or []
        topic = _topic_meta(st.session_state.es_topic)
        _save_score(
            f"{topic['title']} flash cards",
            known,
            len(cards) or 1,
            f"{known}/{len(cards)} known",
        )
        extra = ""
        if learning:
            extra = " Keep practicing the ones you marked."
        _done_box("¡Muy bien!", f"You knew {known} of {len(cards)} cards.{extra}", known, len(cards))
        if learning:
            st.markdown("#### Still learning")
            for card_id in learning:
                card = es.get_card(card_id)
                st.markdown(f"- {card['emoji']} **{card['spanish']}** — {card['english']}")
        return

    card = cards[index]
    flipped = bool(st.session_state.get("es_flipped"))
    _progress_label(index + 1, len(cards))
    face = card["english"] if flipped else card["spanish"]
    label = "English" if flipped else "Spanish"
    border = GOLD if flipped else PRIMARY
    hint = card.get("hint") or ""
    st.markdown(
        f"""
        <div style="min-height:250px;background:linear-gradient(160deg,#fff7ed,#ffedd5);
             border:4px solid {border};border-radius:24px;padding:1.6rem 1.2rem;
             display:flex;flex-direction:column;align-items:center;justify-content:center;
             text-align:center;box-shadow:0 10px 24px rgba(194,65,12,0.12);">
            <div style="font-size:2.6rem;">{_esc(card.get('emoji'))}</div>
            <div style="color:#9a3412;font-size:0.85rem;letter-spacing:0.08em;text-transform:uppercase;margin-top:0.3rem;">
                {label}
            </div>
            <div style="font-size:2.1rem;font-weight:800;color:#1f2937;margin-top:0.45rem;">
                {_esc(face)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if flipped and hint:
        st.info(f"💡 {hint}")
    elif not flipped:
        st.caption("Tap flip, then say the English out loud before you peek.")

    if st.button("🔄 Flip card", key=f"es_flip_{index}", width="stretch", type="primary"):
        st.session_state.es_flipped = not flipped
        st.rerun()

    if flipped:
        k1, k2 = st.columns(2)
        with k1:
            if st.button("✅ I know it", key=f"es_know_{index}", width="stretch"):
                st.session_state.es_known = list(st.session_state.get("es_known") or []) + [card["id"]]
                st.session_state.es_index = index + 1
                st.session_state.es_flipped = False
                st.rerun()
        with k2:
            if st.button("🔁 Still learning", key=f"es_learn_{index}", width="stretch"):
                st.session_state.es_learning = list(st.session_state.get("es_learning") or []) + [card["id"]]
                st.session_state.es_index = index + 1
                st.session_state.es_flipped = False
                st.rerun()


def _render_quiz() -> None:
    questions = st.session_state.get("es_questions") or []
    index = int(st.session_state.get("es_index") or 0)
    if not questions:
        st.warning("Not enough words for a quiz in this topic yet.")
        return
    if index >= len(questions):
        score = int(st.session_state.get("es_score") or 0)
        topic = _topic_meta(st.session_state.es_topic)
        _save_score(f"{topic['title']} quiz", score, len(questions), f"{score}/{len(questions)} correct")
        _done_box("Quiz complete!", f"You got {score} of {len(questions)} right.", score, len(questions))
        return

    q = questions[index]
    _progress_label(index + 1, len(questions))
    direction = "Spanish → English" if q["direction"] == "es_en" else "English → Spanish"
    st.markdown(
        f"""
        <div style="text-align:center;padding:1rem 0 0.4rem 0;">
            <div style="color:#9a3412;font-size:0.85rem;letter-spacing:0.08em;text-transform:uppercase;">
                {_esc(direction)}
            </div>
            <div style="font-size:2.2rem;font-weight:800;margin-top:0.3rem;">
                {_esc(q.get('emoji'))} {_esc(q['prompt'])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    feedback = st.session_state.get("es_feedback")
    if feedback is None:
        for i, option in enumerate(q["options"]):
            if st.button(option, key=f"es_opt_{index}_{i}", width="stretch"):
                correct = option == q["answer"]
                st.session_state.es_choice = option
                st.session_state.es_feedback = "ok" if correct else "no"
                if correct:
                    st.session_state.es_score = int(st.session_state.get("es_score") or 0) + 1
                st.rerun()
        return

    if feedback == "ok":
        st.success(f"¡Correcto! {q['answer']}")
    else:
        st.error(f"Almost — the answer is **{q['answer']}**")
    if q.get("hint"):
        st.caption(f"💡 {q['hint']}")
    if st.button("Next →", key=f"es_quiz_next_{index}", width="stretch", type="primary"):
        st.session_state.es_index = index + 1
        st.session_state.es_feedback = None
        st.session_state.es_choice = None
        st.rerun()


def _render_type() -> None:
    questions = st.session_state.get("es_questions") or []
    index = int(st.session_state.get("es_index") or 0)
    if index >= len(questions):
        score = int(st.session_state.get("es_score") or 0)
        topic = _topic_meta(st.session_state.es_topic)
        _save_score(f"{topic['title']} type-it", score, len(questions), f"{score}/{len(questions)} typed")
        _done_box("Nice typing!", f"You spelled {score} of {len(questions)} correctly.", score, len(questions))
        return

    q = questions[index]
    card = es.get_card(q["card_id"])
    _progress_label(index + 1, len(questions))
    st.markdown(
        f"""
        <div style="text-align:center;padding:0.8rem 0;">
            <div style="font-size:2.4rem;">{_esc(q.get('emoji'))}</div>
            <div style="color:#6b7280;">Type the Spanish for</div>
            <div style="font-size:2rem;font-weight:800;">{_esc(q['prompt'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    typed = st.text_input(
        "Spanish",
        key=f"es_type_in_{index}",
        max_chars=esp.MAX_TYPED_LEN,
        placeholder="escribe aquí…",
        label_visibility="collapsed",
    )
    if not st.session_state.get("es_type_checked"):
        if st.button("Check", key=f"es_type_check_{index}", width="stretch", type="primary"):
            ok = esp.typed_matches(typed, card)
            st.session_state.es_type_checked = True
            st.session_state.es_feedback = "ok" if ok else "no"
            if ok:
                st.session_state.es_score = int(st.session_state.get("es_score") or 0) + 1
            st.rerun()
        return

    if st.session_state.get("es_feedback") == "ok":
        st.success(f"¡Exacto! **{card['spanish']}**")
    else:
        st.error(f"Close! It's **{card['spanish']}**")
    if card.get("hint"):
        st.caption(f"💡 {card['hint']}")
    if st.button("Next →", key=f"es_type_next_{index}", width="stretch", type="primary"):
        st.session_state.es_index = index + 1
        st.session_state.es_type_checked = False
        st.session_state.es_feedback = None
        st.rerun()


def _render_match() -> None:
    match = st.session_state.get("es_match")
    if not match:
        st.warning("Could not build a match round.")
        return
    matched = set(st.session_state.get("es_matched") or [])
    if len(matched) >= match["pairs"]:
        misses = int(st.session_state.get("es_match_misses") or 0)
        score = match["pairs"]
        topic = _topic_meta(st.session_state.es_topic)
        _save_score(
            f"{topic['title']} match",
            score,
            score + misses,
            f"{score} pairs, {misses} misses",
        )
        _done_box("All matched!", f"{score} pairs found · {misses} misses", score, score + misses)
        return

    st.caption("Tap a Spanish word, then its English meaning.")
    pick_left = st.session_state.get("es_pick_left")
    pick_right = st.session_state.get("es_pick_right")
    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown("**Español**")
        for item in match["left"]:
            done = item["id"] in matched
            selected = item["id"] == pick_left
            label = f"{item['emoji']} {item['text']}" if item.get("emoji") else item["text"]
            if done:
                st.button(f"✅ {label}", key=f"es_ml_{item['id']}", width="stretch", disabled=True)
            elif st.button(("👉 " if selected else "") + label, key=f"es_ml_{item['id']}", width="stretch"):
                st.session_state.es_pick_left = item["id"]
                _try_resolve_match()
                st.rerun()
    with right_col:
        st.markdown("**English**")
        for item in match["right"]:
            done = item["id"] in matched
            selected = item["id"] == pick_right
            if done:
                st.button(f"✅ {item['text']}", key=f"es_mr_{item['id']}", width="stretch", disabled=True)
            elif st.button(("👉 " if selected else "") + item["text"], key=f"es_mr_{item['id']}", width="stretch"):
                st.session_state.es_pick_right = item["id"]
                _try_resolve_match()
                st.rerun()

    if st.session_state.get("es_feedback") == "no":
        st.warning("Not a match — try another pair.")
    elif st.session_state.get("es_feedback") == "ok":
        st.success("¡Sí! Matched.")


def _try_resolve_match() -> None:
    left = st.session_state.get("es_pick_left")
    right = st.session_state.get("es_pick_right")
    if not left or not right:
        return
    if left == right:
        matched = list(st.session_state.get("es_matched") or [])
        if left not in matched:
            matched.append(left)
        st.session_state.es_matched = matched
        st.session_state.es_feedback = "ok"
    else:
        st.session_state.es_match_misses = int(st.session_state.get("es_match_misses") or 0) + 1
        st.session_state.es_feedback = "no"
    st.session_state.es_pick_left = None
    st.session_state.es_pick_right = None
