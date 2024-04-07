import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .schemas import ColorCreate, ColorUpdate
from core.models import (
    Palette,
    User,
    Color,
)


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
    color = Color(
        user_id=user_id,
        palette_id=palette_id,
        **color_in.model_dump(),
    )
    session.add(color)
    await session.commit()
    await session.refresh(color)

    return color


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
    color: Color,
    color_update: ColorUpdate,
    partial: bool = True,
) -> Color:
    for hex_color, value in color_update.model_dump(exclude_unset=partial).items():
        setattr(color, hex_color, value)
    await session.commit()

    return color


async def delete_color(
    session: AsyncSession,
    color: Color,
) -> None:
    await session.delete(color)
    await session.commit()
