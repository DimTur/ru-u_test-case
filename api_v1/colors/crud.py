import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .color_fetcher import fetch_color_title
from .schemas import ColorCreate, ColorUpdate
from core.models import (
    Palette,
    User,
    Color,
)
from ..auth.actions import user_has_palette_access


async def get_colors(
    session: AsyncSession,
    user_id: uuid.UUID,
    palette_id: uuid.UUID,
) -> list[Color]:
    stmt = (
        select(Color)
        .join(Color.palette)
        .join(Palette.user)
        .options(joinedload(Color.palette).joinedload(Palette.user))
        .where(User.id == user_id)
        .where(Palette.id == palette_id)
        .order_by(Color.title)
    )
    result: Result = await session.execute(stmt)
    colors = result.scalars().all()

    return list(colors)


async def create_color(
    session: AsyncSession,
    user_id: uuid.UUID,
    palette_id: uuid.UUID,
    color_in: ColorCreate,
) -> Color:
    try:
        if not await user_has_palette_access(
            session=session,
            user_id=user_id,
            palette_id=palette_id,
        ):
            raise HTTPException(status_code=403, detail="Forbidden access to palette")

        title = await fetch_color_title(color_in.hex_color)
        color = Color(
            palette_id=palette_id,
            title=title,
            hex_color=color_in.hex_color,
        )
        session.add(color)
        await session.commit()
        await session.refresh(color)
        return color
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )


async def get_color_by_id(
    session: AsyncSession,
    user_id: uuid.UUID,
    palette_id: uuid.UUID,
    color_id: uuid.UUID,
) -> Color | None:
    stmt = (
        select(Color)
        .join(Color.palette)
        .join(Palette.user)
        .options(joinedload(Color.palette).joinedload(Palette.user))
        .where(User.id == user_id)
        .where(Palette.id == palette_id)
        .where(Color.id == color_id)
    )
    result: Result = await session.execute(stmt)
    color = result.scalar()

    return color


async def update_color_partial(
    session: AsyncSession,
    user_id: uuid.UUID,
    color: Color,
    color_update: ColorUpdate,
    partial: bool = True,
) -> Color:
    try:
        if not await user_has_palette_access(
            session=session,
            user_id=user_id,
            palette_id=color.palette_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have access to the palette",
            )

        for field, value in color_update.model_dump(exclude_unset=partial).items():
            setattr(color, field, value)
            if "hex_color":
                title = await fetch_color_title(color_update.hex_color)
                setattr(color, "title", title)
        await session.commit()
        await session.refresh(color)
        return color
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def delete_color(
    session: AsyncSession,
    color: Color,
) -> None:
    await session.delete(color)
    await session.commit()
