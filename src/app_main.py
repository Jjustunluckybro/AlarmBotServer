import uvicorn
from fastapi import FastAPI

from src.services.database.controller import connect_to_db
from src.services.jobs.scheduler import create_and_start_scheduler
from src.services.routers.users import router as user_routers
from src.services.routers.alarms import router as alarms_routers
from src.services.routers.themes import router as themes_routers
from src.services.routers.notes import router as note_routers
from src.services.routers.ping import router as ping_router

# Create fastApi app
app = FastAPI(title="Alarm_bot_api")


@app.on_event("startup")
def on_startup():
    create_and_start_scheduler()


# Connect to db
app.state.db = connect_to_db()

# Register routers
ROUTERS = (
    user_routers,
    alarms_routers,
    themes_routers,
    note_routers,
    ping_router
)

for router in ROUTERS:
    app.include_router(router=router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
