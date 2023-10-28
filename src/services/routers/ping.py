from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials
from starlette.requests import Request
from starlette import status

from src.services.auth.auth import authenticate_client

router = APIRouter(
    # prefix="/"
)


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping(r: Request) -> dict:
    return {
        "app": r.app.title
    }


@router.get("/protect_ping", status_code=status.HTTP_200_OK)
def protect_ping(r: Request, credentials: Annotated[HTTPBasicCredentials, Depends(authenticate_client)]) -> dict:
    return {
        "app": r.app.title
    }
