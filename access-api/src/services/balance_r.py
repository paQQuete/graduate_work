import uuid

from sqlalchemy.orm import Session

from models import models, schemas


def read_user_balance(db: Session, user_uuid: uuid.UUID):
    """
    Return balance of user
    :param db: sqlalchemy.orm.Session instance
    :param user_uuid: uuid of user
    :return: ORM object
    """
    return db.query(models.Balance).filter(models.Balance.user_uuid == str(user_uuid)).one()