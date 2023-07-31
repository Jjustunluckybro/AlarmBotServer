from fastapi import APIRouter
from starlette.requests import Request
from starlette import status
from src.core.models.ThemeModel import ThemeModel

router = APIRouter(
    prefix="/themes",
    tags=["themes"]
)
