import datetime
import uuid
from copy import deepcopy
from http import HTTPStatus

import stripe
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session

from db.database import get_db
from core.config import SETTINGS
from services import subscribe, transactions_cr, order
from models.schemas.subscription import SimpleGrantAccessCreate
from models.schemas.transaction import TransactionCreate, Transaction

router = APIRouter()


@router.post('/')
async def webhook_success_payment(data: Request, stripe_signature: str = Header(None), db: Session = Depends(get_db)):
    data = await data.body()
    data_str = data.decode()
    try:
        event = stripe.Webhook.construct_event(
            data_str, stripe_signature, SETTINGS.STRIPE.STRIPE__WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid payload")
    else:
        if event["type"] == 'checkout.session.completed':
            checkout_type, value1, value2 = event['data']['object']['client_reference_id'].split('_')
            if checkout_type == 'buy':
                subscribe_id, user_uuid = value1, value2
                cost = event['data']['object']['amount_total'] / 100
                grant = await subscribe.grant_access(db=db, grant_create=SimpleGrantAccessCreate(
                    user_uuid=user_uuid,
                    subscription_id=subscribe_id
                ))
                for trans_type in ('topup', 'spending'):
                    transaction = await transactions_cr.create_transaction(db=db, transaction=Transaction(
                        uuid=uuid.uuid4(),
                        user_uuid=user_uuid,
                        type=trans_type,
                        cost=cost if trans_type == 'topup' else cost * -1,
                        timestamp=datetime.datetime.now(),
                        created_at=datetime.datetime.now()
                    ))
                    if trans_type == 'topup':
                        topup_trans = deepcopy(transaction)
            elif checkout_type == 'topup':
                user_uuid, amount = value1, value2
                topup_trans = await transactions_cr.create_transaction(db=db, transaction=Transaction(
                    uuid=uuid.uuid4(),
                    user_uuid=user_uuid,
                    type='topup',
                    cost=amount,
                    timestamp=datetime.datetime.now(),
                    created_at=datetime.datetime.now()
                ))
                grant = None

            await order.set_order(db=db,
                                  user_uuid=user_uuid,
                                  checkout_session_id=event['data']['object']['id'],
                                  payment_intent_id=event['data']['object']['payment_intent'],
                                  topup_transaction=topup_trans.uuid,
                                  granted_access_id=grant.uuid if grant else None
                                  )
            db.commit()

    return {"msg": "success"}
