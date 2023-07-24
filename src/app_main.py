from fastapi import FastAPI
import uvicorn

from src.services.database.mongo_db import MongoAPI
from src.services.routers.users import router as user_routers



ROUTERS = (
    user_routers,
)

# Connect to db
db = MongoAPI()
db.connect_to_db(connection_string=MONGO_TEST_DB_CONNECTION_PATH, is_test=True)

# Create fastApi app
app = FastAPI(title="Alarm_bot_api")

# Save ref to db
app.state.db = db

app.include_router(router=user_routers)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
