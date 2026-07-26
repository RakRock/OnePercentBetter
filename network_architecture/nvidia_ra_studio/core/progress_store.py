"""SQLite persistence for profiles, progress, quizzes, notes, and plans."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "studio.db"


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class ProgressStore:
    def __init__(self, db_path: Path | None = None):
        self.db_path = Path(db_path or DEFAULT_DB)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._conn() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_name TEXT UNIQUE NOT NULL,
                    role TEXT DEFAULT '',
                    level TEXT DEFAULT 'beginner',
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS modules (
                    id INTEGER PRIMARY KEY,
                    slug TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    difficulty TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY,
                    module_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    FOREIGN KEY (module_id) REFERENCES modules(id)
                );
                CREATE TABLE IF NOT EXISTS user_progress (
                    user_id INTEGER NOT NULL,
                    module_id INTEGER NOT NULL,
                    completed INTEGER DEFAULT 0,
                    notes TEXT DEFAULT '',
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (user_id, module_id)
                );
                CREATE TABLE IF NOT EXISTS quiz_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    quiz_id TEXT NOT NULL,
                    score REAL NOT NULL,
                    total INTEGER NOT NULL,
                    answers_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS design_drills (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS drill_completions (
                    user_id INTEGER NOT NULL,
                    drill_id TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    notes TEXT DEFAULT '',
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (user_id, drill_id)
                );
                CREATE TABLE IF NOT EXISTS generated_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    plan_json TEXT NOT NULL,
                    markdown TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    module_id INTEGER,
                    body TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS bookmarks (
                    user_id INTEGER NOT NULL,
                    ref_type TEXT NOT NULL,
                    ref_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (user_id, ref_type, ref_id)
                );
                """
            )

    def list_profiles(self) -> list[str]:
        with self._conn() as conn:
            rows = conn.execute("SELECT profile_name FROM users ORDER BY profile_name").fetchall()
            return [r["profile_name"] for r in rows]

    def get_or_create_user(self, profile_name: str, role: str = "", level: str = "beginner") -> int:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT id FROM users WHERE profile_name = ?", (profile_name,)
            ).fetchone()
            if row:
                return int(row["id"])
            cur = conn.execute(
                "INSERT INTO users (profile_name, role, level, created_at) VALUES (?, ?, ?, ?)",
                (profile_name, role, level, _utcnow()),
            )
            return int(cur.lastrowid)

    def set_module_completed(self, user_id: int, module_id: int, completed: bool, notes: str = "") -> None:
        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO user_progress (user_id, module_id, completed, notes, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, module_id) DO UPDATE SET
                    completed = excluded.completed,
                    notes = COALESCE(NULLIF(excluded.notes, ''), user_progress.notes),
                    updated_at = excluded.updated_at
                """,
                (user_id, module_id, int(completed), notes, _utcnow()),
            )

    def get_module_progress(self, user_id: int) -> dict[int, dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT module_id, completed, notes FROM user_progress WHERE user_id = ?",
                (user_id,),
            ).fetchall()
            return {int(r["module_id"]): {"completed": bool(r["completed"]), "notes": r["notes"]} for r in rows}

    def save_module_notes(self, user_id: int, module_id: int, notes: str) -> None:
        self.set_module_completed(user_id, module_id, self.is_module_completed(user_id, module_id), notes)

    def is_module_completed(self, user_id: int, module_id: int) -> bool:
        prog = self.get_module_progress(user_id)
        return prog.get(module_id, {}).get("completed", False)

    def record_quiz_attempt(
        self, user_id: int, quiz_id: str, score: float, total: int, answers: dict
    ) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO quiz_attempts (user_id, quiz_id, score, total, answers_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, quiz_id, score, total, json.dumps(answers), _utcnow()),
            )

    def quiz_stats(self, user_id: int) -> dict[str, Any]:
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT quiz_id, score, total, created_at FROM quiz_attempts
                WHERE user_id = ? ORDER BY created_at DESC
                """,
                (user_id,),
            ).fetchall()
        if not rows:
            return {"count": 0, "average_pct": 0.0, "recent": []}
        pcts = [(r["score"] / r["total"] * 100) if r["total"] else 0 for r in rows]
        return {
            "count": len(rows),
            "average_pct": round(sum(pcts) / len(pcts), 1),
            "recent": [dict(r) for r in rows[:5]],
        }

    def weak_domains(self, user_id: int, domain_scores: dict[str, list[float]]) -> list[str]:
        """domain_scores: domain -> list of percentage scores from last attempts."""
        avgs = {d: (sum(s) / len(s) if s else 100) for d, s in domain_scores.items()}
        return sorted(avgs.keys(), key=lambda d: avgs[d])[:3]

    def save_plan(self, user_id: int, plan: dict, markdown: str) -> int:
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO generated_plans (user_id, plan_json, markdown, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, json.dumps(plan), markdown, _utcnow()),
            )
            return int(cur.lastrowid)

    def latest_plan(self, user_id: int) -> dict | None:
        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT plan_json, markdown, created_at FROM generated_plans
                WHERE user_id = ? ORDER BY id DESC LIMIT 1
                """,
                (user_id,),
            ).fetchone()
        if not row:
            return None
        return {
            "plan": json.loads(row["plan_json"]),
            "markdown": row["markdown"],
            "created_at": row["created_at"],
        }

    def set_drill_completed(self, user_id: int, drill_id: str, completed: bool, notes: str = "") -> None:
        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO drill_completions (user_id, drill_id, completed, notes, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, drill_id) DO UPDATE SET
                    completed = excluded.completed,
                    notes = excluded.notes,
                    updated_at = excluded.updated_at
                """,
                (user_id, drill_id, int(completed), notes, _utcnow()),
            )

    def drill_progress(self, user_id: int) -> dict[str, bool]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT drill_id, completed FROM drill_completions WHERE user_id = ?",
                (user_id,),
            ).fetchall()
        return {r["drill_id"]: bool(r["completed"]) for r in rows}

    def toggle_bookmark(self, user_id: int, ref_type: str, ref_id: str) -> bool:
        with self._conn() as conn:
            exists = conn.execute(
                "SELECT 1 FROM bookmarks WHERE user_id = ? AND ref_type = ? AND ref_id = ?",
                (user_id, ref_type, ref_id),
            ).fetchone()
            if exists:
                conn.execute(
                    "DELETE FROM bookmarks WHERE user_id = ? AND ref_type = ? AND ref_id = ?",
                    (user_id, ref_type, ref_id),
                )
                return False
            conn.execute(
                "INSERT INTO bookmarks (user_id, ref_type, ref_id, created_at) VALUES (?, ?, ?, ?)",
                (user_id, ref_type, ref_id, _utcnow()),
            )
            return True

    def list_bookmarks(self, user_id: int) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT ref_type, ref_id, created_at FROM bookmarks WHERE user_id = ?",
                (user_id,),
            ).fetchall()
        return [dict(r) for r in rows]

    def dashboard_summary(self, user_id: int, total_modules: int) -> dict[str, Any]:
        prog = self.get_module_progress(user_id)
        completed = sum(1 for p in prog.values() if p["completed"])
        q = self.quiz_stats(user_id)
        drills = self.drill_progress(user_id)
        drill_done = sum(1 for v in drills.values() if v)
        return {
            "modules_completed": completed,
            "modules_total": total_modules,
            "progress_pct": round(completed / total_modules * 100, 1) if total_modules else 0,
            "quiz_average_pct": q["average_pct"],
            "quiz_attempts": q["count"],
            "drills_completed": drill_done,
        }
