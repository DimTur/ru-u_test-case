from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserCreate
from core.models import User, Token
from secure import pwd_context


async def register_user_controller(session: AsyncSession, user_in: UserCreate) -> User:
    stmt = select(User).where(User.login == user_in.login)
    result: Result = await session.execute(stmt)
    existing_user = result.scalar()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this login already exists!",
        )

    user = User(**user_in.model_dump())
    user.hashed_password = pwd_context.hash(user_in.hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_token(session: AsyncSession, access_token: str):
    stmt = select(Token).where(Token.access_token == access_token)
    result: Result = await session.execute(stmt)
    token = result.scalar()

    if token:
        return await token.user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED",
        )
