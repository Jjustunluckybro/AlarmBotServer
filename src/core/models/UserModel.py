from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    """Model representing the telegram user!"""
    telegram_id: str
    user_name: str
    lang_code: str
    first_name: Optional[str]
    last_name: Optional[str]

