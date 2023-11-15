import pytest
from httpx import AsyncClient
from starlette import status

from src.core.models.AlarmModel import AlarmStatuses
from src.services.test.data import AlarmTestData as Data


class TestAlarmRouters:

    @pytest.mark.parametrize(
        "code, body",
        [
            (status.HTTP_422_UNPROCESSABLE_ENTITY, Data.stub_body),
            (status.HTTP_201_CREATED, Data.test_alarm_model_to_write.dict())
        ]
    )
    async def test_create_alarm(self, ac: AsyncClient, code, body):
        r = await ac.post(
            "alarms/create_alarm?next_notion_time=2030-10-29%2014%3A16%3A11.462380&repeat_interval=600",
            json=body, headers={
                "Authorization": f"bearer {pytest.auth.token}"
            }
        )
        assert r.status_code == code
        pytest.alarm_cash.alarm_id = r.text.replace('"', "")

    @pytest.mark.parametrize(
        "code, alarm_id",
        [
            (status.HTTP_200_OK, None),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id),
            (status.HTTP_400_BAD_REQUEST, "1")
        ]
    )
    async def test_get_alarm(self, ac: AsyncClient, code, alarm_id):
        if status.HTTP_200_OK == code:
            alarm_id = pytest.alarm_cash.alarm_id

        r = await ac.get(f"alarms/get_alarm/{alarm_id}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, parent_id",
        [
            (status.HTTP_200_OK, Data.parent_id),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id),
            (status.HTTP_400_BAD_REQUEST, 1)
        ]
    )
    async def test_get_all_alarm_by_parent_id(self, ac: AsyncClient, code, parent_id):
        r = await ac.get(f"alarms/get_all_alarm_by_parent_id/{parent_id}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, user_id",
        [
            (status.HTTP_200_OK, Data.user_id),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id)
        ]
    )
    async def test_get_all_user_alarms(self, ac: AsyncClient, code, user_id):
        r = await ac.get(f"alarms/get_all_user_alarms/{user_id}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, alarm_id",
        [
            (status.HTTP_200_OK, None),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id),
            (status.HTTP_400_BAD_REQUEST, 1),
            (status.HTTP_400_BAD_REQUEST, None)
        ]
    )
    async def test_postpone_repeatable_alarm(self, ac: AsyncClient, code, alarm_id):
        if status.HTTP_200_OK == code:
            alarm_id = pytest.alarm_cash.alarm_id
        elif code == status.HTTP_400_BAD_REQUEST and alarm_id is None:
            body = Data.test_alarm_model_to_write
            body.is_repeatable = False
            req = await ac.post(
                "alarms/create_alarm?next_notion_time=2030-10-29%2014%3A16%3A11.462380&repeat_interval=600",
                json=body.dict(), headers={
                    "Authorization": f"bearer {pytest.auth.token}"
                }
            )
            alarm_id = req.text.replace('"', "")

        r = await ac.patch(f"alarms/postpone_repeatable_alarm/{alarm_id}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert code == r.status_code

    @pytest.mark.parametrize(
        "code, alarm_id, new_data",
        [
            (status.HTTP_200_OK, None, {"name": "New test name"}),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id, {}),
            (status.HTTP_400_BAD_REQUEST, 1, {})
        ]
    )
    async def test_update_alarm(self, ac: AsyncClient, code, alarm_id, new_data):
        if status.HTTP_200_OK == code:
            alarm_id = pytest.alarm_cash.alarm_id
        r = await ac.patch(f"alarms/update_alarm/{alarm_id}", json=new_data, headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, alarm_id, new_status",
        [
            (status.HTTP_200_OK, None, AlarmStatuses.FINISH.value),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id, AlarmStatuses.FINISH.value),
            (status.HTTP_400_BAD_REQUEST, 1, AlarmStatuses.FINISH.value)
        ]
    )
    async def test_update_alarm_status(self, ac: AsyncClient, code, alarm_id, new_status):
        if status.HTTP_200_OK == code:
            alarm_id = pytest.alarm_cash.alarm_id
        r = await ac.patch(f"alarms/update_alarm_status/{alarm_id}?new_status={new_status}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert code == r.status_code

    @pytest.mark.parametrize(
        "code, alarm_id",
        [
            (status.HTTP_200_OK, None),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id),
            (status.HTTP_400_BAD_REQUEST, 1)
        ]
    )
    async def test_delete_alarm_by_id(self, ac: AsyncClient, code, alarm_id):
        if code == status.HTTP_200_OK:
            alarm_id = pytest.alarm_cash.alarm_id
        r = await ac.delete(f"alarms/delete_alarm_by_id/{alarm_id}", headers={
            "Authorization": f"bearer {pytest.auth.token}"
        })
        assert r.status_code == code

    @pytest.mark.parametrize(
        "code, parent_id",
        [
            (status.HTTP_200_OK, Data.parent_id),
            (status.HTTP_404_NOT_FOUND, Data.non_exist_id),
            (status.HTTP_400_BAD_REQUEST, 1)
        ]
    )
    async def test_delete_all_alarm_by_parent(self, ac: AsyncClient, code, parent_id):
        r = await ac.delete(f"alarms/delete_all_alarm_by_parent/{parent_id}", headers={
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
    async def test_delete_all_alarm_by_user(self, ac: AsyncClient, code, user_id):
        if code == status.HTTP_200_OK:
            r = await ac.post(
                "alarms/create_alarm?next_notion_time=2030-10-29%2014%3A16%3A11.462380&repeat_interval=600",
                json=Data.test_alarm_model_to_write.dict(), headers={
                    "Authorization": f"bearer {pytest.auth.token}"
                }
            )
        r = await ac.delete(f"alarms/delete_all_user_alarms/{user_id}", headers={
                    "Authorization": f"bearer {pytest.auth.token}"
                })
        assert r.status_code == code
