from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.api.v1.schemas import UserOut
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)) -> User:
    return user
