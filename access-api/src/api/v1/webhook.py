import datetime

import stripe
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session

from db.database import get_db
from core.config import SETTINGS
from services import subscribe, transactions_cr
from models.schemas.subscription import SimpleGrantAccessCreate
from models.schemas.transaction import TransactionCreate

router = APIRouter()


@router.post('/')
async def webhook_success_payment(data: Request, stripe_signature: str = Header(None), db: Session = Depends(get_db)):
    data = await data.body()
    data_str = data.decode()
    try:
        event = stripe.Webhook.construct_event(
            data_str, stripe_signature, SETTINGS.STRIPE.STRIPE__WEBHOOK_SECRET
        )
        match event["type"]:
            case 'checkout.session.completed':
                checkout_type, value1, value2 = event['data']['object']['client_reference_id'].split('_')

                match checkout_type:
                    case 'buy':
                        subscribe_id, user_uuid = value1, value2
                        for trans_type in ('topup', 'spending'):
                            transactions_cr.create_transaction(db=db, transaction=TransactionCreate(
                                user_uuid=user_uuid,
                                type=trans_type,
                                cost=event['data']['object']['amount_total'],
                                timestamp=datetime.datetime.now()
                            ))
                        subscribe.grant_access(db=db, grant_access=SimpleGrantAccessCreate(
                            user_uuid=user_uuid,
                            subscribe_id=subscribe_id
                        ))

                    case 'topup':
                        user_id, amount = value1, value2
                        transactions_cr.create_transaction(db=db, transaction=TransactionCreate(
                            user_uuid=user_id,
                            type='topup',
                            cost=amount,
                            timestamp=datetime.datetime.now()
                        ))

    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    return {"msg": "success"}
