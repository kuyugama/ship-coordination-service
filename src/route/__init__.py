from fastapi import APIRouter

# Top-level router
router = APIRouter()

from .v1 import router as v1_router

router.include_router(v1_router, prefix="/v1", tags=["V1"])
