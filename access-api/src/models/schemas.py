import datetime
import uuid
from enum import Enum

import orjson
from pydantic import BaseModel

from .models import TypesEnum


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class TransactionBase(BaseOrjsonModel):
    user_uuid: uuid.UUID
    type: TypesEnum
    cost: int
    timestamp: datetime.datetime


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    uuid: uuid.UUID

    class Config:
        orm_mode = True
