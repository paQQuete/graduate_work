import datetime
import uuid
import enum

from sqlalchemy import Column, Integer, DateTime, Enum, String, ForeignKey, Float, Boolean, Index
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


class DefaultReadOnlyMixin:
    id = Column(UUIDType(binary=False), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

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


# ну это можно убрать, если кешировать айди чекаут сесси в редис - и это будет норм вариант
class TrasnactionOrder(DefaultMixin, Base):
    __tablename__ = "trans_order"
    __table_args__ = {"schema": "billing"}

    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    payment_session_id = Column(String, index=True, nullable=False)
    subscribe_id = Column(UUIDType(binary=False), index=True, nullable=False)
    started_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    ended_at = Column(DateTime, nullable=True)


class GrantedAccess(DefaultMixin, Base):
    __tablename__ = "granted_access"
    __table_args__ = {"schema": "billing"}

    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    subscription_id = Column(UUIDType(binary=False), ForeignKey('content.subscribe.id'))
    granted_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    available_until = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False)

    films = relationship('GrantedFilms', back_populates='grant')
    subscription = relationship('Subscription', back_populates='grants')


class GrantedFilms(DefaultMixin, Base):
    __tablename__ = "granted_films"
    __table_args__ = (
        Index('ix_billing_granted_films_movie_user_uuids', 'movie_uuid', 'user_uuid'),
        {"schema": "billing"},
    )

    movie_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    granted_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    grant_uuid = Column(UUIDType(binary=False), ForeignKey('billing.granted_access.uuid', ondelete='CASCADE'),
                        nullable=False)
    user_uuid = Column(UUIDType(binary=False), index=True, nullable=False)
    is_active = Column(Boolean, nullable=False)

    grant = relationship('GrantedAccess', back_populates='films')


class SubscriptionFilmwork(Base):
    __tablename__ = "subscription_filmwork"
    __table_args__ = {"schema": "content"}

    id = Column(UUIDType(binary=False), primary_key=True)
    created_at = Column(DateTime)
    filmwork_id = Column(UUIDType(binary=False), ForeignKey('content.film_work.id'))
    subscription_id = Column(UUIDType(binary=False), ForeignKey('content.subscribe.id'))

    def _disallow_modification(self, name, *args, **kwargs):
        if not name.startswith('_') and not name in ['metadata']:
            raise NotImplementedError("Cannot modify a read-only instance")
        else:
            super().__setattr__(name, *args, **kwargs)

    __setattr__ = _disallow_modification
    __delattr__ = _disallow_modification


class Subscription(DefaultReadOnlyMixin, Base):
    __tablename__ = "subscribe"
    __table_args__ = {"schema": "content"}

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    periodic_type = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    charge_type = Column(String)
    created_by_id = Column(String)
    payment_gw_product_id = Column(String)
    payment_gw_price_id = Column(String)

    grants = relationship('GrantedAccess', back_populates='subscription')
    filmworks = relationship("Filmwork", secondary=SubscriptionFilmwork.__table__, back_populates='subscribes')

    def _disallow_modification(self, name, *args, **kwargs):
        if not name.startswith('_') and not name in ['metadata']:
            raise NotImplementedError("Cannot modify a read-only instance")
        else:
            super().__setattr__(name, *args, **kwargs)

    __setattr__ = _disallow_modification
    __delattr__ = _disallow_modification


class Filmwork(DefaultReadOnlyMixin, Base):
    __tablename__ = "film_work"
    __table_args__ = {"schema": "content"}

    title = Column(String)
    description = Column(String)
    creation_date = Column(DateTime)
    rating = Column(Float)
    type = Column(String)
    file_path = Column(String)

    subscribes = relationship("Subscription", secondary=SubscriptionFilmwork.__table__, back_populates='filmworks')

    def _disallow_modification(self, name, *args, **kwargs):
        if not name.startswith('_') and not name in ['metadata']:
            raise NotImplementedError("Cannot modify a read-only instance")
        else:
            super().__setattr__(name, *args, **kwargs)

    __setattr__ = _disallow_modification
    __delattr__ = _disallow_modification
