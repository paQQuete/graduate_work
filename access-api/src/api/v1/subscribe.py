import datetime
import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from db.database import get_db
from services import balance_check, subscribe, transactions_cr
from models.models import HTTPErrorDetails
from models.schemas.subscription import GrantedAccess, SimpleGrantAccessCreate
from models.schemas.fund_holds import HoldFundsCreate
from models.schemas.transaction import TransactionCreate

router = APIRouter()


@router.post('/buy/from_balance', response_model=GrantedAccess)
async def buy_from_balance(grant_query: SimpleGrantAccessCreate, db: Session = Depends(get_db)):
    """Purchasing a subscription using the free funds of the user account"""
    price = subscribe.fetch_price(db=db, subscribe_id=grant_query.subscription_id)

    if await balance_check.aggregate(db=db, user_uuid=grant_query.user_uuid) >= price:
        hold_funds = await transactions_cr.create_hold(
            db=db, hold_funds=HoldFundsCreate(
                user_uuid=grant_query.user_uuid,
                type='spending',
                cost=price,
                timestamp=datetime.datetime.now()
            ))
        try:
            grant = subscribe.grant_access(db=db, grant_create=grant_query)

        except NoResultFound:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail=HTTPErrorDetails.NOT_FOUND.value)

        else:
            await transactions_cr.create_transaction(db=db, transaction=TransactionCreate(
                user_uuid=grant_query.user_uuid,
                type='spending',
                cost=price,
                timestamp=datetime.datetime.now()
            ))
            return grant
        finally:
            await transactions_cr.delete_hold(db=db, hold_uuid=hold_funds.uuid)
            db.commit()

    else:
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail=HTTPErrorDetails.NOT_ACCEPTABLE.value)


@router.get('/check/{movie_uuid}/{user_uuid}')
async def check_movie_available_for_user(user_uuid: uuid.UUID, movie_uuid: uuid.UUID, db: Session = Depends(get_db)):
    """Checking if a movie is available to a user"""
    return await subscribe.read_movie_access(db=db, user_uuid=user_uuid, movie_uuid=movie_uuid)
