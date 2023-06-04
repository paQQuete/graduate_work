import datetime
import uuid

from models.schemas.base import BaseSchemaModel, BaseFullModelMixin


class BalanceBase(BaseSchemaModel):
    user_uuid: uuid.UUID
    balance: int
    timestamp_offset: datetime.datetime


class Balance(BalanceBase, BaseFullModelMixin):
    uuid: uuid.UUID
