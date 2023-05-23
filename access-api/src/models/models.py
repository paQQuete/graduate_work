import datetime
import uuid
import enum

from sqlalchemy import Column, Integer, DateTime, Enum, String, ForeignKey
from sqlalchemy_utils.types.uuid import UUIDType
from sqlalchemy.orm import relationship

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


class TrasnactionOrder(DefaultMixin, Base):
    __tablename__ = "trans_order"
    __table_args__ = {"schema": "billing"}

    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    payment_session_id = Column(String, index=True, nullable=False)
    subscribe_id = Column(UUIDType(binary=False), index=True, nullable=False)
    started_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    ended_at = Column(DateTime, nullable=True)


class Subscription(Base):
    __tablename__ = "subscribe"
    __table_args__ = {"schema": "content"}

    id = Column(UUIDType(binary=False), primary_key=True)
    name = Column(String)
    description = Column(String)
    periodic_type = Column(String)
    cost = Column(Integer)
    charge_type = Column(String)
    created_by = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    grants = relationship('GrantedAccesses', back_populates='subscription')

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def _disallow_modification(self, *args, **kwargs):
        raise NotImplementedError("Cannot modify a read-only instance")

    __setattr__ = _disallow_modification
    __delattr__ = _disallow_modification


class GrantedAccess(DefaultMixin, Base):
    __tablename__ = "granted_access"
    __table_args__ = {"schema": "billing"}

    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    subscription_id = Column(UUIDType(binary=False), ForeignKey('content.subscribe.id'))
    granted_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    available_until = Column(DateTime, nullable=False)

    films = relationship('GrantedFilms', back_populates='grant')
    subscribe = relationship('Subscription', back_populates='grants')


class GrantedFilms(DefaultMixin, Base):
    __tablename__ = "granted_films"
    __table_args__ = {"schema": "billing"}

    movie_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    granted_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    grant_uuid = Column(UUIDType(binary=False), ForeignKey('billing.granted_access.uuid', ondelete='CASCADE'), nullable=False)

    grant = relationship('GrantedAccess', back_populates='films')
