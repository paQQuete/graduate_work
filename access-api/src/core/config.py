import os
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings
from .logger import LOGGING

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

    class Config:
        env_file = '.env'


class RedisDSN(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = '.env'


class Stripe(BaseSettings):
    STRIPE__API_KEY: str
    STRIPE__WEBHOOK_SECRET: str
    STRIPE__BALANCE_PROD_ID: str


class Project(BaseSettings):
    PROJECT_NAME: str
    PROJECT_DOMAIN: str
    PROJECT_PORT: int


class Settings(BaseSettings):
    DB: DatabaseDSN = DatabaseDSN()
    REDIS: RedisDSN = RedisDSN()
    STRIPE: Stripe = Stripe()
    PROJECT: Project = Project()
    SENTRY: bool = False

    SQLALCHEMY_DATABASE_URL = \
        f"postgresql://{DB.DB_USER}:{DB.DB_PASSWORD}@{DB.POSTGRES_HOST}:{DB.POSTGRES_PORT}/{DB.BILLING_DB}"
    PROJECT_URL = f"http://{PROJECT.PROJECT_DOMAIN}:{PROJECT.PROJECT_PORT}"

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = '.env'


SETTINGS = Settings()
