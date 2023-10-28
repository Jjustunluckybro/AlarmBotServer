from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class AlarmStatuses(str, Enum):
    READY = "READY"
    QUEUE = "QUEUE"
    STOPPED = "STOPPED"


class AlarmLinksModel(BaseModel):
    user_id: str
    parent_id: str


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
    status: AlarmStatuses
    links: AlarmLinksModel

    def convert_to_alarm_model_write(self, times: AlarmTimesModel) -> AlarmModelWrite:
        return AlarmModelWrite(
            times=times.dict(),
            **self.dict()
        )
