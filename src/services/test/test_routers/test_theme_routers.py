import asyncio

import pytest
from httpx import AsyncClient
from starlette import status

from src.services.test.data import ThemeTestData as Data


class TestThemeRouters:

    @pytest.mark.parametrize(
        "code, body",
        [
            (status.HTTP_422_UNPROCESSABLE_ENTITY, Data.stub_body),
            (status.HTTP_201_CREATED, Data.test_theme_model_to_write.dict())
        ]
    )
    async def test_create_theme(self, ac: AsyncClient, code, body):
        r = await ac.post(
            f"themes/create_theme",
            json=body
        )
        assert r.status_code == code
        pytest.theme_cash.theme_id_1 = r.text.replace('"', "")

    @pytest.mark.parametrize(
        "code, theme_id, theme",
        [
            (
                    status.HTTP_200_OK,
                    None,
                    None
            ),
            (
                    status.HTTP_404_NOT_FOUND,
                    Data.non_exist_id,
                    {"detail": "Theme not found"}
            ),
            (
                    status.HTTP_400_BAD_REQUEST,
                    "1",
                    {"detail": "1 is not a valid, it must be a 12-byte input or a 24-character hex string"}
            )
        ]
    )
    async def test_get_theme(self, ac: AsyncClient, code, theme_id, theme):
        if code == status.HTTP_200_OK:
            theme_id = pytest.theme_cash.theme_id_1
            theme = Data.test_theme_model_to_write.convert_to_theme_model(theme_id).dict(by_alias=True)

        r = await ac.get(f"themes/get_theme/{theme_id}")
        assert r.status_code == code
        assert r.json() == theme

    @pytest.mark.parametrize(
        "code, user_id, res_body",
        [
            (status.HTTP_200_OK, Data.user_id, None),
            (status.HTTP_404_NOT_FOUND, "qqqqqqqq", {"detail": "Themes not found"})
        ]
    )
    async def test_get_all_user_themes(self, ac: AsyncClient, code, user_id, res_body):
        if code == status.HTTP_200_OK:
            theme_id = pytest.theme_cash.theme_id_1
            res_body = [Data.test_theme_model_to_write.convert_to_theme_model(theme_id).dict(by_alias=True)]

        r = await ac.get(f"themes/get_all_user_themes/{user_id}")
        assert r.status_code == code
        assert r.json() == res_body

    @pytest.mark.parametrize(
        "code, theme_id, to_update, res_body",
        [
            (
                    status.HTTP_200_OK,
                    None,
                    Data.to_update,
                    {"update_count": 1}
            ),
            (
                    status.HTTP_404_NOT_FOUND,
                    Data.non_exist_id,
                    Data.to_update,
                    {"detail": "Theme not found"}
            ),
            (
                    status.HTTP_400_BAD_REQUEST,
                    "1",
                    Data.to_update,
                    {"detail": "1 is not a valid, it must be a 12-byte input or a 24-character hex string"})
        ]
    )
    async def test_update_theme(self, ac: AsyncClient, code, theme_id, to_update, res_body):
        if code == status.HTTP_200_OK:
            theme_id = pytest.theme_cash.theme_id_1

        r = await ac.patch(
            f"themes/update_theme/{theme_id}",
            json=to_update
        )
        assert r.status_code == code
        assert r.json() == res_body

    @pytest.mark.parametrize(
        "code, theme_id, res_body",
        [
            (
                    status.HTTP_200_OK,
                    None,
                    {"delete_count": 1}
            ),
            (
                    status.HTTP_404_NOT_FOUND,
                    Data.non_exist_id,
                    {"detail": "Theme not found"}),
            (
                    status.HTTP_400_BAD_REQUEST,
                    "1",
                    {"detail": "1 is not a valid, it must be a 12-byte input or a 24-character hex string"})
        ]
    )
    async def test_delete_theme(self, ac: AsyncClient, code, theme_id, res_body):  # TODO
        if code == status.HTTP_200_OK:
            theme_id = pytest.theme_cash.theme_id_1

        r = await ac.delete(f"themes/delete_theme/{theme_id}")
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, user_id, res_body",
        [
            (status.HTTP_200_OK, Data.user_id, {"delete_count": 3}),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id, {"detail": "Theme not found"}),
        ]
    )
    async def test_delete_all_user_themes(self, ac: AsyncClient, code, user_id, res_body):  # TODO
        if code == status.HTTP_200_OK:
            theme_id = pytest.theme_cash.theme_id_1
            for i in range(0, 2):
                await ac.post(
                    f"themes/create_theme",
                    json=Data.test_theme_model_to_write.dict()
                )
        r = await ac.delete(f"themes/delete_all_user_themes/{user_id}")
        assert r.status_code == code
