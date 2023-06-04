import datetime
import uuid

from models.schemas.base import BaseSchemaModel, BaseFullModelMixin

from models.models import TypesEnumHolds


class HoldsFundsBase(BaseSchemaModel):
    user_uuid: uuid.UUID
    type: TypesEnumHolds
    cost: int
    timestamp: datetime.datetime


class HoldFundsCreate(HoldsFundsBase):
    pass


class HoldFunds(HoldsFundsBase, BaseFullModelMixin):
    uuid: uuid.UUID

    class Config:
        orm_mode = True
