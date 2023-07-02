from fastapi import APIRouter
from starlette.requests import Request
from starlette import status
from src.core.models.UserModel import UserModel

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/get_user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(r: Request, user_id: str) -> UserModel:
    ...


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(r: Request, user: UserModel):
    ...


@router.patch("/update_username", status_code=status.HTTP_200_OK)
async def update_username(r: Request, user_id: str, new_name: str):
    ...


@router.delete("/delete_user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(r: Request, user_id: str):
    ...
