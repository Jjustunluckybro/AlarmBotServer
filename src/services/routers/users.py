from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette import status
from src.core.models.UserModel import UserModel
from src.infrastructure.users.db_interaction import get_user_from_db, write_user_to_db
from src.services.database.database_exceptions import DBNotFound, DuplicateKey
from src.services.database.interface import IDateBase

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/get_user/{user_telegram_id}", status_code=status.HTTP_200_OK)
async def get_user(r: Request, user_telegram_id: str) -> UserModel:
    db: IDateBase = r.app.state.db
    try:
        user = await get_user_from_db(user_id=user_telegram_id,
                                      db=db)
        return user
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(r: Request, user: UserModel) -> str:
    db: IDateBase = r.app.state.db
    try:
        user_id = await write_user_to_db(user=user,
                                         db=db)
        return user_id
    except DuplicateKey as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.patch("/update_username/{user_telegram_id}", status_code=status.HTTP_200_OK)
async def update_username(r: Request, user_telegram_id: str, new_name: str):
    ...


@router.delete("/delete_user/{user_telegram_id}", status_code=status.HTTP_200_OK)
async def delete_user(r: Request, user_telegram_id: str):
    ...
