import datetime
import uuid
from enum import Enum

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class TypesEnum(str, Enum):
    topup = 'topup'
    spending = 'spending'
    refund = 'refund'


class TransactionBase(BaseOrjsonModel):
    user_uuid: uuid.UUID
    type: list[TypesEnum]
    cost: int
    timestamp: datetime.datetime


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    uuid: uuid.UUID

    class Config:
        orm_mode = True
        