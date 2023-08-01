from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette import status

from src.core.models.AlarmModel import AlarmModel, AlarmStatuses
from src.infrastructure.alarms import db_interaction
from src.services.database.database_exceptions import DBNotFound, DuplicateKey, InvalidIdException
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
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.post("/create_alarm", status_code=status.HTTP_201_CREATED)
async def create_alarm(r: Request, alarm: AlarmModel) -> dict:
    db: IDataBase = r.app.state.db
    alarm_id = await db_interaction.write_alarm_to_db(alarm, db)
    return {"alarm_id": alarm_id}


@router.post("/get_by_condition", status_code=status.HTTP_200_OK)
async def get_by_condition(r: Request, condition: dict) -> list[AlarmModel]:
    db: IDataBase = r.app.state.db
    try:
        alarms = await db_interaction.get_all_alarm_by_condition(condition, db)
        return alarms
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.patch("/update_alarm/{alarm_id}", status_code=status.HTTP_200_OK)
async def update_alarm(r: Request, alarm_id: str, new_data: dict) -> dict:
    """Update alarm field, don't use to change status"""
    db: IDataBase = r.app.state.db
    try:
        update_count = await db_interaction.update_alarm(alarm_id, new_data, db)
        return {"update_count": update_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.patch("/update_alarm_status/{alarm_id}", status_code=status.HTTP_200_OK)
async def update_alarm_status(r: Request, alarm_id: str, new_status: AlarmStatuses) -> dict:
    """Update alarm status"""
    db: IDataBase = r.app.state.db
    try:
        update_count = await db_interaction.update_alarm(alarm_id=alarm_id,
                                                         db=db,
                                                         new_data={"status": new_status.value})
        return {"update_count": update_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.delete("/delete_alarm_by_id/{alarm_id}", status_code=status.HTTP_200_OK)
async def delete_alarm(r: Request, alarm_id: str) -> dict:
    db: IDataBase = r.app.state.db
    try:
        deleted_count = await db_interaction.delete_alarm(alarm_id, db)
        return {"deleted_count": deleted_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.delete("/delete_all_alarms_by_condition", status_code=status.HTTP_200_OK)
async def delete_all_alarms_by_condition(r: Request, condition: dict) -> dict:
    db: IDataBase = r.app.state.db
    deleted_count = await db_interaction.delete_all_alarms_by_condition(condition, db)
    return {"deleted_count": deleted_count}
