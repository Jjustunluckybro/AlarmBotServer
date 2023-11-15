import asyncio
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pydantic import BaseModel

from src.app_main import app


class BackendUserData(BaseModel):
    token: str | None = None


class ThemeCash(BaseModel):
    theme_id_1: None | str = None
    theme_id_2: None | str = None


class NoteCash(BaseModel):
    note_id: None | str = None


class AlarmCash(BaseModel):
    alarm_id: None | str = None


def pytest_configure():
    pytest.theme_cash = ThemeCash()
    pytest.note_cash = NoteCash()
    pytest.alarm_cash = AlarmCash()
    pytest.auth = BackendUserData()


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test.io") as ac:
            yield ac
