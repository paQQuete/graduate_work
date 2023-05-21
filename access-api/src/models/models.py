import datetime
import uuid
import enum

from sqlalchemy import Column, Integer, DateTime, Enum, String
from sqlalchemy_utils.types.uuid import UUIDType

from db.database import Base


class DefaultMixin:
    uuid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4())
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = Column(DateTime, nullable=True)

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TypesEnum(enum.Enum):
    topup = 'topup'
    spending = 'spending'
    refund = 'refund'


class TypesEnumHolds(enum.Enum):
    spending = 'spending'
    refund = 'refund'


class TransactionBase:
    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    cost = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class Transaction(DefaultMixin, TransactionBase, Base):
    __tablename__ = "transaction"
    __table_args__ = {"schema": "billing"}

    type = Column(Enum(TypesEnum), index=True, nullable=False)


class Balance(DefaultMixin, Base):
    __tablename__ = "balance"
    __table_args__ = {"schema": "billing"}

    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    balance = Column(Integer, nullable=False)
    timestamp_offset = Column(DateTime, nullable=False)


class FundsOnHold(DefaultMixin, TransactionBase, Base):
    __tablename__ = "funds_hold"
    __table_args__ = {"schema": "billing"}

    type = Column(Enum(TypesEnumHolds), index=True, nullable=False)


# TODO
#     + еще одна модель с объектами созданных заказов,
#     (user id, payment session id ..., subscribe id)
#

class TrasnactionOrder(DefaultMixin, Base):
    __tablename__ = "trans_order"
    __table_args__ = {"schema": "billing"}

    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    payment_session_id = Column(String, index=True, nullable=False)
    subscribe_id = Column(UUIDType(binary=False), index=True, nullable=False)

