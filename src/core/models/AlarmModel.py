from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


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
    name: str
    description: Optional[str]
    is_repeatable: bool
    status: AlarmStatuses
    links: AlarmLinksModel
    times: AlarmTimesModel
