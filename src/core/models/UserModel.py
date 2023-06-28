from pydantic import BaseModel


class UserModel(BaseModel):
    telegram_id: str
    user_name: str
