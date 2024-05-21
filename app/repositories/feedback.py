from uuid import uuid4
import boto3

from app.models.feedback import FeedbackIn, FeedbackOut


class FeedbackRepository:
    
    @staticmethod
    def create_feedback(feedback: FeedbackIn) -> FeedbackOut:
        id = uuid4()

        db_client = boto3.client('dynamodb')
        db_client.put_item(
            TableName="codefeedback",
            Item=feedback.for_db(id)
        )

        return FeedbackOut.model_validate(feedback.model_dump() | {"id":str(id)})