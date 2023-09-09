from typing import Optional
from pydantic import BaseModel, Field


class ThemesLinksModel(BaseModel):
    user_id: str


class ThemeModel(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: Optional[str]
    links: ThemesLinksModel


class ThemeModelForCreate(BaseModel):
    name: str
    description: Optional[str]
    links: ThemesLinksModel
