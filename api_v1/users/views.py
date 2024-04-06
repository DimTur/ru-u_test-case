from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from secure import apikey_scheme
from .controllers import register_user_controller, get_user_by_token
from .responses import post_user_responses
from api_v1.users.schemas import (
    User,
    UserCreate,
    UserBase,
)
from core.models.db_helper import db_helper

router = APIRouter(tags=["Users"])


@router.post(
    "/register/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    responses=post_user_responses,
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


@router.get("/self/", response_model=UserBase)
async def get_user_by_id(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_user_by_token(
        session=session,
        access_token=access_token,
    )
