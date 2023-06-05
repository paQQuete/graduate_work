import datetime
import uuid
from http import HTTPStatus

from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.models import Subscription, GrantedFilms, GrantedAccess
from models.schemas.subscription import SimpleGrantAccessCreate


def fetch_price(db: Session, subscribe_id: uuid.UUID):
    output = db.query(Subscription).filter(Subscription.id == subscribe_id).one()
    return output.all_time_cost


def get_price_id(db: Session, subscribe_id: uuid.UUID) -> str:
    """
    Function return Price ID of Product ID (this is subscription plan on Stripe side) from database.
    There is only one for each subscription.
    :param db:
    :param subscribe_id:
    :return: Price ID string
    """
    return db.query(Subscription).filter(Subscription.id == subscribe_id).one().payment_gw_price_id


async def grant_access(db: Session, grant_create: SimpleGrantAccessCreate):
    """
    Grant access to subscription plan
    :param db:
    :param grant_create:
    :return: ORM object
    """
    subscription = db.query(Subscription).filter(Subscription.id == grant_create.subscription_id).one()

    db_grant = GrantedAccess(
        uuid=uuid.uuid4(),
        user_uuid=grant_create.user_uuid,
        subscription_id=grant_create.subscription_id,
        granted_at=datetime.datetime.now(),
        available_until=datetime.datetime.now() + datetime.timedelta(days=subscription.duration),
        is_active=True,
        cost_per_day=subscription.cost
    )
    db.add(db_grant)
    for film in subscription.filmworks:
        grant_film = GrantedFilms(
            movie_uuid=film.id, user_uuid=db_grant.user_uuid, granted_at=db_grant.granted_at,
            grant_uuid=db_grant.uuid, uuid=uuid.uuid4(), is_active=True
        )
        db_grant.films.append(grant_film)
        db.add(grant_film)

    db.flush()
    return db_grant


async def read_movie_access(db: Session, user_uuid: uuid.UUID, movie_uuid: uuid.UUID) -> bool:
    """
    Check movie available for user
    :param db: sqlalchemy.orm.Session instance
    :param user_uuid: user uuid
    :return: yes or not
    """
    query = db.query(GrantedFilms).filter(
        GrantedFilms.movie_uuid == movie_uuid, GrantedFilms.user_uuid == user_uuid, GrantedFilms.is_active == True
    ).all()
    if not query:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Movie is not available for this user')
    else:
        return True


async def check_active_days_left(db: Session, grant_access_id: uuid.UUID):
    end_date = db.query(GrantedAccess).filter(GrantedAccess.uuid == grant_access_id).one().available_until
    delta = end_date - datetime.datetime.now()
    return delta.days


async def get_refund_amount_subscribe(db: Session, grant_access_id: uuid.UUID, days: int):
    subscription_id = db.query(GrantedAccess).filter(GrantedAccess.uuid == grant_access_id).one().subscription_id
    price_per_day = db.query(Subscription).filter(Subscription.id == subscription_id).one().cost
    return price_per_day * days