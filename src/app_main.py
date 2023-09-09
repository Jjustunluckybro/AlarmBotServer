import os
import uvicorn

from fastapi import FastAPI
from dotenv import load_dotenv

from src.services.database.mongo_db import MongoAPI
from src.services.routers.users import router as user_routers
from src.services.routers.alarms import router as alarms_routers
from src.services.routers.themes import router as themes_routers
from src.services.routers.notes import router as note_routers
from src.services.routers.ping import router as ping_router

# Get env variables
load_dotenv()

TEST_DB_USER_PASSWORD = os.getenv("TEST_DB_USER_PASSWORD")

# Register routers
ROUTERS = (
    user_routers,
    alarms_routers,
    themes_routers,
    note_routers,
    ping_router
)

# Connect to db
db = MongoAPI()
db.connect_to_db(TEST_DB_USER_PASSWORD)

# Create fastApi app
app = FastAPI(title="Alarm_bot_api")

# Save ref to db
app.state.db = db

for router in ROUTERS:
    app.include_router(router=router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
