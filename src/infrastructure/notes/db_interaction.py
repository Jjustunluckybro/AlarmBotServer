from datetime import datetime as dt

from src.core.models.NoteModel import NoteModelWrite, NoteModelRouterInput, NoteTimesModel, NoteModel

from src.services.database.interface import IDataBase


async def get_note_from_db(note_id: str, db: IDataBase) -> NoteModel:
    note = await db.get_note_by_id(note_id)
    return note


async def write_note_to_db(note: NoteModelRouterInput, db: IDataBase) -> str:
    note = note.convert_to_note_model_write(times=NoteTimesModel(
        creation_time=dt.now()
    ))
    note_id = await db.write_new_note(note)
    return note_id


async def get_all_notes_by_condition(condition: dict, db: IDataBase) -> [NoteModelWrite]:
    notes = await db.get_all_notes_by_condition(condition)
    return notes


async def update_note(note_id: str, new_data: dict, db: IDataBase) -> int:
    update_count = await db.update_note(note_id, new_data)
    return update_count


async def delete_note(note_id: str, db: IDataBase) -> int:
    deleted_count = await db.delete_note_by_id(note_id)
    return deleted_count


async def delete_all_notes_by_condition(condition: dict, db: IDataBase) -> int:
    deleted_count = await db.delete_all_notes_by_condition(condition)
    return deleted_count
