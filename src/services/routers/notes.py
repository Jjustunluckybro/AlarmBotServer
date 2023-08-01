from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette import status
from src.core.models.NoteModel import NoteModel
from src.infrastructure.notes import db_interaction
from src.services.database.database_exceptions import DBNotFound, DuplicateKey
from src.services.database.interface import IDataBase

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)


@router.get("/get_note/{note_id}", status_code=status.HTTP_200_OK)
async def get_note(r: Request, note_id: str) -> NoteModel:
    db: IDataBase = r.app.state.db
    try:
        note = await db_interaction.get_note_from_db(note_id, db)
        return note
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/create_note", status_code=status.HTTP_201_CREATED)
async def create_note(r: Request, note: NoteModel) -> str:
    db: IDataBase = r.app.state.db
    try:
        note_id = await db_interaction.write_note_to_db(note, db)
        return note_id
    except DuplicateKey as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.post("/get_all_notes_by_condition", status_code=status.HTTP_200_OK)
async def get_all_notes_by_condition(r: Request, condition: dict) -> list[NoteModel]:
    db: IDataBase = r.app.state.db
    try:
        note = await db_interaction.get_all_notes_by_condition(condition, db)
        return note
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.patch("/update_note/{note_id}", status_code=status.HTTP_200_OK)
async def update_note(r: Request, note_id: str, new_data: dict) -> dict:
    db: IDataBase = r.app.state.db
    try:
        update_count = await db_interaction.update_note(note_id, new_data, db)
        return {"update_count": update_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.delete("/delete_note/{note_id}", status_code=status.HTTP_200_OK)
async def delete_note(r: Request, note_id: str) -> dict:
    db: IDataBase = r.app.state.db
    try:
        deleted_count = await db_interaction.delete_note(note_id, db)
        return {"deleted_count": deleted_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.delete("/delete_all_notes_by_condition", status_code=status.HTTP_200_OK)
async def delete_all_notes_by_condition(r: Request, condition: dict) -> dict:
    db: IDataBase = r.app.state.db
    try:
        deleted_count = await db_interaction.delete_all_notes_by_condition(condition, db)
        return {"deleted_count": deleted_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
