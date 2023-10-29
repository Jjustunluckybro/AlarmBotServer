import datetime

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from src.core.models.AlarmModel import AlarmModel, AlarmStatuses, AlarmRouterModel, AlarmLinksModel
from src.infrastructure.alarms import db_interaction
from src.infrastructure.exceptions import AlarmNotRepeatable, UnexpectedInfrastructureException
from src.utils.depends import get_db
from src.services.database.database_exceptions import DBNotFound, InvalidIdException
from src.services.database.interface import IDataBase

router = APIRouter(
    prefix="/alarms",
    tags=["alarms"]
)


@router.get("/get_alarm/{alarm_id}", status_code=status.HTTP_200_OK)
async def get_alarm(alarm_id: str, db: IDataBase = Depends(get_db)) -> AlarmModel:
    try:
        alarm = await db_interaction.get_alarm_from_db(alarm_id, db)
        return alarm
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.get("/get_all_alarm_by_parent_id/{parent_id}", status_code=status.HTTP_200_OK)
async def get_all_alarms_by_parent_id(parent_id: str, db: IDataBase = Depends(get_db)) -> list[AlarmModel]:
    try:
        AlarmLinksModel.parent_id_must_convert_to_object_id(parent_id)  # Validate Parent id
        alarms = await db_interaction.get_all_alarm_by_condition(
            {"links.parent_id": parent_id}, db
        )
        return alarms
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.get("/get_all_user_alarms/{user_id}", status_code=status.HTTP_200_OK)
async def get_all_user_alarms(user_id, db: IDataBase = Depends(get_db)) -> list[AlarmModel]:
    try:
        alarms = await db_interaction.get_all_alarm_by_condition(
            {"links.user_id": user_id}, db
        )
        return alarms
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.post("/create_alarm", status_code=status.HTTP_201_CREATED)
async def create_alarm(alarm: AlarmRouterModel,
                       next_notion_time: datetime.datetime,
                       repeat_interval: int | None = None,
                       db: IDataBase = Depends(get_db)) -> str:
    alarm_id = await db_interaction.write_alarm_to_db(alarm, db, next_notion_time=next_notion_time,
                                                      repeat_interval=repeat_interval)
    return alarm_id


@router.patch("/postpone_repeatable_alarm/{alarm_id}", status_code=200)
async def get_all_user_ready_alarms(alarm_id: str, db: IDataBase = Depends(get_db)) -> dict:
    try:
        new_next_notion_time = await db_interaction.postpone_repeatable_alarm(alarm_id, db)
        return {"next_notion_time": new_next_notion_time}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except AlarmNotRepeatable as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except UnexpectedInfrastructureException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update_alarm/{alarm_id}", status_code=status.HTTP_200_OK)
async def update_alarm(alarm_id: str, new_data: dict, db: IDataBase = Depends(get_db)) -> dict:
    """Update alarm field, don't use to change status"""
    try:
        update_count = await db_interaction.update_alarm(alarm_id, new_data, db)
        return {"update_count": update_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.patch("/update_alarm_status/{alarm_id}", status_code=status.HTTP_200_OK)
async def update_alarm_status(alarm_id: str, new_status: AlarmStatuses,
                              db: IDataBase = Depends(get_db)) -> dict:
    """Update alarm status"""
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
async def delete_alarm(alarm_id: str, db: IDataBase = Depends(get_db)) -> dict:
    try:
        deleted_count = await db_interaction.delete_alarm(alarm_id, db)
        return {"deleted_count": deleted_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.delete("/delete_all_alarm_by_parent/{parent_id}", status_code=status.HTTP_200_OK)
async def delete_all_alarm_by_parent(parent_id: str, db: IDataBase = Depends(get_db)) -> dict:
    try:
        AlarmLinksModel.parent_id_must_convert_to_object_id(parent_id)  # Validate Parent id
        deleted_count = await db_interaction.delete_all_alarms_by_condition(
            {"links.parent_id": parent_id}, db
        )
        result = {"deleted_count": deleted_count}
        return result
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.delete("/delete_all_user_alarms/{user_id}", status_code=status.HTTP_200_OK)
async def delete_all_user_alarms(user_id, db: IDataBase = Depends(get_db)) -> dict:
    try:
        deleted_count = await db_interaction.delete_all_alarms_by_condition(
            {"links.user_id": user_id}, db
        )
        result = {"deleted_count": deleted_count}
        return result
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
