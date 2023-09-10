from src.core.models.UserModel import UserModel


class TestData:
    ...


class UserTestData(TestData):
    not_exist_id = "000000000"
    test_user_1 = UserModel(
        telegram_id="123456789",
        user_name="TestUserName1",
        lang_code="Ru",
        first_name="TestFirstName1",
        last_name="TestLastName1"
    )
