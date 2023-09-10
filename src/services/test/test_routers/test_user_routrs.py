import pytest
from httpx import AsyncClient
from starlette import status

from src.services.test.data import UserTestData as Data


class TestUserRouters:

    @pytest.mark.parametrize(
        "code, body",
        [
            (status.HTTP_201_CREATED, Data.test_user_1.dict()),
            (status.HTTP_409_CONFLICT, Data.test_user_1.dict()),
            (status.HTTP_422_UNPROCESSABLE_ENTITY, {"key": "value"})
        ]
    )
    async def test_create_user(self, ac: AsyncClient, code, body):
        r = await ac.post(
            "/users/create_user",
            json=body
        )
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, user_id, res_body",
        [

            (
                    status.HTTP_200_OK,
                    Data.test_user_1.telegram_id,
                    Data.test_user_1.dict()
            ),
            (
                    status.HTTP_404_NOT_FOUND,
                    Data.not_exist_id,
                    {'detail': 'User not found'}
            )
        ]
    )
    async def test_get_user(self, ac: AsyncClient, user_id, code, res_body):
        r = await ac.get(
            f"/users/get_user/{user_id}"
        )
        assert r.status_code == code
        assert r.json() == res_body

    @pytest.mark.parametrize(
        "code, user_id",
        [
            (status.HTTP_200_OK, Data.test_user_1.telegram_id),
            (status.HTTP_404_NOT_FOUND, Data.not_exist_id)
        ]
    )
    async def test_update_username(self, ac: AsyncClient, user_id, code):
        r = await ac.patch(
            f"users/update_username/{user_id}?new_name=NewTestName1"
        )
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, user_id, res_body",
        [
            (status.HTTP_200_OK, Data.test_user_1.telegram_id, 1),
            (status.HTTP_404_NOT_FOUND, Data.not_exist_id, {'detail': 'User not found'})
        ]
    )
    async def test_delete_user(self, ac: AsyncClient, user_id, code, res_body):
        r = await ac.delete(
            f"users/delete_user/{user_id}"
        )
        assert r.status_code == code
        assert r.json() == res_body
