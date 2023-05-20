"""
real-time balance aggregation
"""
import uuid

from sqlalchemy.orm import Session

from models.models import Transaction, FundsOnHold


def aggregate(db: Session, user_uuid: uuid.UUID) -> int:
    """
    Aggregate all transactions and holds-transactions for user
    :param db: Session object
    :param user_uuid: uuid of target
    :return: actual balance
    """
    balance = int()
    transactions_list = db.query(Transaction).filter(Transaction.user_uuid == str(user_uuid)).all()
    holds_list = db.query(FundsOnHold).filter(FundsOnHold.user_uuid == str(user_uuid)).all()

    transactions = list(map(lambda x: x.as_dict, transactions_list)) + list(map(lambda x: x.as_dict, holds_list))

    for trans in transactions:
        balance += trans['cost']

    return balance
