import asyncio
import pytest

from typing import AsyncGenerator
from httpx import AsyncClient
from pydantic import BaseModel

from src.app_main import app


class ThemeCash(BaseModel):
    theme_id_1: None | str = None
    theme_id_2: None | str = None


def pytest_configure():
    pytest.theme_cash = ThemeCash()


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
