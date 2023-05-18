import datetime
import uuid
import enum

from sqlalchemy import Enum
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy_utils.types.uuid import UUIDType

from db.database import Base


class TimeStampedMixin:
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = Column(DateTime, nullable=True)


class TypesEnum(enum.Enum):
    topup = 'topup'
    spending = 'spending'
    refund = 'refund'


class Transaction(TimeStampedMixin, Base):
    __tablename__ = "transaction"
    __table_args__ = {"schema": "billing"}

    uuid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4())
    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    type = Column(Enum(TypesEnum), index=True, nullable=False)
    cost = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class Balance(TimeStampedMixin, Base):
    __tablename__ = "balance"
    __table_args__ = {"schema": "billing"}

    uuid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4())
    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    balance = Column(Integer, nullable=False)
    timestamp_offset = Column(DateTime, nullable=False)
