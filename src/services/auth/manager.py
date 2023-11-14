from typing import Optional, Any

from bson import ObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager

from src.services.auth.database import BackendUser, get_user_db
from src.services.database.database_exceptions import InvalidIdException
from src.utils.config import VERIFICATION_TOKEN_SECRET


class UserManager(BaseUserManager[BackendUser, ObjectId]):
    reset_password_token_secret = VERIFICATION_TOKEN_SECRET
    verification_token_secret = VERIFICATION_TOKEN_SECRET

    def parse_id(self, value: Any) -> ObjectId:
        if isinstance(value, ObjectId):
            return value
        try:
            return ObjectId(value)
        except ValueError as e:
            raise InvalidIdException

    async def on_after_register(self, user: BackendUser, request: Optional[Request] = None):
        ...


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
