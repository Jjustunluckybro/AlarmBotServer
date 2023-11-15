from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, Field, validator
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

    @validator('theme_id')
    def theme_id_must_convert_to_object_id(cls, v):
        try:
            ObjectId(v)
            return v
        except InvalidId:
            raise ValueError(f"{v} is not a valid, it must be a 12-byte input or a 24-character hex string")


class NoteTimesModel(BaseModel):
    creation_time: datetime
    end_time: Optional[datetime]


class NoteModel(BaseModel):
    id: str = Field(alias="_id")
    name: str
    links: NoteLinksModel
    data: NoteDataModel
    times: NoteTimesModel


class NoteModelWrite(BaseModel):
    name: str
    links: NoteLinksModel
    data: NoteDataModel
    times: NoteTimesModel

    def convert_to_note_model(self, note_id: str) -> NoteModel:
        return NoteModel(
            _id=note_id, **self.dict()
        )


class NoteRouterModel(BaseModel):
    name: str
    links: NoteLinksModel
    data: NoteDataModel

    def convert_to_note_model_write(self, times: NoteTimesModel) -> NoteModelWrite:
        return NoteModelWrite(
            times=times.dict(),
            **self.dict()
        )
