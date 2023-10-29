import logging

from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from starlette import status
from src.core.models.NoteModel import NoteRouterModel, NoteModel, NoteLinksModel
from src.utils.depends import get_db
from src.infrastructure.notes import db_interaction
from src.services.database.database_exceptions import DBNotFound, InvalidIdException
from src.services.database.interface import IDataBase

logger = logging.getLogger("app.router.notes")

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)


@router.get("/get_note/{note_id}", status_code=status.HTTP_200_OK)
async def get_note(note_id: str, db: IDataBase = Depends(get_db)) -> NoteModel:
    logger.info(f"GET:Start:/get_note:{note_id}")
    try:
        note = await db_interaction.get_note_from_db(note_id, db)
        logger.info(f"GET:Success:/get_note:{note_id}:{note}")
        return note
    except DBNotFound as err:
        logger.info(f"GET:Success handle exception:/get_note:{note_id}:{err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        logger.info(f"GET:Success handle exception:/get_note:{note_id}:{err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.get("/get_all_notes_by_theme_id/{theme_id}", status_code=status.HTTP_200_OK)
async def get_all_notes_by_theme_id(theme_id: str, db: IDataBase = Depends(get_db)) -> list[NoteModel]:
    logger.info(f"GET:Start:/get_all_notes_by_theme_id:{theme_id}")
    try:
        NoteLinksModel.theme_id_must_convert_to_object_id(theme_id)  # Validate theme_id
        note = await db_interaction.get_all_notes_by_condition(
            {"links.theme_id": theme_id}, db
        )
        logger.info(f"GET:Success:/get_all_notes_by_theme_id:{theme_id}:{note}")
        return note
    except DBNotFound as err:
        logger.info(f"GET:Success handle exception:/get_all_notes_by_theme_id:{theme_id}:{err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        logger.info(f"GET:Success handle exception:/get_all_notes_by_theme_id:{theme_id}:{err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.get("/get_all_notes_by_user_id/{user_id}", status_code=status.HTTP_200_OK)
async def get_all_notes_by_user_id(user_id: str, db: IDataBase = Depends(get_db)) -> list[NoteModel]:
    logger.info(f"GET:Start:/get_all_notes_by_user_id:{user_id}")
    try:
        note = await db_interaction.get_all_notes_by_condition(
            {"links.user_id": user_id}, db
        )
        logger.info(f"GET:Success:/get_all_notes_by_user_id:{user_id}:{note}")
        return note
    except DBNotFound as err:
        logger.info(f"GET:Success handle exception:/get_all_notes_by_user_id:{user_id}:{err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/create_note", status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteRouterModel, db: IDataBase = Depends(get_db)) -> str:
    logger.info(f"POST:Start:/create_note:{note}")
    note_id = await db_interaction.write_note_to_db(note, db)
    logger.info(f"POST:Success:/create_note:{note}:{note_id}")
    return note_id


@router.patch("/update_note/{note_id}", status_code=status.HTTP_200_OK)
async def update_note(note_id: str, new_data: dict, db: IDataBase = Depends(get_db)) -> dict:
    logger.info(f"PATCH:Start:/update_note/{note_id}|{new_data}")
    try:
        update_count = await db_interaction.update_note(note_id, new_data, db)
        result = {"update_count": update_count}
        logger.info(f"PATCH:Success:/update_note/{note_id}:{result}")
        return result
    except DBNotFound as err:
        logger.info(f"GET:Success handle exception:/update_note:{note_id}:{err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.delete("/delete_note/{note_id}", status_code=status.HTTP_200_OK)
async def delete_note(r: Request, note_id: str, db: IDataBase = Depends(get_db)) -> dict:
    logger.info(f"DELETE:Start:/delete_note/{note_id}")
    try:
        deleted_count = await db_interaction.delete_note(note_id, db)
        result = {"deleted_count": deleted_count}
        logger.info(f"DELETE:Success:/delete_note/{note_id}:{result}")
        return result
    except DBNotFound as err:
        logger.info(f"GET:Success handle exception:/delete_note:{note_id}:{err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        logger.info(f"GET:Success handle exception:/delete_note:{note_id}:{err}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.delete("/delete_all_note_by_theme_id/{theme_id}", status_code=status.HTTP_200_OK)
async def delete_all_note_by_theme_id(r: Request, theme_id: str, db: IDataBase = Depends(get_db)) -> dict:
    logger.info(f"DELETE:Start:/delete_all_note_by_theme_id/{theme_id}")
    try:
        deleted_count = await db_interaction.delete_all_notes_by_condition(
            {"links.theme_id": theme_id}, db
        )
        result = {"deleted_count": deleted_count}
        logger.info(f"DELETE:Success:/delete_all_note_by_theme_id/{theme_id}:")
        return result
    except DBNotFound as err:
        logger.info(f"DELETE:Success handle exception:/delete_all_note_by_theme_id:{theme_id}:{err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
