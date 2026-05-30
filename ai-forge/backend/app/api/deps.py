"""FastAPI dependencies — dev auth (Clerk-ready in Phase 2)."""

from __future__ import annotations

import uuid

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import User


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    x_forge_user_id: str | None = Header(default=None, alias="X-Forge-User-Id"),
    x_forge_email: str | None = Header(default=None, alias="X-Forge-Email"),
) -> User:
    if x_forge_user_id:
        try:
            uid = uuid.UUID(x_forge_user_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid X-Forge-User-Id") from exc
        user = await db.get(User, uid)
        if user:
            return user

    email = (x_forge_email or "rakesh@aiforge.local").lower()
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user:
        return user

    user = User(email=email, display_name=email.split("@")[0].title())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
