from datetime import datetime, timezone

import boto3
from ksuid import Ksuid

from app.models.feedback import FeedbackIn, FeedbackOut, Feedback, FeedbackKeys

table_name = 'codefeedback'


class FeedbackRepository:

    @staticmethod
    def create_feedback(org_id: str, feedback_in: FeedbackIn, user_id: str) -> FeedbackOut:
        curr_date = datetime.now(timezone.utc)
        feedback = Feedback.model_validate(feedback_in.model_dump() | {
            "org_id": org_id,
            "id": str(Ksuid()),
            "created_date": curr_date,
            "created_by": user_id,
            "updated_date": curr_date,
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
    def get_feedback(org_id: str, feedback_id: str) -> FeedbackOut | None:
        db_client = boto3.client('dynamodb')
        response = db_client.get_item(
            TableName=table_name,
            Key=FeedbackKeys(
                org_id=org_id,
                id=feedback_id,
            ).get_keys()
        )

        if 'Item' not in response:
            return None

        return FeedbackOut.from_db(response['Item'])


    @staticmethod
    def delete_feedback(org_id: str, feedback_id: str) -> None:
        db_client = boto3.client('dynamodb')
        response = db_client.delete_item(
            TableName=table_name,
            Key=FeedbackKeys(
                org_id=org_id,
                id=feedback_id,
            ).get_keys()
        )
