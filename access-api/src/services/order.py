import uuid

from sqlalchemy.orm import Session

from models.models import TransactionOrder


async def set_order(db: Session, **kwargs):
    db_order = TransactionOrder(**kwargs)
    db.add(db_order)
    db.flush()
    return db_order


async def update_order(db: Session, order_id: uuid.UUID, topup_id: uuid.UUID = None, refund_id: uuid.UUID = None):
    db_order = db.query(TransactionOrder).filter(TransactionOrder.uuid == order_id).update(
        {'topup_transaction': topup_id, 'refund_transaction': refund_id}
    )
    db.flush()
    return db_order

