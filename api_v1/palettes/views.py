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
from .dependencies import get_palette_by_id
from .schemas import (
    Palette,
    PaletteCreate,
    PaletteUpdate,
)
from api_v1.users.schemas import User
from core.models.db_helper import db_helper
from ..auth.dependencies import get_current_auth_user

router = APIRouter(tags=["Palettes"])


@router.get(
    "/",
    response_model=list[Palette],
    status_code=status.HTTP_200_OK,
    summary="Returns list for all palettes",
)
async def get_palettes(
    user: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_palettes(
        session=session,
        user_id=user.id,
    )


@router.post(
    "/",
    response_model=PaletteCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Create palette",
)
async def create_palette(
    palette_in: PaletteCreate,
    user: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_palette(
        session=session,
        user_id=user.id,
        palette_in=palette_in,
    )


@router.get(
    "/{palette_id}",
    response_model=Palette,
    status_code=status.HTTP_200_OK,
    summary="Return palette by id",
)
async def get_palette_by_id(palette: Palette = Depends(get_palette_by_id)) -> Palette:
    return palette


@router.patch(
    "/{palette_id}",
    response_model=PaletteUpdate,
    status_code=status.HTTP_200_OK,
    summary="Update palette by id",
)
async def update_palette_partial(
    palette_update: PaletteUpdate,
    palette: Palette = Depends(get_palette_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_palette_partial(
        session=session,
        palette_update=palette_update,
        palette=palette,
    )


@router.delete(
    "/{palette_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete palette by id",
)
async def delete_palette(
    palette: Palette = Depends(get_palette_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_palette(session=session, palette=palette)
