from datetime import datetime as dt


from src.core.models.AlarmModel import AlarmStatuses
from src.infrastructure.alarms.db_interaction import get_all_queued_alarms, update_alarm
from src.services.database.database_exceptions import DBNotFound
from src.services.database.interface import IDataBase
from src.utils.depends import get_db


async def check_queue_status() -> None:
    db: IDataBase = get_db()
    try:
        alarms = await get_all_queued_alarms(db)
    except DBNotFound as err:
        return
    else:
        for alarm in alarms:
            if alarm.times.next_notion_time is not None and alarm.times.next_notion_time < dt.now():
                await update_alarm(
                    alarm_id=alarm.id,
                    new_data={"status": AlarmStatuses.READY.value},
                    db=db
                )
