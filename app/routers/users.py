from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import get_current_active_user
from app.core.user_schema import UserResponse
from app.models.users import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/items/", response_model=UserResponse)
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
