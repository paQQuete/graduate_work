import datetime
import uuid

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy_utils.types.uuid import UUIDType

from db.database import Base


class TimeStampedMixin:
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = Column(DateTime, nullable=True)


class Transaction(TimeStampedMixin, Base):
    __tablename__ = "transaction"
    TYPES = [
        ('topup', 'Top-Up'),
        ('spending', 'Spending'),
        ('refund', 'Refund')
    ]

    uuid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4())
    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    type = Column(ChoiceType(TYPES), index=True, nullable=False)
    cost = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class Balance(TimeStampedMixin, Base):
    __tablename__ = "balance"

    uuid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4())
    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    balance = Column(Integer, nullable=False)
    timestamp_offset = Column(DateTime, nullable=False)
