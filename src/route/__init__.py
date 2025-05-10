from fastapi import APIRouter

# Top-level router
router = APIRouter()

from .auth import router as auth_router
from .user import router as user_router

router.include_router(auth_router, tags=["Authorization"])
router.include_router(user_router, tags=["User"])
