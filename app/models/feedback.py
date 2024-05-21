from typing import List, Literal
from uuid import uuid4
from pydantic import BaseModel


class FeedbackBase(BaseModel):
    title: str
    body: str
    tags: List[str]
    priority: Literal["low", "medium", "high"]
    sentiment: int

class FeedbackIn(FeedbackBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "This app is great!",
                    "body": "wow **looking good**, keep going!",
                    "tags": ['bug'],
                    "priority": "high",
                    "sentiment": 0
                }, {
                    "title": "Dark mode",
                    "body": "we want dark mode",
                    "tags": ['feature_request'],
                    "priority": "high",
                    "sentiment": 1
                }
            ]
        }
    }

    def get_keys(self, id: str):
        return {
            'PK': {'S': 'feedback'},
            'SK': {'S': f'feedback#{id}'},
        }

    def for_db(self, id: str):
        return self.get_keys(id) | {
            "Title": {"S": self.title},
            "Body": {"S": self.body},
            "Tags": {"SS": self.tags},
            "Priority": {"S": self.priority},
            "Sentiment": {"N": str(self.sentiment)}
        }



class FeedbackOut(FeedbackBase):
    id: str