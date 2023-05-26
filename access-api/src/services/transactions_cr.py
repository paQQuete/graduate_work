import uuid

from sqlalchemy.orm import Session

from models import models
from models.schemas.transaction import TransactionCreate
from models.schemas.fund_holds import HoldFundsCreate


def create_transaction(db: Session, transaction: TransactionCreate):
    '''
    Create one transaction
    :param db: sqlalchemy.orm.Session instance
    :param transaction: pydantic model with data
    :return: ORM object
    '''
    db_trans = models.Transaction(**transaction.dict())
    db.add(db_trans)
    db.commit()
    db.refresh(db_trans)
    return db_trans


def create_hold(db: Session, hold_funds: HoldFundsCreate):
    """
    Create hold transaction
    :param db:
    :param hold_funds: pydantic model with data
    :return:
    """
    db_hold = models.FundsOnHold(**hold_funds.dict())
    db.add(db_hold)
    db.commit()
    db.refresh(db_hold)
    return db_hold


def delete_hold(db: Session, hold_uuid: uuid.UUID):
    db.query(models.FundsOnHold).filter(models.FundsOnHold.uuid == hold_uuid).delete()
    db.commit()


def read_all_by_user(db: Session, user_uuid: uuid.UUID):
    '''
    Fetch all transactions by user_uuid
    :param db: db: sqlalchemy.orm.Session instance
    :param user_uuid: user uuid
    :return: ORM object
    '''
    return db.query(models.Transaction).filter(models.Transaction.user_uuid == str(user_uuid)).all()


def read_by_user(db: Session, user_uuid: uuid.UUID, skip: int, limit: int = 50):
    '''
    Fetch transactions by user_uuid with offset and limit
    :param db: sqlalchemy.orm.Session instance
    :param user_uuid: user uuid
    :param skip: offset
    :param limit: limit of rows
    :return: ORM object
    '''
    return db.query(models.Transaction).filter(models.Transaction.user_uuid == str(user_uuid)). \
        offset(skip).limit(limit).all()
