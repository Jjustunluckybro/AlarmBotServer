from httpx import AsyncClient
from starlette import status

from src.services.test.data import UserTestData as Data


async def test_create_user(ac: AsyncClient):
    r = await ac.post(
        "/users/create_user",
        json=Data.test_user_1.dict()
    )
    assert r.status_code == status.HTTP_201_CREATED


async def test_create_user_negative_conflict(ac: AsyncClient):
    r = await ac.post(
        "/users/create_user",
        json=Data.test_user_1.dict()
    )
    assert r.status_code == status.HTTP_409_CONFLICT


async def test_create_user_negative_invalid_data(ac: AsyncClient):
    r = await ac.post(
        "/users/create_user",
        json={"key": "value"}
    )
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_user(ac: AsyncClient):
    r = await ac.get(
        f"/users/get_user/{Data.test_user_1.telegram_id}"
    )
    assert r.status_code == status.HTTP_200_OK
    assert r.json() == Data.test_user_1.dict()


async def test_get_user_negative_not_found(ac: AsyncClient):
    r = await ac.get(
        f"/users/get_user/{Data.not_exist_id}"
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND


async def test_update_username(ac: AsyncClient):
    r = await ac.patch(
        f"users/update_username/{Data.test_user_1.telegram_id}?new_name=NewTestName1"
    )
    assert r.status_code == status.HTTP_200_OK


async def test_update_username_negative_not_found(ac: AsyncClient):
    r = await ac.patch(
        f"users/update_username/{Data.not_exist_id}?new_name=NewTestName1"
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_user(ac: AsyncClient):
    r = await ac.delete(
        f"users/delete_user/{Data.test_user_1.telegram_id}"
    )
    assert r.status_code == status.HTTP_200_OK
    assert r.text == "1"


async def test_delete_user_negative_not_found(ac: AsyncClient):
    r = await ac.delete(
        f"users/delete_user/{Data.not_exist_id}"
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND
