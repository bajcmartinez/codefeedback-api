from fastapi import APIRouter

from app.models.feedback import FeedbackIn, FeedbackOut
from app.repositories.feedback import FeedbackRepository


router = APIRouter(prefix='/feedback', tags=['Feedback'])

@router.post('', status_code=201)
async def create_feedback(feedback: FeedbackIn) -> FeedbackOut:
    return FeedbackRepository.create_feedback(feedback)