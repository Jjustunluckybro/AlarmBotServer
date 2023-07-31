from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette import status

from src.core.models.AlarmModel import AlarmModel
from src.infrastructure.alarms import db_interaction
# from src.infrastructure.alarms.db_interaction import (get_alarm_from_db, write_alarm_to_db, get_all_alarm_by_condition,
#                                                       update_alarm)
from src.services.database.database_exceptions import DBNotFound, DuplicateKey
from src.services.database.interface import IDataBase

router = APIRouter(
    prefix="/alarms",
    tags=["alarms"]
)


@router.get("/get_alarm/{alarm_id}", status_code=status.HTTP_200_OK)
async def get_alarm(r: Request, alarm_id: str) -> AlarmModel:
    db: IDataBase = r.app.state.db
    try:
        alarm = await db_interaction.get_alarm_from_db(alarm_id, db)
        return alarm
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/create_alarm", status_code=status.HTTP_201_CREATED)
async def create_alarm(r: Request, alarm: AlarmModel) -> str:
    db: IDataBase = r.app.state.db
    try:
        alarm_id = await db_interaction.write_alarm_to_db(alarm, db)
        return alarm_id
    except DuplicateKey as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.post("/get_by_condition", status_code=status.HTTP_200_OK)
async def get_by_condition(r: Request, condition: dict) -> list[AlarmModel]:
    db: IDataBase = r.app.state.db
    alarms = await db_interaction.get_all_alarm_by_condition(condition, db)
    return alarms


@router.patch("/update_alarm", status_code=status.HTTP_200_OK)
async def update_alarm(r: Request, alarm_id: str, new_data: dict) -> int:
    """Update alarm field, don't use to change status"""
    db: IDataBase = r.app.state.db
    try:
        update_count = await db_interaction.update_alarm(alarm_id, new_data, db)
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    return update_count
