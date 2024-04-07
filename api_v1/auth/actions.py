import uuid

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Palette


async def get_user_by_login(login: str, session: AsyncSession) -> User:
    stmt = select(User).where(User.login == login)
    result: Result = await session.execute(stmt)
    existing_user = result.scalar()

    if existing_user:
        return existing_user


async def user_has_palette_access(
    session: AsyncSession,
    user_id: uuid.UUID,
    palette_id: uuid.UUID,
) -> bool:
    palette = await session.execute(select(Palette).filter(Palette.id == palette_id))
    palette = palette.scalar_one_or_none()

    if palette and palette.user_id == user_id:
        return True
    else:
        return False
