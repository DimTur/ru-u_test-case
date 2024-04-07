from fastapi import APIRouter

from .users.views import router as users_router
from .auth.views import router as jwt_auth_router


router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=jwt_auth_router, prefix="/jwt")
