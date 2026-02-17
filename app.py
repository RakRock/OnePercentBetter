"""
1% Better Every Day - Main Application
A daily improvement tracker for kids and adults.
"""

import os
import streamlit as st
import database as db
from datetime import datetime
import plotly.graph_objects as go
import time
import reading_content as rc

# ── Optional imports for story generation (only when HF_TOKEN is set) ──
_HF_TOKEN = os.environ.get("HF_TOKEN")
_CAN_GENERATE = bool(_HF_TOKEN)

# ──────────────────────────────────────────────
# App Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="1% Better Every Day",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize database
db.init_db()

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }

    /* Hero title */
    .hero-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }

    /* User card styling */
    .user-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 3px solid transparent;
        min-height: 220px;
    }
    .user-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    .user-emoji { font-size: 4rem; display: block; margin-bottom: 0.5rem; }
    .user-name { font-size: 1.5rem; font-weight: 700; color: #1f2937; }

    /* Streak badge */
    .streak-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Score card */
    .score-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
    }
    .score-number { font-size: 2.5rem; font-weight: 800; color: #667eea; }
    .score-label { font-size: 0.9rem; color: #6b7280; font-weight: 500; }

    /* Button styles */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.5rem 2rem;
    }

    /* Divider */
    .fancy-divider {
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border: none;
        border-radius: 2px;
        margin: 1.5rem 0;
    }

    /* ─── Book covers on reading home ─── */
    .book-cover {
        border-radius: 18px;
        padding: 1.2rem 0.8rem;
        text-align: center;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.10);
        transition: transform 0.2s ease;
    }
    .book-cover:hover {
        transform: scale(1.04);
    }
    .book-emoji { font-size: 2.4rem; }
    .book-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: white;
        margin-top: 0.4rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    .book-pages {
        font-size: 0.8rem;
        color: rgba(255,255,255,0.85);
        margin-top: 0.2rem;
    }

    /* ─── Picture book page ─── */
    .story-page {
        background: #fffef5;
        border: 3px solid #e5e7eb;
        border-radius: 24px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin: 0.75rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .story-page img {
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        max-width: 512px;
        margin: 0 auto;
    }
    .story-page-text {
        font-size: 1.6rem;
        font-weight: 600;
        color: #1f2937;
        line-height: 1.5;
        font-family: 'Georgia', 'Times New Roman', serif;
    }
    .story-page-number {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 0.5rem;
    }

    /* ─── Quiz styling ─── */
    .quiz-question {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.3rem;
    }
    .correct-answer {
        background: #d1fae5;
        border: 3px solid #10b981;
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        font-size: 1.1rem;
    }
    .wrong-answer {
        background: #fee2e2;
        border: 3px solid #ef4444;
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Session State Initialization
# ──────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "selected_user" not in st.session_state:
    st.session_state.selected_user = None
if "selected_activity" not in st.session_state:
    st.session_state.selected_activity = None
if "reading_state" not in st.session_state:
    st.session_state.reading_state = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "reading_start_time" not in st.session_state:
    st.session_state.reading_start_time = None
if "story_page_idx" not in st.session_state:
    st.session_state.story_page_idx = 0
if "gen_status" not in st.session_state:
    st.session_state.gen_status = None  # None | "generating" | "done" | "error"
if "gen_error" not in st.session_state:
    st.session_state.gen_error = ""


# ──────────────────────────────────────────────
# Navigation helpers
# ──────────────────────────────────────────────
def go_home():
    st.session_state.current_page = "home"
    st.session_state.selected_user = None
    st.session_state.selected_activity = None
    st.session_state.reading_state = None
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.story_page_idx = 0


def select_user(name):
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_user = name
    st.session_state.selected_activity = None
    user = db.get_user(name)
    if user:
        db.record_daily_login(user["id"])


def select_activity(activity):
    st.session_state.selected_activity = activity
    if activity == "Reading":
        st.session_state.current_page = "reading_home"
    elif activity == "Math":
        st.session_state.current_page = "math_home"


def start_story(story_id):
    st.session_state.reading_state = story_id
    st.session_state.current_page = "reading_story"
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.reading_start_time = time.time()
    st.session_state.story_page_idx = 0


def back_to_reading_home():
    st.session_state.current_page = "reading_home"
    st.session_state.reading_state = None
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.story_page_idx = 0


def go_to_generate():
    st.session_state.current_page = "generate_story"
    st.session_state.gen_status = None
    st.session_state.gen_error = ""


# ──────────────────────────────────────────────
# PAGE: Home (User Selection)
# ──────────────────────────────────────────────
def render_home():
    st.markdown('<h1 class="hero-title">1% Better Every Day</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Small daily improvements lead to extraordinary results over time</p>', unsafe_allow_html=True)
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    st.markdown("### 👋 Who's practicing today?")
    st.markdown("")

    users = [
        ("Arjun", "🦁", "#ff6b6b", "The fearless learner"),
        ("Krish", "🚀", "#667eea", "Reaching for the stars"),
        ("Sangeetha", "🌸", "#f093fb", "Blooming with knowledge"),
        ("Rakesh", "⚡", "#ffd93d", "Lightning-fast thinker"),
    ]

    cols = st.columns(4, gap="large")
    for i, (name, emoji, color, tagline) in enumerate(users):
        with cols[i]:
            user_data = db.get_user(name)
            streak = db.get_login_streak(user_data["id"]) if user_data else 0
            total_days = db.get_total_login_days(user_data["id"]) if user_data else 0

            st.markdown(f"""
            <div class="user-card" style="border-color: {color}20; background: linear-gradient(135deg, {color}10, {color}25);">
                <span class="user-emoji">{emoji}</span>
                <div class="user-name">{name}</div>
                <div style="color: #6b7280; font-size: 0.85rem; margin: 0.3rem 0;">{tagline}</div>
                <div class="streak-badge">🔥 {streak} day streak</div>
                <div style="color: #9ca3af; font-size: 0.8rem; margin-top: 0.3rem;">{total_days} total days</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button(f"Start as {name}", key=f"btn_{name}", use_container_width=True, type="primary"):
                select_user(name)
                st.rerun()

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #9ca3af; padding: 1rem;">
        <em>"The compound effect is the principle of reaping huge rewards from a series of small, smart choices."</em>
        <br>— Darren Hardy
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE: User Dashboard
# ──────────────────────────────────────────────
def render_user_dashboard():
    name = st.session_state.selected_user
    user = db.get_user(name)
    if not user:
        st.error("User not found!")
        return

    streak = db.get_login_streak(user["id"])
    total_days = db.get_total_login_days(user["id"])
    today_scores = db.get_today_scores(user["id"])

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Home", key="back_home"):
            go_home()
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0;">
        <span style="font-size: 4rem;">{user['avatar_emoji']}</span>
        <h1 style="margin: 0.5rem 0 0.2rem 0;">{name}'s Dashboard</h1>
        <p style="color: #6b7280;">Keep going, you're doing amazing! 🎉</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="score-card"><div class="score-number">🔥 {streak}</div><div class="score-label">Day Streak</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="score-card"><div class="score-number">📅 {total_days}</div><div class="score-label">Total Days</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="score-card"><div class="score-number">✅ {len(today_scores)}</div><div class="score-label">Activities Today</div></div>', unsafe_allow_html=True)
    with col4:
        avg_display = f"{sum(s['score'] for s in today_scores) / len(today_scores):.0f}%" if today_scores else "—"
        st.markdown(f'<div class="score-card"><div class="score-number">⭐ {avg_display}</div><div class="score-label">Avg Score Today</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if name == "Krish":
        st.markdown("### 📚 Choose Your Activity")
        st.markdown("")

        act_col1, act_col2 = st.columns(2, gap="large")
        with act_col1:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #10b981;">
                <div style="font-size: 3rem;">📖</div>
                <h3 style="margin: 0.5rem 0;">Reading</h3>
                <p style="color: #6b7280;">Picture books & fun questions</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("📖 Start Reading", key="btn_reading", use_container_width=True, type="primary"):
                select_activity("Reading")
                st.rerun()

        with act_col2:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #667eea;">
                <div style="font-size: 3rem;">🧮</div>
                <h3 style="margin: 0.5rem 0;">Math</h3>
                <p style="color: #6b7280;">Math puzzles & practice</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🧮 Start Math", key="btn_math", use_container_width=True, type="primary"):
                st.info("🚧 Math module coming soon! Stay tuned.")
    else:
        st.markdown(f"### 🚧 {name}'s activities are coming soon!")
        st.info(f"We're building personalized activities for {name}. Check back soon!")

    # Progress chart
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 Progress Over Time")

    history = db.get_scores_history(user["id"], days=30)
    if history:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[h["log_date"] for h in history],
            y=[h["score"] for h in history],
            mode="lines+markers",
            marker=dict(size=10, color="#667eea"),
            line=dict(color="#667eea", width=3),
            text=[h["activity_name"] for h in history],
            hovertemplate="<b>%{text}</b><br>Score: %{y}%<br>Date: %{x}<extra></extra>",
        ))
        fig.update_layout(
            xaxis_title="Date", yaxis_title="Score (%)",
            yaxis=dict(range=[0, 105]), template="plotly_white",
            height=350, margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown('<div style="text-align:center;padding:2rem;color:#9ca3af;"><div style="font-size:3rem;">📈</div><p>Complete activities to see your progress chart!</p></div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE: Reading Home — Bookshelf
# ──────────────────────────────────────────────
def render_reading_home():
    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">📖 {name}'s Bookshelf</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Pick a book and start reading!</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    reading_history = []
    completed_ids = set()
    today_completed = set()
    if user:
        reading_history = db.get_reading_history(user["id"])
        completed_ids = {h["story_id"] for h in reading_history}
        today = datetime.now().strftime("%Y-%m-%d")
        today_completed = {h["story_id"] for h in reading_history if h["log_date"] == today}

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="score-card"><div class="score-number">📚 {len(completed_ids)}</div><div class="score-label">Stories Read</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="score-card"><div class="score-number">📅 {len(today_completed)}</div><div class="score-label">Read Today</div></div>', unsafe_allow_html=True)
    with col3:
        if reading_history:
            avg_pct = sum(h["questions_correct"] / max(h["questions_total"], 1) * 100 for h in reading_history) / len(reading_history)
            avg_display = f"{avg_pct:.0f}%"
        else:
            avg_display = "—"
        st.markdown(f'<div class="score-card"><div class="score-number">🎯 {avg_display}</div><div class="score-label">Avg Score</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Book covers grid (newest first)
    stories = rc.get_all_stories()[::-1]
    cols = st.columns(3, gap="medium")

    for j, story in enumerate(stories):
        with cols[j % 3]:
            done_today = story["id"] in today_completed
            is_done = story["id"] in completed_ids
            badge = "✅ Done today!" if done_today else ("⭐ Read before" if is_done else "✨ New!")
            color = story.get("color", "#667eea")

            st.markdown(f"""
            <div class="book-cover" style="background: linear-gradient(135deg, {color}, {color}cc);">
                <div class="book-emoji">{story['cover_emoji']}</div>
                <div class="book-title">{story['title']}</div>
                <div class="book-pages">{len(story['pages'])} pages · {len(story['questions'])} questions</div>
                <div style="margin-top:0.4rem;font-size:0.8rem;color:rgba(255,255,255,0.9);">{badge}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button(f"📖 Read: {story['title']}", key=f"story_{story['id']}", use_container_width=True, type="primary"):
                start_story(story["id"])
                st.rerun()
            st.markdown("")

    # "Create New Story" card (only shown when HF_TOKEN is available)
    if _CAN_GENERATE:
        next_col = len(stories) % 3
        with cols[next_col]:
            st.markdown("""
            <div class="book-cover" style="background: linear-gradient(135deg, #9ca3af, #6b7280); border: 2px dashed rgba(255,255,255,0.5);">
                <div class="book-emoji">✨</div>
                <div class="book-title">Create New Story</div>
                <div class="book-pages">AI-generated picture book</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("✨ Create New Story", key="btn_generate", use_container_width=True, type="secondary"):
                go_to_generate()
                st.rerun()
            st.markdown("")


# ──────────────────────────────────────────────
# PAGE: Reading a Picture Book + Quiz
# ──────────────────────────────────────────────
def render_reading_story():
    name = st.session_state.selected_user
    user = db.get_user(name)
    story_id = st.session_state.reading_state
    story = rc.get_story(story_id)

    if not story:
        st.error("Story not found!")
        return

    pages = story["pages"]
    total_pages = len(pages)
    page_idx = st.session_state.story_page_idx
    color = story.get("color", "#667eea")
    in_quiz = page_idx >= total_pages

    # Navigation bar
    col_nav1, col_nav_mid, col_nav2 = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← Books", key="back_stories"):
            back_to_reading_home()
            st.rerun()
    with col_nav_mid:
        if not in_quiz:
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                Page {page_idx + 1} of {total_pages}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                📝 Quiz Time!
            </div>
            """, unsafe_allow_html=True)

    # Book title
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: {color}; margin: 0.3rem 0; font-size: 2.2rem;">{story['cover_emoji']} {story['title']}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    if not in_quiz:
        progress = (page_idx + 1) / total_pages
    else:
        progress = 1.0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,{color},{color}bb);border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Show story pages ──
    if not in_quiz:
        pg = pages[page_idx]
        img_path = rc.get_image_path(story_id, page_idx + 1)

        st.markdown('<div class="story-page">', unsafe_allow_html=True)

        if os.path.exists(img_path):
            st.image(img_path, width=512)
        else:
            fallback = pg.get("fallback_emoji", "📖")
            st.markdown(f'<div style="font-size:5rem;text-align:center;">{fallback}</div>', unsafe_allow_html=True)

        st.markdown(f"""
            <div class="story-page-text">{pg['text']}</div>
            <div class="story-page-number">— page {page_idx + 1} —</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Page navigation buttons
        col_prev, col_mid, col_next = st.columns([1, 2, 1])
        with col_prev:
            if page_idx > 0:
                if st.button("⬅️ Back", key="prev_page", use_container_width=True):
                    st.session_state.story_page_idx -= 1
                    st.rerun()
        with col_next:
            if page_idx < total_pages - 1:
                if st.button("Next ➡️", key="next_page", use_container_width=True, type="primary"):
                    st.session_state.story_page_idx += 1
                    st.rerun()
            else:
                if st.button("📝 Take Quiz!", key="go_quiz", use_container_width=True, type="primary"):
                    st.session_state.story_page_idx = total_pages
                    st.rerun()

    # ── Quiz section ──
    else:
        questions = story["questions"]
        quiz_submitted = st.session_state.quiz_submitted

        st.markdown("""
        <div style="text-align:center; margin-bottom:1rem;">
            <span style="font-size:3rem;">🤔</span>
            <h3 style="margin:0.3rem 0;">Let's see what you remember!</h3>
        </div>
        """, unsafe_allow_html=True)

        for idx, q in enumerate(questions):
            key = f"q_{story_id}_{idx}"

            if quiz_submitted:
                user_ans = st.session_state.quiz_answers.get(key)
                correct_ans = q["answer"]
                is_correct = user_ans == correct_ans

                if is_correct:
                    st.markdown(f"""
                    <div class="correct-answer">
                        <strong style="font-size:1.2rem;">Q{idx+1}: {q['q']}</strong><br><br>
                        ✅ <strong>{q['options'][user_ans]}</strong> — Great job!
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    user_answer_text = q["options"][user_ans] if user_ans is not None else "No answer"
                    st.markdown(f"""
                    <div class="wrong-answer">
                        <strong style="font-size:1.2rem;">Q{idx+1}: {q['q']}</strong><br><br>
                        ❌ You said: <strong>{user_answer_text}</strong><br>
                        ✅ Answer: <strong>{q['options'][correct_ans]}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="quiz-question">Q{idx+1}: {q["q"]}</div>', unsafe_allow_html=True)
                answer = st.radio(
                    "Pick one:",
                    options=range(len(q["options"])),
                    format_func=lambda x, opts=q["options"]: opts[x],
                    key=key,
                    label_visibility="collapsed",
                )
                st.session_state.quiz_answers[key] = answer
                st.markdown("")

        st.markdown("")

        if not quiz_submitted:
            col_back, col_submit, _ = st.columns([1, 2, 1])
            with col_back:
                if st.button("⬅️ Re-read Story", key="back_to_pages", use_container_width=True):
                    st.session_state.story_page_idx = 0
                    st.rerun()
            with col_submit:
                if st.button("✅ Submit Answers!", key="submit_quiz", use_container_width=True, type="primary"):
                    st.session_state.quiz_submitted = True

                    correct = sum(
                        1 for i, q in enumerate(questions)
                        if st.session_state.quiz_answers.get(f"q_{story_id}_{i}") == q["answer"]
                    )
                    total = len(questions)
                    score_pct = int((correct / total) * 100) if total > 0 else 0
                    time_spent = int(time.time() - st.session_state.reading_start_time) if st.session_state.reading_start_time else 0

                    if user:
                        db.save_reading_progress(user["id"], story_id, story["title"], total, correct, time_spent)
                        db.save_activity_score(user["id"], "Reading", story["title"], score_pct, 100, f"{correct}/{total} correct")

                    st.rerun()
        else:
            # Results summary
            correct = sum(
                1 for i, q in enumerate(questions)
                if st.session_state.quiz_answers.get(f"q_{story_id}_{i}") == q["answer"]
            )
            total = len(questions)
            score_pct = int((correct / total) * 100) if total > 0 else 0
            time_spent = int(time.time() - st.session_state.reading_start_time) if st.session_state.reading_start_time else 0
            minutes, seconds = divmod(time_spent, 60)

            if score_pct == 100:
                res_emoji, message, res_color = "🏆", "Perfect! You are a superstar reader!", "#10b981"
            elif score_pct >= 75:
                res_emoji, message, res_color = "🌟", "Great job! Almost perfect!", "#3b82f6"
            elif score_pct >= 50:
                res_emoji, message, res_color = "👍", "Good try! Keep reading!", "#f59e0b"
            else:
                res_emoji, message, res_color = "💪", "Let's read it again! You can do it!", "#ef4444"

            st.markdown(f"""
            <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;border:3px solid {res_color};margin-top:1rem;">
                <div style="font-size:5rem;">{res_emoji}</div>
                <h2 style="color:{res_color};margin:0.5rem 0;font-size:2rem;">{correct} out of {total} correct!</h2>
                <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
                <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("")
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                if st.button("📖 Read Again", key="read_again", use_container_width=True):
                    start_story(story_id)
                    st.rerun()
            with col_r2:
                if st.button("📚 More Books", key="more_stories", use_container_width=True, type="primary"):
                    back_to_reading_home()
                    st.rerun()
            with col_r3:
                if st.button("🏠 Dashboard", key="go_dashboard", use_container_width=True):
                    st.session_state.current_page = "user_dashboard"
                    st.session_state.reading_state = None
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state.story_page_idx = 0
                    st.rerun()


# ──────────────────────────────────────────────
# PAGE: Generate a New Story with AI
# ──────────────────────────────────────────────
def render_generate_story():
    name = st.session_state.selected_user

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Books", key="back_to_books_gen"):
            back_to_reading_home()
            st.rerun()

    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">✨ Create a New Story</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Tell us a topic and AI will write a picture book for you!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    topic = st.text_input(
        "What should the story be about?",
        placeholder="e.g. a bunny learns to share, a kitten goes to school, a dinosaur makes friends",
        key="gen_topic",
    )

    col1, col2, _ = st.columns([2, 2, 3])
    with col1:
        generate_clicked = st.button(
            "✨ Generate Story",
            key="btn_do_generate",
            use_container_width=True,
            type="primary",
            disabled=(not topic),
        )
    with col2:
        if st.button("← Cancel", key="btn_cancel_gen", use_container_width=True):
            back_to_reading_home()
            st.rerun()

    if generate_clicked and topic:
        import story_context
        import generate_images as gen_img

        with st.status("Creating your story...", expanded=True) as status:
            # Step 1: Generate story text via LLM
            st.write("📝 Writing the story...")
            try:
                story = story_context.generate_story_from_topic(topic, _HF_TOKEN)
            except Exception as exc:
                status.update(label="Story generation failed", state="error")
                st.error(f"Could not generate story: {exc}")
                return

            st.write(f"📖 **{story['title']}** — {len(story['pages'])} pages, {len(story['questions'])} questions")

            # Step 2: Save story JSON
            st.write("💾 Saving story...")
            rc.save_generated_story(story)

            # Step 3: Generate illustrations
            st.write("🎨 Drawing illustrations...")
            progress_bar = st.progress(0)

            def _update_progress(page_num, total, msg):
                progress_bar.progress(page_num / total, text=msg)

            gen, skip, fail = gen_img.generate_images_for_story(
                story, _HF_TOKEN, progress_callback=_update_progress
            )

            progress_bar.progress(1.0, text="All illustrations done!")

            st.write(f"✅ Created {gen} illustrations" + (f" ({fail} failed)" if fail else ""))
            status.update(label="Story created!", state="complete")

        st.markdown("")
        st.success(f"**{story['title']}** is ready to read!")

        col_r1, col_r2, _ = st.columns([2, 2, 3])
        with col_r1:
            if st.button(f"📖 Read: {story['title']}", key="read_new_story", use_container_width=True, type="primary"):
                start_story(story["id"])
                st.rerun()
        with col_r2:
            if st.button("📚 Back to Books", key="back_books_after_gen", use_container_width=True):
                back_to_reading_home()
                st.rerun()

    # Show some example topics for inspiration
    if not generate_clicked:
        st.markdown("")
        st.markdown("### 💡 Need ideas? Try one of these:")
        idea_cols = st.columns(3, gap="medium")
        ideas = [
            ("🐰", "A bunny learns to share"),
            ("🦕", "A friendly dinosaur"),
            ("🚀", "A trip to the moon"),
            ("🐱", "A kitten's first day at school"),
            ("🌻", "A seed that grows into a flower"),
            ("🐢", "A slow turtle wins a race"),
        ]
        for idx, (emoji, idea) in enumerate(ideas):
            with idea_cols[idx % 3]:
                st.markdown(f"""
                <div style="background:#f8f9ff;border-radius:12px;padding:1rem;text-align:center;margin-bottom:0.5rem;">
                    <div style="font-size:2rem;">{emoji}</div>
                    <div style="color:#4b5563;font-size:0.9rem;">{idea}</div>
                </div>
                """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Main Router
# ──────────────────────────────────────────────
page = st.session_state.current_page

if page == "home":
    render_home()
elif page == "user_dashboard":
    render_user_dashboard()
elif page == "reading_home":
    render_reading_home()
elif page == "reading_story":
    render_reading_story()
elif page == "generate_story":
    render_generate_story()
else:
    render_home()
