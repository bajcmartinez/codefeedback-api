from fastapi import APIRouter

from app.endpoints import feedback, health

router = APIRouter()

router.include_router(health.router)
router.include_router(feedback.router)