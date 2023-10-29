from datetime import datetime
from enum import Enum
from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, Field, validator


class AlarmStatuses(str, Enum):
    READY = "READY"
    QUEUE = "QUEUE"
    FINISH = "FINISH"


class AlarmLinksModel(BaseModel):
    user_id: str
    parent_id: str

    @validator('parent_id')
    def parent_id_must_convert_to_object_id(cls, v):
        try:
            ObjectId(v)
            return v
        except InvalidId:
            raise ValueError(f"{v} is not a valid, it must be a 12-byte input or a 24-character hex string")


class AlarmTimesModel(BaseModel):
    creation_time: datetime
    next_notion_time: Optional[datetime]
    end_time: Optional[datetime]
    repeat_interval: Optional[int]


class AlarmModel(BaseModel):
    """Represent alarm entity in database"""
    id: str = Field(alias="_id")
    name: str
    description: Optional[str]
    is_repeatable: bool
    status: AlarmStatuses
    links: AlarmLinksModel
    times: AlarmTimesModel


class AlarmModelWrite(BaseModel):
    """Represent alarm entity to write in database"""
    name: str
    description: Optional[str]
    is_repeatable: bool
    status: AlarmStatuses
    links: AlarmLinksModel
    times: AlarmTimesModel


class AlarmRouterModel(BaseModel):
    """Represent alarm entity to router input"""
    name: str
    description: Optional[str]
    is_repeatable: bool
    links: AlarmLinksModel

    def convert_to_alarm_model_write(self, times: AlarmTimesModel, status: AlarmStatuses) -> AlarmModelWrite:
        return AlarmModelWrite(
            times=times.dict(),
            status=status,
            **self.dict()
        )
