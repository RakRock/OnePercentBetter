"""
Database module for the 1% Better Every Day app.
Uses SQLite for persistent storage of user activity, streaks, and scores.
"""

import sqlite3
import os
from datetime import datetime, timedelta
from contextlib import contextmanager

DB_PATH = os.environ.get("ONEPERCENT_DB", "onepercent.db")


@contextmanager
def get_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initialize database tables if they don't exist."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                avatar_emoji TEXT DEFAULT '🧒',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS daily_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                log_date DATE NOT NULL,
                logged_in_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, log_date)
            );

            CREATE TABLE IF NOT EXISTS activity_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_type TEXT NOT NULL,
                activity_name TEXT NOT NULL,
                score INTEGER DEFAULT 0,
                max_score INTEGER DEFAULT 100,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                log_date DATE NOT NULL,
                details TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS reading_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                story_id TEXT NOT NULL,
                story_title TEXT NOT NULL,
                questions_total INTEGER DEFAULT 0,
                questions_correct INTEGER DEFAULT 0,
                time_spent_seconds INTEGER DEFAULT 0,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                log_date DATE NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)

        # Seed default users
        default_users = [
            ("Arjun", "🦁"),
            ("Krish", "🚀"),
            ("Sangeetha", "🌸"),
            ("Rakesh", "⚡"),
        ]
        for name, emoji in default_users:
            conn.execute(
                "INSERT OR IGNORE INTO users (name, avatar_emoji) VALUES (?, ?)",
                (name, emoji),
            )


def get_user(name: str) -> dict | None:
    """Get a user by name."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
        return dict(row) if row else None


def record_daily_login(user_id: int):
    """Record a daily login for the user (once per day)."""
    today = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO daily_logs (user_id, log_date) VALUES (?, ?)",
            (user_id, today),
        )


def get_login_streak(user_id: int) -> int:
    """Calculate the current consecutive login streak for a user."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT log_date FROM daily_logs WHERE user_id = ? ORDER BY log_date DESC",
            (user_id,),
        ).fetchall()

    if not rows:
        return 0

    streak = 0
    today = datetime.now().date()

    for row in rows:
        log_date = datetime.strptime(row["log_date"], "%Y-%m-%d").date()
        expected_date = today - timedelta(days=streak)
        if log_date == expected_date:
            streak += 1
        else:
            break

    return streak


def get_total_login_days(user_id: int) -> int:
    """Get total number of days the user has logged in."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(DISTINCT log_date) as total FROM daily_logs WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return row["total"] if row else 0


def save_activity_score(
    user_id: int,
    activity_type: str,
    activity_name: str,
    score: int,
    max_score: int,
    details: str = "",
):
    """Save a score for an activity."""
    today = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO activity_scores 
               (user_id, activity_type, activity_name, score, max_score, log_date, details)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, activity_type, activity_name, score, max_score, today, details),
        )


def get_today_scores(user_id: int, activity_type: str = None) -> list:
    """Get all scores for today, optionally filtered by activity type."""
    today = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        if activity_type:
            rows = conn.execute(
                """SELECT * FROM activity_scores 
                   WHERE user_id = ? AND log_date = ? AND activity_type = ?
                   ORDER BY completed_at DESC""",
                (user_id, today, activity_type),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM activity_scores 
                   WHERE user_id = ? AND log_date = ?
                   ORDER BY completed_at DESC""",
                (user_id, today),
            ).fetchall()
        return [dict(r) for r in rows]


def get_scores_history(user_id: int, activity_type: str = None, days: int = 30) -> list:
    """Get score history for the past N days."""
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    with get_connection() as conn:
        if activity_type:
            rows = conn.execute(
                """SELECT log_date, activity_name, score, max_score 
                   FROM activity_scores 
                   WHERE user_id = ? AND log_date >= ? AND activity_type = ?
                   ORDER BY log_date ASC""",
                (user_id, start_date, activity_type),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT log_date, activity_type, activity_name, score, max_score 
                   FROM activity_scores 
                   WHERE user_id = ? AND log_date >= ?
                   ORDER BY log_date ASC""",
                (user_id, start_date),
            ).fetchall()
        return [dict(r) for r in rows]


def save_reading_progress(
    user_id: int,
    story_id: str,
    story_title: str,
    questions_total: int,
    questions_correct: int,
    time_spent_seconds: int,
):
    """Save reading comprehension progress."""
    today = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO reading_progress 
               (user_id, story_id, story_title, questions_total, questions_correct, 
                time_spent_seconds, log_date)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                story_id,
                story_title,
                questions_total,
                questions_correct,
                time_spent_seconds,
                today,
            ),
        )


def get_reading_history(user_id: int, days: int = 30) -> list:
    """Get reading history for the past N days."""
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT * FROM reading_progress 
               WHERE user_id = ? AND log_date >= ?
               ORDER BY completed_at DESC""",
            (user_id, start_date),
        ).fetchall()
        return [dict(r) for r in rows]
