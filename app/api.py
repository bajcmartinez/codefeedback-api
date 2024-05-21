from fastapi import APIRouter

from app.endpoints.health import health
from app.endpoints.feedback import feedback


router = APIRouter()

router.include_router(health.router)
router.include_router(feedback.router)