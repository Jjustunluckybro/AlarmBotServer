import asyncio
import datetime

from fastapi import Depends

from src.core.models.AlarmModel import AlarmModel, AlarmStatuses
from src.infrastructure.alarms.db_interaction import get_all_queued_alarms
from src.services.database.interface import IDataBase
from src.utils.depends import get_db


async def check_queue_status(db: IDataBase = Depends(get_db)) -> None:
    ...
