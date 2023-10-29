from src.services.database.interface import IDataBase
from src.services.database.mongo_db import MongoAPI


def get_db() -> IDataBase:
    return MongoAPI()
