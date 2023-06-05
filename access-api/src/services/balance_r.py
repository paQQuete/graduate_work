import uuid

from sqlalchemy.orm import Session

from models import models


async def read_user_balance(db: Session, user_uuid: uuid.UUID):
    """
    Return balance of user. It may not be relevant, because taken from already aggregated data.
    To more accurately determine the balance, you need to aggregate all user transactions)
    :param db: sqlalchemy.orm.Session instance
    :param user_uuid: uuid of user
    :return: ORM object
    """
    return db.query(models.Balance).filter(models.Balance.user_uuid == str(user_uuid)).one()