"""Claude-powered mentor — socratic guidance, not answer dumps."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Conversation, Message, Project
from app.services.llm.provider import LLMProvider

PERSONALITY_PROMPTS = {
    "teacher": (
        "You are a patient AI engineering teacher. Use questions and hints. "
        "Never dump full solutions immediately."
    ),
    "architect": (
        "You are a senior AI architect. Focus on trade-offs, boundaries, and production readiness."
    ),
    "debugger": (
        "You are a debugging mentor. Ask for logs, reproduce steps, and isolate root causes."
    ),
    "interviewer": (
        "You are a technical interviewer. Probe depth with follow-up questions."
    ),
    "reviewer": (
        "You are a code reviewer. Point out risks, missing tests, and clarity issues."
    ),
}

BASE_RULES = """
Rules:
- Guide with questions before giving answers.
- Prefer incremental hints over full code dumps.
- When code is needed, show the smallest snippet that unblocks the learner.
- Tie advice to production AI systems (latency, cost, evals, observability).
- If the user asks for architecture, use bullet trade-offs and a Mermaid diagram when helpful.
"""


class MentorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.llm = LLMProvider()

    async def get_or_create_conversation(
        self,
        user_id: uuid.UUID,
        *,
        conversation_id: uuid.UUID | None = None,
        project_id: uuid.UUID | None = None,
        personality: str = "teacher",
    ) -> Conversation:
        if conversation_id:
            conv = await self.db.get(Conversation, conversation_id)
            if conv and conv.user_id == user_id:
                return conv
        conv = Conversation(
            user_id=user_id,
            project_id=project_id,
            mentor_personality=personality,
            title="Mentor session",
        )
        self.db.add(conv)
        await self.db.flush()
        return conv

    async def list_messages(self, conversation_id: uuid.UUID) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        return list(result.scalars().all())

    async def stream_reply(
        self,
        conversation: Conversation,
        user_text: str,
    ) -> AsyncIterator[str]:
        project_ctx = ""
        if conversation.project_id:
            project = await self.db.get(Project, conversation.project_id)
            if project:
                project_ctx = f"\nActive project: {project.title}\n{project.summary}"

        history = await self.list_messages(conversation.id)
        messages = [
            {
                "role": "system",
                "content": PERSONALITY_PROMPTS.get(conversation.mentor_personality, PERSONALITY_PROMPTS["teacher"])
                + BASE_RULES
                + project_ctx,
            },
        ]
        for msg in history[-12:]:
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": user_text})

        self.db.add(
            Message(conversation_id=conversation.id, role="user", content=user_text)
        )
        await self.db.flush()

        full: list[str] = []
        async for token in self.llm.chat_stream(messages):
            full.append(token)
            yield token

        assistant_text = "".join(full)
        self.db.add(
            Message(
                conversation_id=conversation.id,
                role="assistant",
                content=assistant_text,
            )
        )
        await self.db.commit()
