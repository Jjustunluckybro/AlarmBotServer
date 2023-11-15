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
            json=body, headers={
                "Authorization": f"bearer {pytest.auth.token}"
            }
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

        r = await ac.get(f"notes/get_note/{note_id}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
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
        r = await ac.get(f"notes/get_all_notes_by_theme_id/{theme_id}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, user_id",
        [
            (status.HTTP_200_OK, Data.user_id),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id),
        ]
    )
    async def test_get_all_notes_by_user_id(self, ac: AsyncClient, code, user_id):
        r = await ac.get(f"notes/get_all_notes_by_user_id/{user_id}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, note_id, new_data, res_body",
        [
            (
                    status.HTTP_200_OK,
                    None,
                    Data.new_data_to_update_note,
                    {"update_count": 1}
            ),
            (
                    status.HTTP_404_NOT_FOUND,
                    Data.non_exist_id,
                    dict(),
                    {"detail": "Note not found"}
            )
        ]
    )
    async def test_update_note(self, ac: AsyncClient, code, note_id, new_data, res_body):
        if code == status.HTTP_200_OK:
            note_id = pytest.note_cash.note_id
        r = await ac.patch(
            f"notes/update_note/{note_id}", headers={
                "Authorization": f"bearer {pytest.auth.token}"
            },
            json=new_data
        )
        assert r.status_code == code
        assert r.json() == res_body

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
        r = await ac.delete(f"notes/delete_note/{note_id}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, theme_id, res_body",
        [
            (status.HTTP_200_OK, Data.theme_id, {"deleted_count": 3}),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id, {"detail": "Notes not found"})
        ]
    )
    async def test_delete_all_note_by_theme_id(self, ac: AsyncClient, code, theme_id, res_body):
        if code == status.HTTP_200_OK:
            for i in range(0, 3):
                await ac.post(
                    "notes/create_note",
                    json=Data.test_note_model_to_write.dict(), headers={
                        "Authorization": f"bearer {pytest.auth.token}"
                    }
                )

        r = await ac.delete(f"notes/delete_all_note_by_theme_id/{theme_id}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert r.status_code == code
        assert r.json() == res_body
