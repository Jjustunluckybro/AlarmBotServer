from abc import ABC, abstractmethod
from src.core.models.UserModel import UserModel
from src.core.models.AlarmModel import AlarmModel, AlarmRouterModel, AlarmModelWrite
from src.core.models.ThemeModel import ThemeModel, ThemeModelWrite
from src.core.models.NoteModel import NoteModelWrite, NoteModel


class IDataBase(ABC):

    # --- User methods --- #
    @abstractmethod
    async def write_new_user(self, user: UserModel) -> str:
        """Write new user to db"""
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> UserModel:
        """
        Get user from db by id.
        If user not found, should raise DBNotFound exception
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_id(self, user_id: str) -> int:
        """
        delete user from db by id.
        If user not found, should raise DBNotFound exception
        """
        raise NotImplementedError

    @abstractmethod
    async def update_username(self, user_id: str, new_username: str) -> int:
        """
        Change username in db.
        If user not found, should raise DBNotFound exception
        """
        raise NotImplementedError

    #     # --- Alarm methods --- #
    @abstractmethod
    async def write_new_alarm(self, alarm: AlarmModelWrite) -> str:
        """Write new alarm to db"""
        raise NotImplementedError

    @abstractmethod
    async def get_alarm_by_id(self, alarm_id: str) -> AlarmModel:
        """Get alarm from db by id"""
        raise NotImplementedError

    @abstractmethod
    async def get_all_alarms_by_condition(self, condition: dict) -> list[AlarmModel]:
        """Get all alarms from db by condition"""
        raise NotImplementedError

    @abstractmethod
    async def update_alarm(self, alarm_id: str, new_data: dict) -> int:
        """Update alarm instance in db with new data"""
        raise NotImplementedError

    @abstractmethod
    async def delete_alarm_by_id(self, alarm_id: dict) -> int:
        """Delete single alarm from db by id"""
        raise NotImplementedError

    @abstractmethod
    async def delete_all_alarms_by_condition(self, condition: dict) -> int:
        """Delete many alarms by condition in db"""
        raise NotImplementedError

    #     # --- Themes methods --- #
    @abstractmethod
    async def write_new_theme(self, theme: ThemeModelWrite) -> str:
        """Write new theme to db"""
        raise NotImplementedError

    @abstractmethod
    async def get_theme_by_id(self, theme_id: str) -> ThemeModel:
        """Get theme from db by id"""
        raise NotImplementedError

    @abstractmethod
    async def get_all_themes_by_condition(self, condition: dict) -> list[ThemeModel]:
        """Get all themes!! from db by condition"""
        raise NotImplementedError

    @abstractmethod
    async def update_theme(self, theme_id: str, new_data: dict) -> int:
        """Update theme instance in db with new data"""
        raise NotImplementedError

    @abstractmethod
    def delete_theme_by_id(self, theme_id: str) -> int:
        """Delete single theme from db by id"""
        raise NotImplementedError

    @abstractmethod
    def delete_all_themes_by_condition(self, condition: dict) -> int:
        """Delete many themes by condition in db"""
        raise NotImplementedError

    # --- Notes methods --- #
    @abstractmethod
    async def write_new_note(self, note: NoteModelWrite) -> str:
        """Write new note to db"""
        raise NotImplementedError

    @abstractmethod
    async def get_note_by_id(self, note_id: str) -> NoteModel:
        """Get note from db by id"""
        raise NotImplementedError

    @abstractmethod
    async def get_all_notes_by_condition(self, condition: dict) -> list[NoteModelWrite]:
        """Get all notes from db by condition"""
        raise NotImplementedError

    @abstractmethod
    async def update_note(self, note_id: str, new_data: dict) -> int:
        """Update note instance in db with new data"""
        raise NotImplementedError

    @abstractmethod
    async def delete_note_by_id(self, note_id: str) -> int:
        """Delete single note from db by id"""
        raise NotImplementedError

    @abstractmethod
    async def delete_all_notes_by_condition(self, condition: dict) -> int:
        """Delete many notes by condition in db"""
        raise NotImplementedError
