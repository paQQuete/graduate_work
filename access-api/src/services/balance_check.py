"""
real-time balance aggregation
"""
import uuid
from itertools import chain

from sqlalchemy.orm import Session

from models.models import Transaction, FundsOnHold


async def aggregate(db: Session, user_uuid: uuid.UUID) -> int:
    """
    Aggregate all transactions and holds-transactions for user
    :param db: Session object
    :param user_uuid: uuid of target
    :return: actual balance
    """
    def transactions_generator():
        transactions_query = db.query(Transaction).filter(Transaction.user_uuid == str(user_uuid)).yield_per(200)
        holds_query = db.query(FundsOnHold).filter(FundsOnHold.user_uuid == str(user_uuid)).yield_per(200)

        for transaction in chain(transactions_query, holds_query):
            yield transaction.as_dict

    balance = sum(trans['cost'] for trans in transactions_generator())

    return balance
