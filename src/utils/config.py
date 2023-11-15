import os

from dotenv import load_dotenv

load_dotenv()

APP_HOST: str = os.getenv("APP_HOST")
APP_PORT: int = int(os.getenv("APP_PORT"))

DB_USER_PASSWORD: str = os.getenv("DB_USER_PASSWORD")

JWT_SECRET: str = os.getenv("JWT_SECRET")
VERIFICATION_TOKEN_SECRET: str = os.getenv("VERIFICATION_TOKEN_SECRET")
TEST_BACKEND_USER_USERNAME: str = os.getenv('TEST_BACKEND_USER_USERNAME')
TEST_BACKEND_USER_PASSWORD: str = os.getenv("TEST_BACKEND_USER_PASSWORD")
