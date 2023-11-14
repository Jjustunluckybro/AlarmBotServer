from bson import ObjectId
from fastapi_users import FastAPIUsers

from src.services.auth.auth_backend import auth_backend
from src.services.auth.database import BackendUser
from src.services.auth.manager import get_user_manager

auth_fastapi_users = FastAPIUsers[BackendUser, ObjectId](
    get_user_manager,
    [auth_backend],
)


get_current_backend_user = auth_fastapi_users.current_user()
