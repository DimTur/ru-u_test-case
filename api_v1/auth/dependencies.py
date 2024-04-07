from jwt.exceptions import InvalidTokenError
from fastapi import (
    status,
    Depends,
    Form,
    HTTPException,
)
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.crud import get_user_by_login
from .utils import validate_password, decode_jwt
from core.models.db_helper import db_helper
from ..users.schemas import User
from core.models import User as UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/jwt/login/")


async def validate_auth_user(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid login or password",
    )
    user = await get_user_by_login(
        login=username,
        session=session,
    )

    if not user:
        raise unauthed_exc

    if not validate_password(
        password=password,
        hashed_password=user.hashed_password,
    ):
        raise unauthed_exc

    return user


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )

    return payload


async def get_current_auth_user(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    payload: dict = Depends(get_current_token_payload),
) -> User:
    login: str | None = payload.get("login")
    user: UserModel = await get_user_by_login(
        login=login,
        session=session,
    )

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid",
    )
