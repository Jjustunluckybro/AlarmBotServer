import asyncio

import uvicorn
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.services.database.controller import connect_to_db
from src.services.jobs.alarm_status_check_job import check_queue_status
from src.services.routers.users import router as user_routers
from src.services.routers.alarms import router as alarms_routers
from src.services.routers.themes import router as themes_routers
from src.services.routers.notes import router as note_routers
from src.services.routers.ping import router as ping_router

# Create fastApi app
app = FastAPI(title="Alarm_bot_api")


@app.on_event("startup")
def on_startup():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_queue_status, "interval", seconds=5)
    scheduler.start()


# Connect to db
connect_to_db()

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
