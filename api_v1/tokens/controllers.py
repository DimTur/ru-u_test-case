import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import AuthUser
from core.models import User, Token
from secure import pwd_context


async def create_token_controller(session: AsyncSession, user_in: AuthUser) -> Token:
    stmt = select(User).where(User.login == user_in.login)
    result: Result = await session.execute(stmt)
    existing_user = result.scalar()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not pwd_context.verify(user_in.hashed_password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect login or password",
        )

    token: Token = Token(user_id=existing_user.id, access_token=str(uuid.uuid4()))
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return token
