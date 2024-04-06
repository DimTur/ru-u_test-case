from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .controller import register_user_controller
from api_v1.users.schemas import User, UserCreate
from core.models.db_helper import db_helper

router = APIRouter(tags=["Users"])


@router.post(
    "",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="New user registration",
)
async def register_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await register_user_controller(
        session=session,
        user_in=user_in,
    )
