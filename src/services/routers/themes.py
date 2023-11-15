from logging import getLogger

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.requests import Request

from src.core.models.ThemeModel import ThemeModel, ThemeModelWrite
from src.infrastructure.themes import db_interaction
from src.services.auth.auth import get_current_backend_user
from src.services.auth.database import BackendUser
from src.services.database.database_exceptions import DBNotFound, InvalidIdException
from src.services.database.interface import IDataBase
from src.utils.depends import get_db

logger = getLogger("app.router.themes")

router = APIRouter(
    prefix="/themes",
    tags=["themes"]
)


@router.get("/get_theme/{theme_id}", status_code=status.HTTP_200_OK)
async def get_theme(r: Request, theme_id: str, db: IDataBase = Depends(get_db),
                    backend_user: BackendUser = Depends(get_current_backend_user)) -> ThemeModel:
    try:
        theme = await db_interaction.get_theme_from_db(theme_id, db)
        return theme
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.get("/get_all_user_themes/{user_id}")
async def get_all_user_themes(r: Request, user_id: str, db: IDataBase = Depends(get_db),
                              backend_user: BackendUser = Depends(get_current_backend_user)) -> list[ThemeModel]:
    logger.info(f"GET:Start:/get_all_user_themes/{user_id}")
    try:
        themes = await db_interaction.get_all_themes_by_condition(
            {"links": {"user_id": user_id}}, db
        )
        logger.info(f"GET:Success:/get_all_user_themes/{user_id}:{themes}")
        return themes
    except DBNotFound as err:
        logger.info(f"GET:Success:/get_all_user_themes/{user_id}:{err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/create_theme", status_code=status.HTTP_201_CREATED)
async def create_theme(r: Request, theme: ThemeModelWrite, db: IDataBase = Depends(get_db),
                       backend_user: BackendUser = Depends(get_current_backend_user)) -> str:
    theme_id = await db_interaction.write_theme_to_db(theme, db)
    return theme_id


@router.patch("/update_theme/{theme_id}", status_code=status.HTTP_200_OK)
async def update_theme(r: Request, theme_id: str, new_data: dict, db: IDataBase = Depends(get_db),
                       backend_user: BackendUser = Depends(get_current_backend_user)) -> dict:
    try:
        update_count = await db_interaction.update_theme(theme_id, new_data, db)
        return {"update_count": update_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.delete("/delete_theme/{theme_id}", status_code=status.HTTP_200_OK)
async def delete_theme(r: Request, theme_id: str, db: IDataBase = Depends(get_db),
                       backend_user: BackendUser = Depends(get_current_backend_user)) -> dict:
    try:
        deleted_count = await db_interaction.delete_theme_from_db(theme_id, db)
        return {"deleted_count": deleted_count}
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.delete("/delete_all_user_themes/{user_id}")
async def delete_all_user_themes(r: Request, user_id: str, db: IDataBase = Depends(get_db),
                                 backend_user: BackendUser = Depends(get_current_backend_user)) -> dict:
    logger.info(f"DELETE:Start:/delete_all_user_themes/{user_id}")
    try:
        delete_count = await db_interaction.delete_all_themes_from_db_by_condition(
            {"links": {"user_id": user_id}}, db
        )
        logger.info(f"DELETE:Success:/delete_all_user_themes/{user_id}:delete count - {delete_count}")
        return {"deleted_count": delete_count}
    except DBNotFound as err:
        logger.info(f"DELETE:Success:/delete_all_user_themes/{user_id}:{err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
