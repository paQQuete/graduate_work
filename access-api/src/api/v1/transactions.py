import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.schemas.transaction import TransactionCreate, Transaction
from models.models import HTTPErrorDetails
from db.database import get_db
from services import transactions_cr

router = APIRouter()


@router.post('/', response_model=Transaction)
async def create_trans(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Manually adding a transaction for a user. Do not use directly, only for debugging purposes"""
    try:
        return await transactions_cr.create_transaction(db=db, transaction=transaction)
    finally:
        db.commit()


@router.get('/{user_uuid}/pagination', response_model=list[Transaction])
async def read_trans_by_user_pagination(user_uuid: uuid.UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all user transactions with pagination"""
    result = await transactions_cr.read_by_user(db=db, user_uuid=user_uuid, skip=skip, limit=limit)
    if result:
        return result
    else:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=HTTPErrorDetails.NOT_FOUND.value)


@router.get('/{user_uuid}', response_model=list[Transaction])
async def read_trans_by_user_all(user_uuid: uuid.UUID, db: Session = Depends(get_db)):
    """List all user transactions without pagination"""
    result = await transactions_cr.read_all_by_user(db=db, user_uuid=user_uuid)
    if result:
        return result
    else:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=HTTPErrorDetails.NOT_FOUND.value)



