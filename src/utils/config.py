import os

from dotenv import load_dotenv

load_dotenv()

TEST_DB_USER_PASSWORD = os.getenv("TEST_DB_USER_PASSWORD")
