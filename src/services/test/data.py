from src.core.models.NoteModel import NoteRouterModel, NoteLinksModel, NoteDataModel, CheckPointModel
from src.core.models.ThemeModel import ThemeModelWrite, ThemesLinksModel
from src.core.models.UserModel import UserModel


class TestData:
    stub_body = {"key": "value"}


class UserTestData(TestData):
    non_exist_id = "000000000"
    test_user_1 = UserModel(
        telegram_id="123456789",
        user_name="TestUserName1",
        lang_code="Ru",
        first_name="TestFirstName1",
        last_name="TestLastName1"
    )


class ThemeTestData(TestData):
    non_exist_id = "11aa204076aa1111a1111a1a"
    user_id = "111111111"
    test_theme_model_to_write = ThemeModelWrite(
        name="test_theme_model_to_write",
        description="This is an amazing item that has along description",
        links=ThemesLinksModel(user_id=user_id)
    )
    test_theme_model_after_update = ThemeModelWrite(
        name="test_theme_model_to_update",
        description="^_^",
        links=ThemesLinksModel(user_id=user_id)
    )
    to_update = {
        "name": "test_theme_model_to_update",
        "description": "^_^"
    }


class NoteTestData(TestData):
    non_exist_id = "11aa204076aa1111a1111a1a"
    user_id = "111111111"
    theme_id = "65059e0f09d5360ce08dfacf"
    test_note_model_to_write = NoteRouterModel(
        name="Test note",
        links=NoteLinksModel(
            user_id=user_id,
            theme_id=theme_id
        ),
        data=NoteDataModel(
            text="test note text",
            check_points=[
                CheckPointModel(
                    text="test checkpoint 1",
                    is_finish=True
                ),
                CheckPointModel(
                    text="test checkpoint 1",
                    is_finish=False
                )
            ]
        )
    )
    new_data_to_update_note = {
        "name": "New test name"
    }
