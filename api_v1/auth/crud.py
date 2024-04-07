from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def get_user_by_login(login: str, session: AsyncSession) -> User:
    stmt = select(User).where(User.login == login)
    result: Result = await session.execute(stmt)
    existing_user = result.scalar()

    if existing_user:
        return existing_user
