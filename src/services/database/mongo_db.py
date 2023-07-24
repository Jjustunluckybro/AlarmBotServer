import asyncio
import logging
from typing import NamedTuple, Any

from pymongo.errors import DuplicateKeyError
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.models.UserModel import UserModel
from src.services.database.database_exceptions import DBNotFound, DuplicateKey
from src.services.database.interface import IDateBase

logger = logging.getLogger("app.database_api.mongo")


class MongoAPI(IDateBase):
    _client = AsyncIOMotorClient
    _db = AsyncIOMotorClient  # ??
    _collections = dict

    def connect_to_db(self, connection_string: str, is_test: bool = False) -> bool:
        try:
            # Connect client
            self._client = AsyncIOMotorClient(connection_string)

            # Connect db
            # self._db = self._client.Test if is_test else self._client.Prod
            self._db = self._client.Alarmbot

            class Collections(NamedTuple):
                user: Any
                themes: Any
                alarms: Any
                notes: Any

            # Connect collections
            self._collections = Collections(
                user=self._db.Users,
                themes=self._db.Themes,
                alarms=self._db.Alarms,
                notes=self._db.Notes
            )

        except Exception as err:
            logger.critical(f"Db connection error: {str(err)}")
            return False
        logger.info("Successfully connect to MongoDb")
        return True

    @staticmethod
    def remove_mongo_primary_id_from_data(data: dict) -> dict:
        """Removing "_id" key from data"""
        if "_id" in data:
            data.pop("_id")
        return data

    @staticmethod
    def change_telegram_id_field_to_id_field(data: dict) -> dict:
        """Changing "telegram_id" key to "_id" key"""
        telegram_id = "telegram_id"
        if telegram_id in data:
            value = data.pop(telegram_id)
            data["_id"] = value
        return data

    @staticmethod
    def change_id_field_to_telegram_id(data: dict) -> dict:
        """"""
        _id = "_id"
        if _id in data:
            value = data.pop(_id)
            data["telegram_id"] = value
        return data

    # --- Users --- #
    async def get_user_by_id(self, user_id: str) -> UserModel:
        """Get user object from user collection Mongo database"""
        user = await self._collections.user.find_one(user_id)
        if user is None:
            logger.info(f"User with id {user_id} not found")
            raise DBNotFound("User not found")
        user = self.change_id_field_to_telegram_id(user)
        user = UserModel.parse_obj(user)
        return user

    async def write_new_user(self, user: UserModel) -> str:
        """Add new user to user collection Mongo database"""
        user_dict = self.change_telegram_id_field_to_id_field(user.dict())
        try:
            inserted_obj = await self._collections.user.insert_one(user_dict)
        except DuplicateKeyError:
            logger.info(f"User duplicat with id {user.telegram_id}")
            raise DuplicateKey("User duplicat key")
        return str(inserted_obj.inserted_id)

    async def update_username(self, user_id: str, new_username: str) -> int:
        """
        Change username field of user object in Mongo database
        :param user_id: user "_id" value
        :param new_username:
        :return: how many users objects has changed
        """
        updated_obj = await self._collections.user.update_one({"_id": user_id},
                                                              {"$set": {"user_name": new_username}})
        return updated_obj.modified_count

    async def delete_user_by_id(self, user_id: str) -> int:
        """Delete user from User collection by telegram_id"""
        delete_obj = await self._collections.user.delete_one({"telegram_id": user_id})
        if delete_obj.deleted_count == 0:
            logger.info(f"User with id {user_id} not found")
            raise DBNotFound("User not found")
        return delete_obj.deleted_count
