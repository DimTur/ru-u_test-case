from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.tokens.controllers import create_token_controller
from api_v1.tokens.schemas import Token
from api_v1.users.schemas import AuthUser
from core.models.db_helper import db_helper

router = APIRouter(tags=["Tokens"])


@router.post(
    "/",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    responses={},
    summary="New token created",
)
async def create_token(
    user_in: AuthUser,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await create_token_controller(
        session=session,
        user_in=user_in,
    )
