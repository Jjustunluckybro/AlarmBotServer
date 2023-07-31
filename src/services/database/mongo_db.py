import asyncio
import logging
from abc import ABC
from typing import NamedTuple, Any

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.models.AlarmModel import AlarmModel, AlarmStatuses
from src.core.models.UserModel import UserModel
from src.services.database.database_exceptions import DBNotFound, DuplicateKey
from src.services.database.interface import IDataBase

logger = logging.getLogger("app.database_api.mongo")


class MongoAPI(IDataBase):
    _client = AsyncIOMotorClient
    _db = AsyncIOMotorClient  # ??
    _collections = dict

    def connect_to_db(self, password: str) -> bool:
        try:
            # Connect client
            self._client = AsyncIOMotorClient(self.get_connection_string(password))

            # Connect db
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
    def get_connection_string(password: str) -> str:
        return f"mongodb+srv://admin:{password}@tgnoteapp.fsdy0bs.mongodb.net/?retryWrites=true&w=majority"

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

    @staticmethod
    def change_id_type(_id: str | ObjectId) -> ObjectId | str:
        """"""
        if isinstance(_id, str):
            return ObjectId(_id)
        return str(_id)

    @staticmethod
    def change_alarm_status_type(data: AlarmModel) -> dict:
        result = data.dict()
        result["status"] = data.status.value
        return result

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
        if updated_obj.modified_count == 0:
            raise DBNotFound("User not found")
        return updated_obj.modified_count

    async def delete_user_by_id(self, user_id: str) -> int:
        """Delete user from User collection by telegram_id"""
        delete_obj = await self._collections.user.delete_one({"telegram_id": user_id})
        if delete_obj.deleted_count == 0:
            logger.info(f"User with id {user_id} not found")
            raise DBNotFound("User not found")
        return delete_obj.deleted_count

    # --- Alarms --- #
    async def write_new_alarm(self, alarm: AlarmModel) -> str:
        """Add new alarm to Alarm collection Mongo database,
        If alarm with id already exist, rise DuplicateKey exception"""
        alarm_dict = self.change_alarm_status_type(alarm)
        try:
            inserted_obj = await self._collections.alarms.insert_one(alarm_dict)
        except DuplicateKeyError:
            logger.info(f"Alarm duplicate: {alarm}")
            raise DuplicateKey("Alarm duplicate key")
        return str(inserted_obj.inserted_id)

    async def get_alarm_by_id(self, alarm_id: str) -> AlarmModel:
        """Get alarm object from Alarm collection Mongo database
        If no alarm match id, raise DBNotFound exception"""
        alarm_id = self.change_id_type(alarm_id)
        alarm = await self._collections.alarms.find_one(alarm_id)
        if alarm is None:
            logger.info(f"Alarm with id {alarm_id} not found")
            raise DBNotFound("Alarm not found")
        alarm = self.remove_mongo_primary_id_from_data(alarm)
        alarm = AlarmModel.parse_obj(alarm)
        return alarm

    async def get_all_alarms_by_condition(self, condition: dict) -> list[AlarmModel]:
        """Get all alarms match condition, if no matches, raise DBNotFound exception"""
        alarms = self._collections.alarms.find(condition)
        result = list()
        for alarm in await alarms.to_list(length=100):
            result.append(AlarmModel.parse_obj(alarm))
        if not len(result):
            raise DBNotFound("Alarms match condition not found")
        return result

    async def update_alarm(self, alarm_id: str, new_data: dict) -> int:
        """Update alarm fields of Mongo database object,"""
        update_obj = await self._collections.alarms.update_one({"_id": self.change_id_type(alarm_id)},
                                                               {"$set": new_data})
        if update_obj.modified_count == 0:
            raise DBNotFound("Alarm not found")
        return update_obj.modified_count

    async def delete_alarm_by_id(self, alarm_id: dict) -> int:
        """"""
        deleted_obj = await self._collections.alarms.delete_one({"_id": alarm_id})
        if deleted_obj.delete_count == 0:
            raise DBNotFound(f"Alarm with id {alarm_id} not found")
        return deleted_obj.delete_count

    async def delete_all_alarms_by_condition(self, condition: dict) -> int:
        ...
