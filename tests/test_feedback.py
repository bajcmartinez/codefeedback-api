from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from app.models.feedback import FeedbackIn, FeedbackStatus


def get_new_feedback_in() -> FeedbackIn:
    return FeedbackIn(
        board_id="test",
        title="Test",
        body="The body of the feedback",
        internal_status=FeedbackStatus.reviewing,
        status="In Review"
    )


def test_feedback_create(
        dynamodb_client,
        test_client: TestClient
):
    feedback_in = get_new_feedback_in()
    response = test_client.post('/feedback', json=jsonable_encoder(feedback_in.model_dump()))
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data and data['id'] is not None


def test_feedback_get(
        dynamodb_client,
        test_client: TestClient
):
    # Create feedback
    feedback_in = get_new_feedback_in()
    response = test_client.post('/feedback', json=jsonable_encoder(feedback_in.model_dump()))
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data and data['id'] is not None

    feedback_id = data['id']
    org_id = data['org_id']

    # Get the feedback recently created to make sure it exists
    response = test_client.get(f'/feedback/{org_id}/{feedback_id}')
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data and data['id'] == feedback_id


def test_feedback_get_non_existent(
        dynamodb_client,
        test_client: TestClient
):
    response = test_client.get(f'/feedback/org/not-existent')
    assert response.status_code == 404


def test_feedback_delete(
        dynamodb_client,
        test_client: TestClient
):
    # Create feedback
    feedback_in = get_new_feedback_in()
    response = test_client.post('/feedback', json=jsonable_encoder(feedback_in.model_dump()))
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data and data['id'] is not None

    feedback_id = data['id']
    org_id = data['org_id']

    # delete the feedback
    response = test_client.delete(f'/feedback/{org_id}/{feedback_id}')
    assert response.status_code == 204

    # make sure it's deleted
    response = test_client.get(f'/feedback/{org_id}/{feedback_id}')
    assert response.status_code == 404
