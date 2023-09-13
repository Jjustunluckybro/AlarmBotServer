from src.core.models.ThemeModel import ThemeModel, ThemeModelWrite

from src.services.database.interface import IDataBase


async def get_theme_from_db(theme_id: str, db: IDataBase) -> ThemeModel:
    theme = await db.get_theme_by_id(theme_id)
    return theme


async def write_theme_to_db(theme: ThemeModelWrite, db: IDataBase) -> str:
    theme_id = await db.write_new_theme(theme)
    return theme_id


async def get_all_themes_by_condition(condition: dict, db: IDataBase) -> list[ThemeModel]:
    themes = await db.get_all_themes_by_condition(condition)
    return themes


async def update_theme(theme_id: str, new_data: dict, db: IDataBase) -> int:
    update_counter = await db.update_theme(theme_id, new_data)
    return update_counter


async def delete_theme_from_db(theme_id: str, db: IDataBase) -> int:
    deleted_counter = await db.delete_theme_by_id(theme_id)
    return deleted_counter


async def delete_all_themes_from_db_by_condition(condition: dict, db: IDataBase) -> int:
    deleted_counter = await db.delete_all_themes_by_condition(condition)
    return deleted_counter
