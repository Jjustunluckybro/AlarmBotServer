import motor.motor_asyncio
from beanie import Document, init_beanie
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

from src.services.database.mongo_db import MongoAPI
from src.utils.config import TEST_DB_USER_PASSWORD

DATABASE_URL = MongoAPI.get_connection_string(TEST_DB_USER_PASSWORD)
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
backend_users_db = client["UserStorage"]


class BackendUser(BeanieBaseUser, Document):
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    tags: list[str] = []


async def get_user_db():
    yield BeanieUserDatabase(BackendUser)


async def init_backend_users_db():
    await init_beanie(
        database=backend_users_db,
        document_models=[
            BackendUser,
        ],
    )
