import uvicorn
from fastapi import FastAPI

from src.services.auth.auth import auth_fastapi_users
from src.services.auth.auth_backend import auth_backend
from src.services.auth.database import init_backend_users_db
from src.services.database.controller import connect_to_db
from src.services.jobs.scheduler import create_and_start_scheduler
from src.services.routers.alarms import router as alarms_routers
from src.services.routers.notes import router as note_routers
from src.services.routers.ping import router as ping_router
from src.services.routers.themes import router as themes_routers
from src.services.routers.users import router as user_routers

# Create fastApi app
app = FastAPI(title="Alarm_bot_api")


@app.on_event("startup")
async def on_startup():
    await init_backend_users_db()
    create_and_start_scheduler()


# Connect to db
app.state.db = connect_to_db()

# Register custom routers
ROUTERS = (
    user_routers,
    alarms_routers,
    themes_routers,
    note_routers,
    ping_router
)

for router in ROUTERS:
    app.include_router(router=router)

# Register auth routers
app.include_router(
    auth_fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Router to register new backend user
# app.include_router(
#     auth_fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
