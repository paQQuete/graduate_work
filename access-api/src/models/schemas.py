import datetime
import uuid

import orjson
from pydantic import BaseModel

from .models import TypesEnum


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseSchemaModel(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class TransactionBase(BaseSchemaModel):
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


class BalanceBase(BaseSchemaModel):
    user_uuid: uuid.UUID
    balance: int
    timestamp_offset: datetime.datetime


class Balance(BalanceBase):
    uuid: uuid.UUID
