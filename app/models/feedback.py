from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel


class FeedbackStatus(str, Enum):
    reviewing = "Reviewing"
    planned = "Planned"
    active = "Active"
    Completed = 'Completed'
    Canceled = 'Canceled'


class FeedbackBase(BaseModel):
    org_id: str
    board_id: str
    title: str
    body: str
    tags: List[str] | None = []
    value: int | None = None
    effort: int | None = None
    internal_status: str
    status: str
    comments_disabled: bool | None = False
    sentiment: float | None = 0
    up_votes: int | None = 0
    down_votes: int | None = 0
    comments_count: int | None = 0
    eta: datetime | None = None
    is_spam: bool | None = False


class FeedbackIn(FeedbackBase):
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "org_id": "acme",
                "board_id": "1",
                "title": "This app is great!",
                "body": "wow **looking good**, keep going!",
                "status": "status_id",
            }]
        }
    }


class FeedbackKeys(BaseModel):
    id: str

    def get_pk(self):
        return {'PK': {'S': f'FEEDBACK#{self.id}'}}

    def get_sk(self):
        return {'SK': {'S': f'FEEDBACK#{self.id}'}}

    def get_keys(self):
        return self.get_pk() | self.get_sk()

    def get_gsi1_pk(self):
        return {'GSI1PK': {'S': f'ORG#{self.org_id}#{self.board_id}'}}

    def get_gsi1_sk(self):
        return {'GSI1SK': {'S': f'FEEDBACK#{self.id}'}}

    def get_gsi1(self):
        return self.get_gsi1_pk() | self.get_gsi1_sk()

    def get_gsi2_pk(self):
        return {'GSI2PK': {'S': f'ORG#{self.org_id}'}}

    def get_gsi2_sk(self):
        return {'GSI2SK': {'S': f'FEEDBACK#{self.id}'}}

    def get_gsi2(self):
        return self.get_gsi2_pk() | self.get_gsi2_sk()


class Feedback(FeedbackBase, FeedbackKeys):
    created_date: datetime
    created_by: str
    updated_date: datetime
    updated_by: str

    def for_db(self):
        return (
                self.get_keys() | self.get_gsi1() | self.get_gsi2() |
                {
                    "Title": {"S": self.title},
                    "Body": {"S": self.body},
                    "Tags": {"SS": self.tags},
                    "InternalStatus": {"S": self.internal_status},
                    "Status": {"S": self.status},
                    "CommentsDisabled": {"BOOL": self.comments_disabled},
                    "Sentiment": {"N": str(self.sentiment)},
                    "UpVotes": {"N": str(self.up_votes)},
                    "DownVotes": {"N": str(self.down_votes)},
                    "CommentsCount": {"N": str(self.comments_count)},
                    "ETA": {"S": str(self.comments_count)},
                    'Type': {'S': 'FEEDBACK'},
                    "CreatedDate": {"S": str(self.created_date)},
                    "CreatedBy": {"S": str(self.created_by)},
                    "UpdatedDate": {"S": str(self.updated_date)},
                    "UpdatedBy": {"S": str(self.updated_by)},
                } |
                ({"Value": self.value} if self.value is not None else {}) |
                ({"Effort": self.effort} if self.effort is not None else {})
        )

    @staticmethod
    def from_db(attributes):
        return FeedbackOut(
            id=attributes['PK']['S'].split('#')[1],
            org_id=attributes['GSI1PK']['S'].split('#')[1],
            board_id=attributes['GSI1PK']['S'].split('#')[2],
            title=attributes['Title']['S'],
            body=attributes['Body']['S'],
            tags=attributes['Tags']['SS'],
            value=attributes['VALUE']['S'] if 'VALUE' in attributes else None,
            effort=attributes['EFFORT']['S'] if 'EFFORT' in attributes else None,
            internal_status=attributes['InternalStatus']['S'],
            status=attributes['Status']['S'],
            comments_disabled=attributes['CommentsDisabled']['BOOL'],
            sentiment=attributes['Sentiment']['N'],
            up_votes=attributes['UpVotes']['N'],
            down_votes=attributes['DownVotes']['N'],
            comments_count=attributes['CommentsCount']['N'],
            eta=attributes['ETA']['S'],
            created_date=attributes['CreatedDate']['S'],
            created_by=attributes['CreatedBy']['S'],
            updated_date=attributes['UpdatedDate']['S'],
            updated_by=attributes['UpdatedBy']['S'],
        )


class FeedbackOut(Feedback):
    pass
