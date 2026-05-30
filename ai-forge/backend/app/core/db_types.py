"""Portable column types (SQLite + PostgreSQL)."""

from sqlalchemy import JSON, Uuid

# Re-export for model modules
UuidCol = Uuid
JsonCol = JSON
