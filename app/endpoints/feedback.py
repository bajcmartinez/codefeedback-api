from fastapi import APIRouter, HTTPException, Security

from app.models.feedback import FeedbackIn, FeedbackOut
from app.repositories.feedback import FeedbackRepository
from utils.auth import auth

router = APIRouter(prefix='/feedback', tags=['Feedback'])


@router.post('', status_code=201)
async def create_feedback(feedback_in: FeedbackIn, token_payload=Security(auth.get_authenticated_user)) -> FeedbackOut:
    org_id = token_payload['org_id']
    user_id = token_payload['sub']
    return FeedbackRepository.create_feedback(org_id, feedback_in, user_id)


@router.get('/{org_id}/{feedback_id}')
async def get_feedback(org_id: str, feedback_id: str) -> FeedbackOut:
    feedback = FeedbackRepository.get_feedback(org_id, feedback_id)

    if feedback is None:
        raise HTTPException(status_code=404, detail='Feedback not found')

    return feedback


@router.delete('/{org_id}/{feedback_id}', status_code=204)
async def delete_feedback(org_id: str, feedback_id: str) -> None:
    FeedbackRepository.delete_feedback(org_id, feedback_id)
