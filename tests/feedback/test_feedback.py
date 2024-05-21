from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from app.models.feedback import FeedbackIn
from app.repositories.feedback import FeedbackRepository


def test_feedback_create(
        dynamodb_client,
        test_client: TestClient
):
    feedback_in = FeedbackIn(
        title="Test",
        body="The body of the feedback",
        tags=["bug"],
        priority="high",
        sentiment=0
    )
    # feedback_out = FeedbackRepository.create_feedback(feedback_in)
    response = test_client.post('/feedback', json=jsonable_encoder(feedback_in.model_dump()))
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data and data['id'] is not None
    