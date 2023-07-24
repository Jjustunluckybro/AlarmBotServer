from pydantic import BaseModel, Field


class UserModel(BaseModel):
    telegram_id: str
    user_name: str
