import datetime
import uuid
from http import HTTPStatus

import stripe
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from services import balance_check, subscribe, transactions_cr
from models.models import GrantedAccess, Transaction, TransactionOrder, HTTPErrorDetails
from models.schemas.transaction import TransactionCreate
from models.schemas.transaction import Transaction as TransactionSchema
from models.schemas.fund_holds import HoldFundsCreate

router = APIRouter()


@router.post('/request')
async def refund_availability(user_uuid: uuid.UUID, amount: int, db: Session = Depends(get_db)):
    """Checks the availability of refunding the amount from the balance. Should be deprecated"""
    if await balance_check.aggregate(db=db, user_uuid=user_uuid) >= amount:
        return {'message': 'Refund available'}
    else:
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail=HTTPErrorDetails.NOT_ACCEPTABLE.value)


@router.get('/grant/{grant_id}/')
async def refund_subscribe(grant_id: uuid.UUID, db: Session = Depends(get_db)):
    """Refunds for unused days of a purchased subscription, using Stripe"""
    amount = await subscribe.get_refund_amount_subscribe(
        db=db, grant_access_id=grant_id, days=await subscribe.check_active_days_left(
            db=db, grant_access_id=grant_id
        ))
    if amount <= 0:
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail=HTTPErrorDetails.NOT_ACCEPTABLE.value)

    grant = db.query(GrantedAccess).filter(GrantedAccess.uuid == grant_id).one()
    hold = await transactions_cr.create_hold(db=db, hold_funds=HoldFundsCreate(
        user_uuid=grant.user_uuid,
        type='refund',
        cost=amount * -1,
        timestamp=datetime.datetime.now()
    ))
    try:
        refund = stripe.Refund.create(
            payment_intent=grant.order[0].payment_intent_id,
            amount=amount * 100,
            reason='requested_by_customer'
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        db.query(GrantedAccess).filter(GrantedAccess.uuid == grant_id).update({
            'available_until': datetime.datetime.now(),
            'is_active': False
        })

        for film in db.query(GrantedAccess).filter(GrantedAccess.uuid == grant_id).one().films:
            film.is_active = False

        ref_newtrans = await transactions_cr.create_transaction(db=db, transaction=TransactionCreate(
            user_uuid=grant.user_uuid,
            type='refund',
            cost=amount * -1,
            timestamp=datetime.datetime.now()
        ))
        db.query(TransactionOrder).filter(TransactionOrder.granted_access_id == grant_id).update(
            {'refund_transaction': ref_newtrans.uuid}
        )
    finally:
        await transactions_cr.delete_hold(db=db, hold_uuid=hold.uuid)
    db.commit()

    return refund.to_dict()['status']


@router.get('/transaction/{transaction_id}')
async def refund_transaction(transaction_id: uuid.UUID, db: Session = Depends(get_db)):
    """Refund of a specific transaction, checking if the current balance is enough to refund"""
    transaction = db.query(Transaction).filter(Transaction.uuid == transaction_id).one()
    if transaction.type.value != 'topup':
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail=HTTPErrorDetails.UNPROCESSABLE_ENTITY.value)
    if await balance_check.aggregate(db=db, user_uuid=transaction.user_uuid) < transaction.cost:
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail=HTTPErrorDetails.NOT_ACCEPTABLE.value)

    hold = await transactions_cr.create_hold(db=db, hold_funds=HoldFundsCreate(
        user_uuid=transaction.user_uuid,
        type='refund',
        cost=transaction.cost * -1,
        timestamp=datetime.datetime.now()
    ))

    try:
        refund = stripe.Refund.create(
            payment_intent=transaction.topup_order[0].payment_intent_id,
            amount=transaction.cost * 100,
            reason='requested_by_customer'
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        ref_newtrans_id = uuid.uuid4()
        await transactions_cr.create_transaction(db=db, transaction=TransactionSchema(
            uuid=ref_newtrans_id,
            user_uuid=transaction.user_uuid,
            type='refund',
            cost=transaction.cost * -1,
            timestamp=datetime.datetime.now(),
            created_at=datetime.datetime.now()
        ))
        db.query(TransactionOrder).filter(TransactionOrder.uuid == transaction.topup_order[0].uuid).update(
            {'refund_transaction': ref_newtrans_id}
        )
    finally:
        await transactions_cr.delete_hold(db=db, hold_uuid=hold.uuid)
    db.commit()

    return refund.to_dict()['status']
