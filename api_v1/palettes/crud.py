import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .schemas import PaletteCreate, PaletteUpdate
from core.models import Palette, User


async def get_palettes(session: AsyncSession, user_id: uuid.UUID) -> list[Palette]:
    stmt = (
        select(Palette)
        .join(Palette.user)
        .options(joinedload(Palette.user))
        .where(User.id == user_id)
        .order_by(Palette.title)
    )
    result: Result = await session.execute(stmt)
    palettes = result.scalars().all()

    return list(palettes)


async def create_palette(
    session: AsyncSession,
    user_id: uuid.UUID,
    palette_in: PaletteCreate,
) -> Palette:
    palette = Palette(
        user_id=user_id,
        **palette_in.model_dump(),
    )
    session.add(palette)
    await session.commit()
    await session.refresh(palette)

    return palette


async def get_palette_by_id(
    session: AsyncSession,
    palette_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Palette | None:
    stmt = (
        select(Palette)
        .join(Palette.user)
        .where(User.id == user_id)
        .where(Palette.id == palette_id)
    )
    result: Result = await session.execute(stmt)
    palette = result.scalar()

    return palette


async def update_palette_partial(
    session: AsyncSession,
    palette: Palette,
    palette_update: PaletteUpdate,
    partial: bool = True,
) -> Palette:
    for title, value in palette_update.model_dump(exclude_unset=partial).items():
        setattr(palette, title, value)
    await session.commit()

    return palette


async def delete_palette(
    session: AsyncSession,
    palette: Palette,
) -> None:
    await session.delete(palette)
    await session.commit()
