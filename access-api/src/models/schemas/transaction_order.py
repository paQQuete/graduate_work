from __future__ import annotations
import uuid

from models.schemas.base import BaseSchemaModel, BaseFullModelMixin


class OrderBase(BaseSchemaModel):
    user_uuid: uuid.UUID
    checkout_session_id: str
    payment_intent_id: str
    topup_transaction: uuid.UUID | None
    refund_transaction: uuid.UUID | None


class OrderCreate(OrderBase):
    pass


class Order(OrderBase, BaseFullModelMixin):
    uuid: uuid.UUID

    class Config:
        orm_mode = True
