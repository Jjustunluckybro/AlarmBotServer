from src.core.models.UserModel import UserModel

from src.services.database.interface import IDateBase


async def get_user_from_db(user_id: str, db: IDateBase) -> UserModel:
    user = await db.get_user_by_id(user_id)
    return user


async def write_user_to_db(user: UserModel, db: IDateBase) -> str:
    user_id = await db.write_new_user(user)
    return user_id


async def update_username_in_db(user_id: str, new_name: str, db: IDateBase) -> int:
    ...


async def delete_user_from_db(user_id: str, db: IDateBase) -> int:
    ...
