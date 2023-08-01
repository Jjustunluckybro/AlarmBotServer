from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette import status
from src.core.models.ThemeModel import ThemeModel
from src.infrastructure.themes import db_interaction
from src.services.database.database_exceptions import DBNotFound, DuplicateKey
from src.services.database.interface import IDataBase

router = APIRouter(
    prefix="/themes",
    tags=["themes"]
)


@router.get("/get_theme/{theme_id}", status_code=status.HTTP_200_OK)
async def get_theme(r: Request, theme_id: str) -> ThemeModel:
    db: IDataBase = r.app.state.db
    try:
        theme = await db_interaction.get_theme_from_db(theme_id, db)
        return theme
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/create_theme", status_code=status.HTTP_201_CREATED)
async def create_theme(r: Request, theme: ThemeModel) -> str:
    db: IDataBase = r.app.state.db
    try:
        theme_id = await db_interaction.write_theme_to_db(theme, db)
        return theme_id
    except DuplicateKey as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.post("/get_all_themes_by_condition", status_code=status.HTTP_200_OK)
async def get_all_themes_by_condition(r: Request, condition: dict) -> list[ThemeModel]:
    db: IDataBase = r.app.state.db
    try:
        themes = await db_interaction.get_all_themes_by_condition(condition, db)
        return themes
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.patch("/update_theme/{theme_id}", status_code=status.HTTP_200_OK)
async def update_theme(r: Request, theme_id: str, new_data: dict) -> dict:
    db: IDataBase = r.app.state.db
    try:
        update_count = await db_interaction.update_theme(theme_id, new_data, db)
        return {"update_count": update_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.delete("/delete_theme/{theme_id}", status_code=status.HTTP_200_OK)
async def delete_theme(r: Request, theme_id: str) -> dict:
    db: IDataBase = r.app.state.db
    try:
        deleted_count = await db_interaction.delete_theme_from_db(theme_id, db)
        return {"deleted_count": deleted_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.delete("/delete_all_themes_by_condition", status_code=status.HTTP_200_OK)
async def delete_all_themes_by_condition(r: Request, condition: dict) -> dict:
    db: IDataBase = r.app.state.db
    try:
        deleted_count = await db_interaction.delete_all_themes_from_db_by_condition(condition, db)
        return {"deleted_count": deleted_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
