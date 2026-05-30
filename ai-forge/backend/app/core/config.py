"""Application configuration via environment variables."""

import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# ai-forge/.env (monorepo root), overridable via AIFORGE_ENV_FILE
_DEFAULT_ENV = Path(__file__).resolve().parents[3] / ".env"
_ENV_FILE = Path(os.getenv("AIFORGE_ENV_FILE", _DEFAULT_ENV))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE) if _ENV_FILE.is_file() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    secret_key: str = "dev-secret-change-me"
    cors_origins: str = "http://localhost:3000"

    database_url: str = "sqlite+aiosqlite:///./data/aiforge.db"
    redis_url: str = "redis://localhost:6380/0"
    qdrant_url: str = "http://localhost:6333"

    anthropic_api_key: str = ""
    openai_api_key: str = ""
    google_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"

    default_llm_provider: str = "anthropic"
    default_llm_model: str = "claude-sonnet-4-20250514"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
