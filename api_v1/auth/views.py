from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.schemas import TokenInfo
from api_v1.users.schemas import AuthUser, User
from .dependencies import (
    validate_auth_user,
    get_current_auth_user,
    get_current_token_payload,
)
from .utils import encode_jwt
from core.models.db_helper import db_helper

router = APIRouter(tags=["JWT"])


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


@router.get("/me/")
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_auth_user),
):
    iat = payload.get("iat")
    return {
        "id": user.id,
        "login": user.login,
        "name": user.name,
        "logged_in_at": iat,
    }
