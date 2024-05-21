from datetime import datetime, timezone

import boto3
from ksuid import Ksuid

from app.models.feedback import FeedbackIn, FeedbackOut, Feedback, FeedbackKeys

table_name = 'codefeedback'


class FeedbackRepository:

    @staticmethod
    def create_feedback(feedback_in: FeedbackIn, user_id: str) -> FeedbackOut:
        feedback = Feedback.model_validate(feedback_in.model_dump() | {
            "id": str(Ksuid()),
            "created_date": datetime.now(timezone.utc),
            "created_by": user_id,
            "updated_date": datetime.now(timezone.utc),
            "updated_by": user_id
        })

        db_client = boto3.client('dynamodb')
        db_client.put_item(
            TableName=table_name,
            Item=feedback.for_db(),
            ConditionExpression='attribute_not_exists(PK)',
        )

        return FeedbackOut.model_validate(feedback.model_dump())

    @staticmethod
    def get_feedback(feedback_id: str) -> FeedbackOut | None:
        db_client = boto3.client('dynamodb')
        response = db_client.get_item(
            TableName=table_name,
            Key=FeedbackKeys(id=feedback_id).get_keys()
        )

        if 'Item' not in response:
            return None

        return FeedbackOut.from_db(response['Item'])
