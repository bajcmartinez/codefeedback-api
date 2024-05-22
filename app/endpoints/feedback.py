from fastapi import APIRouter, HTTPException

from app.models.feedback import FeedbackIn, FeedbackOut
from app.repositories.feedback import FeedbackRepository

router = APIRouter(prefix='/feedback', tags=['Feedback'])


@router.post('', status_code=201)
async def create_feedback(feedback_in: FeedbackIn) -> FeedbackOut:
    # FIXME: retrieve the organization from the JWT token
    org_id = "fixme"
    # FIXME: retrieve the user from the JWT token
    return FeedbackRepository.create_feedback(org_id, feedback_in, "")


@router.get('/{feedback_id}')
async def get_feedback(feedback_id: str) -> FeedbackOut:
    # FIXME: retrieve the organization from the JWT token
    org_id = "fixme"
    feedback = FeedbackRepository.get_feedback(org_id, feedback_id)

    if feedback is None:
        raise HTTPException(status_code=404, detail='Feedback not found')

    return feedback
