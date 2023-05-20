import datetime
import uuid

from models.schemas.base import BaseSchemaModel
from models.models import TypesEnum


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
