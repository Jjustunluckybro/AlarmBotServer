from fastapi import APIRouter
from starlette.requests import Request
from starlette import status
from src.core.models.AlarmModel import AlarmModel

router = APIRouter(
    prefix="/alarms",
    tags=["alarms"]
)
