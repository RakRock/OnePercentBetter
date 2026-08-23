"""Repository root path helper for scripts under scripts/."""

from __future__ import annotations

from pathlib import Path

# scripts/repo_root.py → parents[1] is the repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
