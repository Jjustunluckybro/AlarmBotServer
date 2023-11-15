from src.core.models.AlarmModel import AlarmModel, AlarmStatuses, AlarmRouterModel, AlarmTimesModel
from src.infrastructure.exceptions import AlarmNotRepeatable, UnexpectedInfrastructureException

from src.services.database.interface import IDataBase
from datetime import datetime, timedelta


async def get_alarm_from_db(alarm_id: str, db: IDataBase) -> AlarmModel:
    alarm = await db.get_alarm_by_id(alarm_id)
    return alarm


async def write_alarm_to_db(alarm: AlarmRouterModel, db: IDataBase, next_notion_time: datetime,
                            repeat_interval: int | None) -> str:
    alarm_id = await db.write_new_alarm(alarm.convert_to_alarm_model_write(
        status=AlarmStatuses.QUEUE.value,
        times=AlarmTimesModel(
            creation_time=datetime.now(),
            next_notion_time=next_notion_time,
            repeat_interval=repeat_interval,
            end_time=None
        )))
    return alarm_id


async def get_all_alarm_by_condition(condition: dict, db: IDataBase) -> [AlarmModel]:
    alarms = await db.get_all_alarms_by_condition(condition)
    return alarms


async def get_all_queued_alarms(db: IDataBase) -> list[AlarmModel]:
    alarms = await get_all_alarm_by_condition({"status": AlarmStatuses.QUEUE.value}, db)
    return alarms


async def postpone_repeatable_alarm(alarm_id, db: IDataBase) -> datetime:
    alarm = await db.get_alarm_by_id(alarm_id)
    if not alarm.is_repeatable:
        raise AlarmNotRepeatable("Alarm must be repeatable")
    else:
        new_next_notion_time = datetime.now() + timedelta(minutes=alarm.times.repeat_interval)
        result = await db.update_alarm(
            alarm_id=alarm_id,
            new_data={"status": AlarmStatuses.QUEUE.value, "times.next_notion_time": new_next_notion_time}
        )
        if result:
            return new_next_notion_time
        else:
            raise UnexpectedInfrastructureException()


async def update_alarm(alarm_id: str, new_data: dict, db: IDataBase) -> int:
    update_count = await db.update_alarm(alarm_id, new_data)
    return update_count


async def delete_alarm(alarm_id, db: IDataBase) -> int:
    deleted_count = await db.delete_alarm_by_id(alarm_id)
    return deleted_count


async def delete_all_alarms_by_condition(condition: dict, db: IDataBase) -> int:
    deleted_count = await db.delete_all_alarms_by_condition(condition)
    return deleted_count
