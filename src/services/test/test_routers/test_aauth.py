import pytest
from httpx import AsyncClient
from starlette import status

from src.utils import config


class Test01Auth:

    async def test_login_user(self, ac: AsyncClient):
        body = {
            "username": config.TEST_BACKEND_USER_USERNAME,
            "password": config.TEST_BACKEND_USER_PASSWORD,
        }
        r = await ac.post(
            f"auth/jwt/login",
            data=body,
        )
        assert r.status_code == status.HTTP_200_OK
        assert r.json()["token_type"] == "bearer"
        pytest.auth.token = r.json()["access_token"]