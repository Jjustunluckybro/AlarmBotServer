from typing import Optional

from bson import ObjectId
from fastapi_users import schemas


class UserRead(schemas.BaseUser[ObjectId]):
    _id: ObjectId
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    tags: list[str] = []


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    tags: list[str] = []
