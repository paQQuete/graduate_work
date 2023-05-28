import datetime
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from services import balance_check, subscribe, transactions_cr
from models.schemas.subscription import GrantedAccess, GrantedAccessCreate, GrantedFilm
from models.schemas.fund_holds import HoldFundsCreate, HoldFunds
from models.schemas.transaction import TransactionCreate

router = APIRouter()


@router.post('/buy/from_balance', response_model=GrantedAccess)
def buy_from_balance(grant_query: GrantedAccessCreate, db: Session = Depends(get_db)):
    price, charge_type = subscribe.fetch_price(db=db, subscribe_id=grant_query.subscription_id)

    if balance_check.aggregate(db=db, user_uuid=grant_query.user_uuid) >= price:
        hold_funds = transactions_cr.create_hold(
            db=db, hold_funds=HoldFundsCreate(
                user_uuid=grant_query.user_uuid,
                type='spending',
                cost=price,
                timestamp=datetime.datetime.now()
            ))
        try:
            grant = subscribe.grant_access(db=db, grant_access=grant_query)
        except:
            transactions_cr.delete_hold(db=db, hold_uuid=hold_funds.uuid)
            raise HTTPException(status_code=500, detail="Purchase not completed")
        else:
            transactions_cr.create_transaction(db=db, transaction=TransactionCreate(
                user_uuid=grant_query.user_uuid,
                type='spending',
                cost=price,
                timestamp=datetime.datetime.now()
            ))
            transactions_cr.delete_hold(db=db, hold_uuid=hold_funds.uuid)
            return grant
    else:
        raise HTTPException(status_code=406, detail="Refund is not available")


@router.get('/check/{movie_uuid}/{user_uuid}')
def check_movie_available_for_user(user_uuid: uuid.UUID, movie_uuid: uuid.UUID,db: Session = Depends(get_db)):
    return subscribe.read_movie_access(db=db, user_uuid=user_uuid, movie_uuid=movie_uuid)



