import os
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings
from logger import LOGGING

DEBUG = True
if DEBUG:
    load_dotenv()

logging_config.dictConfig(LOGGING)


class DatabaseDSN(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    BILLING_DB: str
    DB_USER: str
    DB_PASSWORD: str


class Settings(BaseSettings):
    PROJECT_NAME: str
    DB: DatabaseDSN = DatabaseDSN()

    SQLALCHEMY_DATABASE_URL = \
        f"postgresql://{DB.DB_USER}:{DB.DB_PASSWORD}@{DB.POSTGRES_HOST}:{DB.POSTGRES_PORT}/{DB.BILLING_DB}"

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = '.env'


SETTINGS = Settings()
