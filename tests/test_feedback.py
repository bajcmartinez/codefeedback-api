from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from app.models.feedback import FeedbackIn, FeedbackStatus


def test_feedback_create(
        dynamodb_client,
        test_client: TestClient
):
    feedback_in = FeedbackIn(
        board_id="test",
        title="Test",
        body="The body of the feedback",
        internal_status=FeedbackStatus.reviewing,
        status="In Review"
    )
    # feedback_out = FeedbackRepository.create_feedback(feedback_in)
    response = test_client.post('/feedback', json=jsonable_encoder(feedback_in.model_dump()))
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data and data['id'] is not None


def test_feedback_get(
        dynamodb_client,
        test_client: TestClient
):
    feedback_in = FeedbackIn(
        board_id="test",
        title="Test",
        body="The body of the feedback",
        internal_status=FeedbackStatus.reviewing,
        status="In Review"
    )
    # feedback_out = FeedbackRepository.create_feedback(feedback_in)
    response = test_client.post('/feedback', json=jsonable_encoder(feedback_in.model_dump()))
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data and data['id'] is not None

    feedback_id = data['id']
    response = test_client.get(f'/feedback/{feedback_id}')
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data and data['id'] == feedback_id


def test_feedback_get_non_existent(
        dynamodb_client,
        test_client: TestClient
):
    response = test_client.get(f'/feedback/not-existent')
    assert response.status_code == 404
