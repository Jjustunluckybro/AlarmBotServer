import logging

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.requests import Request

from src.core.models.UserModel import UserModel
from src.infrastructure.users.db_interaction import (get_user_from_db, write_user_to_db, update_username_in_db,
                                                     delete_user_from_db)
from src.services.auth.auth import get_current_backend_user
from src.services.auth.database import BackendUser
from src.services.database.database_exceptions import DBNotFound, DuplicateKey
from src.services.database.interface import IDataBase
from src.utils.depends import get_db

logger = logging.getLogger("app.router.users")

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/get_user/{user_telegram_id}", status_code=status.HTTP_200_OK)
async def get_user(r: Request, user_telegram_id: str, db: IDataBase = Depends(get_db),
                   backend_user: BackendUser = Depends(get_current_backend_user)) -> UserModel:
    """"""
    logger.info(f"GET:Start:/get_user/{user_telegram_id}")
    try:
        user = await get_user_from_db(user_id=user_telegram_id,
                                      db=db)
        logger.info(f"GET:Success:/get_user/{user_telegram_id}:{user}")
        return user
    except DBNotFound as err:
        logger.info(f"GET:Success:/get_user/{user_telegram_id}:{err}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(r: Request, user: UserModel, db: IDataBase = Depends(get_db),
                      backend_user: BackendUser = Depends(get_current_backend_user)) -> str:
    logger.info(f"POST:Start:/create_user:{user}")
    try:
        user_id = await write_user_to_db(user=user,
                                         db=db)
        logger.info(f"POST:Success:/create_user:{user}:{user_id}")
        return user_id
    except DuplicateKey as err:
        logger.info(f"POST:Success:/create_user:{user}:{err}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.patch("/update_username/{user_telegram_id}", status_code=status.HTTP_200_OK,)
async def update_username(r: Request, user_telegram_id: str, new_name: str, db: IDataBase = Depends(get_db),
                          backend_user: BackendUser = Depends(get_current_backend_user)) -> int:
    try:
        change_counter = await update_username_in_db(user_id=user_telegram_id,
                                                     new_name=new_name,
                                                     db=db)
        return change_counter
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.delete("/delete_user/{user_telegram_id}", status_code=status.HTTP_200_OK)
async def delete_user(r: Request, user_telegram_id: str, db: IDataBase = Depends(get_db),
                      backend_user: BackendUser = Depends(get_current_backend_user)) -> int:
    try:
        deleted_count = await delete_user_from_db(user_telegram_id, db)
        return deleted_count
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
