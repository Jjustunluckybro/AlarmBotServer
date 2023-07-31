from src.core.models.UserModel import UserModel

from src.services.database.interface import IDataBase


async def get_user_from_db(user_id: str, db: IDataBase) -> UserModel:
    user = await db.get_user_by_id(user_id)
    return user


async def write_user_to_db(user: UserModel, db: IDataBase) -> str:
    user_id = await db.write_new_user(user)
    return user_id


async def update_username_in_db(user_id: str, new_name: str, db: IDataBase) -> int:
    change_counter = await db.update_username(user_id, new_name)
    return change_counter


async def delete_user_from_db(user_id: str, db: IDataBase) -> int:
    deleted_count = await db.delete_user_by_id(user_id)
    return deleted_count
