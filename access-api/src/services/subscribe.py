import uuid

from sqlalchemy.orm import Session

from models.models import Subscription, GrantedFilms, GrantedAccess
from models.schemas.subscription import GrantedAccessCreate


def fetch_price(db: Session, subscribe_id: uuid.UUID) -> tuple[int, str]:
    output = db.query(Subscription).filter(Subscription.id == subscribe_id).one()
    return output.cost, output.charge_type


def grant_access(db: Session, grant_access: GrantedAccessCreate):
    subscription = db.query(Subscription).filter(Subscription.id == grant_access.subscription_id).one()
    db_grant = GrantedAccess(uuid=uuid.uuid4() ,**grant_access.dict())
    db.add(db_grant)
    for film in subscription.filmworks:
        film = film.as_dict
        grant_film = GrantedFilms(
            movie_uuid=film['id'], granted_at=db_grant.granted_at, grant_uuid=db_grant.uuid, uuid=uuid.uuid4()
        )
        db_grant.films.append(grant_film)
        db.add(grant_film)

    db.commit()
    db.refresh(db_grant)
    return db_grant