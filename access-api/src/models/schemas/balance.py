import datetime
import uuid

from models.schemas.base import BaseSchemaModel


class BalanceBase(BaseSchemaModel):
    user_uuid: uuid.UUID
    balance: int
    timestamp_offset: datetime.datetime


class Balance(BalanceBase):
    uuid: uuid.UUID
