from typing import Optional
from pydantic import BaseModel, Field


class ThemesLinksModel(BaseModel):
    user_id: str


class ThemeModel(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: Optional[str]
    links: ThemesLinksModel


class ThemeModelWrite(BaseModel):
    name: str
    description: Optional[str]
    links: ThemesLinksModel

    def convert_to_theme_model(self, theme_id: str) -> ThemeModel:
        return ThemeModel(_id=theme_id, **self.dict())
