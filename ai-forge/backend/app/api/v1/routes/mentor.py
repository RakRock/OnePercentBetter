from __future__ import annotations

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.api.deps import get_current_user, get_db
from app.api.v1.schemas import ConversationOut, MentorChatRequest, MessageOut
from app.models import User
from app.services.mentor_service import MentorService

router = APIRouter(prefix="/mentor", tags=["mentor"])


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageOut])
async def list_messages(
    conversation_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list:
    service = MentorService(db)
    conv = await service.get_or_create_conversation(user.id, conversation_id=conversation_id)
    if conv.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await service.list_messages(conversation_id)


@router.post("/chat")
async def mentor_chat(
    body: MentorChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MentorService(db)
    conv = await service.get_or_create_conversation(
        user.id,
        conversation_id=body.conversation_id,
        project_id=body.project_id,
        personality=body.personality,
    )

    async def event_generator():
        async for token in service.stream_reply(conv, body.message):
            yield {"event": "token", "data": json.dumps({"text": token})}
        yield {
            "event": "done",
            "data": json.dumps({"conversation_id": str(conv.id)}),
        }

    return EventSourceResponse(event_generator())


@router.post("/chat/sync", response_model=dict)
async def mentor_chat_sync(
    body: MentorChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Non-streaming fallback for simple clients."""
    from app.agents.mentor_graph import build_mentor_graph

    service = MentorService(db)
    conv = await service.get_or_create_conversation(
        user.id,
        conversation_id=body.conversation_id,
        project_id=body.project_id,
        personality=body.personality,
    )
    graph = build_mentor_graph()
    state = await graph.ainvoke(
        {
            "user_message": body.message,
            "personality": body.personality,
            "project_context": "",
        }
    )
    text = state.get("response", "")
    from app.models import Message

    db.add(Message(conversation_id=conv.id, role="user", content=body.message))
    db.add(Message(conversation_id=conv.id, role="assistant", content=text))
    await db.commit()
    return {"conversation_id": str(conv.id), "reply": text}
