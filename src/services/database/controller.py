from src.services.database.interface import IDataBase
from src.services.database.mongo_db import MongoAPI
from src.utils import config


def connect_to_db() -> IDataBase:
    db = MongoAPI()
    print(db.connect_to_db(config.TEST_DB_USER_PASSWORD))
    return db
