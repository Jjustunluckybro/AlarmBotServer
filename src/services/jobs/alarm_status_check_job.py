import datetime
from datetime import datetime as dt
from logging import getLogger

from src.core.models.AlarmModel import AlarmStatuses
from src.infrastructure.alarms.db_interaction import get_all_queued_alarms, update_alarm
from src.services.database.database_exceptions import DBNotFound
from src.services.database.interface import IDataBase
from src.utils.depends import get_db

logger = getLogger(__name__)


async def check_queue_status() -> None:
    logger.info("Start job 'check_queue_status'")
    db: IDataBase = get_db()
    try:
        alarms = await get_all_queued_alarms(db)
    except DBNotFound:
        return
    else:
        for alarm in alarms:
            user = await db.get_user_by_id(alarm.links.user_id)
            user_tz = user.timezone
            due_time = dt.now() + datetime.timedelta(hours=user_tz)
            next_notion_time = alarm.times.next_notion_time
            if (next_notion_time is not None) and (next_notion_time < due_time):
                await update_alarm(
                    alarm_id=alarm.id,
                    new_data={"status": AlarmStatuses.READY.value},
                    db=db
                )
    finally:
        logger.info("check_queue_status job done")
