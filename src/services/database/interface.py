from abc import ABC, abstractmethod
from src.core.models.UserModel import UserModel
from src.core.models.AlarmModel import AlarmModel


class IDateBase(ABC):

    # --- User methods --- #
    @abstractmethod
    async def write_new_user(self, user: UserModel) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_id(self, user_id: str) -> None:
        raise NotImplementedError

    # --- Alarm methods --- #
    @abstractmethod
    async def write_new_alarm(self, alarm: AlarmModel) -> str:
        raise NotImplementedError

