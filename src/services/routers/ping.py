from datetime import datetime

from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request

from src.services.auth.auth import get_current_backend_user
from src.services.auth.database import BackendUser

router = APIRouter(
    # prefix="/"
)


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping(r: Request) -> dict:
    return {
        "app": r.app.title,
        "server_time": datetime.now()
    }


@router.get("/protected_jwt_ping", status_code=status.HTTP_200_OK)
async def protected_jwt_ping(r: Request, backend_user: BackendUser = Depends(get_current_backend_user)):
    return {
        "app": r.app.title,
        "user": backend_user.tags
    }
