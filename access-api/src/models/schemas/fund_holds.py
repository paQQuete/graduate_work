import datetime
import uuid

from models.schemas.base import BaseSchemaModel

from models.models import TypesEnumHolds


class HoldsFundsBase(BaseSchemaModel):
    user_uuid: uuid.UUID
    type: TypesEnumHolds
    cost: int
    timestamp: datetime.datetime


class HoldFundsCreate(HoldsFundsBase):
    pass


class HoldFunds(HoldsFundsBase):
    uuid: uuid.UUID

    class Config:
        orm_mode = True
