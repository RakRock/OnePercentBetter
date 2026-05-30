"""LiteLLM-backed provider abstraction (Claude primary)."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

from app.core.config import get_settings

settings = get_settings()


class LLMProvider:
    """Unified chat + structured completion interface."""

    def __init__(
        self,
        provider: str | None = None,
        model: str | None = None,
    ):
        self.provider = provider or settings.default_llm_provider
        self.model = model or settings.default_llm_model

    def _litellm_model(self) -> str:
        if self.provider == "anthropic":
            return f"anthropic/{self.model}"
        if self.provider == "openai":
            return f"openai/{self.model}"
        if self.provider == "ollama":
            return f"ollama/{self.model}"
        if self.provider == "gemini":
            return f"gemini/{self.model}"
        return self.model

    async def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.4,
        max_tokens: int = 2048,
    ) -> str:
        if self.provider == "anthropic" and not self._api_key():
            user_msg = messages[-1]["content"] if messages else ""
            return (
                "**Demo mode** (set `ANTHROPIC_API_KEY` in `ai-forge/.env` for live Claude replies)\n\n"
                f"Good question about: *{user_msg[:120]}*\n\n"
                "Try breaking this into smaller steps:\n"
                "1. What is the smallest piece you can verify works?\n"
                "2. What error or output do you see today?\n"
                "3. What would a minimal test prove success?\n\n"
                "Share your answers and I'll guide the next hint."
            )

        import litellm

        response = await litellm.acompletion(
            model=self._litellm_model(),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=self._api_key(),
        )
        return response.choices[0].message.content or ""

    async def chat_stream(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.4,
        max_tokens: int = 2048,
    ) -> AsyncIterator[str]:
        import litellm

        stream = await litellm.acompletion(
            model=self._litellm_model(),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            api_key=self._api_key(),
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    async def structured_json(
        self,
        messages: list[dict[str, str]],
        *,
        schema_hint: str,
        max_tokens: int = 1500,
    ) -> dict[str, Any]:
        system = messages[0]["content"] if messages else ""
        prompt = messages[-1]["content"] if messages else ""
        text = await self.chat(
            [
                {
                    "role": "system",
                    "content": f"{system}\nRespond ONLY with valid JSON. Schema: {schema_hint}",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=max_tokens,
        )
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
        return {"raw": text}

    def _api_key(self) -> str | None:
        if self.provider == "anthropic":
            return settings.anthropic_api_key or None
        if self.provider == "openai":
            return settings.openai_api_key or None
        if self.provider == "gemini":
            return settings.google_api_key or None
        return None
