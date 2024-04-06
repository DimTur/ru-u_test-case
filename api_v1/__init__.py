from fastapi import APIRouter

from .users.views import router as users_router
from .tokens.views import router as tokens_router


router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=tokens_router, prefix="/tokens")
