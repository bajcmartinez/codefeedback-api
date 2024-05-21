from fastapi import APIRouter, HTTPException

from app.models.feedback import FeedbackIn, FeedbackOut
from app.repositories.feedback import FeedbackRepository

router = APIRouter(prefix='/feedback', tags=['Feedback'])


@router.post('', status_code=201)
async def create_feedback(feedback_in: FeedbackIn) -> FeedbackOut:
    return FeedbackRepository.create_feedback(feedback_in, "")


@router.get('/{feedback_id}')
async def get_feedback(feedback_id: str) -> FeedbackOut:
    feedback = FeedbackRepository.get_feedback(feedback_id)

    if feedback is None:
        raise HTTPException(status_code=404, detail='Feedback not found')

    return feedback
