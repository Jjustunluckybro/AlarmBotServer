from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CheckPointModel(BaseModel):
    text: str
    is_finish: bool


class NoteDataModel(BaseModel):
    text: str
    attachments: Optional[list]
    check_points: Optional[list[CheckPointModel]]


class NoteLinksModel(BaseModel):
    user_id: str
    theme_id: str


class NoteTimesModel(BaseModel):
    creation_time: datetime
    end_time: Optional[datetime]


class NoteModel(BaseModel):
    name: str
    links: NoteLinksModel
    data: NoteDataModel
    times: NoteTimesModel
