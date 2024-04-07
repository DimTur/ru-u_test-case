import uuid
from typing import Annotated

from fastapi import (
    status,
    Depends,
    Path,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from api_v1.users.schemas import User
from core.models.db_helper import db_helper
from ..auth.dependencies import get_current_auth_user


async def get_palette_by_id(
    palette_id: Annotated[uuid.UUID, Path],
    user: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    palette = await crud.get_palette_by_id(
        session=session,
        palette_id=palette_id,
        user_id=user.id,
    )

    if palette:
        return palette
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Palette not found",
    )
