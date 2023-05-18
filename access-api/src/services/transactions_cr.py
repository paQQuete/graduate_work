import uuid

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from models import models, schemas


# TODO: определить все допустимые операции записи и чтения для транзакций тут!


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
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
    # db_trans.type = db_trans.type.name
    return db_trans


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
