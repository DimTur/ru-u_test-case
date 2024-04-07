import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    status,
    Depends,
    Path,
)
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.models.db_helper import db_helper
from .dependencies import _get_color_by_id
from .schemas import ColorCreate, Color, ColorUpdate
from ..auth.dependencies import get_current_auth_user
from ..users.schemas import User

router = APIRouter(tags=["Colors"])


@router.get(
    "/",
    response_model="",
    status_code=status.HTTP_200_OK,
    summary="Returns list for all colors",
)
async def get_colors(
    palette_id: Annotated[uuid.UUID, Path],
    user: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_colors(
        session=session,
        user_id=user.id,
        palette_id=palette_id,
    )


@router.post(
    "/",
    response_model="",
    status_code=status.HTTP_200_OK,
    summary="Create color",
)
async def create_color(
    color_in: ColorCreate,
    palette_id: Annotated[uuid.UUID, Path],
    user: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_color(
        session=session,
        user_id=user.id,
        palette_id=palette_id,
        color_in=color_in,
    )


@router.get(
    "/{color_id}",
    response_model="",
    status_code=status.HTTP_200_OK,
    summary="Return color by id",
)
async def get_color_by_id(color: Color = Depends(_get_color_by_id)) -> Color:
    return color


@router.patch(
    "/{color_id}",
    response_model="",
    status_code=status.HTTP_200_OK,
    summary="Update color by id",
)
async def update_color_partial(
    color_update: ColorUpdate,
    color: Color = Depends(_get_color_by_id),
    user: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_color_partial(
        session=session,
        color=color,
        color_update=color_update,
        user_id=user.id,
    )


@router.delete(
    "/{color_id}",
    response_model="",
    status_code=status.HTTP_200_OK,
    summary="Delete color by id",
)
async def delete_color(
    color: Color = Depends(_get_color_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_color(session=session, color=color)
