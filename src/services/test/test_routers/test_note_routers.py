import pytest
from httpx import AsyncClient
from starlette import status

from src.services.test.data import NoteTestData as Data


class TestNoteRouter:

    @pytest.mark.parametrize(
        "code, body",
        [
            (status.HTTP_422_UNPROCESSABLE_ENTITY, Data.stub_body),
            (status.HTTP_201_CREATED, Data.test_note_model_to_write.dict()),
        ]
    )
    async def test_create_note(self, ac: AsyncClient, code, body):
        r = await ac.post(
            "notes/create_note",
            json=body
        )
        assert r.status_code == code
        pytest.note_cash.note_id = r.text.replace('"', "")

    @pytest.mark.parametrize(
        "code, note_id",
        [
            (status.HTTP_200_OK, None),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id),
            (
                    status.HTTP_400_BAD_REQUEST,
                    "1",
            )
        ]
    )
    async def test_get_note(self, ac: AsyncClient, code, note_id):
        if status.HTTP_200_OK == code:
            note_id = pytest.note_cash.note_id

        r = await ac.get(f"notes/get_note/{note_id}")
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, theme_id",
        [
            (status.HTTP_200_OK, Data.theme_id),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id),
            (status.HTTP_400_BAD_REQUEST, "1")
        ]
    )
    async def test_get_all_notes_by_theme_id(self, ac: AsyncClient, code, theme_id):
        r = await ac.get(f"notes/get_all_notes_by_theme_id/{theme_id}")
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, user_id",
        [
            (status.HTTP_200_OK, Data.user_id),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id),
        ]
    )
    async def test_get_all_notes_by_user_id(self, ac: AsyncClient, code, user_id):
        r = await ac.get(f"notes/get_all_notes_by_user_id/{user_id}")
        assert r.status_code == code

    # async def test_update_note(self, ac: AsyncClient, code, new_date):
    #     ...

    @pytest.mark.parametrize(
        "code, note_id",
        [
            (status.HTTP_200_OK, None),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id),
            (status.HTTP_400_BAD_REQUEST, "1")
        ]
    )
    async def test_delete_note(self, ac: AsyncClient, code, note_id):
        if code == status.HTTP_200_OK:
            note_id = pytest.note_cash.note_id
        r = await ac.delete(f"notes/delete_note/{note_id}")
        assert r.status_code == code
