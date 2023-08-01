from typing import Optional
from pydantic import BaseModel


class ThemesLinksModel(BaseModel):
    user_id: str


class ThemeModel(BaseModel):
    name: str
    description: Optional[str]
    links: ThemesLinksModel
