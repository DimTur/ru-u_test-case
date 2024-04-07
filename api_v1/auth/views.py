from fastapi import (
    APIRouter,
    status,
    Depends,
    Form,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.crud import get_user_by_login
from api_v1.auth.schemas import TokenInfo
from api_v1.users.schemas import AuthUser
from .utils import validate_password, encode_jwt
from core.models.db_helper import db_helper

router = APIRouter(tags=["JWT"])


async def validate_auth_user(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    login: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid login or password",
    )
    user = await get_user_by_login(
        login=login,
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


@router.post(
    "/login/",
    response_model=TokenInfo,
)
async def auth_user_issue_jwt(
    user: AuthUser = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": str(user.id),
        "login": user.login,
    }
    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
